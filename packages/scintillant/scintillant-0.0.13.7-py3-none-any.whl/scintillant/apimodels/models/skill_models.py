"""
:mod: `skill_models`
=====================

Description of models of Skills
applications interacting with requests.

.. module:: skill_models
.. module_author:: Niel (Ketov) Gorev <ketov-x@ya.ru>
.. module_author:: http://t.me/ketov-x
"""
from dataclasses import dataclass, field
from datetime import datetime

from scintillant.apimodels.types import SkillResponseType, SkillRequestType


@dataclass
class SkillResponse(SkillResponseType):
    """The skill response to a Dialog service request.

    Relationship diagram
    ---------------------
    Client (DialogAnswerRequest) -> Dialogs \n
    Dialogs (SkillRequest) -> Skill (**SkillResponse**) -> Dialogs \n
    Dialogs (ClientResponse) -> Client \n

    **parameters**, **types**
    -------------------------
    **types**::

    :type status: str.
    :type out_text: str or None.
    :type choices: list or None.
    :type attach: None.
    :type client_app_action: str or None.
    :type request_field_code: str or None.
    :type context: dict or None.
    :type redirect_to: str or None.

    **parameters**::

    :param status: Responsible for the action that the Dialog will take after receiving a response. Not Null. [1]_
    :param out_text: The text that the client will receive to respond to the user. May be HTML text.
    :param choices: A set of lists displayed to the client in the form of buttons or lists. [2]_
    :param attach: This functionality is under development. [3]_
    :param client_app_action: An action that can be performed by any client, if the interface allows it. [4]_
    :param request_field_code: The name of the validator. [5]_
    :param context: Dictionary containing arbitrary JSON-serializable parameters. [6]_
    :param redirect_to: Pointer to the name of the skill to redirect the request to. [7]_

    .. note:: The context returned by the Dialog service can be used instead of the local data stores
    of the form Key: Value. This will allow the skills to save space and memory on a running machine,
    as well as respond more quickly to user requests.

    **footprints**
    --------------

    [1] For instance:
        - exit, Finishes the skill completely ignoring the out_text field.
        In this case, the user will receive a standard Dialog service start phrase in response.
        - wait,Having received this status, the Dialog service will give the user an answer that his request
        is being processed. After 3-5 seconds, the service will send a second request with the old parameters,
        expecting to receive a response. After the Dialog service receives the 'waiting' status for the 3rd time,
        the requests will stop going, and the user will receive an error message.
        - redirect, With this parameter, the Dialog service will ignore all other class fields except redirect_to.
        The user will receive a response from the skill whose name is written in redirect_to, if this skill exists
        and functions, otherwise the user will receive a response that the bot does not understand what the user wants.
    [2] The first item in the list is the visible value, the second is the returned payload.
    For instance: ``[["Choose the first", 1], ["Choose the second", 2]]``
    [3] In the future, it will allow sending images, audio files and other files to users.
    [4] For example, delete the next message from a user (tek clients) or request a phone number (Exclusively telegrams).
    The list of actions available on clients is now expanding, but here are a couple of examples:
        - REQUEST_PHONE_NUMBER;
        - REMOVE_PREVIOUS_USER_MESSAGE.
    [5] This field is used at your own risk. it is supported by a very limited number of clients. For instance:
        - PHONE_NUMBER;
        - VEHICLE_NUMBER.
    [6] The specified values will be saved by the Dialog service and sent unchanged in the all requests.
    [7] Without the status parameter equal to 'redirect', this parameter is ignored.
    """
    status: str = field()
    out_text: str or None = None
    choices: list or None = None
    attach: None = None  # TODO: Отправка изображений, звуков, карт

    client_app_action: str or None = None
    requested_field_code: str or None = None

    context: dict or None = field(default_factory=dict)
    redirect_to: str or None = None

    @classmethod
    def from_dict(cls, data: dict) -> SkillResponseType:
        """Generate SkillResponse from dict data.

        .. Example 1:: TODO
            >> import requests
            >> sr = SkillResponse._from_dict(requests.get(skill-url).json)
            >> print(sr)

        .. Example 2:: TODO
            >> sr = SkillResponse._from_dict({'status': ...})
            >> print(sr

        :type data: dict.

        :param data: Model Generation Data.
        :return: SkillResponse.
        """
        return cls(
            status=data.get('status'),
            out_text=data.get('out_text'),
            choices=data.get('choices'),
            attach=None,
            client_app_action=data.get('client_app_action'),
            requested_field_code=data.get('requested_field_code'),
            context=data.get('context'),
            redirect_to=data.get('redirect_to')
        )

    @classmethod
    def from_response(cls, response) -> SkillResponseType:
        """Generate SkillResponse from basic requests.Response.

        .. Example::
            >> import requests
            >> sr = SkillResponse.from_response(requests.get('skill-url'))
            >> print(sr)

        :type response: requests.Response.

        :param response: HTTP response from the skill service.
        :return: SkillResponse.
        """
        json = response.json()
        return cls.from_dict(json)

    def serialize_json(self) -> dict:
        """Returns a templated dictionary based on the fields of the class.

        This function is designed to send a class as JSON within HTTP requests or to respond to similar requests.

        .. Example aiohttp::
            >> @app.get('/')
            >> async def my_munc(request: Request):
            >>      sr = SkillResponse()
            >>      ...
            >>      return web.json_response(sr.serialize_json(), status=200)

        .. Example flask::
            >> @app.route('/', methods=['GET'])
            >> def my_munc():
            >>      sr = SkillResponse()
            >>      ...
            >>      return sr.serialize_json(), 200

        :return: dict
        """
        return {
            "status": self.status,
            "out_text": self.out_text,
            "choices": self.choices,
            "client_app_action": self.client_app_action,
            "requested_field_code": self.requested_field_code,
            "context": self.context,
            "redirect_to": self.redirect_to
        }


