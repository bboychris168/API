from starlette.endpoints import HTTPEndpoint

from webargs import fields
from webargs_starlette import use_args

from utils.responder import responder


class User(HTTPEndpoint):
    @use_args({"steam_id": fields.String(required=True),
               "ip": fields.String(max=39),
               "name": fields.String(max=36),
               "discord_id": fields.Integer(),
               "pfp": fields.Url()})
    async def post(self, request, args):
        """ Get user. """

        return responder.render(
            await self.obj.user().create(**args)
        )
