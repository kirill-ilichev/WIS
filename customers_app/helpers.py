from django.contrib.auth.models import User

from customers_app.models import Customer, Photo


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


def sort_customers(sort_name, sort_direction, customers):

    if sort_direction not in ['asc', 'desc']:
        return None

    if sort_name in get_model_fields_list(Customer):

        if sort_direction == 'asc':
            order_by = '{}'.format(sort_name)
        elif sort_direction == 'desc':
            order_by = '-{}'.format(sort_name)

    elif sort_name in get_model_fields_list(User):

        if sort_direction == 'asc':
            order_by = 'user__{}'.format(sort_name)
        elif sort_direction == 'desc':
            order_by = '-user__{}'.format(sort_name)
    else:
        return None

    return customers.order_by(order_by)


def filter_and_sort_customers_by_query_params(query_params, customers):

    if query_params.get('first-name', None):
        customers = customers.filter(user__first_name=query_params.get('first-name'))
    if query_params.get('last-name', None):
        customers = customers.filter(user__last_name=query_params.get('last-name'))

    sort_name = query_params.get('sort-name', None)
    if sort_name:
        sorted_customers = sort_customers(sort_name, query_params.get('sort-direction'), customers)

        if sorted_customers:
            return sorted_customers

    return customers
