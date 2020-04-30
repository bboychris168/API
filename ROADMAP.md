# API Roadmap
- Improving modules documentation.
    - Explaining what what each function does.
- Routes documentation.
    - Explaining how each route operates, what data can be pushed, etc.
- Testing payloads for match.create.
- match.select_player & select_map.
    - Methods of selecting players & maps depending on the options provided in match.create.
- Setup script.
    - Script to automate production deploying.
- Login module.
    - Attaching discord & steam accounts to a user id.
    - Deleting & editing logins.
    - Alt detection & VPN blocking using [proxycheck.io](https://proxycheck.io/)
    - Logging events using Websocket.
- Ban module.
    - Adding a ban to a user id, ban length is based off the ban severity value and the rep loss value assigned to the ban type.
    - Removing bans.
    - Logging events using Websocket.
- Demo saving.
    - Using [ftp module](https://github.com/aio-libs/aioftp) to download demo files and uploading them to [b2](https://github.com/WardPearce/aiob2) or [s3](https://github.com/aio-libs/aiobotocore).
- Wrapper for API.
    - Currently async python planned.
- Graphql.
    - Adding a [graphql](https://www.starlette.io/graphql/) endpoint with alternatives to the REST endpoints.
- API Control Panel.
- Example website interface.
- Example discord bot.