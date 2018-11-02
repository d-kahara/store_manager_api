![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Coverage Status](https://coveralls.io/repos/github/d-kahara/store_manager_api/badge.svg?branch=bg-Tests-Travis-CRUD-fix-161645246)](https://coveralls.io/github/d-kahara/store_manager_api?branch=bg-Tests-Travis-CRUD-fix-161645246)
[![Build Status](https://travis-ci.org/d-kahara/store_manager_api.svg?branch=bg-test-refactor-%23161365564)](https://travis-ci.org/d-kahara/store_manager_api)[![Code Climate](https://codeclimate.com/github/codeclimate/codeclimate/badges/gpa.svg)](https://codeclimate.com/github/d-kahara/store_manager_api)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/65dc0c9d43554d21843a56817fd02525)](https://www.codacy.com/app/d-kahara/store_manager_api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=d-kahara/store_manager_api&amp;utm_campaign=Badge_Grade)


[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/f20490b7d2ae6b24f453)

# Store Manager API

### Features

1. Admin can add a product.
2. Admin/store attendant can get all products.
3. Admin/store attendant can get a specific product.
4. Store attendant can add a sale order.
5. Admin can get all sale order records.
6. Admin can add an attendant and assign admin privileges.


### Database
* Swith to postgres account (in terminal)
    ```
    sudo su - postgres
    ```
* Run PostgreSQL command line client.
    ```
    psql
    ```
* Create a database user with a password.
    ```
    CREATE USER store_owner with password 'password12345';
    ```
* Create a database instance.
    ```
    CREATE DATABASE store_manager owner store_owner encoding 'utf-8';
    ```
* Create the test database instance.
    ```
    CREATE DATABASE store_manager_test owner store_owner encoding 'utf-8';
    ```


### Installing

Create directory
```$ mkdir store-manager```

```$ cd store-manager```

Clone the repository [```here```](https://github.com/d-kahara/store_manager_api) or 

``` git clone https://github.com/d-kahara/store_manager_api ```

Create and activate virtual environment

```$ virtualenv env -p python3```


* Create a ```.env```  file in the root of the project folder and add the following
    ```
    export FLASK_APP="run.py"
    export APP_SETTINGS="development"
    export FLASK_SKIP_DOTENV=1  
    source env/bin/activate

    export DATABASE_TEST_URI='postgresql://store_owner:password12345@localhost:5432/store_manager_test'

    export DATABASE_URI='postgresql://store_owner:password12345@localhost:5432/store_manager'

    ```
* Run the following to add the above in the environment and activate virtual environment
    ```
    source .env
    ```



Install project dependencies 


```$ pip install -r requirements.txt```

#### Running the application

```$ flask run```



#### Testing

```$  python run.py test2```



### API-Endpoints

#### Product Endpoints : /api/v2/

Method | Endpoint | Functionality
--- | --- | ---
POST | /products | Post a product
GET | /products | Get a List of all products
GET | /products/int:product_id | Get a product using its id
PUT | /products/int:product_id | Update Product Details
Delete  | /products/int:product_id  | Delete a product record 

#### Sales Endpoints : /api/v2
Method | Endpoint | Functionality
--- | --- | ---
POST | /sales | Post a sale
GET | /sales | Get a List of all sales
GET | /sales/int:sale_id | Get a sale using its id

#### Auth Endpoints : /api/v2
Method | Endpoint | Functionality
--- | --- | ---
Regiser | /auth/register | Register a new user
Login | /auth/login | Logs in a user and generates auth token
Logout | /auth/logout | Logs out a user and blacklists auth token
