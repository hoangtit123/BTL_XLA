# BTL_XLA
Tên Project: CNXLA-15-02 Mô tả: Bài tập lớn học phần Công nghệ xử lý ảnh - Lớp CNTT 15-02  - Khoa Công nghệ thông tin - Đại học Đại Nam
# 🚗 XỬ LÝ HÌNH ẢNH ĐỌC BIỂN SỐ XE TRONG HỆ THỐNG BÃI ĐỖ XE THÔNG MINH
## 👨‍💻 Người thực hiện: Nguyễn Việt Hoàng 
- MSV 1571020108
- Lớp CNTT 15-04 Đại học Đại Nam
- Bộ môn: Xử lý ảnh – Kỹ thuật phần mềm
- Dự án thực hiện năm 2025

## 📝 Giới thiệu
Đây là một hệ thống quản lý bãi đỗ xe thông minh, sử dụng **xử lý ảnh** và **nhận dạng biển số xe** để ghi nhận lượt vào – ra, tính phí và xuất hóa đơn tự động.

Dự án áp dụng các công nghệ như:
- Python + OpenCV
- YOLO + OCR
- Flask Web Interface
- Giao tiếp phần cứng (ESP32, RFID, Servo)

---

## ⚙️ Cơ chế hoạt động

### ✅ Trang chủ
Người dùng chọn:
- **Quét cổng vào**
- **Quét cổng ra**

> Hệ thống sẽ bật webcam và tự động xử lý ảnh biển số.

---

### 🚪 **Cổng vào**
- Nếu **biển số mới** → ghi log giờ vào.
- Nếu **biển số đã tồn tại** → báo lỗi **“Xe đã vào”**.

### 🚪 **Cổng ra**
- Nếu **biển số đã vào** → tính giờ, tính phí, ghi log, hiển thị hóa đơn.
- Nếu **xe đã ra trước đó** → báo lỗi **“Xe đã ra”**.
- Nếu **chưa từng vào** → báo lỗi **“Xe chưa vào”**.

---

## 📊 Chức năng sau khi quét

- Hiển thị biển số nhận diện được
- Hiển thị **giờ vào/ra**, **ảnh biển số**
- Tính toán **phí gửi xe**
- Dashboard quản lý và **xuất hóa đơn PDF**

---

## 🔎 Chức năng nâng cao

- **Lọc biển số** theo từ khoá
- Tra cứu **lịch sử ra vào**
- Thống kê thời gian gửi và số tiền đã thanh toán

---
## 🔄 Sơ đồ cơ chế hoạt động

<img src="images/flowchart.png" alt="Sơ đồ hoạt động" width="700"/>


## 📁 Cấu trúc hệ thống (có thể cập nhật thêm)

