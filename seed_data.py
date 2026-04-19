import os
import sys

# BƯỚC 1: PHẢI THIẾT LẬP MÔI TRƯỜNG TRƯỚC TIÊN - KHÔNG ĐƯỢC IMPORT DJANGO GIS TRƯỚC ĐOẠN NÀY
OSGEO4W_ROOT = r'D:\OSGeo4W'
os.environ['PATH'] = os.path.join(OSGEO4W_ROOT, 'bin') + os.pathsep + os.environ['PATH']
os.environ['PROJ_LIB'] = os.path.join(OSGEO4W_ROOT, 'share', 'proj')
os.environ['GDAL_DATA'] = os.path.join(OSGEO4W_ROOT, 'share', 'gdal')


# BƯỚC 2: KHỞI TẠO DJANGO
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# BƯỚC 3: SAU KHI SETUP XONG MỚI ĐƯỢC IMPORT POINT, POLYGON VÀ MODELS
from django.contrib.gis.geos import Point, Polygon
from rental.models import CarType, Car, SafeZone

def run_seed():
    print("--- Đang bắt đầu nạp dữ liệu... ---")
    
    # Tạo các loại xe
    xe_4_cho, _ = CarType.objects.get_or_create(name="Xe 4 chỗ", base_price_per_km=15000)
    xe_may, _ = CarType.objects.get_or_create(name="Xe máy", base_price_per_km=5000)
    xe_8_cho, _ = CarType.objects.get_or_create(name="Xe 8 chỗ", base_price_per_km=25000)
    
    # Tạo xe máy mẫu
    Car.objects.get_or_create(
        license_plate="59-A1 999.99", 
        car_type=xe_may, 
        current_location=Point(106.69, 10.77)
    )

    # Tạo xe 8 chỗ mẫu
    Car.objects.get_or_create(
        license_plate="51G-888.88", 
        car_type=xe_8_cho, 
        current_location=Point(106.72, 10.79)
    )
    
    print("--- ĐÃ CẬP NHẬT XONG XE MÁY VÀ XE 8 CHỖ! ---")

if __name__ == "__main__":
    run_seed()