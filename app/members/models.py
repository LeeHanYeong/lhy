from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_fields import DefaultStaticImageField
from phonenumber_field.modelfields import PhoneNumberField

from utils.django.mixins import DeletedFlagManager, DeletedFlagMixin

__all__ = (
    'UserManager',
    'User',
)


class UserManager(DeletedFlagManager, BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if extra_fields.get('type') == User.TYPE_EMAIL:
            username = email
        elif username is None:
            raise ValidationError('사용자 생성 필수값(username)이 주어지지 않았습니다')
        return super().create_user(username, email, password, **extra_fields)


class User(AbstractUser, DeletedFlagMixin, TimeStampedModel):
    TYPE_KAKAO, TYPE_FACEBOOK, TYPE_EMAIL = 'kakao', 'facebook', 'email'
    TYPE_CHOICES = (
        (TYPE_KAKAO, '카카오'),
        (TYPE_FACEBOOK, '페이스북'),
        (TYPE_EMAIL, '이메일'),
    )
    first_name = None
    last_name = None
    name = models.CharField('이름', max_length=20, blank=True)
    type = models.CharField('유형', max_length=10, choices=TYPE_CHOICES, default=TYPE_EMAIL)
    img_profile = DefaultStaticImageField(
        '프로필 이미지', upload_to='user', default_image_path='images/profile.jpg', blank=True)
    nickname = models.CharField('닉네임', max_length=20, unique=True, blank=True, null=True)
    email = models.EmailField('이메일', unique=True)
    phone_number = PhoneNumberField('전화번호', blank=True)

    # Deleted
    deleted_email = models.EmailField('삭제된 유저의 이메일', blank=True)
    deleted_username = models.CharField('삭제된 유저의 username', max_length=150, blank=True)

    REQUIRED_FIELDS = ('email',)

    objects = UserManager()

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.type == self.TYPE_EMAIL:
            self.username = self.email
        super().save(*args, **kwargs)

    def perform_delete(self):
        def get_deleted_username(num):
            return f'deleted_{num:05d}'

        self.deleted_username = self.username
        self.deleted_email = self.email

        # is_deleted = True로 저장하기 전에, deleted_숫자 의 username을 갖도록 함
        last_deleted_user = User._base_manager.filter(is_deleted=True).order_by('username').last()
        if last_deleted_user:
            number = int(last_deleted_user.username.rsplit('_', 1)[-1]) + 1
        else:
            number = 0
        deleted_name = get_deleted_username(number)
        self.username = deleted_name
        self.email = None
        self.nickname = None

        # 만약 계산한 deleted_name이 이미 존재할 경우, 모든 삭제된 User들의 deleted_name을 다시 재설정
        if User._base_manager.filter(username=deleted_name).exists():
            index = 0
            for user in User._base_manager.filter(is_deleted=True).order_by('pk'):
                user.username = get_deleted_username(index)
                user.save()
                index += 1
            self.username = get_deleted_username(index)

