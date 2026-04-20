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
    detail_description = models.TextField(blank=True, default='', help_text='Mô tả chi tiết (HTML từ CKEditor), trang car_description.')
    image = models.ImageField(upload_to='cars/', null=True, blank=True)
    current_location = models.PointField(srid=4326, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    def __str__(self): return self.license_plate


class CarGalleryImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='cars/gallery/')
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f'Gallery #{self.pk} ({self.car_id})'

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


class Review(models.Model):
    user = models.ForeignKey(UserCustom, on_delete=models.CASCADE, related_name='reviews')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    booking_history = models.OneToOneField(BookingHistory, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(choices=[(i, f'{i} sao') for i in range(1, 6)])
    comment = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('booking_history',)

    def __str__(self):
        return f'Review by {self.user.username} for {self.car.brand_name} - {self.rating} sao'


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='reviews/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image for {self.review.id}'


class NewsSection(models.Model):
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='news/')
    content = models.TextField(help_text='Nội dung bài viết (HTML từ CKEditor).')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class HomePageContent(models.Model):
    hero_title = models.CharField(max_length=255, default='Hệ thống thuê xe trực tuyến')
    hero_description = models.TextField(default='Nền tảng thuê xe nhanh chóng, tiện lợi và đáng tin cậy.')
    hero_button_text = models.CharField(max_length=100, default='Đặt xe ngay')
    hero_button_url = models.CharField(max_length=255, default='/car-types/')
    hero_image = models.ImageField(upload_to='homepage/', null=True, blank=True)

    feature_1_title = models.CharField(max_length=255, default='Nhiều loại xe đa dạng')
    feature_1_description = models.TextField(default='Cung cấp nhiều loại xe phù hợp cho mọi nhu cầu.')
    feature_2_title = models.CharField(max_length=255, default='Đặt xe nhanh chóng')
    feature_2_description = models.TextField(default='Giao diện đơn giản, dễ sử dụng chỉ trong vài bước.')
    feature_3_title = models.CharField(max_length=255, default='Thông tin minh bạch')
    feature_3_description = models.TextField(default='Hiển thị đầy đủ thông tin xe và giá thuê rõ ràng.')

    news_section_title = models.CharField(max_length=255, default='Tin Tức')
    news_section_subtitle = models.CharField(max_length=255, blank=True, default='Các bài viết mới nhất từ hệ thống')

    def __str__(self):
        return 'Home page content'