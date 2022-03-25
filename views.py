from templateRender.render import HtmlRender


def index():    
    ren = HtmlRender('templates\index.html', {'test': "hello"})
    return ren.render()