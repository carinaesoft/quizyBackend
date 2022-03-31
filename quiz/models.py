from django.db import models


# Create your models here.

class Images (models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(db_column='Name', max_length=100)
    description = models.TextField(db_column='Description')
    image = models.ForeignKey(Images, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, db_column='Category')
    name = models.CharField(max_length=50, db_column='Name')
    release_date = models.DateField(db_column='ReleaseDate')
    description = models.TextField(db_column='Description')
    image = models.ForeignKey(Images, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
