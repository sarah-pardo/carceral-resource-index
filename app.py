import os
import plotly.express as px
import plotly.graph_objects as go
import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from whitenoise import WhiteNoise


# 'https://git.heroku.com/carceral-resource-index.git'
# Load Data
#city_spending includes: City,CRI,State,Year,FY Year,Spending Type,Dollar Amount,Category, Total Spending
city_spending = pd.read_csv('city_spending_all_years.csv').drop(['Unnamed: 0'],axis=1)
# need to make new csv file with 'Year' already as type string
city_spending['Year'] = city_spending['Year'].astype(str)

city_list = ["Albuquerque", "Arlington", "Atlanta", "Austin", "Bakersfield",
             "Baltimore", "Boston", "Charlotte", "Chicago", "Colorado Springs",
             "Columbus", "Dallas", "Denver", "Detroit", "El Paso", "Fort Worth",
             "Fresno", "Houston", "Indianapolis", "Jacksonville", "Kansas City",
             "Las Vegas", "Long Beach", "Los Angeles", "Louisville", "Memphis",
             "Mesa", "Miami", "Milwaukee", "Minneapolis", "Nashville", "Nassau-Suffolk",
             "New Orleans", "New York", "Newark", "Oakland", "Oklahoma City", "Omaha",
             "Philadelphia", "Phoenix", "Portland", "Raleigh", "Sacramento",
             "San Antonio", "San Diego", "San Francisco", "San Jose", "Seattle",
             "Tucson", "Tulsa", "Virginia Beach", "Washington, D.C.", "Wichita"]
region_dct = {'Mesa': 'Southwest', 'Phoenix': 'Southwest', 'Tucson': 'Southwest', 'Bakersfield': 'Pacific',
              'Fresno': 'Pacific', 'Long Beach': 'Pacific', 'Los Angeles': 'Pacific', 'Oakland': 'Pacific',
              'Sacramento': 'Pacific', 'San Diego': 'Pacific', 'San Francisco': 'Pacific',
              'San Jose': 'Pacific', 'Colorado Springs': 'Rocky Mountains', 'Denver': 'Rocky Mountains',
              'Jacksonville': 'Southeast', 'Miami': 'Southeast', 'Atlanta': 'Southeast', 'Chicago': 'Midwest',
              'Indianapolis': 'Midwest', 'Wichita': 'Midwest', 'Louisville': 'Southeast',
              'New Orleans': 'Southeast', 'Baltimore': 'Midatlantic', 'Boston': 'Northeast',
              'Detroit': 'Midwest', 'Minneapolis': 'Midwest', 'Kansas City': 'Southeast',
              'Omaha': 'Midwest', 'Las Vegas': 'Rocky Mountains', 'Newark': 'Midatlantic',
              'Albuquerque': 'Southwest', 'Nassau-Suffolk': 'Northeast', 'New York': 'Northeast',
              'Charlotte': 'Southeast', 'Raleigh': 'Southeast', 'Columbus': 'Midwest',
              'Oklahoma City': 'Southwest', 'Tulsa': 'Southwest', 'Portland': 'Pacific',
              'Philadelphia': 'Northeast', 'Memphis': 'Southeast', 'Nashville': 'Southeast',
              'Arlington': 'Southwest', 'Austin': 'Southwest', 'Dallas': 'Southwest',
              'El Paso': 'Southwest', 'Fort Worth': 'Southwest', 'Houston': 'Southwest',
              'San Antonio': 'Southwest', 'Virginia Beach': 'Southeast', 'Seattle': 'Pacific',
              'Milwaukee': 'Midwest', 'Washington, D.C.': 'Midatlantic'}
city_groupby = city_spending.groupby(['City'])
region_groupby = city_spending.groupby(['Region'])

police_spending = city_spending[(city_spending['Spending Type'] == 'Police') & (city_spending['Year'] =='2020')]
police_spending=police_spending.sort_values('Dollar Amount').reset_index().drop(['index'],axis=1)
similar_cri = city_groupby.first().sort_values('CRI').reset_index()

# TULSA
tulsa_df = city_groupby.get_group('Tulsa')
tulsa_df2020 = tulsa_df[tulsa_df['Year']=='2020'].reset_index()
tulsaTOTAL = tulsa_df2020.at[0,'Total Spending']
tulsaCRI2020 = tulsa_df2020.at[0,'CRI']

#Dollar amounts for Tulsa if CRI is 0
C0 = (tulsaTOTAL*(0-1))/-2
H0 = tulsaTOTAL - C0
tulsa_cri_0 = {'Category':['Carceral','Health and Support'],
              'Key':['Your Guess','Your Guess'],
            'Dollar Amount':[C0,H0]}

guessFig0 = px.bar(tulsa_cri_0,
                 x='Category',
                 y='Dollar Amount',
                 color='Category',
                 color_discrete_sequence=["darkblue","lightgreen"],
                 text='Dollar Amount',
                 title='Spending for Tulsa with CRI = 0') #, Your Estimate
