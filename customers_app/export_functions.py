from io import BytesIO
from xlwt import Workbook

from django.contrib.auth.models import User
from django.http import HttpResponse

from customers_app.helpers import get_model_fields_list
from customers_app.models import Customer


def export_customers_details_in_xlsx(request):
    """
    Collects information about customers and export it in xlsx file.
    Then allows customer to chose where to save export file
    """
    excelfile = BytesIO()

    wb = Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sheetname')

    fields_for_writing = ['username', 'email', 'first_name', 'last_name', 'age', 'date_of_birth']
    for col, field in enumerate(fields_for_writing):
        ws.write(0, col, field)

    customers = Customer.objects.all()
    for row, customer in enumerate(customers, 1):
        for col, field in enumerate(fields_for_writing):
            if field in get_model_fields_list(User):
                ws.write(row, col, getattr(customer.user, field))
            else:
                ws.write(row, col, getattr(customer, field))

    wb.save(excelfile)

    response = HttpResponse(excelfile.getvalue())
    response['Content-Type'] = 'application/x-download'
    response['Content-Disposition'] = 'attachment;filename=table.xlsx'

    return response
