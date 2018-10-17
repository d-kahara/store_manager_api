# Store Manager API

## Introduction
![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Coverage Status](https://coveralls.io/repos/github/d-kahara/store_manager_api/badge.svg?branch=master)](https://coveralls.io/github/d-kahara/store_manager_api?branch=master)

### Features

1. Admin can add a product.
2. Admin/store attendant can get all products.
3. Admin/store attendant can get a specific product.
4. Store attendant can add a sale order.
5. Admin can get all sale order records.
6. Admin can add an attendant and assign admin privileges.


### Installing

*Step 1*

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

```$ python run.py```



#### Testing

```$ nosetests app/tests```