guessFig0.update_traces(texttemplate='%{text:.5s}')

#Dollar amounts for Tulsa if CRI is -0.5
C5 = (tulsaTOTAL*(-0.5-1))/-2
H5 = tulsaTOTAL - C5
tulsa_cri_5 = {'Category':['Carceral','Health and Support'],
              'Key':['Your Guess','Your Guess'],
            'Dollar Amount':[C5,H5]}

guessFig5 = px.bar(tulsa_cri_5,
                 x='Category',
                 y='Dollar Amount',
                 color='Category',
                 color_discrete_sequence=["darkblue","lightgreen"],
                 text='Dollar Amount',
                 title='Spending for Tulsa with CRI = -0.5') #, Your Estimate
guessFig5.update_traces(texttemplate='%{text:.5s}')

#Dollar amounts for Tulsa if CRI is +0.75
C75 = (tulsaTOTAL*(0.75-1))/-2
H75 = tulsaTOTAL - C75
tulsa_cri_75 = {'Category':['Carceral','Health and Support'],
              'Key':['Your Guess','Your Guess'],
            'Dollar Amount':[C75,H75]}

guessFig75 = px.bar(tulsa_cri_75,
                 x='Category',
                 y='Dollar Amount',
                 color='Category',
                 color_discrete_sequence=["darkblue","lightgreen"],
                 text='Dollar Amount',
                 title='Spending for Tulsa with CRI = 0.75') #, Your Estimate
guessFig75.update_traces(texttemplate='%{text:.5s}')

# Answer fig for Tulsa
preDctTulsa = tulsa_df2020.groupby('Category').sum()['Dollar Amount'].to_dict()
postDctTulsa ={
          'Category':['Carceral','Health and Support'],
          'Key':['Correct Answer','Correct Answer'],
          'Dollar Amount':[preDctTulsa['Carceral'],preDctTulsa['Health and Support']]
         }
postDfTulsa = pd.DataFrame.from_dict(postDctTulsa)

compareTulsa = pd.DataFrame.from_dict(tulsa_cri_75).append(postDfTulsa)
    # make guess color key darkblue and answer color lightgreen
answerFig58 = px.bar(compareTulsa,
                 x='Category',
                 y='Dollar Amount',
                 color='Key',
                 color_discrete_sequence=['lightgreen','darkblue'],
                 barmode='group',
                 text='Dollar Amount',
                 title='Guess of CRI = 0.75 versus actual CRI = -0.58')
answerFig58.update_traces(texttemplate='%{text:.2s}')

# Build App
external_stylesheets = [dbc.themes.BOOTSTRAP]
#"https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css", integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T", crossorigin="anonymous"]
#'https://codepen.io/chriddyp/pen/bWLwgP.css',"https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
server = app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/')
            # Container for all layout
