# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Table(Component):
    """A Table component.
Material-UI Table.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The content of the table, normally `TableHead` and `TableBody`.
- padding (a value equal to: "none", "default", "checkbox"; optional): Allows TableCells to inherit padding of the Table.
- size (a value equal to: "small", "medium"; optional): Allows TableCells to inherit size of the Table.
- stickyHeader (boolean; optional): Set the header sticky.

⚠️ It doesn't work with IE11.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, padding=Component.UNDEFINED, size=Component.UNDEFINED, stickyHeader=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'padding', 'size', 'stickyHeader', 'className', 'id', 'classes', 'style']
        self._type = 'Table'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'padding', 'size', 'stickyHeader', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Table, self).__init__(children=children, **args)
