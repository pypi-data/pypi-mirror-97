from mitama.db import BaseDatabase, Table, relationship
from mitama.db.model import UUID
from mitama.db.types import *
from mitama.models import User, Group, Node, permission
from datetime import datetime
import json


class Database(BaseDatabase):
    pass


db = Database(prefix="kyokusui")

class Board(db.Model):
    name = Column(String(255))
    owner_id = Column(String(64), ForeignKey("mitama_node._id"))
    owner = relationship(Node)
    created = Column(DateTime, default=datetime.now)
    subscribers = relationship(User, secondary="kyokusui_subscribe")

    @classmethod
    def list_subscribed(cls, user):
        boards_ = cls.list()
        boards = list()
        for board in boards_:
            if board.owner.object == user or (isinstance(board.owner.object, Group) and board.owner.object.is_in(user)) or user in board.subscribers:
                boards.append(board)
        return boards

class Thread(db.Model):
    board_id = Column(String(64), ForeignKey("kyokusui_board._id"))
    board = relationship(Board, backref="threads")
    user_id = Column(String(64), ForeignKey("mitama_user._id"))
    user = relationship(User)
    created = Column(DateTime, default=datetime.now)
    title = Column(String(1024))
    closed = Column(Boolean, default=False)

    def close(self):
        self.closed = True
        self.update()

class Res(db.Model):
    thread_id = Column(String(64), ForeignKey("kyokusui_thread._id"))
    thread = relationship(Thread, backref="res")
    user_id = Column(String(64), ForeignKey("mitama_user._id"))
    user = relationship(User)
    datetime = Column(DateTime, default=datetime.now)
    data = Column(Text)

    @property
    def parsed_data(self):
        return json.loads(self.data)

subscribe_table = Table("kyokusui_subscribe",
    db.metadata,
    Column("_id", String(64), default=UUID(), primary_key=True),
    Column("user_id", String(64), ForeignKey("mitama_user._id", ondelete="CASCADE")),
    Column("board_id", String(64), ForeignKey("kyokusui_board._id", ondelete="CASCADE"))
)

class Subscribe(db.Model):
    __table__ = subscribe_table
    user_id = subscribe_table.c.user_id,
    board_id = subscribe_table.c.board_id,
    user = relationship(User)
    board = relationship(Board)

Permission = permission(db, [
    {
        "name": "板を立てる",
        "screen_name": "create_board"
    },
    {
        "name": "板を閉じる",
        "screen_name": "delete_board"
    }
])

db.create_all()
