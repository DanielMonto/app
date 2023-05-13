from django.shortcuts import render,redirect,get_object_or_404
import datetime
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from . import forms,models
from django.contrib.auth.decorators import login_required

#tareas
@login_required
def tasks(request):
    return render(request,'tasks.html',{
        'tasks':models.Task.objects.filter(user=request.user, date_completed__isnull=True)
    })
@login_required
def tasks_completed(request):
    return render(request,'tasks_completed.html',{
        'tasks':models.Task.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    })
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request,'create_task.html',{
            'form':forms.NewTask
        })
    elif request.method=='POST':
        try:
            n_form=forms.NewTask(request.POST)
            new_task=n_form.save(commit=False)
            new_task.user=request.user
            new_task.save()
            return redirect('tasks')
        except:
            return render(request,'create_task.html',{
            'form':forms.NewTask,
            'error':'no esta usando datos validos'
        })
@login_required
def task_detail(request,task_name,task_id):
    task=get_object_or_404(models.Task,pk=task_id,name=task_name)
    sub_tasks = models.SubTask.objects.filter(task=task)
    if request.method=='GET':
        task=get_object_or_404(models.Task,pk=task_id,name=task_name)
        return render(request,'task_detail.html',{
        'task':task,
        'sub_tasks':sub_tasks
    })
    elif request.method=='POST':
        try:
            task=get_object_or_404(models.Task,pk=task_id,name=task_name,user=request.user)
            Ntask=forms.NewTask(request.POST,instance=task)
            Ntask.save()
            return redirect('tasks')
        except:
            return render(request,'task_detail.html',{
        'task':task,
        'sub_tasks':sub_tasks,
        'error':'error: datos incorrectos'
    })
@login_required
def completeTask(request,task_name,task_id):
    task=get_object_or_404(models.Task,pk=task_id,name=task_name,user=request.user)
    if request.method=='POST':
        task.date_completed=datetime.datetime.now()
        task.save()
        return redirect('tasks')
    elif request.method=='GET':
        return redirect('tasks')
@login_required
def deleteTask(request,task_name,task_id):
    task=get_object_or_404(models.Task,pk=task_id,name=task_name,user=request.user)
    if request.method=='POST':
        task.delete()
        return redirect('tasks')
#subtareas
@login_required
def create_subtask(request, task_name, task_id):
    task = get_object_or_404(models.Task, pk=task_id, name=task_name)
    sub_tasks=models.SubTask.objects.filter(task=task)
    if request.method == 'GET':
        return render(request, 'create_subtask.html', {'sub_tasks':sub_tasks,'task':task})
    elif request.method == 'POST':
        try:
            n_form = forms.NewSubTask(request.POST)
            new_task = n_form.save(commit=False)
            new_task.user = request.user
            new_task.task = task
            new_task.created_at=datetime.datetime.now()
            name_task=new_task.task.name
            id_task=new_task.task.id
            new_task.save()
            return redirect('tasks')
        except:
            return render(request, 'create_subtask.html', {
                'error': 'no esta usando datos validos',
                'sub_tasks':sub_tasks,
                'task':task
            })
@login_required
def subtask_detail(request,subtask_name,subtask_id):
    form=forms.NewSubTask
    subtask=get_object_or_404(models.SubTask,pk=subtask_id,name=subtask_name)
    if request.method=='GET':
        return render(request,'sub_task_detail.html',{'subtask':subtask,'form':form})
    elif request.method=='POST':
        try:
            n_subtask=forms.NewSubTask(request.POST,instance=subtask)
            n_subtask.save()
            return redirect('tasks')
        except:
            error='Error compruebe que los datos sean validos'
            return render(request,'sub_task_detail.html',{'subtask':subtask,'form':form,'error':error})

@login_required
def delete_subtask(request,subtask_name,subtask_id):
    subtask=get_object_or_404(models.SubTask,pk=subtask_id,name=subtask_name,)
    name_task=subtask.task.name
    id_task=subtask.task.id
    if request.method=='POST':
        subtask.delete()
        return redirect('tasks')
#principal   
def principal(request):
    user=request.user
    return render(request,'Home.html',{'user':user})
#reguistro
def reguistro(request):
    context={'form':UserCreationForm}
    if request.method=='GET':
        return render(request,'sign_in.html',context)
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(username=request.POST['username'],password=request.POST['password2'])
                user.save()
                login(request,user)
                return redirect('tasks')
            except IntegrityError:
                return render(request,'sign_in.html',{
                    'form':UserCreationForm,
                    'error':'el usuario ya existe intente con otros datos'
                })
        elif request.POST['password1']!=request.POST['password2']:
            return render(request,'sign_in.html',{
                    'form':UserCreationForm,
                    'error':'¡las contraseñas no son iguales, compruebelas!'
                })
#cerrar secion
@login_required
def signout(request):
    logout(request)
    return redirect('init')

