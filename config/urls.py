from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt.views import TokenRefreshView
# Importas tu nueva vista personalizada
from users.views import CustomTokenObtainPairView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/character/', include('character.urls')),
    path('api/users/', include('users.urls')),
    
    # Ruta de Login JWT personalizada
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]