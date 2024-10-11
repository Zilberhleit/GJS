from django.contrib import admin
from django.urls import path, include
from jams import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jams/', include('jams.urls')),

]

handler404 = views.handler404