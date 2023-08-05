# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class CardMedia(Component):
    """A CardMedia component.
Material-UI CardMedia.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The content of the component.
- image (string; optional): Image to be displayed as a background image.
Either `image` or `src` prop must be specified.
Note that caller must specify height otherwise the image will not be visible.
- src (string; optional): An alias for `image` property.
Available only with media components.
Media components: `video`, `audio`, `picture`, `iframe`, `img`.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, image=Component.UNDEFINED, src=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'image', 'src', 'className', 'id', 'classes', 'style']
        self._type = 'CardMedia'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'image', 'src', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(CardMedia, self).__init__(children=children, **args)
