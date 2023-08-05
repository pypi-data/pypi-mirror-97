# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class CardHeader(Component):
    """A CardHeader component.
Material-UI CardHeader.

Keyword arguments:
- action (boolean | number | string | dict | list; optional): The action to display in the card header.
- avatar (boolean | number | string | dict | list; optional): The Avatar element to display.
- disableTypography (boolean; optional): If `true`, `subheader` and `title` won't be wrapped by a Typography component.
This can be useful to render an alternative Typography variant by wrapping
the `title` text, and optional `subheader` text
with the Typography component.
- subheader (boolean | number | string | dict | list; optional): The content of the component.
- title (boolean | number | string | dict | list; optional): The content of the component.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, action=Component.UNDEFINED, avatar=Component.UNDEFINED, disableTypography=Component.UNDEFINED, subheader=Component.UNDEFINED, title=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['action', 'avatar', 'disableTypography', 'subheader', 'title', 'className', 'id', 'classes', 'style']
        self._type = 'CardHeader'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['action', 'avatar', 'disableTypography', 'subheader', 'title', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(CardHeader, self).__init__(**args)
