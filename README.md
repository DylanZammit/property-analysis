# Malta Property Analysis

A small web project where I scrape property information off websites and perform basic analysis, both descriptive and
predictive.

## Price Prediction
![anova](https://github.com/DylanZammit/property-analysis/blob/master/readme_img/anova.png)
Here we can choose various features that we would like our property of interest to contain, and we apply the ANOVA (Analysis of Variance) model to predict the property price learned from the scraped property data. The data is only scraped from a single source, so a larger data set would improve the prediction substantially. 
## Map View
![map](https://github.com/DylanZammit/property-analysis/blob/master/readme_img/locality.png)
We visualise the modal price on a locality0by-locality basis with this map view. It is clear that regions around Sliema
and Valletta are the most expensive.
## Regression
![regression](https://github.com/DylanZammit/property-analysis/blob/master/readme_img/regression.png)
Selecting properties of certain conditions we can see how the price of a property changes if the interior area of the
property changes as well. This way we can get a rough estimate of how much a property is valued given its location and
interior area, and helping us decide whether a specific property is over or uder-valued. Clicking on a data-point
displays its features and we can also press "View Property" and get redirected to the original web page from where it
was scraped.
