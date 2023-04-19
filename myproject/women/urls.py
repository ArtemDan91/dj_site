from django.urls import path, re_path, include
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView, TokenVerifyView

from .views import *
from django.views.decorators.cache import cache_page
from rest_framework import routers


# router = routers.SimpleRouter()
# router.register(r'women', WomenVeiwSet, basename='women')
# print(router.urls)


urlpatterns = [
    # path('', index, name='home'),
    path('', WomenHome.as_view(), name='home'),
    path('api/v1/drf-auth', include('rest_framework.urls')), #session_based auth

    path('api/v1/auth/', include('djoser.urls')), #token_based auth
    re_path(r'^auth/', include('djoser.urls.authtoken')), #авторизація по токенам

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #JWT токени
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('about/', WomenAbout.as_view(), name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>', WomenCategory.as_view(), name='category'),

    # path('api/v1/womenlist/', WomenAPIView.as_view()),
    # path('api/v1/womenlist/<int:pk>/', WomenAPIView.as_view()),

    path('api/v1/women/', WomenAPIList.as_view()),
    path('api/v1/women/<int:pk>/', WomenAPIUpdate.as_view()),
    path('api/v1/womendelete/<int:pk>/', WomenAPIDestroy.as_view()),

    # path('api/v1/', include(router.urls)), #http://127.0.0.1:8000/api/v1/women/
]
