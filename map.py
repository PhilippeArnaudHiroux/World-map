import plotly.express as px                                             #Import Plotly Express for creating interactive visualizations
import pandas as pd                                                     #Import pandas for data manipulation and analysis
from my_functions import import_data_from_file, import_labels_from_file #Import custom functions for importing data and labels from files

#####################################Import the data
cities=import_data_from_file()      #Get information about the cities from a file
label_data=import_labels_from_file()#Get information about the colors associated with each year from a file

#########################Convert the data into a DataFrame
df=pd.DataFrame(cities) #Create a pandas DataFrame from the cities data

#################################################Make a color mapping from label to color
year_color_map={}                               #Initialize an empty dictionary to hold the mapping of years to colors
for label_dict in label_data:                   #Iterate through each dictionary in the year_data
    for year, color in label_dict.items():      #Iterate through the year-color pairs in the dictionary
        color_int=int(color, 16)                #Convert the hex string to an integer
        hex_color="#{:06X}".format(color_int)   #Convert the integer back to a hexadecimal string in #RRGGBB format
        year_color_map[year]=hex_color          #Map the year to its corresponding hex color in the dictionary
df['color']=df['label'].map(year_color_map)     #Add a new column 'color' to the DataFrame by mapping the 'label' column to the year_color_map

fig=px.scatter_geo(##########################################Create a scatter geo plot using Plotly Express
    df,                                                     #Use the DataFrame df as the data source
    lon='lon',                                              #Specify the longitude column for the scatter plot
    lat='lat',                                              #Specify the latitude column for the scatter plot
    hover_name='name',                                      #Display the city name when hovering over a point
    title='My world map!',                                  #Set the title of the map
    projection='natural earth',                             #Use the 'natural earth' projection for the map
    color='label',                                          #Use the 'label' column to determine the color of the points
    color_discrete_map=year_color_map,                      #Map colors to years using the year_color_map
    hover_data={'lon': False, 'lat': False, 'label': False} #Hide longitude, latitude, and label data when hovering
)

##########################################Change the size of the markers
fig.update_traces(marker=dict(size=10))  #Adjust the size of the markers to 10 (you can change this value as desired)

fig.update_geos(#############Update the geographic features of the figure
    showland=True,          #Enable the display of land areas
    landcolor='lightgreen', #Set the color of the land to light green
    showocean=True,         #Enable the display of ocean areas
    oceancolor='lightblue', #Set the color of the ocean to light blue
    showcoastlines=True,    #Enable the display of coastlines
    coastlinecolor='black', #Set the color of the coastlines to black
    showlakes=True,         #Enable the display of lakes
    lakecolor='lightblue',  #Set the color of lakes to light blue
    showrivers=True,        #Enable the display of rivers
    rivercolor='blue',      #Set the color of rivers to blue
    showcountries=True,     #Enable the display of country borders
    countrycolor='black',   #Set the color of country borders to black
    showframe=False,        #Hide the frame around the map
    resolution=50,          #Set a higher resolution for more detail
    projection_scale=1,     #Set the scale of the projection
    bgcolor='black'         #Set the background color of the map to black
)

fig.update_layout(###############Update the layout of the figure for better visibility
    title='My world map!',      #Set the title of the map
    geo=dict(                   #Define geographic features for the layout
        showland=True,          #Enable the display of land areas
        landcolor='lightgreen', #Set the color of the land to light green
        oceancolor='lightblue', #Set the color of the ocean to light blue
        showocean=True,         #Enable the display of ocean areas
        showcoastlines=True,    #Enable the display of coastlines
        coastlinecolor='black', #Set the color of coastlines to black
        showlakes=True,         #Enable the display of lakes
        lakecolor='lightblue',  #Set the color of lakes to light blue
        showrivers=True,        #Enable the display of rivers
        rivercolor='blue',      #Set the color of rivers to blue
        showcountries=True,     #Enable the display of country borders
        countrycolor='black'    #Set the color of country borders to black
    ),
    showlegend=True,            #Ensure the legend is displayed
    legend_title_text='Labels', #Set the title of the legend
    plot_bgcolor='black',       #Set the background color of the plot to black
    paper_bgcolor='black',      #Set the background color of the entire page to black
    font=dict(color='white')    #Set the font color to white
)

####################################Show map
fig.write_html("world_map.html")    #Save the figure as an HTML file named "world_map.html"
fig.show()                          #Display the figure in the default web browser or viewer
