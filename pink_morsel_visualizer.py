import pandas
from dash import Dash, html, dcc, Input, Output
from plotly.express import line

DATA_PATH = "./formatted_data.csv"
REGION_OPTIONS = ["north", "east", "south", "west", "all"]
DEFAULT_REGION = "north"
COLORS = {
    "primary": "#FEDBFF",
    "secondary": "#D598EB",
    "font": "#522A61",
}


def load_data():
    loaded = pandas.read_csv(DATA_PATH)
    return loaded.sort_values(by="date")


def generate_figure(chart_data):
    line_chart = line(chart_data, x="date", y="sales", title="Pink Morsel Sales")
    line_chart.update_layout(
        plot_bgcolor=COLORS["secondary"],
        paper_bgcolor=COLORS["primary"],
        font_color=COLORS["font"],
    )
    return line_chart


def filter_data_by_region(full_data, region):
    if region == "all":
        return full_data
    return full_data[full_data["region"] == region]


def build_header():
    return html.H1(
        "Pink Morsel Visualizer",
        id="header",
        style={
            "background-color": COLORS["secondary"],
            "color": COLORS["font"],
            "border-radius": "20px",
        },
    )


def build_region_picker():
    picker = dcc.RadioItems(
        REGION_OPTIONS,
        DEFAULT_REGION,
        id="region_picker",
        inline=True,
    )
    return html.Div([picker], style={"font-size": "150%"})


dash_app = Dash(__name__)
data = load_data()
visualization = dcc.Graph(id="visualization", figure=generate_figure(data))
header = build_header()
region_picker_wrapper = build_region_picker()
region_picker = region_picker_wrapper.children[0]


@dash_app.callback(Output(visualization, "figure"), Input(region_picker, "value"))
def update_graph(region):
    trimmed_data = filter_data_by_region(data, region)
    return generate_figure(trimmed_data)


dash_app.layout = html.Div(
    [header, visualization, region_picker_wrapper],
    style={
        "textAlign": "center",
        "background-color": COLORS["primary"],
        "border-radius": "20px",
    },
)

if __name__ == "__main__":
    dash_app.run_server()
