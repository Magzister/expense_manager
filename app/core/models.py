from django.db import models
from django.contrib.auth.models import User


class CreateUpdateInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        default=0.0
    )
    money = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.money)


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='categories'
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'


class DefaultCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'default_category'


class Transaction(CreateUpdateInfo):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='transactions',
        null=True
    )
    organization = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return f'{self.user} {self.amount} {self.category}'

    class Meta:
        db_table = 'transtaction'


class Sample(models.Model):
    attachment = models.FileField()
