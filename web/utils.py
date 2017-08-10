# -*- coding: utf-8 -*-


def handle_error_message(request):
    if "error" in request.session:
        del request.session['error']
        return {'error': 'نام کاربری یا رمز عبور اشتباه است'}
    return
