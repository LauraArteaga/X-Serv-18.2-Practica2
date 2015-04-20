from django.db import models

class UrlsList(models.Model):
	url = models.CharField(max_length = 100)
	shortedUrl = models.CharField(max_length = 50)
