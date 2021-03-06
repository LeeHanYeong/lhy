# Generated by Django 2.2.8 on 2019-12-08 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='choice',
            options={'ordering': ('_order',), 'verbose_name': '선택지', 'verbose_name_plural': '선택지 목록'},
        ),
        migrations.AddField(
            model_name='choice',
            name='_order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='choice',
            name='is_text',
            field=models.BooleanField(default=False, verbose_name='주관식'),
        ),
        migrations.AddField(
            model_name='vote',
            name='text',
            field=models.CharField(blank=True, max_length=100, verbose_name='주관식 응답'),
        ),
    ]
