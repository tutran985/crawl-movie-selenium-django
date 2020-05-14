from rest_framework import serializers
from phimmoi_chieurap.models import PhimChieuRap, MovieDetail


class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDetail
        fields = ('id', 'movie', 'year', 'debut', 'language', 'business', 'description', 'url_movie', 'url_movie_iframe')



class PhimChieuRapSerializer(serializers.ModelSerializer):
    # movie = serializers.PrimaryKeyRelatedField(many=True, queryset=MovieDetail.objects.all())
    movie = MovieDetailSerializer(many=True, read_only=True)
    class Meta:
        model = PhimChieuRap
        fields = ['id', 'name', 'title', 'url', 'image', 'playtime', 'sub', 'movie']


