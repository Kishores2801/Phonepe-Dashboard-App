import pandas as pd
import numpy as np
import folium
import streamlit as st
import streamlit.components.v1 as components
import warnings
import json
import plotly.express as px
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
st.set_page_config(page_title="Phone-pe Web Dashboard App",layout="wide")




# Loading Geo_json files here
india_geo_json = "Data/Geo json Data/india_state_geo.json"

with open(india_geo_json) as f:
    india_geo = json.load(f)

# Creating Streamlit APP
# st.image("assets\Phone Pe App")
st.title("Phone-pe Interactive Web Dashboard")
st.write("The narrative of digital payments in India has captivated global attention. It spans from major cities to the most remote areas, driven by the widespread adoption of mobile phones, mobile internet, and modern payment infrastructure developed as public assets by the central bank and government. Established in December 2015, PhonePe has thrived in this era of API-driven digitization of payments in India. At its inception, we faced the challenge of accessing detailed and reliable data on digital payments in the country. PhonePe Pulse represents our contribution to the digital payments ecosystem, offering comprehensive insights derived from our journey and experiences.")

maintab1, maintab2, maintab3 = st.tabs(["Insurance Data", "Transactions Data", "User Data"])


# ====================================================== Insurance ====================================================#
# aggrgated Map
with maintab1:
    # Dataset
    insurance_aggregated = pd.read_csv("Data/aggregated/agg_insurance.csv")
    insurance_states = pd.read_csv("Data/aggregated/state_agg_insurance.csv")
    insurance_aggregated["Date"] = insurance_aggregated["Year"].astype(str) + insurance_aggregated["Quarter"].astype(str)
    insurance_aggregated["Date"] = pd.PeriodIndex(insurance_aggregated['Date'], freq='Q').strftime('%m-%Y')
    insurance_states["Date"] = insurance_states["Year"].astype(str) + insurance_states["Quarter"].astype(str)
    insurance_states["Date"] = pd.PeriodIndex(insurance_states['Date'], freq='Q').strftime('%m-%Y')

    # Years and Quarter dropdowns
    years = insurance_states["Year"].unique()
    # Calcuations
    Total_sum = insurance_aggregated["Amount"].sum()
    formatted_total_sum = format(Total_sum, ",") 
    min_year = insurance_aggregated["Year"].min()
    max_year = insurance_aggregated["Year"].max()
    # Visualization of Insurance Data
    st.header("Insurance Data")
    st.write(f'Insurance Transactions exceeding *₹{formatted_total_sum}* were conducted through the PhonePe app between {min_year} and {max_year}.')
    
    
    # Data Dropdown
    col1, col2, col3 = st.columns(3)
    with col1:
        year_selected = st.selectbox("Select Year", years)
    with col2:
        quarters = insurance_states[insurance_states["Year"]==year_selected]["Quarter"].unique()
        quarter_selected = st.selectbox("Select Quarter", quarters)
    with col3:
        col = st.selectbox("Select the column", ["Amount", "Average Transaction", "Count"], key="select_column1")
    # filtering the Quarter
    col1, col2 = st.columns(2)
    with col1:
        m= folium.Map(location=(20.5937, 78.9629),prefer_canvas=True,  zoom_start=4, min_zoom=4, max_zoom=4,  tiles="cartodb positron")
        filtered_data = insurance_states[(insurance_states["Year"]==year_selected) & (insurance_states["Quarter"]==quarter_selected)]
            

            # creating a chloropeth map
        folium.Choropleth(
                data=filtered_data,
                geo_data=india_geo,
                columns=['State', col],
                key_on="feature.properties.NAME_1",
                tooltip=folium.GeoJsonTooltip(fields=['NAME_1', col], aliases=['State', col], labels=True, sticky=False),
                highlight=True,
                fill_color="PuOr",
                fill_opacity=0.7,
                line_opacity=0.5,
                legend_name=col).add_to(m)

        components.html(m._repr_html_(),height=500)

    with col2:
        st.info(
                '''
                **Details of Chloropeth Map:**
                - More the color/shade varies towards purple, more Insurance premium were made in a given period.
                - We can change the Years, Quarters and Columns to see variety of Chloropeth Map.
                - The Columns options are Amount, Average Transaction.
                - The Quarters are filtered based on Years.
                - We can use filters to update the charts.

                '''
            )

        st.info(
                '''
                **Important Observations:**
                - Karnataka & Maharashtra has Highest Insurance Premium paid through Phone pe App.
                - Arunachal Pradesh has Highest Average Transaction.
                - Maharashtra has Highest Count of Insurance Premium paid.
                '''
            )


    
    st.header("Aggregated Insurance Data Analysis")
    # tabs Section for Insurance Aggregated
    Aggtab1, Aggtab2 = st.tabs(["Line Graph", "Column Graph",])
    
    
    with Aggtab1:
        # Creating a line Chart
        if col == "Count":
            title = "Number of Users"
        else:
            title = "Amount Spend in INR (₹)"
        
        col1, col2 = st.columns(2)

        with col1:
            fig = px.line(insurance_aggregated, x="Date", y=col, title=f'{col} of Insurance Premium paid using Phone-pe App')
            fig.update_yaxes(range=[0,max(insurance_aggregated[col])*1.2])
            fig.update_layout(
                        xaxis_title = "Date",
                        yaxis_title=title,
                        title_x=0.2,  # Align title to the center horizontally,
                        title_y=0.9,
                        title_font_size=30,
                        font_size=25

                    )
                
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            
            st.info(
                '''
                **Details of Line Graph:**
                - Line chart is used to represent the trend of the data.
                - X axis includes Date which combines Year and Quarter.
                - Y Axis represents total transactions in INR or total count of transaction.
                - We can use filters to update the charts.
                '''
            )

            st.info(
                '''
                **Important Observations:**
                - The trend of the data is increasing.
                - We can see an exponential growth in Insurance Premium from September 2021.
                - Based on the line chart we can expect Increase in future period based on the trend.
                - We can see surge on Average Transaction on March-2022.
                - We can see surge on Number of Users on December-2022.
                '''
            )
    with Aggtab2:
        col1, col2 = st.columns(2)
        with col1:
            # bar graph
            fig = px.bar(insurance_aggregated, x="Date", y=col, title=f'{col} of Insurance Premium paid using Phone-pe App')
            fig.update_yaxes(range=[0,max(insurance_aggregated[col])*1.2])
            fig.update_layout(
                        xaxis_title = "Date",
                        yaxis_title=title,
                        title_x=0.2,  # Align title to the center horizontally,
                        title_y=0.9,
                        title_font_size=30,
                        font_size=20

                    )
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.info(
                '''
                **Details of Bar Graph:**
                - Bar chart is used to compare Transaction for each Quarter.
                - X axis includes Date which combines Year and Quarter.
                - Y Axis represents total transactions in INR or total count of transaction.
                - We can use filters to update the charts.
                
                

                '''
            )

            st.info(
                '''
                **Important Observations:**
                - The trend of the data is increasing for each Quarter for every State.
                - Based on the line chart we can expect Increase in future period based on the trend.
                
                ''')

        


        
    # Third Section     
    states = insurance_states["State"].unique()
    # State Functions
    selected_state = st.selectbox("Select the State", states)
    # A
    st.header("Aggregated States Insurance Data Analysis")
    # tabs Section for Insurance Aggregated
    statetab1, statetab2 = st.tabs(["Line Graph", "Column Graph",])
                    
    with statetab1:
            col1, col2 = st.columns(2)
            with col1:
                # creating Line Chart
                # Filtering the data
                insurance_states_filtered = insurance_states[insurance_states["State"] == selected_state]
                fig =px.line(insurance_states_filtered, x="Date", y=col, title=f'{col} of Insurance Premium paid using Phone-pe App in {selected_state}')
                fig.update_yaxes(range=[0,max(insurance_states_filtered[col])*1.2])
                fig.update_layout(
                        xaxis_title = "Date",
                        yaxis_title=title,
                        title_y=0.9,
                        title_x=0.2,  # Align title to the center horizontally,
                        title_font_size=20,
                        font_size=10,

                    )
                st.plotly_chart(fig, use_container_width=True,)


        
            with col2:
                st.info(
                    '''
                    **Details of Line Graph:**
                    - Line chart is used to compare Transaction for each Quarter for each States.
                    - X axis includes Date which combines Year and Quarter.
                    - Y Axis represents total transactions in INR or total count of transaction for selected States.
                    - We can use filters to update the charts.
                    '''
                )

                st.info(
                    '''
                    **Important Observations:**
                    - The trend of the data is increasing for each Quarter in each States.
                    - Based on the line chart we can expect Increase in future period based on the trend.
                    ''')
    with statetab2:
        col1, col2 = st.columns(2)
        with col1:
            # bar graph
            fig = px.bar(insurance_states_filtered, x="Date", y=col, title=f'{col} of Insurance Premium paid using Phone-pe App in {selected_state}')
            fig.update_yaxes(range=[0,max(insurance_states_filtered[col])*1.2])
            fig.update_layout(
                        xaxis_title = "Date",
                        yaxis_title=title,
                        title_x=0.1,  # Align title to the center horizontally,
                        title_y=0.9,
                        title_font_size=20,
                        font_size=10
                    )
            st.plotly_chart(fig, use_container_width=True,)
        with col2:
            st.info(
                    '''
                    **Details of Bar Graph:**
                    - Bar chart is used to compare Transaction for each Quarter for each States.
                    - X axis includes Date which combines Year and Quarter.
                    - Y Axis represents total transactions in INR or total count of transaction for selected States.
                    - We can use filters to update the charts.
                    '''
                )

            st.info(
                    '''
                    **Important Observations:**
                    - The trend of the data is increasing for each Quarter in each States.
                    - Based on the line chart we can expect Increase in future period based on the trend.
                    ''')
            
    # Fourth Section
    st.header("Aggregated Transaction by Districts Data Analysis")
  
    Districttab1, Districttab2  = st.tabs(["Column Graph", "Pie Graph"])
    top_district = pd.read_csv("Data/top/Top_Districts_Insurance.csv")
  
   

    with Districttab1:
        Districtcol1, Districtcol2 = st.columns(2)
    with Districtcol1:
        filtered_data = top_district[(top_district["Year"]==year_selected) & (top_district["Quarter"]==quarter_selected) & (top_district["State"]==selected_state)]
        fig = px.bar(filtered_data, x=col, y="District", orientation="h", title=f'Districts in {selected_state} on {year_selected}-{quarter_selected}')
        fig.update_layout(
                    xaxis_title = title,
                    yaxis_title="District",
                    title_y=0.9,
                    title_x=0.2,  # Align title to the center horizontally,
                    title_font_size=20,
                    font_size=10,  
                    )

        st.plotly_chart(fig, use_container_width=True)
    
    with Districtcol2:
        st.info(
            """
            **Details of Bar graph Graph:**
            - This Horizontal Bar Graph, is used to show transaction for Each District in Each States in each Quarters.
            - We can use filters to update the charts.
            """
        )

        st.info(
            """
            **Important Observation:**
            - All the transactions types are in increasing trend in percentage for each Quarter in Districts.

            """
        )



       
       
    with Districttab2:
       Districtcol1, Districtcol2 = st.columns(2)
       with Districtcol1:
            filtered_data = top_district[(top_district["Year"]==year_selected) & (top_district["Quarter"]==quarter_selected) & (top_district["State"]==selected_state)]
            fig = px.pie(filtered_data, values=col, names="District", title=f"{year_selected} - {quarter_selected} District Breakdown in {selected_state}",hole=.4)
            st.plotly_chart(fig, use_container_width=True)
        
       with Districtcol2:
        st.info(
            """
            **Details of Pie Chart:**
            - The plot was used to show breakdown of transaction happened through Phone-pe app for Each District in Each States in each Quarters.
            - We can use filters to update the charts.
            """
        )

        st.info(
            """
            **Important Observation:**
            - All the transactions types are in increasing trend in percentage for each Quarter in Districts.

            """
        )

    
