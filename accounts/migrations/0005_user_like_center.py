# Generated by Django 4.2.14 on 2024-07-31 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0014_merge_0011_centerreview_user_id_0013_region_city_code'),
        ('accounts', '0004_alter_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='like_center',
            field=models.ManyToManyField(blank=True, to='house.center', verbose_name='저장한 시설'),
        ),
    ]