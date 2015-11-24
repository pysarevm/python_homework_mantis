from model.project import Project
from selenium.webdriver.support.ui import Select
# -*- coding: utf-8 -*-


class ProjectHelper:
    def __init__(self, app):
        self.app = app

    def navigate_manage_projects_page(self):
        wd = self.app.wd
        if not (len(wd.find_elements_by_css_selector("input[value='Create New Project']")) > 0 and
                        wd.current_url.endswith("manage_proj_page.php") > 0):
            wd.get("http://localhost/mantisbt-1.2.19/manage_proj_page.php")

    project_cache = None

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.navigate_manage_projects_page()
            self.project_cache = []
            elements = wd.find_elements_by_xpath("/html/body/table[3]/tbody/tr")[2:]
            for element in elements:
                href = element.find_element_by_tag_name("a").get_attribute("href")
                name = element.find_element_by_tag_name("a").text
                id = href[70:len(href)]
                status = element.find_elements_by_tag_name("td")[1].text
                enabled =  element.find_elements_by_tag_name("td")[2].text
                view_state =  element.find_elements_by_tag_name("td")[3].text
                description =  element.find_elements_by_tag_name("td")[4].text
                self.project_cache.append(Project(name=name, id=id, status=status, enabled=enabled,
                                          view_state=view_state, description=description))
                print("Project 1: ", self.project_cache[0])
        return list(self.project_cache)

    def create(self, project):
            wd = self.app.wd
            self.navigate_manage_projects_page()
            # init group creation
            wd.find_element_by_css_selector("input[value='Create New Project']").click()
            self.fill_project_form(project)
            wd.find_element_by_css_selector("input[value='Add Project']").click()
            self.project_cache = None

    def fill_project_form(self, project):
        wd = self.app.wd
        self.fill_text_field("name", project.name)
        Select(wd.find_element_by_name("status")).select_by_visible_text(project.status)
        Select(wd.find_element_by_name("view_state")).select_by_visible_text(project.view_status)
        self.fill_text_field("description", project.description)

    def fill_text_field(self, field_name, field_data):
        wd = self.app.wd
        if field_data is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(field_data)