# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DialogContentText(Component):
    """A DialogContentText component.
Material-UI DialogContentText.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The content of the component.
- variant (a value equal to: "button", "caption", "h1", "h2", "h3", "h4", "h5", "h6", "inherit", "subtitle1", "subtitle2", "body1", "body2", "overline"; optional): Applies the theme typography styles.
- typography (string; optional): The **`typography`** property  is shorthand for the CSS properties **`font-family`**, **`font-weight`**, **`font-size`**, **`line-height`**, **`letter-spacing`** and **`text-transform``**.
It takes the values defined under `theme.typography` and spreads them on the element.

**Initial value**: `0`

| Chrome | Firefox | Safari |  Edge  |  IE   |
| :----: | :-----: | :----: | :----: | :---: |
| **2**  |  **1**  | **1**  | **12** | **5.5** |
- align (a value equal to: "inherit", "left", "right", "center", "justify"; optional): Set the text-align on the component.
- gutterBottom (boolean; optional): If `true`, the text will have a bottom margin.
- noWrap (boolean; optional): If `true`, the text will not wrap, but instead will truncate with a text overflow ellipsis.

Note that text overflow can only happen with block or inline-block level elements
(the element needs to have a width in order to overflow).
- paragraph (boolean; optional): If `true`, the text will have a bottom margin.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, variant=Component.UNDEFINED, typography=Component.UNDEFINED, align=Component.UNDEFINED, gutterBottom=Component.UNDEFINED, noWrap=Component.UNDEFINED, paragraph=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'variant', 'typography', 'align', 'gutterBottom', 'noWrap', 'paragraph', 'className', 'id', 'classes', 'style']
        self._type = 'DialogContentText'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'variant', 'typography', 'align', 'gutterBottom', 'noWrap', 'paragraph', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DialogContentText, self).__init__(children=children, **args)
