# Store Manager API

## Introduction
![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Coverage Status](https://coveralls.io/repos/github/d-kahara/store_manager_api/badge.svg?branch=bg-test-refactor-%23161365564)](https://coveralls.io/github/d-kahara/store_manager_api?branch=bg-test-refactor-%23161365564)
[![Build Status](https://travis-ci.org/d-kahara/store_manager_api.svg?branch=bg-test-refactor-%23161365564)](https://travis-ci.org/d-kahara/store_manager_api)[![Code Climate](https://codeclimate.com/github/codeclimate/codeclimate/badges/gpa.svg)](https://codeclimate.com/github/d-kahara/store_manager_api)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/65dc0c9d43554d21843a56817fd02525)](https://www.codacy.com/app/d-kahara/store_manager_api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=d-kahara/store_manager_api&amp;utm_campaign=Badge_Grade)

### Features

1. Admin can add a product.
2. Admin/store attendant can get all products.
3. Admin/store attendant can get a specific product.
4. Store attendant can add a sale order.
5. Admin can get all sale order records.
6. Admin can add an attendant and assign admin privileges.

### Installing

Create directory
```$ mkdir store-manager```

```$ cd store-manager```

Create and activate virtual environment

```$ virtualenv env -p python3```


```$ source env/bin/activate```

Clone the repository [```here```](https://github.com/d-kahara/store_manager_api) or 

``` git clone https://github.com/d-kahara/store_manager_api ```

Install project dependencies 


```$ pip install -r requirements.txt```

#### Running the application

```$ python run.py run```



#### Testing

```$  python run.py test```



### API-Endpoints

#### Product Endpoints : /api/v1/

Method | Endpoint | Functionality
--- | --- | ---
POST | /products | Post a product
GET | /products | Get a List of all products
GET | /products/int:product_id | Get a product using its id

#### Sales Endpoints : /api/v1
Method | Endpoint | Functionality
--- | --- | ---
POST | /sales | Post a sale
GET | /sales | Get a List of all sales
GET | /sales/int:sale_id | Get a sale using its id

#### Auth Endpoints : /api/v1
Method | Endpoint | Functionality
--- | --- | ---
Regiser | /auth/register | Register a new user
Login | /auth/login | Logs in a user and generates auth token
Logout | /auth/logout | Logs out a user and destroys auth token
