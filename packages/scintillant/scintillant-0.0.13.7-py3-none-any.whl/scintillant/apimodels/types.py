from http import HTTPStatus


class SkillResponseType:
    status: str
    out_text: str or None
    choices: list or None
    attach: None
    client_app_action: str or None
    request_field_code: str or None
    context: dict or None
    redirect_to: str or None

    @classmethod
    async def from_json_response(cls, response: dict): ...

    @classmethod
    async def from_response(cls, response): ...

    def serialize_json(self) -> dict: ...


class SkillRequestType:
    class User:

        class Client:
            name: str
            type: str
            _meta_: dict

        user_id: str
        client: Client
        global_id: str

    class Update:
        in_text: str
        in_choice: str
        datetime: int

    user: User
    update: Update
    context: dict

    def serialize_json(self) -> dict: ...

    @classmethod
    async def from_dict(cls, request): ...


class ClientResponseType:
    out_text: str
    status_code: HTTPStatus or int
    choices: list or None
    client_app_action: str or None
    requested_field_code: str or None

    @classmethod
    def from_dict(cls, data: dict): ...

    @classmethod
    def from_skill_response(cls, response: SkillResponseType): ...

    def serialize_json(self) -> dict: ...


class DialogAnswerRequestType:
    client_id: str
    client_app: str
    client_type: str
    in_text: str or None
    in_choice: str or None

    @classmethod
    async def from_dict(cls, request): ...

    def serialize_json(self) -> dict: ...
