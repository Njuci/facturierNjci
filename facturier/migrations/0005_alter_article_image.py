# Generated by Django 4.1.7 on 2023-05-03 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturier', '0004_alter_client_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='article'),
        ),
    ]
