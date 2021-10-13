# Generated by Django 3.2.7 on 2021-09-26 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Musician',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('instrument', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('release_date', models.DateField()),
                ('num_stars', models.IntegerField()),
                ('music_type', models.CharField(choices=[('0', 'Rock'), ('1', 'Blues'), ('2', 'Jazz'), ('3', 'Metal'), ('4', 'Classic'), ('5', 'Pop'), ('6', 'Electro')], max_length=1)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.musician')),
            ],
        ),
    ]
