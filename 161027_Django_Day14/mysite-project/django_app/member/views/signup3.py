from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.conf import settings
from member.forms import SignupModelForm


def signup3(request):
    context = {}
    if request.method == 'POST':
        form = SignupModelForm(request.POST)
        if form.is_valid():
            user = form.save()
            # user = authenticate(
            #     email=form.cleaned_data['email'],
            #     password=form.cleaned_data['password1']
            # )
            login(
                request,
                user,
                settings.AUTH_BACKEND_DEFAULT
            )
            return redirect('blog:post_list')
        context['form'] = form
    else:
        form = SignupModelForm()
        context['form'] = form
    return render(request, 'member/signup2.html', context)
