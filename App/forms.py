import requests
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django import forms


class LoginForm(ModelForm):
    class Meta:
        model = User
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control','type':'password'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','type':'email','required':True}),
        }
        fields = ['email','password',]


class ProctorForm(ModelForm):
    class Meta:
        model = Proctor
        widgets = {
            'proctor_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'proctor_phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'assign_section': forms.SelectMultiple(attrs={'class': 'form-control '}),
            'proctor_name':forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[A-Za-z ]+', 'title':'Enter Characters Only '})
        }
        labels = {
            'proctor_name': 'Proctor Name',
            'proctor_phone': 'Proctor Mobile No.',
            'proctor_email': 'Proctor Email'
        }
        exclude = ['college_id','doc','slug','proctor_password']

    def __init__(self, *args, **kwargs):
        super(ProctorForm, self).__init__(*args, **kwargs)
        self.fields["assign_section"].label = "Assign Section"
        self.fields["proctor_title"].choices = [("", "Choose"),] + list(self.fields["proctor_title"].choices)[1:]
        self.fields["proctor_title"].label = "Proctor Title"


class BranchForm(ModelForm):
    class Meta:
        model = Branch
        exclude = ['college_id','doc','slug']
        widgets = {
            'branch_name':forms.TextInput(attrs={'class':'form-control'})

        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        college = College.objects.get(user_id=request.user)
        super(BranchForm, self).__init__(*args, **kwargs)
        if college.type == 'College':
            self.fields['branch_name'].label = "Branch Name"
        elif college.type == 'School':
            self.fields['branch_name'].label = "Class"


class SemesterForm(ModelForm):
    class Meta:
        model = Semester
        exclude = ['college_id','doc','slug']
        widgets = {
            'semester_name':forms.TextInput(attrs={'class':'form-control'})

        }
        labels = {
            'semester_name':'Semester Name'
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        college = College.objects.get(user_id=request.user)
        super(SemesterForm, self).__init__(*args, **kwargs)
        if college.type == 'College':
            self.fields['semester_name'].label = "Semester Name"
        elif college.type == 'School':
            self.fields['semester_name'].label = "Section"


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        widgets = {
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'total_marks': 'Total Marks',
            'subject_code': 'Subject Code'
        }
        exclude = ['college_id','doc','slug','subject_name']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        college = College.objects.get(user_id=request.user)
        super(SubjectForm, self).__init__(*args, **kwargs)
        if college.type == 'College':
            self.fields['branch_id'].label = "Branch Name"
        elif college.type == 'School':
            self.fields['branch_id'].label = "Class"
        self.fields['branch_id'].empty_label = 'Choose'


class ExamForm(ModelForm):
    class Meta:
        model = Exam
        widgets = {
            'proctor_id': forms.SelectMultiple(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'type':"date",'class': 'form-control'}),
            'starting_time': forms.TimeInput(attrs={'type':"time",'class': 'form-control'}),
            'ending_time': forms.TimeInput(attrs={'type':"time",'class': 'form-control'}),
        }
        labels = {
            'starting_time':'Start Time',
            'ending_time':'End Time'
        }
        exclude = ['college_id','doc','slug','duration','exam_name']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        college = College.objects.get(user_id=request.user)
        super(ExamForm, self).__init__(*args, **kwargs)
        if college.type == 'College':
            self.fields['semester_id'].label = "Semester Name"
            self.fields['branch_id'].label = "Branch Name"
        elif college.type == 'School':
            self.fields['semester_id'].label = "Section"
            self.fields['branch_id'].label = "Class"
        self.fields['semester_id'].empty_label = 'Choose'
        self.fields['subject_id'].label = "Subject Name"
        self.fields['subject_id'].empty_label = 'Choose'
        self.fields['branch_id'].empty_label = 'Choose'
        self.fields['is_calc'].label = "Is Calculator Required!."
        self.fields["is_calc"].choices = [("", "Choose"),] + list(self.fields["is_calc"].choices)[1:]
        self.fields['proctor_id'].label = "Proctor"

        self.fields['subject_id'].queryset = Subject.objects.none()
        if 'branch_id' in self.data:
            try:
                branch_id = int(self.data.get('branch_id'))
                self.fields['subject_id'].queryset = Subject.objects.filter(branch_id=branch_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subject_id'] = forms.ModelChoiceField(queryset=Subject.objects.filter(branch_id=self.instance.branch_id))
            self.fields['subject_id'].initial = self.instance.subject_id
            self.fields['subject_id'].empty_label = 'Choose'
            self.fields['subject_id'].label = 'Subject Name'


class ExamForm1(ModelForm):
    class Meta:
        model = Exam
        fields = ['instructions']


class ExamForm2(ModelForm):
    class Meta:
        model = Exam
        widgets = {
            'date': forms.DateInput(attrs={'type': "date", 'class': 'form-control'}),
            'starting_time': forms.TimeInput(attrs={'type': "time", 'class': 'form-control'}),
            'ending_time': forms.TimeInput(attrs={'type': "time", 'class': 'form-control'}),
        }
        labels = {
            'starting_time': 'Start Time',
            'ending_time': 'End Time'
        }
        fields = ['date','starting_time','ending_time','proctor_id']

    def __init__(self, *args, **kwargs):
        super(ExamForm2, self).__init__(*args, **kwargs)
        self.fields['proctor_id'].label = "Proctor"


class ExamForm3(ModelForm):
    class Meta:
        model = Exam
        fields = ['semester_id','branch_id','subject_id','is_calc']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        college = College.objects.get(user_id=request.user)
        super(ExamForm3, self).__init__(*args, **kwargs)
        if college.type == 'College':
            self.fields['semester_id'].label = "Semester Name"
            self.fields['branch_id'].label = "Branch Name"
        elif college.type == 'School':
            self.fields['semester_id'].label = "Section"
            self.fields['branch_id'].label = "Class"
        self.fields['semester_id'].empty_label = 'Choose'
        self.fields['branch_id'].empty_label = 'Choose'
        self.fields['subject_id'].label = "Subject Name"
        self.fields['subject_id'].empty_label = 'Choose'
        self.fields['is_calc'].label = "Is Calculator Required!."
        self.fields["is_calc"].choices = [("", "Choose"),] + list(self.fields["is_calc"].choices)[1:]
        self.fields['subject_id'].queryset = Subject.objects.none()
        if 'branch_id' in self.data:
            try:
                branch_id = int(self.data.get('branch_id'))
                self.fields['subject_id'].queryset = Subject.objects.filter(branch_id=branch_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subject_id'] = forms.ModelChoiceField(queryset=Subject.objects.filter(branch_id=self.instance.branch_id))
            self.fields['subject_id'].initial = self.instance.subject_id
            self.fields['subject_id'].label = "Subject Name"
            self.fields['subject_id'].empty_label = 'Choose'


class QuestionForm(ModelForm):
    class Meta:
        model = Questions
        fields = ['exam_id','question_type']

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['exam_id'].label = "Exam Name"
        self.fields['exam_id'].empty_label = 'Choose'
        self.fields['question_type'].label = "Question Type"
        self.fields["question_type"].choices = [("", "Choose"), ] + list(self.fields["question_type"].choices)[1:]


class QuestionManualForm(ModelForm):
    class Meta:
        model = Questions
        widgets = {
            'questions': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 1}),
        }
        exclude = ['exam_id','doc','slug','college_id','branch_id','subject_id','question_type']

    def __init__(self, *args, **kwargs):
        type = kwargs.pop('type')
        super(QuestionManualForm, self).__init__(*args, **kwargs)
        if type == 'MCQ':
            self.fields['option_a'].label = "Option A"
            self.fields['option_a'].required = True
            self.fields['option_b'].label = "Option B"
            self.fields['option_b'].required = True
            self.fields['option_c'].label = "Option C"
            self.fields['option_c'].required = True
            self.fields['option_d'].label = "Option D"
            self.fields['option_d'].required = True
            self.fields['answer'].required = True
        elif type == 'Subjective':
            del self.fields['option_a']
            del self.fields['option_b']
            del self.fields['option_c']
            del self.fields['option_d']
            del self.fields['answer']



class StudentForm(ModelForm):
    class Meta:
        model = Students
        fields = ['branch_id','semester_id']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        college = College.objects.get(user_id=request.user)
        super(StudentForm, self).__init__(*args, **kwargs)
        if college.type == 'College':
            self.fields['semester_id'].label = "Semester Name"
            self.fields['branch_id'].label = "Branch Name"
            self.fields['semester_id'].empty_label = 'Choose'
        elif college.type == 'School':
            del self.fields['semester_id']
            self.fields['branch_id'].label = "Class"
        self.fields['branch_id'].empty_label = 'Choose'


class StudentManualForm(ModelForm):
    class Meta:
        model = Students
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[A-Za-z ]+','title': 'Enter Characters Only '}),
            'student_address':forms.Textarea(attrs={'class':'form-control','rows':5,'cols':1}),
            'country':forms.Select(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'city':forms.Select(attrs={'class':'form-control'}),
        }
        labels = {
            'student_name': 'Student Name',
            'student_phone': 'Student Mobile No',
            'student_email': 'Student Email',
            'student_address': 'Student Address'
        }
        exclude = ['doc','slug','student_password','college_id']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        college = College.objects.get(user_id=request.user)
        super(StudentManualForm, self).__init__(*args, **kwargs)
        if college.type == 'College':
            self.fields['semester_id'].label = "Semester Name"
            self.fields['branch_id'].label = "Branch Name"
            self.fields["section"].choices = [("", "Choose"), ] + list(self.fields["section"].choices)[1:]
        elif college.type == 'School':
            self.fields['semester_id'].label = "Section"
            self.fields['branch_id'].label = "Class"
            del self.fields['section']
        self.fields['semester_id'].empty_label = 'Choose'
        self.fields['branch_id'].empty_label = 'Choose'


class UpdateUser(forms.ModelForm):
    email = forms.EmailField(label="Email")
    class Meta:
        model = User
        fields = ['email',]


class UpdateCollege(forms.ModelForm):
    class Meta:
        model = College
        exclude = ['user_id','doc','slug','type']
        labels = {
            'college_name': 'Name',
            'college_code': 'Code',
            'college_university': 'University',
            'college_address': 'Address',
            'college_contact': 'Contact No.'
        }
