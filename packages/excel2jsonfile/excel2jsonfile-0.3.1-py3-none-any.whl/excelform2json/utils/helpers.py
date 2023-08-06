from lineage_excel2meta_interface.utils import messages, check_schema
import logging
import jinja2
import json


class UtilsHelper:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def __init__(self):
        self.jinja_environment = None

    def get_jinja_template(self, template_directory, template_name):
        module = __name__ + ".get_jinja_template"
        if template_name is None:
            return messages.message["jinja_template_name_not_provided"], None

        the_template = None
        self.logger.debug(module, "Jinja template requested: >%s<" % template_name)
        self.logger.debug(module, "Jinja template directory: >%s<" % template_directory)
        try:
            self.jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_directory))
            self.jinja_environment.filters["safe"] = json.dumps
            the_template = self.jinja_environment.get_template(template_name)
            self.logger.debug(module + ": Found jinja template: " + template_name)
        except jinja2.exceptions.TemplateNotFound:
            self.logger.error(module + ": Could not find jinja template >" + template_name
                            + "< in directory >" + template_directory + "<.")
            return messages.message["jinja_template_not_found"], None

        return messages.message["ok"], the_template

    def get_json(self, json_file):
        with open(json_file) as f:
            data = json.load(f)
        return data

    def check_schema(self, base_schema_folder, data):
        return check_schema.CheckSchema().check_schema(base_schema_folder=base_schema_folder, data=data)
