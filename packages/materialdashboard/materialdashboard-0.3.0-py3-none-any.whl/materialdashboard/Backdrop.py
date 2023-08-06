# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Backdrop(Component):
    """A Backdrop component.
Material-UI Backdrop.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The content of the component.
- in (boolean; optional): If `true`, the component will transition in.
- mountOnEnter (boolean; optional): By default the child component is mounted immediately along with the
parent Transition component. If you want to "lazy mount" the component on
the first `in={true}` you can set `mountOnEnter`. After the first enter
transition the component will stay mounted, even on "exited", unless you
also specify `unmountOnExit`.
- unmountOnExit (boolean; optional): By default the child component stays mounted after it reaches the
'exited' state. Set `unmountOnExit` if you'd prefer to unmount the
component after it finishes exiting.
- enter (boolean; optional): Enable or disable enter transitions.
- appear (boolean; optional): Perform the enter transition when it first mounts if `in` is also `true`.
Set this to `false` to disable this behavior.
- exit (boolean; optional): Enable or disable exit transitions.
- open (boolean; optional): If `true`, the component is shown.
- invisible (boolean; optional): If `true`, the backdrop is invisible.
It can be used when rendering a popover or a custom select component.
- className (string; optional)
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- classes (dict; optional): Override or extend the styles applied to the component.
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, mountOnEnter=Component.UNDEFINED, unmountOnExit=Component.UNDEFINED, enter=Component.UNDEFINED, appear=Component.UNDEFINED, exit=Component.UNDEFINED, open=Component.UNDEFINED, invisible=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'in', 'mountOnEnter', 'unmountOnExit', 'enter', 'appear', 'exit', 'open', 'invisible', 'className', 'id', 'classes', 'style']
        self._type = 'Backdrop'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'in', 'mountOnEnter', 'unmountOnExit', 'enter', 'appear', 'exit', 'open', 'invisible', 'className', 'id', 'classes', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Backdrop, self).__init__(children=children, **args)
