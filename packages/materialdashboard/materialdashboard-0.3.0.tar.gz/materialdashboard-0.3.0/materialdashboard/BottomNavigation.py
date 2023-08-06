# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class BottomNavigation(Component):
    """A BottomNavigation component.
Material-UI BottomNavigation.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The content of the component.
- showLabels (boolean; optional): If `true`, all `BottomNavigationAction`s will show their labels.
By default, only the selected `BottomNavigationAction` will show its label.
- value (boolean | number | string | dict | list; optional): The value of the currently selected `BottomNavigationAction`.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, showLabels=Component.UNDEFINED, value=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'showLabels', 'value', 'className', 'id', 'classes', 'style']
        self._type = 'BottomNavigation'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'showLabels', 'value', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(BottomNavigation, self).__init__(children=children, **args)
