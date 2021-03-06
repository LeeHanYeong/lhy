# Generated by Django 2.2.8 on 2019-12-07 07:49

import apps.members.models.base
import apps.members.models.wps
from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields
import django_fields.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=20, verbose_name='이름')),
                ('type', models.CharField(choices=[('wps', '웹 프로그래밍 스쿨')], max_length=20, verbose_name='분류')),
                ('img_profile', django_fields.fields.DefaultStaticImageField(blank=True, upload_to='user', verbose_name='프로필 이미지')),
                ('nickname', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='닉네임')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='이메일')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='전화번호')),
                ('deleted_email', models.EmailField(blank=True, max_length=254, verbose_name='삭제된 유저의 이메일')),
                ('deleted_username', models.CharField(blank=True, max_length=150, verbose_name='삭제된 유저의 username')),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='삭제한 사용자')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_members.user_set+', to='contenttypes.ContentType')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '사용자',
                'verbose_name_plural': '사용자 목록',
            },
            managers=[
                ('objects', apps.members.models.base.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='WPSUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('period', models.CharField(choices=[('12', '12기')], max_length=5, verbose_name='기수')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('members.user',),
            managers=[
                ('objects', apps.members.models.wps.WPSUserManager()),
            ],
        ),
    ]
