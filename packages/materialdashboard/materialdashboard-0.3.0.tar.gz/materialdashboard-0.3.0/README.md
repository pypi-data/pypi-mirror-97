# materialdashboard

`materialdashboard` is a Dash component library exposing [Material-UI](https://next.material-ui.com/) components.

Dash components are automatically generated using TypeScript definitions from the source React components.

## Installation

```bash
pip install materialdashboard
```

Although it is not listed in the requirements for this package, you will obviously need [Dash](https://dash.plotly.com/) to include the components in a web app.

## Documentation

Although the component properties should be documented from the extracted TypeScript comments, please refer to the [Material-UI documentation](https://next.material-ui.com/components/box/) for more information about each component.

## Example

This is a one-file example (two if you count the CSS) setting up the app with a top bar, a drawer, and some main content. When building an actual application, you will probably want to organize the code better and split it into several files.

```python
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import materialdashboard as md


DRAWER_WIDTH = "240px"
THEME = {
    "palette": {"primary": {"main": "#ff7043"}, "secondary": {"main": "#9ccc65"}},
    "zIndex": {"appBar": 1300},  # Higher than the drawer.
}


# External stylesheets contain the icons and Roboto font.
app = dash.Dash(__name__, external_stylesheets=md.external_stylesheets, suppress_callback_exceptions=True)


# The ThemeProvider allows you to set some style properties of all its children, like the color palette.
app.layout = md.ThemeProvider(theme=THEME, children=[
    html.Div(children=[
        # As the name suggests, adds a baseline style to the entire application.
        md.CssBaseline(),

        # The bar displayed at the top of Material applications.
        md.AppBar(position="fixed", className="top_bar", children=[
            md.Toolbar(children=[
                md.IconButton(id="menu", edge="start", color="inherit", style={"marginRight": "10px"}, children=[
                    # Only the base Icon component is exposed. Pass the name of the icon you want to display as the
                    # child of this component. Remember to pass the external stylesheets when creating your web app.
                    md.Icon(children="menu"),
                ]),
                # Typography allows you to have a coherent font and size across your app. Remember to pass the external
                # stylesheets when creating your web app.
                md.Typography(variant="h6", children="Title"),
            ]),
        ]),

        # The drawer allowing navigation between the app's pages. The variant used here is `persistent`, meaning the
        # drawer can be toggled and stay visible while using the rest of the app.
        md.Drawer(id="drawer", className="drawer", classes={"paper": "drawer"}, variant="persistent", anchor="left",
                  open=False, children=[
            # An empty toolbar adds the top offset, such that components are not hidden behind the app bar.
            md.Toolbar(),
            md.List(children=[
                md.ListItem(id="first_page", button=True, children=[md.ListItemText(primary="First page")]),
                md.ListItem(id="second_page", button=True, children=[md.ListItemText(primary="Second page")]),
            ]),
        ]),

        # Same as for the drawer.
        md.Toolbar(),

        # The main content of the app. It needs to be padded if the drawer is open.
        html.Main(id="main", style={"flexGrow": 1, "display": "flex"}, children=[
            # The content of the container is added by `drawer_item_click()`.
            md.Container(id="main_container", maxWidth=False, style={"padding": "20px"}),
        ]),
    ]),
])


@app.callback(
    [Output("drawer", "open"), Output("main", "style")],
    [Input("menu", "n_clicks")],
    [State("drawer", "open")]
)
def drawer_button_click(n_clicks, open):
    # Toggles the drawer state.
    new_open = not open
    return (new_open, {"paddingLeft": DRAWER_WIDTH if new_open else "0"})

@app.callback(
    [Output("main_container", "children")],
    [Input("first_page", "n_clicks"), Input("second_page", "n_clicks")],
)
def drawer_item_click(*args):
    # Checks which of the two items was clicked (it could also be none if the app is initializing).
    ctx = dash.callback_context
    if ctx.triggered and ctx.triggered[0]['prop_id'].split('.')[0] == "second_page":
        return [md.Typography(children="Second page")]

    return [
        # Grid is used for both the grid itself (when `container=True`) and child elements (when `item=True`).
        md.Grid(style={"alignContent": "space-around", "alignItems": "center"},
                container=True, spacing=3, children=[
            md.Grid(item=True, md=4, sm=6, children=[
                md.Typography(children=["Welcome to my app!"])
            ]),
            md.Grid(item=True, md=4, sm=6, xs=12, style={"alignContent": "center"}, children=[
                # Like for many other components, you can chose between several button variants. Check the
                # Material-UI documentation for all possible options.
                md.Button(id="my_button", title="Click Me!", color="secondary", children=["Click me!"],
                            variant="contained"),
            ]),
            md.Grid(item=True, md=4, sm=6, xs=12, children=[
                # A multi-function text field that you can turn into a date selector for example. Unfortunately,
                # not all browsers are yet supported.
                md.TextField(id="my_date_field", type="date", value=""),
            ]),
        ]),
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
```

Add this CSS to the `assets` directory of the app:

```css
body {
  margin: 0;
}

.drawer {
  width: 240px;
}
```

## Limitations

### Child nodes

Child nodes are only supported for the `children` property of each component. If Material-UI components expect child components for properties other than `children`, you will not be able to pass a Dash component to them. You can however pass other types. For example, a string is a valid child node.

### Events

Not all events are implemented. Currently, all components support clicks through the `n_clicks` property. If you need an event that's currently missing, please open an issue or a pull request.