# ====================================================== Transaction ====================================================#

# Transaction Tab
with maintab2:
   # Columns
   
   # loading the Dataset
   transaction_aggregated = pd.read_csv("Data/aggregated/agg_transaction.csv")
   transaction_states = pd.read_csv("Data/aggregated/state_agg_transaction.csv")
   transaction_aggregated["Date"] = transaction_aggregated["Year"].astype(str) + transaction_aggregated["Quarter"].astype(str)
   transaction_aggregated["Date"] = pd.PeriodIndex(transaction_aggregated['Date'], freq='Q').strftime('%m-%Y')
   transaction_states["Date"] = transaction_states["Year"].astype(str) + transaction_states["Quarter"].astype(str)
   transaction_states["Date"] = pd.PeriodIndex(transaction_states['Date'], freq='Q').strftime('%m-%Y')

   # Years and Quarter dropdowns
   years = transaction_states["Year"].unique()

   # calculation
   Total_sum = transaction_aggregated["Amount"].sum()
   formatted_total_sum = format(Total_sum, ",")
   min_year = transaction_aggregated["Year"].min()
   max_year = transaction_aggregated["Year"].max()

   # Visualization of Transaction Data
   st.header("Transactions Data")
   st.write(f'Overall Transaction exceeding *₹{formatted_total_sum}* were conducted through the PhonePe app between {min_year} and {max_year}.')

    # Data Dropdown
   col1, col2, col3, col4 = st.columns(4)
   with col1:
       year_selected = st.selectbox("Select Year", years)
   with col2:
    quarters = transaction_states[transaction_states["Year"]==year_selected]["Quarter"].unique()
    quarter_selected = st.selectbox("Select Quarter", quarters, key="quarter2")
   with col3:
    transaction_type = transaction_states["Name"].unique()
    transaction_selected =st.selectbox("Select Transaction Type", transaction_type)
   with col4:
    colo2 = st.selectbox("Select the column", ["Amount", "Average Transaction", "Count"], key="select_column3")

    
   col1, col2 =  st.columns(2)

   with col1:
        # filtering the Quarter
        m= folium.Map(location=(20.5937, 78.9629),prefer_canvas=True,  zoom_start=4, min_zoom=4, max_zoom=4,  tiles="cartodb positron")
        filtered_data = transaction_states[(transaction_states["Year"]==year_selected) & (transaction_states["Quarter"]==quarter_selected) & (transaction_states["Name"]==transaction_selected)]

        # creating a chloropeth map
        folium.Choropleth(
                data=filtered_data,
                geo_data=india_geo,
                columns=['State', colo2],
                key_on="feature.properties.NAME_1",
                tooltip=folium.GeoJsonTooltip(fields=['NAME_1', colo2], labels=True, sticky=False),
                highlight=True,
                fill_color="PuOr",
                fill_opacity=0.7,
                line_opacity=0.5,
                legend_name=colo2).add_to(m)
        components.html(m._repr_html_(),height=500)
    
   with col2:
        st.info(
            '''
            **Details of Chloropeth Map:**
            - More the color/shade varies towards purple, more transaction made in a given period.
            - We can change the Years, Quarters and Columns to see variety of Chloropeth Map.
            - The Columns options are Amount, Average Transaction.
            - The Quarters are filtered based on Years. 
            - We can use filters to update the charts.

            '''
        )
        st.info(
            '''
            **Important Observations:**
            - Maharashtra has high Recharge Bill paid through Phone pe App.
            - Maharashtra, Karnataka, Telugana, Andra Predesh has high Peer to Peer payments paid through Phone pe App.
            - Maharashtra, Karnataka has high Merchant payments paid through Phone pe App.
            - Maharashtra, Karnataka, has high Merchant payments paid through Phone pe App.

            '''
        )

   # Second Section
   st.header("Aggregated Transaction Data Analysis")
   Aggtab1, Aggtab2, Aggtab3  = st.tabs(["Line Graph", "Column Graph", "Pie Graph"])
   
    
    # Line Chart
   with Aggtab1:
      aggcol1, aggcol2 = st.columns(2)

      with aggcol1:
        # Creating a line Chart
        
        fig = px.line(transaction_aggregated, x="Date", y=colo2,color="Name", title=f'{colo2} of Transactions using Phone-pe App')
        fig.update_yaxes(range=[0,max(transaction_aggregated[col])*1.2])
        fig.update_layout(
                    xaxis_title = "Date",
                    yaxis_title=title,
                    title_y=0.9,
                    title_x=0.2,  # Align title to the center horizontally,
                    title_font_size=20,
                    font_size=10
                )
        st.plotly_chart(fig, use_container_width=True)
            
      with aggcol2:
                st.info(
                    '''
                    **Details of Line Graph:**
                    - Line chart is used to represent the trend of the data.
                    - X axis includes Date which combines Year and Quarter.
                    - Y Axis represents total transactions in INR or total count of transaction.
                    - We can use filters to update the charts.
                    
                    '''
                )

                st.info(
                    '''
                    **Important Observation:**
                    - Highest type of transactions made through Phone-pe App is Peer to Peer payments.
                    - Recently, We can also see that Merchant Payments are also has a considerable increase over period of time.
                    
                    '''
                )
   with Aggtab2:
       Aggcol1, Aggcol2 = st.columns(2)

       with Aggcol1:
           # Creating a column chart
           fig = px.bar(transaction_aggregated, x="Date", y=colo2,color="Name", title=f'{colo2} Transactions paid through Phone-Pe App')
           fig.update_yaxes(range=[0,max(transaction_aggregated[col])*1.2])
           fig.update_layout(
                    xaxis_title = "Date",
                    yaxis_title=title,
                    title_y=0.9,
                    title_x=0.2,  # Align title to the center horizontally,
                    title_font_size=20,
                    font_size=10,
                )
           st.plotly_chart(fig, use_container_width=True)
       with Aggcol2:
           st.info(
               """
                **Details of Bar Graph:**
                - Bar chart is used to compare Transaction for each Quarter for each Transaction Types.
                - X axis includes Date which combines Year and Quarter.
                - Y Axis represents total transactions in INR or total count of transaction for Transaction Types.
                - We can use filters to update the charts.

               """
           )

           st.info(
               """
               **Important Observation:**
               - All the transactions types are in increasing trend for each Quarter.
               - Highest type of transactions made through Phone-pe App is Peer to Peer payments.
               - Recently, We can also see that Merchant Payments are also has a considerable increase over period of time.
               """
           )
   with Aggtab3:
       Aggcol1, Aggcol2 = st.columns(2)
       # Filter Data
       transaction_aggregated_filter = transaction_aggregated[(transaction_aggregated["Year"]==year_selected) & (transaction_aggregated["Quarter"]==quarter_selected)]
       with Aggcol1:
           # Pie Chart
           fig = px.pie(transaction_aggregated_filter, values=colo2, names="Name", title=f"{year_selected} - {quarter_selected}",hole=.4)
           fig.update_traces(textposition='outside', textinfo='percent+label')
           st.plotly_chart(fig, use_container_width=True)
        
       with Aggcol2:
           st.info(
               """
                **Details of Pie Graph:**
                - The plot was used to show breakdown of transaction happened through Phone-pe app by Each Quarter.
                - We can use filters to update the charts.

                """
           )
           st.info(
               '''
                **Important Observation:**
               - All the transactions types are in increasing trend in percentage for each Quarter.
               - Highest type of transactions made through Phone-pe App is Peer to Peer payments in each Quarter.
               - Recently, We can also see that Merchant Payments are also has a considerable increase over period of time in each Quarter.
                '''
           )
   # Third Section
   st.header("Aggregated Transaction by States Data Analysis")
   states = transaction_states["State"].unique()
    # State Functions
   selected_state = st.selectbox("Select the State", states, key="States2")
   Statetab1, Statetab2, Statetab3  = st.tabs(["Line Graph", "Column Graph", "Pie Graph"])
   
   # Filtered Dataset
   filtered_data = transaction_states[transaction_states["State"] == selected_state]

   # Line Chart
   with Statetab1:
       
       statecol1, statecol2 = st.columns(2)
       with statecol1:
           # Creating Line Chart
            fig = px.line(filtered_data, x="Date", y=colo2, color="Name", title=f'{colo2} of Transactions paid in {selected_state}')
            fig.update_yaxes(range=[0,max(filtered_data[colo2])*1.5])
            fig.update_layout(
                xaxis_title = "Date",
                yaxis_title=title,
                title_y=0.9,
                title_x=0.2,  # Align title to the center horizontally,
                title_font_size=20,
                font_size=10,  
            )
            st.plotly_chart(fig, use_container_width=True)
      
       with statecol2:
           st.info(
               """
                **Details of Line Graph:**
                - Line chart is used to represent the trend of the data by each states.
                - X axis includes Date which combines Year and Quarter.
                - Y Axis represents total transactions in INR or total count of transaction.
                - We can use filters to update the charts.
               
               """
           )
           st.info(
               """
               **Important Observation:**
               - All the transactions types are in increasing trend in percentage for each Quarter in each state.
               - Highest type of transactions made through Phone-pe App is Peer to Peer payments in each Quarter in each states.
               """
           )
   # column Chart
   with Statetab2:
       statecol1, statecol2 = st.columns(2)

       with statecol1:
           fig = px.bar(filtered_data, x="Date", y=colo2,color="Name", title=f'{colo2} Transactions paid through Phone-Pe App in {selected_state}')
           fig.update_yaxes(range=[0,max(filtered_data[colo2])*1.5])
           fig.update_layout(
                xaxis_title = "Date",
                yaxis_title=title,
                title_y=0.9,
                title_x=0.2,  # Align title to the center horizontally,
                title_font_size=20,
                font_size=10,  
            )
           st.plotly_chart(fig, use_container_width=True)

       with statecol2:
           st.info(
               """
               **Details of Bar Graph:**
               - The bar graph shows the number of transactions made through Phone-Pe App in each Quarter in each state.
               - X axis includes Date which combines Year and Quarter.
               - Y Axis represents total transactions in INR or total count of transaction for Transaction Types.
               - We can use filters to update the charts.
               """
           )

           st.info(
               '''
               **Important Observation:**
               - All the transactions types are in increasing trend in percentage for each Quarter in each state.
               - Highest type of transactions made through Phone-pe App is Peer to Peer payments in each Quarter in each states.
               '''
           )
    
   with Statetab3:
       statecol1, statecol2 = st.columns(2)
       with statecol1:
           fig = px.pie(filtered_data, values=colo2, names="Name", title=f"{year_selected} - {quarter_selected} in {selected_state}",hole=.4)
           fig.update_traces(textposition='outside', textinfo='percent+label')
           st.plotly_chart(fig, use_container_width=True)
       
       with statecol2:
           st.info(
               """
               **Details of Pie Graph:**
                - The plot was used to show breakdown of transaction happened through Phone-pe app by Each Quarter.
                - We can use filters to update the charts.
                
                
                """
           )
           st.info(
               """
               **Important Observation:**
               - All the transactions types are in increasing trend in percentage for each Quarter in states.
               - Highest type of transactions made through Phone-pe App is Peer to Peer payments in each Quarter in states.
               - Recently, We can also see that Merchant Payments are also has a considerable increase over period of time in each Quarter in states..
               """
           )

   # Fourth Section
   st.header("Aggregated Transaction by Districts Data Analysis")
  
   Districttab1, Districttab2  = st.tabs(["Column Graph", "Pie Graph"])
   top_district = pd.read_csv("Data/top/Top_Districts_Transaction.csv")
  
   

   with Districttab1:
    Districtcol1, Districtcol2 = st.columns(2)
    with Districtcol1:
        filtered_data = top_district[(top_district["Year"]==year_selected) & (top_district["Quarter"]==quarter_selected) & (top_district["State"]==selected_state)]
        fig = px.bar(filtered_data, x=colo2, y="District", orientation="h", title=f'Districts in {selected_state} on {year_selected}-{quarter_selected}')
        fig.update_layout(
                    xaxis_title = title,
                    yaxis_title="District",
                    title_y=0.9,
                    title_x=0.2,  # Align title to the center horizontally,
                    title_font_size=20,
                    font_size=10,  
                    )

        st.plotly_chart(fig, use_container_width=True)
    
    with Districtcol2:
        st.info(
            """
            **Details of Bar graph Graph:**
            - This Horizontal Bar Graph, is used to show transaction for Each District in Each States in each Quarters.
            - We can use filters to update the charts.
            """
        )

        st.info(
            """
            **Important Observation:**
            - All the transactions types are in increasing trend in percentage for each Quarter in Districts.

            """
        )



       
       
   with Districttab2:
       Districtcol1, Districtcol2 = st.columns(2)
       with Districtcol1:
            filtered_data = top_district[(top_district["Year"]==year_selected) & (top_district["Quarter"]==quarter_selected) & (top_district["State"]==selected_state)]
            fig = px.pie(filtered_data, values=colo2, names="District", title=f"{year_selected} - {quarter_selected} District Breakdown in {selected_state}",hole=.4)
            st.plotly_chart(fig, use_container_width=True)
        
       with Districtcol2:
        st.info(
            """
            **Details of Pie Graph:**
            - The plot was used to show breakdown of transaction happened through Phone-pe app for Each District in Each States in each Quarters.
            - We can use filters to update the charts.
            """
        )

        st.info(
            """
            **Important Observation:**
            - All the transactions types are in increasing trend in percentage for each Quarter in Districts.

            """
        )

       

    
