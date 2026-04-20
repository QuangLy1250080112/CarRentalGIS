from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('news/add/', views.add_news, name='add_news'),
    path('home-content/edit/', views.edit_home_content, name='edit_home_content'),
    path('car-types/', views.car_types_view, name='car_types'),
    path('car-type/<int:type_id>/', views.car_detail_view, name='car_detail'),
    path('car/<int:car_id>/description/', views.car_description, name='car_description'),
    path('car/<int:car_id>/ckeditor/upload/', views.ckeditor_upload, name='ckeditor_upload'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('management/', views.management, name='management'),
    path('administration/', views.administration, name='administration'),
    path('about/', views.about, name='about'),

    path('api/simulate/', views.simulate_movement, name='simulate_movement'),
    path('api/reset-data/', views.reset_data, name='reset_data'),
    path('api/checkout-car/', views.checkout_car, name='checkout_car'),
    path('api/get-cars-in-zone/', views.get_cars_in_zone, name='get_cars_in_zone'),
    path('book-car/', views.book_car, name='book_car'),
    
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register_view, name='register'),
    path('activate/<str:token>/', views.activate, name='activate'),
    path('accounts/', views.account_management, name='account_management'),
    
    path('addCar/', views.get_addCar, name='add_car'),
    path('addCar_save/', views.add_car, name='add_car_save'),
    path('delete/<int:id>/', views.delete_car, name='delete_car'),
    path('car/short-description/', views.update_car_short_description, name='update_car_short_description'),
      
    path('accounts/', views.account_management, name='account_management'),
    path('api/upsert-user/', views.upsert_user, name='upsert_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('update-order/<int:user_id>/<str:status>/', views.update_order_status, name='update_order_status'),
    path('delete-order/<int:user_id>/', views.delete_order, name='delete_order'),

    path('api/get-stations-nearby/', views.get_stations_nearby, name='get_stations_nearby'),
    path('station/<int:station_id>/', views.station_detail, name='station_detail'),
    path('stations/', views.station_list, name='station_list'),
    path('add-station/', views.add_station, name='add_station'),
    path('station/delete/<int:station_id>/', views.delete_station, name='delete_station'),

    path('history/', views.booking_history_list, name='booking_history'),
    path('return-car/<int:history_id>/', views.return_car, name='return_car'),
    path('revenue/', views.revenue_statistics, name='revenue_statistics'),
    path('revenue/export/', views.export_revenue_excel, name='export_revenue_excel'),

    path('api/reviews/<int:car_id>/', views.get_reviews_for_car, name='get_reviews'),
    path('api/check-review/<int:car_id>/', views.check_can_review, name='check_can_review'),
    path('api/add-review/', views.add_review, name='add_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),

    path('error-403/', views.error_403_view, name='error_403'),
]