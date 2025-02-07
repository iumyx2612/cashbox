import json

from llama_index.core.output_parsers import PydanticOutputParser


class ViPydanticOutputParser(PydanticOutputParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_format_string(self, escape_json: bool = True) -> str:
        """Format string."""
        schema_dict = self._output_cls.model_json_schema()
        for key in self._excluded_schema_keys_from_format:
            del schema_dict[key]

        schema_str = json.dumps(schema_dict, ensure_ascii=False) # To output Vietnamese
        output_str = self._pydantic_format_tmpl.format(schema=schema_str)
        if escape_json:
            return output_str.replace("{", "{{").replace("}", "}}")
        else:
            return output_str