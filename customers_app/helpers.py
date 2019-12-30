from django.contrib.auth.models import User

from customers_app.models import Customer


def is_passwords_match(form):
    cleaned_data = form.cleaned_data
    if cleaned_data['password'] != cleaned_data['confirm_password']:
        msg = 'Passwords doen\'t match'
        form.errors['password'] = form.error_class([msg])

        del cleaned_data['password']
        del cleaned_data['confirm_password']
        return False

    return True


def get_model_fields_list(model):
    return [field.name for field in model._meta.get_fields()]


def sort_customers(field, customers):

    if field in get_model_fields_list(Customer):
        order_by = '{}'.format(field)
    elif field in get_model_fields_list(User):
        order_by = 'user__{}'.format(field)
    else:
        return None

    return customers.order_by(order_by)
