import json

from matrix_client.client import MatrixClient
from vibora import Request, Route, Vibora

from knopfler.modules.alertmanager import alertmanager


class MatrixLink:
    client: MatrixClient
    server: str
    user_id: str
    token: str
    rooms: dict

    def __init__(self, vibora: Vibora):
        self.vibora = vibora
        try:
            config = json.load(open('knopfler.hcl'))
            self.server = config['server']
            self.user_id = config['user']
            self.token = config['token']
        except FileNotFoundError:
            # self._setup()
            return
        self.client = MatrixClient(self.server, user_id=self.user_id, token=self.token)
        self.rooms = {}
        if config.get('alerting'):
            self.alerting(config['alerting'])

    def alerting(self, conf):
        async def newroute(request: Request):
            return await alertmanager(request, self)

        self.rooms['alert_room'] = self.client.join_room(conf['room'])
        pattern = f"/hooks{conf['hook']}"
        new_route = Route(pattern.encode(), newroute, (b'GET', b'POST'))
        self.vibora.add_route(new_route)
        print(f'added route {pattern}')
