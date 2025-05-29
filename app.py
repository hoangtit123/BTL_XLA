from flask import Flask, render_template, request, send_from_directory, jsonify, redirect, url_for, send_file
from ultralytics import YOLO
import cv2
import uuid
import os
import csv
from datetime import datetime
from math import ceil
import numpy as np
import easyocr
import base64
import io
from PIL import Image
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DASHBOARD_FOLDER'] = 'static/plates'
app.config['CSV_LOG'] = 'data/log.csv'

# Tạo thư mục nếu chưa có
for folder in ['uploads', 'static/plates', 'data', 'temp']:
    os.makedirs(folder, exist_ok=True)

# Model YOLO và OCR
model = YOLO('weights/best.pt')
ocr = easyocr.Reader(['en', 'vi'], gpu=False)

# Lịch sử xe
plate_history = {}
if os.path.exists(app.config['CSV_LOG']):
    with open(app.config['CSV_LOG'], newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) < 4:
                continue
            plate = row[2].strip().upper()
            if plate not in plate_history:
                plate_history[plate] = {'in': row[1], 'out': None}
            if row[3] == "Ra":
                plate_history[plate]['out'] = row[1]

def normalize_plate(text):
    return text.upper().replace(" ", "").replace("-", "").replace(".", "").replace("O", "0")

def calculate_fee(entry_time_str, exit_time_str):
    fmt = "%Y-%m-%d %H:%M:%S"
    entry = datetime.strptime(entry_time_str, fmt)
    exit = datetime.strptime(exit_time_str, fmt)
    duration = exit - entry
    hours = ceil(duration.total_seconds() / 3600)
    return hours, str(duration).split(".")[0], hours * 5000

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    image_data = []
    if os.path.exists(app.config['CSV_LOG']):
        with open(app.config['CSV_LOG'], newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 4:
                    image_data.append((row[0], row[1], row[2], row[3]))
    image_data.reverse()
    return render_template(
        'dashboard.html',
        image_data=image_data,
        plate_history=plate_history,
        datetime=datetime
    )

@app.route('/dashboard_img/<filename>')
def dashboard_image(filename):
    return send_from_directory(app.config['DASHBOARD_FOLDER'], filename)

@app.route('/capture/in')
def capture_in():
    return render_template('capture.html', gate='in')

@app.route('/capture/out')
def capture_out():
    return render_template('capture.html', gate='out')

@app.route('/capture', methods=['POST'])
def capture():
    image_data = request.form.get('imageData')
    gate = request.form.get('gate')
    if not image_data or gate not in ['in', 'out']:
        return render_template('result.html', msg="❌ Không nhận được ảnh hoặc thiếu loại cổng", gate=gate)

    header, encoded = image_data.split(",", 1)
    img_bytes = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(img_bytes))
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    temp_filename = f"webcam_{uuid.uuid4().hex[:8]}.jpg"
    temp_path = os.path.join("temp", temp_filename)
    cv2.imwrite(temp_path, frame)

    results = model(temp_path)
    os.remove(temp_path)

    if not results or results[0].boxes is None:
        return render_template("result.html", msg="❌ Không phát hiện được biển số", gate=gate)

    h, w = frame.shape[:2]
    padding = 20

    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        x1_crop = max(0, x1 - padding)
        x2_crop = min(w, x2 + padding)
        y1_crop = max(0, y1 - padding)
        y2_crop = min(h, y2 + padding)
        plate_img = frame[y1_crop:y2_crop, x1_crop:x2_crop]

        gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        ocr_results = ocr.readtext(thresh)
        text_parts = [text.strip() for _, text, conf in ocr_results if conf > 0.5]

        if not text_parts:
            continue

        full_text = normalize_plate("".join(text_parts))
        if len(full_text) < 5:
            continue

        final_filename = f"{uuid.uuid4().hex[:8]}_{full_text}.jpg"
        save_path = os.path.join(app.config['DASHBOARD_FOLDER'], final_filename)
        cv2.rectangle(frame, (x1_crop, y1_crop), (x2_crop, y2_crop), (0, 255, 0), 2)
        cv2.putText(frame, full_text, (x1_crop, y1_crop - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.imwrite(save_path, frame)

        if gate == 'in':
            if full_text in plate_history and plate_history[full_text]['out'] is None:
                return render_template("result.html", msg=f"⚠️ Biển số {full_text} đã tồn tại trong hệ thống!", gate=gate)
            plate_history[full_text] = {'in': timestamp, 'out': None}
            with open(app.config['CSV_LOG'], 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([final_filename, timestamp, full_text, "Vào"])
            return redirect(url_for("dashboard"))

        if gate == 'out':
            if full_text not in plate_history:
                return render_template("result.html", msg=f"❌ Biển số {full_text} chưa được ghi nhận vào – không hợp lệ!", gate=gate)
            if plate_history[full_text]['out'] is not None:
                return render_template("result.html", msg=f"⚠️ Biển số {full_text} đã được ghi nhận ra rồi!", gate=gate)

            in_time = plate_history[full_text]['in']
            out_time = timestamp
            plate_history[full_text]['out'] = out_time

            hours, duration_str, fee = calculate_fee(in_time, out_time)

            with open(app.config['CSV_LOG'], 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([final_filename, out_time, full_text, "Ra"])

            return render_template("result.html",
                                   filename=final_filename,
                                   plate=full_text,
                                   time=out_time,
                                   note="Ra",
                                   gate=gate,
                                   msg=f"✅ Xe đã ra lúc {out_time} (vào lúc {in_time})",
                                   duration=duration_str,
                                   fee=fee)

    return render_template("result.html", msg="❌ Không đọc được biển số hợp lệ", gate=gate)

@app.route('/invoice/<plate>')
def generate_invoice(plate):
    if plate not in plate_history or plate_history[plate]['in'] is None or plate_history[plate]['out'] is None:
        return "Không thể tạo hóa đơn cho biển số này.", 400

    in_time = plate_history[plate]['in']
    out_time = plate_history[plate]['out']
    hours, duration_str, fee = calculate_fee(in_time, out_time)

    file_path = f"temp/invoice_{plate}.pdf"
    c = canvas.Canvas(file_path, pagesize=(400, 600))

    # Logo
    logo_path = "static/img/DAINAM_Logo.png"
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 150, 510, width=100, height=100)

    # Tiêu đề
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0.1, 0.3, 0.6)
    c.drawCentredString(200, 490, "HÓA ĐƠN GỬI XE")

    c.setFont("Helvetica", 12)
    y = 450
    for text in [
        f"Biển số: {plate}",
        f"Vào: {in_time}",
        f"Ra: {out_time}",
        f"Tổng thời gian: {duration_str}",
        f"Tổng tiền: {fee:,.0f} đ"
    ]:
        c.drawString(50, y, text)
        y -= 24

    c.setFont("Helvetica-Oblique", 10)
    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.drawCentredString(200, 60, "Cảm ơn quý khách đã sử dụng bãi xe Đại Nam!")
    c.save()

    return send_file(file_path, as_attachment=True)

@app.route('/get-latest-plate')
def get_latest_plate():
    if not os.path.exists(app.config['CSV_LOG']):
        return jsonify({"plate": "Chưa có", "time": "", "note": ""})
    with open(app.config['CSV_LOG'], newline='', encoding='utf-8') as f:
        reader = list(csv.reader(f))
        if len(reader) <= 1:
            return jsonify({"plate": "Chưa có", "time": "", "note": ""})
        row = reader[-1]
        return jsonify({"plate": row[2], "time": row[1], "note": row[3]})

if __name__ == '__main__':
    app.run(debug=True)
