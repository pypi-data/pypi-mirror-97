"""
:mod: `dialog_models`
=====================

Description of models of Dialog service
applications interacting with requests

.. module:: skill_models
.. module_author:: Niel (Ketov) Gorev <ketov-x@ya.ru>
.. module_author:: http://t.me/ketov-x
"""
from dataclasses import dataclass, field
from scintillant.apimodels.types import DialogAnswerRequestType


@dataclass()
class DialogAnswerRequest(DialogAnswerRequestType):
    """Request model for the Dialog service.

    Relationship diagram
    ---------------------
    Client (**DialogAnswerRequest**) -> Dialogs \n
    Dialogs (SkillRequest) -> Skill (SkillResponse) -> Dialogs \n
    Dialogs (ClientResponse) -> Client \n

    **parameters**, **types**
    -------------------------
    **types**::

    :type client_id: str.
    :type client_app: str.
    :type client_type: str or None
    :type in_text: str or None.
    :type in_choice: str or None.

    **parameters**::

    :param client_id: str, Unique identifier for the customer, such as telegram ID or phone number. Not Null.
    :param client_app: str, The name of the client accessing the Dialog. [1]_
    :param in_text: str or None, The message that the user sent to the client. [2]_
    :param in_choice: User-made selection. [3]_

    **footprints**
    --------------

    [1] Clients are the services of the layer between the application servers and Dialog,
    but the name is correct for the application. Thus, for a bot responding to messages in telegrams,
    client_app will be equal to 'telegram'. Not Null.
    [2] This field is required if the in_choice field is empty.
    [3] The choice is made based on the values of the Choices field received in the ClientResponse.
    For instance:``
    >> choices = ClientResponse(...).choices # [["Choose the first", 1], ["Choose the second", 2]]
    >> da = DialogAnswerRequest(..., in_choice="Choose the first")``
    """
    client_id: str = field()
    client_app: str = field()
    in_text: str = field(default=None)
    in_choice: str = field(default=None)
    client_type: str = field(default='text')

    @classmethod
    def from_dict(cls, data: dict) -> DialogAnswerRequestType:
        """Generation DialogAnswerRequest from aiohttp.Request

        .. Example:: TODO
            >> @app.get('/')
            >> async def my_func(request: aiohttp.Request):
            >>      da = await DialogAnswerRequest.from_aio_request(request)
            >>      ...

        :type data: dict

        :param data: Model Generation Data.
        :return: DialogAnswerRequest
        """
        return cls(
            client_id=data.get('client_id'),
            client_app=data.get('client_app'),
            client_type=data.get('client_type'),
            in_text=data.get('in_text'),
            in_choice=data.get('in_choice'),
        )

    def serialize_json(self) -> dict:
        """Returns a templated dictionary based on the fields of the class.

        This function is designed to send a class as JSON within HTTP requests or to respond to similar requests.

        .. Example aiohttp::
            >> @app.get('/')
            >> async def my_munc(request: Request):
            >>      da = DialogAnswerRequest()
            >>      ...
            >>      return web.json_response(da.serialize_json(), status=200)

        .. Example flask::
            >> @app.route('/', methods=['GET'])
            >> def my_munc():
            >>      da = DialogAnswerRequest()
            >>      ...
            >>      return da.serialize_json(), 200

        :return: dict
        """
        return {
            'client_id': self.client_id,
            'client_app': self.client_app,
            'client_type': self.client_type,
            'in_text': self.in_text,
            'in_choice': self.in_choice
        }