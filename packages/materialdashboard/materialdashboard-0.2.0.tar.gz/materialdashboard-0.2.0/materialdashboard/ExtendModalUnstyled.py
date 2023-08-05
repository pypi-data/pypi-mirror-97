# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ExtendModalUnstyled(Component):
    """An ExtendModalUnstyled component.
Material-UI ExtendModalUnstyled.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): A single child content element.
- closeAfterTransition (boolean; optional): When set to true the Modal waits until a nested Transition is completed before closing.
- disableAutoFocus (boolean; optional): If `true`, the modal will not automatically shift focus to itself when it opens, and
replace it to the last focused element when it closes.
This also works correctly with any modal children that have the `disableAutoFocus` prop.

Generally this should never be set to `true` as it makes the modal less
accessible to assistive technologies, like screen readers.
- disableEnforceFocus (boolean; optional): If `true`, the modal will not prevent focus from leaving the modal while open.

Generally this should never be set to `true` as it makes the modal less
accessible to assistive technologies, like screen readers.
- disableEscapeKeyDown (boolean; optional): If `true`, hitting escape will not fire the `onClose` callback.
- disablePortal (boolean; optional): The `children` will be under the DOM hierarchy of the parent component.
- disableRestoreFocus (boolean; optional): If `true`, the modal will not restore focus to previously focused element once
modal is hidden.
- disableScrollLock (boolean; optional): Disable the scroll lock behavior.
- hideBackdrop (boolean; optional): If `true`, the backdrop is not rendered.
- keepMounted (boolean; optional): Always keep the children in the DOM.
This prop can be useful in SEO situation or
when you want to maximize the responsiveness of the Modal.
- open (boolean; optional): If `true`, the component is shown.
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component."""
    @_explicitize_args
    def __init__(self, children=None, closeAfterTransition=Component.UNDEFINED, disableAutoFocus=Component.UNDEFINED, disableEnforceFocus=Component.UNDEFINED, disableEscapeKeyDown=Component.UNDEFINED, disablePortal=Component.UNDEFINED, disableRestoreFocus=Component.UNDEFINED, disableScrollLock=Component.UNDEFINED, hideBackdrop=Component.UNDEFINED, keepMounted=Component.UNDEFINED, open=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'closeAfterTransition', 'disableAutoFocus', 'disableEnforceFocus', 'disableEscapeKeyDown', 'disablePortal', 'disableRestoreFocus', 'disableScrollLock', 'hideBackdrop', 'keepMounted', 'open', 'id', 'classes']
        self._type = 'ExtendModalUnstyled'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'closeAfterTransition', 'disableAutoFocus', 'disableEnforceFocus', 'disableEscapeKeyDown', 'disablePortal', 'disableRestoreFocus', 'disableScrollLock', 'hideBackdrop', 'keepMounted', 'open', 'id', 'classes']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ExtendModalUnstyled, self).__init__(children=children, **args)
