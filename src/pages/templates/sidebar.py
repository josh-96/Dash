from dash import html, dcc

def generate_sidebar(pages):
    content = html.Ul(
        id="accordionSidebar",
        className="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion",
        children=[
            html.Hr(className="sidebar-divider my-0"),
            html.Div(
                children=[
                    dcc.Link(
                        className="nav-link",
                        children="Home",
                        href=get_relative_path(pages, "/Home"),
                        style={'color': 'white'}
                    ),
                    dcc.Link(
                        className="nav-link",
                        children="Exploratory Data Analysis",
                        href=get_relative_path(pages, "/ExploratoryDataAnalysis"),
                        style={'color': 'white'}
                    ),
                    dcc.Link(
                        className="nav-link",
                        children="Prediction",
                        href=get_relative_path(pages, "/Prediction"),
                        style={'color': 'white'}
                    ),
                ]
            ),
        ]
    )
    return content

def get_relative_path(pages, path):
    matching_pages = [page["relative_path"] for page in pages if page["path"] == path]
    return matching_pages[0] if matching_pages else "/"
