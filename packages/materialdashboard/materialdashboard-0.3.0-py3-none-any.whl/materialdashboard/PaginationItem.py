# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class PaginationItem(Component):
    """A PaginationItem component.
Material-UI PaginationItem.

Keyword arguments:
- color (a value equal to: "standard", "primary", "secondary"; optional): The active color.
- disabled (boolean; optional): If `true`, the component is disabled.
- page (number; optional): The current page number.
- selected (boolean; optional): If `true` the pagination item is selected.
- shape (a value equal to: "circular", "rounded"; optional): The shape of the pagination item.
- size (a value equal to: "small", "medium", "large"; optional): The size of the component.
- type (a value equal to: "page", "next", "previous", "first", "last", "start-ellipsis", "end-ellipsis"; optional): The type of pagination item.
- variant (a value equal to: "text", "outlined"; optional): The variant to use.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, color=Component.UNDEFINED, disabled=Component.UNDEFINED, page=Component.UNDEFINED, selected=Component.UNDEFINED, shape=Component.UNDEFINED, size=Component.UNDEFINED, type=Component.UNDEFINED, variant=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['color', 'disabled', 'page', 'selected', 'shape', 'size', 'type', 'variant', 'className', 'id', 'classes', 'style']
        self._type = 'PaginationItem'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['color', 'disabled', 'page', 'selected', 'shape', 'size', 'type', 'variant', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(PaginationItem, self).__init__(**args)
