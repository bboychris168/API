import sqlalchemy

# CURRENTLY ONLY DEVELOPED FOR MySQL!
# Current MySQL dependances
# sqlalchemy.dialects.mysql.VARBINARY


class Tables(object):
    metadata = sqlalchemy.MetaData()

    # API tables
    sqlalchemy.Table(
        "api_keys",
        metadata,
        sqlalchemy.Column(
            "user_id",
            sqlalchemy.String(length=36),
            sqlalchemy.ForeignKey("users.user_id")
        ),
        sqlalchemy.Column(
            "key",
            sqlalchemy.String(length=36),
            primary_key=True
        ),
        sqlalchemy.Column(
            "league_id",
            sqlalchemy.String(length=4),
            sqlalchemy.ForeignKey("league_info.league_id")
        ),
        sqlalchemy.Column(
            "access_level",
            sqlalchemy.Integer
        ),
        sqlalchemy.Column(
            "active",
            sqlalchemy.Boolean
        ),
    )

    sqlalchemy.Table(
        "api_paths",
        metadata,
        sqlalchemy.Column(
            "path_id",
            sqlalchemy.Integer,
            primary_key=True,
            autoincrement=True
        ),
        sqlalchemy.Column(
            "path",
            sqlalchemy.String(length=64)
        ),
    )

    sqlalchemy.Table(
        "api_permissions",
        metadata,
        sqlalchemy.Column(
            "league_id",
            sqlalchemy.String(length=4),
            sqlalchemy.ForeignKey("league_info.league_id")
        ),
        sqlalchemy.Column(
            "path_id",
            sqlalchemy.Integer,
            sqlalchemy.ForeignKey("api_paths.path_id")
        ),
        sqlalchemy.Column(
            "access_level",
            sqlalchemy.Integer
        ),
    )

    sqlalchemy.Table(
        "elo_settings",
        metadata,
        sqlalchemy.Column(
            "elo_id",
            sqlalchemy.Integer,
            primary_key=True,
            autoincrement=True
        ),
        sqlalchemy.Column(
            "kill",
            sqlalchemy.Float
        ),
        sqlalchemy.Column(
            "death",
            sqlalchemy.Float
        ),
        sqlalchemy.Column(
            "round_won",
            sqlalchemy.Float
        ),
        sqlalchemy.Column(
            "round_lost",
            sqlalchemy.Float
        ),
        sqlalchemy.Column(
            "match_won",
            sqlalchemy.Float
        ),
        sqlalchemy.Column(
            "match_lost",
            sqlalchemy.Float
        ),
        sqlalchemy.Column(
            "assist",
            sqlalchemy.Float
        ),
        sqlalchemy.Column(
            "mate_blined",
            sqlalchemy.Float
        ),
        sqlalchemy.Column(
            "mate_killed",
            sqlalchemy.Float
        ),
    )

    # Basic league info
    # knife_round
    # 0 - Disabled
    # 1 - Enabled

    # pause
    # If no time given in seconds its disabled.

    # warmup_commands_only
    # Commands can only be used during warmup.

    # captain_choice_time
    # Max amount of time for a captain choice.

    # surrender
    # If teams are allowed to surrender.
    sqlalchemy.Table(
        "league_info",
        metadata,
        sqlalchemy.Column(
            "league_id",
            sqlalchemy.String(length=4),
            primary_key=True
        ),
        sqlalchemy.Column(
            "league_name",
            sqlalchemy.String(length=32)
        ),
        sqlalchemy.Column(
            "league_website",
            sqlalchemy.String(length=255)
        ),
        sqlalchemy.Column(
            "websocket_endpoint",
            sqlalchemy.String(length=255)
        ),
        sqlalchemy.Column(
            "discord_webhook",
            sqlalchemy.String(length=255),
            nullable=True,
        ),
        sqlalchemy.Column(
            "queue_limit",
            sqlalchemy.Integer
        ),
        sqlalchemy.Column(
            "discord_prefix",
            sqlalchemy.String(length=3)
        ),
        sqlalchemy.Column(
            "sm_message_prefix",
            sqlalchemy.String(length=24)
        ),
        sqlalchemy.Column(
            "knife_round",
            sqlalchemy.Integer
        ),
        sqlalchemy.Column(
            "pause",
            sqlalchemy.Integer
        ),
        sqlalchemy.Column(
            "surrender",
            sqlalchemy.Integer
        ),
        sqlalchemy.Column(
            "warmup_commands_only",
            sqlalchemy.Integer
        ),
        sqlalchemy.Column(
            "captain_choice_time",
            sqlalchemy.Integer
        ),
        sqlalchemy.Column(
            "elo_id",
            sqlalchemy.Integer,
            sqlalchemy.ForeignKey("elo_settings.elo_id")
        ),
    )

    # League Discords
    sqlalchemy.Table(
        "league_discords",
        metadata,
        sqlalchemy.Column(
            "guild_id",
            sqlalchemy.BigInteger,
            primary_key=True
        ),
        sqlalchemy.Column(
            "league_id",
            sqlalchemy.String(length=4),
            sqlalchemy.ForeignKey("league_info.league_id")
        ),
    )

    # Queue Channels
    # queue_type
    # 0 - bot interface
    # 1 - website interface
    sqlalchemy.Table(
        "league_queues",
        metadata,
        sqlalchemy.Column(
            "channel_id",
            sqlalchemy.BigInteger,
            primary_key=True
        ),
        sqlalchemy.Column(
            "guild_id",
            sqlalchemy.BigInteger,
            sqlalchemy.ForeignKey("league_discords.guild_id")
        ),
        sqlalchemy.Column(
            "queue_size",
            sqlalchemy.Integer
        ),
        sqlalchemy.Column(
            "queue_type",
            sqlalchemy.Integer
        ),
    )

    # Admins & Owners
    # Access Levels
    # 0 = Owner
    # 1 = Admin
    # 2 = Moderator
    # 3 = Anti cheat reviewer
    # 4 = Demo reviewer
    # 5 = Sepecator
    sqlalchemy.Table(
        "league_admins",
        metadata,
        sqlalchemy.Column(
            "league_id",
            sqlalchemy.String(length=4),
            sqlalchemy.ForeignKey("league_info.league_id")
        ),
        sqlalchemy.Column(
            "user_id",
            sqlalchemy.String(length=36),
            sqlalchemy.ForeignKey("users.user_id")
        ),
        sqlalchemy.Column(
            "access_level",
            sqlalchemy.Integer
        ),
    )

    # User account details
    # Region here is the users most recent region.
    sqlalchemy.Table(
        "users",
        metadata,
        sqlalchemy.Column(
            "user_id",
            sqlalchemy.String(length=36),
            primary_key=True
        ),
        sqlalchemy.Column(
            "steam_id",
            sqlalchemy.String(length=64),
            primary_key=True,
            nullable=True
        ),
        sqlalchemy.Column(
            "discord_id",
            sqlalchemy.BigInteger,
            primary_key=True,
            nullable=True
        ),
        sqlalchemy.Column(
            "region",
            sqlalchemy.String(length=4),
            sqlalchemy.ForeignKey("region.region")
        ),
        sqlalchemy.Column(
            "name",
            sqlalchemy.String(length=36)
        ),
        sqlalchemy.Column(
            "pfp",
            sqlalchemy.String(length=128)
        ),
        sqlalchemy.Column(
            "joined",
            sqlalchemy.types.TIMESTAMP,
            server_default=sqlalchemy.text("CURRENT_TIMESTAMP()")
        ),
        sqlalchemy.Column(
            "ip_id",
            sqlalchemy.String(length=36),
            sqlalchemy.ForeignKey("ip_details.ip_id")
        ),
    )

    # Region table
    sqlalchemy.Table(
        "region",
        metadata,
        sqlalchemy.Column(
            "region",
            sqlalchemy.String(length=4),
            primary_key=True
        ),
    )

    # IP details / Proxy caching
    sqlalchemy.Table(
        "ip_details",
        metadata,
        sqlalchemy.Column(
            "ip_id",
            sqlalchemy.String(length=36),
            primary_key=True
        ),
        sqlalchemy.Column(
            "ip",
            sqlalchemy.VARBINARY(length=16)
        ),
        sqlalchemy.Column(
            "region",
            sqlalchemy.String(length=4),
            sqlalchemy.ForeignKey("region.region")
        ),
        sqlalchemy.Column(
            "proxy",
            sqlalchemy.Boolean
        ),
        sqlalchemy.Column(
            "provider",
            sqlalchemy.String(length=124)
        ),
        sqlalchemy.Column(
            "city",
            sqlalchemy.String(length=64)
        ),
        sqlalchemy.Column(
            "country",
            sqlalchemy.String(length=64)
        ),
    )

    # Scoreboard
    # Status codes
    # 0 - Finished
    # 1 - Live
    # 2 - Map selection
    # 3 - Player selection
    sqlalchemy.Table(
        "scoreboard_total",
        metadata,
        sqlalchemy.Column(
            "match_id",
            sqlalchemy.String(length=36),
            primary_key=True
        ),
        sqlalchemy.Column(
            "server_id",
            sqlalchemy.String(length=36)
        ),
        sqlalchemy.Column(
            "map_order",
            sqlalchemy.String(length=20),
            nullable=True
        ),
        sqlalchemy.Column(
            "player_order",
            sqlalchemy.String(length=20),
            nullable=True
        ),
        sqlalchemy.Column(
            "timestamp",
            sqlalchemy.types.TIMESTAMP,
            server_default=sqlalchemy.text("CURRENT_TIMESTAMP()")
        ),
        sqlalchemy.Column(
            "status",
            sqlalchemy.Integer
        ),
        sqlalchemy.Column(
            "map",
            sqlalchemy.String(length=24), server_default="NULL"
        ),
        sqlalchemy.Column(
            "region",
            sqlalchemy.String(length=4),
            sqlalchemy.ForeignKey("region.region")
        ),
        sqlalchemy.Column(
            "league_id",
            sqlalchemy.String(length=4),
            sqlalchemy.ForeignKey("league_info.league_id")
        ),
        sqlalchemy.Column(
            "team_1_name",
            sqlalchemy.String(length=64)
        ),
        sqlalchemy.Column(
            "team_2_name",
            sqlalchemy.String(length=64)
        ),
        sqlalchemy.Column(
            "team_1_score",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "team_2_score",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "team_1_side",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "team_2_side",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "record_statistics",
            sqlalchemy.Boolean,
            server_default="1"
        ),
    )

    # Team Codes
    # 0 Teamless
    # 1 = CT
    # 2 = T
    sqlalchemy.Table(
        "scoreboard",
        metadata,
        sqlalchemy.Column(
            "match_id",
            sqlalchemy.String(length=36),
            sqlalchemy.ForeignKey("scoreboard_total.match_id")
        ),
        sqlalchemy.Column(
            "user_id",
            sqlalchemy.String(length=36),
            sqlalchemy.ForeignKey("users.user_id")
        ),
        sqlalchemy.Column(
            "captain",
            sqlalchemy.Integer
        ),
        sqlalchemy.Column(
            "team",
            sqlalchemy.Integer
        ),
        sqlalchemy.Column(
            "alive",
            sqlalchemy.Integer,
            server_default="1"
        ),
        sqlalchemy.Column(
            "ping",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "kills",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "headshots",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "assists",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "deaths",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "shots_fired",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "shots_hit",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "mvps",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "score",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "disconnected",
            sqlalchemy.Boolean,
            server_default="0"
        ),
    )

    # Match Map Pool
    # Data is delete from here once match has ended.
    sqlalchemy.Table(
        "map_pool",
        metadata,
        sqlalchemy.Column(
            "match_id",
            sqlalchemy.String(length=36),
            sqlalchemy.ForeignKey("scoreboard_total.match_id")
        ),
        sqlalchemy.Column(
            "map",
            sqlalchemy.String(length=24)
        ),
    )

    # Statistics
    # user_id isn't unique here,
    # different regions have different stats.
    sqlalchemy.Table(
        "statistics",
        metadata,
        sqlalchemy.Column(
            "user_id",
            sqlalchemy.String(length=36),
            sqlalchemy.ForeignKey("users.user_id")
        ),
        sqlalchemy.Column(
            "league_id",
            sqlalchemy.String(length=4),
            sqlalchemy.ForeignKey("league_info.league_id")
        ),
        sqlalchemy.Column(
            "region",
            sqlalchemy.String(length=4), sqlalchemy.ForeignKey("region.region")
        ),
        sqlalchemy.Column(
            "last_connected",
            sqlalchemy.types.TIMESTAMP,
            server_default=sqlalchemy.text("""CURRENT_TIMESTAMP()
                                              ON UPDATE CURRENT_TIMESTAMP()""")
        ),
        sqlalchemy.Column(
            "total_time",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "elo",
            sqlalchemy.Float,
            server_default="0"
        ),
        sqlalchemy.Column(
            "kills",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "deaths",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "assists",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "shots",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "hits",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "damage",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "headshots",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "roundswon",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "roundslost",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "wins",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "ties",
            sqlalchemy.Integer,
            server_default="0"
        ),
        sqlalchemy.Column(
            "losses",
            sqlalchemy.Integer,
            server_default="0"
        ),
    )

    def __init__(self, obj):
        """ Ensures all the tables have been built correctly. """

        engine = sqlalchemy.create_engine(
            str(
                obj.database_url.replace(driver="pymysql")
            ) + "?charset=utf8mb4"
        )

        self.metadata.create_all(engine)