app.title = "Carceral Resource Index"
app.layout = html.Div(
        #children in container
        children=[
            #div for the top of the page (intro)
            html.Div([
                # Row, column for title
                dbc.Row(dbc.Col(
                        # Div for title
                        html.Div(html.H3("How well do you know your city's spending priorities?"),
                            className='app-header-title'),
                        width={'size':8}),justify='center'
                       ),
                # row, column for intro par
                dbc.Row(dbc.Col(
                        html.P([
                            html.Span('''We are in the midst of a nationwide debate rethinking how to achieve public safety
                                and also promote public health, equity, and justice. If “money talks,” then budgets tell a story
                                about a community’s priorities. We at the Health in Justice Action Lab have created the Carceral
                                Resource Index (CRI) to represent in a single number a city's spending on'''),
                            html.Span(''' carceral systems''',style={"font-weight": "bold"}),
                            html.Span(''' (e.g. Community Supervision, Corrections, Courts, Police,
                                Prosecutors, Public Defenders, and Sheriff departments)''',style={"font-style": "italic"}),
                            html.Span(''' versus '''),
                            html.Span('''health and support systems''',style={"font-weight": "bold"}),
                            html.Span(''' (e.g. Health and Human Services, Parks and Recreation, Public Health,
                                Arts and Culture, Civic and Community Engagement, Employment, Housing).''',style={"font-style": "italic"}),
                            html.Span(''' The index may be used to benchmark one city's relative spending against
                                another's. Below we explain how to read the index and ask you to guess your own city's CRI value.
                                ''')
                                 ]),width=8),
                        justify='center'
                       ),],className='introDiv'),
                html.Div([
                    dbc.Row(dbc.Col(
                            # Div for title
                            html.Div(html.H3("Carceral Resource Index Walkthrough"),
                                className='app-header-title'),
                            ),justify='center'
                           ),
                    dbc.Row(dbc.Col(html.P('''To understand the Carceral Resource Index tool, let's take a look at Tulsa, Oklahoma.
                                            ''',style={'font-size':'20px','padding-bottom':'25px'}),),justify='center'),
                    dbc.Row(dbc.Col(html.P(["Tulsa spends ${:,} on carceral systems and health and supportive services combined.".format(tulsaTOTAL)],
                                    style={'font-size':'18px',}),),justify='center'),
                    dbc.Row([
                            html.Div(dbc.Col([
                                dbc.Row(html.P("Ex. 1",style={'font-size':'22px'}),justify='center'),
                                dbc.Row(html.P('''A CRI value of 0 would mean Tulsa spends equal amounts (about $66 million each) on carceral
                                                systems and health and support services:''' ),justify='center'),
                                dbc.Row(html.Img(src='/CRI0.png',height='200px'),justify='center'),
                                dbc.Row(dcc.Graph(figure=guessFig0,style={'max-width':'100%','min-width':'100%'}),justify='center',)],
                                width=12
                            ),className='example'),
                            html.Div(dbc.Col([
                                dbc.Row(html.P("Ex. 2",style={'font-size':'22px'}),justify='center'),
                                dbc.Row(html.P('''A CRI value of -0.5 would mean Tulsa spends about $100 million (75%)
                                                 on carceral systems and about $33 million (25%) health and support systems:'''),justify='center'),
                                dbc.Row(html.Img(src='/CRIneg05.png',height='200px'),justify='center'),
                                dbc.Row(dcc.Graph(figure=guessFig5,style={'max-width':'100%','min-width':'100%'}),justify='center')],
                                width=12
                            ),className='example'),
                        ],justify='center'),
                    dbc.Row([
                            html.Div(dbc.Col([
                                dbc.Row(html.P("Ex. 3 (Guess)",style={'font-size':'22px'}),justify='center'),
                                dbc.Row(html.P('''Let's say we guess that Tulsa has a CRI value of 0.75, meaning we think the city spends about $116 million or about 88% on Health and Support services
                                                and about $16 million or 12% on carceral systems.''' ),justify='center'),
                                dbc.Row(html.Img(src='/CRIpos75.png',height='200px'),justify='center'),
                                dbc.Row(dcc.Graph(figure=guessFig75,style={'max-width':'100%','min-width':'100%'}),justify='center',)],
                                width=12
                            ),className='example'),
                            html.Div(dbc.Col([
                                dbc.Row(html.P("Ex. 3 (Answer)",style={'font-size':'22px'}),justify='center'),
                                dbc.Row(html.P('''This estimate would be quite inaccurate, as shown in the chart below. Tulsa actually has a CRI -0.58, which means our guess underestimated
                                carceral spending and overestimated health spending by a large margin.'''),justify='center'),
                                dbc.Row(html.Img(src='/tulsa_cri_answer.png',height='200px'),justify='center'),
                                dbc.Row(dcc.Graph(figure=answerFig58,style={'max-width':'100%','min-width':'100%'}),justify='center')],
                                width=12
                            ),className='example'),
                        ],justify='center'),
                    dbc.Row(dbc.Col(html.P('''For easier conversion, this number line shows the relationship between CRI and percent values:
                                            ''',style={'font-size':'20px','padding-top':'15px'}),width={'size':8,'offset':0}),justify='center'),
                    dbc.Row(dbc.Col(html.Img(src='/CRIKey.png',width='60%',style={'border-bottom':'none'})),justify='center'),

                ],className='walkthrough'),

                html.Div([
                    # row for drop down, label of drop down
                    dbc.Row(dbc.Col(html.P('''Now that you understand how the CRI index relates to spending, pick from the 50 most populous
                                            cities in the United States and estimate its CRI value. We'll tell you how close you were.'''),width=8,id='guesser-description'),justify='center'),
                    dbc.Row(id='select-container',
                            children=[
                                dbc.Col(html.H5("Select Your City:"),width=2),
                                dbc.Col(dcc.Dropdown(
                                        id='city-dropdown', clearable=False,
                                        value='Boston', options=[
                                            {'label': c, 'value': c}
                                            for c in city_list
                                            ]),width=3),
                                ],justify="center"
                           ),
                    # Store info
                    dcc.Store('city-df-store'),
                    dcc.Store('city-df2020-store'),
                    dcc.Store('total-store'),
                    dcc.Store('cri-store'),
                    # 4 Header explaining the slider, amount in city budget
                            # 2 another Div containing a paragraph and multiple tooltips for certain words
                    html.Div(dbc.Row(dbc.Col([ # 2.0
                            html.Div(html.P(
                                [
                                    "The total spending on ",
                                    html.Span(
                                        "carceral",
                                        id="tooltip-carc-target",
                                        style={"font-weight": "bold", "cursor": "pointer"},
                                    ),
                                    " and ",
                                    html.Span(
                                        "health and support",
                                        id="tooltip-health-target",
                                        style={"font-weight": "bold", "cursor": "pointer"},
                                    ),
                                    " in ",
                                    html.Span(id='total-spending'),
                                ]),className='app-total-budget-par'),
                            # 2.1
                            dbc.Tooltip(
                                " Community Supervision, Corrections, Courts, Police, Prosecutors, Public Defenders, Sheriff ",
                                target="tooltip-carc-target", #style={"background-color": "#ffcc99"}
                            ),
                            # 2.2
                            dbc.Tooltip(
                                ''' Health and Human Services (HHS), Parks and Recreation, Public Health,
                                 Arts and Culture, Civic and Community Engagement, Employment, Housing ''',
                                target="tooltip-health-target",#style={"background-color": "#99ccff"}
                            ),
                        ],width={'size':8}),justify="center")),
                    #dbc.Row(dbc.Col(html.P('''If Imaginary City had a CRI of 0.25, that would mean it spends $375,000 on carceral systems and $625,000 on health and support systems.'''),width={'size':8}),justify="center"),
                    html.Div([
                        dbc.Row(dbc.Col(html.Div(id='slider-drag-output', style={'margin-bottom':'20px'}),
                                         width=8),justify='center'),
                        dbc.Row(dbc.Col(html.Div(id='real-output', style={'display':'none'}),
                                         width=8),justify='center'),
                        dbc.Row(dbc.Col(html.Div(id='answer-percent-output'),
                                          width=8),justify='center')
                        ],className='app-estimate-answer'),
                    html.Div(id='post-guess',children=[
                        html.Div(id='javascript'),
                        dbc.Row([
                            dbc.Col(html.A(dbc.Button('Try another city', style={'width':'150px'},id='try-another-button'),href="/"),width={'size':1,'offset':0},style={'margin-bottom':'75px'}),
                            ],justify="center"
                            )],
                        style={'display':'none'},className='tryagainbutton'),
                    dbc.Row([
                        #dbc.Col(html.P('-1')),
                        dbc.Col(
                            html.Div(
                                dcc.Slider(id='slider',
                                  min=-1,
                                  max=1,
                                  step=0.01,
                                  value=0,
                                  vertical=False,
                                  tooltip = { 'always_visible': True },
                                  marks={
                                        -1: '-1',
                                        -0.5: '-0.5',
                                        0: '0',
                                        0.5: '0.5',
                                        1: '1',
                                    }
                                  ), id='slider-container',
                            ),width={'size':8,'offset':0}),
                        #dbc.Col(html.P('1')),
                    ],justify='center'),
                    dbc.Row([
                        #dbc.Col(html.P('-1')),
                        dbc.Col(
                            html.Div(
                                dcc.RangeSlider(id='range-slider',
                                  min=-1,
                                  max=1,
                                  step=0.01,
                                  value=[0,0.5],
                                  vertical=False,
                                  tooltip = { 'always_visible': True },
                                  ),
                                  id='range-slider-container',
                                  style={"display":'none'}
                            )
                            ,width={'size':6,'offset':0}),
                        #dbc.Col(html.P('1')),
                    ],justify='center'),
                    # dbc.Row([
                    #     dbc.Col(html.P(-1),width={'offset':1}), dbc.Col(html.P(0)), dbc.Col(html.P(+1)),
                    # ],justify="between",align="stretch"),
                    dbc.Row(
                        dbc.Col(# 7 button to press guess
                            html.Div(id = 'guess-button-slider-container', children=[
                            dbc.Button('Guess', size='lg', id='submit-button')],style={'margin':'30px'}),width={'size':1}),align='center',justify='center'),
                    dbc.Row(dbc.Col([
                        html.Div(id='guess-graph-container',
                            children=[
                            dcc.Store(id='guess-dict-store'),
                            dcc.Graph(id='guess-spending',style={"display": "inline-block","width": "100%"}),
                                ]
                            )],width={'size':6,'offset':0}),justify='center'),
                    dbc.Row(dbc.Col(
                        html.Div(id='results-graph-container',children=[dcc.Graph(id='results')],
                                 style={'display':'none'}),width={'size':6,'offset':0}),justify='center'
                           ),
                    dbc.Row(dbc.Col(html.P("But which departments actually contribute to the CRI value?",id='breakdown-lead-in',style={'display':'none'})))

                ],className = 'guesserDiv'),
        html.Div(id='more-info-container', style={"display":"none"},
                children=[
                # more graphs div
                html.Div(
                    children=[
                            html.Div([
                            dbc.Row(dbc.Col(html.Div(html.H4("City Spending Breakdown"),className='app-header-title'),width=8),justify='center'),
                            dbc.Row(dbc.Col(html.P('''Not every city has all of the departments we have classified as carceral, health and support related.
                                Toggle the buttons to view spending by department, by year, or to view average spending by category over the last four years.
                                Click on the departments listed under the "Spending Type" key
                                to make them temporarily disappear. Double click to view only that department.'''),width=8),justify='center'),
                            dbc.Row([
                                dbc.Col(dcc.Graph(id='explore-spending'),width=6),
                                dbc.Col(dbc.RadioItems(
                                    id='field',
                                    options=[{'label': i, 'value': i}
                                             for i in ['By Category','By Year','Departmental Spending 2020','Average Carceral Spending',
                                                       'Average Health and Support Spending']],
                                    value='By Category',
                                    labelStyle={'display': 'inline-block'}
                                ),width=3, style={'text-align':'left'})
                                ],align='center',justify='center'),
                            dbc.Row(dbc.Col(html.Div(html.H4("Let's see how your city compares across categories"),className='app-header-title'),width=8),justify='center'),
                            dbc.Row(dbc.Col(html.P('''The Carceral Resource Index is useful for comparing cities to each other because it quantifies
                                relative spending, which is easier to compare than raw dollar amounts. Toggle the buttons to compare
                                your city to others based on the different categories.'''),width=8),justify='center'),
                            dbc.Row([
                                dbc.Col(dcc.Graph(id='compareFig'),width=6,),
                                dbc.Col(
                                    dbc.RadioItems(
                                    id='compareby',
                                    options=[{'label': i, 'value': i} for i in ['Similar CRI Values','Similar Budget Size','Cities in the Same Region','Similar Police Budget Size']],
                                    value='Similar CRI Values',
                                    labelStyle={'display': 'inline-block'}
                                ),width=3,style={'text-align':'left'}),
                                ],align='center',justify='center')],className='compareexplore'),
                        ]),
                    html.Div([
                            dbc.Row(dbc.Col(html.H4('Why CRI')),justify='center'),
                            dbc.Row(dbc.Col(html.P('''Over the last several decades, many U.S. cities have defunded healthcare, housing assistance, benefit programs,
                                    substance use treatment, and community engagement, all of which have been shown to prevent the need for carceral systems in the first place.
                                    To varying degrees, municipalities have all bought into the idea
                                    that public safety requires surveillance and punishment, state violence, and
                                    the confinement of people in prisons. But decades of research have shown this approach has not made our communities
                                    safer nor healthier. The Carceral Resource Index measures where cities stand:
                                    do city leaders that purport to value community health and safety make spending decisions based on scientific
                                    evidence, or do they continue to pander to fear-based and racialized "law and order" rhetoric? '''),
                                width=8),justify='center'),
                            dbc.Row(dbc.Col(html.P('''Importantly, the lab does not prescribe a particular CRI value cities ought to achieve.
                                            Even a city with a positive CRI like Washington D.C. (0.53) can still have an $800 million investment in carceral systems which
                                            cause immense harm. Rather, the index provides community members and policy makers alike an insight into the relationship
                                            between city spending on carceral systems versus health and supportive services.'''), width=8),justify='center'),
                            dbc.Row(dbc.Col(html.P(['''You can read more about our CRI research on our ''',html.A(' website.',href='https://www.healthinjustice.org/copy-of-carceral-resource-index',target="_blank")],style={'font-size':'20px'}), width=8),justify='center'),
                            dbc.Row(dbc.Col(html.A(dbc.Button("Learn More"),href='https://www.healthinjustice.org/copy-of-carceral-resource-index',target="_blank")))
                        ],className='whyDiv'),
                    html.Div([
                            dbc.Row(dbc.Col(html.H4('What can you do?')),justify='center'),
                            dbc.Row(dbc.Col(html.P('''There are many groups across the United States organizing for investment
                                                    in the health and wellbeing of their communities on one hand, and divestment from police,
                                                    jails, prisons, and related institutions on the other. Below is small sampling of organizations
                                                    working towards the decriminalization of our communities, the abolition of the Prison Industrial Complex,
                                                    and the empowerment of affected communities and individuals.
                                                    Many of these organizations offer educational resources and accept monetary donations. There are also similar
                                                    local groups in towns and cities around the country which rely on volunteer organizing.
                                            '''),width=8),justify='center'),
                            dbc.Row(dbc.Col(html.P([
                                    html.P(html.A("Interrupting Criminalization",href='https://www.interruptingcriminalization.com/',target="_blank")),
                                    html.P(html.A("The National Council for Incarcerated and Formerly Incarcerated Women and Girls",href='https://www.nationalcouncil.us/',target="_blank")),
                                    html.P(html.A("#DefundThePolice",href='https://defundthepolice.org/ ',target="_blank")),
                                    html.P(html.A("Movement 4 Black Lives Invest-Divest Policy Platform",href='https://m4bl.org/policy-platforms/invest-divest/',target="_blank")),
                                    html.P(html.A("Critical Resistance",href='http://criticalresistance.org/',target="_blank")),
                                    html.P(html.A("Families for Justice as Healing",href='https://www.justiceashealing.org/',target="_blank")),
                                    html.P(html.A("Black and Pink",href='https://www.blackandpink.org/',target="_blank")),
                                    html.P(html.A("Action Center on Race & The Economy",href='https://acrecampaigns.org/?s=defund+the+police',target="_blank")),
                                    html.P(html.A("Black Lives Matter",href='https://blacklivesmatter.com/blm-demands/',target="_blank")),
                                    html.P(html.A("ACLU Cops and No Counselors Report",href='aclu.org/issues/juvenile-justice/school-prison-pipeline/cops-and-no-counselors',target="_blank")),
                                    html.P(html.A("Project NIA",href='https://project-nia.org/',target="_blank")),
                            ],style={'font-size':'20px'})))
                        ],className='whatDiv'),
                ])
            ])



