from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from rental import views as rental_views

urlpatterns = [
    path('news/add/', rental_views.add_news, name='add_news'),
    path('news/<int:news_id>/', rental_views.news_detail, name='news_detail'),
    path('home-content/edit/', rental_views.edit_home_content, name='edit_home_content'),
    path('', include('rental.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'rental.views.error_404_view'

# Fallback để luôn render trang 404 custom khi không khớp URL nào.
urlpatterns += [
    re_path(r'^.*$', rental_views.error_404_view),
]