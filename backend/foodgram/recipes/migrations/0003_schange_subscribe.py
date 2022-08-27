# Generated by Django 2.2.16 on 2022-08-27 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_subscribe_tags_ingredients'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='subscribe',
            name='unique_object',
        ),
        migrations.RenameField(
            model_name='subscribe',
            old_name='subscribing',
            new_name='author',
        ),
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.UniqueConstraint(fields=('author', 'user'), name='unique_object'),
        ),
    ]
