# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Chip(Component):
    """A Chip component.
Material-UI Chip.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): This prop isn't supported.
Use the `component` prop if you need to change the children structure.
- clickable (boolean; optional): If `true`, the chip will appear clickable, and will raise when pressed,
even if the onClick prop is not defined.
If `false`, the chip will not appear clickable, even if onClick prop is defined.
This can be used, for example,
along with the component prop to indicate an anchor Chip is clickable.
Note: this controls the UI and does not affect the onClick event.
- color (a value equal to: "primary", "secondary", "default"; optional): The color of the component. It supports those theme colors that make sense for this component.
- disabled (boolean; optional): If `true`, the component is disabled.
- label (boolean | number | string | dict | list; optional): The content of the component.
- size (a value equal to: "small", "medium"; optional): The size of the component.
- variant (a value equal to: "outlined", "filled"; optional): The variant to use.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, clickable=Component.UNDEFINED, color=Component.UNDEFINED, disabled=Component.UNDEFINED, label=Component.UNDEFINED, size=Component.UNDEFINED, variant=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'clickable', 'color', 'disabled', 'label', 'size', 'variant', 'className', 'id', 'classes', 'style']
        self._type = 'Chip'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'clickable', 'color', 'disabled', 'label', 'size', 'variant', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Chip, self).__init__(children=children, **args)
