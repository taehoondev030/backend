"""
Database models
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a user with the given email and password."""
        if not email:
            raise ValueError('User must have an email address')
        
        # 이름과 학번 등을 처리하는 부분
        name = extra_fields.pop('name', None)
        student_id = extra_fields.pop('student_id', None)
        
        user = self.model(email=self.normalize_email(email), name=name, student_id=student_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length = 255, unique=True)
    name = models.CharField(max_length = 255)
    student_id = models.CharField(max_length = 9, unique = True, default="")
    description = models.CharField(max_length = 255, default="")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'student_id']

# 유저 응답 모델
class Answer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    answer = models.JSONField(default = dict)  # 유저의 응답을 딕셔너리로 저장
    
    def __str__(self):
        return f"User: {self.user.email}, Answer: {self.answer}"

# 룸메이트 신청 모델
class Match(models.Model):
    # 요청한 사람
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_requests',
        on_delete=models.CASCADE,
    )
    # 요청을 받은 사람
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_requests',
        on_delete=models.CASCADE,
    )
    # 요청 상태
    status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], default = 'pending')
    # 요청 일시
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 동일한 사용자에게 중복 신청 방지
        unique_together = ('requester', 'recipient')

# 매칭 그룹 모델
class Group(models.Model):
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add = True)