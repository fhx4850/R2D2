class UrlRouting:
    
    def __init__(self, urls_path):
        self.urls_path = urls_path
        self._parse_path(self.urls_path)
    
    URLS = {}
    URLS_NAME = {}
    
    def _parse_path(self, urls_path):
        for path in urls_path:
            self.path(path['path'], path['handler'], path['name'])
    

    def path(self, path, handler, name=None):
        self.__class__.URLS[path] = handler
        self.__class__.URLS_NAME[name] = path