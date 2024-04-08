from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Diabetes(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  Pregnancies = models.IntegerField()
  Glucose = models.IntegerField()
  BloodPressure = models.IntegerField()
  SkinThickness = models.IntegerField()
  Insulin = models.IntegerField()
  BMI = models.FloatField()
  DiabetesPedigreeFunction = models.FloatField()
  Age = models.IntegerField()
  Result = models.TextField()

  def __str__(self):
    return self.user.username
  