# Generated by Django 2.2.5 on 2019-09-27 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('what', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memos',
            name='images',
            field=models.ImageField(blank=True, upload_to='usr'),
        ),
        migrations.AlterField(
            model_name='memos',
            name='text2',
            field=models.TextField(max_length=150),
        ),
        migrations.AlterField(
            model_name='memos',
            name='text3',
            field=models.TextField(max_length=150),
        ),
    ]
