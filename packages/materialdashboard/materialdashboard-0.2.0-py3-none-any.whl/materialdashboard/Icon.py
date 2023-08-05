# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Icon(Component):
    """An Icon component.
Material-UI Icon.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The name of the icon font ligature.
- baseClassName (string; optional): The base class applied to the icon. Defaults to 'material-icons', but can be changed to any
other base class that suits the icon font you're using (e.g. material-icons-rounded, fas, etc).
- color (a value equal to: "inherit", "action", "disabled", "error", "primary", "secondary"; optional): The color of the component. It supports those theme colors that make sense for this component.
- fontSize (a value equal to: "small", "inherit", "medium", "large"; optional): The fontSize applied to the icon. Defaults to 24px, but can be configure to inherit font size.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, baseClassName=Component.UNDEFINED, color=Component.UNDEFINED, fontSize=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'baseClassName', 'color', 'fontSize', 'className', 'id', 'classes', 'style']
        self._type = 'Icon'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'baseClassName', 'color', 'fontSize', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Icon, self).__init__(children=children, **args)
