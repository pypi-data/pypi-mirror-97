class HeaderResolve(object):
    def __init__(self, request):
        scope = dict(request)
        header_dict = {}
        headers = scope.get('headers')
        for header in headers:
            header_dict[str(header[0], encoding="utf-8")] = str(header[1], encoding="utf-8")
        self.header_dict = header_dict
        self.projectid = header_dict.get('projectid')
        self.request_id = header_dict.get('requestid')
        self.token = header_dict.get('token')
        self.featureid = header_dict.get('featureid')
        self.path = '/common' + scope.get('path')
