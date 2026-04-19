from django.contrib.gis.db import models
from django.db.models import Count
from django.db.models import Sum

# Thêm vào models.py
class UserCustom(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    IRL_name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, default='guest')
    is_active = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    book_day = models.DateTimeField(null=True, blank=True)
    pickup_day = models.DateTimeField(null=True, blank=True)
    ORDER_STATUS = [
        ('pending', 'Chờ xử lý'),
        ('confirmed', 'Đã xác nhận (Chờ nhận xe)'),
        ('cancelled', 'Đã hủy'),
    ]
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')

    def __str__(self):
        return self.username


class Station(models.Model):
    name = models.CharField(max_length=100)
    area = models.PolygonField(srid=4326)
    capacity = models.IntegerField(default=10)
    def current_car_count(self):
        """Chỉ đếm xe nằm trong trạm VÀ chưa bị ai đặt"""
        return Car.objects.filter(
            current_location__within=self.area,
            is_available=True # Chỉ đếm xe sẵn sàng
        ).count()
    def get_inventory(self):
        return Car.objects.filter(
            current_location__within=self.area,
            is_available=True
        ).values('brand_name', 'car_type__name', 'id')\
         .annotate(total=Sum('quantity'))

class CarType(models.Model):
    name = models.CharField(max_length=50)
    base_price_per_km = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self): return self.name

class Car(models.Model):
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    license_plate = models.CharField(max_length=15, unique=True)
    brand_name = models.CharField(max_length=50, null=True, blank=True)
    short_description = models.TextField(blank=True, default='', help_text='Mô tả ngắn hiển thị trên trang loại xe (admin chỉnh sửa).')
    image = models.ImageField(upload_to='cars/', null=True, blank=True)
    current_location = models.PointField(srid=4326, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    def __str__(self): return self.license_plate

class GPSLog(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    location = models.PointField(srid=4326)
    timestamp = models.DateTimeField(auto_now_add=True)

class SafeZone(models.Model):
    name = models.CharField(max_length=100)
    area = models.PolygonField(srid=4326) 
    def __str__(self): return self.name

class BookingHistory(models.Model):
    user = models.ForeignKey(UserCustom, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    pickup_station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True, related_name='pickups')
    return_station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True, related_name='returns')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    total_distance = models.FloatField(default=0.0)
    total_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default='ongoing')