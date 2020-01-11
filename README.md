# Customers app

## This app provides:

1. Viewing information from database about customers with sorting and filtering functions.
2. Creating customers.
3. Manipulate customers's data.
4. Vote for customers's photos.
5. Export information about customers in xlsx file

## All manipulations with data are available by:

1. Django Admin
2. Simple graphic interface
3. REST API

## Installation:

1. `git clone https://github.com/kirill-ilichev/WIS.git`
2. `cd WIS`
3. `python3 -m venv venv`
4. `source venv/bin/activate`
5. `pip3 install -r requirements.txt`
6. `python manage.py migrate`
7. `python manage.py createsuperuser`
8.  Follow the instructions from terminal
9. `python manage.py runserver 8000`
10. Follow the link from terminal and visit admin page (example : http://127.0.0.1:8000/admin/)
11. Log in with username and password that you wrote when created a superuser
12. Create a customer and in field user chose your superuser, don't forget about photo!
13. Done! Now you can visit your page by link http://127.0.0.1:8000/customers/1/

# Links for graphic interface:
| *URL* | 
|-------| 
| `/`   |
|Home page with list of links on other project's pages|

| *URL*               |
|---------------------|  
| `/customers/list/`  |
|Page with information about customers. Allows filter and sort customer's information by buttons|

| *URL* |
|-------|
| `/customers/voting/`|
|Page with photos and points for each photo. Allows to vote for certain photo by click on button near photo's points |

| *URL* | 
|-------| 
|`/customers/create/`|
|Registration page|

| *URL* | 
|-------| 
|`/customers/auth/`|
|Authentication page|

| *URL* | 
|-------| 
|`/customers/logout/`|
|Logout page|

| *URL* | 
|-------| 
|`/customers/{customers_id}/`|
|Detail customer's page|

| *URL* | 
|-------| 
|`/customers/{customers_id}/delete/`|
|Delete customer's page|

| *URL* | 
|-------| 
|`/customers/export/`|
|Collects information about customers and export it in xlsx file. Then allows customer to chose where to save export file|


# REST API end points

| *URL* | *Method*|*Description*|
|-------|---------|-------------|
| `/api/token/` | `POST` | Get JWT Token by username and password|

Request:
```
{
  "username": string,
  "password": string
}
```

Success Response:
- Content:

```
{
    "refresh": "token_to_refresh",
    "access": "token_to_access"
}
```
Use token_to_access to verify your account. Set token to HEADERS (KEY: Authorization, VALUE: Bearer token_to_access)



| *URL* | *Method*|*Description*|
|-------|---------|-------------|
| `/api/token/refresh/` | `POST` | Refresh JWT Token by token_to_refresh|

Request:
```
{
  "refresh": token_to_refresh,
}
```

Success Response:
- Content:

```
{
    "access": "token_to_access"
}
```


## All info about next endpoints in APIViews.py
| *URL* | *Method*|*Description*|
|-------|---------|-------------|
| `api/customers/list/` | `GET` | Data of all customers|

| *URL* | *Method*|*Description*|
|-------|---------|-------------|
| `api/customers/create/` | `POST` | Create new customer with user account and photo|

| *URL* | *Method*|*Description*|
|-------|---------|-------------|
| `api/customers/voting/` | `GET` / `POST` | Data about customer's photos with opportunity to vote for photo|

| *URL* | *Method*|*Description*|
|-------|---------|-------------|
| `api/customers/{id_of_customer}/`| `GET` / `PATCH` / `DELETE` | Data about certain customer and opportunity to change his data |

