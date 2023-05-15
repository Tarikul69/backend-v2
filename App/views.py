from django.shortcuts import *
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime
from tablib import Dataset
import random, string
from django.core.mail import send_mail
import pandas as pd
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.http import HttpResponse
from weasyprint import HTML, CSS
from django.template.loader import get_template,render_to_string
# Create your views here.

def load_subject(request):
    branch_id = request.GET.get('branch_id')
    subjects = Subject.objects.filter(branch_id=branch_id).all()
    return render(request, 'subject_dropdown_list_options.html', {'subjects': subjects})

@login_required(login_url='logins')
def home(r):
    if r.user.is_superuser:
        return redirect('admin:index')
    data = {
        "user": User.objects.filter(username=r.user),
        "college": College.objects.filter(user_id=r.user)
    }
    return render(r,'home.html',data)

@login_required(login_url='logins')
def branch(r):
    if r.user.is_superuser:
        return redirect('admin:index')
    college = College.objects.get(user_id=r.user)
    br = BranchForm(r.POST or None, r.FILES or None,request=r)
    if r.method == "POST":
        if br.is_valid():
            d = br.save(commit=False)
            d.college_id = College(college.college_id)
            d.save()
            if college.type == 'College':
                messages.success(r, 'Branch added successfully!')
            elif college.type == 'School':
                messages.success(r, 'Class added successfully!')
            return redirect('branch')
    branch = Branch.objects.filter(college_id=college.college_id).order_by('-branch_id')
    paginator = Paginator(branch, 10)
    page_number = r.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {
        "form": br,
        'page_obj': page_obj,
    }
    return render(r,'branch.html',data)

@login_required(login_url='logins')
def subject(r):
    if r.user.is_superuser:
        return redirect('admin:index')
    college = College.objects.get(user_id=r.user)
    if r.is_ajax():
        term = r.GET.get('term')
        if college.type == 'College':
            subject = ['English','Regional Language(s)','Maths','Science','Social Sciences','Physical Education',
                       'Computer Basics','Arts (Drawing)','History','Languages and linguistics','Literature','Performing arts',
                       'Philosophy','Religion and Religious studies','Visual arts','Anthropology','Archaeology','Area Studies',
                       'Cultural and Ethnic Studies','Economics','Gender and Sexuality Studies','Geography','Political Science',
                       'Psychology','Sociology','Chemistry','Earth Sciences','Life Sciences','Physics','Space Sciences','Computer Sciences',
                       'Logic','Mathematics','Statistics','Systems Science','Agriculture','Architecture and Design','Business','Divinity',
                       'Education','Engineering','Environmental Studies and Forestry','Family and Consumer Science','Health Sciences',
                       'Human Physical Performance and Recreation','Journalism, Media Studies and Communication','Law','Library and Museum Studies',
                       'Military Sciences','Public Administration','Social Work','Transportation']
        elif college.type == 'School':
            subject = ['Mathematics','Environmental Studies','Social Studies','English','Hindi','General Knowledge','Science','Sanskrit','Urdu','Computer']
        response = []
        for x in subject:
            if term.lower() in x.lower():
                response.append(x)
        return JsonResponse(response, safe=False)

    college = College.objects.get(user_id=r.user)
    sub = SubjectForm(r.POST or None, r.FILES or None,request=r)
    if r.method == "POST":
        subject_name = r.POST.get('subject_name')
        branch = r.POST.get('branch_id')
        code = r.POST.get('subject_code')
        if Subject.objects.filter(subject_name=subject_name,branch_id=branch,college_id=college.college_id).exists()==True:
            if college.type == 'College':
                messages.success(r, 'Subject already exists in this branch!!')
            elif college.type == 'School':
                messages.success(r, 'Subject already exists in this class!!')
            return redirect('subject')
        elif Subject.objects.filter(subject_code=code,branch_id=branch,college_id=college.college_id).exists()==True:
            if college.type == 'College':
                messages.success(r, 'Subject code already exists in this branch!!')
            elif college.type == 'School':
                messages.success(r, 'Subject code already exists in this class!!')
            return redirect('subject')
        elif sub.is_valid():
            if subject_name == 'Others':
                sub.instance.subject_name = r.POST.get('other_subject')
            else:
                sub.instance.subject_name = subject_name
            sub.instance.college_id = College(college.college_id)
            sub.save()
            messages.success(r, 'Subject added successfully!')
            return redirect('subject')
    subject = Subject.objects.filter(college_id=college.college_id).order_by('-subject_id')
    paginator = Paginator(subject, 10)
    page_number = r.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {
        "form": sub,
        'page_obj': page_obj,
    }
    return render(r,'subject.html',data)

