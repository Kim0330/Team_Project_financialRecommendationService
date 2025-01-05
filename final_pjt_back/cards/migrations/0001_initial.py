# Generated by Django 4.2.16 on 2024-11-26 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_company', models.TextField()),
                ('card_type', models.CharField(max_length=50)),
                ('card_name', models.CharField(max_length=50)),
                ('card_url', models.URLField(blank=True, null=True)),
                ('card_img', models.TextField(blank=True, null=True)),
                ('card_benefits_category', models.TextField()),
                ('card_benefits', models.JSONField(blank=True, null=True)),
            ],
        ),
    ]