from django.db import models  # type: ignore


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone_no = models.CharField(max_length=10)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name
