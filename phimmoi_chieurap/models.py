from django.db import models


# Create your models here.
class PhimChieuRap(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=250, blank=True)
    title = models.CharField(max_length=100, blank=True, default='')
    url = models.CharField(max_length=250, blank=True, default='')
    image = models.CharField(max_length=250, blank=True, default='')
    playtime = models.CharField(max_length=250, blank=True, default='')
    sub = models.CharField(max_length=250, blank=True, default='')

    class Meta:
        ordering = ['created']


class MovieDetail(models.Model):
    movie = models.ForeignKey(PhimChieuRap, related_name='movie', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    year = models.CharField(max_length=250, blank=True)
    debut = models.CharField(max_length=100, blank=True, default='')
    language = models.CharField(max_length=100, blank=True, default='')
    business = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    url_movie = models.CharField(max_length=100, blank=True, default='')
    url_movie_iframe = models.CharField(max_length=100, blank=True, default='')