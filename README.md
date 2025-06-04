# 🚗 Hệ thống Nhận diện Biển số Xe trong Bãi đỗ Xe Thông minh

## 📌 Giới thiệu

Dự án này là bài tập lớn của học phần **Công nghệ Xử lý Ảnh**, với mục tiêu xây dựng một hệ thống nhận diện biển số xe tự động trong bãi đỗ xe thông minh. Hệ thống sử dụng mô hình YOLOv8 để phát hiện và nhận diện biển số xe từ camera, kết hợp với giao diện web để quản lý và hiển thị thông tin.


Dự án áp dụng các công nghệ như:
- Python + OpenCV
- YOLO + OCR
- Flask Web Interface
- HTML

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
<img src="https://github.com/hoangtit123/BTL_XLA/blob/main/a%CC%89nh%20btl/sodocoche.jpg" alt="Sơ đồ hoạt động" width="400"/>



## 🖥️ Giao diện trang chủ

<img src="https://github.com/hoangtit123/BTL_XLA/blob/main/a%CC%89nh%20btl/a%CC%89nh%201.png" alt="Giao diện trang chủ" width="400"/>

### 🟢 Giao diện cổng vào

<img src="https://github.com/hoangtit123/BTL_XLA/blob/main/a%CC%89nh%20btl/a%CC%89nh%202.png" alt="Giao diện cổng vào" width="400"/>

### 🔴 Giao diện cổng ra

<img src="https://github.com/hoangtit123/BTL_XLA/blob/main/a%CC%89nh%20btl/a%CC%89nh%203.jpg" alt="Giao diện cổng ra" width="400"/>

### 📋 Giao diện lịch sử ra – vào

<img src="https://github.com/hoangtit123/BTL_XLA/blob/main/a%CC%89nh%20btl/a%CC%89nh%204.png" alt="Giao diện lịch sử ra - vào" width="400"/>

---
## ⚠️ Các tình huống lỗi và cách hệ thống xử lý
### ❌ Trường hợp quét biển số **2 lần tại cổng vào**
- Hiển thị: **"Xe đã vào bãi"**
- Không ghi log lại → đảm bảo dữ liệu không trùng lặp.

<img src="https://github.com/hoangtit123/BTL_XLA/blob/main/a%CC%89nh%20btl/a%CC%89nh%205%20ba%CC%81o%20l%C3%B4%CC%83i.jpg" alt="Lỗi vào 2 lần" width="400"/>

### ❌ Trường hợp quét ở cổng ra nhưng **chưa từng vào hoặc quét 2 lần**
- Hiển thị: **"Xe chưa vào bãi/xe đã ghi nhận ra rồi"**
- Không thực hiện bất kỳ thao tác ghi log hay tính tiền.

<img src="https://github.com/hoangtit123/BTL_XLA/blob/main/a%CC%89nh%20btl/a%CC%89nh%206%20ba%CC%81o%20l%C3%B4%CC%83i.jpg" alt="Lỗi ra khi chưa vào" width="400"/>






