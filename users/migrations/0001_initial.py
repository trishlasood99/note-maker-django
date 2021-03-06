# Generated by Django 3.0.4 on 2020-04-12 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('user_name', models.CharField(max_length=15)),
                ('email_id', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=15)),
                ('security_question', models.IntegerField(default=1)),
                ('security_ans', models.CharField(max_length=15)),
                ('following', models.TextField(blank=True)),
            ],
        ),
    ]
