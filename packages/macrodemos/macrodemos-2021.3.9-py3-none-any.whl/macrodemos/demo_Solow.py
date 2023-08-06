
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash_table import DataTable


import webbrowser

from macrodemos.common_components import app_model_parameter, app_table_headers, editable_cell_format, header_cell_format


import numpy as np
import pandas as pd


# Esta parte controla asuntos de estética de la página
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': 'SteelBlue',
    'text': 'White',
    'controls': '#DDDDDD',
    'buttons': 'Orange'
}






class SolowSwan:
    names = dict(
        A='total productivity of factors',
        s='marginal rate of savings',
        α='marginal product of capital',
        δ='depreciation rate',
        n='population growth rate',
        k='Capital Stock (per capita)',
        y='Output per capita',
        sy='Savings per capita',
        c='Consumption per capita',
        Δk='Change in capital stock',
        gy='Output growth rate'
    )

    math_form = dict(
        A=r'$A$',
        s=r'$s$',
        α=r'$\alpha$',
        δ=r'$\delta$',
        n=r'$n$',
        k=r'$k_t$',
        y=r'$y_t$',
        sy=r'$sy_t$',
        c=r'$c_t$',
        Δk=r'$\Delta k_t$',
        gy=r'${g_y}_t$'
    )
    endogenous = ['k','y','sy','c','Δk','gy']


    def __init__(self, A, s, α, δ, n):
        """

        :param A: float, total productivity of factors
        :param s: float, marginal rate of savings
        :param α: float, marginal product of capital
        :param δ: float, depreciation rate
        :param n: float, population growth rate
        """
        self.A = A
        self.s = s
        self.α = α
        self.δ = δ
        self.n = n
        self.data = None
        self.steady_state = dict()
        self.compute_steady_state()

    def parameters(self):
        A, s, α, δ, n = self.A, self.s, self.α, self.δ, self.n
        return dict(A=A, s=s, α=α, δ=δ, n=n)

    def sameparameter(self, param, value):
        return self.__getattribute__(param) if value is None else value

    def f(self, k):
        return self.A * k** self.α

    def compute_steady_state(self):
        A, s, α, δ, n = self.A, self.s, self.α, self.δ, self.n

        k = ((n+δ) / (s*A)) ** (1/(α - 1))
        y = self.f(k)
        i = (n + δ) * k
        c = y - i

        for name, value in zip('ykic', [y,k,i,c]):
            self.steady_state[name] = value

        self.steady_state['Δk'] = 0.0
        self.steady_state['gy'] = 0.0
        self.steady_state['sy'] = s*y

    def shock(self, T, A=None, s=None, α=None, δ=None, n=None):
        A = self.sameparameter('A', A)
        s = self.sameparameter('s', s)
        α = self.sameparameter('α', α)
        δ = self.sameparameter('δ', δ)
        n = self.sameparameter('n', n)

        K, S, Y = np.zeros([3, T+1], dtype=float)
        K[0], S[0], Y[0] = [self.steady_state[var] for var in ['k','sy','y']]

        for t in range(T):
            K[t+1] = ((1 - δ)*K[t] + S[t]) / (1 + n)
            Y[t+1] = A * K[t+1]**α
            S[t+1] = s*Y[t+1]

        datos = pd.DataFrame({'k':K, 'y':Y, 'sy': S})
        datos['c'] = Y - S
        datos['Δk'] = (S - (n+δ)*K) / (1 + n)
        datos.loc[0, 'Δk'] = (S[0] - (self.n + self.δ)*K[0]) / (1 + self.n)
        datos['gy'] = datos['Δk']*datos['k']

        self.data = datos

    def plot_field(self, ser):
        df = self.data[[ser]].rename(columns={ser: 'Alternative'})
        df['Baseline'] = self.steady_state[ser]
        fig = px.line(df,
                      y=df.columns,
                      title=self.names[ser],
                      template='simple_white'
                      )
        fig.update_layout(legend_orientation = 'h',
                          xaxis_title = '',
                          yaxis_title = '')

        fig.add_annotation(x=0.1,
                           y=0.9,
                           xref='paper',
                           yref='paper',
                           showarrow=False,
                           text= self.math_form[ser],
                           font=dict(size=30)
                           )
        return fig



#=======================================================================================================================
#
#  APP STARTS HERE
#
#_______________________________________________________________________________________________________________________
mathjax = ["https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML"]  # to display math
omega = np.linspace(0, np.pi, 121)  # frequencies for spectral plot


app = JupyterDash(__name__,external_stylesheets=external_stylesheets, external_scripts=mathjax)

#======DESIGN THE APP===============

