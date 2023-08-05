"""
:mod: `postgres_db`
=====================

Methods for interacting with database systems that support the REST API.

.. module:: postgres_db
.. module_author:: Aminov Emil
.. module_author:: Niel (Ketov) Gorev <ketov-x@ya.ru>
.. module_author:: http://t.me/ketov-x
"""
import json

import requests
from requests.exceptions import HTTPError


class BaseDBClient:
    """Basic methods of interaction with the database.

    .. note:: The base client is a great way to write a convenient wrapper
    to get specific models from the database.
    Thus, you can create child classes that contain wrappers around the
    existing methods, or implement this class in another, for hidden access
    to the database.

    **parameters**, **types**
    -------------------------
    **types**::

    :type db_manager_url: str.

    **parameters**::

    :param db_manager_url: The address of the service providing the REST API
    for working with the database. [1]_

    **footprints**
    --------------

    [1] The URL specified this field must be the route to which the substring
    '/<model_name>/<primary_key>' is substituted and all of the following
    methods are executed: GET, POST, PUT, DELETE.
    """

    def __init__(self, db_manager_url: str):
        self.manager_url = db_manager_url + "/api/model"

    def get_object_by_id(self, model_name: str, pk: int or str):
        """Get model object by unique identifier (ID).

        :type model_name: str.
        :type pk: int or str.

        :param model_name: The name of the collection or table in the database.
        :param pk: The unique identifier of the received object.
        :return: dict.
        """
        request_path = f'{self.manager_url}/{model_name}/{pk}'

        def _get_object_by_id():
            """Executing a query on the model."""
            _data = requests.get(request_path)
            if not _data.status_code == 200:
                raise HTTPError(data['error_message'])
            return _data.json() if _data.status_code == 200 else None

        data = _get_object_by_id()
        response = data if data and len(data) > 0 else None
        return response

    def get_objects(self, model_name: str,
                    filters: dict = None,
                    limit: int = None,
                    offset: int = None):
        """Get a list of objects for a specific model.

        :type model_name: str.
        :type filters: dict.
        :type limit: int.
        :type offset: int.

        :param model_name: The name of the collection or table in the database.
        :param filters: They are indicated as a dictionary, the keys
        of which are possible fields (columns). [1]_
        :param limit: How many values to return. [2]_
        :param offset: How many values to ignore. [3]_
        :return: list.

        [1] Only those entities for which the statement is true will
        be returned: the column name is equal to one of the dictionary keys,
        and its value is equal to the corresponding value in the dictionary.
        [2] The maximum number of items specified will be returned. Those,
        if the base does not have the number of elements specified in the
        limit field, all available elements will be returned, otherwise None.
        [3] I mean how many received values from the beginning of the request
        should be skipped. Thus, if you specify offset equal to ten, then the
        first 10 lines of the query will be skipped.
        """
        filters = {} if not filters else filters
        request_path = f'{self.manager_url}/list/{model_name}'
        if limit and offset:
            response = requests.get(request_path + '?{}&{}&{}'.format(
                f'filters={json.dumps(filters)}',
                f'limit={limit}',
                f'offset={offset}'
            ))
        elif limit:
            response = requests.get(request_path + '?{}&{}'.format(
                f'filters={json.dumps(filters)}',
                f'limit={limit}'
            ))
        elif offset:
            response = requests.get(request_path + '?{}&{}'.format(
                f'filters={json.dumps(filters)}',
                f'offset={offset}'
            ))
        else:
            response = requests.get(request_path + '?{}'.format(
                f'filters={json.dumps(filters)}'
            ))
        return response.json()

    def insert_object(self, model_name: str, data: dict):
        """Create a new object of the corresponding model.

        :type model_name: str.
        :type data: dict.

        :param model_name: The name of the collection or table in the database.
        :param data: The data to be saved in the model.
        :return: dict.
        """
        request_path = f'{self.manager_url}/{model_name}'
        response = requests.post(request_path, json=data)
        data = response.json()
        if not response.status_code == 200:
            raise HTTPError(data['error_message'])
        return data

    def update_object(self, model_name: str, pk: int, data: dict):
        """Refresh data for a specific object in the model.

        :type model_name: str.
        :type pk: int.
        :type data: dict.

        :param model_name: The name of the collection or table in the database.
        :param data: The data to be saved in the model.
        :param pk: The unique identifier of the received object.
        :return: dict.
        """
        request_path = f'{self.manager_url}/{model_name}/{pk}'
        response = requests.patch(request_path, json=data)
        data = response.json()
        if not response.status_code == 200:
            raise HTTPError(data['error_message'])
        return data

    def put_object(self, model_name: str, pk: int, data: dict):
        """Replacing the data of a specific model object.

        :type model_name: str.
        :type pk: int.
        :type data: dict.

        :param model_name: The name of the collection or table in the database.
        :param data: The data to be saved in the model.
        :param pk: The unique identifier of the received object.
        :return: dict.
        """
        request_path = f'{self.manager_url}/{model_name}/{pk}'
        response = requests.put(request_path, json=data)
        data = response.json()
        if not response.status_code == 200:
            raise HTTPError(data['error_message'])
        return data

    def delete_object_by_id(self, model_name: str, pk: int):
        """Removes a specific object from the model data.

        :type model_name: str.
        :type pk: int.

        :param model_name: The name of the collection or table in the database.
        :param pk: The unique identifier of the received object.
        :return: dict.
        """
        request_path = f'{self.manager_url}/{model_name}/{pk}'
        response = requests.delete(request_path)
        data = response.json()
        if not response.status_code == 200:
            raise HTTPError(data['error_message'])
        return data

    def get_object_by_field(self, model_name: str,
                            field_name: str, field_value: object):
        """Returns one or more objects for which the value of the field
        'field_name' is equal to the value of 'field_value'.

        :type model_name: str.
        :type field_name: str.
        :type field_value: any.

        :param model_name: The name of the collection or table in the database.
        :param field_name: The name of the field or column by which the
        selection is made.
        :param field_value: A specific value that will be sampled.
        :return: dict or list
        """
        data = self.get_objects(model_name, filters={field_name: field_value})
        obj = data if data and len(data) == 0 else data[0]
        return obj


class DBUserClient(BaseDBClient):
    """An extension to the BaseDBClient that adds work
    exclusively with the user model.

    .. note:: For arguments, types and a detailed description of the models,
    see the description of the BaseDBClient class.
    """
    def __init__(self, db_manager_url: str):
        super().__init__(db_manager_url)

    def is_user_exist(self, client_app, client_id):
        """Checks if a user with the specified ID
        exists inside the Dialog service system

        :type client_app: str.
        :type client_id: str.

        :param client_app: The client application through which the
        user is accessing.
        :param client_id: Use the identifier inside the client application.
        :return: bool
        """
        user = self.get_object_by_field('User', client_app + '_id', client_id)
        return True if user and 'phone_number' in user else False

    def get_user_by_client_id(self, client_app: str,
                              user_id: int):
        """

        :param client_app:
        :param user_id:
        :return: dict
        """
        data = self.get_object_by_field('User', client_app + '_id', user_id)
        return data
        # TODO: требует добавления

    def add_token_for_user(self, client_app: str, user_id: int,
                           token_type: str, token: str):
        """

        :param client_app:
        :param user_id:
        :param token_type:
        :param token:
        :return:
        """
        data = self.get_user_by_client_id(client_app, user_id)
        if data:
            data['tokens'][token_type] = token
            updated_data = self.update_object('User', data.get('_id'), data)
            return updated_data
        raise HTTPError(f'No user found with id = {user_id}')


class DBClient(DBUserClient):
    """Export"""
