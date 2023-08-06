# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FormControl(Component):
    """A FormControl component.
Material-UI FormControl.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The content of the component.
- color (a value equal to: "primary", "secondary"; optional): The color of the component. It supports those theme colors that make sense for this component.
- disabled (boolean; optional): If `true`, the label, input and helper text should be displayed in a disabled state.
- error (boolean; optional): If `true`, the label is displayed in an error state.
- fullWidth (boolean; optional): If `true`, the component will take up the full width of its container.
- focused (boolean; optional): If `true`, the component is displayed in focused state.
- hiddenLabel (boolean; optional): If `true`, the label is hidden.
This is used to increase density for a `FilledInput`.
Be sure to add `aria-label` to the `input` element.
- margin (a value equal to: "none", "normal", "dense"; optional): If `dense` or `normal`, will adjust vertical spacing of this and contained components.
- required (boolean; optional): If `true`, the label will indicate that the `input` is required.
- size (a value equal to: "small", "medium"; optional): The size of the component.
- variant (a value equal to: "outlined", "standard", "filled"; optional): The variant to use.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, color=Component.UNDEFINED, disabled=Component.UNDEFINED, error=Component.UNDEFINED, fullWidth=Component.UNDEFINED, focused=Component.UNDEFINED, hiddenLabel=Component.UNDEFINED, margin=Component.UNDEFINED, required=Component.UNDEFINED, size=Component.UNDEFINED, variant=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'color', 'disabled', 'error', 'fullWidth', 'focused', 'hiddenLabel', 'margin', 'required', 'size', 'variant', 'className', 'id', 'classes', 'style']
        self._type = 'FormControl'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'color', 'disabled', 'error', 'fullWidth', 'focused', 'hiddenLabel', 'margin', 'required', 'size', 'variant', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(FormControl, self).__init__(children=children, **args)
