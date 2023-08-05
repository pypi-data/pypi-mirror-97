# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TablePagination(Component):
    """A TablePagination component.
Material-UI TablePagination.

Keyword arguments:
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
- color (string; optional)
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
- abbr (string; optional)
- variant (a value equal to: "body", "footer", "head"; optional): Specify the cell type.
The prop defaults to the value inherited from the parent TableHead, TableBody, or TableFooter components.
- height (string | number; optional)
- width (string | number; optional)
- padding (a value equal to: "none", "default", "checkbox"; optional): Sets the padding applied to the cell.
The prop defaults to the value (`'default'`) inherited from the parent Table component.
- size (a value equal to: "small", "medium"; optional): Specify the size of the cell.
The prop defaults to the value (`'medium'`) inherited from the parent Table component.
- align (a value equal to: "inherit", "left", "right", "center", "justify"; optional): Set the text-align on the table cell content.

Monetary or generally number fields **should be right aligned** as that allows
you to add them up quickly in your head without having to worry about decimals.
- colSpan (number; optional)
- headers (string; optional)
- rowSpan (number; optional)
- scope (string; optional): Set scope attribute.
- valign (a value equal to: "bottom", "top", "baseline", "middle"; optional)
- sortDirection (a value equal to: false, "desc", "asc"; optional): Set aria-sort direction.
- count (number; optional): The total number of rows.

To enable server side pagination for an unknown number of items, provide -1.
- labelRowsPerPage (boolean | number | string | dict | list; optional): Customize the rows per page label.

For localization purposes, you can use the provided [translations](/guides/localization/).
- page (number; optional): The zero-based index of the current page.
- rowsPerPage (number; optional): The number of rows per page.

Set -1 to display all the rows.
- showFirstButton (boolean; optional): If `true`, show the first-page button.
- showLastButton (boolean; optional): If `true`, show the last-page button.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)
- n_clicks (number; default 0): An integer that represents the number of times that this element has been clicked on."""
    @_explicitize_args
    def __init__(self, className=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, id=Component.UNDEFINED, lang=Component.UNDEFINED, placeholder=Component.UNDEFINED, slot=Component.UNDEFINED, spellCheck=Component.UNDEFINED, tabIndex=Component.UNDEFINED, title=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, role=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, color=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, abbr=Component.UNDEFINED, variant=Component.UNDEFINED, height=Component.UNDEFINED, width=Component.UNDEFINED, padding=Component.UNDEFINED, size=Component.UNDEFINED, align=Component.UNDEFINED, colSpan=Component.UNDEFINED, headers=Component.UNDEFINED, rowSpan=Component.UNDEFINED, scope=Component.UNDEFINED, valign=Component.UNDEFINED, sortDirection=Component.UNDEFINED, count=Component.UNDEFINED, labelRowsPerPage=Component.UNDEFINED, page=Component.UNDEFINED, rowsPerPage=Component.UNDEFINED, showFirstButton=Component.UNDEFINED, showLastButton=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['className', 'defaultChecked', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'accessKey', 'contentEditable', 'contextMenu', 'dir', 'draggable', 'hidden', 'id', 'lang', 'placeholder', 'slot', 'spellCheck', 'tabIndex', 'title', 'translate', 'radioGroup', 'role', 'about', 'datatype', 'inlist', 'prefix', 'property', 'resource', 'typeof', 'vocab', 'autoCapitalize', 'autoCorrect', 'autoSave', 'color', 'itemProp', 'itemScope', 'itemType', 'itemID', 'itemRef', 'results', 'security', 'unselectable', 'inputMode', 'is', 'abbr', 'variant', 'height', 'width', 'padding', 'size', 'align', 'colSpan', 'headers', 'rowSpan', 'scope', 'valign', 'sortDirection', 'count', 'labelRowsPerPage', 'page', 'rowsPerPage', 'showFirstButton', 'showLastButton', 'classes', 'style', 'n_clicks']
        self._type = 'TablePagination'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['className', 'defaultChecked', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'accessKey', 'contentEditable', 'contextMenu', 'dir', 'draggable', 'hidden', 'id', 'lang', 'placeholder', 'slot', 'spellCheck', 'tabIndex', 'title', 'translate', 'radioGroup', 'role', 'about', 'datatype', 'inlist', 'prefix', 'property', 'resource', 'typeof', 'vocab', 'autoCapitalize', 'autoCorrect', 'autoSave', 'color', 'itemProp', 'itemScope', 'itemType', 'itemID', 'itemRef', 'results', 'security', 'unselectable', 'inputMode', 'is', 'abbr', 'variant', 'height', 'width', 'padding', 'size', 'align', 'colSpan', 'headers', 'rowSpan', 'scope', 'valign', 'sortDirection', 'count', 'labelRowsPerPage', 'page', 'rowsPerPage', 'showFirstButton', 'showLastButton', 'classes', 'style', 'n_clicks']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TablePagination, self).__init__(**args)
