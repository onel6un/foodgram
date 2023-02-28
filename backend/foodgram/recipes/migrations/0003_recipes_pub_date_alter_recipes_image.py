# Generated by Django 4.1.7 on 2023-02-27 13:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20230219_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipes',
            name='pub_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipes',
            name='image',
            field=models.ImageField(blank=True, upload_to='recipes/image/'),
        ),
    ]