from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from users.models import Profile,Relationship
from django.views.generic import ListView
from django.db.models import Q

def invite_profiles_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)
    context = {'qs':qs}

    return render(request,'users/send_invites.html',context)

def home(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)
    context = {'qs':qs}

    return render(request,'friends/home.html',context)
class Home(ListView):
    model = Profile
    template_name = 'friends/home.html'
    context_object_name = 'qs'
    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)

        for item in rel_s:
            rel_sender.append(item.sender.user)

        context['rel_receiver']= rel_receiver
        context['rel_sender']=rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) ==0:
            context['is_empty'] = True
        return context

def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender,receiver=receiver,status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('users:')

def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        
        rel =Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
            )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('users:')