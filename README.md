# MDML Examples
Try this example on [Google Collab](https://colab.research.google.com/github/anl-mdml/examples/blob/main/intro.ipynb).

## Tutorial of Grafana Dashboard Basics

This tutorial will show how to:
* Log in to Grafana
* View your experiment's dashboard
* Add a data panel
* Connect to a data source
* Build a query
* View streaming data in real-time

#### Log in to Grafana
First, navigate to the Grafana webpage for your MDML instance at https://[MDML Hostname]/grafana. Log in with the same username and password you use to connect to the MDML. Congrats! You should have been successfully logged into Grafana.

#### View your experiment's dashboard
If your experiment's ID was associated with your account during registration, your dashboard will be the page shown upon logging in. If not, use the Search tool on the left hand side of the page to find your experiment's dashboard. They are named with the following format "[Experiment ID] Dashboard".

#### Add a data panel
Dashboards in Grafana are made up of panels. Panels can be added with a button in the top right of the page.
![](gifs/grafana_add_panel.gif)

#### Connect to a data source
Grafana shows real-time data by connecting to and querying a data source. The MDML creates a user in its TimescaleDB (PostgreSQL) database for the Grafana data source to use. This database user has read-only access to data streamed under the corresponding experiment ID. Data sources are selected while creating a panel and are named with the following format "[Experiment ID] PostgreSQL".
![](gifs/grafana_data_source.gif)

#### Build a query
After adding a panel and selecting a data source, a query is needed to start viewing data. Data streamed via the MDML is stored in PostgreSQL as tables with the following format "[Experiment ID].[Device ID]". Column names for each table are identical to the variables names used while streaming. For example, our tutorial will have a table titled __TUTORIAL.device1__ and data in columns __time__, __val1__, and __val2__. __time__ is used by Grafana as the time column to organize the time-series data. The right side of the page can be used to change panel settings, display options to customize the graph, and visualization types.
![](gifs/grafana_query.gif)

#### View streaming data in real-time
Your streaming data should now be visible and will update according to the refresh rate set on the dashboard (dropdown in the upper right hand corner). Panels can be resized and/or moved around the page. The data panel itself is interactive. It will show data values when hovering and will zoom in with a click and drag. Notice that zooming will change the time range (top right corner of dashboard) used when querying which affects all other panels.

## Grafana and other data types in MDML
The Grafana basics tutorial above covers how to visualize any data sent via the .publish_data() method in the MDML Python client. However, it is possible to stream vector data and image data via the MDML. This section will assume that data has already been streamed and go over querying for that data in Grafana.

#### Vector data
In the MDML, vector data can be used for things like spectrometry scans where it does not make sense to have a column for every wavelength. Instead, two vectors are used to represent the data. In the case of spectrometry data, the vectors could be wavelength and intensity values. This type of data is best displayed with Grafana's Plotly visualization type.  

#### Image data
Before querying for this data in Grafana, it is important to know how image streaming is done in the MDML. When the MDML receives image data, it loads the image into a motion-JPEG stream. This stream's endpoint must be initially created by an MDML admin.     