from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .form import PollForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import datetime

from .models import Poll

@login_required
def index(request):

    search = request.GET.get('search')
    filter = request.GET.get('filter')
    tasksDoneRecently = Poll.objects.filter(done='done', updated_at__gt=datetime.datetime.now()-datetime.timedelta(days=30), user=request.user).count()
    tasksDone = Poll.objects.filter(done = 'done', user=request.user).count()
    tasksDoing = Poll.objects.filter(done = 'doing', user=request.user).count()

    if search:
        tasks = Poll.objects.filter(title__icontains=search, user=request.user)

    elif filter:
        tasks = Poll.objects.filter(done=filter, user=request.user)

    else:

        tasks_list = Poll.objects.all().order_by('-created_at').filter(user=request.user)
        
        paginator = Paginator(tasks_list, 3 )
        
        page = request.GET.get("page")

        tasks = paginator.get_page(page)

    return render(request, 'polls/index.html', 
        {'tasks': tasks, 'tasksrecently': tasksDoneRecently, 'tasksdone': tasksDone, 'tasksdoing': tasksDoing})

@login_required
def taskView(request, id):
    task = get_object_or_404(Poll, pk=id)
    return render(request, 'polls/task.html', {'task': task})

@login_required
def newTask(request):
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.done = 'doing'
            task.user =request.user
            task.save()
            return redirect('/')
    else:
        form = PollForm()
        return render(request, 'polls/addtask.html', {'form': form})

@login_required
def editTask(request, id):
    task = get_object_or_404(Poll, pk=id)
    form = PollForm(instance=task)

    if(request.method == 'POST'):
        form = PollForm(request.POST, instance=task)
        if(form.is_valid()):
            task.save()
            return redirect('/')
        else:
            return render(request, 'polls/edittask.html', {'form': form, 'task': task})
    else:
        return render(request, 'polls/edittask.html', {'form': form, 'task': task})

@login_required
def changeStatus(request, id):
    task = get_object_or_404(Poll, pk=id)

    if (task.done == 'doing'):
        task.done = 'done'
    else:
        task.done = 'doing'

    task.save()

    return redirect('/')

@login_required
def deleteTask(request, id):
    task = get_object_or_404(Poll, pk=id)
    task.delete()

    messages.info(request, "Tarefa deletada com sucesso")

    return redirect('/')

@login_required
def helloWorld(request):
    return HttpResponse('Helo World!')
