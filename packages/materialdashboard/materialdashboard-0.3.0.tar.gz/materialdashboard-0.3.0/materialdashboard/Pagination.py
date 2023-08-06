# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Pagination(Component):
    """A Pagination component.
Material-UI Pagination.

Keyword arguments:
- color (a value equal to: "standard", "primary", "secondary"; optional): The active color.
- shape (a value equal to: "circular", "rounded"; optional): The shape of the pagination items.
- size (a value equal to: "small", "medium", "large"; optional): The size of the component.
- variant (a value equal to: "text", "outlined"; optional): The variant to use.
- boundaryCount (number; optional): Number of always visible pages at the beginning and end.
- componentName (string; optional): The name of the component where this hook is used.
- count (number; optional): The total number of pages.
- defaultPage (number; optional): The page selected by default when the component is uncontrolled.
- disabled (boolean; optional): If `true`, the component is disabled.
- hideNextButton (boolean; optional): If `true`, hide the next-page button.
- hidePrevButton (boolean; optional): If `true`, hide the previous-page button.
- page (number; optional): The current page.
- showFirstButton (boolean; optional): If `true`, show the first-page button.
- showLastButton (boolean; optional): If `true`, show the last-page button.
- siblingCount (number; optional): Number of always visible pages before and after the current page.
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
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)
- n_clicks (number; default 0): An integer that represents the number of times that this element has been clicked on."""
    @_explicitize_args
    def __init__(self, color=Component.UNDEFINED, shape=Component.UNDEFINED, size=Component.UNDEFINED, variant=Component.UNDEFINED, boundaryCount=Component.UNDEFINED, componentName=Component.UNDEFINED, count=Component.UNDEFINED, defaultPage=Component.UNDEFINED, disabled=Component.UNDEFINED, hideNextButton=Component.UNDEFINED, hidePrevButton=Component.UNDEFINED, page=Component.UNDEFINED, showFirstButton=Component.UNDEFINED, showLastButton=Component.UNDEFINED, siblingCount=Component.UNDEFINED, className=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, id=Component.UNDEFINED, lang=Component.UNDEFINED, placeholder=Component.UNDEFINED, slot=Component.UNDEFINED, spellCheck=Component.UNDEFINED, tabIndex=Component.UNDEFINED, title=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, role=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['color', 'shape', 'size', 'variant', 'boundaryCount', 'componentName', 'count', 'defaultPage', 'disabled', 'hideNextButton', 'hidePrevButton', 'page', 'showFirstButton', 'showLastButton', 'siblingCount', 'className', 'defaultChecked', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'accessKey', 'contentEditable', 'contextMenu', 'dir', 'draggable', 'hidden', 'id', 'lang', 'placeholder', 'slot', 'spellCheck', 'tabIndex', 'title', 'translate', 'radioGroup', 'role', 'about', 'datatype', 'inlist', 'prefix', 'property', 'resource', 'typeof', 'vocab', 'autoCapitalize', 'autoCorrect', 'autoSave', 'itemProp', 'itemScope', 'itemType', 'itemID', 'itemRef', 'results', 'security', 'unselectable', 'inputMode', 'is', 'classes', 'style', 'n_clicks']
        self._type = 'Pagination'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['color', 'shape', 'size', 'variant', 'boundaryCount', 'componentName', 'count', 'defaultPage', 'disabled', 'hideNextButton', 'hidePrevButton', 'page', 'showFirstButton', 'showLastButton', 'siblingCount', 'className', 'defaultChecked', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'accessKey', 'contentEditable', 'contextMenu', 'dir', 'draggable', 'hidden', 'id', 'lang', 'placeholder', 'slot', 'spellCheck', 'tabIndex', 'title', 'translate', 'radioGroup', 'role', 'about', 'datatype', 'inlist', 'prefix', 'property', 'resource', 'typeof', 'vocab', 'autoCapitalize', 'autoCorrect', 'autoSave', 'itemProp', 'itemScope', 'itemType', 'itemID', 'itemRef', 'results', 'security', 'unselectable', 'inputMode', 'is', 'classes', 'style', 'n_clicks']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Pagination, self).__init__(**args)
