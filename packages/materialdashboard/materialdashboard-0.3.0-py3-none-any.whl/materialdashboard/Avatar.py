# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Avatar(Component):
    """An Avatar component.
Material-UI Avatar.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): Used to render icon or text elements inside the Avatar if `src` is not set.
This can be an element, or just a string.
- alt (string; optional): Used in combination with `src` or `srcSet` to
provide an alt attribute for the rendered `img` element.
- sizes (string; optional): The `sizes` attribute for the `img` element.
- src (string; optional): The `src` attribute for the `img` element.
- srcSet (string; optional): The `srcSet` attribute for the `img` element.
Use this attribute for responsive image display.
- variant (a value equal to: "square", "circular", "rounded"; optional): The shape of the avatar.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, alt=Component.UNDEFINED, sizes=Component.UNDEFINED, src=Component.UNDEFINED, srcSet=Component.UNDEFINED, variant=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'alt', 'sizes', 'src', 'srcSet', 'variant', 'className', 'id', 'classes', 'style']
        self._type = 'Avatar'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'alt', 'sizes', 'src', 'srcSet', 'variant', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Avatar, self).__init__(children=children, **args)
