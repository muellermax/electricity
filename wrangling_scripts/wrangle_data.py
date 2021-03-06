# import libraries
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

from entsoe import EntsoePandasClient # doc: https://github.com/EnergieID/entsoe-py

from matplotlib import pyplot as plt
import seaborn as sns

# Information about Entsoe: https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html

# read token (stored in text file)
with open('token.txt', 'r') as file:
    data = file.read().replace('\n', '')

# connect to ENTSOE API
client = EntsoePandasClient(api_key=data)

# Define function to query generation
def query_generation(country_code, days_ago):
    """
    Function to query the generation for a given country for a specific period. 
    
    Input: 
        country_code (String): The country code, see here a list: https://github.com/EnergieID/entsoe-py
        days_ago (Int): Number of days in the past that should be considered. 
        
    Output: 
        generation (DataFrame): A DataFrame with the generation during the last [days_ago] days, 
        sorted by the variance of the energy sources. 
    """
    
    # define start and end date
    n_days_ago = (1*days_ago)
    date_today = datetime.today()
    date_past = date_today - timedelta(days=n_days_ago)

    start = pd.Timestamp(date_past.strftime('%Y%m%d'), tz='UTC')
    end = pd.Timestamp(date_today.strftime('%Y%m%d'), tz='UTC')
    
    # Get generation for given time and country code
    df = client.query_generation(country_code, start=start,end=end, psr_type=None)

    # Flatten multiindex columns and sort out consumption columns
    df.columns = [' '.join(col).strip() for col in df.columns.values]
    cols = [c for c in df.columns if 'Consumption' not in c]
    df = df[cols]
    
    # Filter out the words 'Actual' and 'Aggregated'
    noise_words_set = {'Actual', 'Aggregated'}
    new_cols = [' '.join(w for w in col.split() if w not in noise_words_set)
         for col in cols
         ]

    df.columns = [new_cols]
    
    # Flatten multiindex columns (again!) and sort out consumption columns
    df.columns = [' '.join(col).strip() for col in df.columns.values]
    cols = [c for c in df.columns if 'Consumption' not in c]
    df = df[cols]
    
    # Summarize different sources
    try:
    
        # Summarize renewable energy sources
        df['Other Renewables'] = df['Geothermal'] + df['Other renewable'] + df['Wind Offshore'] + df['Hydro Run-of-river and poundage'] + df['Hydro Water Reservoir']
        df = df.drop(['Geothermal', 'Other renewable', 'Wind Offshore', 'Hydro Run-of-river and poundage', 'Hydro Water Reservoir'], axis = 1)

        # Summarize fossil sources
        df['Fossil Oil, Fossil Gas, Hard coal'] = df['Fossil Oil'] + df['Fossil Hard coal'] + df['Fossil Gas']
        df = df.drop(['Fossil Oil', 'Fossil Hard coal', 'Fossil Gas'], axis = 1)

        # Summarize other sources
        df['Other sources'] = df['Other'] + df['Waste']
        df = df.drop(['Other', 'Waste'], axis = 1)

    except: 
        pass

    # Transpose DataFrame, calculate std and sort by std
    df = df.T
    df['variation'] = df.std(numeric_only=True, axis=1)
    df = df.sort_values('variation')

    # Remove extra std column and tranpose DataFrame back
    df = df.drop('variation', axis = 1)
    df = df.T

    return df


def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    df = query_generation('DE', 14)

    graph_one = []
    x_val = df.index

    for energy_source in df.columns:

        y_val = df[energy_source].tolist()

        graph_one.append(
            go.Scatter(
                x=x_val,
                y=y_val,
                mode='lines',
                name=energy_source,
                stackgroup = 'one'
            )
        )

    layout_one = dict(title='Generation in Germany during the last 14 days',
                      xaxis=dict(title='Date'),
                      yaxis=dict(title='Net Generation (MW)'),
                      colorway = ['#008000', '#ffa500', '#ff0000', '#000080', '#008080', '#808080', '#a52a2a', '#1e90ff', '#ffc40c'],
                      plot_bgcolor = '#E8E8E8',
                      hovermode = 'closest', 
                      hoverdistance = -1,
                      height = 500
                      )

    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))

    return figures
