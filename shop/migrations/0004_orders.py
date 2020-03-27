# Generated by Django 3.0.4 on 2020-03-24 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.IntegerField(primary_key=True, serialize=False)),
                ('itemjason', models.CharField(max_length=5000)),
                ('name', models.CharField(max_length=256)),
                ('email', models.CharField(max_length=256)),
                ('address', models.CharField(max_length=256)),
                ('city', models.CharField(max_length=256)),
                ('state', models.CharField(max_length=256)),
                ('zip', models.CharField(max_length=256)),
                ('phone', models.CharField(max_length=256)),
            ],
        ),
    ]
