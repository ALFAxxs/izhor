from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return render(request, 'auth/login.html')


@login_required(login_url='/auth/login/')
def dashboard_home(request):
    return render(request, 'dashboard/home.html')


@login_required(login_url='/auth/login/')
def templates_list(request):
    return render(request, 'dashboard/templates_list.html')


@login_required(login_url='/auth/login/')
def template_new(request):
    return render(request, 'dashboard/template_new.html')


@login_required(login_url='/auth/login/')
def template_builder(request, pk):
    from apps.templates_app.models import IzhorTemplate
    try:
        tmpl = IzhorTemplate.objects.get(pk=pk, merchant__user=request.user)
        qr_slug = tmpl.qr_code.slug if hasattr(tmpl, 'qr_code') else ''
    except IzhorTemplate.DoesNotExist:
        from django.http import Http404
        raise Http404
    return render(request, 'dashboard/builder.html', {
        'template_id': pk,
        'qr_slug':     qr_slug,
    })


@login_required(login_url='/auth/login/')
def qrcodes_page(request, pk=None):
    return render(request, 'dashboard/qrcodes.html', {'template_id': pk or ''})


@login_required(login_url='/auth/login/')
def analytics_page(request):
    return render(request, 'dashboard/analytics.html')


def logout_page(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('/auth/login/')
