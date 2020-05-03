# Documentation
- [Modules](#modules)
- [Routes](#routes)

## Modules 
#### modulelift.client
- validate_user(self, user_id)

#### modulelift.client.league(self, league_id, region)
- get_server(self)
- queue_allowed(self)
- details(self)
- update(self, args: dict)

##### match(self, match_id=None)

---

```python
create(self, players: dict, maps: dict, team_names: dict)
```

**Parameters**
```json
    - players
        {
            "options": {
                "type": "random"
                        / "elo"
                        / "given",
                "param": None
                        / ASC OR DESC
                        / {"capt_1": index, "capt_2": index}
                "selection": "ABBAABBA"
                                / "ABBABABA"
                                / "ABABABAB"
                                / None,
                "assiged_teams": True / False,
                "record_statistics": True / False,
            },
            "list": {
                "user_id": None / 1 / 2
            },
        }
    - maps
        {
            "options": {
                "type": "veto" / "random" / "vote" / "given",
                "selection": "ABBAABBA"
                                / "ABBABABA"
                                / "ABABABAB"
                                / None,
            },
            "list": [list of full map names],
        }
    - team_names
        {
            "team_1": "Max 13 characters",
            "team_2": "",
        }
```
**Response**

[Full scoreboard model](https://github.com/ModuleLIFT/API/blob/master/models/scoreboard.py#L15) inside the [response object](https://github.com/ModuleLIFT/API/blob/master/utils/response.py).

---

- get(self)
- clone(self)
- scoreboard(self)
- end(self)
- players(self) - being developed
- select_player(self, user_id: str) - being developed
- select_map(self, map_id: str) - being developed

##### list(self, limit: int, offset: int, desc: bool, search: str = "")
- matches(self)
- players(self)

##### player(self, user_id)
- get(self)
- reset(self)
- delete(self)

##### players(self, user_ids)
- fetch(self, include_stats=False)
- validate(self)

##### api_key(self)
- paths(self)
- generate(self, user_id, access_level: int, active: bool = True)
- interact(self, api_key)
    - validate(self)
    - edit(self, access_level: int, active: bool = True)
    - delete(self)
    - paths(self)

## Routes
Coming soon