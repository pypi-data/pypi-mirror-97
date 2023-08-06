from mitama.app import Controller
from mitama.app.http import Response
from mitama.models import User, Node, Role, is_admin
from datetime import datetime
import json
import re
import markdown
import magic

from .model import db, Board, Thread, Res, Permission
from .forms import CreateBoardForm, CreateThreadForm, SettingForm
from .utils import hiroyuki

class HomeController(Controller):
    def handle(self, request):
        template = self.view.get_template("home.html")
        threads = list()
        for board in Board.list_subscribed(request.user):
            for thread in board.threads:
                if not thread.closed:
                    threads.append(thread)
        return Response.render(template, {
            "is_admin": is_admin,
            "threads": threads,
            "boards": Board.list_subscribed(request.user)
        })
    def settings(self, request):
        template = self.view.get_template("settings.html")
        error = ""
        if request.method == "POST":
            form = SettingForm(request.post())
            for permission_screen_name, permission_roles in form['permissions'].items():
                permission = Permission.retrieve(screen_name = permission_screen_name)
                permission.roles = [Role.retrieve(screen_name = r) for r in permission_roles]
            permission.update()
            error = "保存しました"
        return Response.render(template, {
            "permissions": Permission.list(),
            "roles": Role.list(),
            "error": error
        })

class BoardController(Controller):
    def create(self, request):
        form = CreateBoardForm(request.post())
        board = Board()
        board.name = form['name']
        board.owner = Node.retrieve(form['owner'])
        board.create()
        return Response.json({
            "_id": board._id,
        })

    def retrieve(self, request):
        template = self.view.get_template("board.html")
        board = Board.retrieve(request.params['board'])
        return Response.render(template, {
            "board": board,
            "boards": Board.list_subscribed(request.user)
        })

    def subscribe(self, request):
        board = Board.retrieve(request.params['board'])
        board.subscribers.append(request.user)
        board.update()
        return Response.json({
            "subscribe": True,
            "board": {
                "_id": board._id
            }
        })

    def unsubscribe(self, request):
        board = Board.retrieve(request.params['board'])
        board.subscribers.remove(request.user)
        board.update()
        return Response.json({
            "subscribe": False,
            "board": {
                "_id": board._id
            }
        })

class UserController(Controller):
    def icon(self, request):
        user = User.retrieve(request.params['user'])
        f = magic.Magic(mime=True, uncompress=True)
        mime = f.from_buffer(self.icon)
        return Response(user._icon, content_type=mime)

class ThreadController(Controller):
    def create(self, request):
        form = CreateThreadForm(request.post())
        board = Board.retrieve(request.params['board'])
        thread = Thread()
        thread.title = form['title']
        thread.board = board
        thread.user = request.user
        thread.create()
        for user in board.subscribers:
            user.push({
                "title": res.thread.title + " - Kyokusui",
                "body": "スレッドが立ちました",
                "icon": self.app.convert_fullurl(request, "/user/{}/icon".format(requst.user._id))
            })
        return Response.json({
            "_id": thread._id,
        })

    def retrieve(self, request):
        template = self.view.get_template("thread.html")
        board = Board.retrieve(request.params['board'])
        thread = Thread.retrieve(request.params['thread'])
        return Response.render(template, {
            "board": board,
            "thread": thread,
            "boards": Board.list_subscribed(request.user)
        })

class WebSocketController(Controller):
    streams = {}
    def handle(self, request):
        ws = request.websocket
        board = Board.retrieve(request.params['board'])
        thread = Thread.retrieve(request.params['thread'])
        if board._id not in self.streams:
            self.streams[board._id] = dict()
        if thread._id not in self.streams[board._id]:
            self.streams[board._id][thread._id] = list()
        self.streams[board._id][thread._id].append(ws)
        db.manager.close_session()
        while True:
            received = ws.receive()
            if received is None:
                continue
            try:
                db.manager.start_session()
                data = json.loads(received)
                if data['type'] == "message":
                    res = Res()
                    res.data = json.dumps(data['data'])
                    res.user = request.user
                    res.thread = Thread.retrieve(request.params['thread'])
                    res.create()
                    mentions = re.findall(r"\>\>([0-9a-zA-Z.-_]+)", data['data']['message'])
                    for mention in mentions:
                        try:
                            user = User.retrieve(screen_name = mention)
                            user.push({
                                "title": res.thread.title + " - Kyokusui",
                                "body": res.user.name+"さんがメンションしました",
                                "icon": self.app.convert_fullurl(request, "/user/{}/icon".format(res.user._id))
                            })
                        except Exception as err:
                            print(err, mention)
                            pass
                    remove = list()
                    for s in self.streams[board._id][thread._id]:
                        try:
                            s.send(json.dumps({
                                "type": "message",
                                "_id": res._id,
                                "data": {
                                    "message": markdown.markdown(hiroyuki(res.parsed_data["message"]), extensions=['fenced_code']),
                                    "images": res.parsed_data["images"]
                                },
                                "user": {
                                    "_id": res.user._id,
                                    "name": res.user.name,
                                    "screen_name": res.user.screen_name
                                },
                                "datetime": res.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                                "thread": thread._id,
                            }))
                        except Exception as err:
                            print(err)
                            remove.append(s)
                    for s in remove:
                        self.streams[board._id][thread._id].remove(s)
                elif data['type'] == "close":
                    thread = Thread.retrieve(request.params['thread'])
                    thread.close()
                    remove = list()
                    for s in self.streams[board._id][thread._id]:
                        try:
                            s.send(json.dumps({
                                "type": "close"
                            }))
                        except Exception as err:
                            print(err)
                            pass
                    del self.streams[board._id][thread._id]
            except Exception as err:
                print(err)
                db.manager.rollback_session()
            finally:
                db.manager.close_session()
        return Response()
