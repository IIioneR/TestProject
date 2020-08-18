from django.shortcuts import render


def error400(request, exception=None):
    return render(request, 'info/errors/400.html',
                  {'title': '400 (Bad request)'}, status=400)


def error403(request, exception=None):
    return render(request, 'info/errors/400.html',
                  {'title': '403 (HTTP Forbidden)'}, status=400)


def error404(request, exception=None):
    return render(request, 'info/errors/400.html',
                  {'title': '404 (Page not found)'}, status=400)


def error500(request, exception=None):
    return render(request, 'info/errors/400.html',
                  {'title': '500 (Server error)'}, status=400)
