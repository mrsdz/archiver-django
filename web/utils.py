# -*- coding: utf-8 -*-


def handle_message(request):
    if "error" in request.session:
        context = {'error': request.session['error']}
        del request.session['error']
        return context
    elif "done" in request.session:
        context = {'done': request.session['done']}
        del request.session['done']
        return context
    return