#continuar secion cerrada
def confirm_user(request):
    if request.method=='GET':
        return render(request,'confirm_user.html',{
        'form':AuthenticationForm
        })
    elif request.method=='POST':
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            error='¡No se encontro un usuario con los datos dados! '
            return render(request,'confirm_user.html',{
            'form':AuthenticationForm,
            'error':error
            })
        else:
            login(request,user)
            return redirect('tasks')

#blog simple
@login_required
def menajes_blog(request):
    mensajes=models.Mensaje.objects.all()
    if request.method=='GET':
        return render(request,'blog.html',{'form':forms.NewMensaje,'mensajes':mensajes,'user':request.user})
    elif request.method=='POST':
        try:
            http='http'
            com='.com'
            if (http in request.POST['Mensaje']) or (com in request.POST['Mensaje']):
                error_de_name='No se admiten links de nombre'
                return render(request,'blog.html',{'error':error_de_name,'form':forms.NewMensaje,'mensajes':mensajes,'user':request.user})
            else: 
                N_form=forms.NewMensaje(request.POST)
                new_mensaje=N_form.save(commit=False) 
                new_mensaje.user=request.user
                new_mensaje.fecha=datetime.datetime.now()
                new_mensaje.save()
                return redirect('blog')
        except:
            error='Datos no validos'
            return render(request,'blog.html',{'error':error,'form':forms.NewMensaje,'mensajes':mensajes,'user':request.user})
#borrar mensaje del blog
@login_required
def deleteMensaje(request,M_id,M_Mensaje):
    try:
        mensajes=models.Mensaje.objects.all()
        mensaje=get_object_or_404(models.Mensaje,pk=M_id,Mensaje=M_Mensaje,user=request.user)
    except:
        error='¡no puedes borrar este mensaje porque no lo creaste!!'
        return render(request,'blog.html',{'error_user':error,'mensajes':mensajes,'user':request.user})
    if request.method=='POST':
            mensaje.delete()
            return redirect('blog')

@login_required
def chat_privado(request,name_receptor,name_talker):
    receptor=get_object_or_404(User,username=name_receptor)
    talker=get_object_or_404(User,username=name_talker)
    mensajes=models.MensajePrivado.objects.filter(sender=talker.id,receptor=receptor.id)
    mensajes_2=models.MensajePrivado.objects.filter(sender=receptor.id,receptor=talker.id)
    if request.method=='GET':
        return render(request,'chat_privado.html',{'user':receptor,'mensajes_2':mensajes_2,'talker':name_talker,'mensajes':mensajes})  
    elif request.method=='POST':
        try:
            http='http'
            com='.com'
            if (http in request.POST['mensaje']) or (com in request.POST['mensaje']):
                error_de_name='No se admiten links de nombre'
                mensajes=models.MensajePrivado.objects.filter(sender=talker.id,receptor=receptor.id)
                return render(request,'chat_privado.html',{'error':error_de_name,'mensajes_2':mensajes_2,'talker':talker,'mensajes':mensajes,'user':receptor})
            else:
                n_form=forms.NewPrivateMensaje(request.POST)
                mensaje_privado=n_form.save(commit=False)
                mensaje_privado.receptor=receptor
                mensaje_privado.sender=talker
                mensaje_privado.fecha=datetime.datetime.now()
                mensaje_privado.mensaje=request.POST['mensaje']
                mensaje_privado.save()
                mensajes=models.MensajePrivado.objects.filter(sender=talker.id,receptor=receptor.id)
                return render(request,'chat_privado.html',{'user':receptor,'mensajes_2':mensajes_2,'talker':name_talker,'mensajes':mensajes})
        except:
            mensajes=models.MensajePrivado.objects.filter(sender=talker.id,receptor=receptor.id)
            error='¡Hubo un error vuelve a intentarlo!!'
            return render(request,'chat_privado.html',{'error':error,'mensajes_2':mensajes_2,'user':receptor,'talker':name_talker,'mensajes':mensajes})

@login_required
def mostrarUsuarios(request):
    users=User.objects.all()
    return render(request,'usuarios.html',{'users':users,'user':request.user})
@login_required
def deletePrivateMensaje(request,pm_id,pm_mensaje,name_receptor):
    talker=request.user
    receptor=get_object_or_404(User,username=name_receptor)
    mensajes=models.MensajePrivado.objects.filter(sender=request.user.id,receptor=receptor.id)
    mensaje=get_object_or_404(models.MensajePrivado,pk=pm_id,mensaje=pm_mensaje,sender=request.user.id)
    if request.method=='POST':
            mensaje.delete()
            mensajes_2=models.MensajePrivado.objects.filter(sender=receptor.id,receptor=talker.id)
            return render(request,'chat_privado.html',{'user':receptor,'mensajes_2':mensajes_2,'talker':talker,'mensajes':mensajes,'receptor':receptor})