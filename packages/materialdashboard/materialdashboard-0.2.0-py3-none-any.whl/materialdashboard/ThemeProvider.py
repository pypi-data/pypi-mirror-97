# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ThemeProvider(Component):
    """A ThemeProvider component.
Material-UI ThemeProvider.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional)
- theme (dict; optional): The theme that will be applied to all children of this component.
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app."""
    @_explicitize_args
    def __init__(self, children=None, theme=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'theme', 'id']
        self._type = 'ThemeProvider'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'theme', 'id']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ThemeProvider, self).__init__(children=children, **args)
