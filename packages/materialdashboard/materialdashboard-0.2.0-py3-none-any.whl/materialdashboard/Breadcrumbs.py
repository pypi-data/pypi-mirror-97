# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Breadcrumbs(Component):
    """A Breadcrumbs component.
Material-UI Breadcrumbs.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The content of the component.
- expandText (string; optional): Override the default label for the expand button.

For localization purposes, you can use the provided [translations](/guides/localization/).
- itemsAfterCollapse (number; optional): If max items is exceeded, the number of items to show after the ellipsis.
- itemsBeforeCollapse (number; optional): If max items is exceeded, the number of items to show before the ellipsis.
- maxItems (number; optional): Specifies the maximum number of breadcrumbs to display. When there are more
than the maximum number, only the first `itemsBeforeCollapse` and last `itemsAfterCollapse`
will be shown, with an ellipsis in between.
- separator (boolean | number | string | dict | list; optional): Custom separator node.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, expandText=Component.UNDEFINED, itemsAfterCollapse=Component.UNDEFINED, itemsBeforeCollapse=Component.UNDEFINED, maxItems=Component.UNDEFINED, separator=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'expandText', 'itemsAfterCollapse', 'itemsBeforeCollapse', 'maxItems', 'separator', 'className', 'id', 'classes', 'style']
        self._type = 'Breadcrumbs'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'expandText', 'itemsAfterCollapse', 'itemsBeforeCollapse', 'maxItems', 'separator', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Breadcrumbs, self).__init__(children=children, **args)
