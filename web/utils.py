# -*- coding: utf-8 -*-


def handle_error_message(request):
    if "error" in request.session:
        context = {'error': request.session['error']}
        del request.session['error']
        return context
    return
