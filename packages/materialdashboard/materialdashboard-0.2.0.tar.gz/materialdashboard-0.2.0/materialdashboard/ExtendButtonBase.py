# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ExtendButtonBase(Component):
    """An ExtendButtonBase component.
Material-UI ExtendButtonBase.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The content of the component.
- href (string; optional)
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
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, href=Component.UNDEFINED, tabIndex=Component.UNDEFINED, centerRipple=Component.UNDEFINED, disabled=Component.UNDEFINED, disableRipple=Component.UNDEFINED, disableTouchRipple=Component.UNDEFINED, focusRipple=Component.UNDEFINED, focusVisibleClassName=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'href', 'tabIndex', 'centerRipple', 'disabled', 'disableRipple', 'disableTouchRipple', 'focusRipple', 'focusVisibleClassName', 'className', 'id', 'classes', 'style']
        self._type = 'ExtendButtonBase'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'href', 'tabIndex', 'centerRipple', 'disabled', 'disableRipple', 'disableTouchRipple', 'focusRipple', 'focusVisibleClassName', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ExtendButtonBase, self).__init__(children=children, **args)
