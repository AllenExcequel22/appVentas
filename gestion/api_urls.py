
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Viewsets y vistas de la API
from .api_views import (
    ClienteViewSet,
    ProductoViewSet,
    VentaViewSet,
    DashboardView,
    UserRegisterView,
    UserProfileView,
)

# Swagger / OpenAPI (documentación)
schema_view = get_schema_view(
    openapi.Info(
        title="API Sistema de Gestión de Ventas",
        default_version='v1',
        description="API para clientes, productos y ventas",
        contact=openapi.Contact(email="contacto@sistema-ventas.local"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Router para clientes, productos y ventas
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'ventas', VentaViewSet, basename='venta')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', UserRegisterView.as_view(), name='api_register'),
    path('profile/', UserProfileView.as_view(), name='api_profile'),

    path('dashboard/', DashboardView.as_view(), name='api_dashboard'),

    path('', include(router.urls)),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]