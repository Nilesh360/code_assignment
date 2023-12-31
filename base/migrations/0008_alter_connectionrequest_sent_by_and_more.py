# Generated by Django 4.2.2 on 2023-09-11 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_connectionrequest_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectionrequest',
            name='sent_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_connection_requests', to=settings.AUTH_USER_MODEL, verbose_name='Sent By'),
        ),
        migrations.AlterField(
            model_name='connectionrequest',
            name='sent_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_connection_requests', to=settings.AUTH_USER_MODEL, verbose_name='Sent To'),
        ),
    ]
