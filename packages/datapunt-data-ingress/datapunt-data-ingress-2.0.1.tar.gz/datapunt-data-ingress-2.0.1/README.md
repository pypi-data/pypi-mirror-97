# Data Ingress

This is a simple ingress app which stores all incoming messages in a queue categorized
into collections. 

Data is always posted in the form of messages to a specific collection, 
and can be processed from the queue by consumers.


## Usage:

### 1. Add the app
Enable in installed apps:

```python
INSTALLED_APPS = [
    ...,
    'ingress'
]
```

### 2. Create and configure a consumer
Implement a consumer to handle the data. Note: the ingress can be deployed without a 
consumer when you (probably temporarily) want to ingest data, but not consume it.

```python
class MyConsumer(IngressConsumer):
    collection_name = 'foobar'

    def consume_message(self):
        ...

    # by default consume_batch() loops and calls consume_message(), but it can be 
    # overridden to have more control, for instance to bulk insert into the db.
    def consume_batch(self):
        ...
```

Configure the consumer in settings.py.  Each consumer must implement the BaseConsumer
and implement the proper methods (see above). On consumption consumers are passed 
all messages in the collection that corresponds to `Consumer.collection_name`.
```python
# A list of classpaths to implementations of ingress.consumer.IngressConsumer
# to handle the data in the queue.
INGRESS_CONSUMER_CLASSES = ['app.module.MyConsumer']
```

### 3. Authentication and Authorization
Configure at least the authentication classes or permission classes:
```python
# A list of authentication classes used in the ingress view.
# See https://www.django-rest-framework.org/api-guide/authentication/
INGRESS_AUTHENTICATION_CLASSES = []

# A list of permission classes used in the ingress view.
# See https://www.django-rest-framework.org/api-guide/permissions/
INGRESS_PERMISSION_CLASSES = []
```

### 4. Accept data posted to non-existing collections?
By default data posted to non-existing collections is not stored, and an error is 
returned for such requests.

If data posted to non-existing collections should be stored, modify the setting:
```python
# Whether or not to accept data posted to a non-existing collection.
INGRESS_ACCEPT_NEW_COLLECTIONS = False
```

### 5. Set encoding when other than UTF-8
By default the ingress decodes all incoming data using UTF-8. If the data needs to be
decoded differently before being stored in the database, configure the setting:
```python
# Encoding that the data will be in when posted to the ingress
INGRESS_ENCODING = "utf-16"
```