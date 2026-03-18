from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Member
# from django.db.models import Q
# def member_list(request):
#     # return HttpResponse("Helloooo Rinku")
#     template = loader.get_template('myfirst.html')
#     return HttpResponse(template.render())

# Create your views here.
def member_list(request):
    mymembers= Member.objects.all().values()
    # return HttpResponse("Helloooo Rinku")
    template = loader.get_template('all_members.html')
    context={
       'mymembers':mymembers,
    }
    return HttpResponse(template.render(context,request))

def details(request, id):
  mymember = Member.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'mymember': mymember,
  }
  return HttpResponse(template.render(context, request))

def main(request):
  # template = loader.get_template('Main.html')
  return render(request, "Main.html")

def testing(request):
  # mymembers= Member.objects.values_list('fname', flat=True)
  # mymembers= Member.objects.all()
  # mymembers= Member.objects.filter(lname='Jambukiya',id=2).values() #AND condition
  # mymembers = Member.objects.filter(Q(fname='Rinku') | Q(fname='Bhakti')).values()  #OR condition using Q objects
  # mymembers = Member.objects.filter(fname='Vidhya').values() | Member.objects.filter(fname='Mital').values()  #OR condition using bitwise operator
  # mymembers= Member.objects.filter(fname__startswith='A').values()  #field_lookups
  mymembers= Member.objects.all().order_by('lname').values()
  template= loader.get_template('template.html')
  context = {
    'greeting':1,
    'mymembers':mymembers,
    # 'fname': ['Rinku'],
    'fruits': ['Apple', 'Banana', 'Cherry','Mango','Potato','Chilly','Tomato','Brinjal'],
  }
  return HttpResponse(template.render(context, request))
  
# def test(request):
#   template = loader.get_template('childtemplate.html')
#   return HttpResponse(template.render())