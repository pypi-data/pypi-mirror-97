# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Box(Component):
    """A Box component.
Material-UI Box.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional)
- typography (string; optional): The **`typography`** property  is shorthand for the CSS properties **`font-family`**, **`font-weight`**, **`font-size`**, **`line-height`**, **`letter-spacing`** and **`text-transform``**.
It takes the values defined under `theme.typography` and spreads them on the element.

**Initial value**: `0`

| Chrome | Firefox | Safari |  Edge  |  IE   |
| :----: | :-----: | :----: | :----: | :---: |
| **2**  |  **1**  | **1**  | **12** | **5.5** |
- clone (boolean; optional)
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, typography=Component.UNDEFINED, clone=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'typography', 'clone', 'className', 'id', 'classes', 'style']
        self._type = 'Box'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'typography', 'clone', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Box, self).__init__(children=children, **args)
