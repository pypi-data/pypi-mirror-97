class Form:
    def __init__(self, body):
        self.body = body

        self.data = self._getjson(body.decode() if isinstance(body, bytes) else body)

    def _getjson(self, data):
        data = data.split("&")

        parsed_json = {}

        for i in data:
            i = i.split("=")
            parsed_json[i[0]] = i[1]

        return parsed_json
    
    def __getitem__(self, key):
        return self.data[key]