@login_required(login_url='logins')
def semester(r):
    if r.user.is_superuser:
        return redirect('admin:index')
    college = College.objects.get(user_id=r.user)
    sm = SemesterForm(r.POST or None, r.FILES or None,request=r)
    if r.method == "POST":
        if sm.is_valid():
            d = sm.save(commit=False)
            d.college_id = College(college.college_id)
            d.save()
            if college.type == 'College':
                messages.success(r, 'Semester added successfully!')
            elif college.type == 'School':
                messages.success(r, 'Section added successfully!')
            return redirect('semester')
    semester = Semester.objects.filter(college_id=college.college_id).order_by('-semester_id')
    paginator = Paginator(semester, 10)
    page_number = r.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {
        "form": sm,
        'page_obj': page_obj,
    }
    return render(r,'semester.html',data)


def check_time(start,end,semester,branch,date,college_id):
    exam = Exam.objects.filter(date=date, semester_id=semester, branch_id=branch,college_id=college_id)
    if exam.exists() == True:
        for e in exam:
            if (start.strftime("%H:%M") <= e.starting_time <= end.strftime("%H:%M")) == True:
                return True
            elif (start.strftime("%H:%M") <= e.ending_time <= end.strftime("%H:%M")) == True:
                return True
            elif (e.starting_time <= start.strftime("%H:%M") <= e.ending_time) == True:
                return True
            elif (e.starting_time <= end.strftime("%H:%M") <= e.ending_time) == True:
                return True
            else:
                return False
    elif exam.exists() == False:
        return False


def check_time_edit(start,end,semester,branch,date,college_id,exclude):
    exam = Exam.objects.filter(date=date, semester_id=semester, branch_id=branch,college_id=college_id).exclude(exam_id=exclude)
    if exam.exists() == True:
        for e in exam:
            if (start.strftime("%H:%M") <= e.starting_time <= end.strftime("%H:%M")) == True:
                return True
            elif (start.strftime("%H:%M") <= e.ending_time <= end.strftime("%H:%M")) == True:
                return True
            elif (e.starting_time <= start.strftime("%H:%M") <= e.ending_time) == True:
                return True
            elif (e.starting_time <= end.strftime("%H:%M") <= e.ending_time) == True:
                return True
            else:
                return False
    elif exam.exists() == False:
        return False

