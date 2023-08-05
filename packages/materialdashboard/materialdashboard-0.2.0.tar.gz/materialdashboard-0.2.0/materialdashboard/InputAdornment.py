# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class InputAdornment(Component):
    """An InputAdornment component.
Material-UI InputAdornment.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The content of the component, normally an `IconButton` or string.
- disablePointerEvents (boolean; optional): Disable pointer events on the root.
This allows for the content of the adornment to focus the `input` on click.
- disableTypography (boolean; optional): If children is a string then disable wrapping in a Typography component.
- position (a value equal to: "end", "start"; optional): The position this adornment should appear relative to the `Input`.
- variant (a value equal to: "outlined", "standard", "filled"; optional): The variant to use.
Note: If you are using the `TextField` component or the `FormControl` component
you do not have to set this manually.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, disablePointerEvents=Component.UNDEFINED, disableTypography=Component.UNDEFINED, position=Component.UNDEFINED, variant=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'disablePointerEvents', 'disableTypography', 'position', 'variant', 'className', 'id', 'classes', 'style']
        self._type = 'InputAdornment'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'disablePointerEvents', 'disableTypography', 'position', 'variant', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(InputAdornment, self).__init__(children=children, **args)
