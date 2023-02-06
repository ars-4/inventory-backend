# Stock Management System

##### Backend for stock management system by Shahzaib Durrani and ARS. Made entirely on Python and VueJS

---

<br>

## Installation
---
* Clone the repo and cd into it.
* Install python and virtualenv.
    * `pip install virtualenv`
* Create and activate virtualenv.
    * `virtualenv venv & venv\Scripts\activate`
* Install requirements.txt.
    * `pip install -r requirements.txt`
* Migrate.
    * `py manage.py migrate`

---

<br>
<br>

## Usage
---
* Start the server.
    * `py manage.py runserver`
* In browser go to
    * `http://127.0.0.1:8000/`
* Send JSON request to the url
    * `{
        "title": "title_of_product",
        "description": "description",
        "type": "qty",
        "sale_price": "3000",
        "purchase_price": "2500",
        "stock": "0"
        }`