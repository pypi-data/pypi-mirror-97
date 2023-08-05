# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ButtonGroup(Component):
    """A ButtonGroup component.
Material-UI ButtonGroup.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The content of the component.
- color (a value equal to: "inherit", "primary", "secondary"; optional): The color of the component. It supports those theme colors that make sense for this component.
- disabled (boolean; optional): If `true`, the component is disabled.
- disableElevation (boolean; optional): If `true`, no elevation is used.
- disableFocusRipple (boolean; optional): If `true`, the button keyboard focus ripple is disabled.
- disableRipple (boolean; optional): If `true`, the button ripple effect is disabled.
- fullWidth (boolean; optional): If `true`, the buttons will take up the full width of its container.
- orientation (a value equal to: "horizontal", "vertical"; optional): The component orientation (layout flow direction).
- size (a value equal to: "small", "medium", "large"; optional): The size of the component.
`small` is equivalent to the dense button styling.
- variant (a value equal to: "text", "outlined", "contained"; optional): The variant to use.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, color=Component.UNDEFINED, disabled=Component.UNDEFINED, disableElevation=Component.UNDEFINED, disableFocusRipple=Component.UNDEFINED, disableRipple=Component.UNDEFINED, fullWidth=Component.UNDEFINED, orientation=Component.UNDEFINED, size=Component.UNDEFINED, variant=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'color', 'disabled', 'disableElevation', 'disableFocusRipple', 'disableRipple', 'fullWidth', 'orientation', 'size', 'variant', 'className', 'id', 'classes', 'style']
        self._type = 'ButtonGroup'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'color', 'disabled', 'disableElevation', 'disableFocusRipple', 'disableRipple', 'fullWidth', 'orientation', 'size', 'variant', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ButtonGroup, self).__init__(children=children, **args)
