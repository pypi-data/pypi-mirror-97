import json
import jsonschema
from lineage_excel2meta_interface.utils import messages


class CheckSchema:
    """
    Checks the JSON schema of a given JSON file
    """
    code_version = "0.1.0"

    def __init__(self):
        self.json_file = "not provided"
        self.json_data = ""
        self.meta_type = "unknown"
        self.meta_version = "unknown"
        self.schema_file = "unknown"

    def check_schema(self, base_schema_folder, data):
        """
        Checks the JSON to determine which JSON schema is used and which version
        """
        module = "CheckSchema.check_schema"
        self.json_data = data

        try:
            self.meta_type = data["meta"]
            self.meta_version = data["meta_version"]
        except KeyError as e:
            result = messages.message["meta_error"]
            result["info"] = "Key error. meta and meta_version must be in JSON file."
            return result
        except jsonschema.exceptions.SchemaError as e:
            result = messages.message["json_schema_error"]
            result["info"] = e.message
            return result
        except jsonschema.exceptions.ValidationError as e:
            result = messages.message["json_validation_error"]
            result["info"] = e.message
            return result
        except json.decoder.JSONDecodeError as e:
            result = messages.message["json_parse_error"]
            result["info"] = e.msg
            return result

        schema_directory = base_schema_folder + self.meta_version + "/"
        self.schema_file = schema_directory + self.meta_type + ".json"
        try:
            with open(self.schema_file) as f:
                schema = json.load(f)
                try:
                    jsonschema.validate(data, schema)
                except jsonschema.exceptions.SchemaError as e:
                    result = messages.message["jsonschema_validation_error"]
                    result["info"] = e.message
                    return result
                except jsonschema.exceptions.ValidationError as e:
                    result = messages.message["jsonschema_validation_error"]
                    result["info"] = e.message
                    return result
        except FileNotFoundError:
            return messages.message["schema_file_not_found"]

        return messages.message["ok"]
