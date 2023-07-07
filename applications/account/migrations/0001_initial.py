# Generated by Django 3.2 on 2023-07-07 00:09

import applications.account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('age', models.PositiveSmallIntegerField(verbose_name='Age')),
                ('address', models.CharField(max_length=100, verbose_name='Address')),
                ('phone', models.CharField(max_length=50, verbose_name='Phone number')),
                ('last_name', models.CharField(max_length=100, verbose_name='Last name')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Is admin?')),
                ('first_name', models.CharField(max_length=100, verbose_name='First name')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is active?')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Is staff member?')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='Username')),
                ('birth', models.DateField(verbose_name='Birth')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=10, verbose_name='Gender')),
                ('photo', models.ImageField(default='no-user-photo.png', upload_to=applications.account.models.photo_file_name, verbose_name='Profile photo')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