@login_required(login_url='logins')
def exam_add(r):
    if r.user.is_superuser:
        return redirect('admin:index')

    if r.is_ajax():
        term = r.GET.get('term')
        exam = ["Math", "Physics", "English","Mathematics","Science","Verbal Ability",
                "Pre-assessment","Formative assessment","Summative assessment","Unit Test",
                "Entrance Examination","Competitive Examination","Social Science","Hindi",
                "Annual Final","Quiz"]
        response = []
        for x in exam:
            if term.lower() in x.lower():
                response.append(x)
        return JsonResponse(response, safe=False)

    college = College.objects.get(user_id=r.user)
    ex = ExamForm(r.POST or None, r.FILES or None,request=r)

    if r.method == "POST":
        start_time = r.POST.get('starting_time')
        ending_time = r.POST.get('ending_time')
        end = pd.to_datetime(ending_time)
        start = pd.to_datetime(start_time)
        duration = end - start
        total_duration = int(duration.total_seconds() / 60)
        date = datetime.strptime(r.POST.get('date'), '%Y-%m-%d').date()
        check_exists_time = check_time(start, end, r.POST.get('semester_id'), r.POST.get('branch_id'), date,
                                       college.college_id)
        subject_name = Subject.objects.get(subject_id=r.POST.get('subject_id'))

        try:
            # if today exam subject already exists.
            cond1 = Q(date=date) & Q(semester_id=r.POST.get('semester_id')) & Q(branch_id=r.POST.get('branch_id')) & Q(
                subject_id=r.POST.get('subject_id'))
            # if today exam time already exists.
            cond2 = Q(date=date) & Q(semester_id=r.POST.get('semester_id')) & Q(branch_id=r.POST.get('branch_id'))

            if Exam.objects.filter(cond1, college_id=college.college_id).exists() == True:
                messages.error(r, 'Today this subject exam already exists!')
                return redirect('exam_add')
            elif Exam.objects.filter(cond2,
                                     college_id=college.college_id).exists() == True and check_exists_time == True:
                messages.error(r, 'Today this time exam already exists!')
                return redirect('exam')
            elif total_duration < 5:
                messages.error(r, 'Minimum duration is 5 Minutes!')
                return redirect('exam_add')
            try:
                if ex.is_valid():
                    exam_name = r.POST.get('exam_name')
                    if exam_name == 'Others':
                        ex.instance.exam_name = r.POST.get('other')
                    else:
                        ex.instance.exam_name = exam_name
                    ex.instance.duration = total_duration
                    ex.instance.college_id = College(college.college_id)
                    ex.save()

                    # #send mail to students
                    students = Students.objects.filter(semester_id=r.POST.get('semester_id'),
                                                       branch_id=r.POST.get('branch_id'), college_id=college.college_id)
                    for student in students:
                        subject = "Confirmation of Examination Scheduled"
                        message = f"Dear Student, \n\nGreetings from Engage and Reap!!! \nYour exam has been scheduled. Please click on the below link for appearing in the exam.\nURL: https://enr-online-exam.herokuapp.com \nExam Name: {r.POST.get('exam_name')} \nSubject: {subject_name.subject_name} \nDate: {r.POST.get('date')} \nStarting Time: {start_time} \nEnding Time: {ending_time} \n\nWe wish you all the very best!!! \n\nThanking You \nEnR Team"
                        sender = 'info@engagenreap.com'
                        send_mail(subject, message, sender, [student.student_email], fail_silently=False)

                    # send mail to proctors
                    proctor_list = r.POST.getlist('proctor_id')
                    for proctors in proctor_list:
                        proctor = Proctor.objects.get(proctor_id=int(proctors), college_id=college.college_id)
                        subject = "Assigned as Proctor for Exam"
                        message = f"Hi {proctor.proctor_name}, \nYou are assigned as an invigilator for this examination. \nPlease click on the link and login with the given credentials at https://enr-online-exam.herokuapp.com\nExam Name: {r.POST.get('exam_name')} \nSubject: {subject_name.subject_name}\nDate: {r.POST.get('date')}\nStarting Time: {start_time} \nEnding Time: {ending_time} \n\nThanking You \nEnR Team"
                        sender = 'info@engagenreap.com'
                        send_mail(subject, message, sender, [proctor.proctor_email], fail_silently=False)

                    messages.success(r, 'Exam added  successfully!')
                    return redirect('exam')
            except:
                pass
        except:
            pass

    data = {
        "form": ex,
    }
    return render(r, 'exam_add.html', data)


@login_required(login_url='logins')
def exam(r):
    if r.user.is_superuser:
        return redirect('admin:index')

    college = College.objects.get(user_id=r.user)
    exam = Exam.objects.filter(college_id=college.college_id).order_by('-exam_id')
    paginator = Paginator(exam, 10)
    page_number = r.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {
        'page_obj': page_obj,
    }
    return render(r,'exam.html',data)


@login_required(login_url='logins')
def proctor(r):
    if r.user.is_superuser:
        return redirect('admin:index')
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    college = College.objects.get(user_id=r.user)
    form = ProctorForm(r.POST or None, r.FILES or None)
    if r.method == "POST":
        if form.is_valid():
            form.instance.college_id = College(college.college_id)
            form.instance.proctor_password = password
            form.save()
            subject = "Assigned as Proctor for Exam"
            message = f"Dear User, \n\nGreetings from Engage and Reap!!! \nYou have been assigned as a proctor and you need to monitor the activity of student and help them if they are facing any issue.Please click on the below link and log in with the below credentials. \n\nURL: https://enr-online-exam.herokuapp.com \nUsername: {r.POST.get('proctor_email')} \nPassword: {password}\n\nThanking You\nEnR Team"
            sender = 'info@engagenreap.com'
            send_mail(subject, message, sender, [r.POST.get('proctor_email')], fail_silently=False)
            messages.success(r, 'Proctor added successfully!')
            return redirect('proctor')
    proctor = Proctor.objects.filter(college_id=college.college_id).order_by('-proctor_id')
    paginator = Paginator(proctor, 10)
    page_number = r.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {
        "form": form,
        'page_obj': page_obj
    }
    return render(r,'proctor.html',data)

