from jinja2 import Environment, FileSystemLoader
import settings

class HtmlRender:
    def __init__(self, template_path: str, template_data: dict):
        self.template_path = template_path
        self.template_data = template_data
        
    def render(self):
        
        templ_path, templ_name = self._create_template_path(self.template_path)
        
        env = Environment(loader=FileSystemLoader(templ_path))
        templ = env.get_template(templ_name)
        
        data = self.template_data
        
        template = templ.render(data)
        return template
    
    def _create_template_path(self, path):
        parse_path = path.split('\\')
        template_path = ''
        template_name = parse_path[-1]
        for i in parse_path[:-1]:
            template_path += i + '/'
        return template_path, template_name