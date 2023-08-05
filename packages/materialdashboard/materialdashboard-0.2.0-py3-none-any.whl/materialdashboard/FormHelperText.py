# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FormHelperText(Component):
    """A FormHelperText component.
Material-UI FormHelperText.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The content of the component.

If `' '` is provided, the component reserves one line height for displaying a future message.
- disabled (boolean; optional): If `true`, the helper text should be displayed in a disabled state.
- error (boolean; optional): If `true`, helper text should be displayed in an error state.
- filled (boolean; optional): If `true`, the helper text should use filled classes key.
- focused (boolean; optional): If `true`, the helper text should use focused classes key.
- margin (string; optional): If `dense`, will adjust vertical spacing. This is normally obtained via context from
FormControl.
- required (boolean; optional): If `true`, the helper text should use required classes key.
- variant (a value equal to: "outlined", "standard", "filled"; optional): The variant to use.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, disabled=Component.UNDEFINED, error=Component.UNDEFINED, filled=Component.UNDEFINED, focused=Component.UNDEFINED, margin=Component.UNDEFINED, required=Component.UNDEFINED, variant=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'disabled', 'error', 'filled', 'focused', 'margin', 'required', 'variant', 'className', 'id', 'classes', 'style']
        self._type = 'FormHelperText'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'disabled', 'error', 'filled', 'focused', 'margin', 'required', 'variant', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(FormHelperText, self).__init__(children=children, **args)
