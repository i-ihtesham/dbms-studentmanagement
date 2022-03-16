from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    CreateView, ListView, UpdateView, DeleteView
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from results.models import DeclareResult
from results.forms import DeclareResultForm
from subjects.models import SubjectCombination
from student_classes.models import StudentClass
from students.models import Student
from django.http import HttpResponse, JsonResponse

from django.core import serializers
import json
from django.http import FileResponse
from django.http import HttpResponseRedirect
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from .models import *


def venue_pdf(request):
    buf=io.BytesIO()
    c=canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob=c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)

    # lines = [
    #     "This is line 1",
    #     "This is line 2",
    #     "This is line 3",
    # ]
    
    lines = []
    venues=DeclareResult.objects.all()


    for venue in venues:
        lines.append(str(venue.select_department))
        lines.append(str(venue.select_student))
        lines.append(str(venue.marks))
        # lines.append(str(venue.resource_type))
        # lines.append(str(venue.department_name))
        # lines.append(str(venue.unit_cost))
        lines.append("=========================")
    
    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venue.pdf')


def venue_pdf1(request):
    buf=io.BytesIO()
    c=canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob=c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)

    # lines = [
    #     "This is line 1",
    #     "This is line 2",
    #     "This is line 3",
    # ]
    
    lines = []
    venues=Student.objects.all()


    for venue in venues:
        lines.append(str(venue.student_name))
        lines.append(str(venue.student_usn))
        #lines.append(str(venue.marks))
        # lines.append(str(venue.resource_type))
        # lines.append(str(venue.department_name))
        # lines.append(str(venue.unit_cost))
        lines.append("=========================")
    
    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venue.pdf')
# Create your views here.

def validate_data(request):
    smt = SubjectCombination.objects.all()
    data = {}
    if request.method == "GET":
        rc = request.GET['selectedClass']
        subjects = []
        for s in smt:
            if s.select_department.department_name in rc and s.select_department.semester in rc:
                subjects.append(s.select_subject)
        sir_subjects = serializers.serialize('json', subjects)
        data['subjects'] = sir_subjects
        return JsonResponse(data)
    subjects = None
    data['result'] = 'you made a request with empty data'
    return HttpResponse(json.dumps(data), content_type="application/json")

def declare_result_view(request):
    context = {}
    if request.method == "POST":
        form = request.POST
        data = json.loads(json.dumps(form))
        data.pop('csrfmiddlewaretoken')
        pk = data['select_department']
        clas = StudentClass.objects.get(id=pk)
        pk = data['select_student']
        student = Student.objects.get(id=pk)
        data.pop('select_department')
        data.pop('select_student')
        DeclareResult.objects.create(select_department=clas, select_student=student, marks=data)
    else:
        form = DeclareResultForm()
        context['main_page_title'] = 'Declare Students Result'
        context['panel_name'] = 'Results'
        context['panel_title'] = 'Declare Result'
        context['form'] = form
    return render(request, "results/declareresult_form.html", context)

def setup_update_view(request):
    data = {}
    if request.method == "GET":
        pk_value = int(request.GET['pk_value'])
        result_obj = get_object_or_404(DeclareResult, pk = pk_value)
        dt = result_obj.marks
        data['dt'] = dt
        return HttpResponse(json.dumps(data), content_type="application/json")
    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
def result_update_view(request, pk):
    result = get_object_or_404(DeclareResult, pk=pk)
    form = DeclareResultForm(instance=result)
    context = {}
    context['main_page_title'] = 'Update Students Result'
    context['panel_name'] = 'Results'
    context['panel_title'] = 'Update Result'
    context['form'] = form
    context['pk'] = pk
    if request.method == "POST":
        all_data = request.POST
        data = json.loads(json.dumps(all_data))
        data.pop('csrfmiddlewaretoken')
        pk = data['select_department']
        clas = StudentClass.objects.get(id=pk)
        pk = data['select_student']
        student = Student.objects.get(id=pk)
        data.pop('select_department')
        data.pop('select_student')
        print('Modified Data = ', data)
        result.select_department = clas
        result.select_student = student
        result.marks = data
        result.save()
        print('\nResult updated\n')
        return redirect('results:result_list')
    return render(request, "results/update_form.html", context)

@login_required
def result_delete_view(request, pk):
    obj = get_object_or_404(DeclareResult, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('results:result_list')
    return render(request, "results/result_delete.html", {"object":obj})

class DeclareResultListView(LoginRequiredMixin, ListView):
    model = DeclareResult

    field_list = [
        'Student Name', 'USN', 'Department', 'Reg Date', 'View Result'
    ]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_page_title'] = 'Manage Results'
        context['panel_name']   =   'Results'
        context['panel_title']  =   'View Results Info'
        context['field_list']   =   self.field_list
        return context
    
