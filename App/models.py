from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import datetime
from django.core.exceptions import ValidationError
import random, string
from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator
alphanumeric = RegexValidator(r'^[0-9a-zA-Z\s]*$', 'Only alphanumeric characters are allowed.')
slug_random = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
from tinymce.models import HTMLField
from multiselectfield import MultiSelectField

# Create your models here.


class College(models.Model):
    college_id = models.AutoField(primary_key=True)
    college_name = models.CharField(max_length=200)
    college_code = models.CharField(max_length=200)
    college_university = models.CharField(max_length=200)
    college_address = models.CharField(max_length=200)
    college_contact = models.CharField(max_length=200)
    type = models.CharField(max_length=100,choices=(('College','College'),('School','School')))
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    doc = models.DateTimeField(default=datetime.now(), blank=True)
    slug = models.SlugField(blank=True,null=True)

    def __str__(self):
        return self.college_name

    def save(self,*args,**kwargs):
        self.slug = slugify(str(slug_random)+'-'+str(self.doc))
        super(College, self).save(*args,**kwargs)


class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=50)
    college_id = models.ForeignKey(College, on_delete=models.CASCADE)
    doc = models.DateTimeField(default=datetime.now(), blank=True)
    slug = models.SlugField(blank=True,null=True)

    def __str__(self):
        return self.branch_name

    def save(self,*args,**kwargs):
        self.slug = slugify(str(slug_random)+'-'+str(self.doc))
        super(Branch, self).save(*args,**kwargs)


class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=50)
    subject_code = models.CharField(max_length=50)
    total_marks = models.IntegerField(default=100, validators=[
        MaxValueValidator(100),
        MinValueValidator(1)
    ])
    branch_id = models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True)
    college_id = models.ForeignKey(College, on_delete=models.CASCADE)
    doc = models.DateTimeField(default=datetime.now(), blank=True)
    slug = models.SlugField(blank=True,null=True)

    def __str__(self):
        return self.subject_name

    def save(self,*args,**kwargs):
        self.slug = slugify(str(slug_random)+'-'+str(self.doc))
        super(Subject, self).save(*args,**kwargs)


class Semester(models.Model):
    semester_id = models.AutoField(primary_key=True)
    semester_name = models.CharField(max_length=50)
    college_id = models.ForeignKey(College, on_delete=models.CASCADE)
    doc = models.DateTimeField(default=datetime.now(), blank=True)
    slug = models.SlugField(blank=True,null=True)

    def __str__(self):
        return self.semester_name

    def save(self,*args,**kwargs):
        self.slug = slugify(str(slug_random)+'-'+str(self.doc))
        super(Semester, self).save(*args,**kwargs)


class Proctor(models.Model):
    proctor_id = models.AutoField(primary_key=True)
    proctor_title = models.CharField(max_length=50,choices=(('Mr.','Mr.'),('Mrs.','Mrs.')))
    proctor_name = models.CharField(max_length=50)
    proctor_email = models.CharField(max_length=100,unique=True)
    proctor_phone = models.CharField(max_length=100)
    proctor_password = models.CharField(max_length=100)
    college_id = models.ForeignKey(College,on_delete=models.CASCADE)
    assign_section = MultiSelectField(max_length=100,choices=(("A", "A"), ("B", "B"),("C","C"),("D","D"),("E","E"),("F","F"),("G","G"),("H","H"),
                                                              ("I","I"),("J","J"),("K","K"),("L","L"),("M","M"),("N","N"),("O","O"),("P","P"),("Q","Q"),
                                                              ("R","R"),("S","S"),("T","T"),("U","U"),("V","V"),("W","W"),("X","X"),("Y","Y"),("Z","Z")))
    doc = models.DateTimeField(default=datetime.now(), blank=True)
    slug = models.SlugField(blank=True,null=True)

    def __str__(self):
        return self.proctor_title+' '+ self.proctor_name

    def save(self,*args,**kwargs):
        self.slug = slugify(str(slug_random)+'-'+str(self.doc))
        super(Proctor, self).save(*args,**kwargs)


