from settings import CONFIG


class PlayerModel:
    def __init__(self, data: dict):
        self.data = data

    @property
    def full(self):
        """ Formats and returns full player. """

        return {
            **self.minimal,
            "statistics": self.statistics,
            "ranking": self.ranking,
        }

    @property
    def statistics(self):
        """ Formats and returns statistics. """

        return {
                "kills": self.data["kills"],
                "deaths": self.data["deaths"],
                "assists": self.data["assists"],
                "shots": self.data["shots"],
                "hits": self.data["hits"],
                "damage": self.data["damage"],
                "headshots": self.data["headshots"],
                "rounds_won": self.data["rounds_won"],
                "rounds_lost": self.data["rounds_lost"],
                "wins": self.data["wins"],
                "ties": self.data["ties"],
                "loses": self.data["loses"],
        }

    @property
    def ranking(self):
        """ Formats and returns rankings. """

        return {
                    "elo": self.data["elo"],
        }

    @property
    def minimal(self):
        """ Formats and returns minimal player. """

        return {
                "name": self.data["name"],
                "user_id": self.data["user_id"],
                "steam_id": self.data["steam_id"],
                "discord_id": self.data["discord_id"],
                "pfp": "{}{}.{}".format(
                    CONFIG.cdn["link"],
                    CONFIG.cdn["paths"]["pfps"].format(self.data["user_id"]),
                    self.data["file_type"]),
                "joined": self.data["joined"].strftime(CONFIG.timestamp),
        }
