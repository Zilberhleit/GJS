from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from jams import views
from users import views as users_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('jams/', include('jams.urls')),
    path('login/', users_view.login_view, name='login'),
    path('logout/', users_view.logout_view, name='logout'),
    path('register/', users_view.RegisterUser.as_view(), name='regist'),
    path('accounts/profile/', include('users.urls'), name='user_profile')
]

handler404 = views.handler404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
