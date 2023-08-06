# Webservice Stash

A PyPI packages that supports all the necessary error codes, validation exception, common exceptions of a webservice. This PyPI package includes a method that establishes the connection to your firebase account.

## Installation

Run the following to install:

```cmd
pip install stash-service
```

## Usage

#### Connect to Firestore with key

A connection can be established easily with your Firestore account. This method receives two mandatory parameters. The first string parameters receives your collection name of the Firestore database and the second string or dictionary parameter will receive your firestore account's secret key.

```python
from stash_service import connect_firestore_with_key

db_reference = connect_firestore_with_key(collection_name, firestore_secret_key)
```

---

MIT Licensed - 2021 : Britsa - britsa.tech@gmail.com

Contributors:
Maria Irudaya Regilan J

---