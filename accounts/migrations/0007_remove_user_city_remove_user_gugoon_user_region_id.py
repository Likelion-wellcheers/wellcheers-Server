# Generated by Django 4.2.14 on 2024-08-02 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0016_report_region_id'),
        ('accounts', '0006_remove_user_goon_remove_user_gu_user_gugoon_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='city',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gugoon',
        ),
        migrations.AddField(
            model_name='user',
            name='region_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='house.region', verbose_name='지역'),
        ),
    ]