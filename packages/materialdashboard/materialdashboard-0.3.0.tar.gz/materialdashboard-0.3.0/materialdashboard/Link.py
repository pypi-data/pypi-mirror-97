# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Link(Component):
    """A Link component.
Material-UI Link.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The content of the component.
- className (string; optional)
- defaultChecked (boolean; optional)
- suppressContentEditableWarning (boolean; optional)
- suppressHydrationWarning (boolean; optional)
- accessKey (string; optional)
- contentEditable (a value equal to: false, true, "true", "false", "inherit"; optional)
- contextMenu (string; optional)
- dir (string; optional)
- draggable (a value equal to: false, true, "true", "false"; optional)
- hidden (boolean; optional)
- id (string; optional)
- lang (string; optional)
- placeholder (string; optional)
- slot (string; optional)
- spellCheck (a value equal to: false, true, "true", "false"; optional)
- tabIndex (number; optional)
- title (string; optional)
- translate (a value equal to: "yes", "no"; optional)
- radioGroup (string; optional)
- role (string; optional)
- about (string; optional)
- datatype (string; optional)
- inlist (boolean | number | string | dict | list; optional)
- prefix (string; optional)
- property (string; optional)
- resource (string; optional)
- typeof (string; optional)
- vocab (string; optional)
- autoCapitalize (string; optional)
- autoCorrect (string; optional)
- autoSave (string; optional)
- itemProp (string; optional)
- itemScope (boolean; optional)
- itemType (string; optional)
- itemID (string; optional)
- itemRef (string; optional)
- results (number; optional)
- security (string; optional)
- unselectable (a value equal to: "on", "off"; optional)
- inputMode (a value equal to: "text", "none", "tel", "url", "email", "numeric", "decimal", "search"; optional): Hints at the type of data that might be entered by the user while editing the element or its contents
- is (string; optional): Specify that a standard HTML element should behave like a defined custom built-in element
- download (boolean | number | string | dict | list; optional)
- href (string; optional)
- hrefLang (string; optional)
- media (string; optional)
- ping (string; optional)
- rel (string; optional)
- target (string; optional)
- type (string; optional)
- referrerPolicy (a value equal to: "", "no-referrer", "no-referrer-when-downgrade", "origin", "origin-when-cross-origin", "same-origin", "strict-origin", "strict-origin-when-cross-origin", "unsafe-url"; optional)
- key (string | number; optional)
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
- underline (a value equal to: "none", "hover", "always"; optional): Controls when the link should have an underline.
- variant (a value equal to: "button", "caption", "h1", "h2", "h3", "h4", "h5", "h6", "inherit", "subtitle1", "subtitle2", "body1", "body2", "overline"; optional): Applies the theme typography styles.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)
- n_clicks (number; default 0): An integer that represents the number of times that this element has been clicked on."""
    @_explicitize_args
    def __init__(self, children=None, className=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, id=Component.UNDEFINED, lang=Component.UNDEFINED, placeholder=Component.UNDEFINED, slot=Component.UNDEFINED, spellCheck=Component.UNDEFINED, tabIndex=Component.UNDEFINED, title=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, role=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, download=Component.UNDEFINED, href=Component.UNDEFINED, hrefLang=Component.UNDEFINED, media=Component.UNDEFINED, ping=Component.UNDEFINED, rel=Component.UNDEFINED, target=Component.UNDEFINED, type=Component.UNDEFINED, referrerPolicy=Component.UNDEFINED, key=Component.UNDEFINED, typography=Component.UNDEFINED, align=Component.UNDEFINED, gutterBottom=Component.UNDEFINED, noWrap=Component.UNDEFINED, paragraph=Component.UNDEFINED, underline=Component.UNDEFINED, variant=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'className', 'defaultChecked', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'accessKey', 'contentEditable', 'contextMenu', 'dir', 'draggable', 'hidden', 'id', 'lang', 'placeholder', 'slot', 'spellCheck', 'tabIndex', 'title', 'translate', 'radioGroup', 'role', 'about', 'datatype', 'inlist', 'prefix', 'property', 'resource', 'typeof', 'vocab', 'autoCapitalize', 'autoCorrect', 'autoSave', 'itemProp', 'itemScope', 'itemType', 'itemID', 'itemRef', 'results', 'security', 'unselectable', 'inputMode', 'is', 'download', 'href', 'hrefLang', 'media', 'ping', 'rel', 'target', 'type', 'referrerPolicy', 'key', 'typography', 'align', 'gutterBottom', 'noWrap', 'paragraph', 'underline', 'variant', 'classes', 'style', 'n_clicks']
        self._type = 'Link'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'className', 'defaultChecked', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'accessKey', 'contentEditable', 'contextMenu', 'dir', 'draggable', 'hidden', 'id', 'lang', 'placeholder', 'slot', 'spellCheck', 'tabIndex', 'title', 'translate', 'radioGroup', 'role', 'about', 'datatype', 'inlist', 'prefix', 'property', 'resource', 'typeof', 'vocab', 'autoCapitalize', 'autoCorrect', 'autoSave', 'itemProp', 'itemScope', 'itemType', 'itemID', 'itemRef', 'results', 'security', 'unselectable', 'inputMode', 'is', 'download', 'href', 'hrefLang', 'media', 'ping', 'rel', 'target', 'type', 'referrerPolicy', 'key', 'typography', 'align', 'gutterBottom', 'noWrap', 'paragraph', 'underline', 'variant', 'classes', 'style', 'n_clicks']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Link, self).__init__(children=children, **args)
