from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class User(models.Model):

    GENDER_TYPE = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=70)
    gender = models.CharField(max_length=5, choices=GENDER_TYPE) # django custom field
    age = models.IntegerField(validators=(MinValueValidator(5), MaxValueValidator(100)))


class RecommendResult(models.Model):
    
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True,null=False)
    user_id = models.IntegerField()
    steam_game_name = models.IntegerField()
    rec_genres = models.TextField() # tood : change field Type


class BaseGames(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=100)
    genres = models.TextField()
    image_url = models.TextField()