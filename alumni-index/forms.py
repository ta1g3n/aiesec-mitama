from mitama.app.forms import Form, Field, FileField, DictField


class ProfileForm(Form):
    name = Field(label='名前', required=True)
    ruby = Field(label='ふりがな', required=True)
    epoch = Field(label='入会年度', required=True)
    birthday = Field(label="生年月日", required=True)
    image = FileField(label='写真', required=True)
    extra = DictField()
    email = Field(label="メールアドレス", required=True)
    careers = DictField(label="キャリア")
    contactOption = Field(label="その他の連絡手段", required=True)
    contactIdent = Field(label="連絡手段の内容", required=True)


class ExtraColumnForm(Form):
    name = Field(label="カラム名", required=True)