@login_required(login_url='logins')
def students(r):
    if r.user.is_superuser:
        return redirect('admin:index')
    college = College.objects.get(user_id=r.user)
    students = Students.objects.filter(college_id=college.college_id).order_by('-student_id')
    paginator = Paginator(students, 10)
    page_number = r.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {
        'page_obj': page_obj
    }
    return render(r,'students.html',data)


@login_required(login_url='logins')
def student_add(r):
    if r.user.is_superuser:
        return redirect('admin:index')
    college = College.objects.get(user_id=r.user)
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    form = StudentManualForm(r.POST or None,request=r)
    if r.method == 'POST':
        if form.is_valid():
            form.instance.college_id = College(college.college_id)
            form.instance.proctor_password = password
            if college.type == 'School':
                semester = Semester.objects.get(semester_id=r.POST.get('semester_id'))
                form.instance.section = Semester(semester.semester_name)
            form.save()
            subject = "Credential Generated for Examination"
            message = f"Dear Student, \n\nGreetings from Engage and Reap!!! \nYour credentials has been generated and you will be soon notified about your exam with proper date and time. This is the credential that you are required to use while logging in for the exam.\nURL: https://enr-online-exam.herokuapp.com \nUsername: {r.POST.get('student_email')} \nPassword: {password} \n\nWe wish you all the very best!!!\n\nThanking You\nEnR Team"
            sender = 'info@engagenreap.com'
            send_mail(subject, message, sender, [r.POST.get('student_email')], fail_silently=False)
            messages.success(r, 'Student added successfully!')
            return redirect('students')
    data = {
        'form':list(form)
    }
    return render(r,'student_add.html',data)

def logins(r):
    form = LoginForm(r.POST or None)
    if r.method == 'POST':
        if form.is_valid:
            email = r.POST['email']
            password = r.POST['password']
            try:
                username = User.objects.get(email=email.lower()).username
                user = authenticate(username=username,password=password)
                if user is not None:
                    login(r, user)
                    if user.is_superuser:
                        return redirect('admin:index')
                    return redirect('home')
                else:
                    messages.error(r,"Your password is incorrect!")
                    return redirect('logins')

            except User.DoesNotExist:
                messages.error(r,"The email address or password is incorrect. Please retry...")
                return redirect('logins')

    data = {"form": form}
    return render(r, 'signin.html', data)

def logouts(r):
    logout(r)
    return redirect('logins')

