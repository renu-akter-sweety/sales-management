
from django.contrib import admin
from django.urls import path
from myproject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', basepage, name='baseurl'),          # ✅ now Django knows basepage
    path('add_sale/', Add_Salepage, name='add_saleurl'),
    path('sale_list/', Sale_listpage, name='sale_listurl'),
    path('grade/', Gradepage, name='gradeurl'),
    path('cgpa/', Cgpapage, name='cgpaurl'),
]
