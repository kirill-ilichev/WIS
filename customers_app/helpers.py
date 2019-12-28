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


def get_model_fields(model):
    return [field.name for field in model._meta.get_fields()]


def sort_customers(field, customers):
    customer_fields = get_model_fields(Customer)
    user_fields = get_model_fields(User)

    if field in customer_fields:
        order_by = '{}'.format(field)
    elif field in user_fields:
        order_by = 'user__{}'.format(field)
    else:
        return None

    return customers.order_by(order_by)
