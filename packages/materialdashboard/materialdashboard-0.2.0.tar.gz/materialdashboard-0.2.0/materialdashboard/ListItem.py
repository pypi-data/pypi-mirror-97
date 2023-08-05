# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ListItem(Component):
    """A ListItem component.
Material-UI ListItem.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The content of the component if a `ListItemSecondaryAction` is used it must
be the last child.
- button (boolean; optional): If `true`, the list item is a button (using `ButtonBase`). Props intended
for `ButtonBase` can then be applied to `ListItem`.
- alignItems (a value equal to: "center", "flex-start"; optional): Defines the `align-items` style property.
- autoFocus (boolean; optional): If `true`, the list item is focused during the first mount.
Focus will also be triggered if the value changes from false to true.
- dense (boolean; optional): If `true`, compact vertical padding designed for keyboard and mouse input is used.
The prop defaults to the value inherited from the parent List component.
- disabled (boolean; optional): If `true`, the component is disabled.
- disableGutters (boolean; optional): If `true`, the left and right padding is removed.
- divider (boolean; optional): If `true`, a 1px light border is added to the bottom of the list item.
- selected (boolean; optional): Use to apply selected styling.
- className (string; optional)
- n_clicks (number; default 0)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, button=Component.UNDEFINED, alignItems=Component.UNDEFINED, autoFocus=Component.UNDEFINED, dense=Component.UNDEFINED, disabled=Component.UNDEFINED, disableGutters=Component.UNDEFINED, divider=Component.UNDEFINED, selected=Component.UNDEFINED, className=Component.UNDEFINED, n_clicks=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'button', 'alignItems', 'autoFocus', 'dense', 'disabled', 'disableGutters', 'divider', 'selected', 'className', 'n_clicks', 'id', 'classes', 'style']
        self._type = 'ListItem'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'button', 'alignItems', 'autoFocus', 'dense', 'disabled', 'disableGutters', 'divider', 'selected', 'className', 'n_clicks', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ListItem, self).__init__(children=children, **args)
