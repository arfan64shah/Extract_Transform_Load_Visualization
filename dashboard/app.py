#import required libraries
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#read dataset and make it ready for later use
dataset = pd.read_excel("dashboard.xlsx")

def success(outcome):
    if outcome == "Success":
        return 1
    else:
        return 0
def failure(outcome):
    if outcome == "Failure":
        return 1
    else:
        return 0


dataset["Success"] = dataset.Outcome.apply(success)
dataset["Failure"] = dataset.Outcome.apply(failure)


number_of_calls = dataset.groupby("Date")["Country"].count()
number_of_success_calls = dataset.groupby("Date")["Success"].sum()
number_of_failure_calls = dataset.groupby("Date")["Failure"].sum()

ratio_success_overall = number_of_success_calls / number_of_calls * 100

failed_success_timeout = dataset.groupby("Outcome")["Outcome"].count()

number_of_calls_by_state = dataset.groupby("State")["Success"].count()
number_of_calls_by_state_success = dataset.groupby("State")["Success"].sum()


number_of_calls_by_state_ratio = (number_of_calls_by_state_success / number_of_calls_by_state * 100).sort_values(ascending=False)

success_time_out = dataset[dataset["Success"] == 1].groupby("Time_Period")["Success"].count().sort_index()

#initialize app
server = Flask(__name__)
app = dash.Dash(__name__, server = server, external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
server = app.server

#all the components
header = html.H1("Welcome to the Dashboard", style = {'color': '#808080', 'textAlign': 'center', 'backgroundColor':'lightblue'})

#figure1
figure1 = go.Figure()
figure1.add_trace(go.Scatter(x=number_of_calls.index, y=number_of_calls.values,
                    mode='lines+markers', name='Total calls', marker = {'color' : '#C45AEC'}))
figure1.add_trace(go.Scatter(x=number_of_success_calls.index, y=number_of_success_calls.values,
                    mode='lines+markers',
                    name='Successful calls', marker = {'color' : '#997070'}))
figure1.add_trace(go.Scatter(x=number_of_failure_calls.index, y=number_of_failure_calls.values,
                    mode='lines+markers', 
                    name='Failed calls', marker = {'color' : '#E9AB17'}))
figure1.add_trace(go.Scatter(x=ratio_success_overall.index, y=ratio_success_overall.values,
                    mode='lines+markers', 
                    name='Ratio', marker = {'color' : '#9AFEFF'}))
figure1.update_layout(title = "Ratio and Time Series of Calls")
figure1["layout"]["xaxis"]["title"] = "Date"
figure1["layout"]["yaxis"]["title"] = "Number of calls/Ratio"

#figure2
figure2 = go.Figure()
figure2.add_trace(go.Bar(x=number_of_success_calls.index, y=number_of_success_calls.values,
                    name='Successful calls', marker = {'color' : '#FFA500'}))

figure2.add_trace(go.Bar(x=number_of_failure_calls.index, y=number_of_failure_calls.values, 
                    name='Failed calls', marker = {'color' : '#808000'}))
figure2.update_layout(title = "Successful/Failure calls")
figure2["layout"]["xaxis"]["title"] = "Date"
figure2["layout"]["yaxis"]["title"] = "Number of calls"

#figure3
sunflowers_colors = ['rgb(177, 127, 38)', 'rgb(205, 152, 36)', 'rgb(99, 79, 37)']
figure3 = go.Figure(data=[go.Pie(labels = failed_success_timeout.index, values = failed_success_timeout.values,
                                marker_colors=sunflowers_colors)])
figure3.update_layout(title = "Success and Failure and Timeout")

#figure4
figure4 = go.Figure()
figure4.add_trace(go.Bar(x=number_of_calls_by_state_ratio.index, y=number_of_calls_by_state_ratio.values,
                    name='Successful calls', marker = {'color': '#FFD700'}))
figure4.update_layout(title =  "Most successfull state by success call")
figure4["layout"]["xaxis"]["title"] = "Date"
figure4["layout"]["yaxis"]["title"] = "Success Ratio"

#figure5
figure5 = make_subplots(rows=1, cols=2, 
    column_widths=[0.5, 0.5],specs=[[{"type": "pie"}, {"type": "pie"}]])
figure5.add_trace(row=1, col=1,
    trace=go.Pie(labels=number_of_calls_by_state.index, values=number_of_calls_by_state.values,)) 
figure5.add_trace(row=1, col=2,
    trace=go.Pie(labels=number_of_calls_by_state_success.index, values=number_of_calls_by_state_success.values))
figure5.update_layout(title = "left:calls/state & right:successcalls/state")

#figure6
figure6 = go.Figure()
figure6.add_trace(go.Bar(x=success_time_out.index, y=success_time_out.values, marker = {'color': '#808000'}))
figure6.add_trace(go.Scatter(x=success_time_out.index, y=success_time_out.values, marker = {'color': '#FFD700'}))
figure6.update_layout(title = "Successful calls by Time")
figure6["layout"]["xaxis"]["title"] = "Hourly Time"
figure6["layout"]["yaxis"]["title"] = "Successful Calls"


#layout
app.layout = html.Div([
    dbc.Row([
         header
    ]),
    dbc.Row([
        dbc.Col([dcc.Graph(figure = figure1)]),
        dbc.Col([dcc.Graph(figure = figure2)])
    ]),
    dbc.Row([
        dbc.Col([dcc.Graph(figure = figure3)]),
        dbc.Col([dcc.Graph(figure = figure4)])
    ]),
    dbc.Row([
        dbc.Col([dcc.Graph(figure = figure5)])
    ]),
    dbc.Row([
        dbc.Col([dcc.Graph(figure = figure6)])
    ])
])

#run app
app.run_server()