from django import template
from App.models import *

register = template.Library()



@register.filter
def total_marks(exam_id):
    marks = 0
    try:
        question = Questions.objects.filter(exam_id=exam_id, question_type='M')
        for q in question:
            marks += int(q.marks)
    except:
        pass
    return marks

@register.filter
def obtained_marks(student_id,exam_id):
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

@register.filter
def get_college_type(user_id):
    college = College.objects.get(user_id=user_id)
    return college.type