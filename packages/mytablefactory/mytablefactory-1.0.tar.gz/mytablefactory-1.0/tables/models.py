from django.db import models
from django.core.exceptions import ValidationError

class Table(models.Model):
  name = models.CharField(max_length=255, unique=True)
  def __str__(self):
      return self.name

class Leg(models.Model):
  table_id = models.ForeignKey(Table, on_delete=models.CASCADE)

class Foot(models.Model):
  width = models.FloatField(default=0, blank=True, null=True)
  length = models.FloatField(default=0, blank=True, null=True)
  radius = models.FloatField(default=0, blank=True, null=True)
  legs = models.ManyToManyField(Leg)

  def clean(self):
    if self.radius and (self.length or self.width):
      raise ValidationError('A foot with a radius must not have length or width.')
    if self.length and not self.width:
      raise ValidationError('A foot with a length must also have a width.')
    if self.width and not self.length:
      raise ValidationError('A foot with a width must also have a length.')