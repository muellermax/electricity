import pandas as pd
import plotly.graph_objs as go

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

# Read in Covid-19 cases and deaths datasets from CSSE at John Hopkins University on Github.
csse_cases_all = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
csse_deaths_all = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

latin_america = ['Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'French', 'Guiana',
                 'Guyana Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela']


# Function to retrieve data for a single country from the CSSE data.
def single_country(country, df):
    """
    Function to provide Dataframe with cumulated cases of Covid-19
    out of CSSE data for a single country.

    Args:
        country (string): Name of country whose timeline should be prepared.
        df (Dataframe): Name of dataframe (confirmed cases or deaths) that should be included.

    Returns:
        country_timeline (Dataframe): Dataframe with two columns, datetime and confirmed cases.
    """

    # Select rows for the given country and apply pd.melt to unpivot DataFrame
    # from wide to long format. Drop for now unnessary rows ('Province/State', 'Lat', 'Long').
    country_timeline = df[df['Country/Region'] == country]
    country_timeline = country_timeline.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], axis=1)
    country_timeline = pd.melt(country_timeline)
    # country_timeline = country_timeline.drop(country_timeline.index[[0, 1, 2, 3]])

    # Rename columns and apply pandas datetime function.
    country_timeline.columns = ['date', 'cases']
    country_timeline['date'] = country_timeline['date'].astype('datetime64[ns]')

    return country_timeline[country_timeline.cases != 0]


# Function to retrieve data for the daily increase from the CSSE data.
def country_daily(country, df, days=7):
    """
    Function to provide the daily increase of confirmed cases of
    Covid-19 in a chosen country. An extra column includes the rolling
    average for a given amount of days.

    Args:
        country (string): Name of country whose timeline should be prepared.
        days (int), optional: Number of days for rolling average.
        df (Dataframe): Name of dataframe (confirmed cases or deaths) that should be included.

    Returns:
        Dataframe with three columns: date, daily increase and rolling average.
    """

    # Apply single_country_confirmed function and retrieve difference between
    # two dates. Add one column with rolling average and finally fill NaNs will 0.
    country_df = single_country(country, df)
    country_df['cases'] = country_df.cases.diff()

    confirmed_cases_series = country_df.cases
    country_df['rolling_avg'] = confirmed_cases_series.rolling(days).mean()

    country_df.columns = ['date', 'daily increase', 'rolling_avg']

    return country_df.fillna(0)


def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # first chart plots daily increase of Covid-19 infections in Chile and rolling average.
    # as a line chart

    graph_one = []
    df = country_daily('Chile', csse_cases_all)
    x_val = df.date.tolist()
    y_val = df['daily increase'].tolist()

    graph_one.append(
        go.Bar(
            x=x_val,
            y=y_val,
            name='Confirmed cases',
            hovertemplate='%{y:,.2}'
        )
    )

    y_val2 = df.rolling_avg.tolist()

    graph_one.append(
        go.Scatter(
            x=x_val,
            y=y_val2,
            mode='lines',
            name='Rolling Average',
            hovertemplate='%{y:,.2r}'
        )
    )

    layout_one = dict(title='Daily increase of confirmed cases of Covid-19 in Chile',
                      xaxis=dict(title='Date'),
                      yaxis=dict(title='Confirmed cases'),
                      )

    # second chart plots daily increase of Covid-19 deaths in Chile and rolling average.
    graph_two = []
    df = country_daily('Chile', csse_deaths_all)
    x_val = df.date.tolist()
    y_val = df['daily increase'].tolist()

    graph_two.append(
        go.Bar(
            x=x_val,
            y=y_val,
            name='Confirmed deaths',
            hovertemplate='%{y:,.2}'
        )
    )

    y_val2 = df.rolling_avg.tolist()

    graph_two.append(
        go.Scatter(
            x=x_val,
            y=y_val2,
            mode='lines',
            name='Rolling Average',
            hovertemplate='%{y:,.2r}'
        )
    )

    layout_two = dict(title='Daily increase of deaths caused by Covid-19 in Chile',
                      xaxis=dict(title='Date', ),
                      yaxis=dict(title='Deaths'),
                      )

    # third chart plots confirmed cases in South America
    graph_three = []

    for country in latin_america:
        df = single_country(country, csse_cases_all)
        x_val = df.date.tolist()
        y_val = df.cases.tolist()

        graph_three.append(
            go.Scatter(
                x=x_val,
                y=y_val,
                mode='lines',
                name=country,
                hovertemplate='%{y:,.2}'

            )
        )

    layout_three = dict(title='Total confirmed cases of Covid-19 in South America',
                        xaxis=dict(title='Date'),
                        yaxis=dict(title='Confirmed cases (log scale)',
                                   type='log')
                        )

    # Fourth chart plots deaths caused by Covid-19 in South America

    graph_four = []

    for country in latin_america:
        df = single_country(country, csse_deaths_all)
        x_val = df.date.tolist()
        y_val = df.cases.tolist()

        graph_four.append(
            go.Scatter(
                x=x_val,
                y=y_val,
                mode='lines',
                name=country,
                hovertemplate='%{y:,.2}'

            )
        )

    layout_four = dict(title='Total deaths caused by Covid-19 in South America',
                       xaxis=dict(title='Date'),
                       yaxis=dict(title='Deaths caused by Covid-19 (log scale)',
                                  type='log')
                       )

    # Fifth chart is a single value showing the total amount of cases in Chile and the increase.

    df = single_country('Chile', csse_cases_all)
    graph_five = go.Figure(go.Indicator(
                 title={'text': 'Covid-19 cases in Chile'},
                 mode='number+delta',
                 value=df.iloc[-1, 1],
                 delta={'position': "top",
                        'reference': df.iloc[-2, 1],
                        'increasing': {'color': '#8b0000'},
                        'valueformat': '{,}'},
                 number={'valueformat': '{,}'})
                 )

    # Sixths chart is a single value showing the total amount of deaths in Chile and the increase.

    df = single_country('Chile', csse_deaths_all)
    graph_six = go.Figure(go.Indicator(
                 title={'text': 'Covid-19 deaths in Chile'},
                 mode='number+delta',
                 value=df.iloc[-1, 1],
                 delta={'position': "top",
                        'reference': df.iloc[-2, 1],
                        'increasing': {'color': '#8b0000'},
                        'valueformat': '{,}'},
                 number={'valueformat': '{,}'})
                 )


    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))
    figures.append(dict(data=graph_five))
    figures.append(dict(data=graph_six))

    return figures
