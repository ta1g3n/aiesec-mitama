#!/usr/bin/python

"""
uwsgi --http=0.0.0.0:8080 --wsgi-file=/path/to/this --callable=app.wsgi
"""
import os

from mitama.project import Project, include
from mitama.db import DatabaseManager

project_dir = os.path.dirname(os.path.abspath(__file__))

DatabaseManager({
    "type":"mysql",
    "host": "mysql",
    "name": "mitama",
    "password": os.environ["MITAMA_MYSQL_PASSWORD"],
    "user": "mitama"
})

project = Project(
    include("mitama.portal", path="/"),
    include("alumni-index", path="/alumni-index"),
    project_dir = project_dir
)
application = project.wsgi


if __name__ == "__main__":
    project.command()
