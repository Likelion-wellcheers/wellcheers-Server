# Generated by Django 4.2.14 on 2024-07-28 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("house", "0008_cart"),
    ]

    operations = [
        migrations.AddField(
            model_name="center",
            name="thumbnail",
            field=models.ImageField(
                blank=True, null=True, upload_to="", verbose_name="썸네일"
            ),
        ),
        migrations.AddField(
            model_name="region",
            name="thumbnail",
            field=models.ImageField(
                blank=True, null=True, upload_to="", verbose_name="썸네일"
            ),
        ),
    ]