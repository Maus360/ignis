from datetime import datetime
from django.db import models

from django.urls import reverse
from django.contrib.auth.models import User

from engine.tool import *


class Dataset(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to="datasets/", null=False, blank=False)
    date = models.DateTimeField(default=datetime.today)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    sharing = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date"]

    def get_absolute_url(self):
        """
        Returns the url to access a particular blog instance.
        """
        return reverse("dataset-detail", args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """

        return self.name

    def meta_data(self):
        resolver = DatasetResolver(self.file)
        return resolver.get_meta_data()


class NN(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateTimeField(default=datetime.today)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    sharing = models.BooleanField(default=False)
    code = models.TextField(max_length=2000)

    class Meta:
        ordering = ["-date"]

    def get_absolute_url(self):
        """
        Returns the url to access a particular blog instance.
        """
        return reverse("nn-detail", args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """

        return self.name

    def meta_data(self):
        resolver = NNResolver(self)
        return resolver.get_meta_data()
