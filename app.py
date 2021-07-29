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

# Build App
external_stylesheets = [dbc.themes.BOOTSTRAP]
#"https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css", integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T", crossorigin="anonymous"]
#'https://codepen.io/chriddyp/pen/bWLwgP.css',"https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
server=app.server
            # Container for all layout
app.layout = dbc.Container(
        #children in container
        children=[
            #div for the top half of the page
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
                        html.P('''We are in the midst of a nationwide debate rethinking how to achieve public safety
                                and also promote public health, equity, and justice. If “money talks,” then budgets tell a story
                                about a community’s priorities. Select your city from the dropdown menu and then adjust the
                                slider to change the spending bar graph. Press "Guess" when you're satisfied to see how accurate
                                your estimate was.'''),width=8),
                        justify='center'
                       ),
                # row for drop down, label of drop down
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
                dcc.Store('total-store')
                ]),

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
                        ", ",
                        html.Span(
                            "health",
                            id="tooltip-health-target",
                            style={"font-weight": "bold", "cursor": "pointer"},
                        ),
                        ", and ",
                        html.Span(
                            "support",
                            id="tooltip-support-target",
                            style={"font-weight": "bold", "cursor": "pointer"},
                        ),
                        " categories in ",
                        html.Span(id='total-spending'),
                    ]),className='app-total-budget-par'),
                # 2.1
                dbc.Tooltip(
                    " Community Supervision, Corrections, Courts, Police, Prosecutors, Public Defenders, Sheriff ",
                    target="tooltip-carc-target", #style={"background-color": "#ffcc99"}
                ),
                # 2.2
                dbc.Tooltip(
                    " Health and Human Services (HHS), Parks and Recreation, Public Health ",
                    target="tooltip-health-target",#style={"background-color": "#99ccff"}
                ),
                # 2.3
                dbc.Tooltip(
                    " Arts and Culture, Civic and Community Engagement, Employment, Housing ",
                    target="tooltip-support-target",#style={"background-color": "#99ff99"}
                ),
            ],width={'size':8}),justify="center")),
        html.Div([
            dbc.Row(dbc.Col(html.Div(id='range-slider-drag-output'),
                             width=8),justify='center'),
            dbc.Row(dbc.Col(html.Div(id='answer-percent-output'),
                              width=8),justify='center')
            ],className='app-estimate-answer'),
        dbc.Row(
            dbc.Col(
                dcc.RangeSlider(id='range-slider',
                  min=0,
                  max=100,
                  step=0.5,
                  value=[33.3,66.6],
                  vertical=False,
                  allowCross=False,
                  ),width={'size':10,'offset':0}),justify='center'),
        dbc.Row(
            dbc.Col(# 7 button to press guess
                html.Div(id = 'guess-button-slider-container', children=[
                dbc.Button('Guess', id='submit-button')]),width={'size':3,'offset':2}),justify='center'),
        dbc.Row(dbc.Col([
            html.Div(id='guess-graph-container',
                children=[
                dcc.Store(id='guess-dict-store'),
                dcc.Graph(id='guess-spending',style={"display": "inline-block","width": "100%"}),
                    ]
                )],width={'size':9,'offset':2})),
        dbc.Row(dbc.Col(
            html.Div(id='results-graph-container',children=[dcc.Graph(id='results')],
                     style={'display':'none'}),width={'size':9,'offset':2})
               ),
        html.Div(id='post-guess',children=[
            dbc.Row([
                dbc.Col(html.A(dbc.Button('Try another city'),href='/'),width=3),
                dbc.Col(html.A(dbc.Button('Show Me More',id='show-more-button'),href='#more-info-container'),width=3)
                ],justify="center"
                )],
            style={'display':'none'}),
        dbc.Row(dbc.Col(
            html.A(id='more-info-container',children=html.Div(
                style={"display":"none"},
                children=[
                            # comparing
                            html.Div(html.H4("City Spending Breakdown"),className='app-header-title'),
                            html.P('''The Carceral Resource Index (CRI), compares municipal spending on health
                            and social support services versus carceral systems. The CRI is intended to be a tool to help inform
                            this long overdue nationwide debate. The CRI offers values ranging from -1 to 1.
                            A CRI coefficient of -1 represents a jurisdiction’s fiscal prioritization of carceral systems
                            to the exclusion of health and support, while 1 represents fiscal prioritization of health and
                            support systems to the exclusion of carceral expenditures. Expenditures that do not fall
                            squarely into the categories of "Carceral", "Health", or "Support" resources are excluded.'''),
                            dbc.Row([
                                dbc.Col(dcc.Graph(id='explore-spending'),width=9),
                                dbc.Col(dbc.RadioItems(
                                    id='field',
                                    options=[{'label': i, 'value': i}
                                             for i in ['By Category','By Year','Departmental Spending 2020','Average Carceral Spending',
                                                       'Average Health Spending','Average Support Spending']],
                                    value='By Category',
                                    labelStyle={'display': 'inline-block'}
                                ),width=3)
                                ],align='center'),
                            html.Div(html.H4("Let's see how your city compares across categories"),className='app-header-title'),
                            dbc.Row([
                                dbc.Col(dcc.Graph(id='compareFig'),width=9),
                                dbc.Col(
                                    dbc.RadioItems(
                                    id='compareby',
                                    options=[{'label': i, 'value': i} for i in ['Similar CRI Values','Similar Budget Size','Cities in the Same Region','Similar Police Budget Size']],
                                    value='Similar CRI Values',
                                    labelStyle={'display': 'inline-block'}
                                ),width=3),
                        ],align='center')
                ])))
               )
            ])



