# Generated by Django 3.0.7 on 2020-06-28 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_set', '0011_auto_20200625_2000'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.PositiveSmallIntegerField()),
                ('sold_on', models.DateField(auto_now_add=True)),
                ('sum', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]
