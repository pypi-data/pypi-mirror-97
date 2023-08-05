# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SliderValueLabelUnstyled(Component):
    """A SliderValueLabelUnstyled component.
Material-UI SliderValueLabelUnstyled.

Keyword arguments:
- className (string; optional)
- valueLabelDisplay (a value equal to: "on", "off", "auto"; optional): Controls when the value label is displayed:

- `auto` the value label will display when the thumb is hovered or focused.
- `on` will display persistently.
- `off` will never display.
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, className=Component.UNDEFINED, valueLabelDisplay=Component.UNDEFINED, id=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['className', 'valueLabelDisplay', 'id', 'style']
        self._type = 'SliderValueLabelUnstyled'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['className', 'valueLabelDisplay', 'id', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(SliderValueLabelUnstyled, self).__init__(**args)