@app.callback(Output('city-df-store','data'),
              Output('city-df2020-store','data'),
              Output('total-store','data'),
              Input('city-dropdown','value'))

def make_filters(City):
    '''Create filtered dataframes once and store them as dictionaries in the browswer so that this expensive
    task only needs to be performed once'''
    city_df = city_groupby.get_group(City)
    #print(city_df)
    city_df2020 = city_df[city_df['Year']=='2020'].reset_index()
    TOTAL = city_df2020.at[0,'Total Spending']
    return city_df.to_dict(),city_df2020.to_dict(),TOTAL


@app.callback(Output('guess-spending','figure'),
              Output('guess-dict-store','data'),
              Output('total-spending','children'),
              Output('range-slider','marks'),
              [Input('range-slider', 'value'),
               Input('city-dropdown','value'),
               Input('total-store','data')])
def make_guess(value,City,total):
    TOTAL = total
    # percents
    a = value[0]
    b = value[1] - value[0]
    c = 100 - value[1]
    color = {
        i: "blue" if i <= a else "red" if (a < i <= (a + b)) else "green"
        for i in range(106)
    }
    marks = {
        i: {"label": str(i), "style": {"color": color[i]}}
        for i in range(0, 106, 5)
    }
    # dollar amounts
    A = a / 100 * TOTAL
    B = b / 100 * TOTAL
    C = c / 100 * TOTAL

    guess_dict = {'Category':['Carceral','Health','Support'],
                  'Key':['Guess','Guess','Guess'],
                'Dollar Amount':[A,B,C]}
    guessFig = px.bar(guess_dict,
                     x='Category',
                     y='Dollar Amount',
                     color='Category',
                     text='Dollar Amount',
                     title='Spending by Category, Your Estimate')
    guessFig.update_traces(texttemplate='%{text:.2s}')
    return guessFig, guess_dict, '{} in 2020 was ${:,}. What percent do you think {} spent on each category?'.format(City,TOTAL,City), marks

@app.callback(Output('range-slider-drag-output', 'children'),
              [Input('range-slider', 'value')])
def display_value(value):
    carc = value[0]
    health = value[1] -value[0]
    support = 100 - value[1]
    result = 'Your estimate: Carceral: {}%, Health: {}%, Support: {}%'.format(round(carc),round(health),round(support))
             #'Total Value Will Be {}% | Total Value Is: {}%'.format(round(drag_value1+drag_value2+drag_value3), round(value1+value2+value3))]
    return result
#show new graph after pressing "Guess"
@app.callback(Output("results","figure"),
              Output("guess-graph-container","style"),
              Output("results-graph-container","style"),
              Output('guess-button-slider-container',"style"),
              Output('select-container',"style"),
              Output('post-guess',"style"),
              Output('answer-percent-output','children'),
              Output('range-slider','disabled'),
              Input('submit-button', 'n_clicks'),
              Input('city-dropdown','value'),
              Input('city-df2020-store','data'),
              Input('total-store','data'),
              State('guess-dict-store','data')
        )
