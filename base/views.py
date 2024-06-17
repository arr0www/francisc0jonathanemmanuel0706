from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, User, Reservation,Message, Reservation2, Reservation3, Reservation4
from .forms import RoomForm, UserForm, MyUserCreationForm, ReservationForm


# Create your views here.

#rooms =[
   # {'id':1, 'name': 'Lets learn python!'},
  #  {'id':2, 'name': 'design with me'},
 #   {'id':3, 'name': 'frontend'},
#]


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('home')

    if request.method=="POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('index')

def registerPage(request):  
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect ('home')
        else:
            messages.error(request, 'An error has occured')

    return render(request, 'base/login_register.html',{'form':form})


def indexcard(request):

    print('Redirecting...')


    return render (request, 'base/index.html')



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    binfo=Reservation.objects.all()
    binfo2=Reservation2.objects.all()
    binfo3=Reservation3.objects.all()
    binfo4=Reservation4.objects.all()
    


    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(author__icontains=q) |
        Q(status__icontains=q) |
        Q(serialnumber__icontains=q) |
        Q(description__icontains=q)
        )

    topics = Topic.objects.all()
    
    room_count = Room.objects.filter(status=0).count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))


    context = {'rooms':rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages, 'binfo':binfo, 'binfo2':binfo2,'binfo3':binfo3,'binfo4':binfo4 }
    return render(request,'base/home.html',context)


def room(request, pk):
    binfo=Reservation.objects.all()
    binfo2=Reservation2.objects.all()
    binfo3=Reservation3.objects.all()
    binfo4=Reservation4.objects.all()
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    # if request.method == 'POST':
    #     binfo = Reservation.objects.get(
    #         room=room,
    #         user=request.user,
    #         requestdate=request.POST.get('requestdate'),
    #         returndate=request.POST.get('returndate'),
    #     )


    context = {'room' : room, 'room_messages' : room_messages, 'participants' : participants,'binfo':binfo, 'binfo2':binfo2,'binfo3':binfo3,'binfo4':binfo4 }
    return render(request, 'base/room.html',context)



def BorrowRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = ReservationForm()

    if request.method == 'POST':
        binfo = Reservation.objects.create(
            id = None,
            pk = None,
            room = room.name,
            user = request.user.name,
            requestdate = request.POST.get('requestdate'),
            returndate = request.POST.get('returndate')
        )
        
        Room.objects.filter(id=pk).update(status = 1)
        
        
        return redirect ('home')   

    context = {'room' : room, 'form':form}
    return render(request, 'base/borrow.html',context)

@login_required(login_url='login')
def confirmresbtn(request, pk):
    room = Room.objects.get(id=pk)


    if request.method == 'POST':
            binfo = Reservation.objects.last()
            binfo2 = Reservation2.objects.create(
            
            id = None,
            pk = None,
            room = room.name,
            user = binfo.user,
            requestdate = binfo.requestdate,
            returndate = binfo.returndate
            )
            Room.objects.filter(id=pk).update(status = 2)
            binfo = Reservation.objects.last().delete()


            return redirect('home')
    
    return render(request, 'base/confirmres.html', {'obj':room})


@login_required(login_url='login')
def returnBook(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
            binfo2 = Reservation2.objects.last()
            binfo3 = Reservation3.objects.create(
            id = None,
            pk = None,
            room=room.name,
            user=binfo2.user,
            requestdate=binfo2.requestdate,
            returndate=binfo2.returndate,
            )
            
            Room.objects.filter(id=pk).update(status = 0)
            binfo2 = Reservation2.objects.last().delete()
            

            return redirect('home')

    return render(request, 'base/returned.html', {'obj':room})

@login_required(login_url='login')
def denyBook(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':

            binfo = Reservation.objects.last()
            binfo4 = Reservation4.objects.create(      
            id = None,
            pk = None,    
            room=room.name,
            user=binfo.user,
            requestdate = binfo.requestdate,
            returndate= binfo.returndate,
        )
            
            Room.objects.filter(id=pk).update(status = 0)
            binfo = Reservation.objects.last().delete()
            

            
            return redirect('home')

    return render(request, 'base/denied.html', {'obj':room})



def userProfile(request, pk):
    user = User.objects.get(id=pk)
    room_messages = user.message_set.all()
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms' : rooms, 'room_messages' : room_messages,'topics' : topics}
    return render(request, 'base/profile.html', context)






@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.author = request.POST.get('author')
        room.serialnumber = request.POST.get('serialnumber')
        room.date_published = request.POST.get('date_published')
        room.publisher = request.POST.get('publisher')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')


    context = {'form':form , 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    
    room = Room.objects.get(id=pk)
    

    if request.method == 'POST':
        
        Room.objects.filter(id=pk).update(status = 4)
        
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})


def viewArchive(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(author__icontains=q) |
        Q(serialnumber__icontains=q) |
        Q(description__icontains=q)
        )

    context = {'rooms':rooms}
    return render(request,'base/archive.html',context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name )


        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            author=request.POST.get('author'),
            serialnumber=request.POST.get('serialnumber'),
            date_published=request.POST.get('date_published'),
            publisher=request.POST.get('publisher'),
            description=request.POST.get('description'),
        )

        return redirect('home')

    context = {'form':form , 'topics':topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)


    return render (request, 'base/update-user.html', {'form':form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics':topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render (request, 'base/activity.html', {'room_messages':room_messages})