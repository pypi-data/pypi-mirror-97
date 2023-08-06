from mitama.app import App, Router
from mitama.utils.controllers import static_files
from mitama.utils.middlewares import SessionMiddleware
from mitama.app.method import view, post, put

from .controller import HomeController, BoardController, ThreadController, WebSocketController, UserController
from .model import Board, Thread, Res, Permission
from .utils import hiroyuki

class App(App):
    name = 'Kyokusui'
    description = '業務用便所の落書き'
    router = Router(
        [
            view("/", HomeController),
            view("/settings", HomeController, 'settings'),
            view("/static/<path:path>", static_files()),
            view("/<board>", BoardController, 'retrieve'),
            view("/<board>/<thread>", ThreadController, 'retrieve'),
            view("/user/<user>/icon", UserController, 'icon'),
            post("/api/v0/board", BoardController, 'create'),
            put("/api/v0/board/<board>", BoardController, 'update'),
            post("/api/v0/board/<board>", ThreadController, 'create'),
            post("/api/v0/board/<board>/subscribe", BoardController, 'subscribe'),
            post("/api/v0/board/<board>/unsubscribe", BoardController, 'unsubscribe'),
            put("/api/v0/board/<board>/<thread>", ThreadController, 'update'),
            view("/api/v0/board/<board>/<thread>/socket", WebSocketController),
        ],
        middlewares=[SessionMiddleware]
    )
    models = [Board, Thread, Res, Permission]

    @property
    def view(self):
        view = super().view
        view.globals['permission'] = Permission.is_accepted
        view.filters['hiroyuki'] = hiroyuki
        return view
