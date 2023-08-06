import json
import time
from typing import List

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL, MATCH
from jupyter_dash import JupyterDash
from pyngrok import ngrok

from .utils import convert_to_md


def answer_component(
    n,
    source=None,
    retrieved_answer="Answer will appear here...",
    rating=None,
    generated_feedback="Answer will appear here...",
):
    answer_card = dbc.Card(
        [
            dbc.CardHeader(f"Retrieved Answer #{n}"),
            dbc.Spinner(
                dbc.CardBody(
                    [
                        html.H4(
                            source,
                            id={"name": "title-answer", "index": n},
                            className="card-title",
                        ),
                        dbc.Collapse(
                            dcc.Markdown(
                                retrieved_answer,
                                id={"name": "markdown-preview", "index": n},
                            ),
                            id={"name": "collapse-preview", "index": n},
                            is_open=True,
                        ),
                        dbc.Collapse(
                            dcc.Markdown(
                                retrieved_answer,
                                id={"name": "markdown-answer", "index": n},
                            ),
                            id={"name": "collapse-answer", "index": n},
                            is_open=False,
                        ),
                        dbc.Button(
                            "Show More",
                            id={"name": "show-more-btn", "index": n},
                            className="mb-3",
                            color="primary",
                        ),
                    ],
                    className="card-text",
                )
            ),
        ],
        color="primary",
        outline=True,
        style={"height": "100%"},
    )

    feedback_card = dbc.Card(
        [
            dbc.CardHeader(f"Generated Explanation #{n}"),
            dbc.Spinner(
                dbc.CardBody(
                    [
                        html.H4(
                            rating,
                            id={"name": "title-feedback", "index": n},
                            className="card-title",
                        ),
                        dcc.Markdown(
                            generated_feedback,
                            id={"name": "markdown-feedback", "index": n},
                        ),
                    ],
                    className="card-text",
                )
            ),
        ],
        color="info",
        outline=True,
        style={"height": "100%"},
    )

    return dbc.Row(
        [
            dbc.Col(answer_card, width=7),
            dbc.Col(feedback_card, width=5),
        ],
        style={"padding-top": "15px", "padding-bottom": "15px"},
    )


def layout(sample_questions: List[str]) -> dbc.Container:
    navbar = dbc.NavbarSimple(
        [
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="# Answers",
                children=[
                    dbc.DropdownMenuItem(
                        f"{i} answers", id={"type": "n-answers", "index": i}
                    )
                    for i in range(2, 11)
                ],
            ),
        ],
        color="primary",
        dark=True,
        brand="❓ FeedbackQA System",
    )

    search_bar = dbc.InputGroup(
        [
            # dbc.DropdownMenu(
            #     label="Examples",
            #     color="info",
            #     children=[
            #         dbc.DropdownMenuItem(p[:80] + "...", id={"type": "preset", "index": i})
            #         for i, p in enumerate(sample_questions)
            #     ],
            #     addon_type="prepend"
            # ),
            dbc.Input(id="search-bar", placeholder="Ask your question here..."),
            dbc.InputGroupAddon(
                dbc.Button("🔍 Search", id="search-button", color="primary"),
                addon_type="append",
            ),
            dbc.InputGroupAddon(
                dbc.Button("✘ Clear", id="clear-button", color="danger"),
                addon_type="append",
            ),
        ]
    )

    return dbc.Container(
        [
            navbar,
            html.Br(),
            dcc.Dropdown(
                options=[{"label": x, "value": x} for x in sample_questions],
                placeholder="Select a sample question...",
                id="preset",
            ),
            html.Br(),
            search_bar,
            html.Br(),
            html.Div([answer_component(n) for n in range(1, 3)], id="answers"),
            dcc.Store(id="n-answers-store", data=2),
        ],
        fluid=False,
    )


