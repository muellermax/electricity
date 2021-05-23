# import libraries
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

from entsoe import EntsoePandasClient # doc: https://github.com/EnergieID/entsoe-py

from matplotlib import pyplot as plt
import seaborn as sns

# Information about Entsoe: https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html

colorway_elec = px.colors.qualitative.Prism

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

    # Transpose DataFrame, calculate std and sort by std
    df = df.T
    df['variation'] = df.std(numeric_only=True, axis=1)
    df = df.sort_values('variation')

    # Remove extra std column and tranpose DataFrame back
    df = df.drop('variation', axis = 1)
    generation = df.T
    
    return generation


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

    layout_one = dict(title='Generation in Germany',
                      xaxis=dict(title='Date'),
                      yaxis=dict(title='Generation'),
                      colorway = colorway,
                      )

    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))

    return figures
