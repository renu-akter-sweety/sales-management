from django.db import models
from django.utils import timezone


class categorymodel(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Salesmodel(models.Model):
    product_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sale_date = models.DateField(auto_now_add=True)  # automatically set on create
    

class Grade(models.Model):
    marks = models.FloatField()
    grade = models.CharField(max_length=2)  # e.g., "A+", "B", "F"
    date_created = models.DateTimeField(default=timezone.now)    


