# Generated by Django 3.1.6 on 2021-02-06 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('M', 'Mobiles'), ('L', 'Laptops'), ('TW', 'Top Wears'), ('BW', 'Bottom Wears')], max_length=2),
        ),
    ]
