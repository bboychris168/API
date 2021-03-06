from utils.response import Response

from .match import Match
from .player import Player
from .players import Players
from .list_info import List
from .api_key import ApiKey

from settings import CONFIG

from memory_cache import IN_MEMORY_CACHE

from sessions import SESSIONS


class League:
    def __init__(self, league_id, region=None):
        self.league_id = league_id
        self.region = region

    @property
    def api_key(self):
        """ Object used for interacting
            with api keys.
        """

        return ApiKey(current_league=self)

    def match(self, match_id=None):
        """ Match Object.
            If no match_id passed random UUID4 will be generated and used
            for create function.
        """

        return Match(current_league=self, match_id=match_id)

    def list(self, limit: int, offset: int, desc: bool, search: str = ""):
        """ List Object.
                - limit.
                - offset.
                - desc.
                - search.
        """

        return List(current_league=self, limit=limit, offset=offset,
                    search=search, desc=desc)

    def player(self, user_id):
        """ Player Object. """

        return Player(current_league=self, user_id=user_id)

    def players(self, user_ids):
        """ Players Object. """

        return Players(current_league=self, user_ids=user_ids)

    async def get_server(self):
        """ Finds a available server for the current league.
            https://github.com/ModuleLIFT/API/blob/master/docs/modules.md#get_serverself
        """

        if not CONFIG.server["regions"].get(self.region):
            print(self.region)
            print(CONFIG.server["regions"])
            return Response(error="No server IDs for that region")

        region_servers = list(
            CONFIG.server["regions"][self.region]
        )
        region_servers_remove = region_servers.remove

        query = """SELECT server_id
                   FROM scoreboard_total
                   WHERE server_id IN :server_ids AND status != 0"""
        values = {"server_ids": region_servers}

        # Removing any server ID being used in an active match.
        async for row in SESSIONS.database.iterate(query=query, values=values):
            region_servers_remove(row["server_id"])

        # Removing any server IDs from our temp blacklist.
        for server_id in IN_MEMORY_CACHE.temp_server_blacklist:
            if server_id in region_servers:
                region_servers_remove(server_id)

        if len(region_servers) > 0:
            return Response(data=region_servers[0])
        else:
            return Response(error="No available servers")

    async def queue_allowed(self):
        """ Checks if over the active queue limit.
            https://github.com/ModuleLIFT/API/blob/master/docs/modules.md#queue_allowedself
        """

        query = """SELECT COUNT(score.status) AS active_queues,
                          IFNULL(info.queue_limit, 0) AS queue_limit
                   FROM league_info AS info
                    LEFT JOIN scoreboard_total AS score
                        ON score.league_id = info.league_id
                           AND score.status != 0
                   WHERE info.league_id = :league_id"""
        row = await SESSIONS.database.fetch_one(
            query=query,
            values={"league_id": self.league_id, }
        )

        if row:
            # Ensures users can't create another
            # queue when another queue is being created
            # what would put them over the queue limit.
            if IN_MEMORY_CACHE.started_queues.get(self.league_id):
                active_queues = row["active_queues"] \
                     + IN_MEMORY_CACHE.started_queues[self.league_id]
            else:
                active_queues = row["active_queues"]

            return Response(data=row["queue_limit"] > active_queues)
        else:
            return Response(error=True)

    async def details(self):
        """ Gets basic details of league.
            https://github.com/ModuleLIFT/API/blob/master/docs/modules.md#detailsself
        """

        row = await SESSIONS.database.fetch_one(
            query="""SELECT league_name, league_website, discord_webhook,
                            websocket_endpoint, queue_limit,
                            league_id, discord_prefix,
                            sm_message_prefix, knife_round,
                            pause, surrender,
                            warmup_commands_only, captain_choice_time
                     FROM league_info WHERE league_id = :league_id""",
            values={"league_id": self.league_id, })

        if row:
            formatted_row = {**row}

            if formatted_row["pause"] == 0:
                formatted_row["pause"] = False

            formatted_row["surrender"] = formatted_row["surrender"] == 1
            formatted_row["warmup_commands_only"] = \
                formatted_row["warmup_commands_only"] == 1
            formatted_row["knife_round"] = formatted_row["knife_round"] == 1

            return Response(data=formatted_row)

        return Response(error="No such league")

    async def update(self, args: dict):
        """ Updates details of league.
            https://github.com/ModuleLIFT/API/blob/master/docs/modules.md#updateself-args-dict
        """

        if len(args) > 0:
            query = "UPDATE league_info SET "
            values = {"league_id": self.league_id}

            for key, item in args.items():
                if type(item) == bool:
                    if item:
                        item = 1
                    else:
                        item = 0

                values[key] = item

                # Don't worry this isn't
                # injecting any values.
                query += "{}={},".format(key, ":"+key)

            query = query[:-1]
            query += " WHERE league_id = :league_id"

            await SESSIONS.database.execute(query=query, values=values)

            return Response(data=args)

        return Response(error="No arguments")
