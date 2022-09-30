# Surf's Up: Analyzing SQLite Data with SQLAlchemy

## Overview

### Purpose

The analyst was asked to compile an analysis of June and December weather data for an investor who was considering buying beachfront property. Using SQLAlchemy and the pandas Python libraries, the analyst used an SQLite database of weather data to report on weather patterns for the desired location. The code used to generate these results may be found [here](https://github.com/cbeckler/surfs_up/blob/main/SurfsUp_Challenge.ipynb).

### Results

The results for June:

![June results](https://github.com/cbeckler/surfs_up/blob/main/Resources/june_results.png)

* June temperatures are mild, with a mean of roughly 75 degrees Farenheit and half of all observations falling between 73 and 77 degrees.

The results for December:

![December results](https://github.com/cbeckler/surfs_up/blob/main/Resources/dec_results.png)

* The weather for December was almost equally mild, with a mean of roughly 71 degrees and half of all observations falling between 69 ad 74 degrees.

When we take both of these months together, each representing the beginning of their opposite seasons, two things are clear:

* Temperatures year-round appear quite stable, with very little variation six months apart.
* While December minimum temperatures are about 10 degrees colder than June's, the maximum temperatures are nearly the same, indicating that most of the seasonal variation takes the form of slightly cooler winters.

## Summary

### Additional Analyses

The analyst created an additional dataframe with additional information for further analyses, using this method:

```
query_data = session.query(extract('month', Measurement.date),extract('year', Measurement.date), Measurement.tobs, Measurement.prcp).\
    filter(or_(extract('month', Measurement.date)==6, extract('month', Measurement.date)==12)).all()

query_df = pd.DataFrame(query_data, columns=['month','year','temp','precipitation'])
```

This dataset contained data for only June and December, but with created month and year variables for additional categorization, and with the inclusion of precipitation data.

A groupby by months was done with this method:

```
query_df.groupby('month').agg({'temp':['min','max','mean'],'precipitation':['min','max','mean']})
```
producing these results:

![month groupby](https://github.com/cbeckler/surfs_up/blob/main/Resources/month_analysis.png)

* As seen in the above analyses, temperature data is quite stable, with the biggest difference being between minimum temperatures.
* Precipitation is also stable, with under two-tenths of an inch in difference in the averages.
* These is a two inch difference in the maximums, indicating that December may be more prone to irregularly large incidents of rainfall than June.

A second groupby by month and year was done with this method:

```
query_df.groupby(['month','year']).agg({'temp':['min','max','mean'],'precipitation':['min','max','mean']})
```
producing these results:

![year groupby](https://github.com/cbeckler/surfs_up/blob/main/Resources/year_analysis.png)

* The temperature data also appears to be stable across years. June average temperatures fluctated between just under 74 degrees to just over 77 degrees, while December average temperatures ranged from just under 70 degrees to roughly 73 and a half degrees, though every other year stayed below 72.
* Precipitation was likewise stable across years. June average precipitation ranged from 0.04 to 0.21 inches, while December average precipitation ranged from 0.09 to 0.46 inches.

### Recommendations

Based on the mildness of the weather and its stability over time, the analyst would recommend this location as a good investment for beachfront property.

