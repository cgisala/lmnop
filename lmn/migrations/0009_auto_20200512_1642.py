# Generated by Django 3.0.4 on 2020-05-12 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmn', '0008_merge_20200511_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.ImageField(default='default.jpg', upload_to='user-images-lmnop'),
        ),
    ]