@app.callback(Output('city-df-store','data'),
              Output('city-df2020-store','data'),
              Output('total-store','data'),
              Output('cri-store', 'data'),
              Input('city-dropdown','value'))

def make_filters(City):
    '''Create filtered dataframes once and store them as dictionaries in the browswer so that this expensive
    task only needs to be performed once'''
    city_df = city_groupby.get_group(City)
    #print(city_df)
    city_df2020 = city_df[city_df['Year']=='2020'].reset_index()
    TOTAL = city_df2020.at[0,'Total Spending']
    CRI2020 = city_df2020.at[0,'CRI']
    return city_df.to_dict(),city_df2020.to_dict(),TOTAL, CRI2020

#blues
@app.callback(Output('guess-spending','figure'),
              Output('guess-dict-store','data'),
              Output('total-spending','children'),
              [Input('slider', 'drag_value'),
               Input('city-dropdown','value'),
               Input('total-store','data')])
def make_guess(value,City,total):
    T = total
    CRI = value
    # calc health spending
    C = (T*(CRI-1))/-2
    H = T - C

    guess_dict = {'Category':['Carceral','Health and Support'],
                  'Key':['Your Guess','Your Guess'],
                'Dollar Amount':[C,H]}
    guessFig = px.bar(guess_dict,
                     x='Category',
                     y='Dollar Amount',
                     color='Category',
                     color_discrete_sequence=["darkblue","lightgreen"],
                     text='Dollar Amount',
                     title='Spending by Category for {}'.format(City)) #, Your Estimate
    guessFig.update_traces(texttemplate='%{text:.5s}')
    #guessFig.update_layout(height = 500)

    return guessFig, guess_dict, "{} in 2020 was ${:,}. Can you guess {}'s CRI?".format(City,T,City)
    #'{} in 2020 was ${:,}. What do you think the CRI value for {} was in 2020?'.format(City,TOTAL,City)

