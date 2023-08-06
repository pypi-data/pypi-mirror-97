# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TableRow(Component):
    """A TableRow component.
Material-UI TableRow.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): Should be valid <tr> children such as `TableCell`.
- hover (boolean; optional): If `true`, the table row will shade on hover.
- selected (boolean; optional): If `true`, the table row will have the selected shading.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, hover=Component.UNDEFINED, selected=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'hover', 'selected', 'className', 'id', 'classes', 'style']
        self._type = 'TableRow'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'hover', 'selected', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TableRow, self).__init__(children=children, **args)
