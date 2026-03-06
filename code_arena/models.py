from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.core.validators import FileExtensionValidator
from django.db import models
from UAP_CodeArena import settings
from django.utils import timezone
from ckeditor.fields import RichTextField
class UserManager(BaseUserManager):
    def create_user(self, email, full_name, university_id, password=None):
        if not email:
            raise ValueError("Email is required")
        if not email.endswith("@uap-bd.edu"):
            raise ValueError("This email is not allowed")

        email = self.normalize_email(email)

        if User.objects.filter(university_id=university_id).exists():
            raise ValueError("This university ID is already taken")

        user = self.model(
            email=email,
            full_name=full_name,
            university_id=university_id
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, university_id, password=None):
        user = self.create_user(email, full_name, university_id, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user