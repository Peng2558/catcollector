from django.shortcuts import render,redirect
from .models import Cat
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import FeedingForm

# Create your views here.

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def cats_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html',{
     'cats': cats

})

def cats_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    # instantiate FeedingForm to be rendered in the template
    feeding_form = FeedingForm()
    return render(request,'cats/detail.html',{
     'cat':cat ,
     'feeding_form': feeding_form
    })

class CatCreate(CreateView):
  model = Cat
  fields = '__all__'
#   success_url = '/cats' in it's here will be override the detail page

class CatUpdate(UpdateView):
  model = Cat
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['bread', 'description', 'age']

class CatDelete(DeleteView):
  model = Cat
  success_url = '/cats'


def add_feeding(request, cat_id):
    # create a ModelForm instance using the data in request.POST
    form = FeedingForm(request.POST)
  # validate the form
    if form.is_valid():
    # don't save the form to the db until it
    # has the cat_id assigned
     new_feeding = form.save(commit=False)
     new_feeding.cat_id = cat_id
     new_feeding.save()
    return redirect('detail', cat_id=cat_id)
