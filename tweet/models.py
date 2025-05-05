from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    sap_id = models.CharField(max_length=11, unique=True, null=True, blank=True)
    admission_year = models.IntegerField(null=True, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Tweet(models.Model):
    CATEGORY_CHOICES = [
        ('operating_systems', 'Operating Systems'),
        ('programming', 'Programming'),
        ('data_science', 'Data Science'),
        ('web_development', 'Web Development'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Name")
    file = models.FileField(upload_to='file/', verbose_name="File", default='file/answers.pdf')
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name="Category"
    )
    custom_category = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Custom Category"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        preview = self.name[:10]
        if len(self.name) > 10:
            preview += '...'
        return f'{self.user.username} - {preview}'

    def get_category_display_name(self):
        if self.category == 'other' and self.custom_category:
            return self.custom_category
        return dict(self.CATEGORY_CHOICES).get(self.category, 'Other')
