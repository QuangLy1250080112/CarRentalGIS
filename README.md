# Car Rental GIS - Hệ thống Quản lý và Thuê xe Trực tuyến

Ứng dụng quản lý cho thuê xe tích hợp hệ thống GIS (Địa lý thông tin) sử dụng Django, PostgreSQL với PostGIS.

## 🌟 Tính Năng Chính

- **Quản lý Xe**: Thêm, sửa, xóa thông tin xe với hình ảnh chi tiết
- **Hệ thống GIS**: Quản lý vị trí xe, trạm và các vùng an toàn sử dụng bản đồ Leaflet
- **Đặt Xe**: Khách hàng có thể đặt xe trực tuyến với lựa chọn điểm nhận/trả
- **Lịch Sử Đặt Xe**: Theo dõi toàn bộ lịch sử đặt xe, khoảng cách, phí dịch vụ
- **Đánh Giá & Nhận Xét**: Khách hàng có thể đánh giá xe cùng với hình ảnh
- **Quản lý Trạm**: Quản lý các trạm nhận/trả xe với hình vùng phục vụ
- **Tin Tức**: Quản lý tin tức cho trang chủ
- **Thống Kê Doanh Thu**: Báo cáo tổng hợp doanh thu theo thời gian
- **Xác Thực Email**: Xác minh email khi đăng ký tài khoản
- **Giao Diện Quản Trị**: Dashboard cho admin quản lý hệ thống

## 🛠️ Công Nghệ Sử Dụng

- **Backend**: Django 6.0.2 (Python Web Framework)
- **Database**: PostgreSQL 12+ với PostGIS (Geospatial Extension)
- **Frontend**: HTML, CSS, JavaScript, Leaflet.js (Bản đồ GIS)
- **Image Processing**: Pillow
- **Email**: SMTP (Mailtrap)
- **Geolocation**: GeoPy, GeographicLib
- **Excel Export**: OpenpyXL
- **ORM**: Django ORM

## 📋 Yêu Cầu Hệ Thống

### Bắt Buộc:
- **Python**: 3.10 hoặc cao hơn
- **PostgreSQL**: 12 hoặc cao hơn
- **PostGIS**: 3.0 hoặc cao hơn (Extension của PostgreSQL)
- **OSGeo4W** (Windows): Cung cấp các thư viện GIS cần thiết

### Tùy Chọn:
- **pip** hoặc **Poetry** (quản lý package Python)
- **Git** (quản lý code)

## 🚀 Hướng Dẫn Cài Đặt

### 1. Cài Đặt PostgreSQL với PostGIS

#### Trên Windows:
a) Tải PostgreSQL từ: https://www.postgresql.org/download/windows/
   - Chọn phiên bản 12 hoặc cao hơn
   - Ghi nhớ mật khẩu superuser (mặc định: postgres)

b) Tải PostGIS Extension:
   - Mở pgAdmin 4 (tương ứng với PostgreSQL)
   - Kết nối với server mặc định
   - Chạy SQL Script để cài đặt PostGIS:
   ```sql
   CREATE EXTENSION IF NOT EXISTS postgis;
   CREATE EXTENSION IF NOT EXISTS postgis_topology;
   ```

c) Tải OSGeo4W từ: https://trac.osgeo.org/osgeo4w/
   - Chọn Express Desktop Install
   - Chọn GDAL, GEOS, PROJ (các thư viện GIS cần thiết)
   - Ghi nhớ đường dẫn cài đặt (mặc định: D:\OSGeo4W)

#### Trên Linux (Ubuntu/Debian):
```bash
# Cài đặt PostgreSQL
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib postgis postgresql-12-postgis

# Khởi động PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Cài đặt GDAL, GEOS
sudo apt-get install gdal-bin libgdal-dev libgeos-dev
```

### 2. Tạo Database

Kết nối với PostgreSQL và chạy:
```sql
-- Tạo database mới
CREATE DATABASE car_rental_gis;

-- Kết nối vào database
\c car_rental_gis

-- Cài đặt PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
```

**Lưu ý**: Cập nhật tên database và credentials trong file `core/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'car_rental_gis',      # Tên database
        'USER': 'postgres',             # Username PostgreSQL
        'PASSWORD': '123',              # Mật khẩu
        'HOST': 'localhost',            # Host
        'PORT': '5432',                 # Port mặc định
    }
}
```

### 3. Cài Đặt Python Environment

#### a) Clone hoặc Tải Project
```bash
cd C:\path\to\CarRentalGIS
# hoặc nếu dùng Git:
git clone <repository-url>
cd CarRentalGIS
```

#### b) Tạo Virtual Environment
```bash
# Trên Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1

# Trên macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

#### c) Cài Đặt Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### d) Cập Nhật Đường Dẫn OSGeo4W (Chỉ Windows)
Mở file `core/settings.py` và cập nhật đường dẫn nếu cần:
```python
OSGEO4W_ROOT = r'D:\OSGeo4W'  # Thay đổi nếu cài đặt ở nơi khác
```

### 4. Cấu Hình Django

#### a) Tạo Environment Variables (Tùy Chọn)
Tạo file `.env` tại thư mục gốc:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_NAME=car_rental_gis
DATABASE_USER=postgres
DATABASE_PASSWORD=123
DATABASE_HOST=localhost
DATABASE_PORT=5432
EMAIL_HOST_USER=your-mailtrap-user
EMAIL_HOST_PASSWORD=your-mailtrap-password
```

