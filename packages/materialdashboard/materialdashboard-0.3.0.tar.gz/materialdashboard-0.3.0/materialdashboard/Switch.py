# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Switch(Component):
    """A Switch component.
Material-UI Switch.

Keyword arguments:
- checkedIcon (boolean | number | string | dict | list; optional): The icon to display when the component is checked.
- color (a value equal to: "primary", "secondary", "default"; optional): The color of the component. It supports those theme colors that make sense for this component.
- disabled (boolean; optional): If `true`, the component is disabled.
- icon (boolean | number | string | dict | list; optional): The icon to display when the component is unchecked.
- size (a value equal to: "small", "medium"; optional): The size of the component.
`small` is equivalent to the dense switch styling.
- value (boolean | number | string | dict | list; optional): The value of the component. The DOM API casts this to a string.
The browser uses "on" as the default value.
- className (string; optional)
- defaultChecked (boolean; optional): The default checked state. Use when the component is not controlled.
- suppressContentEditableWarning (boolean; optional)
- suppressHydrationWarning (boolean; optional)
- accessKey (string; optional)
- contentEditable (a value equal to: false, true, "true", "false", "inherit"; optional)
- contextMenu (string; optional)
- dir (string; optional)
- draggable (a value equal to: false, true, "true", "false"; optional)
- hidden (boolean; optional)
- id (string; optional): The id of the `input` element.
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
- form (string; optional)
- key (string | number; optional)
- centerRipple (boolean; optional): If `true`, the ripples are centered.
They won't start at the cursor interaction position.
- disableRipple (boolean; optional): If `true`, the ripple effect is disabled.
- disableTouchRipple (boolean; optional): If `true`, the touch ripple effect is disabled.
- focusRipple (boolean; optional): If `true`, the base button will have a keyboard focus ripple.
- focusVisibleClassName (string; optional): This prop can help identify which element has keyboard focus.
The class name will be applied when the element gains the focus through keyboard interaction.
It's a polyfill for the [CSS :focus-visible selector](https://drafts.csswg.org/selectors-4/#the-focus-visible-pseudo).
The rationale for using this feature [is explained here](https://github.com/WICG/focus-visible/blob/master/explainer.md).
A [polyfill can be used](https://github.com/WICG/focus-visible) to apply a `focus-visible` class to other components
if needed.
- type (string; optional)
- name (string; optional): Name attribute of the `input` element.
- autoFocus (boolean; optional)
- formAction (string; optional)
- formEncType (string; optional)
- formMethod (string; optional)
- formNoValidate (boolean; optional)
- formTarget (string; optional)
- checked (boolean; optional): If `true`, the component is checked.
- readOnly (boolean; optional)
- required (boolean; optional): If `true`, the `input` element is required.
- disableFocusRipple (boolean; optional): If `true`, the  keyboard focus ripple is disabled.
- edge (a value equal to: false, "end", "start"; optional): If given, uses a negative margin to counteract the padding on one
side (this is often helpful for aligning the left or right
side of the icon with content above or below, without ruining the border
size and shape).
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)
- n_clicks (number; default 0): An integer that represents the number of times that this element has been clicked on."""
    @_explicitize_args
    def __init__(self, checkedIcon=Component.UNDEFINED, color=Component.UNDEFINED, disabled=Component.UNDEFINED, icon=Component.UNDEFINED, size=Component.UNDEFINED, value=Component.UNDEFINED, className=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, id=Component.UNDEFINED, lang=Component.UNDEFINED, placeholder=Component.UNDEFINED, slot=Component.UNDEFINED, spellCheck=Component.UNDEFINED, tabIndex=Component.UNDEFINED, title=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, role=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, form=Component.UNDEFINED, key=Component.UNDEFINED, centerRipple=Component.UNDEFINED, disableRipple=Component.UNDEFINED, disableTouchRipple=Component.UNDEFINED, focusRipple=Component.UNDEFINED, focusVisibleClassName=Component.UNDEFINED, type=Component.UNDEFINED, name=Component.UNDEFINED, autoFocus=Component.UNDEFINED, formAction=Component.UNDEFINED, formEncType=Component.UNDEFINED, formMethod=Component.UNDEFINED, formNoValidate=Component.UNDEFINED, formTarget=Component.UNDEFINED, checked=Component.UNDEFINED, readOnly=Component.UNDEFINED, required=Component.UNDEFINED, disableFocusRipple=Component.UNDEFINED, edge=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['checkedIcon', 'color', 'disabled', 'icon', 'size', 'value', 'className', 'defaultChecked', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'accessKey', 'contentEditable', 'contextMenu', 'dir', 'draggable', 'hidden', 'id', 'lang', 'placeholder', 'slot', 'spellCheck', 'tabIndex', 'title', 'translate', 'radioGroup', 'role', 'about', 'datatype', 'inlist', 'prefix', 'property', 'resource', 'typeof', 'vocab', 'autoCapitalize', 'autoCorrect', 'autoSave', 'itemProp', 'itemScope', 'itemType', 'itemID', 'itemRef', 'results', 'security', 'unselectable', 'inputMode', 'is', 'form', 'key', 'centerRipple', 'disableRipple', 'disableTouchRipple', 'focusRipple', 'focusVisibleClassName', 'type', 'name', 'autoFocus', 'formAction', 'formEncType', 'formMethod', 'formNoValidate', 'formTarget', 'checked', 'readOnly', 'required', 'disableFocusRipple', 'edge', 'classes', 'style', 'n_clicks']
        self._type = 'Switch'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['checkedIcon', 'color', 'disabled', 'icon', 'size', 'value', 'className', 'defaultChecked', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'accessKey', 'contentEditable', 'contextMenu', 'dir', 'draggable', 'hidden', 'id', 'lang', 'placeholder', 'slot', 'spellCheck', 'tabIndex', 'title', 'translate', 'radioGroup', 'role', 'about', 'datatype', 'inlist', 'prefix', 'property', 'resource', 'typeof', 'vocab', 'autoCapitalize', 'autoCorrect', 'autoSave', 'itemProp', 'itemScope', 'itemType', 'itemID', 'itemRef', 'results', 'security', 'unselectable', 'inputMode', 'is', 'form', 'key', 'centerRipple', 'disableRipple', 'disableTouchRipple', 'focusRipple', 'focusVisibleClassName', 'type', 'name', 'autoFocus', 'formAction', 'formEncType', 'formMethod', 'formNoValidate', 'formTarget', 'checked', 'readOnly', 'required', 'disableFocusRipple', 'edge', 'classes', 'style', 'n_clicks']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Switch, self).__init__(**args)
