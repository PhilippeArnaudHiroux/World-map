# World-map
This python project is a project where you can indicate on a world map where you have been before. You can also give each location a label.

## Libraries
```
pip install pandas
```
```
pip install plotly
```
```
pip install pycountry
```
```
pip install requests
```

## The code
When you start the code you will see the following screen. You will be given three options:
* Going to the location page
* Going to the label page
* Going to the world map

![main](image/readme/main.jpg)
### Add frame
![add city](image/City.jpg)

#### Add a location
Here you can add a location by typing the name of the location. You also need to add a label to the location. When you press the green plus symbol the longitude, latitude and country are requested from the location.
![add location](image/readme/add_city.jpg)

#### Delete location
On the **add location** page you have a button **Delete place**. Here you can delete a location. When you click open the page all locations from your list will appear. You can also filter by countries and by labels. When you select a location and then click on the red cross, this location will be removed from your list.
![delete location](image/readme/del_city.jpg)

#### Add a location manually
On the add location page there is also a button add place manually. If you click on this you can add a location manually by adding a name, longitude, latitude country code and label. When you press the green plus the location will be added to your list.
<details>
  <summary>Bekijk afbeelding</summary>
<img src="image/readme/add_city_manual.jpg" alt="Afbeelding beschrijving" />
</details>

# Source
## Python
* [plotly.express](https://plotly.com/python/plotly-express/)
    * [Scatter plots on maps](https://plotly.com/python/scatter-plots-on-maps/)
* [tkinter](https://docs.python.org/3/library/tkinter.html)
    * [messagebox](https://docs.python.org/3/library/tkinter.messagebox.html#module-tkinter.messagebox)
    * [colorchooser](https://docs.python.org/3/library/tkinter.colorchooser.html#module-tkinter.colorchooser)
    * [ttk](https://docs.python.org/3/library/tkinter.ttk.html#module-tkinter.ttk)
* [requests](https://www.w3schools.com/python/module_requests.asp)
* [ast](https://docs.python.org/3/library/ast.html)
* [pycountry](https://pypi.org/project/pycountry/)
* [subprocess](https://docs.python.org/3/library/subprocess.html)
* [Python Image Library (PIL)](https://pillow.readthedocs.io/en/stable/)
    * [Image](https://pillow.readthedocs.io/en/stable/reference/Image.html)
    * [ImageTk](https://pillow.readthedocs.io/en/stable/reference/ImageTk.html)
* [Pandas](https://www.w3schools.com/python/pandas/default.asp)

## API
* [OpenWeathermap](https://openweathermap.org/api/geocoding-api)