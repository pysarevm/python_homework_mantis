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
            for element in wd.find_elements_by_class_name.startswith("row-"):
                a = element.find_elements_by_tag_name("td")[0]
                name = a.find_element_by_tag_name("a").text
                href = a.find_element_by_tag_name("a").getAttribute("href")
                id = href[37:len(href)]
                status = element.find_elements_by_tag_name("td")[1].text
                enabled =  element.find_elements_by_tag_name("td")[2].text
                view_status =  element.find_elements_by_tag_name("td")[3].text
                description =  element.find_elements_by_tag_name("td")[4].text
                self.project_cache.append(Project(name=name, id=id, status=status, enabled=enabled,
                                                  view_status=view_status, description=description))
        return list(self.project_cache)

    def create(self, project):
            wd = self.app.wd
            self.navigate_manage_projects_page()
            # init group creation
            wd.find_element_by_css_selector("input[value='Create New Project']").click()
            self.fill_project_form(project)
            # submit group creation
            wd.find_element_by_name("submit").click()
            self.return_to_groups_page()
            self.group_cache = None

    def fill_project_form(self, project):
        wd = self.app.wd
        self.fill_text_field("name", project.name)
        Select(wd.find_element_by_name("status")).select_by_visible_text(project.status)
        Select(wd.find_element_by_name("view_state")).select_by_visible_text(project.status)
        self.fill_text_field("description", project.description)
        wd.find_element_by_css_selector("input[value='Add Project']").click()





    def fill_text_field(self, field_name, field_data):
        wd = self.app.wd
        if field_data is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(field_data)

    def open_group_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/group.php") and len( wd.find_elements_by_name("new")) > 0):
            self.navigate_main_page()
            wd.find_element_by_link_text("Групи").click()

    def delete_first_group(self):
        self.delete_group_by_index(0)

    def delete_group_by_index(self, index):
        wd = self.app.wd
        self.open_group_page()
        self.select_group_by_index(index)
        wd.find_element_by_name("delete").click()
        self.return_to_groups_page()
        self.group_cache = None

    def delete_group_by_id(self, id):
        wd = self.app.wd
        self.open_group_page()
        self.select_group_by_id(id)
        wd.find_element_by_name("delete").click()
        self.return_to_groups_page()
        self.group_cache = None

    def edit_first_group(self, group):
        self.edit_group_by_index(0, group)

    def edit_group_by_index(self, index, group):
        wd = self.app.wd
        self.open_group_page()
        self.select_group_by_index(index)
        wd.find_element_by_name("edit").click()
        self.fill_group_form(group)
        wd.find_element_by_name("update").click()
        self.return_to_groups_page()
        self.group_cache = None

    def edit_group_by_id(self, id, group):
        wd = self.app.wd
        self.open_group_page()
        self.select_group_by_id(id)
        wd.find_element_by_name("edit").click()
        self.fill_group_form(group)
        wd.find_element_by_name("update").click()
        self.return_to_groups_page()
        self.group_cache = None

    def select_first_group(self):
        wd = self.app.wd
        wd.find_element_by_name("selected[]").click()

    def select_group_by_index(self, index):
        wd = self.app.wd
        wd.find_elements_by_name("selected[]")[index].click()

    def select_group_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_css_selector("input[value='%s']" % id).click()

    def count(self):
        wd = self.app.wd
        self.open_group_page()
        return len(wd.find_elements_by_name("selected[]"))

    def navigate_main_page(self):
        wd = self.app.wd
        if not (len(wd.find_elements_by_name("searchstring"))>0 and wd.current_url.endswith("/addressbook/") > 0):
            wd.get("http://localhost/addressbook/")

    group_cache = None

    def get_group_list(self):
        if self.group_cache is None:
            wd = self.app.wd
            self.open_group_page()
            self.group_cache = []
            for element in wd.find_elements_by_css_selector("span.group"):
                text = element.text
                id = element.find_element_by_name("selected[]").get_attribute("value")
                self.group_cache.append(Group(name=text, id=id))
        return list(self.group_cache)

    def delete_groups_with_same_names(self):
        group_list = self.get_group_list()
        to_delete_list = []
        for i in range(0, len(group_list)-1):
            for j in range(i+1, len(group_list)):
                if group_list[i].name == group_list[j].name:
                    if group_list[j].id not in to_delete_list:
                        to_delete_list.append(group_list[j].id)
        print("test. to_deleteList: ", to_delete_list)
        for i in to_delete_list:
            self.delete_group_by_id(i)