@app.callback(Output('slider-drag-output', 'children'),
              [Input('city-dropdown','value'),
              Input('slider', 'drag_value')])
def display_value(city,value):
    result = "Your guess: {}'s Carceral Resource Index = {}".format(city,value)

    return result
#show new graph, correct slider after pressing "Guess"
@app.callback(Output("results","figure"),
              Output("guess-graph-container","style"),
              Output("results-graph-container","style"),
              Output("breakdown-lead-in","style"),
              Output('guess-button-slider-container',"style"),
              Output('select-container',"style"),
              Output('post-guess',"style"),
              Output('slider-container','style'),
              Output('range-slider-container','style'),
              Output('range-slider','value'),
              Output('range-slider','marks'),
              Output('real-output', 'children'),
              Output('real-output', 'style'),
              Output('guesser-description','style'),
              Input('slider','value'),
              Input('submit-button', 'n_clicks'),
              Input('city-dropdown','value'),
              Input('city-df2020-store','data'),
              Input('total-store','data'),
              Input('cri-store','data'),
              State('guess-dict-store','data')
        )
def show_results(guessVal,n_clicks,City,city_df2020_data,total,cri,guess_dict):
    if n_clicks is None:
        raise PreventUpdate
    else:
        #city_df = city_groupby.get_group(City)
        city_df2020 = pd.DataFrame.from_dict(city_df2020_data)#city_df[city_df['Year']=='2020'].reset_index()
        TOTAL = total#city_df2020.at[0,'Total Spending']
        preDct = city_df2020.groupby('Category').sum()['Dollar Amount'].to_dict()
        postDct ={
                  'Category':['Carceral','Health and Support'],
                  'Key':['Correct Answer','Correct Answer'],
                  'Dollar Amount':[preDct['Carceral'],preDct['Health and Support']]
                 }
        postDf = pd.DataFrame.from_dict(postDct)

        compare = pd.DataFrame.from_dict(guess_dict).append(postDf)

        # change color scheme based on if they overshot or undershot CRI
        # if real carceral spending less than than guessed carceral spending
        if (postDct['Dollar Amount'][0] < guess_dict['Dollar Amount'][0]):
            # then make guess color key lightgreen and and answer color dark blue
            colors=["darkblue","lightgreen"]
        else:
            colors=["lightgreen","darkblue"]
            # make guess color key darkblue and answer color lightgreen
        resultsFig = px.bar(compare,
                         x='Category',
                         y='Dollar Amount',
                         color='Key',
                         color_discrete_sequence=colors,
                         barmode='group',
                         text='Dollar Amount',
                         title='Your Estimate versus Actual Spending')
        resultsFig.update_traces(texttemplate='%{text:.2s}')
        #resultsFig.update_layout(height = 600)
        CRI = cri
        if (abs(guessVal - CRI) > 0.35):
            marks = {CRI: 'Actual CRI', guessVal: 'Guess'}
        else: marks = {CRI: 'Actual CRI'}
        #actualPercents = round(postDf['Dollar Amount']*100/TOTAL).to_list()
        #answerPercentOutput = 'Actual values: Carceral: {:.0f}%, Health: {:.0f}%'.format(actualPercents[0],actualPercents[1])
        return (resultsFig, #results, figure
                {'display':'none'}, # "guess-graph-container","style"
                {'display':'block'}, # "results-graph-container","style"
                {'display':'block', 'font-size':'20px'}, # "breakdown-lead-in","style"
                {'display':'none'}, # 'guess-button-slider-container',"style"
                {'display':'none'}, # 'select-container',"style"
                {'display':'inline'}, # 'post-guess',"style"
                {'display':'none'}, #'slider-container','style'
                {'display':'inline'},#'range-slider-container','style'
                [guessVal,CRI], #'range-slider','value' # two values
                marks,#'range-slider','marks'
                'Actual 2020 CRI value for {} = {}'.format(City,CRI),#'real-output', 'children'
                {'margin-bottom':'30px', 'display':'block'},#'real-output', 'style'
                {'display':'none'},#'guesser-description','style'
                )

