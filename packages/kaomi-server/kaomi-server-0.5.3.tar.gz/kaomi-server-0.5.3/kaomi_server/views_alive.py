import cherrypy
from .functions import build_response, log_api_call


class Alive(object):
    """
    Classe contenitore di viste che danno informazioni di stato ai client
    """

    @cherrypy.expose()
    @cherrypy.tools.clear_content_type_parsers()
    def index(self):
        """
        Utilizzato per indicare se il kaomi deployer è up
        """
        res = build_response(status=0, substatus=0, message="https://www.youtube.com/watch?v=oHg5SJYRHA0")
        log_api_call(request=cherrypy.request, data='(omitted)', result=res)
        return res
