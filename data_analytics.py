from bokeh.palettes import viridis, d3
from sklearn import preprocessing
import matplotlib.pyplot as plt
import folium
from geopy.distance import vincenty
from sklearn.metrics.pairwise import euclidean_distances

# All
def plot_scatter(df, column, with_line = True):
    le = preprocessing.LabelEncoder()
    le.fit(df.salesman_id.unique())

    colors = viridis(len(df.salesman_id.unique()))
    colors = d3['Category10'][len(df.salesman_id.unique())]

    plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')

    plt.scatter(df.client_lat, df.client_lon, s=10, 
                c=[colors[x] for x in le.transform(df[column])], alpha=0.8)
    
    #Plot Center Salesman
    if 'salesman_lat' in df:
        df_s = df[['salesman_id','salesman_lat', 'salesman_lon']].drop_duplicates()
        #df_s.set_index('salesman_id')
        plt.scatter(df_s.salesman_lat, df_s.salesman_lon, s=50, 
                    c='red', #[colors[x] for x in le.transform(df_s.salesman_id)]
                    marker='^')    
        
        #plot lines
        if with_line:
            for i, row in df_s.iterrows():
                df_line = df[df[column] == row.salesman_id]

                for i2, row2 in df_line.iterrows():
                    plt.annotate("",
                                  xy=(row.salesman_lat, row.salesman_lon), 
                                     xycoords='data',
                                  xytext=(row2.client_lat, row2.client_lon), 
                                     textcoords='data',
                                  arrowprops=dict(arrowstyle="-",
                                                  color=colors[le.transform([row.salesman_id])[0]],
                                                  connectionstyle="arc3,rad=0."), 
                                  )
                    
    plt.show() 

def plot_map(df):
  c_latitude  = -16.673960
  c_longitude = -49.270990
  c_dist      = 5 #km  
  max_avg_ticket = df.client_revenue_avg.max()

  le = preprocessing.LabelEncoder()
  le.fit(df.salesman_id.unique())
  colors = d3['Category10'][len(df.salesman_id.unique())]

  # Build map 
  map_nyc = folium.Map(location=[c_latitude, c_longitude], zoom_start=11, width=840, height=580, 
                      tiles='cartodbpositron')
  # Plot Clients
  for i, row in df.iterrows():
      folium.CircleMarker(location=[row['client_lat'], row['client_lon']], 
                      popup="{}: {}".format(i, row.client_id),
                      fill_color= colors[le.transform([row['salesman_id']])[0]],
                      radius=4).add_to(map_nyc) 
      
      
  # Plot Center Salesman
  df_s = df[['salesman_id','salesman_lat', 'salesman_lon']].drop_duplicates()

  for i, row in df_s.iterrows():
      lat, long = row.salesman_lat, row.salesman_lon
      folium.Marker([lat, long], popup=str(i), icon=folium.Icon(color=colors[le.transform([row['salesman_id']])[0]])).add_to(map_nyc)
      folium.RegularPolygonMarker(
          [lat, long],
          popup=str(row.salesman_id),
          fill_color=colors[le.transform([row['salesman_id']])[0]],
          number_of_sides=4,
          radius=7
          ).add_to(map_nyc)
  return map_nyc