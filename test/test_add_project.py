# -*- coding: utf-8 -*-
from model.project import Project


def test_add_project(app, json_project):
#    app.session.login("administrator", "root")
    project = json_project
    old_projects = app.project.get_project_list()
    app.project.create(project)
    new_projects = app.project.get_project_list()
    assert len(old_projects)+1 == len(new_projects)
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects,  key=Project.id_or_max)
