# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ExtendSliderUnstyled(Component):
    """An ExtendSliderUnstyled component.
Material-UI ExtendSliderUnstyled.

Keyword arguments:
- disabled (boolean; optional): If `true`, the component is disabled.
- isRtl (boolean; optional): Indicates whether the theme context has rtl direction. It is set automatically.
- max (number; optional): The maximum allowed value of the slider.
Should not be equal to min.
- min (number; optional): The minimum allowed value of the slider.
Should not be equal to max.
- name (string; optional): Name attribute of the hidden `input` element.
- orientation (a value equal to: "horizontal", "vertical"; optional): The component orientation.
- step (number; optional): The granularity with which the slider can step through values. (A "discrete" slider.)
The `min` prop serves as the origin for the valid values.
We recommend (max - min) to be evenly divisible by the step.

When step is `null`, the thumb can only be slid onto marks provided with the `marks` prop.
- track (a value equal to: false, "normal", "inverted"; optional): The track presentation:

- `normal` the track will render a bar representing the slider value.
- `inverted` the track will render a bar representing the remaining slider value.
- `false` the track will render without a bar.
- valueLabelDisplay (a value equal to: "on", "off", "auto"; optional): Controls when the value label is displayed:

- `auto` the value label will display when the thumb is hovered or focused.
- `on` will display persistently.
- `off` will never display.
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component."""
    @_explicitize_args
    def __init__(self, disabled=Component.UNDEFINED, isRtl=Component.UNDEFINED, max=Component.UNDEFINED, min=Component.UNDEFINED, name=Component.UNDEFINED, orientation=Component.UNDEFINED, step=Component.UNDEFINED, track=Component.UNDEFINED, valueLabelDisplay=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, **kwargs):
        self._prop_names = ['disabled', 'isRtl', 'max', 'min', 'name', 'orientation', 'step', 'track', 'valueLabelDisplay', 'id', 'classes']
        self._type = 'ExtendSliderUnstyled'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['disabled', 'isRtl', 'max', 'min', 'name', 'orientation', 'step', 'track', 'valueLabelDisplay', 'id', 'classes']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ExtendSliderUnstyled, self).__init__(**args)
