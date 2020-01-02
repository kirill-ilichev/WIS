from django.contrib.auth.models import User

from customers_app.models import Customer


def are_passwords_match(form):
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


def sort_customers(filter_query, customers):

    try:
        field = filter_query[:filter_query.rindex('_')]
    except ValueError:
        return None

    sort_direction = filter_query[filter_query.rindex('_')+1:]

    if sort_direction not in ['up', 'down']:
        return None

    if field in get_model_fields_list(Customer):

        if sort_direction == 'up':
            order_by = '{}'.format(field)
        elif sort_direction == 'down':
            order_by = '-{}'.format(field)
    elif field in get_model_fields_list(User):

        if sort_direction == 'up':
            order_by = 'user__{}'.format(field)
        elif sort_direction == 'down':
            order_by = '-user__{}'.format(field)
    else:
        return None

    return customers.order_by(order_by)
