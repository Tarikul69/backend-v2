# Generated by Django 3.0.10 on 2021-10-25 08:07

import App.models
import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('branch_id', models.AutoField(primary_key=True, serialize=False)),
                ('branch_name', models.CharField(max_length=50)),
                ('doc', models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 25, 13, 37, 8, 440044))),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('college_id', models.AutoField(primary_key=True, serialize=False)),
                ('college_name', models.CharField(max_length=200)),
                ('college_code', models.CharField(max_length=200)),
                ('college_university', models.CharField(max_length=200)),
                ('college_address', models.CharField(max_length=200)),
                ('college_contact', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('College', 'College'), ('School', 'School')], max_length=100)),
                ('doc', models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 25, 13, 37, 8, 439761))),
                ('slug', models.SlugField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('exam_id', models.AutoField(primary_key=True, serialize=False)),
                ('exam_name', models.CharField(max_length=100)),
                ('instructions', tinymce.models.HTMLField()),
                ('duration', models.CharField(max_length=100)),
                ('date', models.DateField(validators=[App.models.validate_date])),
                ('starting_time', models.CharField(max_length=100, validators=[App.models.validate_time])),
                ('ending_time', models.CharField(max_length=100, validators=[App.models.validate_time1])),
                ('is_calc', models.CharField(choices=[('yes', 'yes'), ('no', 'no')], max_length=10)),
                ('doc', models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 25, 13, 37, 8, 441502))),
                ('slug', models.SlugField(blank=True, null=True)),
                ('branch_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.Branch')),
                ('college_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.College')),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('semester_id', models.AutoField(primary_key=True, serialize=False)),
                ('semester_name', models.CharField(max_length=50)),
                ('doc', models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 25, 13, 37, 8, 440573))),
                ('slug', models.SlugField(blank=True, null=True)),
                ('college_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.College')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('subject_id', models.AutoField(primary_key=True, serialize=False)),
                ('subject_name', models.CharField(max_length=50)),
                ('subject_code', models.CharField(max_length=50)),
                ('total_marks', models.IntegerField(default=100, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('doc', models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 25, 13, 37, 8, 440276))),
                ('slug', models.SlugField(blank=True, null=True)),
                ('branch_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.Branch')),
                ('college_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.College')),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('student_name', models.CharField(max_length=50)),
                ('student_email', models.EmailField(max_length=254, unique=True)),
                ('student_phone', models.CharField(max_length=50, unique=True)),
                ('student_address', models.CharField(max_length=200)),
                ('session', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('section', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z')], max_length=100)),
                ('student_password', models.CharField(max_length=100)),
                ('doc', models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 25, 13, 37, 8, 441110))),
                ('slug', models.SlugField(blank=True, null=True)),
                ('branch_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.Branch')),
                ('college_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.College')),
                ('semester_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.Semester')),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('questions', models.TextField()),
                ('option_a', models.CharField(max_length=200)),
                ('option_b', models.CharField(max_length=200)),
                ('option_c', models.CharField(max_length=200)),
                ('option_d', models.CharField(max_length=200)),
                ('answer', models.CharField(max_length=200)),
                ('marks', models.CharField(max_length=200)),
                ('doc', models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 25, 13, 37, 8, 442098))),
                ('slug', models.SlugField(blank=True, null=True)),
                ('branch_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.Branch')),
                ('college_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.College')),
                ('exam_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.Exam')),
                ('subject_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='Proctor',
            fields=[
                ('proctor_id', models.AutoField(primary_key=True, serialize=False)),
                ('proctor_title', models.CharField(choices=[('Mr.', 'Mr.'), ('Mrs.', 'Mrs.')], max_length=50)),
                ('proctor_name', models.CharField(max_length=50)),
                ('proctor_email', models.CharField(max_length=100, unique=True)),
                ('proctor_phone', models.CharField(max_length=100)),
                ('proctor_password', models.CharField(max_length=100)),
                ('assign_section', multiselectfield.db.fields.MultiSelectField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z')], max_length=100)),
                ('doc', models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 25, 13, 37, 8, 440811))),
                ('slug', models.SlugField(blank=True, null=True)),
                ('college_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.College')),
            ],
        ),
        migrations.AddField(
            model_name='exam',
            name='proctor_id',
            field=models.ManyToManyField(to='App.Proctor'),
        ),
        migrations.AddField(
            model_name='exam',
            name='semester_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.Semester'),
        ),
        migrations.AddField(
            model_name='exam',
            name='subject_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.Subject'),
        ),
        migrations.AddField(
            model_name='branch',
            name='college_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.College'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('answer_id', models.AutoField(primary_key=True, serialize=False)),
                ('answer', models.CharField(max_length=200)),
                ('doc', models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 25, 13, 37, 8, 442381))),
                ('slug', models.SlugField(blank=True, null=True)),
                ('exam_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.Exam')),
                ('question_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='question', to='App.Questions')),
                ('student_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.Students')),
            ],
        ),
    ]