import datetime

import pandas as pd
import streamlit as st

from data_io import load_bookings_from_csv, save_bookings_to_csv
from desk_booking import (check_desk_bookings, check_team_desk_bookings,
                          collect_team_members, get_all_desk_bookings,
                          get_desk_availability)

# Replace with your actual API URL
url = "https://unityplace.smarttwin.app/UnityPlace/mobile-api/v1/bookingavailability/GetDesks"

# Fetch initial 'people' data from the API (Replace this with your actual API call)
people_data = []

def main():
    st.set_page_config(page_title="UP - Desk Booking Insights 🧑‍💻️💡", page_icon="💡")
    st.title("UP - Desk Booking Insights 🧑‍💻️💡")
    daily_desk_data = {}
    daily_desk_data_by_floor = {}

    with st.sidebar:
        # User inputs their token
        token = st.text_input("Enter your API token:", type="password")

        # Load bookings from CSV
        all_bookings = load_bookings_from_csv()

        # Adding a date range selector
        date_range = st.date_input("Select a date range:", [datetime.date.today(), datetime.date.today() + datetime.timedelta(days=3)])

        if len(date_range) == 2:
            start_date, end_date = date_range
        else:
            st.warning("Please select both a start and end date.")
        
        # Initialize session state for all_team_members and daily_desk_data_by_floor if they don't exist
        if 'all_team_members' not in st.session_state:
            st.session_state['all_team_members'] = []
        if 'daily_desk_data_by_floor' not in st.session_state:
            st.session_state['daily_desk_data_by_floor'] = {}

        if token:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            }

            if st.button("Fetch Booking Data"):
                all_bookings, all_team_members, daily_desk_data, daily_desk_data_by_floor = get_all_desk_bookings(url, headers, start_date=start_date, end_date=end_date)
                st.session_state['all_team_members'] = all_team_members  # Update session state
                st.session_state['all_bookings'] = all_bookings  # Update session state
                st.session_state['daily_desk_data_by_floor'] = daily_desk_data_by_floor  # Update session state
                st.write("✅ Booking data fetched successfully!")
            
            if st.button("Clear Cached Data"):
                get_all_desk_bookings.clear()

        st.header("How to find your API token:")
        st.markdown("""
        1. Log in to the [Unity Place web app](https://unityplace.smarttwin.app/webapp/).
        2. Right-click anywhere on the page and select "Inspect".
        3. In the Developer Tools panel, find and click on the "Network" tab.
        4. While the Network tab is open, click on the 'Desk Booking' option in the menu.
        5. Look through the list of network requests and find the one labelled 'GetDesks'. Click on it.
        6. With the API request selected, look for the "Headers" tab or section.
        7. The API token is found in the "Authorization" header.
        8. Select and copy the part of the "Authorization" header after "Bearer " - this is your API token.
        9. Paste the token into the field at the top of this section.
        """)

    tab1, tab2, tab3, tab4 = st.tabs(["Office Capacity", "Desk Availability", "People Finder", "Team Finder"])

    with tab1:
        st.markdown("""
                    Use the graphs below to quickly see how many desks are booked or available for each floor in the building within the selected date range.
                    """)
        # Add a table to display daily desk counts by floor
        for date, floors in st.session_state['daily_desk_data_by_floor'].items():  # Use session state
            st.subheader(date)
            floor_df = pd.DataFrame(floors.values(), index=floors.keys())
            floor_df['booked_desks'] = floor_df[['booked_desks_am', 'booked_desks_pm']].max(axis=1)
            floor_df['available_desks'] = floor_df['total_desks'] - floor_df['booked_desks']
            floor_df = floor_df[['booked_desks', 'available_desks']]
            st.bar_chart(floor_df)

    with tab2:
        st.title("Desk Availability (per Neighbourhood)")
        st.markdown("""
                    This tab allows you to check specific neighbourhood of desks for availability. Each date within the selected date range is displayed in a seperate expander. Expand a date to see the existing bookings for each day.
                    """)
        

        level6_neighbourhood_a_station = [
            "Desk 6.A01.1",
            "Desk 6.A01.2",
            "Desk 6.A01.3",
            "Desk 6.A01.4",
            "Desk 6.A01.5",
            "Desk 6.A01.6",
            "Desk 6.A01.7",
            "Desk 6.A01.8",
            "Desk 6.A02.1",
            "Desk 6.A02.2",
            "Desk 6.A02.3",
            "Desk 6.A02.4",
            "Desk 6.A03.1",
            "Desk 6.A03.2",
            "Desk 6.A03.3",
            "Desk 6.A03.4",
            "Desk 6.A04.1",
            "Desk 6.A04.2",
            "Desk 6.A04.3",
            "Desk 6.A04.4",
            "Desk 6.A05.1",
            "Desk 6.A05.2",
            "Desk 6.A05.3",
            "Desk 6.A05.4",
            "Desk 6.A06.1",
            "Desk 6.A06.2",
            "Desk 6.A06.3",
            "Desk 6.A06.4",
            "Desk 6.A06.5",
            "Desk 6.A06.6",
            "Desk 6.A06.7",
            "Desk 6.A06.8",
            "Desk 6.A07.1",
            "Desk 6.A07.2",
            "Desk 6.A07.3",
            "Desk 6.A07.4",
            "Desk 6.A07.5",
            "Desk 6.A07.6",
            "Desk 6.A07.7",
            "Desk 6.A07.8",
            "Desk 6.A08.1",
            "Desk 6.A08.2",
            "Desk 6.A08.3",
            "Desk 6.A08.4",
            "Desk 6.A08.5",
            "Desk 6.A08.6",
            "Desk 6.A08.7",
            "Desk 6.A08.8",
            "Desk 6.A09.1",
            "Desk 6.A09.2",
            "Desk 6.A09.3",
            "Desk 6.A09.4",
            "Desk 6.A09.5",
            "Desk 6.A09.6",
            "Desk 6.A09.7",
            "Desk 6.A09.8",
            "Desk 6.A10.1",
            "Desk 6.A10.2",
            "Desk 6.A10.3",
            "Desk 6.A10.4",
            "Desk 6.A11.1",
            "Desk 6.A11.2",
            "Desk 6.A11.3",
            "Desk 6.A11.4",
            "Desk 6.A12.1",
            "Desk 6.A12.2",
            "Desk 6.A12.3",
            "Desk 6.A12.4",
            "Desk 6.A12.5",
            "Desk 6.A12.6",
            "Desk 6.A12.7",
            "Desk 6.A12.8",
            "Desk 6.A21.1",
            "Desk 6.A21.2",
            "Desk 6.A21.3",
            "Desk 6.A21.4",
            "Desk 6.A21.5",
            "Desk 6.A21.6",
            "Desk 6.A21.7",
            "Desk 6.A21.8",
            "Desk 6.A22.1",
            "Desk 6.A22.2",
            "Desk 6.A22.3",
            "Desk 6.A22.4",
            "Desk 6.A22.5",
            "Desk 6.A22.6",
            "Desk 6.A22.7",
            "Desk 6.A22.8"
        ]

        level6_neighbourhood_a_city = [
            "Desk 6.A13.1",
            "Desk 6.A13.2",
            "Desk 6.A13.3",
            "Desk 6.A13.4",
            "Desk 6.A13.5",
            "Desk 6.A13.6",
            "Desk 6.A13.7",
            "Desk 6.A13.8",
            "Desk 6.A14.1",
            "Desk 6.A14.2",
            "Desk 6.A14.3",
            "Desk 6.A14.4",
            "Desk 6.A14.5",
            "Desk 6.A14.6",
            "Desk 6.A14.7",
            "Desk 6.A14.8",
            "Desk 6.A15.1",
            "Desk 6.A15.2",
            "Desk 6.A15.3",
            "Desk 6.A15.4",
            "Desk 6.A16.1",
            "Desk 6.A16.2",
            "Desk 6.A16.3",
            "Desk 6.A16.4",
            "Desk 6.A16.5",
            "Desk 6.A16.6",
            "Desk 6.A16.7",
            "Desk 6.A16.8",
            "Desk 6.A17.1",
            "Desk 6.A17.2",
            "Desk 6.A17.3",
            "Desk 6.A17.4",
            "Desk 6.A17.5",
            "Desk 6.A17.6",
            "Desk 6.A17.7",
            "Desk 6.A17.8",
            "Desk 6.A18.1",
            "Desk 6.A18.2",
            "Desk 6.A18.3",
            "Desk 6.A18.4",
            "Desk 6.A19.1",
            "Desk 6.A19.2",
            "Desk 6.A19.3",
            "Desk 6.A19.4",
            "Desk 6.A19.5",
            "Desk 6.A19.6",
            "Desk 6.A19.7",
            "Desk 6.A19.8",
            "Desk 6.A20.1",
            "Desk 6.A20.2",
            "Desk 6.A20.3",
            "Desk 6.A20.4",
            "Desk 6.A20.5",
            "Desk 6.A20.6",
            "Desk 6.A20.7",
            "Desk 6.A20.8"
        ]

        level6_neighbourhood_b_station = [
            "Desk 6.B01.1",
            "Desk 6.B01.2",
            "Desk 6.B01.3",
            "Desk 6.B01.4",
            "Desk 6.B02.1",
            "Desk 6.B02.2",
            "Desk 6.B02.3",
            "Desk 6.B02.4",
            "Desk 6.B03.1",
            "Desk 6.B03.2",
            "Desk 6.B03.3",
            "Desk 6.B03.4",
            "Desk 6.B03.5",
            "Desk 6.B03.6",
            "Desk 6.B03.7",
            "Desk 6.B03.8",
            "Desk 6.B04.1",
            "Desk 6.B04.2",
            "Desk 6.B04.3",
            "Desk 6.B04.4",
            "Desk 6.B04.5",
            "Desk 6.B04.6",
            "Desk 6.B04.7",
            "Desk 6.B04.8",
            "Desk 6.B05.1",
            "Desk 6.B05.2",
            "Desk 6.B05.3",
            "Desk 6.B05.4",
            "Desk 6.B06.1",
            "Desk 6.B06.2",
            "Desk 6.B06.3",
            "Desk 6.B06.4",
            "Desk 6.B07.1",
            "Desk 6.B07.2",
            "Desk 6.B07.3",
            "Desk 6.B07.4",
            "Desk 6.B08.1",
            "Desk 6.B08.2",
            "Desk 6.B08.3",
            "Desk 6.B08.4",
            "Desk 6.B17.1",
            "Desk 6.B17.2",
            "Desk 6.B17.3",
            "Desk 6.B17.4",
            "Desk 6.B17.5",
            "Desk 6.B17.6",
            "Desk 6.B17.7",
            "Desk 6.B17.8",
            "Desk 6.B18.1",
            "Desk 6.B18.2",
            "Desk 6.B18.3",
            "Desk 6.B18.4",
            "Desk 6.B18.5",
            "Desk 6.B18.6",
            "Desk 6.B18.7",
            "Desk 6.B18.8"
        ]

        level6_neighbourhood_b_city = [
            "Desk 6.B09.1",
            "Desk 6.B09.2",
            "Desk 6.B09.3",
            "Desk 6.B09.4",
            "Desk 6.B09.5",
            "Desk 6.B09.6",
            "Desk 6.B09.7",
            "Desk 6.B09.8",
            "Desk 6.B10.1",
            "Desk 6.B10.2",
            "Desk 6.B10.3",
            "Desk 6.B10.4",
            "Desk 6.B10.5",
            "Desk 6.B10.6",
            "Desk 6.B10.7",
            "Desk 6.B10.8",
            "Desk 6.B11.1",
            "Desk 6.B11.2",
            "Desk 6.B11.3",
            "Desk 6.B11.4",
            "Desk 6.B11.5",
            "Desk 6.B11.6",
            "Desk 6.B11.7",
            "Desk 6.B11.8",
            "Desk 6.B12.1",
            "Desk 6.B12.2",
            "Desk 6.B12.3",
            "Desk 6.B12.4",
            "Desk 6.B13.1",
            "Desk 6.B13.2",
            "Desk 6.B13.3",
            "Desk 6.B13.4",
            "Desk 6.B14.1",
            "Desk 6.B14.2",
            "Desk 6.B14.3",
            "Desk 6.B14.4",
            "Desk 6.B14.5",
            "Desk 6.B14.6",
            "Desk 6.B14.7",
            "Desk 6.B14.8",
            "Desk 6.B15.1",
            "Desk 6.B15.2",
            "Desk 6.B15.3",
            "Desk 6.B15.4",
            "Desk 6.B15.5",
            "Desk 6.B15.6",
            "Desk 6.B15.7",
            "Desk 6.B15.8",
            "Desk 6.B16.1",
            "Desk 6.B16.2",
            "Desk 6.B16.3",
            "Desk 6.B16.4",
            "Desk 6.B16.5",
            "Desk 6.B16.6",
            "Desk 6.B16.7",
            "Desk 6.B16.8"
        ]

        level6_neighbourhood_c_station = [
            "Desk 6.C01.1",
            "Desk 6.C01.2",
            "Desk 6.C01.3",
            "Desk 6.C01.4",
            "Desk 6.C01.5",
            "Desk 6.C01.6",
            "Desk 6.C01.7",
            "Desk 6.C01.8",
            "Desk 6.C02.1",
            "Desk 6.C02.2",
            "Desk 6.C02.3",
            "Desk 6.C02.4",
            "Desk 6.C03.1",
            "Desk 6.C03.2",
            "Desk 6.C03.3",
            "Desk 6.C03.4",
            "Desk 6.C04.1",
            "Desk 6.C04.2",
            "Desk 6.C04.3",
            "Desk 6.C04.4",
            "Desk 6.C05.1",
            "Desk 6.C05.2",
            "Desk 6.C05.3",
            "Desk 6.C05.4",
            "Desk 6.C06.1",
            "Desk 6.C06.2",
            "Desk 6.C06.3",
            "Desk 6.C06.4",
            "Desk 6.C06.5",
            "Desk 6.C06.6",
            "Desk 6.C06.7",
            "Desk 6.C06.8",
            "Desk 6.C07.1",
            "Desk 6.C07.2",
            "Desk 6.C07.3",
            "Desk 6.C07.4",
            "Desk 6.C08.1",
            "Desk 6.C08.2",
            "Desk 6.C08.3",
            "Desk 6.C08.4",
            "Desk 6.C09.1",
            "Desk 6.C09.2",
            "Desk 6.C09.3",
            "Desk 6.C09.4",
            "Desk 6.C09.5",
            "Desk 6.C09.6",
            "Desk 6.C09.7",
            "Desk 6.C09.8",
            "Desk 6.C10.1",
            "Desk 6.C10.2",
            "Desk 6.C10.3",
            "Desk 6.C10.4",
            "Desk 6.C10.5",
            "Desk 6.C10.6",
            "Desk 6.C10.7",
            "Desk 6.C10.8"
        ]
        
        level6_neighbourhood_d_station = [
            "Desk 6.D01.1",
            "Desk 6.D01.2",
            "Desk 6.D01.3",
            "Desk 6.D01.4",
            "Desk 6.D01.5",
            "Desk 6.D01.6",
            "Desk 6.D01.7",
            "Desk 6.D01.8",
            "Desk 6.D02.1",
            "Desk 6.D02.2",
            "Desk 6.D02.3",
            "Desk 6.D02.4",
            "Desk 6.D03.1",
            "Desk 6.D03.2",
            "Desk 6.D03.3",
            "Desk 6.D03.4",
            "Desk 6.D04.1",
            "Desk 6.D04.2",
            "Desk 6.D04.3",
            "Desk 6.D04.4",
            "Desk 6.D04.5",
            "Desk 6.D04.6",
            "Desk 6.D04.7",
            "Desk 6.D04.8",
            "Desk 6.D05.1",
            "Desk 6.D05.2",
            "Desk 6.D05.3",
            "Desk 6.D05.4",
            "Desk 6.D05.5",
            "Desk 6.D05.6",
            "Desk 6.D05.7",
            "Desk 6.D05.8",
            "Desk 6.D06.1",
            "Desk 6.D06.2",
            "Desk 6.D06.3",
            "Desk 6.D06.4",
            "Desk 6.D07.1",
            "Desk 6.D07.2",
            "Desk 6.D07.3",
            "Desk 6.D07.4",
            "Desk 6.D08.1",
            "Desk 6.D08.2",
            "Desk 6.D08.3",
            "Desk 6.D08.4",
            "Desk 6.D08.5",
            "Desk 6.D08.6",
            "Desk 6.D08.7",
            "Desk 6.D08.8",
            "Desk 6.D16.1",
            "Desk 6.D16.2",
            "Desk 6.D16.3",
            "Desk 6.D16.4",
            "Desk 6.D16.5",
            "Desk 6.D16.6",
            "Desk 6.D16.7",
            "Desk 6.D16.8",
            "Desk 6.D17.1",
            "Desk 6.D17.2",
            "Desk 6.D17.3",
            "Desk 6.D17.4",
            "Desk 6.D17.5",
            "Desk 6.D17.6",
            "Desk 6.D17.7",
            "Desk 6.D17.8"
        ]
        
        level6_neighbourhood_d_city = [
            "Desk 6.D09.1",
            "Desk 6.D09.2",
            "Desk 6.D09.3",
            "Desk 6.D09.4",
            "Desk 6.D09.5",
            "Desk 6.D09.6",
            "Desk 6.D09.7",
            "Desk 6.D09.8",
            "Desk 6.D10.1",
            "Desk 6.D10.2",
            "Desk 6.D10.3",
            "Desk 6.D10.4",
            "Desk 6.D11.1",
            "Desk 6.D11.2",
            "Desk 6.D11.3",
            "Desk 6.D11.4",
            "Desk 6.D11.5",
            "Desk 6.D11.6",
            "Desk 6.D11.7",
            "Desk 6.D11.8",
            "Desk 6.D12.1",
            "Desk 6.D12.2",
            "Desk 6.D12.3",
            "Desk 6.D12.4",
            "Desk 6.D12.5",
            "Desk 6.D12.6",
            "Desk 6.D12.7",
            "Desk 6.D12.8",
            "Desk 6.D13.1",
            "Desk 6.D13.2",
            "Desk 6.D13.3",
            "Desk 6.D13.4",
            "Desk 6.D14.1",
            "Desk 6.D14.2",
            "Desk 6.D14.3",
            "Desk 6.D14.4",
            "Desk 6.D14.5",
            "Desk 6.D14.6",
            "Desk 6.D14.7",
            "Desk 6.D14.8",
            "Desk 6.D15.1",
            "Desk 6.D15.2",
            "Desk 6.D15.3",
            "Desk 6.D15.4",
            "Desk 6.D15.5",
            "Desk 6.D15.6",
            "Desk 6.D15.7",
            "Desk 6.D15.8"
        ]

        
        
        NEIGHBOURHOODS = {
            "Level 6": {
                "A (Station)": level6_neighbourhood_a_station,
                "A (City)": level6_neighbourhood_a_city,
                "B (Station)": level6_neighbourhood_b_station,
                "B (City)": level6_neighbourhood_b_city,
                "C (Station)": level6_neighbourhood_c_station,
                "D (Station)": level6_neighbourhood_d_station,
                "D (City)": level6_neighbourhood_d_city,
            }
        }

        
        
        col1, col2 = st.columns(2)

        with col1:
            selected_floor = st.selectbox("Select a floor:", list(NEIGHBOURHOODS.keys()), placeholder="Select a floor", label_visibility="hidden")
        
        with col2:
            selected_neighbourhood = st.selectbox("Select a neighbourhood:", list(NEIGHBOURHOODS[selected_floor].keys()), placeholder="Select a neighbourhood", label_visibility="hidden")

        
        st.warning("Only desks in Level 6 neighbourhoods are currently supported.")
        if st.button("Check Desk Availability"):
            selected_desks = NEIGHBOURHOODS[selected_floor][selected_neighbourhood]
            df = get_desk_availability(selected_desks, st.session_state['all_bookings'], start_date, end_date)
            st.session_state['df'] = df  # Store the DataFrame in the session state

            # Convert 'date' column to pandas Timestamp objects
            df['date'] = pd.to_datetime(df['date'])

            # Get all unique dates from the DataFrame
            dates = df['date'].unique()

            # Create an expander for each date and put the data for that date inside it
            for date in dates:
                # Convert the numpy.datetime64 object to a pandas.Timestamp object
                date = pd.Timestamp(date)

                with st.expander(f"{date.strftime('%Y-%m-%d')} ({len(df[(df['date'] == date) & (df['availability'] == 'Available')])} desks available)"):
                    filtered_df = df[df['date'] == date]
                    st.table(filtered_df)
    

    with tab3:
        st.markdown("""
                    This tab allows you to select one or more colleagues and check their desk bookings for the selected date range.

                    If an individual's name is not listed, it means they have not booked a desk within the selected date range.
                    """)
        # Create a dropdown list of all team members for the user to select from
        selected_team_members = st.multiselect('Select team members:', st.session_state['all_team_members'])

        if st.button("Check Desk Bookings"):
            # Pass the selected start_date and end_date to your booking checking function
            check_desk_bookings(selected_team_members, st.session_state['all_bookings'], st, start_date, end_date)  # Use session state 


    with tab4:
        st.markdown("""
                    This tab allows you to upload a CSV file containing the names of team members. 
                    It will then display a table showing whether or not they're in the office on the selected dates.

                    This should be useful for Managers, or those arranging in-person meetings, who want to quickly check which people in a group are in the office on a given day.
                    """)

        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

        st.info("""
        * Each name in the CSV file must match the name of a person recorded in the Unity Place system. If the name is not an exact match, the desk will not be included in the results.
        * The CSV file must contain a single column of names, with no header row. Each row must end with a comma. For example:
        ```
        Elon Musk,
        Jeff Bezos,
        Bill Gates,
        ```
        """)

        if uploaded_file is not None:
            team_df = pd.read_csv(uploaded_file)
            team_members = team_df.iloc[:, 0].tolist()  # assuming names are in the first column

            # Check if any of the team members have bookings
            booked_team_members = set(team_members) & set(st.session_state['all_bookings'].keys())
            if booked_team_members:
                st.subheader("Desk bookings specified team members:")
                check_team_desk_bookings(booked_team_members, st.session_state['all_bookings'], st, start_date, end_date)
            else:
                st.write("None of the team members specified have desk bookings in the selected date range.")


if __name__ == "__main__":
    main()