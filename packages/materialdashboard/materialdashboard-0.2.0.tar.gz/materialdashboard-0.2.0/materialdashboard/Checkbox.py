# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Checkbox(Component):
    """A Checkbox component.
Material-UI Checkbox.

Keyword arguments:
- checked (boolean; optional): If `true`, the component is checked.
- checkedIcon (boolean | number | string | dict | list; optional): The icon to display when the component is checked.
- color (a value equal to: "primary", "secondary", "default"; optional): The color of the component. It supports those theme colors that make sense for this component.
- disabled (boolean; optional): If `true`, the component is disabled.
- disableRipple (boolean; optional): If `true`, the ripple effect is disabled.
- icon (boolean | number | string | dict | list; optional): The icon to display when the component is unchecked.
- id (string; optional): The id of the `input` element.
- indeterminate (boolean; optional): If `true`, the component appears indeterminate.
This does not set the native input element to indeterminate due
to inconsistent behavior across browsers.
However, we set a `data-indeterminate` attribute on the `input`.
- indeterminateIcon (boolean | number | string | dict | list; optional): The icon to display when the component is indeterminate.
- required (boolean; optional): If `true`, the `input` element is required.
- size (a value equal to: "small", "medium"; optional): The size of the component.
`small` is equivalent to the dense checkbox styling.
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
- disableTouchRipple (boolean; optional): If `true`, the touch ripple effect is disabled.
- focusRipple (boolean; optional): If `true`, the base button will have a keyboard focus ripple.
- focusVisibleClassName (string; optional): This prop can help identify which element has keyboard focus.
The class name will be applied when the element gains the focus through keyboard interaction.
It's a polyfill for the [CSS :focus-visible selector](https://drafts.csswg.org/selectors-4/#the-focus-visible-pseudo).
The rationale for using this feature [is explained here](https://github.com/WICG/focus-visible/blob/master/explainer.md).
A [polyfill can be used](https://github.com/WICG/focus-visible) to apply a `focus-visible` class to other components
if needed.
- name (string; optional): Name attribute of the `input` element.
- autoFocus (boolean; optional)
- formAction (string; optional)
- formEncType (string; optional)
- formMethod (string; optional)
- formNoValidate (boolean; optional)
- formTarget (string; optional)
- readOnly (boolean; optional)
- disableFocusRipple (boolean; optional): If `true`, the  keyboard focus ripple is disabled.
- edge (a value equal to: false, "end", "start"; optional): If given, uses a negative margin to counteract the padding on one
side (this is often helpful for aligning the left or right
side of the icon with content above or below, without ruining the border
size and shape).
- persistence (boolean | string | number; optional): Used to allow user interactions in this component to be persisted when
 the component - or the page - is refreshed. If `persisted` is truthy and
 hasn't changed from its previous value, a `value` that the user has
 changed while using the app will keep that change, as long as
 the new `value` also matches what was given originally.
Used in conjunction with `persistence_type`.
- persisted_props (list of a value equal to: 'checked's; default ['checked']): Properties whose user interactions will persist after refreshing the
 component or the page. Since only `value` is allowed this prop can
normally be ignored.
- persistence_type (a value equal to: 'local', 'session', 'memory', 'location'; default 'local'): Where persisted user changes will be stored:
 memory: only kept in memory, reset on page refresh.
 local: window.localStorage, data is kept after the browser quit.
 session: window.sessionStorage, data is cleared once the browser quit.
 location: window.location, data appears in the URL and can be shared with others.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)
- n_clicks (number; default 0): An integer that represents the number of times that this element has been clicked on."""
    @_explicitize_args
    def __init__(self, checked=Component.UNDEFINED, checkedIcon=Component.UNDEFINED, color=Component.UNDEFINED, disabled=Component.UNDEFINED, disableRipple=Component.UNDEFINED, icon=Component.UNDEFINED, id=Component.UNDEFINED, indeterminate=Component.UNDEFINED, indeterminateIcon=Component.UNDEFINED, required=Component.UNDEFINED, size=Component.UNDEFINED, value=Component.UNDEFINED, className=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, lang=Component.UNDEFINED, placeholder=Component.UNDEFINED, slot=Component.UNDEFINED, spellCheck=Component.UNDEFINED, tabIndex=Component.UNDEFINED, title=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, role=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, form=Component.UNDEFINED, key=Component.UNDEFINED, centerRipple=Component.UNDEFINED, disableTouchRipple=Component.UNDEFINED, focusRipple=Component.UNDEFINED, focusVisibleClassName=Component.UNDEFINED, name=Component.UNDEFINED, autoFocus=Component.UNDEFINED, formAction=Component.UNDEFINED, formEncType=Component.UNDEFINED, formMethod=Component.UNDEFINED, formNoValidate=Component.UNDEFINED, formTarget=Component.UNDEFINED, readOnly=Component.UNDEFINED, disableFocusRipple=Component.UNDEFINED, edge=Component.UNDEFINED, persistence=Component.UNDEFINED, persisted_props=Component.UNDEFINED, persistence_type=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['checked', 'checkedIcon', 'color', 'disabled', 'disableRipple', 'icon', 'id', 'indeterminate', 'indeterminateIcon', 'required', 'size', 'value', 'className', 'defaultChecked', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'accessKey', 'contentEditable', 'contextMenu', 'dir', 'draggable', 'hidden', 'lang', 'placeholder', 'slot', 'spellCheck', 'tabIndex', 'title', 'translate', 'radioGroup', 'role', 'about', 'datatype', 'inlist', 'prefix', 'property', 'resource', 'typeof', 'vocab', 'autoCapitalize', 'autoCorrect', 'autoSave', 'itemProp', 'itemScope', 'itemType', 'itemID', 'itemRef', 'results', 'security', 'unselectable', 'inputMode', 'is', 'form', 'key', 'centerRipple', 'disableTouchRipple', 'focusRipple', 'focusVisibleClassName', 'name', 'autoFocus', 'formAction', 'formEncType', 'formMethod', 'formNoValidate', 'formTarget', 'readOnly', 'disableFocusRipple', 'edge', 'persistence', 'persisted_props', 'persistence_type', 'classes', 'style', 'n_clicks']
        self._type = 'Checkbox'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['checked', 'checkedIcon', 'color', 'disabled', 'disableRipple', 'icon', 'id', 'indeterminate', 'indeterminateIcon', 'required', 'size', 'value', 'className', 'defaultChecked', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'accessKey', 'contentEditable', 'contextMenu', 'dir', 'draggable', 'hidden', 'lang', 'placeholder', 'slot', 'spellCheck', 'tabIndex', 'title', 'translate', 'radioGroup', 'role', 'about', 'datatype', 'inlist', 'prefix', 'property', 'resource', 'typeof', 'vocab', 'autoCapitalize', 'autoCorrect', 'autoSave', 'itemProp', 'itemScope', 'itemType', 'itemID', 'itemRef', 'results', 'security', 'unselectable', 'inputMode', 'is', 'form', 'key', 'centerRipple', 'disableTouchRipple', 'focusRipple', 'focusVisibleClassName', 'name', 'autoFocus', 'formAction', 'formEncType', 'formMethod', 'formNoValidate', 'formTarget', 'readOnly', 'disableFocusRipple', 'edge', 'persistence', 'persisted_props', 'persistence_type', 'classes', 'style', 'n_clicks']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Checkbox, self).__init__(**args)
