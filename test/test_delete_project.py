from model.project import Project
import random


def test_delete_some_project(app):
    if len(app.project.get_project_list()) == 0:
        app.project.create(Project(name="for_delete_test"))
    old_projects = app.project.get_project_list()
    project = random.choice(old_projects)
    app.project.delete_project_by_name(project.name)
    print("deleted")
    new_projects = app.project.get_project_list()
    assert len(old_projects) - 1 == len(new_projects)
    old_projects.remove(project)
    assert old_projects == new_projects
