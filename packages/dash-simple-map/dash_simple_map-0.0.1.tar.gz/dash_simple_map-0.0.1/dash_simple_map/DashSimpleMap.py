# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashSimpleMap(Component):
    """A DashSimpleMap component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- width (number; optional): Width of the figure to draw, in pixels
- height (number; optional): Height of the figure to draw, in pixels
- padding (number; optional): Pixels to leave blank around the edges of the map
- colorScaleDomain (list of numbers; optional): Array of min and max values used to define scale of color
- colorScaleRange (list of strings; optional): Array of hexadecimal colors for the chloropleth map
- tooltip (boolean; optional): Display or not a tooltip when hovering countries/states
- legend (boolean; optional): Display or not a legend
- geojson (dict; required): The sunburst data. Should have the form:

  `{name: '...', children: [c0, c1, c2]}`

and children `c<i>` can have the same form to arbitrary nesting,
or for leaf nodes the form is:

  `{name: '...', size: ###}`

any node can also have a `color` property, set to any CSS color string,
to use instead of the default coloring. Nodes with no children will
inherit their parent's color if not specified. Otherwise colors are pulled
from d3.scale.category20 in the order nodes are encountered.
- data (dict; required): The sunburst data. Should have the form:

  `{name: '...', children: [c0, c1, c2]}`

and children `c<i>` can have the same form to arbitrary nesting,
or for leaf nodes the form is:

  `{name: '...', size: ###}`

any node can also have a `color` property, set to any CSS color string,
to use instead of the default coloring. Nodes with no children will
inherit their parent's color if not specified. Otherwise colors are pulled
from d3.scale.category20 in the order nodes are encountered."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, padding=Component.UNDEFINED, colorScaleDomain=Component.UNDEFINED, colorScaleRange=Component.UNDEFINED, tooltip=Component.UNDEFINED, legend=Component.UNDEFINED, geojson=Component.REQUIRED, data=Component.REQUIRED, **kwargs):
        self._prop_names = ['id', 'width', 'height', 'padding', 'colorScaleDomain', 'colorScaleRange', 'tooltip', 'legend', 'geojson', 'data']
        self._type = 'DashSimpleMap'
        self._namespace = 'dash_simple_map'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'width', 'height', 'padding', 'colorScaleDomain', 'colorScaleRange', 'tooltip', 'legend', 'geojson', 'data']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['geojson', 'data']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashSimpleMap, self).__init__(**args)
