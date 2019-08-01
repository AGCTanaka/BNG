from wsgiref.handlers import CGIHandler
from hello import hello
CGIHandler().run(hello)
