# Generated by Django 4.2.3 on 2023-12-29 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_favourite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(error_messages={'requared': 'Поле должно быть заполнено'}, max_length=50, verbose_name='Фамилия имя'),
        ),
    ]