@dataclass
class SkillRequest(SkillRequestType):
    """Skill request from Dialog service.

    Relationship diagram
    ---------------------
    Client (DialogAnswerRequest) -> Dialogs \n
    Dialogs (**SkillRequest**) -> Skill (SkillResponse) -> Dialogs \n
    Dialogs (ClientResponse) -> Client \n

    **parameters**, **types**
    -------------------------
    **types**::

    :type user: SkillRequest.User.
    :type update: SkillRequest.Update.
    :type context: dict or None

    **parameters**::

    :param user: Data about the user who sent the request. Not Null.
    :param update: Information of the request sent by the user. Not Null.
    :param context: Dictionary containing arbitrary JSON-serializable parameters. [1]_

    .. note:: Initially, the request for this model goes to a URL like ... /skill,
    but the application of this model is not limited to this route.
    This model can be used to write complex tests for skills in order to simulate
    a real request from the Dialog service.

    **footprints**
    --------------

    [1] The specified values will be saved by the Dialog service and sent unchanged in the all requests.
    """
    @dataclass
    class User:
        """Data about the user who sent the request.

        :type user_id: str.
        :type client: dict.
        :type global_id: str or None.

        :param user_id: Unique identifier for the customer, such as telegram ID or phone number. Not Null.
        :param client: The name of the client accessing the Dialog.
        :param global_id: User identifier within the Dialog service system. [1]_

        [1] Using this identifier, you can request additional data about the user:
            - Phone number;
            - Email;
            - Authorizations.
        """

        @dataclass
        class Client:
            name: str = field()
            type: str = field()
            _meta_: dict = field(default=None)

        user_id: str = field()
        client: Client = field()
        global_id: str or None

    @dataclass
    class Update:
        """Information of the request sent by the user.

        :type in_text: str.
        :type in_choice: str.
        :type datetime: int.

        :param in_text: The message that the user sent to the client.
        This field is required if the in_choice field is empty.
        :param in_choice: User-made selection. [1]_
        :param datetime: Time of sending a request from a client service (Telegram, VK, etc.).

        [1] The choice is made based on the values of the Choices field received in the ClientResponse. For instance:``
        >> choices = ClientResponse(...).choices # [["Choose the first", 1], ["Choose the second", 2]]
        >> da = DialogAnswerRequest(..., in_choice="Choose the first")``
        """
        in_text: str = field(default=None)
        in_choice: str = field(default=None)
        datetime: int = field(default=datetime.now().timestamp())

        def __init__(self, in_text=None, in_choice=None, datetime=None):
            if not (in_text or in_choice):
                raise Exception("Update must contain at least one update value (in_text or in_choice)")
            self.in_text = in_text
            self.in_choice = in_choice
            self.datetime = datetime if datetime else None

    user: User
    update: Update
    context: dict

    @classmethod
    def from_dict(cls, data: dict) -> SkillRequestType:
        """Generate SkillRequest from dict data.

        .. Example:: TODO
            >> sr = SkillRequest._from_dict({'status': ...})
            >> print(sr

        :type data: dict.

        :param data: Model Generation Data.
        :return: SkillRequest.
        """
        user, upd, ctx = data.get('User'), data.get('Update'), data.get('Context')
        return cls(
            user=cls.User(
                user_id=user.get('user_id'),
                client=cls.User.Client(
                    name=user.get('client')['name'],
                    type=user.get('client')['type']
                ),
                global_id=user.get('global_id')
            ),
            update=cls.Update(
                in_text=upd.get('in_text'),
                in_choice=upd.get('in_choice'),
                datetime=upd.get('datetime', datetime.now().timestamp())
            ),
            context=ctx
        )

    def serialize_json(self) -> dict:
        """Returns a templated dictionary based on the fields of the class.

        This function is designed to send a class as JSON within HTTP requests or to respond to similar requests.

        .. Example aiohttp::
            >> @app.get('/')
            >> async def my_munc(request: Request):
            >>      sr = SkillRequest()
            >>      ...
            >>      return web.json_response(sr.serialize_json(), status=200)

        .. Example flask::
            >> @app.route('/', methods=['GET'])
            >> def my_munc():
            >>      sr = SkillRequest()
            >>      ...
            >>      return sr.serialize_json(), 200

        :return: dict
        """
        return {
            'User': {
                'user_id': self.user.user_id,
                'global_id': self.user.global_id,
                'client': self.user.client.__dict__
            },
            'Update': self.update.__dict__,
            'Context': self.context
        }