app.layout = html.Div(children=[
    html.H2(id='title',
            children='The Solow-Swan Model',
            style={'textAlign': 'center', 'color': colors['text']}),
    html.Div(children=[html.H4("Parameters"),
                       html.Table(children=[
                           app_table_headers(['  ', 'Baseline', 'Alternative']),
                           app_model_parameter('α', 0.35, 0.35),
                           app_model_parameter('δ', 0.06, 0.06),
                           app_model_parameter('n', 0.02, 0.02)]
                       ),
                       html.Hr(),
                       html.H4("Exogenous variables"),
                       html.Table(children=[
                           app_table_headers(['  ', 'Baseline', 'Alternative']),
                           app_model_parameter('A', 1.0, 1.0),
                           app_model_parameter('s', 0.2, 0.2)]
                       ),
                       html.Hr(),
                       html.H4("Steady state"),
                       html.Div(id='output-data-upload',
                                children=[
                                    DataTable(
                                        id='table-transition-matrix',
                                        columns=([{'id': p, 'name': p} for p in ['Variable', 'Baseline', 'Alternative', '% change']]),
                                        editable=False,
                                        #style_table={'width': '75%'},
                                        style_cell=editable_cell_format,
                                        style_header=header_cell_format
                                    )
                                ],
                                ),
                       html.Hr(),
                       html.H4("Figure parameter"),
                       html.Table(children=[
                           html.Tr([html.Th('Number of periods'), dcc.Input(id='horizon', type='text', value=60, size='10')])]
                       ),
                       html.Button('PLOT', id='execute',style={'textAlign': 'center', 'backgroundColor': colors['buttons']}),
                       html.H5('Solow-Swan-DEMO', style={'textAlign': 'center', 'color': colors['text'],'marginTop':100}),
                       html.P('Based on chapter 9 of Bongers, Gómez and Torres (2019) Introducción a la Macroeconomía Computacional. Vernon Press.',
                              style={'textAlign': 'left', 'color': colors['text'],'marginTop':20}),
                       ],
             style={'textAlign': 'center', 'color': colors['controls'], 'width': '25%', 'display': 'inline-block'}),

    html.Div(style={'width': '75%', 'float': 'right', 'display': 'inline-block'},
             children=[
                 # --PLOT 1a:  capital stock----------------------------------------------------------------------------
                 dcc.Graph(id='plot-capital',
                           style={'width': '49%', 'float': 'left', 'display': 'inline-block'}),
                 #--PLOT 1b:  output per capita ------------------------------------------------------------------------------
                 dcc.Graph(id='plot-output',
                           style={'width': '49%', 'float': 'left', 'display': 'inline-block'}),
                 #--PLOT 1c: savings---------------------------------------------------------------------------
                 dcc.Graph(id='plot-savings',
                           style={'width': '49%', 'float': 'left', 'display': 'inline-block'}),
                 # --PLOT 2a:  consumption----------------------------------------------------------------
                 dcc.Graph(id='plot-consumption',
                           style={'width': '49%', 'float': 'left', 'display': 'inline-block'}),
                 #--PLOT 2b: change in capital--------------------------------------------------------------------------
                 dcc.Graph(id='plot-delta-capital',
                           style={'width': '49%', 'float': 'left', 'display': 'inline-block'}),
                 #--PLOT 2c:  Growth rate -------------------------------------------------------------------------------
                 dcc.Graph(id='plot-growth',
                           style={'width': '49%', 'float': 'left', 'display': 'inline-block'}),
                 # --Link to my website----------------------------------------------------------------
                 html.A(children='Randall Romero Aguilar', href='http://randall-romero.com', style={'textAlign': 'center', 'color': colors['text'],'marginBottom':60}),
             ]),
],
    style={'backgroundColor': colors['background']})


@app.callback(
    [Output('plot-capital', 'figure'),
     Output('plot-output', 'figure'),
     Output('plot-savings', 'figure'),
     Output('plot-consumption', 'figure'),
     Output('plot-delta-capital', 'figure'),
     Output('plot-growth', 'figure'),
     Output('table-transition-matrix', 'data')
     ],
    [Input('execute', 'n_clicks')],
    [State('horizon','value'),
     State('base_α', 'value'),
     State('base_δ', 'value'),
     State('base_n', 'value'),
     State('base_A', 'value'),
     State('base_s', 'value'),
     State('scen_α', 'value'),
     State('scen_δ', 'value'),
     State('scen_n', 'value'),
     State('scen_A', 'value'),
     State('scen_s', 'value')])
def update_ARMA_parameters(n_clicks,T, α, δ, n, A, s, α1, δ1, n1, A1, s1):
    modelo = SolowSwan(*[float(xx) for xx in (A, s, α, δ, n)])
    modelo.shock(int(T), *[float(xx) for xx in [A1, s1, α1, δ1, n1]])

    modelo1= SolowSwan(*[float(xx) for xx in (A1, s1, α1, δ1, n1)])
    df = pd.DataFrame({'Baseline': [v for v in modelo.steady_state.values()],
                      'Alternative': [v for v in modelo1.steady_state.values()]},
                      index=modelo.steady_state.keys()
                      )
    df['% change'] = 100 * (df['Alternative'] / df['Baseline'] - 1)
    df = df.round(3).loc[modelo.endogenous]
    df.index.name = 'Variable'
    return [modelo.plot_field(ser) for ser in modelo.endogenous].append(df.reset_index().to_dict('records'))



def Solow_demo(colab=False):
    if colab:
        app.run_server(mode='external')
    else:
        webbrowser.open('http://127.0.0.1:8050/')
        app.run_server(debug=False)

if __name__ == '__main__':
    Solow_demo()