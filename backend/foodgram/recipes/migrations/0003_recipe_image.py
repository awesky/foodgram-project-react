# Generated by Django 3.2.19 on 2023-06-12 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, upload_to='recipes/', verbose_name='Картинка'),
        ),
    ]