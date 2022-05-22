# Generated by Django 4.0 on 2022-05-03 14:31

from django.db import migrations, models
import django.db.models.deletion
import faceid.models
import picklefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loc_name', models.CharField(max_length=100)),
                ('last_updated', models.CharField(default='0002-02-02 00:00:00.000000', max_length=128)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('profile_pic', models.ImageField(upload_to=faceid.models.person_directory_path)),
                ('phone', models.PositiveIntegerField()),
                ('email', models.EmailField(max_length=264, unique=True)),
                ('enrolment_data', picklefield.fields.PickledObjectField(blank=True, editable=False, null=True)),
                ('location', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='faceid.location')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persons', to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sno', models.CharField(max_length=100, unique=True)),
                ('analytics_file', models.FileField(blank=True, upload_to=faceid.models.analytics_directory_path)),
                ('image_file', models.ImageField(blank=True, upload_to=faceid.models.images_directory_path)),
                ('video_file', models.FileField(blank=True, upload_to=faceid.models.videos_directory_path)),
                ('script_file', models.FileField(blank=True, upload_to=faceid.models.script_directory_path)),
                ('location', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='faceid.location')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='auth.user')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
