# revmicro_core service


![PyPI - Python Version](https://img.shields.io/pypi/pyversions/revcore_micro)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)



## Install

To install latest revcore_mirco for a specific service.
```console
$ pip install revcore_micro
```
To install revcore different version, and the dependencies required for that specific service.  
```console
$ pip install revcore_micro==[version]
```

## A Little Brief

> There's a bit different between **boto3** and **revcore_micro**

**Revcore-micro-service** is a package that allows you to easily implement AWS Services - dynamodb.

And the base code is by the AWS servise package boto3 




### ＊ In the previous Boto3 to create table :

```python3

import boto3

# Make sure credientials setup already

client = boto3.client('dynamodb')

resp = client.create_table(
        TableName="Bookstore",
        KeySchema=[
            {
                "AttributeName": "Author",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "Title",
                "KeyType": "RANGE"
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "Author",
                "AttributeType": "S"
            },
            {
                "AttributeName": "Title",
                "AttributeType": "S"
            }
        ]
       ...
```

### ＊ Now see Revcore_micro to create table :

```python3
from revcore_micro.ddb.models import Model


class Bookstore(Model):
    table_name = Bookstore
    region = 'ap-northeast-1'
    partition_key = 'Author'
    sort_key = 'Title'


bookstore = Bookstore()

# To initial the table to create
bookstore.init_table()   


```

### ＊ Table of Different


| **Action**            | **Boto3**                     | **Revcore_micro**               | 
|-----------------------|-------------------------------|---------------------------------|
| Create                | put_item                      | put                             |
| Read                  | get_item                      | get                             |
| Update                | put_item                      | put                             |
| Delete                | delete_item                   | delete                          |
| Query                 | query                         | query                           |
| Filter Query          | filter_query                  | filter_query                    |



## Usage

Must Inherit the models from revcore_micro first.

```python3
from revcore_micro.ddb.models import Model

#Inherit models.Model 
class Bookstore(Model):
    table_name = "bookstore"
    partition_key = "name"
    sort_key = "author"
    
#create a table in ddb
table = Bookstore()
table.init_table() 
```
### ＊ Put

```python3
# to create an item
table.put(name="Harry Potter, author="JK Rowling")
```

### ＊ Get

```python3
table.get(name="Harry Potter, author="JK Rowling")
```


### ＊ Delete

```python3
table.delete(name="Harry Potter, author="JK Rowling")
```

### ＊ Query

```python3
table.query(name="Harry Potter, author="JK Rowling")
```
