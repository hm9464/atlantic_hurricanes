# Hurricanes
Analysis of historical hurricane data from the US National Oceanic and Atmospheric Administration

## Data Source
The NOAA records all historical hurricanes and tropical storms in their hurdat dataset. For this project, we will focus on the Atlantic hurricane seasons from 1850-2017. The data are structured with recordings every 6 hours (0000, 0600, 1200, 1800). Hence, one limitation of this dataset is that it does not consider PEAK intensity when determingin strength of a storm, everything is relative to time.

## Background
Hurricanes have become increasingly prominent in recent years due to a combination of factors; most notably, climate change. According to weather.gov, prime conditions for a hurricane to form include
* Sea temperature of at least 26 degrees Celsius (80 degrees Farenheit)
* Latitiude of at least 5 degrees N/S of the equator (cannot form at the intertropical convergence zone due to the Corioles force that causes hurricanes to spin).
* High relative humidity.

This project will analyze hurricane paths in recent seasons, where storms tend to be at their strongest, including visual analysis and statistical trends over time.

## Installation
In a virtual environment (I am using Python 3.6):<br>
`pip install -r requirements/requirements.txt`<br>
`pip install basemap-1.2.0-cp36-cp36m-win_amd64.whl`<br>
* Download the basemap .whl file from here: https://www.lfd.uci.edu/~gohlke/pythonlibs/#basemap
* Put the file where you python packages are located and run above command

## Analysis
Results of analysis will be posted on my Github Pages.

### Hypothesis 1
Storms are making more frequent landfalls due to increased strength and duration of systems.

Comparison of storm paths in the last 100 years:
[2008-2017](maps/hurricane_paths_2008-2017.html)<br>
[1918-1927](maps/hurricane_paths_1918-1927.html)

### Hypothesis 2
Storms have increased in strength (wind speed) and intensity (minimum pressure) over time due to rising sea temperatures that have been observed (approximately 0.13 degrees Celsius per decade over the last 100 years).
