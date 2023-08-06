from mitama.app.forms import Form, Field, DictField


class CreateBoardForm(Form):
    name = Field(label="タイトル", required=True)
    owner = Field(label="板主", required=True)

class CreateThreadForm(Form):
    title = Field(label="タイトル", required=True)

class SettingForm(Form):
    permissions = DictField(label="権限", listed=True)

class UpdateThreadForm(Form):
    title = Field(label="タイトル", required=True)

class UpdateBoardForm(Form):
    name = Field(label="タイトル", required=True)
