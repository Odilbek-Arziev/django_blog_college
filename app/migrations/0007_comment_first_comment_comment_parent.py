# Generated by Django 5.1.5 on 2025-01-30 13:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_comment_dislikes_comment_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='first_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_comment', to='app.comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='app.comment'),
        ),
    ]
