from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile,Relationship
def Register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account Created For {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request,'users/register.html',{'form':form})

@login_required
def UserFriends(request):
    userfriends = Profile.objects.get(user=request.user)
    context = {'userfriends':userfriends}
    return render(request,'users/userfriends.html',context)

def invitations_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)
    results = list(map(lambda x:x.sender,qs))
    is_empty =False
    if len(results)==0:
        is_empty =True
    context = {'qs':results,
                'is_empty':is_empty,
                }

    return render(request,'users/invites.html',context)

def accept_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        print("------------------",pk)
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship,sender=sender,receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('invites')
    

def reject_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship,sender=sender,receiver=receiver)
        rel.delete()
    return redirect('invites')