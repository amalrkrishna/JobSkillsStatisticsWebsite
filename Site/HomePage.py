import textwrap

from django.http import HttpResponse
from django.views.generic.base import View

class HomePageView(View):
    def dispatch(self, request, *args, **kwargs):
        
        response_text = textwrap.dedent('''\
        <link rel="stylesheet" type="text/css" href="/static/HomePage.css" />
            <html>
            <head>
                <title> Testing Hello World </title>
            </head>
            <body>
                <h1> Hello to the world </h1>
                <p> Hello Everyone! </p>
            </body>
            </html>
        ''')
        return HttpResponse(response_text)