# ====================================================== Users ====================================================#
with maintab3:
    # User Data
    User_agg = pd.read_csv("Data/aggregated/agg_Users.csv")
    User_states = pd.read_csv("Data/aggregated/state_agg_Users.csv")

    User_agg["Date"] = User_agg["Year"].astype(str) + User_agg["Quarter"].astype(str)
    User_agg["Date"] = pd.PeriodIndex(User_agg['Date'], freq='Q').strftime('%m-%Y')
    User_states["Date"] = User_states["Year"].astype(str) + User_states["Quarter"].astype(str)
    User_states["Date"] = pd.PeriodIndex(User_states['Date'], freq='Q').strftime('%m-%Y')

    # Years and Quarter dropdowns
    years = User_states["Year"].unique()
    st.header("Users Data")

    # Creating Columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        year_selected = st.selectbox("Select Year", years)
    with col2:
        quarters = User_states[User_states["Year"]==year_selected]["Quarter"].unique()
        quarter_selected = st.selectbox("Select Quarter", quarters, key="select_quarter")
    with col3:
        Phones = User_states[(User_states["Year"]==year_selected) & (User_states["Quarter"]==quarter_selected)]["Brand"].unique()
        phone_selected = st.selectbox("Select Phone", Phones)
    with col4:
        selected_col = st.selectbox("Select the columns:", ["Count", "App Open Percentage"], key="Columns3")
    
    # Creating Map
    if selected_col == "Count":
        title ="Number of Users"
    else:
        title ="App Opening % by users"

    col1, col2 = st.columns(2)
    with col1:
        m= folium.Map(location=(20.5937, 78.9629),prefer_canvas=True,  zoom_start=4, min_zoom=4, max_zoom=4,  tiles="cartodb positron")
        filtered_data = User_states[(User_states["Year"]==year_selected) & (User_states["Quarter"]==quarter_selected) & (User_states["Brand"]==phone_selected)]
        # creating a chloropeth map
        folium.Choropleth(
                        data=filtered_data,
                        geo_data=india_geo,
                        columns=['State', selected_col],
                        key_on="feature.properties.NAME_1",
                        tooltip=folium.GeoJsonTooltip(fields=['NAME_1', selected_col], labels=True, sticky=False),
                        highlight=True,
                        fill_color="PuOr",
                        fill_opacity=0.7,
                        line_opacity=0.5,
                        legend_name=title).add_to(m)
        components.html(m._repr_html_(), height=500)

    with col2:
        st.info(
                '''
                **Details of Chloropeth Map:**
                - More the color/shade varies towards purple, more Usage in given period.
                - We can change the Years, Quarters and Columns to see variety of Chloropeth Map.
                - The Columns options are Count of Users and App Opening %.
                - The Quarters are filtered based on Years.
                - Currently we have data upto 2022-Q1.
                - We can use filters to update the charts.
                '''
            )

    # Second Section
    st.header("Aggregated User Data Analysis")
    Aggtab1, Aggtab2, Aggtab3  = st.tabs(["Line Graph", "Column Graph", "Pie Graph"])

    with Aggtab1:
        # Columns
        Aggcol1, Aggcol2 = st.columns(2)

        with Aggcol1:
            # Line Graph
            filtered_data = User_agg[(User_agg["Brand"]==phone_selected)]
            fig = px.line(filtered_data, x="Date", y=selected_col, title=f'{selected_col} of {phone_selected} brand Users Using Phone-Pe App')
            fig.update_yaxes(range=[0,max(filtered_data[selected_col])*1.2])
            fig.update_layout(
                            xaxis_title = "Date",
                            yaxis_title=title,
                            title_x=0.2,  # Align title to the center horizontally,
                            title_y=0.9,
                            title_font_size=20,
                            font_size=10
                        )
            st.plotly_chart(fig, use_container_width=True)
        
        with Aggcol2:
            st.info(
                """
                **Details of Line Chart:**
                - Line chart is used to represent the trend of the data by each states.
                - X axis includes Date which combines Year and Quarter.
                - Y Axis represents count of Users.
                - Currently we have data upto 2022-Q1.
                - We can use filters to update the charts.
                    
                """
            )

            st.info(
                """
                **Important Observations:**
                - We can see a increasing trend on number of users in every Quarters.
                - We can see a declining trend in % of app openning.
                
                """
            )
    with Aggtab2:
        Aggcol1, Aggcol2 = st.columns(2)

        with Aggcol1:
            # Bar Chart with 2 Bars from 2 different
            fig = px.bar(filtered_data, x="Date", y=selected_col, title=f'{selected_col} of {phone_selected} brand Users Using Phone-Pe App')
            fig.update_yaxes(range=[0,max(filtered_data[selected_col])*1.2])
            fig.update_layout(
                        xaxis_title = "Date",
                        yaxis_title=title,
                        title_y=0.9,
                        title_x=0.2,  # Align title to the center horizontally,
                        title_font_size=20,
                        font_size=10
                    )
            st.plotly_chart(fig, use_container_width=True)

            
        with Aggcol2:
            # Bar Chart with 2 Bars from 2 different
            st.info(
                """
                **Details of Bar Chart:**
                - Bar chart is used to represent the trend of the data.
                - X axis includes Date which combines Year and Quarter.
                - Y Axis represents count of Users.
                - Currently we have data upto 2022-Q1.
                - We can use filters to update the charts.
                    
                """
            )

            st.info(
                """
                **Important Observations:**
                - We can see an increasing trend on number of users in every Quarters.
                - We can see a declining trend in % of app openning.
                
                """
            )
        with Aggtab3:
            Aggcol1, Aggcol2 = st.columns(2)
            with Aggcol1:
                # pie Chart
                Users_aggregated_filter = User_agg[(User_agg["Year"]==year_selected) & (User_agg["Quarter"]==quarter_selected)]
                fig = px.pie(Users_aggregated_filter, values=selected_col, names="Brand", title=f"{phone_selected} Brand users {selected_col} in {year_selected} - {quarter_selected}",hole=.4)
                
                st.plotly_chart(fig, use_container_width=True)

            with Aggcol2:
                st.info(
                    """
                    **Details of Pie Chart:**
                    - The plot was used to show breakdown of Users through Phone-pe app for Each District in Each States in each Quarters.
                    - We can use filters to update the charts.

                    """
                )

                st.info(
                    """
                    **Important Observations:**
                    - Xiaomi Brand Users are highest users in Phonepe Users & App Open Percentage.
                    """
                )

    # Third Section
    st.header("Aggregated User by State Data Analysis")
    states = User_states["State"].unique()
    # State Functions
    selected_state = st.selectbox("Select the State", states, key="States3")

    statetab1,statetab2,statetab3=st.tabs(["Line Graph", "Column Graph", "Pie Graph"])

    with statetab1:
        statecol1, statecol2 = st.columns(2)

        # Section Breakdown
        with statecol1:
            # Line Chart
            Users_states_filter = User_states[(User_states["State"]==selected_state) & (User_states["Brand"]==phone_selected) ]
            fig = px.line(Users_states_filter, x="Date", y=selected_col, title=f'{selected_col} of {phone_selected} brand Users Using Phone-Pe App in {selected_state}')
            fig.update_yaxes(range=[0,max(Users_states_filter[selected_col])*1.2])
            fig.update_layout(
                            xaxis_title = "Date",
                            yaxis_title=title,
                            title_x=0.2,  # Align title to the center horizontally,
                            title_y=0.9,
                            title_font_size=20,
                            font_size=10

                        )
            st.plotly_chart(fig, use_container_width=True)
        with statecol2:
            st.info(
                """
                **Details of Line Chart:**
                - Line chart is used to represent the trend of the data by each states.
                - X axis includes Date which combines Year and Quarter.
                - Y Axis represents count of Users.
                - Currently we have data upto 2022-Q1.
                - We can use filters to update the charts.
                """
            )

            st.info(
                """
                **Important Observations:**
                - We can see an increasing trend on number of users in every Quarters.
                - We can see a declining trend in % of app openning.

                """
            )
    with statetab2:
        statecol1, statecol2 = st.columns(2)
        with statecol1:

            # Section Breakdown
            fig = px.bar(Users_states_filter, x="Date", y=selected_col, title=f'{selected_col} of {phone_selected} brand Users Using Phone-Pe App in {selected_state}')
            fig.update_yaxes(range=[0,max(Users_states_filter[selected_col])*1.2])
            fig.update_layout(
                            xaxis_title = "Date",
                            yaxis_title=title,
                            title_y=0.9,
                            title_x=0.2,  # Align title to the center horizontally,
                            title_font_size=20,
                            font_size=10
                        )
            st.plotly_chart(fig, use_container_width=True)

        with statecol2:
            st.info(
                """
                **Details of Bar Chart:**

                - The bar graph shows the number of Users made accessed Phone-Pe App in each Quarter in each state.
                - X axis includes Date which combines Year and Quarter.
                - Y Axis represents total transactions in INR or total count of transaction for Transaction Types.
                - We can use filters to update the charts.
                
                """
            )

            st.info(
                """
                **Important Observations:**
                - We can see an increasing trend on number of users in every Quarters.
                - We can see a declining trend in % of app openning.

                """
            )
    with statetab3:
        statecol1, statecol2 = st.columns(2)
        with statecol1:
            # Section Breakdown
            # pie Chart
            Users_states_filter = User_states[(User_states["State"]==selected_state) & (User_states["Year"]==year_selected) & (User_states["Quarter"]==quarter_selected) ]
            
            fig = px.pie(Users_states_filter, values=selected_col, names="Brand", title=f"{phone_selected} Brand users {selected_col} in {year_selected} - {quarter_selected} in {selected_state}",hole=.4)
            
            st.plotly_chart(fig, use_container_width=True)
        
        with statecol2:
            st.info(
                """
                **Details of Pie Chart:**

                - The plot was used to show breakdown of Users through Phone-pe app for Each District in Each States in each Quarters.
                - We can use filters to update the charts.
                
                """
            )

            st.info(
                """
                **Important Observations:**
                - We can see an increasing trend on number of users in every Quarters.
                - We can see a declining trend in % of app openning.

                """
            )

    # Fourth Section
    st.header("Aggregated Transaction by Districts Data Analysis")
  
    Districttab1, Districttab2  = st.tabs(["Column Graph", "Pie Graph"])
    top_district = pd.read_csv("Data/top/Top_Districts_Users.csv")

    with Districttab1:
        Districtcol1, Districtcol2 = st.columns(2)
        with Districtcol1:
            filtered_data = top_district[(top_district["Year"]==year_selected) & (top_district["Quarter"]==quarter_selected) & (top_district["State"]==selected_state)]
            fig = px.bar(filtered_data, x="Registered Users", y="District", orientation="h", title=f'Districts in {selected_state} on {year_selected}-{quarter_selected}')
            fig.update_layout(
                        xaxis_title = title,
                        yaxis_title="District",
                        title_y=0.9,
                        title_x=0.2,  # Align title to the center horizontally,
                        title_font_size=20,
                        font_size=10,  
                        )

            st.plotly_chart(fig, use_container_width=True)
        
        with Districtcol2:
            st.info(
                """
                **Details of Bar graph Graph:**
                - This Horizontal Bar Graph, is used to show transaction for Each District in Each States in each Quarters.
                - We can use filters to update the charts.
                """
            )

            st.info(
                """
                **Important Observation:**
                - All the transactions types are in increasing trend in percentage for each Quarter in Districts.

                """
            )

    with Districttab2:
        Districtcol1, Districtcol2 = st.columns(2)
        with Districtcol1:
            filtered_data = top_district[(top_district["Year"]==year_selected) & (top_district["Quarter"]==quarter_selected) & (top_district["State"]==selected_state)]
            fig = px.pie(filtered_data, values="Registered Users", names="District", title=f"{year_selected} - {quarter_selected} District Breakdown in {selected_state}",hole=.4)
            st.plotly_chart(fig, use_container_width=True)

        with Districtcol2:
            st.info(
                """
                **Details of Pie Graph:**
                - The plot was used to show breakdown of Users Breakdown through Phone-pe app for Each District in Each States in each Quarters.
                - We can use filters to update the charts.
                """
            )

            

    