@login_required(login_url='logins')
def password_change(r):
    if r.user.is_superuser:
        return redirect('admin:index')
    if r.method == 'POST':
        form = PasswordChangeForm(r.user, r.POST or None)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(r, user)  # Important!
            messages.success(r, 'Your password is successfully updated!')
            return redirect('password_change')
        else:
            messages.error(r, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(r.user)
    data = {
        "form":form,
    }
    return render(r, 'password_change.html', data)

@login_required(login_url='logins')
def upload_data(r):
    if r.user.is_superuser:
        return redirect('admin:index')
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    college = College.objects.get(user_id=r.user)
    if r.method == 'POST':
        dataset = Dataset()
        new_file = r.FILES['upload_file']
        imported_data = dataset.load(new_file.read(), format='xlsx')
        for data in imported_data:
            try:
                if len(data) != 9:
                    messages.error(r, 'Your file indexing is out of range or less!')
                    return redirect('upload_data')
                else:
                    if Students.objects.filter(student_email=data[1], college_id=college.college_id).exists() == True:
                        messages.error(r, 'Duplicate email exist!')
                        return redirect('upload_data')
                    elif Students.objects.filter(student_phone=data[2], college_id=college.college_id).exists() == True:
                        messages.error(r, 'Duplicate phone exist!')
                        return redirect('upload_data')
                    else:
                        value = Students()
                        value.student_name = data[0]
                        value.student_email = data[1]
                        value.student_phone = data[2]
                        value.student_address = data[3]
                        value.session = data[4]
                        value.country = data[5]
                        value.state = data[6]
                        value.city = data[7]
                        value.section = data[8]
                        value.student_password = password
                        value.branch_id = Branch(r.POST.get('branch_id'))
                        if college.type == 'College':
                            value.semester_id = Semester(r.POST.get('semester_id'))
                        elif college.type == 'School':
                            check_semester = Semester.objects.filter(semester_name=data[8],college_id=college.college_id)
                            if check_semester.exists() == True:
                                value.semester_id = Semester(check_semester[0].semester_id)
                            else:
                                semester = Semester.objects.create(semester_name=data[8], college_id=College(college.college_id))
                                value.semester_id = Semester(semester.semester_id)
                        value.college_id = College(college.college_id)
                        value.save()
                        subject = "Credential Generated for Examination"
                        message = f"Dear Student, \n\nGreetings from Engage and Reap!!! \nYour credentials has been generated and you will be soon notified about your exam with proper date and time. This is the credential that you are required to use while logging in for the exam.\nURL: https://enr-online-exam.herokuapp.com \nUsername: {data[1]} \nPassword: {password} \n\nWe wish you all the very best!!!\n\nThanking You\nEnR Team"
                        sender = 'info@engagenreap.com'
                        send_mail(subject, message, sender, [data[1]], fail_silently=False)
            except (IndexError, AttributeError):
                messages.error(r,'Please check file indexing format "OR" rows and columns is Duplicate or Empty!')
                return redirect('upload_data')
        messages.success(r, 'Your Students File successfully upload!')
        return redirect('students')
    st = StudentForm(r.POST or None,request=r)
    ex = QuestionForm(r.POST or None)
    data = {
        "question": ex,
        "student": st,
        "branch": Branch.objects.filter(college_id=college.college_id)
    }
    return render(r, 'upload_data.html',data)

@login_required(login_url='logins')
def upload_questions(r):
    if r.user.is_superuser:
        return redirect('admin:index')
    college = College.objects.get(user_id=r.user)
    if r.method == 'POST':
        dataset = Dataset()
        new_file = r.FILES['upload_questions']
        imported_data = dataset.load(new_file.read(), format='xlsx')
        for data in imported_data:
            try:
                type = r.POST.get('question_type')
                if type == 'M':
                    if len(data) != 7:
                        messages.error(r, 'Your file indexing is out of range or less!')
                        return redirect('upload_data')
                    else:
                        value = Questions()
                        value.questions = data[0]
                        value.option_a = data[1]
                        value.option_b = data[2]
                        value.option_c = data[3]
                        value.option_d = data[4]
                        value.answer = data[5]
                        value.marks = data[6]
                        value.college_id = College(college.college_id)
                        value.exam_id = Exam(r.POST.get('exam_id'))
                        exam = Exam.objects.get(exam_id=r.POST.get('exam_id'))
                        value.branch_id = Branch(exam.branch_id.branch_id)
                        value.subject_id = Subject(exam.subject_id.subject_id)
                        value.question_type = type
                        value.save()
                elif type == 'S':
                    if len(data) != 2:
                        messages.error(r, 'Your file indexing is out of range or less!')
                        return redirect('upload_data')
                    else:
                        value = Questions()
                        value.questions = data[0]
                        value.marks = data[1]
                        value.college_id = College(college.college_id)
                        value.exam_id = Exam(r.POST.get('exam_id'))
                        exam = Exam.objects.get(exam_id=r.POST.get('exam_id'))
                        value.branch_id = Branch(exam.branch_id.branch_id)
                        value.subject_id = Subject(exam.subject_id.subject_id)
                        value.question_type = type
                        value.save()
                else:
                    messages.error(r, 'This question type not match!')
                    return redirect('upload_data')
            except (IndexError, AttributeError):
                messages.error(r,'Please check file indexing format "OR" rows and columns is Empty!')
                return redirect('upload_data')
        messages.success(r, 'Your Questions File successfully upload!')
        return redirect("../exam_view/" + str(exam.exam_id))
    form = QuestionForm(r.POST or None)
    data = {
        "question":form,
    }
    return render(r, 'upload_data.html',data)

@login_required(login_url=logins)
def update_college(r,c_id):
    if r.user.is_superuser:
        return redirect('admin:index')
    user = User.objects.get(username=r.user)
    college = College.objects.get(college_id=c_id)
    clg_form = UpdateCollege(r.POST or None, instance=college)
    user_form = UpdateUser(r.POST or None, instance=user)
    if r.method == "POST":
        if user_form.is_valid() and clg_form.is_valid():
            user_form.save()
            clg_form.save()
            return redirect('home')
    else:
        user_form = UpdateUser(instance=user)
        clg_form = UpdateCollege(instance=college)
    data = {
        "college": clg_form,
        "user": user_form,
    }
    return render(r,'update_college.html',data)

@login_required(login_url='logins')
def student_view(r,st_id):
    if r.user.is_superuser:
        return redirect('admin:index')
    student = Students.objects.get(student_id=st_id)
    form = StudentManualForm(r.POST or None,instance=student,request=r)
    if r.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("../student_view/" + str(student.student_id))
        else:
            form = StudentManualForm(instance=student,request=r)

    data = {
        "student": Students.objects.filter(student_id=st_id),
        "form": form,
    }
    return render(r,'student_view.html',data)

@login_required(login_url='logins')
def proctor_view(r,pr_id):
    if r.user.is_superuser:
        return redirect('admin:index')
    proctor = Proctor.objects.get(proctor_id=pr_id)
    form = ProctorForm(r.POST or None,instance=proctor)
    if r.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("../proctor_view/" + str(proctor.proctor_id))
        else:
            form = ProctorForm(instance=proctor)

    data = {
        "proctor": Proctor.objects.filter(proctor_id=pr_id),
        "form": form,
    }
    return render(r, 'proctor_view.html', data)

@login_required(login_url='logins')
def exam_view(r,ex_id):
    if r.user.is_superuser:
        return redirect('admin:index')

    data = {
        "exam": Exam.objects.filter(exam_id=ex_id),
        "questions": Questions.objects.filter(exam_id=ex_id).order_by('-question_id')
    }
    return render(r, 'exam_view.html', data)


@login_required(login_url='logins')
def question_add(r,ex_id):
    if r.user.is_superuser:
        return redirect('admin:index')
    college = College.objects.get(user_id=r.user)
    exam = Exam.objects.get(exam_id=ex_id)
    type = r.GET.get('type')
    form = QuestionManualForm(r.POST or None,type=type)
    if type == 'MCQ':
        question_type = 'M'
    elif type == 'Subjective':
        question_type = 'S'
    if r.method == 'POST':
        if form.is_valid():
            form.instance.college_id = College(college.college_id)
            form.instance.exam_id = Exam(ex_id)
            form.instance.branch_id = Branch(exam.branch_id.branch_id)
            form.instance.subject_id = Subject(exam.subject_id.subject_id)
            form.instance.question_type = question_type
            form.save()
            messages.success(r, 'Question added successfully!')
            return redirect("../exam_view/" + str(exam.exam_id))
    data = {
        'form': list(form)
    }
    return render(r, 'question_add.html', data)



@login_required(login_url='logins')
def question_view(r,qs_id):
    if r.user.is_superuser:
        return redirect('admin:index')
    question = Questions.objects.get(question_id=qs_id)
    if question.question_type == 'M':
        type = 'MCQ'
    elif question.question_type == 'S':
        type = 'Subjective'
    form = QuestionManualForm(r.POST or None,type=type,instance=question)
    if r.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("../question_view/" + str(question.question_id))
        else:
            form = QuestionManualForm(instance=question)

    data = {
        "question": Questions.objects.filter(question_id=qs_id),
        "form": form,
    }
    return render(r,'question_view.html',data)


@login_required(login_url='logins')
def exam_update(r,ex_id):
    if r.user.is_superuser:
        return redirect('admin:index')
    exam = Exam.objects.get(exam_id=ex_id)
    college = College.objects.get(user_id=r.user)
    form1 = ExamForm1(r.POST or None,instance=exam)
    form2 = ExamForm2(r.POST or None,instance=exam)
    form3 = ExamForm3(r.POST or None,instance=exam,request=r)
    if r.method == "POST":
        start_time = r.POST.get('starting_time')
        ending_time = r.POST.get('ending_time')
        end = pd.to_datetime(ending_time)
        start = pd.to_datetime(start_time)
        duration = end - start
        total_duration = int(duration.total_seconds() / 60)
        date = datetime.strptime(r.POST.get('date'), '%Y-%m-%d').date()
        check_exists_time = check_time_edit(start, end, r.POST.get('semester_id'), r.POST.get('branch_id'), date,college.college_id,ex_id)
        # if today exam subject already exists.
        cond1 = Q(date=date) & Q(semester_id=r.POST.get('semester_id')) & Q(branch_id=r.POST.get('branch_id')) & Q(
            subject_id=r.POST.get('subject_id'))
        # if today exam time already exists.
        cond2 = Q(date=date) & Q(semester_id=r.POST.get('semester_id')) & Q(branch_id=r.POST.get('branch_id'))

        if Exam.objects.filter(cond1,college_id=college.college_id).exclude(exam_id=ex_id).exists() == True:
            messages.error(r, 'Today this subject exam already exists!')
            return redirect("../exam_update/" + str(exam.exam_id))
        elif Exam.objects.filter(cond2,college_id=college.college_id).exclude(exam_id=ex_id).exists() == True and check_exists_time == True:
            messages.error(r, 'Today this time exam already exists!')
            return redirect("../exam_update/" + str(exam.exam_id))
        if total_duration < 5:
            messages.error(r, 'Minimum duration is 5 Minutes!')
            return redirect("../exam_update/" + str(exam.exam_id))

        elif form1.is_valid() and form2.is_valid() and form3.is_valid():
            form3.instance.exam_name = r.POST.get('exam_name')
            form3.instance.duration = total_duration
            form1.save()
            form2.save()
            form3.save()
            return redirect("../exam_view/" + str(exam.exam_id))
    else:
        form1 = ExamForm1(instance=exam)
        form2 = ExamForm2(instance=exam)
        form3 = ExamForm3(instance=exam,request=r)

    data = {
        "exam": Exam.objects.filter(exam_id=ex_id),
        "form1": form1,
        "form2": form2,
        "form3": form3,
    }
    return render(r,'exam_update.html', data)


@login_required(login_url='logins')
def branch_update(r,br_id):
    if r.user.is_superuser:
        return redirect('admin:index')
    branch = Branch.objects.get(branch_id=br_id)
    form = BranchForm(r.POST or None,instance=branch,request=r)
    if r.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('branch')
    else:
        form = BranchForm(instance=branch,request=r)

    data = {
        "form": form,
    }
    return render(r, 'branch_update.html', data)

@login_required(login_url='logins')
def subject_update(r,su_id):
    if r.user.is_superuser:
        return redirect('admin:index')
    subject = Subject.objects.get(subject_id=su_id)
    form = SubjectForm(r.POST or None,instance=subject,request=r)
    if r.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('subject')
    else:
        form = SubjectForm(instance=subject,request=r)

    data = {
        "form": form,
        "subject":subject
    }
    return render(r, 'subject_update.html', data)

@login_required(login_url='logins')
def semester_update(r,sem_id):
    if r.user.is_superuser:
        return redirect('admin:index')
    semester = Semester.objects.get(semester_id=sem_id)
    form = SemesterForm(r.POST or None,instance=semester,request=r)
    if r.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('semester')
    else:
        form = SemesterForm(instance=semester,request=r)

    data = {
        "form": form,
    }
    return render(r, 'semester_update.html', data)

@login_required(login_url=logins)
def subject_delete(r,dl_id):
    if r.user.is_superuser:
        return redirect('admin:index')
    query = Subject.objects.get(subject_id=dl_id)
    query.delete()
    return redirect('subject')\

@login_required(login_url=logins)
def branch_delete(r,dl_id):
    if r.user.is_superuser:
        return redirect('admin:index')
    query = Branch.objects.get(branch_id=dl_id)
    query.delete()
    return redirect('branch')

@login_required(login_url=logins)
def semester_delete(r,dl_id):
    if r.user.is_superuser:
        return redirect('admin:index')
    query = Semester.objects.get(semester_id=dl_id)
    query.delete()
    return redirect('semester')

@login_required(login_url=logins)
def exam_delete(r,dl_id):
    if r.user.is_superuser:
        return redirect('admin:index')
    query = Exam.objects.get(exam_id=dl_id)
    query.delete()
    return redirect('exam')

@login_required(login_url=logins)
def question_delete(r,dl_id):
    if r.user.is_superuser:
        return redirect('admin:index')
    query = Questions.objects.get(question_id=dl_id)
    exam_id = query.exam_id.exam_id
    query.delete()
    return redirect("../exam_view/" + str(exam_id))

@login_required(login_url=logins)
def student_delete(r,dl_id):
    if r.user.is_superuser:
        return redirect('admin:index')
    query = Students.objects.get(student_id=dl_id)
    query.delete()
    return redirect('students')

@login_required(login_url=logins)
def proctor_delete(r,dl_id):
    if r.user.is_superuser:
        return redirect('admin:index')
    query = Proctor.objects.get(proctor_id=dl_id)
    query.delete()
    return redirect('proctor')

@login_required(login_url=logins)
def exam_done(r):
    if r.user.is_superuser:
        return redirect('admin:index')
    college = College.objects.get(user_id=r.user)

    exam_done = []
    exam = Exam.objects.filter(college_id=college.college_id)
    for e in exam:
        exam_exist = Answer.objects.filter(exam_id = e.exam_id).count()
        if exam_exist != 0:
            exam_done.append(e)

    paginator = Paginator(exam_done, 10)
    page_number = r.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {
        'page_obj': page_obj
    }

    return render(r,'exam_done.html',data)


@login_required(login_url=logins)
def exam_attend_students(r,ex_id):
    if r.user.is_superuser:
        return redirect('admin:index')
    college = College.objects.get(user_id=r.user)

    students = []
    check_attend = Answer.objects.filter(exam_id=ex_id)
    for a in check_attend:
        try:
            student = Students.objects.get(student_id=a.student_id.student_id,college_id=college.college_id)
            students.append(student)
        except:
            pass

    students = list(set(students))
    paginator = Paginator(students, 10)
    page_number = r.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {
        'page_obj': page_obj,
        'exam_id': int(ex_id)
    }
    return render(r, 'exam_attend_students.html',data)

@login_required(login_url=logins)
def student_answer_demo(r,std_id,ex_id):
    if r.user.is_superuser:
        return redirect('admin:index')

    sort = r.GET.get('sort')
    answer = Answer.objects.filter(student_id=std_id,exam_id=ex_id)
    paginator = Paginator(answer, sort)
    page_number = r.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {
        'page_obj': page_obj,
        'std_id':std_id,
        'ex_id':ex_id,
        'sort':sort
    }
    return render(r, 'student_answer_demo.html',data)


def total_mark(exam_id):
    marks = 0
    try:
        question = Questions.objects.filter(exam_id=exam_id, question_type='M')
        for q in question:
            marks += int(q.marks)
    except:
        pass
    return marks

def obtained_mark(student_id,exam_id):
    answer = Answer.objects.filter(exam_id=exam_id,student_id=student_id)
    marks = 0
    for a in answer:
        if a.question_id != None:
            if a.question_id.answer != None:
                if a.answer.lower() == a.question_id.answer.lower():
                    marks += int(a.question_id.marks)
        else:
            marks = 0
    return marks

@login_required(login_url=logins)
def send_test_result(r,ex_id):
    if r.user.is_superuser:
        return redirect('admin:index')
    college = College.objects.get(user_id=r.user)
    exam = Exam.objects.get(exam_id=ex_id)
    students = []
    check_attend = Answer.objects.filter(exam_id=ex_id)
    for a in check_attend:
        student = Students.objects.get(student_id=a.student_id.student_id,college_id=college.college_id)
        students.append(student)

    students = list(set(students))
    #send mail to students result
    for student in students:
        subject = f"Exam Result Decleared >> {exam.exam_name}"
        message = f"Hi,{student.student_name}\n\nGreetings from Engage and Reap!!!\nYou have successfully attempted the exam {exam.exam_name} held on {exam.date}.\nOut of {total_mark(exam.exam_id)} you got {obtained_mark(student.student_id, exam.exam_id)} in questions correct of MCQ.\nKeep working hard!!!. We wish you all the very best!\n\nThanking You\nEnR Team"
        sender = 'info@engagenreap.com'
        send_mail(subject, message, sender, [student.student_email], fail_silently=False)
    return redirect('exam_done')


# Opens up page as PDF
@login_required(login_url=logins)
def viewPdf(r,std_id,ex_id):
    student = Students.objects.get(student_id=std_id)
    exam = Exam.objects.get(exam_id=ex_id)
    data = {
        'student_answer': Answer.objects.filter(student_id=std_id, exam_id=ex_id),
        'student': student,
        'exam': exam
    }
    html_string = render_to_string('student_answer_pdf.html', data)
    html = HTML(string=html_string).write_pdf()
    filename = student.student_name + "(" + exam.exam_name + ")" + ".pdf"
    response = HttpResponse(html, content_type='application/pdf')
    response['Content-Disposition'] = 'filename=%s' % filename
    return response


# Automaticly downloads to PDF file
@login_required(login_url=logins)
def downloadPdf(r,std_id,ex_id):
    student = Students.objects.get(student_id=std_id)
    exam = Exam.objects.get(exam_id=ex_id)
    data = {
        'student_answer': Answer.objects.filter(student_id=std_id, exam_id=ex_id),
        'student': student,
        'exam': exam
    }
    html_string = render_to_string('student_answer_pdf.html', data)
    html = HTML(string=html_string).write_pdf()
    filename = student.student_name + "(" + exam.exam_name + ")" + ".pdf"
    response = HttpResponse(html, content_type='application/pdf')
    content = "attachment; filename=%s" % (filename)
    response['Content-Disposition'] = content
    return response


