# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Autocomplete(Component):
    """An Autocomplete component.
Material-UI Autocomplete.

Keyword arguments:
- clearIcon (boolean | number | string | dict | list; optional): The icon to display in place of the default clear icon.
- clearText (string; optional): Override the default text for the *clear* icon button.

For localization purposes, you can use the provided [translations](/guides/localization/).
- closeText (string; optional): Override the default text for the *close popup* icon button.

For localization purposes, you can use the provided [translations](/guides/localization/).
- disabled (boolean; optional): If `true`, the component is disabled.
- disablePortal (boolean; optional): If `true`, the `Popper` content will be under the DOM hierarchy of the parent component.
- forcePopupIcon (a value equal to: false, true, "auto"; optional): Force the visibility display of the popup icon.
- fullWidth (boolean; optional): If `true`, the input will take up the full width of its container.
- loading (boolean; optional): If `true`, the component is in a loading state.
- loadingText (boolean | number | string | dict | list; optional): Text to display when in a loading state.

For localization purposes, you can use the provided [translations](/guides/localization/).
- limitTags (number; optional): The maximum number of tags that will be visible when not focused.
Set `-1` to disable the limit.
- noOptionsText (boolean | number | string | dict | list; optional): Text to display when there are no options.

For localization purposes, you can use the provided [translations](/guides/localization/).
- openText (string; optional): Override the default text for the *open popup* icon button.

For localization purposes, you can use the provided [translations](/guides/localization/).
- popupIcon (boolean | number | string | dict | list; optional): The icon to display in place of the default popup icon.
- size (a value equal to: "small", "medium"; optional): The size of the component.
- autoComplete (boolean; optional): If `true`, the portion of the selected suggestion that has not been typed by the user,
known as the completion string, appears inline after the input cursor in the textbox.
The inline completion string is visually highlighted and has a selected state.
- autoHighlight (boolean; optional): If `true`, the first option is automatically highlighted.
- autoSelect (boolean; optional): If `true`, the selected option becomes the value of the input
when the Autocomplete loses focus unless the user chooses
a different option or changes the character string in the input.
- blurOnSelect (a value equal to: false, true, "mouse", "touch"; optional): Control if the input should be blurred when an option is selected:

- `false` the input is not blurred.
- `true` the input is always blurred.
- `touch` the input is blurred after a touch event.
- `mouse` the input is blurred after a mouse event.
- clearOnBlur (boolean; optional): If `true`, the input's text is cleared on blur if no value is selected.

Set to `true` if you want to help the user enter a new value.
Set to `false` if you want to help the user resume his search.
- clearOnEscape (boolean; optional): If `true`, clear all values when the user presses escape and the popup is closed.
- componentName (string; optional): The component name that is using this hook. Used for warnings.
- disableCloseOnSelect (boolean; optional): If `true`, the popup won't close when a value is selected.
- disabledItemsFocusable (boolean; optional): If `true`, will allow focus on disabled items.
- disableListWrap (boolean; optional): If `true`, the list box in the popup will not wrap focus.
- filterSelectedOptions (boolean; optional): If `true`, hide the selected options from the list box.
- handleHomeEndKeys (boolean; optional): If `true`, the component handles the "Home" and "End" keys when the popup is open.
It should move focus to the first option and last option, respectively.
- id (string; optional): This prop is used to help implement the accessibility logic.
If you don't provide this prop. It falls back to a randomly generated id.
- includeInputInList (boolean; optional): If `true`, the highlight can move to the input.
- inputValue (string; optional): The input value.
- open (boolean; optional): If `true`, the component is shown.
- openOnFocus (boolean; optional): If `true`, the popup will open on input focus.
- selectOnFocus (boolean; optional): If `true`, the input's text is selected on focus.
It helps the user clear the selected value.
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
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)
- n_clicks (number; default 0): An integer that represents the number of times that this element has been clicked on."""
    @_explicitize_args
    def __init__(self, clearIcon=Component.UNDEFINED, clearText=Component.UNDEFINED, closeText=Component.UNDEFINED, disabled=Component.UNDEFINED, disablePortal=Component.UNDEFINED, forcePopupIcon=Component.UNDEFINED, fullWidth=Component.UNDEFINED, loading=Component.UNDEFINED, loadingText=Component.UNDEFINED, limitTags=Component.UNDEFINED, noOptionsText=Component.UNDEFINED, openText=Component.UNDEFINED, popupIcon=Component.UNDEFINED, size=Component.UNDEFINED, autoComplete=Component.UNDEFINED, autoHighlight=Component.UNDEFINED, autoSelect=Component.UNDEFINED, blurOnSelect=Component.UNDEFINED, clearOnBlur=Component.UNDEFINED, clearOnEscape=Component.UNDEFINED, componentName=Component.UNDEFINED, disableCloseOnSelect=Component.UNDEFINED, disabledItemsFocusable=Component.UNDEFINED, disableListWrap=Component.UNDEFINED, filterSelectedOptions=Component.UNDEFINED, handleHomeEndKeys=Component.UNDEFINED, id=Component.UNDEFINED, includeInputInList=Component.UNDEFINED, inputValue=Component.UNDEFINED, open=Component.UNDEFINED, openOnFocus=Component.UNDEFINED, selectOnFocus=Component.UNDEFINED, className=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, lang=Component.UNDEFINED, placeholder=Component.UNDEFINED, slot=Component.UNDEFINED, spellCheck=Component.UNDEFINED, tabIndex=Component.UNDEFINED, title=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, role=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, color=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['clearIcon', 'clearText', 'closeText', 'disabled', 'disablePortal', 'forcePopupIcon', 'fullWidth', 'loading', 'loadingText', 'limitTags', 'noOptionsText', 'openText', 'popupIcon', 'size', 'autoComplete', 'autoHighlight', 'autoSelect', 'blurOnSelect', 'clearOnBlur', 'clearOnEscape', 'componentName', 'disableCloseOnSelect', 'disabledItemsFocusable', 'disableListWrap', 'filterSelectedOptions', 'handleHomeEndKeys', 'id', 'includeInputInList', 'inputValue', 'open', 'openOnFocus', 'selectOnFocus', 'className', 'defaultChecked', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'accessKey', 'contentEditable', 'contextMenu', 'dir', 'draggable', 'hidden', 'lang', 'placeholder', 'slot', 'spellCheck', 'tabIndex', 'title', 'translate', 'radioGroup', 'role', 'about', 'datatype', 'inlist', 'prefix', 'property', 'resource', 'typeof', 'vocab', 'autoCapitalize', 'autoCorrect', 'autoSave', 'color', 'itemProp', 'itemScope', 'itemType', 'itemID', 'itemRef', 'results', 'security', 'unselectable', 'inputMode', 'is', 'classes', 'style', 'n_clicks']
        self._type = 'Autocomplete'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['clearIcon', 'clearText', 'closeText', 'disabled', 'disablePortal', 'forcePopupIcon', 'fullWidth', 'loading', 'loadingText', 'limitTags', 'noOptionsText', 'openText', 'popupIcon', 'size', 'autoComplete', 'autoHighlight', 'autoSelect', 'blurOnSelect', 'clearOnBlur', 'clearOnEscape', 'componentName', 'disableCloseOnSelect', 'disabledItemsFocusable', 'disableListWrap', 'filterSelectedOptions', 'handleHomeEndKeys', 'id', 'includeInputInList', 'inputValue', 'open', 'openOnFocus', 'selectOnFocus', 'className', 'defaultChecked', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'accessKey', 'contentEditable', 'contextMenu', 'dir', 'draggable', 'hidden', 'lang', 'placeholder', 'slot', 'spellCheck', 'tabIndex', 'title', 'translate', 'radioGroup', 'role', 'about', 'datatype', 'inlist', 'prefix', 'property', 'resource', 'typeof', 'vocab', 'autoCapitalize', 'autoCorrect', 'autoSave', 'color', 'itemProp', 'itemScope', 'itemType', 'itemID', 'itemRef', 'results', 'security', 'unselectable', 'inputMode', 'is', 'classes', 'style', 'n_clicks']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Autocomplete, self).__init__(**args)
