# Generated by Django 3.0.7 on 2020-06-20 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('code', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('total_duration', models.IntegerField()),
                ('increment', models.IntegerField()),
                ('time_remaining_white', models.DecimalField(decimal_places=3, max_digits=7)),
                ('time_remaining_black', models.DecimalField(decimal_places=3, max_digits=7)),
                ('is_white_moving', models.BooleanField(default=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('black_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='black', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=8)),
                ('index', models.IntegerField()),
                ('duration', models.DecimalField(decimal_places=3, max_digits=7)),
                ('color', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Mossa',
        ),
        migrations.DeleteModel(
            name='Partita',
        ),
        migrations.AddField(
            model_name='game',
            name='moves',
            field=models.ManyToManyField(to='game.Move'),
        ),
        migrations.AddField(
            model_name='game',
            name='white_player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='white', to=settings.AUTH_USER_MODEL),
        ),
    ]
