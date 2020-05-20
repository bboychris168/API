from utils.response import Response


class Interact(object):
    def __init__(self, current_league, api_key):
        self.current_league = current_league
        self.values = {
            "key": api_key,
            "league_id": current_league.league_id,
        }

    async def validate(self):
        """ Validates if key exists. """

        query = """SELECT COUNT(*)
                   FROM api_keys
                   WHERE `key` = :key
                          AND league_id = :league_id"""

        count = await self.current_league.obj.database.fetch_val(
            query=query,
            values=self.values
        )

        return Response(data=count == 1)

    async def edit(self, access_level: int, active: bool = True):
        """ Edit API Key """

        validate_key = await self.validate()
        if not validate_key.data:
            return validate_key

        query = """UPDATE api_keys
                   SET access_level = :access_level,
                       active = :active
                   WHERE `key` = :key AND league_id = :league_id"""

        values = {
            **self.values,
            "access_level": access_level,
            "active": int(active),
        }

        await self.current_league.obj.database.execute(
            query=query,
            values=values
        )

        return Response(data=True)

    async def delete(self):
        """ Deletes API Key """

        query = """DELETE FROM api_keys
                   WHERE `key` = :key AND league_id = :league_id"""

        await self.current_league.obj.database.execute(
            query=query,
            values=self.values
        )

        return Response(data=True)

    async def paths(self):
        """ Gets all paths this key can access. """

        query = """SELECT api_paths.path FROM api_keys
                        INNER JOIN api_permissions
                            ON api_permissions.league_id = api_keys.league_id
                        INNER JOIN api_paths
                            ON api_paths.path_id = api_permissions.path_id
                   WHERE api_keys.key = :key
                         AND api_keys.league_id = :league_id
                         AND api_keys.access_level
                             >= api_permissions.access_level
                         AND api_keys.active = 1"""

        rows_formatted = []
        rows_formatted_append = rows_formatted.append
        async for row in self.current_league.obj.database.iterate(
                query=query, values=self.values):
            rows_formatted_append(row["path"])

        return Response(data=rows_formatted)
