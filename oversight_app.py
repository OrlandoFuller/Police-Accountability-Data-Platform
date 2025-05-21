# import necessary libraries
import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Oversight App", 
                   page_icon=":guardsman:", 
                   layout="wide")

# Helper function to load data
@st.cache_data
def load_data():
    data = pd.read_excel("dataset/police_complaints.xlsx")
    return data

def create_metric_chart(data, chart_type, y=None, column=None, height=150):
    if chart_type == 'bar':
        st.bar_chart(data=data, y=y, height=height)
    elif chart_type=='bullet':
        for i in data:
            st.markdown(i[0])
   
           
# display metrics function
def display_metrics(col, subheader, data, chart_type, column = None, y= None, value=None):
    with col:
        with st.container(border=True):
            st.metric(label=subheader, value=value)
            create_metric_chart(data=data, y=None, column=None, chart_type=chart_type, height=150)

            


# Load data
data = load_data()

# Title of the app
with st.sidebar:
    st.title("Oversight App")
    st.write("This is a simple oversight app to monitor and manage police complaints.")
    st.write("")

    # Date filter
    st.write("Adjust the dates below to filter complaints by date.")

    
    
    

    max_date = data['date_received'].max()
    min_date = data['date_received'].min()

    start_date = st.date_input("Start Date",value=min_date, min_value=min_date, max_value=max_date)
    end_date = st.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

    
    data = data[(data['date_received'] >= pd.to_datetime(start_date)) & (data['date_received'] <= pd.to_datetime(end_date))]
    
    # Gender filter
    st.write("Uncheck the boxes below to filter complaints by gender.")
    st.write("Note: If both boxes are unchecked, all complaints will be shown.")
    
    include_males = st.checkbox("Include Males", value=True)
    include_females = st.checkbox("Include Females", value=True)
    include_non_binary = st.checkbox("Include Non-Binary", value=True)

    # Collect genders to include based on checkboxes
    genders_to_include = []
    if include_males:
        genders_to_include.append('Male')
    if include_females:
        genders_to_include.append('Female')
    if include_non_binary:
        genders_to_include.append('Non-binary')

    # Filter data if any genders are selected
    if genders_to_include:
        data = data[data['complainant_gender'].isin(genders_to_include)]

# Dashboard section
st.title("Complaints Dashboard")


#  make a subheader for the date range
st.write(f"Complaints from {start_date} to {end_date}")

cols  = st.columns(3)

# Display total number of complaints    
number_of_complaints = data['complaint_id'].nunique()

complaints_graph_data = data[['date_received','complaint_id']]
complaints_graph_data['year'] = complaints_graph_data['date_received'].dt.year
complaints_graph_data = complaints_graph_data.groupby('year').count()
complaints_graph_data = complaints_graph_data.rename(columns={'complaint_id': 'number_of_complaints'})
complaints_graph_data = complaints_graph_data['number_of_complaints']

display_metrics(col=cols[0], 
                subheader="Total Complaints", 
                data=complaints_graph_data, 
                chart_type='bar', 
                y= 'number_of_complaints', 
                value=number_of_complaints)

precincts_involved = data['precinct'].nunique()

complaints_graph_data = data[['precinct']].value_counts().index


display_metrics(col=cols[1], 
                subheader="Total Precincts Involved", 
                data=complaints_graph_data, 
                chart_type="bullet", 
                column = 0, 
                y= None, 
                value=precincts_involved)
# Display total number of officers involved



number_of_officers = data['officer_id'].nunique()

complaints_graph_data = data[['date_received', 'officer_id']]
complaints_graph_data['year'] = complaints_graph_data['date_received'].dt.year
complaints_graph_data = complaints_graph_data.groupby('year')['officer_id'].nunique()
complaints_graph_data = complaints_graph_data.rename('number_of_officers')


display_metrics(col = cols[2], 
                subheader = "Total Officers Involved", 
                data = complaints_graph_data, 
                chart_type = 'bar', 
                column = None, 
                y= number_of_officers, 
                value=number_of_officers)

# Display total number of complaints with use of force
row1  = st.columns(3)

use_of_force_complaints = data[data['use_of_force_involved'] == True]['complaint_id'].count()

complaints_graph_data = data[['date_received', 'use_of_force_involved']]
complaints_graph_data['year'] = complaints_graph_data['date_received'].dt.year
complaints_graph_data = complaints_graph_data.groupby('year')['use_of_force_involved'].sum()    

display_metrics(col = row1[0], 
                subheader = "Total Complaints with Use of Force", 
                data = complaints_graph_data, 
                chart_type = 'bar', 
                column = None, 
                y= use_of_force_complaints, 
                value=use_of_force_complaints)

resolved_complaints = data[data['resolution'] != 'Pending']['resolution'].count()
complaints_graph_data = data[data['resolution'] != 'Pending'][['date_received', 'resolution']]
complaints_graph_data['year'] = complaints_graph_data['date_received'].dt.year
complaints_graph_data = complaints_graph_data.groupby('year').count()
complaints_graph_data = complaints_graph_data.rename(columns={'resolution': 'resolved_complaints'})
complaints_graph_data = complaints_graph_data['resolved_complaints']

display_metrics(col = row1[1], 
                subheader = "Resolved Complaints", 
                data = complaints_graph_data, 
                chart_type = 'bar', 
                column = None, 
                y= resolved_complaints, 
                value=resolved_complaints)


unresolved_complaints = data[data['resolution'] == 'Pending']['resolution'].count()
complaints_graph_data = data[data['resolution'] == 'Pending'][['date_received', 'resolution']]
complaints_graph_data['year'] = complaints_graph_data['date_received'].dt.year
complaints_graph_data = complaints_graph_data.groupby('year').count()
complaints_graph_data = complaints_graph_data.rename(columns={'resolution': 'unresolved_complaints'})
complaints_graph_data = complaints_graph_data['unresolved_complaints']


display_metrics(col = row1[2], 
                subheader = "Unresolved Complaints", 
                data = complaints_graph_data, 
                chart_type = 'bar', 
                column = None, 
                y= unresolved_complaints, 
                value=unresolved_complaints)


# st.title("Breakdown by precinct")
# precincts = data['precinct'].value_counts().keys().sort_values()
# # precinct_count = len(data[data['precinct'] == precincts[0]]['complaint_type'].value_counts())
# complaint_types = data['complaint_type'].value_counts().keys()


# for p in precincts:
#     precinct_data = data[data['precinct'] == p]
#     st.subheader(p)
#     cols = st.columns(len(complaint_types))
#     count = 0 
#     for c in complaint_types:
#         if count < len(cols):
#             complaint_type_data = precinct_data[precinct_data['complaint_type'] == c]
#             num = complaint_type_data.shape[0]
#             display_metrics(col = cols[count],subheader = c, data=data, value = num)
#             count += 1    

with st.expander('See Filtered DataFrame'):
    st.write(data)