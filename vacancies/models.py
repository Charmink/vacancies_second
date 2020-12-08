from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    description = models.TextField()
    employee_count = models.IntegerField()
    logo = models.ImageField(upload_to='company_logos', height_field='height_field',
                             width_field='width_field')
    height_field = models.PositiveIntegerField(default=150)
    width_field = models.PositiveIntegerField(default=150)
    owner = models.OneToOneField(User, related_name='companies', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class Specialty(models.Model):
    code = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    picture = models.ImageField(upload_to='specialty_pictures', height_field='height_field',
                                width_field='width_field')
    height_field = models.PositiveIntegerField(default=150)
    width_field = models.PositiveIntegerField(default=150)

    def __str__(self):
        return f'{self.title}'


class Vacancy(models.Model):
    title = models.CharField(max_length=64)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateTimeField()

    def __str__(self):
        return f'{self.title}'


class Application(models.Model):
    written_username = models.CharField(max_length=128)
    written_phone = models.CharField(max_length=15)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, related_name='applications', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='applications', on_delete=models.CASCADE)

    def __str__(self):
        return f'Application of {self.written_username}'


class Resume(models.Model):
    owner = models.OneToOneField(User, related_name='resume', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    STATUS_CHOICES = [('Не ищу работу', 'Не ищу работу'),
                      ('Рассматриваю предложения', 'Рассматриваю предложения'),
                      ('Ищу работу', 'Ищу работу')]
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, default='Ищу работу')
    salary = models.IntegerField()
    specialty = models.ForeignKey(Specialty, related_name='resumes', on_delete=models.CASCADE)
    GRAGE_CHOICES = [('Стажер', 'Стажер'),
                     ('Джуниор', 'Джуниор'),
                     ('Миддл', 'Миддл'),
                     ('Синьор', 'Синьор'),
                     ('Лид', 'Лид')]
    grage = models.CharField(max_length=64, choices=GRAGE_CHOICES, default='Стажер')
    education = models.TextField()
    experience = models.TextField()
    portfolio = models.TextField()

    def __str__(self):
        return f'Resume of {self.name}'
