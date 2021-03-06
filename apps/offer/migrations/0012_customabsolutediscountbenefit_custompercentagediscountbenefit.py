# Generated by Django 2.1 on 2019-09-14 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0011_auto_20190730_1216'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomAbsoluteDiscountBenefit',
            fields=[
                ('benefit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='offer.Benefit')),
            ],
            options={
                'verbose_name': 'Benefit',
                'verbose_name_plural': 'Benefits',
                'abstract': False,
            },
            bases=('offer.absolutediscountbenefit',),
        ),
        migrations.CreateModel(
            name='CustomPercentageDiscountBenefit',
            fields=[
                ('benefit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='offer.Benefit')),
            ],
            options={
                'verbose_name': 'Benefit',
                'verbose_name_plural': 'Benefits',
                'abstract': False,
            },
            bases=('offer.percentagediscountbenefit',),
        ),
    ]
