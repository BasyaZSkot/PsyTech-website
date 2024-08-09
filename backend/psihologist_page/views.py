from django.shortcuts import render, redirect
from .models import Summary, SummaryDescription, FreePlaces, SessionsDate
from .forms import SummaryForm, SummaryDescriptionForm, SubscribesForm
from django.views import generic
from main_page.models import SystemMessages
from django.contrib.auth.models import Group
from chat.models import Chat
from django.contrib.auth.decorators import login_required
import json
from django.contrib.auth.models import User

@login_required(login_url='/accounts/login/')
def choose_work_date(request):
    if request.method == "POST":
        sessions_date = json.loads(request.POST.get("selected_dates"))
        lists = []
        if type(sessions_date) != list:
            for i, l in sessions_date.items():
                _ = i.split("-")
                new_ = []
                for k in _:
                    new_.append(int(k))
                _ = new_
                for q in l:
                    o = q.split(':')
                    newo = []
                    for k in o:
                        newo.append(int(k))
                    o = newo
                    lists.append([_, o])
            FreePlaces.objects.create(user=request.user, free_places=json.dumps(lists))

    return render(request, "choose_work_dates.html")


@login_required(login_url='/accounts/login/')
def choose_sessions_date(request, psih_id):
    user = User.objects.get(id=psih_id)
    free_dates = FreePlaces.objects.get(user=user)
    try:
        sess_dates = SessionsDate.objects.get(user=request.user)
    except:
        pass

    if request.method == "POST":
        try:
            dates = json.loads(request.POST.get("dates"))
        except:
            return redirect(request.path_info)
        lists = []
    
        for i, l in dates.items():
            _ = i.split("-")
            new_ = []
            for k in _:
                new_.append(int(k))
            _ = new_
            for q in l:
                o = q.split(':')
                newo = []
                for k in o:
                    if k:
                        newo.append(int(k))
                o = newo
                lists.append([_, o])
            intersections = []
            a = []
            changes = []
            if sess_dates != None:
                for i in lists:
                    if i not in json.loads(sess_dates.dates):
                        intersections.append(i)
                    else:
                        a.append(i)
            for i in json.loads(sess_dates.dates):
                if i not in a:
                    changes.append(i)
            free_dates_new = json.loads(free_dates.free_places)
            for _ in intersections:
                try:
                    free_dates_new.remove(_)
                except:
                    pass
            free_dates.free_places = json.dumps(free_dates_new)
            free_dates.save()

            try:
                obj = SessionsDate.objects.get(user=request.user)
                obj.dates = json.dumps(lists)
                obj.save()
            except:
                SessionsDate.objects.create(user=request.user, dates=json.dumps(lists))

            for i in changes:
                message = {"new": i}
                SystemMessages.objects.create(sender=request.user, recipient=user, content=f"{message}")
                chat = Chat(chat_name=f"{request.user.username}-{user.username}")
                chat.members.add(request.user)
                chat.members.add(user)
                chat.save()
            for i in intersections:
                if intersections != []: 
                    message = {"change": i}
                else:
                    message = {"delete": i}
                
                SystemMessages.objects.create(sender=request.user, recipient=user, content=json.dumps(message))
        return redirect("home")

    return render(request, "choose_sessions_dates.html", context={
        "free_dates": json.loads(free_dates.free_places),
        "sess_dates": sess_dates.dates
    })


@login_required(login_url='/accounts/login/')
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

            return redirect("add-subscribe")
    else:
        form = SummaryForm()
    
    return render(request, "psihologyst_form.html", context={'form':form})


class SummaryDetailView(generic.DetailView):
    model = Summary
    template_name = "summaries_view.html" 
    context_object_name = "summary"

@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')   
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

@login_required(login_url='/accounts/login/')
def subscribe(request):
    if request.method == "POST":
        form = SubscribesForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            # form.save()
            return redirect("add_payment")
    else:
        form = SubscribesForm()
    
    return render(request, "add_subscribe.html", context={
        "form": form,
        "threshold": 1000
    })
