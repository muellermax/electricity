# Analysis of Covid-19 in Chile

The dashboard of Covid-19 in Chile can be found here: https://covid-chile-dashboard.herokuapp.com/

### About this project
The plan is to make a dashboard that includes daily updated information about Covid-19 in Chile. The dashboard should include the following plots: 
* Daily infections in Chile including rolling average
* Daily deaths in Chile including rolling average
* Cases in comparison with other Latin American Countries
* Deaths in comparison with other Latin American Countries
* Map of Santiago de Chile with number of infections in the differenct city districs

### Installation
This project uses the following python packages: plotly, pandas, flask, gunicorn. For the deployment of the app I tried Heroku. 


### Data sources
* Main data source is the [John Hopkins University CSSE database](https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv)
* Furthermore, the Chilean government provides daily [updated data also on a district level](https://github.com/MinCiencia/Datos-COVID19/). 


### More ideas:
* Include daily tests in Chile, following the information provided here: https://github.com/MinCiencia/Datos-COVID19/blob/master/output/producto7/PCR.csv and here: https://github.com/MinCiencia/Datos-COVID19/blob/master/output/producto17/PCREstablecimiento.csv
* Include information about ventilators: https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto20
* Plots indicating the confirmed cases/deaths per 100,000 inhabitants
* Include data about mobility, as in here: https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto33
* Compare information about mortality: https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto32


### Files
The folder mayapp contains the following the following files: 
* __init__: Imports flask and initiates app
* routes.py: calls return_figures() from /wrangling_scripts/wrangle_data.py and sends JSON files to front-end

The folder wrangling_scripts contains the following files: 
* wrangle_data.py: Loads data from CSSE and defines to functions: get information for one single_country and about the daily_increase. Then, in return_figures the four plotly plots are prepared. 


### Further information to Covid-19 in Chile
* Government website: http://www.minciencia.gob.cl/covid19
* Government website: https://www.gob.cl/coronavirus/cifrasoficiales/


### Acknowledgments
Thanks to CSSE of John Hopkins University for providing the data on GitHub as well as to the government of Chile! 


### About
Maximilian Müller, Business Development Manager in the Renewable Energy sector. Now diving into the field of data analysis. 


### License

Copyright 2020 Maximilian Müller

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the 
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit 
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the 
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

From opensource.org
