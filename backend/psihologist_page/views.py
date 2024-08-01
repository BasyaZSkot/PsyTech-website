from django.shortcuts import render, redirect
from .models import Summary, SummaryDescription
from .forms import SummaryForm, SummaryDescriptionForm
from django.views import generic
from main_page.models import SystemMessages
from django.contrib.auth.models import Group
from chat.models import Chat

# Create your views here.

def getting_summary(request):
    if request.POST:
        form = SummaryForm(request.POST, request.FILES)
        if form.is_valid():
            form.clean()

            model = Summary(user=request.user,
                            degree=form.cleaned_data["degree"],
                            universyty=form.cleaned_data["universyty"],
                            diploma=form.cleaned_data["diploma"],
                            training=form.cleaned_data["training"], 
                            advanced_curses=form.cleaned_data["advanced_curses"], 
                            description=form.cleaned_data["description"], 
                            science_interestings=form.cleaned_data["science_interestings"], 
                            achievements=form.cleaned_data["achievements"], 
                            work_area=form.cleaned_data["work_area"], 
                            often_questions=form.cleaned_data["often_questions"], 
                            experience=form.cleaned_data["experience"], 
                            something_to_add=form.cleaned_data["something_to_add"])
            model.save()

            return redirect("home")
    else:
        form = SummaryForm()
    
    return render(request, "psihologyst_form.html", context={'form':form})

class SummaryDetailView(generic.DetailView):
    model = Summary
    template_name = "summaries_view.html" 
    context_object_name = "summary"

def summary_mistakes(request, pk):
    summary = Summary.objects.get(id=pk)
    
    if request.method == "POST":
        form = SummaryDescriptionForm(request.POST)
        if form.is_valid():
            form.clean()
            description = form.cleaned_data["description"]
            model = SummaryDescription(summary=summary, inspector=request.user, description=description)
            model.save()
            return redirect("reject_summary", pk)
    else:
        form = SummaryDescriptionForm

    return render(request, 'summary_description.html', context={'form': form})


def reject_summary(request, pk):
    if request.user.is_superuser:
        summary_sender = Summary.objects.get(id=pk).user

        rejection = SystemMessages(sender=request.user, recipient=summary_sender, content="summary rejection")
        rejection.save()

        group = Group.objects.get(name="reject psihologyst")
        previous_group = Group.objects.get(name="psihologyst")
        group.user_set.add(summary_sender)
        previous_group.user_set.remove(summary_sender)

        return redirect("home")
    else:
        return redirect("404")
    
def confirm_summary(request, pk):
    if request.user.is_superuser:
        summary_sender = Summary.objects.get(id=pk).user
        
        confirmation = SystemMessages(sender=request.user,
                               recipient=summary_sender, 
                               content="summary confirmation", 
                               )
        confirmation.save()
        new_chat = Chat(chat_name=f'{request.user}-{summary_sender}')
        new_chat.save()

        return redirect("chat", new_chat.chat_name)
    else:
        return redirect("404")
    
def summary_description_detail_view(request, pk):
    rejection_message = SystemMessages.objects.get(id=pk)

    summary = Summary.objects.get(user=rejection_message.recipient)

    return render(request, "summary_mistakes_detail_view.html", context={"summary_description": SummaryDescription.objects.get(summary=summary)})
