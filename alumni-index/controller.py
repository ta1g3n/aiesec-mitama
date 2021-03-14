from mitama.app import Controller
from mitama.app.http import Response
from mitama.app.forms import ValidationError
import io
from PIL import Image


from .model import (
    Profile, ExtraColumn, ExtraColumnValue, Career, TravelHistory
)
from .forms import ProfileForm, CareerForm, ExtraColumnForm


def resize(icon):
    if icon is None:
        return None
    try:
        img = Image.open(io.BytesIO(icon))
    except Exception:
        return icon
    width, height = img.size
    if width > height:
        scale = 256 / height
    else:
        scale = 256 / width
    width *= scale
    height *= scale
    r = img.resize((int(width), int(height)), resample=Image.NEAREST)
    export = io.BytesIO()
    r.save(export, format="JPEG", quality=90)
    return export.getvalue()


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

    def start_create(self, request):
        template = self.view.get_template("create/start.html")
        return Response.render(template)

    def fin_create(self, request):
        template = self.view.get_template("create/fin.html")
        return Response.render(template)

    def first_create(self, request):
        template = self.view.get_template("create/profile.html")
        error = ""
        if request.method == "POST":
            try:
                form = ProfileForm(request.post())
                prof = Profile()
                prof.name = form["name"]
                prof.ruby = form["ruby"]
                prof.epoch = form["epoch"]
                prof.image = resize(form["image"])
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
                sess = request.session()
                sess["profile_id"] = prof._id
                return Response.redirect(
                    self.app.convert_url("/create/second")
                )
            except Exception as err:
                error = str(err)
        return Response.render(template, {
            "title": "図鑑登録",
            "error": error,
            "extra_columns": ExtraColumn.list()
        })

    def second_create(self, request):
        template = self.view.get_template("create/tables.html")
        error = ""
        form = {}
        sess = request.session()
        try:
            prof = Profile.retrieve(sess["profile_id"])
        except Exception:
            return Response.redirect(self.app.convert_url("/create"))
        if request.method == "POST":
            form = CareerForm(request.post())
            try:
                careers = form["careers"]
                histories = form["histories"]
                for career_ in careers.values():
                    career = Career()
                    career.type = int(career_["type"])
                    career.grade = int(career_["grade"])
                    career.profile = prof
                    career.create()
                for history_ in histories.values():
                    history = TravelHistory()
                    history.year = history_["year"]
                    history.place = history_["place"]
                    history.profile = prof
                    history.description = history_["description"]
                    history.create()
                return Response.redirect(
                    self.app.convert_url("/create/fin")
                )
            except Exception as err:
                error = str(err)
        return Response.render(template, {
            "error": error,
            "form": form
        })

    def create(self, request):
        template = self.view.get_template("create/profile.html")
        if request.method == "POST":
            try:
                form = ProfileForm(request.post())
                prof = Profile()
                prof.name = form["name"]
                prof.ruby = form["ruby"]
                prof.epoch = form["epoch"]
                prof.image = resize(form["image"])
                extra = form["extra"]
                prof.email = form["email"]
                prof.contactOption = int(form["contactOption"])
                prof.contactIdent = form["contactIdent"]
                prof.create()
                careers = form["careers"]
                histories = form["histories"]
                for career_ in careers.values():
                    career = Career()
                    career.type = int(career_["type"])
                    career.grade = int(career_["grade"])
                    career.profile = prof
                    career.create()
                for history_ in histories.values():
                    history = TravelHistory()
                    history.year = history_["year"]
                    history.place = history_["place"]
                    history.profile = prof
                    history.description = history_["description"]
                    history.create()
                for colid, value in extra.items():
                    col = ExtraColumn.retrieve(colid)
                    val = ExtraColumnValue()
                    val.column = col
                    val.profile = prof
                    val.value = value
                    val.create()
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
        extra_columns = ExtraColumnValue.query.filter(
            ExtraColumnValue.profile == prof
        )
        return Response.render(template, {
            "title": prof.name,
            "prof": prof,
            "extra_columns": extra_columns
        })

    def search(self, request):
        template = self.view.get_template("search.html")
        # wordsets = [
        #     wordset.split(' ')
        #     for wordset
        #     in request.query['words'][0].split(',')
        # ]
        return Response.render(template, {
            "title": "「" + request.query + "」の検索結果",
            # "profs": profs
        })
