import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/gumdropsteve/intro_to_python/main/day_09/data/titanic.csv').dropna()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#e2e2e2',
    'text': 'blue'
}


fig2 = px.bar(df, x="Survived", y=df.Fare.astype('int64'), color="Sex",barmode="group")

fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig3 = px.pie(df, values='Fare', names='Survived', title='Total Fare based on Survived')

pass_sum1=df.groupby(['Pclass']).Survived.sum()
fig4 = px.bar(pass_sum1, barmode='group', title='Survived Passengers Count based on Pclass')

fig4.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div([ 
    html.H1(
        children='Titanic Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='Pclass-slider',
        min=df['Pclass'].min(),
        max=df['Pclass'].max(),
        value=df['Pclass'].min(),
        marks={str(Pclass): str(Pclass) for Pclass in df['Pclass'].unique()},
        step=None
    ),    

    html.Div(children='Dash: Relationship between Fare and Survived by Sex', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure=fig2
    ),

    
    dcc.Graph(
        id='example-graph-3',
        figure=fig3
    ),
    
    dcc.Graph(
        id='example-graph-4',
        figure=fig4
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('Pclass-slider', 'value'))


def update_figure(selected_Pclass):
    filtered_df = df[df.Pclass == selected_Pclass]

    fig = px.scatter(filtered_df, x="Age", y="Fare",
                     color="Embarked"
                     )

    fig.update_layout(transition_duration=500)

    return fig
    

if __name__ == '__main__':
    app.run_server(debug=True)