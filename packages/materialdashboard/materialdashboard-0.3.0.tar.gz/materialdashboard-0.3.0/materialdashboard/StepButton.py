# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class StepButton(Component):
    """A StepButton component.
Material-UI StepButton.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): Can be a `StepLabel` or a node to place inside `StepLabel` as children.


The content of the component.
- href (string; optional)
- icon (boolean | number | string | dict | list; optional): The icon displayed by the step label.
- optional (boolean | number | string | dict | list; optional): The optional node to display.
- tabIndex (string | number; optional)
- centerRipple (boolean; optional): If `true`, the ripples are centered.
They won't start at the cursor interaction position.
- disabled (boolean; optional): If `true`, the component is disabled.
- disableRipple (boolean; optional): If `true`, the ripple effect is disabled.

⚠️ Without a ripple there is no styling for :focus-visible by default. Be sure
to highlight the element by applying separate styles with the `.Mui-focusedVisible` class.
- disableTouchRipple (boolean; optional): If `true`, the touch ripple effect is disabled.
- focusRipple (boolean; optional): If `true`, the base button will have a keyboard focus ripple.
- focusVisibleClassName (string; optional): This prop can help identify which element has keyboard focus.
The class name will be applied when the element gains the focus through keyboard interaction.
It's a polyfill for the [CSS :focus-visible selector](https://drafts.csswg.org/selectors-4/#the-focus-visible-pseudo).
The rationale for using this feature [is explained here](https://github.com/WICG/focus-visible/blob/master/explainer.md).
A [polyfill can be used](https://github.com/WICG/focus-visible) to apply a `focus-visible` class to other components
if needed.
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
- key (string | number; optional)
- download (boolean | number | string | dict | list; optional)
- hrefLang (string; optional)
- media (string; optional)
- ping (string; optional)
- rel (string; optional)
- target (string; optional)
- type (string; optional)
- referrerPolicy (a value equal to: "", "no-referrer", "no-referrer-when-downgrade", "origin", "origin-when-cross-origin", "same-origin", "strict-origin", "strict-origin-when-cross-origin", "unsafe-url"; optional)
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)
- n_clicks (number; default 0): An integer that represents the number of times that this element has been clicked on."""
    @_explicitize_args
    def __init__(self, children=None, href=Component.UNDEFINED, icon=Component.UNDEFINED, optional=Component.UNDEFINED, tabIndex=Component.UNDEFINED, centerRipple=Component.UNDEFINED, disabled=Component.UNDEFINED, disableRipple=Component.UNDEFINED, disableTouchRipple=Component.UNDEFINED, focusRipple=Component.UNDEFINED, focusVisibleClassName=Component.UNDEFINED, className=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, id=Component.UNDEFINED, lang=Component.UNDEFINED, placeholder=Component.UNDEFINED, slot=Component.UNDEFINED, spellCheck=Component.UNDEFINED, title=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, role=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, color=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, key=Component.UNDEFINED, download=Component.UNDEFINED, hrefLang=Component.UNDEFINED, media=Component.UNDEFINED, ping=Component.UNDEFINED, rel=Component.UNDEFINED, target=Component.UNDEFINED, type=Component.UNDEFINED, referrerPolicy=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'href', 'icon', 'optional', 'tabIndex', 'centerRipple', 'disabled', 'disableRipple', 'disableTouchRipple', 'focusRipple', 'focusVisibleClassName', 'className', 'defaultChecked', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'accessKey', 'contentEditable', 'contextMenu', 'dir', 'draggable', 'hidden', 'id', 'lang', 'placeholder', 'slot', 'spellCheck', 'title', 'translate', 'radioGroup', 'role', 'about', 'datatype', 'inlist', 'prefix', 'property', 'resource', 'typeof', 'vocab', 'autoCapitalize', 'autoCorrect', 'autoSave', 'color', 'itemProp', 'itemScope', 'itemType', 'itemID', 'itemRef', 'results', 'security', 'unselectable', 'inputMode', 'is', 'key', 'download', 'hrefLang', 'media', 'ping', 'rel', 'target', 'type', 'referrerPolicy', 'classes', 'style', 'n_clicks']
        self._type = 'StepButton'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'href', 'icon', 'optional', 'tabIndex', 'centerRipple', 'disabled', 'disableRipple', 'disableTouchRipple', 'focusRipple', 'focusVisibleClassName', 'className', 'defaultChecked', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'accessKey', 'contentEditable', 'contextMenu', 'dir', 'draggable', 'hidden', 'id', 'lang', 'placeholder', 'slot', 'spellCheck', 'title', 'translate', 'radioGroup', 'role', 'about', 'datatype', 'inlist', 'prefix', 'property', 'resource', 'typeof', 'vocab', 'autoCapitalize', 'autoCorrect', 'autoSave', 'color', 'itemProp', 'itemScope', 'itemType', 'itemID', 'itemRef', 'results', 'security', 'unselectable', 'inputMode', 'is', 'key', 'download', 'hrefLang', 'media', 'ping', 'rel', 'target', 'type', 'referrerPolicy', 'classes', 'style', 'n_clicks']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(StepButton, self).__init__(children=children, **args)
