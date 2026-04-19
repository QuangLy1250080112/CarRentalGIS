import math
# Đưa các import models lên đầu để tránh lỗi "is not defined"
from .models import GPSLog, Car, SafeZone, CarType

# Vị trí gốc (Bến Thành)
START_POINT_COORD = (10.771, 106.698) # (lat, lon)
EARTH_RADIUS_KM = 6371.0

def haversine_distance(coord1, coord2):
    """Tính khoảng cách giữa 2 điểm (lat, lon) bằng công thức Haversine"""
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS_KM * c

def is_inside_polygon(point, polygon_coords):
    """Thuật toán Ray Casting kiểm tra điểm trong đa giác"""
    x, y = point # (lat, lon)
    n = len(polygon_coords)
    inside = False
    if n < 3: return False
    p1x, p1y = polygon_coords[0]
    for i in range(n + 1):
        p2x, p2y = polygon_coords[i % n]
        if y > min(p1y, p2y) and y <= max(p1y, p2y) and x <= max(p1x, p2x):
            if p1y != p2y:
                xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if p1x == p2x or x <= xinters:
                    inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def calculate_stats(car):
    """Tính toán quãng đường và chi phí, phạt nếu rời xa điểm gốc > 5km"""
    logs = GPSLog.objects.filter(car=car).order_by('timestamp')
    total_km = 0.0
    has_exited_safe_zone = False 
    
    # Phạm vi tính phí phạt ngoài vùng an toàn (km)
    SAFE_LIMIT_KM = 5  

    if logs.exists():
        # 1. Kiểm tra điểm đầu tiên
        first_pos = (logs[0].location.y, logs[0].location.x)
        dist_to_start = haversine_distance(START_POINT_COORD, first_pos)
        total_km += dist_to_start
        
        if dist_to_start > SAFE_LIMIT_KM:
            has_exited_safe_zone = True
        
        # 2. Kiểm tra các điểm tiếp theo
        for i in range(len(logs) - 1):
            p1 = (logs[i].location.y, logs[i].location.x)
            p2 = (logs[i+1].location.y, logs[i+1].location.x)
            
            total_km += haversine_distance(p1, p2)
            
            if not has_exited_safe_zone:
                dist_from_origin = haversine_distance(START_POINT_COORD, p2)
                if dist_from_origin > SAFE_LIMIT_KM:
                    has_exited_safe_zone = True

    if total_km <= 0:
        return {
            'total_km': 0, 'base_fee': 0, 'extra_fee': 0, 'penalty_fee': 0, 'total_fee': 0, 'violated': False
        }

    base_fee = 200000
    # Chỗ này tính theo mốc km miễn phí, sửa số km miễn phí qua biến SAFE_LIMIT_KM
    extra_km = max(0, total_km - SAFE_LIMIT_KM) 
    # Điều chỉnh phí phạt khi rời xa vùng an toàn
    penalty_fee = 120000 if has_exited_safe_zone else 0
    total_fee = base_fee + (extra_km * 15000) + penalty_fee
    
    return {
        'total_km': round(total_km, 2),
        'base_fee': base_fee,
        'extra_fee': round(extra_km * 15000, 0),
        'penalty_fee': penalty_fee,
        'total_fee': round(total_fee, 0),
        'violated': has_exited_safe_zone
    }

def is_car_in_safe_zone(car_id):
    """Kiểm tra xe hiện tại có nằm trong vùng đa giác an toàn (SafeZone model) không"""
    try:
        car = Car.objects.get(id=car_id)
        if not car.current_location:
            return False
            
        car_point = (car.current_location.y, car.current_location.x)
        safe_zones = SafeZone.objects.all()
        
        for zone in safe_zones:
            # Lưu ý: polygon_coords giả định là list các tuple (lat, lon)
            if is_inside_polygon(car_point, zone.area_coords):
                return True
    except Exception:
        return False
    return False