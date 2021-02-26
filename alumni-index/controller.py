from mitama.app import Controller
from mitama.app.http import Response
from mitama.app.forms import ValidationError
from datetime import datetime

from .model import Profile, ExtraColumn, ExtraColumnValue, CONTACT_OPTION_TYPES, CARRER_TYPES
from .forms import ProfileForm, ExtraColumnForm

class ProfileController(Controller):
    def handle(self, request):
        template = self.view.get_template("index.html")
        profs = Profile.list()
        extra_columns = ExtraColumn.list()
        if request.method == "POST":
            try:
                form = ExtraColumnForm(request.post())
                extra_column = ExtraColumn()
                extra_column.name = form["name"]
                extra_column.create()
            except Exception as err:
                return Response.render(template, {
                    "title": "一覧",
                    "profs": profs,
                    "extra_columns": extra_columns,
                    "error": str(err)
                })
        return Response.render(template, {
            "title": "一覧",
            "profs": profs,
            "extra_columns": extra_columns
        })
    def create(self, request):
        template = self.view.get_template("create.html")
        if request.method == "POST":
            try:
                form = ProfileForm(request.post())
                prof = Profile()
                prof.name = form["name"]
                prof.ruby = form["ruby"]
                prof.epoch = form["epoch"]
                prof.career1 = int(form["career1"]) if form["career1"] is not None else None
                prof.career2 = int(form["career2"]) if form["career2"] is not None else None
                prof.career3 = int(form["career3"]) if form["career3"] is not None else None
                prof.career4 = int(form["career4"]) if form["career4"] is not None else None
                isostring = form["birthday"]
                if isostring[-1] == "Z": isostring = isostring[:-2]
                prof.birthday = datetime.fromisoformat(isostring)
                prof.image = form["image"]
                extra = form["extra"]
                prof.email = form["email"]
                prof.contactOption = int(form["contactOption"])
                prof.contactIdent = form["contactIdent"]
                prof.create()
                for colid, value in extra.items():
                    col = ExtraColumn.retrieve(colid)
                    val = ExtraColumnValue()
                    val.column = col
                    val.profile = prof
                    val.value = value
                    val.create()
                    print(val)
                template = self.view.get_template("thanks.html")
                return Response.render(template, {
                    "title": "図鑑登録",
                    "extra_columns": ExtraColumn.list()
                })
            except ValidationError as err:
                return Response.render(template, {
                    "title": "図鑑登録",
                    "error": err.message,
                    "extra_columns": ExtraColumn.list()
                })
        return Response.render(template, {
            "title": "図鑑登録",
            "extra_columns": ExtraColumn.list()
        })
    def retrieve(self, request):
        template = self.view.get_template("retrieve.html")
        prof = Profile.retrieve(request.params['id'])
        extra_columns = ExtraColumnValue.query.filter(ExtraColumnValue.profile == prof)
        return Response.render(template, {
            "title": prof.name,
            "prof": prof,
            "extra_columns": extra_columns
        })
    def search(self, request):
        template = self.view.get_template("search.html")
        wordsets = [wordset.split(' ') for wordset in request.query['words'][0].split(',')]
        return Response.render(template, {
            "title": "「" + request.query + "」の検索結果",
            "profs": profs
        })
