# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class MenuItem(Component):
    """A MenuItem component.
Material-UI MenuItem.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The content of the component.
- button (boolean; optional)
- alignItems (a value equal to: "center", "flex-start"; optional): Defines the `align-items` style property.
- disabled (boolean; optional): If `true`, the component is disabled.
- autoFocus (boolean; optional): If `true`, the list item is focused during the first mount.
Focus will also be triggered if the value changes from false to true.
- selected (boolean; optional): Use to apply selected styling.
- dense (boolean; optional): If `true`, compact vertical padding designed for keyboard and mouse input is used.
The prop defaults to the value inherited from the parent List component.
- disableGutters (boolean; optional): If `true`, the left and right padding is removed.
- divider (boolean; optional): If `true`, a 1px light border is added to the bottom of the list item.
- className (string; optional)
- value (string; default ''): The value represented by this menu item.
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, button=Component.UNDEFINED, alignItems=Component.UNDEFINED, disabled=Component.UNDEFINED, autoFocus=Component.UNDEFINED, selected=Component.UNDEFINED, dense=Component.UNDEFINED, disableGutters=Component.UNDEFINED, divider=Component.UNDEFINED, className=Component.UNDEFINED, value=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'button', 'alignItems', 'disabled', 'autoFocus', 'selected', 'dense', 'disableGutters', 'divider', 'className', 'value', 'id', 'classes', 'style']
        self._type = 'MenuItem'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'button', 'alignItems', 'disabled', 'autoFocus', 'selected', 'dense', 'disableGutters', 'divider', 'className', 'value', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(MenuItem, self).__init__(children=children, **args)
