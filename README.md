# Instalation
```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8010
```

## Aditional Info
-   Developed with: Python3.9.2
-   In the main folder, there is a file called clients.csv, which contains some clients information.
-   In the main folder, there is a file called db.sqlite3, which contains the database used in development.
-   In the main folder, there is a file called quick.postman_collection.json, which contains the postman collection used in development.


---

| LinkedIn | https://www.linkedin.com/in/williambarriga/ |
| ------ | ------ |
| Github | https://github.com/WilliamBarriga |

---


# Documentacion API

## __SignIn__
-   Method: POST
-   Path: /api/signin/
-   Parameters:
    -   email: string
    -   password: string
    -   password_confirmation: string
-   response:
    -   username: string
    -   mail: string
-   Example:
```json
{
    "email": "test1@gmail.com",
    "password": "1234qwe.",
    "password_confirmation": "1234qwe."
}
```

## __Create Token__
-   Method: POST
-   Path: /api/token/
-   Parameters:
    -   username: string (the registered mail)
    -   password: string
-   response:
    -   token: string
    -   refresh: string
-   Example
```json
{
    "username":"test1@gmail.com",
    "password":"1234qwe."
}
```

## __Create one product__
-   Method: POST
-   Path: /api/product/
-   Parameters:
    -   name: string
    -   description: string
    -   attributes: list/array of strings
-   response:
    -   product_id: int
    -   product_name: string
-   Example
```
{
    "product_id": 4,
    "product_name": "new product 6"
}
```

## __get products__
-   Method: GET
-   Path: /api/product/
-   Query_parameters:
    -   id: int | optional
-   response:
    -   json/object or list of json/objects
        -   id: int
        -   is_active: boolean
        -   name: string
        -   description: string
        -   attributes: list/array of strings
-   Example
```
URL: http://127.0.0.1:8010/api/product?id=1
{
    "id": 1,
    "is_active": true,
    "name": "greatProduct",
    "description": "a great description",
    "attributes": [
        "good",
        "awesome",
        "pro"
    ]
}
```
```
URL: http://127.0.0.1:8010/api/product
[
    {
        "id": 1,
        "is_active": true,
        "name": "greatProduct",
        "description": "a great description",
        "attributes": [
            "good",
            "awesome",
            "pro"
        ]
    },
    {
        "id": 2,
        "is_active": true,
        "name": "another great product",
        "description": "awesome description",
        "attributes": [
            "little",
            "aio",
            "compact"
        ]
    }
]
```
## __Create/Update/Delete client__
-   Method: POST
-   Path: /api/client/
-   Parameters:
    -   initial_key: string | action
        -   id: int | optional
        -   first_name: string
        -   last_name: string
        -   email: string
-   response:
    -   id: int
    -   first_name: string
    -   last_name: string
    -   email: string
-   Example
```
{
    "delete": {
        "id": 4,
        "first_name": "client4",
        "last_name": "importatn",
        "email": "client4@gmail.com"
    }
}
```
```
{
    "create": {
        "first_name": "client4",
        "last_name": "importatn",
        "email": "client4@gmail.com"
    }
}
```

## __get clients__
-   Method: GET
-   Path: /api/client/
-   Query_parameters:
    -   id: int | optional
-   response:
    -   json/object or list of json/objects
        -   id: int
        -   first_name: string
        -   last_name: string
        -   email: string
-   Example
```
URL http://127.0.0.1:8010/api/client
[
    {
        "id": 1,
        "document": 100000000,
        "first_name": "client0",
        "last_name": "important",
        "email": "client0@example.com"
    },
    {
        "id": 2,
        "document": 100000001,
        "first_name": "client1",
        "last_name": "important",
        "email": "client1@important.com"
    },
]
```
```
URL http://127.0.0.1:8010/api/client?id=1
{
    "id": 1,
    "document": 100000000,
    "first_name": "client0",
    "last_name": "important",
    "email": "client0@example.com"
}
```

## __Get file clients__
-   Method: GET
-   Path: /api/clients/
-   Query_parameters:
    -   id: int | optional
-   Response:
    -   CSV File
-   Example URLS:
    -   http://127.0.0.1:8010/api/clients?id=1
    -   http://127.0.0.1:8010/api/clients/

## __Create file clients__
-   Method: POST
-   Path: /api/clients/
-   Parameters:
    -   file: CSV File
-   Response:
    -   Array of clients