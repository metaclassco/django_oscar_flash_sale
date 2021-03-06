# Generated by Django 2.0.13 on 2019-07-29 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0009_auto_20190716_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conditionaloffer',
            name='offer_type',
            field=models.CharField(choices=[('Site', 'Site offer - available to all users'), ('Sale', 'Sale offer - for the particular products'), ('Voucher', 'Voucher offer - only available after entering the appropriate voucher code'), ('User', 'User offer - available to certain types of user'), ('Session', 'Session offer - temporary offer, available for a user for the duration of their session')], default='Site', max_length=128, verbose_name='Type'),
        ),
    ]
