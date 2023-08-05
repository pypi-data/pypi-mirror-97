# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Container(Component):
    """A Container component.
Material-UI Container.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional)
- disableGutters (boolean; optional): If `true`, the left and right padding is removed.
- fixed (boolean; optional): Set the max-width to match the min-width of the current breakpoint.
This is useful if you'd prefer to design for a fixed set of sizes
instead of trying to accommodate a fully fluid viewport.
It's fluid by default.
- maxWidth (a value equal to: false, "xs", "sm", "md", "lg", "xl"; optional): Determine the max-width of the container.
The container width grows with the size of the screen.
Set to `false` to disable `maxWidth`.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, disableGutters=Component.UNDEFINED, fixed=Component.UNDEFINED, maxWidth=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'disableGutters', 'fixed', 'maxWidth', 'className', 'id', 'classes', 'style']
        self._type = 'Container'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'disableGutters', 'fixed', 'maxWidth', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Container, self).__init__(children=children, **args)
