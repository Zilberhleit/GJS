from django.contrib import admin
from django.urls import path, include
from jams import views
from users import views as users_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('jams/', include('jams.urls')),
    path('login/', users_view.LoginUser.as_view(), name='login'),
    #path('logout/', name='logout'),
    path('register/', users_view.RegisterUser.as_view(), name='regist')
]

handler404 = views.handler404