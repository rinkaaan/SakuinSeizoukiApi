from apiflask import Schema
from marshmallow.fields import Integer, List, Nested, String


class PageType(Schema):
    width = Integer()
    height = Integer()
    page_numbers = List(Integer())
    type = Integer()


class Annotation(Schema):
    x = Integer()
    y = Integer()
    width = Integer()
    height = Integer()
    group_index = Integer()


class PageTypeDetail(Schema):
    annotations = List(Nested(Annotation))
    page_numbers = List(Integer())


class WordPages(Schema):
    word = String()
    pages = List(Integer())
