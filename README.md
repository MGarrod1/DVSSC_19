## Finding the right tool for the job

My entry to the Data Visualization Community Survey Challenge 2019 explores how members of the data visualization community use different tools and chart types for different purposes. It focuses on user’s responses to the questions:

1. What technologies do you use to visualize data?
2. Which of these charts have you used in production in the last 6 months? 
3. What does your audience use your data visualization for?

The 'make_bar_charts.py' script generates bar charts which show the top 5 technologies used by those whose answer to the question 3) contained research, education, journalism or entertainment. For example, those who answered with Education were most likely to be R users:

The 'make_cooc_map.py' script generates a heatmap which illustrates the most commonly occurring pairs of technologies and chart types from the user’s answer to the questions 1) and 2) respectively. The co-occurence of charts and technologies was defined by the number of times specific chart types and technologies were found to co-occur divided by the total possible times that they could have co-occurred.



Starting from the LHS of the chart the audience can choose a particular chart type (e.g Raster Map) moving right allows them to identify the two technologies that were most likely to co-occur with that chart type (for Raster map this is ArcGIS and QGIS). 

Each user could use multiple answers to questions 1) and 2). As a result, the correspondence between technologies used and chart types won’t be exact. For example,  I can't imagine a particular reason why ArcGIS should co-occur with Infographics. However, many of the pairings seem intuitive. Gephi (a software platform for graph/network visualization) tends to co-occur with both force-directed graph and network diagram - which is what one should expect!

