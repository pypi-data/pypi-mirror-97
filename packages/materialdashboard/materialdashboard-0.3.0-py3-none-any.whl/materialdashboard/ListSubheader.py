# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ListSubheader(Component):
    """A ListSubheader component.
Material-UI ListSubheader.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The content of the component.
- color (a value equal to: "inherit", "primary", "default"; optional): The color of the component. It supports those theme colors that make sense for this component.
- disableGutters (boolean; optional): If `true`, the List Subheader will not have gutters.
- disableSticky (boolean; optional): If `true`, the List Subheader will not stick to the top during scroll.
- inset (boolean; optional): If `true`, the List Subheader is indented.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, color=Component.UNDEFINED, disableGutters=Component.UNDEFINED, disableSticky=Component.UNDEFINED, inset=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'color', 'disableGutters', 'disableSticky', 'inset', 'className', 'id', 'classes', 'style']
        self._type = 'ListSubheader'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'color', 'disableGutters', 'disableSticky', 'inset', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ListSubheader, self).__init__(children=children, **args)
