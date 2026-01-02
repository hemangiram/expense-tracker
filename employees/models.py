from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=10)
    phone_no = models.CharField(max_length=10)
    salary = models.CharField(max_length=10)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name