@app.callback(
    Output('explore-spending', 'figure'),
    Output('more-info-container','style'),
    [Input('submit-button', 'n_clicks'),
    Input("city-dropdown", "value"),
    Input('city-df-store','data'),
    Input("field", "value")]
)
def explore_budget(n_clicks,City,city_df_dict,field):
    #print(city_df_dict)
    if n_clicks is None:
        raise PreventUpdate
    else:
        # Set up city database filter
        city_df = pd.DataFrame.from_dict(city_df_dict, orient='columns')

        # drop rows where there are values of 0 (makes it look prettier)
        no0 = city_df[city_df['Dollar Amount'] != 0]
        byCategoryNo0 = no0.groupby(['Category','Spending Type']).mean().reset_index()

        # spending by year
        if (field == 'By Category'):
            exploreFig = px.bar(byCategoryNo0.sort_values('Dollar Amount',ascending=False),
                                x="Category",
                                y="Dollar Amount",
                                color="Spending Type",
                                #color_discrete_sequence=["blue", "lightgreen"],
                                #barmode='stack',
                                title = 'Average Departmental Spending 2017-2020')
            exploreFig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'})
        elif (field == 'By Year'):
            exploreFig = px.bar(no0.sort_values('Dollar Amount',ascending=False),
                                x="Year",
                                y="Dollar Amount",
                                color="Spending Type",
                                barmode='group',
                                text='Dollar Amount',
                                title = 'Departmental Spending 2017-2020')
            exploreFig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
            exploreFig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',xaxis={'categoryorder':'category ascending'})
        elif (field == 'Departmental Spending 2020'):
            # this includes departments that are nonexistent for comparison.
            # could add toggle for that
            exploreFig = px.bar(city_df.groupby(['Category','Spending Type']).mean().reset_index(),
                           x="Spending Type",
                           y="Dollar Amount",
                           color="Spending Type",
                           barmode='stack',
                           text='Dollar Amount',
                           title="Average spending (including non-existant departments)")
            exploreFig.update_traces(texttemplate='%{text:.2s}')
            exploreFig.update_xaxes(tickangle=45)
            exploreFig.update_layout(xaxis={'categoryorder':'total descending'},uniformtext_minsize=8, uniformtext_mode='hide')

        elif (field =='Average Carceral Spending'):
            try:
                exploreFig = px.bar(byCategoryNo0.loc[byCategoryNo0['Category']=='Carceral'].sort_values('Dollar Amount',ascending=False),
                                      x="Category",
                                      y="Dollar Amount",
                                      color="Spending Type",
                                      barmode='group',
                                      text='Dollar Amount',
                                      title=field +" 2017-2020")
                exploreFig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
                exploreFig.update_traces(texttemplate='%{text:.2s}')
            except:
                exploreFig = px.bar(city_df[(city_df['Category']=='Carceral') &(city_df['Year']=='2020')],
                                      x="Category",
                                      y="Dollar Amount",
                                      color="Spending Type",
                                      barmode='group',
                                      text='Dollar Amount',
                                      title="No carceral spending in this city")
                exploreFig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
                exploreFig.update_traces(texttemplate='%{text:.2s}')
        elif (field =='Average Health and Support Spending'):
            try:
                exploreFig = px.bar(byCategoryNo0.loc[byCategoryNo0['Category']=='Health and Support'].sort_values('Dollar Amount',ascending=False),
                                      x="Category",
                                      y="Dollar Amount",
                                      color="Spending Type",
                                      barmode='group',
                                      text='Dollar Amount',
                                      title=field +" 2017-2020")
                exploreFig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
                exploreFig.update_traces(texttemplate='%{text:.2s}')

            except:
                exploreFig = px.bar(city_df[(city_df['Category']=='Health and Support') &(city_df['Year']=='2020')],
                                      x="Category",
                                      y="Dollar Amount",
                                      color="Spending Type",
                                      barmode='group',
                                      text='Dollar Amount',
                                      title="No health spending in this city 2017-2020")
                exploreFig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
                exploreFig.update_traces(texttemplate='%{text:.2s}')

        # include depts that have no funding but exist in other cities / were coded in the dataset

        return exploreFig, {"display":"inline"}
