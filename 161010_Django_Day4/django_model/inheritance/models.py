from django.db import models


class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    def get_info(self):
        return '%s (%s)' % (self.name, self.age)

    class Meta:
        abstract = True
        ordering = ('-age', )


class Student(CommonInfo):
    home_group = models.CharField(max_length=5)

    class Meta:
        ordering = ('id', )


class Teacher(CommonInfo):
    year = models.CharField(max_length=10)