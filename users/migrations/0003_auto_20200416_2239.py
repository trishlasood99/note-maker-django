# Generated by Django 3.0.4 on 2020-04-16 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200416_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='security_question',
            field=models.IntegerField(choices=[(1, 'What primary school did you attend?'), (2, 'In what town or city did your mother and father meet?'), (3, "What is your mother's maiden name?"), (4, "What was your childhood pet's name?")], default=1),
        ),
    ]
