# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Divider(Component):
    """A Divider component.
Material-UI Divider.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The content of the component.
- absolute (boolean; optional): Absolutely position the element.
- flexItem (boolean; optional): If `true`, a vertical divider will have the correct height when used in flex container.
(By default, a vertical divider will have a calculated height of `0px` if it is the child of a flex container.)
- light (boolean; optional): If `true`, the divider will have a lighter color.
- orientation (a value equal to: "horizontal", "vertical"; optional): The component orientation.
- textAlign (a value equal to: "left", "right", "center"; optional): The text alignment.
- variant (a value equal to: "inset", "middle", "fullWidth"; optional): The variant to use.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, absolute=Component.UNDEFINED, flexItem=Component.UNDEFINED, light=Component.UNDEFINED, orientation=Component.UNDEFINED, textAlign=Component.UNDEFINED, variant=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'absolute', 'flexItem', 'light', 'orientation', 'textAlign', 'variant', 'className', 'id', 'classes', 'style']
        self._type = 'Divider'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'absolute', 'flexItem', 'light', 'orientation', 'textAlign', 'variant', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Divider, self).__init__(children=children, **args)
