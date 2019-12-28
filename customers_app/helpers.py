def is_passwords_match(form):
    cleaned_data = form.cleaned_data
    if cleaned_data['password'] != cleaned_data['confirm_password']:
        msg = 'Passwords doen\'t match'
        form.errors['password'] = form.error_class([msg])

        del cleaned_data['password']
        del cleaned_data['confirm_password']
        return False

    return True
