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




## 📁 Cấu trúc hệ thống (có thể cập nhật thêm)

