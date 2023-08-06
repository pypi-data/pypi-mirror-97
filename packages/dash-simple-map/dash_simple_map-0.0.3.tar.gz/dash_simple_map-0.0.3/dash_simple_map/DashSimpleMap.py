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
- colorScaleDomain (list of numbers; optional): Array of min and max values used to define scale of color domains
- colorScaleRange (list of strings; optional): Array of hexadecimal colors for the chloropleth map
- borderColor (list of strings; optional): Array of hexadecimal colors for the borders strokes, normal and on hover
- dataField (string; optional): The field to use in data for the chloropleth, default to value.
- tooltip (boolean; optional): Display or not a tooltip when hovering countries/states
- tooltip_format (string; optional): Define the text to display in the tooltip, allow jsx tags and variables of data between braces, eg. :
<strong>Canton: {canton_name}</strong><br><br>Taux d'occupation des unités de soin intensifs: {ICUPercent_FreeCapacity}
- legend (boolean; optional): Display or not a legend
- legend_title (string; optional): Legeng title, default to ""
- legend_labels (list of numbers; optional): Array of tick number to display in the legend, default to [0, 25, 50, 75, 100]
- legend_square_size (number; optional): Size of a square in the legend, in pixels
- geojson (dict; required): GeoJSON file containing the geometry information of what we want to draw, 
Should contain a unique id for each feature `feature.id` and the coordinates 
should be already computed. If not, you can create/modify your geojson at
https://mapshaper.org/
- data (dict; required): The chloropleth and tooltip data. Should have the form:

  `{feature.id: '...', dataField: '...', ...}`

Make sure that for each feature id you have in your geojson, there is a match in data.
Any additionnal field associated with a feature id can be display in the tooltip_format."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, padding=Component.UNDEFINED, colorScaleDomain=Component.UNDEFINED, colorScaleRange=Component.UNDEFINED, borderColor=Component.UNDEFINED, dataField=Component.UNDEFINED, tooltip=Component.UNDEFINED, tooltip_format=Component.UNDEFINED, legend=Component.UNDEFINED, legend_title=Component.UNDEFINED, legend_labels=Component.UNDEFINED, legend_square_size=Component.UNDEFINED, geojson=Component.REQUIRED, data=Component.REQUIRED, **kwargs):
        self._prop_names = ['id', 'width', 'height', 'padding', 'colorScaleDomain', 'colorScaleRange', 'borderColor', 'dataField', 'tooltip', 'tooltip_format', 'legend', 'legend_title', 'legend_labels', 'legend_square_size', 'geojson', 'data']
        self._type = 'DashSimpleMap'
        self._namespace = 'dash_simple_map'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'width', 'height', 'padding', 'colorScaleDomain', 'colorScaleRange', 'borderColor', 'dataField', 'tooltip', 'tooltip_format', 'legend', 'legend_title', 'legend_labels', 'legend_square_size', 'geojson', 'data']
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
