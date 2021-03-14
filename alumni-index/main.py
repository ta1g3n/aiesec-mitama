from mitama.app import App, Router
from mitama.utils.controllers import static_files
from mitama.utils.middlewares import SessionMiddleware, CsrfMiddleware
from mitama.app.method import view

from .model import CONTACT_OPTION_TYPES, CAREER_TYPES, CAREER_TYPES_FLAT
from .controller import ProfileController


class App(App):
    name = 'Alumni図鑑'
    description = ''
    router = Router(
        [
            view("/static/<path:path>", static_files()),
            view("/create", ProfileController, 'start_create'),
            view("/create/first", ProfileController, 'first_create'),
            view("/create/second", ProfileController, 'second_create'),
            view("/create/third", ProfileController, 'third_create'),
            view("/create/fin", ProfileController, 'fin_create'),
            Router([
                view("/", ProfileController),
                view("/register", ProfileController, 'register'),
                view("/search", ProfileController, 'search'),
                view("/<id>", ProfileController, 'retrieve'),
            ], middlewares = [SessionMiddleware]),
        ],
        middlewares = [CsrfMiddleware]
    )
    @property
    def view(self):
        view = super().view
        view.globals["CONTACT_OPTION_TYPES"] = CONTACT_OPTION_TYPES
        view.globals["CAREER_TYPES"] = CAREER_TYPES
        view.globals["CAREER_TYPES_FLAT"] = CAREER_TYPES_FLAT
        return view
