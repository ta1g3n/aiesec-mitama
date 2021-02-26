from mitama.app import App, Router
from mitama.utils.controllers import static_files
from mitama.utils.middlewares import SessionMiddleware, CsrfMiddleware
from mitama.app.method import view

from .model import CONTACT_OPTION_TYPES, CARRER_TYPES
from .controller import ProfileController


class App(App):
    name = 'Alumni図鑑'
    description = ''
    router = Router(
        [
            view("/static/<path:path>", static_files()),
            view("/create", ProfileController, 'create'),
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
        view.globals["CARRER_TYPES"] = CARRER_TYPES
        return view
