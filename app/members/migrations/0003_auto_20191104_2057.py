# Generated by Django 2.2.7 on 2019-11-04 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_user_img_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='deleted_email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='삭제된 유저의 이메일'),
        ),
        migrations.AddField(
            model_name='user',
            name='deleted_username',
            field=models.CharField(blank=True, max_length=150, verbose_name='삭제된 유저의 username'),
        ),
    ]