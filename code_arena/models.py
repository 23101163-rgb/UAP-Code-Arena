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
class Problem(models.Model):
    problem_id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='problems')

    title = models.CharField(max_length=255)
    statement = RichTextField()
    input_specification = RichTextField()
    output_specification = RichTextField()
    difficulty = models.CharField(max_length=10, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')],
                                  default='Easy')
    time_limit = models.IntegerField(default=1)

    # New many-to-many field for categories
    categories = models.ManyToManyField(Category, related_name='problems', blank=True)

def __str__(self):
    return f"{self.title}"
def test_input_upload_to(instance, filename):
    return f"problems/{instance.problem.problem_id}/test_inputs/{filename}"
def test_output_upload_to(instance, filename):
    return f"problems/{instance.problem.problem_id}/test_outputs/{filename}"
class TestInput(models.Model):
    problem = models.ForeignKey('Problem', on_delete=models.CASCADE, related_name='test_inputs')
    file = models.FileField(upload_to=test_input_upload_to)

def __str__(self):
    return f"{self.problem.title} - {self.file.name}"
class TestOutput(models.Model):
    problem = models.ForeignKey('Problem', on_delete=models.CASCADE, related_name='test_outputs')
    file = models.FileField(upload_to=test_output_upload_to)

def __str__(self):
    return f"{self.problem.title} - {self.file.name}"
