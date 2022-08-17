import requests

requests.post("http://localhost:8000/orm/model/orjson/", json={"login": "zsu8"})
requests.post("http://localhost:8000/orm/model/default/", json={"login": "zsu8"})
requests.post(
    "http://localhost:8000/orm/values/response/",
    json={
        "login": "zsu8",
        "start": "2021-07-01T00:00:0.0Z",
        "end": "2021-08-01T00:00:0.0Z",
    },
)
