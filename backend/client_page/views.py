from django.shortcuts import render, redirect
from .forms import UserPsihHelpInfoForm

# Create your views here.
def additionaly_regular_user(request):
    if request.method == "POST":
        form = UserPsihHelpInfoForm(request.POST)
        if form.is_valid:
            form = form.save()
            form.user = request.user
            form.save()
            return redirect("home")
    else:
        form = UserPsihHelpInfoForm
    return render(request, "additionaly_regular_user.html", context={
        "form": form
    })