from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import (SpectacularRedocView,SpectacularAPIView,SpectacularSwaggerView)
urlpatterns = [
    path('api/schema/',SpectacularAPIView.as_view(),name="schema"),
    path('api/docs/',SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui"),
    path('api/redoc/',SpectacularRedocView.as_view(url_name="schema"),name="swagger-redoc"),
    path("admin/", admin.site.urls),
    path('auth/',include("apps.accounts.urls")),
    path('contact/',include("apps.contact.urls")),
    path('products/',include("apps.products.urls")),
]
