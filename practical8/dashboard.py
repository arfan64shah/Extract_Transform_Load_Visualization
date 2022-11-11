from dash import Dash, html, dcc
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd



app = Dash(__name__)
df = pd.read_excel("dashboard.xlsx")
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


df["Success"] = df.Outcome.apply(success)
df["Failure"] = df.Outcome.apply(failure)


number_of_calls = df.groupby("Date")["Country"].count()
number_of_success_calls = df.groupby("Date")["Success"].sum()
number_of_failure_calls = df.groupby("Date")["Failure"].sum()

ratio_success_overall = number_of_success_calls / number_of_calls * 100

failed_success_timeout = df.groupby("Outcome")["Outcome"].count()

number_of_calls_by_state = df.groupby("State")["Success"].count()
number_of_calls_by_state_success = df.groupby("State")["Success"].sum()


number_of_calls_by_state_ratio = (number_of_calls_by_state_success / number_of_calls_by_state * 100).sort_values(ascending=False)

success_time_out = df[df["Success"] == 1].groupby("Time_Period")["Success"].count().sort_index()

fig = go.Figure()
fig.add_trace(go.Scatter(x=number_of_calls.index, y=number_of_calls.values,
                    mode='lines+markers',
                    name='Overall calls '))
fig.add_trace(go.Scatter(x=number_of_success_calls.index, y=number_of_success_calls.values,
                    mode='lines+markers',
                    name='Number of successful calls'))
fig.add_trace(go.Scatter(x=number_of_failure_calls.index, y=number_of_failure_calls.values,
                    mode='lines+markers', 
                    name='Number of failed calls'))
fig.add_trace(go.Scatter(x=ratio_success_overall.index, y=ratio_success_overall.values,
                    mode='lines+markers', 
                    name='Ratio of successful calls to overall'))
fig["layout"]["title"] =  "Time series and ratio of successful calls"
fig["layout"]["xaxis"]["title"] =  "Date"
fig["layout"]["yaxis"]["title"] = "Number of calls or ratio"
fig["layout"]["legend_title"] = "Options"


fig1 = go.Figure()

fig1.add_trace(go.Bar(x=number_of_success_calls.index, y=number_of_success_calls.values,
                    name='Number of successful calls'))

fig1.add_trace(go.Bar(x=number_of_failure_calls.index, y=number_of_failure_calls.values, 
                    name='Number of failed calls'))

fig1["layout"]["title"] = "Failed/successful calls"
fig1["layout"]["xaxis"]["title"] = "Date"
fig1["layout"]["yaxis"]["title"] = "Number of calls"
fig1["layout"]["legend_title"] = "Options"



fig2 = go.Figure(data=[go.Pie(labels = failed_success_timeout.index, values = failed_success_timeout.values)])
fig2["layout"]["title"] = "Failure/Success/Timeout"
fig2["layout"]["legend_title"] = "Call outcome"


fig3 = go.Figure()

fig3.add_trace(go.Bar(x=number_of_calls_by_state_ratio.index, y=number_of_calls_by_state_ratio.values,
                    name='Number of successful calls'))
fig3["layout"]["title"] = "Most successfull state by success call"
fig3["layout"]["xaxis"]["title"] = "Date"
fig3["layout"]["yaxis"]["title"] = "Ratio of success"
fig3["layout"]["legend_title"] = "Options"


fig4 = make_subplots(rows=1, cols=2, 
    column_widths=[0.5, 0.5],specs=[[{"type": "pie"}, {"type": "pie"}]],
    subplot_titles=("Calls per state", "successfull calls per state"))
fig4.add_trace(row=1, col=1,
    trace=go.Pie(labels=number_of_calls_by_state.index, values=number_of_calls_by_state.values,)) 
fig4.add_trace(row=1, col=2,
    trace=go.Pie(labels=number_of_calls_by_state_success.index, values=number_of_calls_by_state_success.values,))


fig5 = go.Figure()

fig5.add_trace(go.Bar(x=success_time_out.index, y=success_time_out.values,
                    name='Number of successful calls'))



app.layout = html.Div(
    [
        html.H1("Assignment 8"),
        dcc.Graph(figure=fig),
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2),
        dcc.Graph(figure=fig3),
        dcc.Graph(figure=fig4),
        dcc.Graph(figure=fig5),
    ]
)






if __name__ == "__main__":
    app.run_server(debug=True)