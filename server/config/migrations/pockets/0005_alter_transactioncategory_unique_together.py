# Generated by Django 3.2.2 on 2022-07-15 06:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pockets', '0004_alter_transaction_category'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='transactioncategory',
            unique_together={('user', 'name')},
        ),
    ]
