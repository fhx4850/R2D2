from templateService.render import HtmlRender


def index():    
    ren = HtmlRender('templates\index.html', {'test': "hello"})
    ren.add_template_func(hi)    
    return ren.render()

def hi():
    return 'hello'