def show_results(n_clicks,City,city_df2020_data,total,guess_dict):
    if n_clicks is None:
        raise PreventUpdate
    else:
        #city_df = city_groupby.get_group(City)
        city_df2020 = pd.DataFrame.from_dict(city_df2020_data)#city_df[city_df['Year']=='2020'].reset_index()
        TOTAL = total#city_df2020.at[0,'Total Spending']
        preDct = city_df2020.groupby('Category').sum()['Dollar Amount'].to_dict()
        postDct ={
                  'Category':['Carceral','Health','Support'],
                  'Key':['Answer','Answer','Answer'],
                  'Dollar Amount':[preDct['Carceral'],preDct['Health'],preDct['Support']]
                 }
        postDf = pd.DataFrame.from_dict(postDct)

        compare = pd.DataFrame.from_dict(guess_dict).append(postDf)
        resultsFig = px.bar(compare,
                         x='Category',
                         y='Dollar Amount',
                         color='Key',
                         barmode='group',
                         text='Dollar Amount',
                         title='Your Estimate versus Actual Spending')
        resultsFig.update_traces(texttemplate='%{text:.2s}')
        actualPercents = round(postDf['Dollar Amount']*100/TOTAL).to_list()
        answerPercentOutput = 'Actual values: Carceral: {:.0f}%, Health: {:.0f}%, Support: {:.0f}%'.format(actualPercents[0],actualPercents[1],actualPercents[2])
        return resultsFig, {'display':'none'},{'display':'block'},{'display':'none'}, {'display':'none'},{'display':'inline'},answerPercentOutput,True

@app.callback(
    Output('explore-spending', 'figure'),
    Output('more-info-container','style'),
    [Input('show-more-button', 'n_clicks'),
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
            exploreFig = px.bar(byCategoryNo0,
                                x="Category",
                                y="Dollar Amount",
                                color="Spending Type",
                                barmode='stack',
                                #text='Dollar Amount',
                                title = 'Departmental Spending 2017-2020')
        elif (field == 'By Year'):
            exploreFig = px.bar(no0,
                                x="Year",
                                y="Dollar Amount",
                                color="Spending Type",
                                barmode='group',
                                text='Dollar Amount',
                                title = 'Departmental Spending 2017-2020')
            exploreFig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
            exploreFig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
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
                exploreFig = px.bar(byCategoryNo0.loc[byCategoryNo0['Category']=='Carceral'],
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
        elif (field =='Average Health Spending'):
            try:
                exploreFig = px.bar(byCategoryNo0.loc[byCategoryNo0['Category']=='Health'],
                                      x="Category",
                                      y="Dollar Amount",
                                      color="Spending Type",
                                      barmode='group',
                                      text='Dollar Amount',
                                      title=field +" 2017-2020")
                exploreFig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
                exploreFig.update_traces(texttemplate='%{text:.2s}')
            except:
                exploreFig = px.bar(city_df[(city_df['Category']=='Health') &(city_df['Year']=='2020')],
                                      x="Category",
                                      y="Dollar Amount",
                                      color="Spending Type",
                                      barmode='group',
                                      text='Dollar Amount',
                                      title="No health spending in this city 2017-2020")
                exploreFig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
                exploreFig.update_traces(texttemplate='%{text:.2s}')
        elif (field =='Average Support Spending'):
            try:
                exploreFig = px.bar(byCategoryNo0.loc[byCategoryNo0['Category']=='Support'],
                                      x="Category",
                                      y="Dollar Amount",
                                      color="Spending Type",
                                      barmode='group',
                                      text='Dollar Amount',
                                      title=field +" 2017-2020")
                exploreFig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
                exploreFig.update_traces(texttemplate='%{text:.2s}')
            except:
                exploreFig = px.bar(city_df[(city_df['Category']=='Support') &(city_df['Year']=='2020')],
                                      x="Category",
                                      y="Dollar Amount",
                                      color="Spending Type",
                                      barmode='group',
                                      text='Dollar Amount',
                                      title="No support spending in this city 2017-2020")
                exploreFig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
                exploreFig.update_traces(texttemplate='%{text:.2s}')

        # include depts that have no funding but exist in other cities / were coded in the dataset

        return exploreFig, {"display":"inline"}
# Comparison charts
@app.callback(Output('compareFig', 'figure'),
              [Input('show-more-button', 'n_clicks'),
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
                               color='CRI',
                               text='CRI',
                               # color range corresponds to actual range of possible CRI values
                               range_color=[-1,1],
                               color_continuous_scale='Agsunset',
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
                               color_continuous_scale='Agsunset',
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
                               color_continuous_scale='Agsunset',
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
                               color_continuous_scale='Agsunset',
                               title='Cities with similar sized 2020 police department budgets compared to '+City
                              )
            compareFig.update_traces(texttemplate='%{text:.2s}')
            compareFig.update_layout(xaxis={'categoryorder':'total descending'},uniformtext_minsize=8, uniformtext_mode='hide')

        return compareFig

if __name__ == '__main__':
    app.run_server(debug=True)
