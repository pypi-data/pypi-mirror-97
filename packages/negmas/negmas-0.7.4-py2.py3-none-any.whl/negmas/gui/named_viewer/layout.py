from typing import Type

import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import dash_table as tbl
from dash.dependencies import Input, Output, State

from negmas.common import NamedObject
from negmas.visualizers import visualizer_type


def layout(object_type: Type[NamedObject]):
    """Returns a layout appropriate for the given named object"""

    layout = [html.Div(id="basic_info", children=None)]
    v = visualizer_type(object_type)
    children = v.children
    if len(children) > 0:
        c = html.Div(id="children")
        for category, v in children:
            c.append(html.H1(category))
            c.append(html.Div(id=category))
