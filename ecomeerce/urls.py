from django.conf.urls import url,include
from django.contrib import admin
from .views import home_page,about_page,contact_page
from django.views.generic import TemplateView
from accounts.views import login_page,register_page,guest_login_view
from django.contrib.auth.views import LogoutView

#static files
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home',home_page,name='home'),
    url(r'^about/',about_page,name='about'),
    url(r'^contact/',contact_page,name='contact'),
    url(r'^login/',login_page,name='login'),
    url(r'^logout/',LogoutView.as_view(),name='logout'),
    url(r'^register/',register_page,name='register'),
    url(r'^guest/',guest_login_view,name='guest_register'),

    url(r'^bootstrap/',TemplateView.as_view(template_name='bootstrap/example.html')),
    
    url(r'^products/',include("products.urls",namespace="products")),
    url(r'^search/',include("search.urls",namespace="search")),
    url(r'^cart/',include("carts.urls",namespace="cart")),
    url(r'^face/',include("facedetection.urls",namespace="facedetection")),

    

    
]

if settings.DEBUG:
    urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns=urlpatterns+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

