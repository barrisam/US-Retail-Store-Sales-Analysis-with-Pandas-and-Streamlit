import streamlit as st
import plotly as py
import streamlit_nested_layout
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import plotly.express as px

st.set_page_config(page_title = "Sales Dashboard", layout = "wide")
st.header("US Retail Superstore Sales Analysis")


# read in the excel dataset with pandas
df = pd.read_csv("retail sales.csv")

# using the sum() function we get the sum of sales, profit and shipping cost

#sum = df.sum()
#sum

# to the nearest round figure
# sales is 2.3M
# profit is 286.4K
# shipping cost is 262.4K

# create layout. We have two outer columns
outer_cols = st.columns([1,1], gap = 'large')

# layout is divided into two columns. This is for the first one
# column 1 layout

with outer_cols[0]:
    sales, profit, shipping = st.columns([1,1,1])

    sales.metric(
                  label = "Total Sales",
                  value = "2.3M"
                )

    profit.metric(
                  label = "Total Profit",
                  value = "286.4K"
                 )

    shipping.metric(
                    label = "Total Shipping",
                    value = "262.4K"
                    )
    white_space = st.columns([1]) # create white space between the figures and chart

    # creating an inner nested col within col 1
     # This inner columns will hold the chart for sales and profit for the four regions and a table with the list of states and their sales and profits

    # using groupby to extract the columns we need from the dataframe
    plt.style.use("fivethirtyeight")
    
    region_sales_profit = df.groupby(by=['Region']).mean()[['Sales', 'Profit']]
    region_sales_profit = region_sales_profit.reset_index()
    sales = region_sales_profit['Sales']
    profit = region_sales_profit['Profit']
    region = region_sales_profit['Region']

    # creating a stacked bar chart
    fig = plt.figure(figsize = (9,6))

    plt.bar(region, sales, color = 'purple', label = 'Sales', width = 0.3)
    plt.bar(region, profit, bottom = sales, color = 'orange', label = 'Profit', width = 0.3)

    plt.xlabel("Region")
    plt.ylabel("Sales and Profit")
    plt.title("Average Sales and Profits by Region")

    plt.legend()
    plt.tight_layout()

    st.pyplot(fig)

    white_space = st.columns([1]) # create white space between the figures and chart
    # next we create an interactive table with the top 10 states by sales, profit on it. More states can be added if need be
    # give it a title

    st.write("""
    ##### Dataframe to show the top 10 performing states by sales #####
    """)


    sales_unique = df['Sales'].unique().tolist()
    profit_unique = df['Profit'].unique().tolist()
    state_unique = df['State'].unique().tolist()
  
    # add sidebar filter
    with st.sidebar:
     dataframe_sidebar_selection = st.multiselect('Choose State:',
                                        state_unique, default = ['California', 'New York', 'Texas', 'Washington', 'Pennsylvania', 'Florida', 'Illinois', 'Ohio', 'Michigan', 'Virginia'])
    
    
    state_dataframe = (df['State'].isin(dataframe_sidebar_selection))
    #use groupby to group data into sales and profit by state
    state_sales_profit = df[state_dataframe].groupby('State')[('Sales', 'Profit')].sum().sort_values(by = ['Sales'], ascending = False)
    state_sales_profit = state_sales_profit.reset_index()

    st.dataframe(state_sales_profit, use_container_width = True)


# THE END OF FIRST COLUMN

# This is the second outer column
with outer_cols[1]:

  st.write("""##### Regional Managers """)

  img1, img2, img3, img4 = st.columns(4)
  with img1:
    nick_img = Image.open('Images/nick-modified.png', )
    st.image(nick_img, width = 80)
    st.write(""" Nick """)

  
  with img2:
    susan_img = Image.open('Images/susan-modified.png', )
    st.image(susan_img, width = 80)
    st.write(""" Susan """)
  
  with img3:
    george_img = Image.open('Images/george-modified.png', )
    st.image(george_img, width = 80)
    st.write(""" George """)
  

  with img4:
    esther_img = Image.open('Images/esther-modified.png', )
    st.image(esther_img, width = 80)
    st.write(""" Esther """)

  white_space = st.columns([1])

  #second nested column

  # first get a table of the regional manager and the sum of sales 
  r_manager = df.groupby('Regional Manager')[('Sales')].sum().reset_index()

  st.write("""##### Pie chart to show the percentage profit by each manager in their respective regions """)

  # pie chart with matplotlib

  #fig2, ax1 = plt.subplots()
  fig2 = plt.figure(figsize = (6,6))
  labels = ["Esther (Central)", "George (South)", "Nick (East)", "Susan (West)"]

  # labels = r_manager['Regional Manager']
  value = r_manager['Sales']

  colors = ['#66b3ff', '#99ff99', '#ffcc99', '#ff9999']

  #explosion
  explode = (0,0.1,0,0.1)

  #plot
  plt.pie(value, colors = colors, labels = labels, autopct = '%1.1f%%', startangle = 90, pctdistance = 0.70, explode = explode)

  #draw circle
  centre_circle = plt.Circle((0,0), 0.60, fc = 'white')
  fig = plt.gcf()
  fig.gca().add_artist(centre_circle)

  #axis
  #equal aspect ratio ensures the pie is drawn as a circle
  plt.axis('equal')
  plt.tight_layout()

  st.pyplot(fig2)

  #third nested column
  fig3 = px.scatter_mapbox(df, lat="Latitude", lon="Longtitude", hover_name="City", hover_data=["State", "Sales"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
  fig3.update_layout(mapbox_style="open-street-map")
  fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
  st.plotly_chart(fig3, use_container_width = True)

# STYLING FOR THE METRIC

with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