#### b) Apply Database Migrations
```bash
python manage.py migrate
```

### 5. Chạy Development Server

```bash
python manage.py runserver
```

Truy cập ứng dụng tại: **http://localhost:8000**


## 📁 Cấu Trúc Project

```
CarRentalGIS/
├── core/                    # Cấu hình chính Django
│   ├── settings.py         # Cài đặt ứng dụng
│   ├── urls.py             # URL routing chính
│   ├── wsgi.py             # WSGI config
│   └── asgi.py             # ASGI config
├── rental/                  # Ứng dụng chính (app)
│   ├── models.py           # Định nghĩa models
│   ├── views.py            # Xử lý logic view
│   ├── urls.py             # URL routing app
│   ├── forms.py            # Django forms
│   ├── gis_tools.py        # Hàm tiện ích GIS
│   ├── migrations/         # Database migrations
│   ├── templates/          # HTML templates
│   │   ├── rental/         # Templates chính
│   │   ├── registration/   # Login/Register templates
│   │   └── emails/         # Email templates
│   └── tests.py            # Unit tests
├── static/                  # CSS, JS, Images (tĩnh)
│   └── css/
│       └── style.css
├── media/                   # Uploaded files
│   ├── cars/               # Car images
│   ├── news/               # News images
│   └── reviews/            # Review images
├── manage.py               # Django CLI
├── requirements.txt        # Python dependencies
├── seed_data.py            # Script tạo dữ liệu mẫu
└── README.md               # File này
```

---

## 🔧 Sử Dụng Django CLI Commands

```bash
# Tạo migration cho model
python manage.py makemigrations

# Apply migration vào database
python manage.py migrate

# Tạo superuser mới
python manage.py createsuperuser

# Dừng server khi cần
Ctrl + C

# Chạy tests
python manage.py test

# Tạo static files
python manage.py collectstatic

# Vào Django shell (tương tác trực tiếp với models)
python manage.py shell
```

---

## 🔐 Cấu Hình Email (Mailtrap)

1. Đăng ký tài khoản tại: https://mailtrap.io/
2. Lấy SMTP credentials từ Dashboard
3. Cập nhật trong `core/settings.py`:
```python
EMAIL_HOST_USER = 'your-mailtrap-username'
EMAIL_HOST_PASSWORD = 'your-mailtrap-password'
```

---

## 📝 Các Models Chính

- **UserCustom**: Thông tin người dùng tùy chỉnh
- **Car**: Thông tin xe (biển số, loại, vị trí GIS)
- **CarType**: Loại xe (Xe 4 chỗ, Xe máy, etc.)
- **Station**: Trạm nhận/trả xe (có hình vùng phục vụ)
- **BookingHistory**: Lịch sử đặt/thuê xe
- **Review**: Đánh giá và nhận xét từ khách
- **NewsSection**: Tin tức trang chủ
- **HomePageContent**: Nội dung trang chủ
- **SafeZone**: Vùng an toàn cho xe
- **GPSLog**: Log vị trí GPS xe

---

## 🐛 Troubleshooting

### Lỗi: "django.core.exceptions.ImproperlyConfigured: 'django.contrib.gis' requires GDAL"

**Giải Pháp**:
- Đảm bảo OSGeo4W đã cài đặt trên Windows
- Cập nhật đường dẫn OSGEO4W_ROOT trong `core/settings.py`
- Restart Python interpreter

### Lỗi: "psycopg2: FATAL: Ident authentication failed for user"

**Giải Pháp**:
- Kiểm tra username/password trong `DATABASES` (settings.py)
- Đảm bảo PostgreSQL đang chạy: `sudo systemctl status postgresql`
- Thử reset mật khẩu PostgreSQL: `ALTER USER postgres WITH PASSWORD 'newpassword';`

### Lỗi: "ModuleNotFoundError: No module named 'django'"

**Giải Pháp**:
- Đảm bảo Virtual Environment đã activate
- Cài lại requirements: `pip install -r requirements.txt`

### Bản đồ Leaflet không hiển thị

**Giải Pháp**:
- Kiểm tra console browser cho lỗi (F12)
- Đảm bảo có kết nối internet (Leaflet cần download tiles từ CDN)
- Xác minh coordinates (latitude, longitude) hợp lệ

---

## 📚 Tài Liệu Tham Khảo

- [Django Official Documentation](https://docs.djangoproject.com/)
- [GeoDjango Guide](https://docs.djangoproject.com/en/6.0/ref/contrib/gis/)
- [PostGIS Documentation](https://postgis.net/documentation/)
- [Leaflet.js Maps](https://leafletjs.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## 📧 Liên Hệ & Hỗ Trợ

Nếu gặp vấn đề trong quá trình cài đặt hoặc sử dụng, vui lòng kiểm tra:
1. Tất cả dependencies đã cài đặt đúng
2. Database kết nối thành công
3. Environment variables đúng
4. Cấp quyền file nếu cần

---

## 📄 License

Dự án này được phát triển cho mục đích học tập.

---

**Phiên bản**: 1.0  
**Cập nhật lần cuối**: Tháng 4, 2026
