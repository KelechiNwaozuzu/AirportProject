 # **Smart Travel: Predictive Security Wait Time Planner for ATL**

## What Our Application Does
**Our application is designed to provide travelers with an accurate prediction of the best time to leave their homes to arrive at Hartsfield-Jackson Atlanta International Airport (ATL) for their flights. By leveraging multiple data sources and sophisticated predictive modeling, we help users optimize their travel plans and reduce the stress associated with airport security wait times.**

## Key Features (Actively being worked on)
Real-time Flight Departure Information: We scrape up-to-date departure details from FlightStats.
Comprehensive Data Integration: Our system collects and processes data on weather conditions, traffic patterns, historical airport data, and current security wait times.
Predictive Modeling: Using a Random Forest Model, we analyze the collected data to predict expected security wait times and recommend optimal departure times from home.

## Current Implementation
Our code currently performs the following steps:
**Data Scraping:** Using Selenium, we scrape departure information from [FlightStats](https://www.flightstats.com/v2/flight-tracker/departures/ATL) and live security wait times from the [Hartisfield website](https://www.atl.com/times/). This involves navigating the website, extracting relevant flight details, and storing this data for further processing.

### Data Collection via APIs: We collect real-time and historical data on:

**Weather:** Using weather APIs to get current and forecasted weather conditions.

**Traffic:** Accessing traffic data APIs to understand current road conditions and predict travel times to the airport.

**Historical Data:** Aggregating historical data on flight departures, delays, and security wait times to identify patterns and trends.

**Holidays**: Collecting data for integrating and anylizing important U.S holidays in data collection.

## Collaborator Information: 

| Collaborator Name| github           | linkedIn  |
| ------------- |:-------------:| :-----:|
| Terrence Onodipe | https://github.com/TerrenceOnodipe | https://www.linkedin.com/in/terrence-onodipe/ |
| Steven Exil | https://github.com/stexil | https://www.linkedin.com/in/stexil |
| Kelechi Nwaozuzu | https://github.com/KelechiNwaozuzu | https://www.linkedin.com/in/kelechi-nwaozuzu2005/ |
| Teni Ojosipe | https://github.com/teniojosipe | https://www.linkedin.com/in/teni-ojosipe-201a98226/ |
| Jurmain Mitchell | https://github.com/L-JOM | https://www.linkedin.com/in/jurmain-mitchell/ |
