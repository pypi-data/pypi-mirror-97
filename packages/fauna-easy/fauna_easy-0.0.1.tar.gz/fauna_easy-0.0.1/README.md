# Fauna Easy Python
A convenient wrapper around faunadb for python that abstracts away FQL code for the database service faunadb

## Installation

Use the package manager [pip](https://pypi.org/) to install fauna-easy.

```bash
pip install fauna_easy
```

## QuickStart

```python
from fauna_easy.base_model import FaunaEasyBaseModel
from pydantic import BaseModel
from faunadb.client import FaunaClient

if __name__ == '__main__':
    class NewPost(BaseModel):
        title: str
        content: str

    fauna_client = FaunaClient('YOUR_CLIENT_SECRET')

    Post = FaunaEasyBaseModel('posts', NewPost)

    create_query = Post.create({
        'title': 'my post title',
        'content': 'my post content'
    }) # Will not automatically create document in database. This merely creates the query

    created_documents = fauna_client.query(create_query) # creates document in database
    print(created_documents)
```

## Documentation
Still under development :)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)
