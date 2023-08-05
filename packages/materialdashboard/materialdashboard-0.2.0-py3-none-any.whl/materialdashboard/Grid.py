# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Grid(Component):
    """A Grid component.
Material-UI Grid.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The content of the component.
- typography (string; optional): The **`typography`** property  is shorthand for the CSS properties **`font-family`**, **`font-weight`**, **`font-size`**, **`line-height`**, **`letter-spacing`** and **`text-transform``**.
It takes the values defined under `theme.typography` and spreads them on the element.

**Initial value**: `0`

| Chrome | Firefox | Safari |  Edge  |  IE   |
| :----: | :-----: | :----: | :----: | :---: |
| **2**  |  **1**  | **1**  | **12** | **5.5** |
- container (boolean; optional): If `true`, the component will have the flex *container* behavior.
You should be wrapping *items* with a *container*.
- direction (a value equal to: "column", "column-reverse", "row", "row-reverse"; optional): Defines the `flex-direction` style property.
It is applied for all screen sizes.
- item (boolean; optional): If `true`, the component will have the flex *item* behavior.
You should be wrapping *items* with a *container*.
- lg (a value equal to: false, true, "auto", 1, 10, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12; optional): Defines the number of grids the component is going to use.
It's applied for the `lg` breakpoint and wider screens if not overridden.
- md (a value equal to: false, true, "auto", 1, 10, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12; optional): Defines the number of grids the component is going to use.
It's applied for the `md` breakpoint and wider screens if not overridden.
- sm (a value equal to: false, true, "auto", 1, 10, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12; optional): Defines the number of grids the component is going to use.
It's applied for the `sm` breakpoint and wider screens if not overridden.
- spacing (a value equal to: 0, 1, 10, 2, 3, 4, 5, 6, 7, 8, 9; optional): Defines the space between the type `item` component.
It can only be used on a type `container` component.
- wrap (a value equal to: "wrap", "nowrap", "wrap-reverse"; optional): Defines the `flex-wrap` style property.
It's applied for all screen sizes.
- xl (a value equal to: false, true, "auto", 1, 10, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12; optional): Defines the number of grids the component is going to use.
It's applied for the `xl` breakpoint and wider screens.
- xs (a value equal to: false, true, "auto", 1, 10, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12; optional): Defines the number of grids the component is going to use.
It's applied for all the screen sizes with the lowest priority.
- zeroMinWidth (boolean; optional): If `true`, it sets `min-width: 0` on the item.
Refer to the limitations section of the documentation to better understand the use case.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, typography=Component.UNDEFINED, container=Component.UNDEFINED, direction=Component.UNDEFINED, item=Component.UNDEFINED, lg=Component.UNDEFINED, md=Component.UNDEFINED, sm=Component.UNDEFINED, spacing=Component.UNDEFINED, wrap=Component.UNDEFINED, xl=Component.UNDEFINED, xs=Component.UNDEFINED, zeroMinWidth=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'typography', 'container', 'direction', 'item', 'lg', 'md', 'sm', 'spacing', 'wrap', 'xl', 'xs', 'zeroMinWidth', 'className', 'id', 'classes', 'style']
        self._type = 'Grid'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'typography', 'container', 'direction', 'item', 'lg', 'md', 'sm', 'spacing', 'wrap', 'xl', 'xs', 'zeroMinWidth', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Grid, self).__init__(children=children, **args)
