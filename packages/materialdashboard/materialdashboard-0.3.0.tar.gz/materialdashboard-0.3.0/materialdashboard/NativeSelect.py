# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class NativeSelect(Component):
    """A NativeSelect component.
Material-UI NativeSelect.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The option elements to populate the select with.
Can be some `<option>` elements.
- value (boolean | number | string | dict | list; optional): The `input` value. The DOM API casts this to a string.
- variant (a value equal to: "outlined", "standard", "filled"; optional): The variant to use.
- className (string; optional)
- defaultChecked (boolean; optional)
- defaultValue (boolean | number | string | dict | list; optional): The default value. Use when the component is not controlled.
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
- placeholder (string; optional): The short hint displayed in the `input` before the user enters a value.
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
- color (a value equal to: "primary", "secondary"; optional): The color of the component. It supports those theme colors that make sense for this component.
The prop defaults to the value (`'primary'`) inherited from the parent FormControl component.
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
- margin (a value equal to: "none", "dense"; optional): If `dense`, will adjust vertical spacing. This is normally obtained via context from
FormControl.
The prop defaults to the value (`'none'`) inherited from the parent FormControl component.
- disabled (boolean; optional): If `true`, the component is disabled.
The prop defaults to the value (`false`) inherited from the parent FormControl component.
- type (string; optional): Type of the `input` element. It should be [a valid HTML5 input type](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#Form_%3Cinput%3E_types).
- error (boolean; optional): If `true`, the `input` will indicate an error.
The prop defaults to the value (`false`) inherited from the parent FormControl component.
- size (a value equal to: "small", "medium"; optional): The size of the component.
- name (string; optional): Name attribute of the `input` element.
- autoFocus (boolean; optional): If `true`, the `input` element is focused during the first mount.
- autoComplete (string; optional): This prop helps users to fill forms faster, especially on mobile devices.
The name can be confusing, as it's more like an autofill.
You can learn more about it [following the specification](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#autofill).
- readOnly (boolean; optional): It prevents the user from changing the value of the field
(not from interacting with the field).
- required (boolean; optional): If `true`, the `input` element is required.
The prop defaults to the value (`false`) inherited from the parent FormControl component.
- rows (string | number; optional): Number of rows to display when multiline option is set to true.
- fullWidth (boolean; optional): If `true`, the `input` will take up the full width of its container.
- endAdornment (boolean | number | string | dict | list; optional): End `InputAdornment` for this component.
- multiline (boolean; optional): If `true`, a `textarea` element is rendered.
- maxRows (string | number; optional): Maximum number of rows to display when multiline option is set to true.
- minRows (string | number; optional): Minimum number of rows to display when multiline option is set to true.
- startAdornment (boolean | number | string | dict | list; optional): Start `InputAdornment` for this component.
- disableUnderline (boolean; optional): If `true`, the `input` will not have an underline.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)
- n_clicks (number; default 0): An integer that represents the number of times that this element has been clicked on."""
    @_explicitize_args
    def __init__(self, children=None, value=Component.UNDEFINED, variant=Component.UNDEFINED, className=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, defaultValue=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, id=Component.UNDEFINED, lang=Component.UNDEFINED, placeholder=Component.UNDEFINED, slot=Component.UNDEFINED, spellCheck=Component.UNDEFINED, tabIndex=Component.UNDEFINED, title=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, role=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, color=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, margin=Component.UNDEFINED, disabled=Component.UNDEFINED, type=Component.UNDEFINED, error=Component.UNDEFINED, size=Component.UNDEFINED, name=Component.UNDEFINED, autoFocus=Component.UNDEFINED, autoComplete=Component.UNDEFINED, readOnly=Component.UNDEFINED, required=Component.UNDEFINED, rows=Component.UNDEFINED, fullWidth=Component.UNDEFINED, endAdornment=Component.UNDEFINED, multiline=Component.UNDEFINED, maxRows=Component.UNDEFINED, minRows=Component.UNDEFINED, startAdornment=Component.UNDEFINED, disableUnderline=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'value', 'variant', 'className', 'defaultChecked', 'defaultValue', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'accessKey', 'contentEditable', 'contextMenu', 'dir', 'draggable', 'hidden', 'id', 'lang', 'placeholder', 'slot', 'spellCheck', 'tabIndex', 'title', 'translate', 'radioGroup', 'role', 'about', 'datatype', 'inlist', 'prefix', 'property', 'resource', 'typeof', 'vocab', 'autoCapitalize', 'autoCorrect', 'autoSave', 'color', 'itemProp', 'itemScope', 'itemType', 'itemID', 'itemRef', 'results', 'security', 'unselectable', 'inputMode', 'is', 'margin', 'disabled', 'type', 'error', 'size', 'name', 'autoFocus', 'autoComplete', 'readOnly', 'required', 'rows', 'fullWidth', 'endAdornment', 'multiline', 'maxRows', 'minRows', 'startAdornment', 'disableUnderline', 'classes', 'style', 'n_clicks']
        self._type = 'NativeSelect'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'value', 'variant', 'className', 'defaultChecked', 'defaultValue', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'accessKey', 'contentEditable', 'contextMenu', 'dir', 'draggable', 'hidden', 'id', 'lang', 'placeholder', 'slot', 'spellCheck', 'tabIndex', 'title', 'translate', 'radioGroup', 'role', 'about', 'datatype', 'inlist', 'prefix', 'property', 'resource', 'typeof', 'vocab', 'autoCapitalize', 'autoCorrect', 'autoSave', 'color', 'itemProp', 'itemScope', 'itemType', 'itemID', 'itemRef', 'results', 'security', 'unselectable', 'inputMode', 'is', 'margin', 'disabled', 'type', 'error', 'size', 'name', 'autoFocus', 'autoComplete', 'readOnly', 'required', 'rows', 'fullWidth', 'endAdornment', 'multiline', 'maxRows', 'minRows', 'startAdornment', 'disableUnderline', 'classes', 'style', 'n_clicks']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(NativeSelect, self).__init__(children=children, **args)