# Comparison charts
@app.callback(Output('compareFig', 'figure'),
              [Input('submit-button', 'n_clicks'),
              Input("city-dropdown", "value"),
              Input("compareby", "value")]
             )
def city_comparisons(n_clicks,City,compareby):
    if n_clicks is None:
        raise PreventUpdate
    else:
        compareFig = px.bar()
        if (compareby =='Similar CRI Values'):
            #find indices of cities with similar CRIs and make mini dataframe

            index = similar_cri.index[similar_cri['City']==City].tolist()[0]
            similar_cri.iloc[index-2:index+3]
            if (index<2):
                #don't want negative indexing
                similarCRICities = similar_cri.iloc[0:6]
            else:
                similarCRICities = similar_cri.iloc[index-3:index+4]

            # make graph from iloc
            compareFig = px.bar(similarCRICities,
                               x="City",
                               y="CRI",
                               #color='lightblue',
                               text='CRI',
                               # color range corresponds to actual range of possible CRI values
                               #range_color=[-1,1],
                               #color_continuous_scale=[[0,"darkblue"], [1,"lightgreen"]],
                               title='Cities with most similar CRI values to '+City
                              )

        elif (compareby =='Similar Budget Size'):
            total_spending = city_groupby.first().sort_values('Total Spending').reset_index()
            index = total_spending.index[total_spending['City']==City].tolist()[0]
            if (index<3):
                similarSpendingCities = total_spending.iloc[0:6]
