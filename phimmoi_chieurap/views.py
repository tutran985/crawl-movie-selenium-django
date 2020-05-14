from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import PhimChieuRap, MovieDetail as MovieDetailModels
from .serializers import PhimChieuRapSerializer, MovieDetailSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import status
from config.selenium_web_driver import SeleniumDriver
from config.common_action import CommonAction


# Create your views here.
class MoviesList(GenericViewSet, CreateModelMixin, ListModelMixin):
    serializer_class = PhimChieuRapSerializer
    permission_classes = [AllowAny, ]
    queryset = PhimChieuRap.objects.all().order_by('created')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = {
            "error_code": 0,
            "massage": "success",
            "data": serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        driver = SeleniumDriver().get_driver()
        driver.get("http://www.phimmoi.net/phim-chieu-rap/page-{}.html".format(request.data['page']))
        common_action = CommonAction(driver)
        data_end = {
            "error_code": 0,
            "massage": "success",
            "total_movies": 0,
            "data": []
        }
        try:
            common_action.wait_until_element_visible('//ul[@class="list-movie"]', 50)
            movies_count = common_action.get_number_of_elements('//ul[@class="list-movie"]//li[@class="movie-item"]')
            data_end['total_movies'] = movies_count
            for i in range(1, movies_count + 1):
                try:
                    data = {
                        'name': common_action.get_text_from_elements('//ul[@class="list-movie"]//li[@class="movie-item"][{}]//div[@class="movie-meta"]//span[@class="movie-title-1"]'.format(i))[0],
                        'title': common_action.get_text_from_elements('//ul[@class="list-movie"]//li[@class="movie-item"][{}]//div[@class="movie-meta"]//span[@class="movie-title-2"]'.format(i))[0],
                        'url': common_action.get_attribute('//ul[@class="list-movie"]//li[@class="movie-item"][{}]//a[@class="block-wrapper"]'.format(i), 'href'),
                        'image': common_action.get_attribute('//ul[@class="list-movie"]//li[@class="movie-item"][{}]//a[@class="block-wrapper"]//div[@class="movie-thumbnail"]'.format(i), 'style').split('("')[1].split('")')[0],
                        'playtime': common_action.get_text_from_elements('//ul[@class="list-movie"]//li[@class="movie-item"][{}]//div[@class="movie-meta"]//span[@class="movie-title-chap"]'.format(i))[0],
                        'sub': common_action.get_text_from_elements('//ul[@class="list-movie"]//li[@class="movie-item"][{}]//div[@class="movie-meta"]//span[@class="ribbon"]'.format(i))[0]
                    }
                    serializer = self.get_serializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    data_end['data'].append(data)
                except:
                    pass
        except:
            data_end = {
                "error_code": 404,
                "massage": "Error"
            }
            return Response(data_end, status=status.HTTP_404_NOT_FOUND)
        return Response(data_end, status=status.HTTP_201_CREATED)


class MovieDetail(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin):
    serializer_class = MovieDetailSerializer
    permission_classes = [AllowAny, ]
    queryset = MovieDetailModels.objects.all()

    def get_detail_phimcheurap(self, movie_id):
        try:
            return PhimChieuRap.objects.get(id=movie_id)
        except:
            data_end = {
                "error_code": 404,
                "massage": "Error"
            }
            return Response(data_end, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        if len(MovieDetailModels.objects.filter(movie=request.data['movie_id'])) >= 1:
            data_end = {
                "error_code": 201,
                "massage": "da co data"
            }
            return Response(data_end, status=status.HTTP_201_CREATED)
        movie_detail = self.get_detail_phimcheurap(request.data['movie_id'])
        serializer_movie_detail = PhimChieuRapSerializer(movie_detail)
        driver = SeleniumDriver().get_driver()
        driver.get(serializer_movie_detail.data['url'])
        common_action = CommonAction(driver)
        try:
            common_action.wait_until_element_visible('//a[@id="btn-film-watch"]', 50)
        except:
            data_end = {
                "error_code": 404,
                "massage": "Error"
            }
            return Response(data_end, status=status.HTTP_404_NOT_FOUND)
        checker = {}
        if common_action.get_number_of_elements('//dl[@class="movie-dl"]') > 0:
            line_dt = common_action.get_number_of_elements('//dl[@class="movie-dl"]//dt')
            for i in range(1, line_dt + 1):
                get_text_dt = common_action.get_text_from_elements('//dl[@class="movie-dl"]//dt[{}]'.format(i))[0]
                get_text_dd = common_action.get_text_from_elements('//dl[@class="movie-dl"]//dd[{}]'.format(i))[0]
                checker[get_text_dt] = get_text_dd
        description = common_action.get_text_from_elements('//div[@id="film-content"]//p')[0]
        driver.get(serializer_movie_detail.data['url'] + 'xem-phim.html')
        common_action.wait_until_element_visible('//iframe[@class="player-embed-iframe"]', 50)
        if checker != {}:
            data = {
                'movie': serializer_movie_detail.data['id'],
                'year': checker['Năm:'],
                'debut': checker['Ngày ra rạp:'],
                'language': checker['Ngôn ngữ:'],
                'description': description,
                'url_movie': serializer_movie_detail.data['url'] + 'xem-phim.html',
                'url_movie_iframe': common_action.get_attribute('//iframe[@class="player-embed-iframe"]', 'src'),
            }
        else:
            data_end = {
                "error_code": 404,
                "massage": "Error"
            }
            return Response(data_end, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(data, status=status.HTTP_201_CREATED)
