# Generated by Django 2.2 on 2019-07-31 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(null='True', upload_to=''),
            preserve_default='True',
        ),
    ]