class Students(models.Model):
    student_id = models.AutoField(primary_key=True,blank=True)
    student_name = models.CharField(max_length=50)
    student_email = models.EmailField(unique=True)
    student_phone = models.CharField(max_length=50,unique=True)
    student_address = models.CharField(max_length=200)
    session = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    section = models.CharField(max_length=100,choices=(("A", "A"), ("B", "B"),("C","C"),("D","D"),("E","E"),("F","F"),("G","G"),("H","H"),
                                                        ("I","I"),("J","J"),("K","K"),("L","L"),("M","M"),("N","N"),("O","O"),("P","P"),("Q","Q"),
                                                        ("R","R"),("S","S"),("T","T"),("U","U"),("V","V"),("W","W"),("X","X"),("Y","Y"),("Z","Z")))
    student_password = models.CharField(max_length=100)
    college_id = models.ForeignKey(College, on_delete=models.CASCADE)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL,null=True)
    semester_id = models.ForeignKey(Semester, on_delete=models.SET_NULL,null=True)
    doc = models.DateTimeField(default=datetime.now(), blank=True)
    slug = models.SlugField(blank=True,null=True)

    def __str__(self):
        return self.student_name

    def save(self,*args,**kwargs):
        self.slug = slugify(str(slug_random)+'-'+str(self.doc))
        super(Students, self).save(*args,**kwargs)


def validate_date(date):
    validate_date.start_new=date
    if (date < datetime.now().date()):
        raise ValidationError("Date cannot be in the past")
def validate_time(starting_time):
    validate_time.start=starting_time
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    dt_string = now.strftime("%Y-%m-%d")
    if(str(dt_string)==str(validate_date.start_new)):
        if (starting_time<current_time):
            raise ValidationError("starting time is in past")
def validate_time1(ending_time):
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    if(ending_time<current_time):
        raise ValidationError("ending time is in past")
    elif (validate_time.start>ending_time):
        raise ValidationError("ending time is less then starting time")

    
class Exam(models.Model):
    exam_id = models.AutoField(primary_key=True)
    exam_name = models.CharField(max_length=100)
    instructions = HTMLField()
    duration = models.CharField(max_length=100)
    date = models.DateField(validators=[validate_date])
    starting_time = models.CharField(max_length=100,validators=[validate_time])
    ending_time = models.CharField(max_length=100,validators=[validate_time1])
    semester_id = models.ForeignKey(Semester, on_delete=models.SET_NULL,null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL,null=True)
    subject_id = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    proctor_id = models.ManyToManyField(Proctor)
    college_id = models.ForeignKey(College, on_delete=models.CASCADE)
    is_calc = models.CharField(max_length=10,choices=(("yes", "yes"), ("no", "no")))
    doc = models.DateTimeField(default=datetime.now(), blank=True)
    slug = models.SlugField(blank=True,null=True)

    def __str__(self):
        return self.exam_name

    def save(self,*args,**kwargs):
        self.slug = slugify(str(slug_random)+'-'+str(self.doc))
        super(Exam, self).save(*args,**kwargs)


class Questions(models.Model):
    question_id = models.AutoField(primary_key=True)
    questions = models.TextField()
    question_type = models.CharField(max_length=50,choices=(("M","MCQ"),("S","Subjective")))
    option_a = models.CharField(max_length=200,null=True,blank=True)
    option_b = models.CharField(max_length=200,null=True,blank=True)
    option_c = models.CharField(max_length=200,null=True,blank=True)
    option_d = models.CharField(max_length=200,null=True,blank=True)
    answer = models.CharField(max_length=200,null=True,blank=True)
    marks = models.CharField(max_length=200)
    subject_id = models.ForeignKey(Subject, on_delete=models.SET_NULL,null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL,null=True)
    college_id = models.ForeignKey(College, on_delete=models.CASCADE)
    exam_id = models.ForeignKey(Exam, on_delete=models.SET_NULL,null=True)
    doc = models.DateTimeField(default=datetime.now(), blank=True)
    slug = models.SlugField(blank=True,null=True)

    def __str__(self):
        return self.questions

    def save(self,*args,**kwargs):
        self.slug = slugify(str(slug_random)+'-'+str(self.doc))
        super(Questions, self).save(*args,**kwargs)


class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    answer = models.TextField()
    exam_id = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True)
    question_id = models.ForeignKey(Questions,  on_delete=models.SET_NULL,null=True,blank=True,related_name='question')
    student_id = models.ForeignKey(Students,  on_delete=models.SET_NULL,null=True,blank=True)
    doc = models.DateTimeField(default=datetime.now(), blank=True)
    slug = models.SlugField(blank=True,null=True)

    def __str__(self):
        return self.answer+"|"+str(self.student_id)

    def save(self,*args,**kwargs):
        self.slug = slugify(str(slug_random)+'-'+str(self.doc))
        super(Answer, self).save(*args,**kwargs)