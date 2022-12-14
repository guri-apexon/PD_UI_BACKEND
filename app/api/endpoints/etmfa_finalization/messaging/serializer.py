from datetime import datetime, timedelta
import json


class JsonSerializer(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%d-%m-%Y %H:%M:%S')
        elif isinstance(o, timedelta):
            return str(o)

        return super().default(o)

    def encode(self, o):

        # This is a workaround until management is able to
        # process list of values inside DB
        # https://gitlabrnds.quintiles.com/etmf-group/etmfa-management-service/issues/5
        if isinstance(o, dict):
            dict_with_string_lists = {}
            for key, value in o.items():
                
                if (isinstance(value, list) or isinstance(value, dict)) and key != "doc_date":
                    dict_with_string_lists[key] = str(value)
                else:
                    dict_with_string_lists[key] = value
            
            return super().encode(dict_with_string_lists)

        return super().encode(o)
