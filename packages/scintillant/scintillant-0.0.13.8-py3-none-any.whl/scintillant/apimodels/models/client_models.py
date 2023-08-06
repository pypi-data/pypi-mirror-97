"""
:mod: `client_models`
=====================

Description of models of client
applications interacting with requests.

.. module:: client_models
.. module_author:: Niel (Ketov) Gorev <ketov-x@ya.ru>
.. module_author:: http://t.me/ketov-x
"""
from dataclasses import dataclass, field
from http import HTTPStatus

from scintillant.apimodels.types import SkillResponseType, ClientResponseType


@dataclass
class ClientResponse(ClientResponseType):
    """Response model for the client application (Telegram, VK and others).

    .. note:: The skill does not return a response to the client,
    it is the task of the Dialog service.
    Inside the skill, we use SkillModels to receive requests from the Dialog
    and return the correct responses.

    Relationship diagram
    ---------------------
    Client (DialogAnswerRequest) -> Dialogs \n
    Dialogs (SkillRequest) -> Skill (SkillResponse) -> Dialogs \n
    Dialogs (**ClientResponse**) -> Client \n

    **parameters**, **types**
    -------------------------
    **types**::

    :type out_text: str.
    :type status_code: HTTPStatus.
    :type choices: list or None.
    :type client_app_action: str or None.
    :type requested_field_code: str or None.

    **parameters**::

    :param out_text: The text that the client will receive to respond to the
    user. May be HTML text.
    :param status_code: Internal status of the response to the client. [1]_
    :param choices: A set of lists displayed to the client in the form of
    buttons or lists. [2]_
    :param client_app_action: An action that can be performed by any client,
    if the interface allows it. [3]_
    :param requested_field_code: The name of the validator. [4]_

    **footprints**
    --------------

    [1] The specification of all statuses is currently under development,
    but here are a couple of values that clients are considering:
        - 200, Successful query execution;
        - 205, Resetting content, returning the bot to its original state;
        - 404, The class is not recognized or the skill responsible
        for the class is currently disabled;
        - 500, Internal error of the skill or Dialog.
    [2] The first item in the list is the visible value,
    the second is the returned payload.
    For instance: [["Choose the first", 1], ["Choose the second", 2]]
    [3] For example, delete the next message from a user (tek clients)
    or request a phone number (Exclusively telegrams).
    The list of actions available on clients is now expanding,
    but here are a couple of examples:
        - REQUEST_PHONE_NUMBER;
        - REMOVE_PREVIOUS_USER_MESSAGE.
    [4] This field is used at your own risk.
    it is supported by a very limited number of clients. For instance:
        - PHONE_NUMBER;
        - VEHICLE_NUMBER;
    """
    out_text: str = field()
    status_code: HTTPStatus or int = field(default=HTTPStatus.OK)
    choices: list or None = None
    client_app_action: str or None = None
    requested_field_code: str or None = None

    @classmethod
    def from_dict(cls, data: dict) -> ClientResponseType:
        """Generate ClientResponse from dict data.

        .. Example 1:: TODO
            >> import requests
            >> cr = ClientResponse._from_dict(requests.get(skill-url).json)
            >> print(cr)

        .. Example 2:: TODO
            >> cr = ClientResponse._from_dict({'out_text': ...})
            >> print(cr)

        :type data: dict

        :param data: Model Generation Data.
        :return: ClientResponse
        """
        return cls(
            out_text=data.get('out_text'),
            status_code=data.get('status_code', [500]),
            choices=data.get('choices'),
            client_app_action=data.get('client_app_action'),
            requested_field_code=data.get('requested_field_code')
        )

    @classmethod
    def from_skill_response(cls, response: SkillResponseType):
        """Generate ClientResponse from SkillResponse.

        Fastest way to get ClientResponse.
        For testing, you can use it right inside a skill,
        generating a skill response and matching against the
        ClientResponse class.

        .. note:: It is assumed that the method will be used after receiving
        a response from the skill to automatically generate
        a template response for the client.

        .. Example::
            >> import requests
            >> sr = SkillResponse._from_dict(requests.post(skill-url))
            >> cr = ClientResponse.from_skill_response(sr)

        :type response: SkillResponse

        :param response: HTTP response from the skill service.
        :return: ClientResponse
        """
        return cls.from_dict(response.serialize_json())

    def serialize_json(self) -> dict:
        """Returns a templated dictionary based on the fields of the class.

        This function is designed to send a class as JSON within HTTP requests
        or to respond to similar requests.

        .. Example aiohttp::
            >> @app.get('/')
            >> async def my_munc(request: Request):
            >>      cr = ClientResponse()
            >>      ...
            >>      return web.json_response(cr.serialize_json(), status=200)

        .. Example flask::
            >> @app.route('/', methods=['GET'])
            >> def my_munc():
            >>      cr = ClientResponse()
            >>      ...
            >>      return cr.serialize_json(), 200

        :return: dict
        """
        return {
            'out_text': self.out_text,
            'status_code': self.status_code,
            'choices': self.choices,
            'client_app_action': self.client_app_action,
            'requested_field_code': self.requested_field_code
        }
