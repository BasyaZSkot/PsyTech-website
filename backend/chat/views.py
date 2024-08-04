from django.shortcuts import render, redirect
from .models import Message, Chat
from psihologist_page.models import Summary
from django.contrib.auth.decorators import login_required

# Create your views here.
def mark_as_read(request, pk):
    message = Message.objects.get(id=pk)
    message.read_status = True
    message.save()
    
# def chat(request, pk):
#     summary = Summary.objects.get(id=pk)
#     if request.user == summary.user:
#         recipient = SystemMessages.objects.get(content="summary confirmation", recipient=request.user).sender
#     else:
#         recipient = summary.user

#     if request.method == 'POST':
#         if request.POST.get('message') != "":
#             message = Message(content=request.POST.get('message'), sender=request.user, recipient=recipient, read_status=False)
#             message.save()
#             return HttpResponseRedirect(request.path_info)
    
#     messages = Message.objects.filter(
#                 Q(sender=request.user, recipient=recipient,) | 
#                 Q(sender=recipient, recipient=request.user,)).order_by('timestamp')
    
#     return render(request, 'chat.html', {"messages" : messages,
#                                          "user": request.user,
#                                          "id": pk,
#                                          "recipient": recipient,
#                                          })


def save(request):
    if request.method == 'POST':
        message_id = request.POST.get('model_id')
        chat = request.POST.get('chat')
        message = Message.objects.get(id=message_id)
        message.read_status = True
        message.save()

        if request.user.is_superuser:
            summary = Summary.objects.get(user=message.sender)
        
        return redirect('chat', chat.chat_name)
    else:
        return redirect("home")

@login_required(login_url='/accounts/login/')
def MessageView(request, chat_name):
    chat = Chat.objects.get(chat_name=chat_name)
    if request.user in chat.members.all():
        messages = Message.objects.filter(chat=chat)
        return render(request, 'chat.html', context={
            "messages": messages,
            "user": request.user,
            "chat": chat
        })
    else:
        return redirect("404")   