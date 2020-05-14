from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import MovieDetail
from phimmoi_chieurap import views

router = SimpleRouter()
router.register('movie-theaters', views.MoviesList)
router.register('movie-detail', views.MovieDetail)
# router.register('test/delete', DeleteTestAPI, base_name='test-delete')

urlpatterns = [
    # url('login/', UserLoginAPI.as_view()),
    url('', include(router.urls)),
    # url('detail/', MovieDetail.as_view()),
    # url('upload/', UploadAPI.as_view()),
]