def assign_callbacks(app, system, sample_questions: List[str]) -> None:
    @app.callback(
        Output({"name": "collapse-preview", "index": MATCH}, "is_open"),
        Output({"name": "collapse-answer", "index": MATCH}, "is_open"),
        Output({"name": "show-more-btn", "index": MATCH}, "children"),
        Input({"name": "show-more-btn", "index": MATCH}, "n_clicks"),
    )
    def toggle_collapse(n):
        if not n:
            return [dash.no_update] * 3

        return n % 2 == 0, n % 2 != 0, "Show more" if n % 2 == 0 else "Show less"

    @app.callback(Output("answers", "children"), Input("n-answers-store", "data"))
    def change_n_cards(n):
        return [answer_component(n) for n in range(1, n + 1)]

    @app.callback(
        Output("n-answers-store", "data"),
        Input({"type": "n-answers", "index": ALL}, "n_clicks"),
    )
    def update_n_answers_store(n_clicks):
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update

        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        ix = json.loads(prop_id)["index"]
        return ix

    @app.callback(
        Output("search-bar", "value"),
        Output("search-button", "n_clicks"),
        Input("clear-button", "n_clicks"),
        # Input({"type": "preset", "index": ALL}, "n_clicks"),
        Input("preset", "value"),
        State("search-button", "n_clicks"),
    )
    def clear_search(n_clicks, preset, search_n_clicks):
        if search_n_clicks is None:
            search_n_clicks = 0

        ctx = dash.callback_context

        if not ctx.triggered:
            return "", dash.no_update

        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "clear-button":
            return "", dash.no_update

        # selected_dict = json.loads(prop_id)
        # idx = selected_dict["index"]
        # return sample_questions[idx], search_n_clicks + 1
        return preset, search_n_clicks + 1

    @app.callback(
        Output({"name": "show-more-btn", "index": ALL}, "disabled"),
        Output({"name": "markdown-preview", "index": ALL}, "children"),
        Output({"name": "markdown-answer", "index": ALL}, "children"),
        Output({"name": "markdown-feedback", "index": ALL}, "children"),
        Output({"name": "title-answer", "index": ALL}, "children"),
        Output({"name": "title-feedback", "index": ALL}, "children"),
        Input("search-button", "n_clicks"),
        Input("search-bar", "n_submit"),
        State("search-bar", "value"),
        State("n-answers-store", "data"),
    )
    def run_search_and_feedback(n_clicks, n_submit, query, n_answers):
        if n_answers is None:
            n_answers = 2
        if not query:
            return [[dash.no_update] * n_answers] * 6

        time.sleep(0.75)

        best_passages = system.retrieve(query)[:n_answers]
        best_passages_md = [convert_to_md(p["content_html"]) for p in best_passages]
        best_passages_content = [
            p["content"] for p in best_passages
        ]  # TODO: change this

        ratings = system.rate(query, best_passages_content)
        feedback = system.give_feedback(query, best_passages_content)

        return [
            [len(c) <= 500 for c in best_passages_md],  # show-more-btn disabled
            [
                c[:500] + "..." if len(c) > 500 else c for c in best_passages_md
            ],  # md-preview
            best_passages_md,  # md-answer
            feedback,  # md-feedback
            [f"Source: {p['source']}" for p in best_passages],  # title-answer
            [f"Rating: {r}" for r in ratings],  # title-feedback
        ]


def build(system, sample_questions: List[str], platform: str = "local", **kwargs):
    platform = platform.lower()

    stylesheets = [dbc.themes.YETI]

    if platform == "local":
        app = dash.Dash(__name__, external_stylesheets=stylesheets)

    elif platform == "colab":
        app = JupyterDash(__name__, external_stylesheets=stylesheets)

    elif platform == 'kaggle':
        port = kwargs.get('port', 8050)
        tunnel = ngrok.connect(port)
        app = JupyterDash(__name__, external_stylesheets=stylesheets, server_url=tunnel.public_url)
        warning = (
            "When using kaggle, it is recommend to run app.run_server(mode='inline'). Otherwise, you might run into ngrok issues."
        )
        print(warning)
    app.layout = layout(sample_questions)
    assign_callbacks(app, system, sample_questions)

    return app, app.server


def start(system, sample_questions: List[str], platform: str = "local", **kwargs):
    app = build(system, sample_questions, platform, **kwargs)
    app.run_server(**kwargs)
