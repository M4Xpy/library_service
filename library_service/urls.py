from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
                  path(
                      "admin/", admin.site.urls, ),
                  path(
                      "api/doc/", SpectacularAPIView.as_view(), name="schema", ),
                  path("api/doc/swagger/",
                       SpectacularSwaggerView.as_view(url_name="schema"), ),
                  path(
                      "api/doc/redoc/",
                      SpectacularRedocView.as_view(url_name="schema"),
                      name="redoc", ),
                  path(
                      "__debug__/", include("debug_toolbar.urls"), ),
                  path(
                      "api/books/",
                      include("books.urls",
                              namespace="books"), ),
                  path(
                      "api/borrowings/",
                      include("borrowings.urls", namespace="borrowings"), ),
                  path(
                      "api/payments/",
                      include("payments.urls", namespace="payments"), ),
                  path(
                      "api/user/", include("users.urls", namespace="user"), ),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
