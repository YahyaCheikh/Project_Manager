from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.detail import DetailView
from rest_framework import permissions
from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from .serializers import *
from rest_framework import mixins
from rest_framework import generics
from .permissions import IsOwnerOrReadOnly
import datetime
import io
import urllib, base64

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'tasks': reverse('tasks-apis', request=request, format=format)
    })


# ---------------------------------------------------
#                 Task CRUD
# ---------------------------------------------------

class TaskCreate(CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "main/task-create.html"
    success_url = "all-tasks"

    def form_valid(self, form):
        form.instance.created_at = pytz.utc.localize(datetime.datetime.now())
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
class TaskDetail(DetailView):
    model = Task
    context_object_name = "task"
    template_name = 'main/task-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        lables = ["Unused time","Lost in ready to test","Lost in to reveiw","Lost in stop"]
        data = [self.object.unused_time.total_seconds()/60 ,self.object.lost_in_ready_to_test.total_seconds()/60 ,self.object.lost_in_to_reveiw.total_seconds()/60 ,self.object.lost_in_stop.total_seconds()/60 ]
        context["data"], context["labels"]= data,lables
        return context

# ---------------------------------------------------
#                 End Task CRUD
# ---------------------------------------------------


class LandingView(LoginRequiredMixin, ListView):
    template_name = "main/landing_page.html"
    context_object_name = "tasks"

    def get_queryset(self):
        if self.request.user.is_staff :
            queryset = Task.objects.filter(status= "PG")
        else :
            queryset = Task.objects.filter(status= "PG", owner= self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["user"] = self.request.user
        lables = []
        data = []
        if self.request.user.is_staff:
            tasks = Task.objects.filter(status = "DN")
            for task in tasks:
                lables.append(task.title)
                data.append(task.total_time.total_seconds()/60)
        
        context["labels"] = lables
        context["data"] = data
        
        return context



class AllTaskes(LoginRequiredMixin, ListView):
    template_name = "main/all_tasks.html"
    context_object_name = "tasks"
    queryset = Task.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskCompletForm()
        return context
    
    def get_queryset(self):
        if self.request.user.is_staff :
            queryset = Task.objects.all()
        else :
            queryset = Task.objects.filter(owner= self.request.user, status__in =["AS","PG","SP","RV","RG"])
        return queryset


class AllTaskAPI(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def update_task_in_page(request, pk):
    if request.is_ajax() and request.method == 'GET':
        # main logic here setting the value of resp_data
        task_to_update = Task.objects.get(pk = pk)
        print(task_to_update.title)
        print(task_to_update.start_time)
        print("today is %s"%datetime.datetime.now())
        
        task_to_update.update_time_left()
        left_time = task_to_update.time_left 
        resp_data = {
            'html': 'Time left : %s'%left_time,
            'time_left' : "00:20:00"
        }
        return JsonResponse(resp_data, status=200)

def assigne_task(request, pk, user_pk):
    if request.is_ajax() and request.method == 'GET':
        # main logic here setting the value of resp_data
        owner = User.objects.get(pk=user_pk)
        task_to_assign = Task.objects.get(pk = pk)
        task_to_assign.assign_task(owner)
        resp_data = {
            'button': f'<button type="button" class="btn btn-outline-success" data-toggle="modal" data-target="#startModal{pk}">Start</button>',
            'status' : f'<span class="badge badge-outline-secondary">{task_to_assign.get_status_display()}</span>',
            'owner' : f'{task_to_assign.owner}',
        }
        return JsonResponse(resp_data, status=200)

def start_task(request, pk):
    if request.is_ajax() and request.method == 'POST':
        estimated_duration = request.POST.get("estimated_time")
        # main logic here setting the value of resp_data
        task_to_start = Task.objects.get(pk = pk)
        task_to_start.start_task(estimated_duration)
        resp_data = {
            'button': f'<div class="btn btn-outline-danger" onclick="stop_task({pk})">Stop</div>',
            'status' : f'<span class="badge badge-outline-secondary">{task_to_start.get_status_display()}</span>',
            'estimated_durattion' : f'{task_to_start.estimated_durattion}'
        }
        return JsonResponse(resp_data, status=200)

def stop_task(request, pk):
    if request.is_ajax() and request.method == 'GET':
        # main logic here setting the value of resp_data
        task_to_stop = Task.objects.get(pk = pk)
        task_to_stop.stop_task()
        resp_data = {
            'button': f'<button type="button" class="btn btn-outline-info mr-1" onclick="upload_to_test_task({pk})" >Upload totest</button><button class="btn btn-outline-success" onclick="resume_task({pk})">Resume</button>',
            'status' : f'<span class="badge badge-outline-secondary">{task_to_stop.get_status_display()}</span>'
        }
        return JsonResponse(resp_data, status=200)

def upload_to_test_task(request, pk):
    if request.is_ajax() and request.method == 'GET':
        task_to_upload_to_review = Task.objects.get(pk = pk)
        task_to_upload_to_review.mark_as_ready_to_test()
        if request.user.is_staff :
            button = f'<div class="btn btn-outline-success mr-1" onclick="validate_task({pk})">Validate</div><div class="btn btn-outline-warning">To review</div>'
        else:
            button = "Task uploaded to test"
        resp_data = {
            'button': button,
            'status' : f'<span class="badge badge-outline-secondary">{task_to_upload_to_review.get_status_display()}</span>'
        }
        return JsonResponse(resp_data, status=200)

def to_reveiw_task(request, pk):
    if request.is_ajax() and request.method == 'GET':
        # main logic here setting the value of resp_data
        task_to_review = Task.objects.get(pk = pk)
        task_to_review.mark_as_to_reveiw()
        resp_data = {
            'button': '<button type="button" class="btn btn-outline-info mr-1" data-toggle="modal" data-target="#exampleModal">Reupload to test</button>',
            'status' : f'<span class="badge badge-outline-secondary">{task_to_review.get_status_display()}</span>'
        }
        return JsonResponse(resp_data, status=200)

def resume_task(request, pk):
    if request.is_ajax() and request.method == 'GET':
        # main logic here setting the value of resp_data
        task_to_resume = Task.objects.get(pk = pk)
        task_to_resume.resume_task()
        resp_data = {
            'button': f'<div class="btn btn-outline-danger" onclick="stop_task({pk})">Stop</div>',
            'status' : f'<span class="badge badge-outline-secondary">{task_to_resume.get_status_display()}</span>'
        }
        return JsonResponse(resp_data, status=200)

def validate_task(request, pk):
    if request.is_ajax() and request.method == 'GET':
        # main logic here setting the value of resp_data
        task_to_validate = Task.objects.get(pk = pk)
        task_to_validate.mark_as_done()
        resp_data = {
            'button': 'This task is done <a href="#">See detailas</a>',
            'status' : f'{task_to_validate.get_status_display()}'
        }
        return JsonResponse(resp_data, status=200)

def mark_as_to_reveiw_task(request, pk):
    if request.is_ajax() and request.method == 'GET':
        # main logic here setting the value of resp_data
        task_to_mark_as_to_reveiw = Task.objects.get(pk = pk)
        task_to_mark_as_to_reveiw.mark_as_to_reveiw()
        resp_data = {
            'button': '<div class="btn btn-outline-success" onclick="start_reveiw_task({pk})">Start reveiw</div>',
            'status' : f'<span class="badge badge-outline-secondary">{task_to_mark_as_to_reveiw.get_status_display()}</span>'
        }
        return JsonResponse(resp_data, status=200)

def start_reveiw_task(request, pk):
    if request.is_ajax() and request.method == 'GET':
        # main logic here setting the value of resp_data
        task_to_start_eveiw = Task.objects.get(pk = pk)
        task_to_start_eveiw.start_reveiwing()
        resp_data = {
            'button': f'<div class="btn btn-outline-danger" onclick="stop_task({pk})">Stop</div>',
            'status' : f'<span class="badge badge-outline-secondary">{task_to_start_eveiw.get_status_display()}</span>'
        }
        return JsonResponse(resp_data, status=200)

def start_test_task(request, pk):
    if request.is_ajax() and request.method == 'GET':
        # main logic here setting the value of resp_data
        task_to_start_test = Task.objects.get(pk = pk)
        task_to_start_test.start_testing()
        resp_data = {
            'button': f'<div class="btn btn-outline-success mr-1" onclick="validate_task({pk})">Validate</div><div class="btn btn-outline-warning" onclick="mark_to_reveiw_task({pk})">To review</div>',
            'status' : f'<span class="badge badge-outline-secondary">{task_to_start_test.get_status_display()}</span>'
        }
        return JsonResponse(resp_data, status=200)



#test view
def get_name_from_form(request):
    if request.method == "POST":
        form = TaskCompletForm(request.POST)
        if form.is_valid():
            return HttpResponse("good")
        
    else :
        form = TaskCompletForm()
        return render(request, 'main/form_assign.html', {'form': form})


#------------------------------------------------------------------------------#
#                                                                              #
#-----------------------------CRUD ENTREPRISE----------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class EntrepriseModelCreate(generics.CreateAPIView):
    model = EntrepriseModel
    form_class = EntrepriseModelForm
    template_name = "main/entreprise-create.html"
    success_url = "all-tasks"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)



#------------------------------------------------------------------------------#
#                                                                              #
#--------------------------------Dashboards------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class EntreprenerDashboard(TemplateView):
    template_name  = 'dashboards/enreprener_dashboard.html'

    def get_context_data(self, **kwargs) :
        return super().get_context_data(**kwargs)



class EntreprenerDashboard(TemplateView):
    template_name  = 'dashboards/project_owner_dashboard.html'

    def get_context_data(self, **kwargs) :
        return super().get_context_data(**kwargs)



class EntreprenerDashboard(TemplateView):
    template_name  = 'dashboards/task_developer_dashboard.html'

    def get_context_data(self, **kwargs) :
        return super().get_context_data(**kwargs)


class EntreprenerDashboard(TemplateView):
    template_name  = 'dashboards/task_validator_dashboard.html'

    def get_context_data(self, **kwargs) :
        return super().get_context_data(**kwargs)











































#-----------------------------------matplotlib---------------------------------
# import matplotlib.pyplot as plt                                             |                             |
# plt.plot(list_of_times)                                                     |
#         fig = plt.gcf()                                                     |
#         buf = io.BytesIO()                                                  |
#         fig.savefig(buf, format='png')                                      |
#         buf.seek(0)                                                         |
#         string = base64.b64encode(buf.read())                               |
#         uri = urllib.parse.quote(string)                                    |
#         context["chart"] = uri                                              |
#-----------------------------------matplotlib---------------------------------