from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # اضافه کردن فیلد موبایل برای توسعه‌های آینده (مثل سیستم OTP)
    phone_number = models.CharField(
        max_length=11, 
        blank=True, 
        null=True, 
        unique=True,
        verbose_name="شماره موبایل"
    )

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        # اگر کاربر نام و نام خانوادگی داشت آن را برمی‌گرداند، در غیر این صورت نام کاربری
        if self.get_full_name():
            return self.get_full_name()
        return self.username