#             elif (index>45):
#                 similarSpendingCities = total_spending.iloc[index:]
            else:
                similarSpendingCities = total_spending.iloc[index-3:index+4]
            compareFig = px.bar(similarSpendingCities,
                               x="City",
                               y="Total Spending",
                               color='CRI',
                               text='Total Spending',
                               # color range is actual range of budget sizes in the dataset
                               #range_color=[104859447,19379830651],
                               # color range corresponds to actual range of CRI values in the dataset
                               range_color=[-1,1],
                               color_continuous_scale=[[0,"darkblue"], [1,"lightgreen"]],
                               title='Cities with similar sized 2020 budgets compared to '+City
                              )
            compareFig.update_traces(texttemplate='%{text:.2s}')
            compareFig.update_layout(xaxis={'categoryorder':'total descending'},uniformtext_minsize=8, uniformtext_mode='hide')

        elif (compareby =='Cities in the Same Region'):
            # use region groupby to show all cities from the same region
            # see region_dct line 23
            region = region_dct[City]
            cities_in_region = region_groupby.get_group(region).groupby('City').first().reset_index()
            compareFig = px.bar(cities_in_region,
                               x="City",
                               y="CRI",
                               color='CRI',
                               text='CRI',
                               # color range is actual range of budget sizes in the dataset
                               #range_color=[104859447,19379830651],
                               # color range corresponds to actual range of CRI values in the dataset
                               range_color=[-1,1],
                               color_continuous_scale=[[0,"darkblue"], [1,"lightgreen"]],
                               title='CRI of cities in the ' + region + " region"
                              )
            compareFig.update_layout(xaxis={'categoryorder':'total descending'})
        elif (compareby == 'Similar Police Budget Size'):
            #print(police_spending.index[police_spending['City']==City])
            index = police_spending.index[police_spending['City']==City].tolist()[0]

            if (index<3):
                similarPoliceSpending = police_spending.iloc[0:6]
            else:
                similarPoliceSpending = police_spending.iloc[index-3:index+4]
            compareFig = px.bar(similarPoliceSpending,
                               x="City",
                               y="Dollar Amount",
                               color='CRI',
                               text='Dollar Amount',
                               range_color=[-1,1],
                               color_continuous_scale=[[0,"darkblue"], [1,"lightgreen"]],
                               title='Cities with similar sized 2020 police department budgets compared to '+City
                              )
            compareFig.update_traces(texttemplate='%{text:.2s}')
            compareFig.update_layout(xaxis={'categoryorder':'total descending'},uniformtext_minsize=8, uniformtext_mode='hide')

        return compareFig

# app.clientside_callback(
#     """
#     function(n_clicks) {
#         if n_clicks == None{
#             raise PreventUpdate;
#         }
#         else{
#             window.scrollTo(0, document.body.scrollHeight);
#         }
#
#     }
#     """,
#     Output("javascript", "children"),
#     Input('try-another-button', 'n_clicks'),
# )


if __name__ == '__main__':
    app.run_server(debug=True)
