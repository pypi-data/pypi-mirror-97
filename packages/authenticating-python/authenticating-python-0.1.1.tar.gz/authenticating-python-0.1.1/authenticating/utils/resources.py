class Header:
    def __init__(self, api_key, format):
        self.api_key = api_key
        self.format = format

    def get_headers(self):
        return{
            'Authorization: Bearer {api_key}'.format(api_key=self.api_key),
            'Content-Type: application/{format}'.format(format=self.format)
        }