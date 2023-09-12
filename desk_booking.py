import datetime

import pandas as pd
import requests
import streamlit as st


# Function to get all desk bookings for a given date range
@st.cache_data(show_spinner="Fetching desk booking data...")
def get_all_desk_bookings(url, headers, start_date, end_date):
    all_bookings = {}
    all_team_members = set()
    daily_desk_data = {}  
    daily_desk_data_by_floor = {}  

    delta = (end_date - start_date).days
    for i in range(delta + 1):

        current_date = (start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        payload = {
            "buildingId": "",
            "startDate": f"{current_date}T00:00:00",
            "endDate": f"{current_date}T23:59:59"
        }
        try:  # try to make the request
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:  # catch any RequestException
            st.error("Unable to fetch booking data, please try again later.")
            st.stop()
        response_data = response.json()

        for floor in response_data.get('floors', []):
            total_desks = len(floor.get('desks', []))  
            booked_desks = 0  
            booked_desks_morning = set()  
            booked_desks_afternoon = set()  

            for desk in floor.get('desks', []):
                for slot in desk.get('timeSlots', []):
                    if slot['user']:  # only consider slots that are booked
                        user_name = slot['user']['name']  # get the user's name
                        all_team_members.add(user_name)
                        if user_name not in all_bookings:
                            all_bookings[user_name] = []
                        all_bookings[user_name].append({
                            'date': current_date,
                            'desk': desk['name'],
                            'startTime': slot['startTime'],
                            'endTime': slot['endTime'],
                            'availability': slot['availability'],
                        })

                        if '00:00:00' <= slot['startTime'] < '13:00:00':
                            booked_desks_morning.add(desk['id'])  
                        elif '13:00:00' <= slot['startTime'] < '24:00:00':
                            booked_desks_afternoon.add(desk['id']) 

                booked_desks_am = len(booked_desks_morning)  
                booked_desks_pm = len(booked_desks_afternoon)

            if current_date not in daily_desk_data_by_floor:
                daily_desk_data_by_floor[current_date] = {}
            daily_desk_data_by_floor[current_date][floor['floorName']] = {'total_desks': total_desks, 'booked_desks_am': booked_desks_am, 'booked_desks_pm': booked_desks_pm}

    return all_bookings, sorted(list(all_team_members)), daily_desk_data, daily_desk_data_by_floor


# Function to collect team member names based on actual bookings
def collect_team_members(all_bookings):
    team_members = []
    
    while True:
        name = input("Enter a team member's name (or type 'done' to finish): ")
        if name.lower() == 'done':
            break
        elif name in all_bookings:
            team_members.append(name)
        else:
            print("Invalid name. Please try again.")
    
    return team_members



# Function to check desk bookings for selected team members
def check_desk_bookings(team_members, all_bookings, st, start_date, end_date):
    for name in team_members:
        st.subheader(f"Bookings for {name}:")
        daily_bookings = {}
        for booking in all_bookings.get(name, []):
            booking_date = datetime.datetime.strptime(booking['date'], '%Y-%m-%d').date()
            if start_date <= booking_date <= end_date:
                start_time = datetime.datetime.strptime(booking['startTime'], '%H:%M:%S').time()
                end_time = datetime.datetime.strptime(booking['endTime'], '%H:%M:%S').time()

                booking_period = ""
                if start_time <= datetime.datetime.strptime('00:00:00', '%H:%M:%S').time() and end_time >= datetime.datetime.strptime('23:59:00', '%H:%M:%S').time():
                    booking_period = "All Day"
                elif end_time <= datetime.datetime.strptime('13:00:00', '%H:%M:%S').time():
                    booking_period = "Morning Only"
                elif start_time >= datetime.datetime.strptime('13:00:00', '%H:%M:%S').time():
                    booking_period = "Afternoon Only"
                
                if booking_date not in daily_bookings or booking_period == "All Day":
                    daily_bookings[booking_date] = {
                        'date': booking['date'],
                        'desk': booking['desk'],
                        'bookingPeriod': booking_period,
                        'name': name
                    }

        bookings_list = list(daily_bookings.values())
        if bookings_list:
            df = pd.DataFrame(bookings_list)
            st.table(df[['date', 'desk', 'bookingPeriod']])
        else:
            st.write("No bookings found for this date range.")



def check_team_desk_bookings(team_members, all_bookings, st, start_date, end_date):
    bookings_by_date = {}

    for name in team_members:
        daily_bookings = {}
        for booking in all_bookings.get(name, []):
            booking_date = datetime.datetime.strptime(booking['date'], '%Y-%m-%d').date()
            if start_date <= booking_date <= end_date:
                start_time = datetime.datetime.strptime(booking['startTime'], '%H:%M:%S').time()
                end_time = datetime.datetime.strptime(booking['endTime'], '%H:%M:%S').time()

                booking_period = ""
                if start_time <= datetime.datetime.strptime('00:00:00', '%H:%M:%S').time() and end_time >= datetime.datetime.strptime('23:59:00', '%H:%M:%S').time():
                    booking_period = "All Day"
                elif end_time <= datetime.datetime.strptime('13:00:00', '%H:%M:%S').time():
                    booking_period = "Morning Only"
                elif start_time >= datetime.datetime.strptime('13:00:00', '%H:%M:%S').time():
                    booking_period = "Afternoon Only"
                
                if booking_date not in daily_bookings or booking_period == "All Day":
                    daily_bookings[booking_date] = {
                        'date': booking['date'],
                        'desk': booking['desk'],
                        'bookingPeriod': booking_period,
                        'name': name
                    }
        
        for date, booking in daily_bookings.items():
            if date not in bookings_by_date:
                bookings_by_date[date] = []
            bookings_by_date[date].append(booking)

    for date, bookings in bookings_by_date.items():
        st.subheader(f"Bookings for {date.strftime('%Y-%m-%d')}:")

        bookings_list = bookings
        if bookings_list:
            df = pd.DataFrame(bookings_list)
            st.table(df[['date', 'name', 'desk', 'bookingPeriod']])
        else:
            st.write("No bookings found for this date.")
    


def get_desk_availability(desk_names, all_bookings, start_date, end_date):
    desk_availability = []
    for name, bookings in all_bookings.items():
        for booking in bookings:
            if booking['desk'] in desk_names:
                booking['name'] = name
                desk_availability.append(booking)
    df = pd.DataFrame(desk_availability)
    df = df[['date', 'desk', 'name', 'availability']]
    
    # Assuming that if a desk is booked by the same person on the same day in the morning and afternoon, it's a single booking
    df['date'] = pd.to_datetime(df['date'])
    df = df.groupby(['date', 'desk', 'name']).agg({'availability': 'first'}).reset_index()
    
    # Create a DataFrame with all possible combinations of dates and desks
    date_range = pd.date_range(start_date, end_date)
    all_combinations = pd.MultiIndex.from_product([date_range, desk_names], names=['date', 'desk'])
    all_df = pd.DataFrame(index=all_combinations).reset_index()
    
    # Merge the DataFrame with all combinations with the actual bookings, filling in gaps with "Available"
    merged_df = pd.merge(all_df, df, on=['date', 'desk'], how='left')
    merged_df['availability'].fillna('Available', inplace=True)
    merged_df['name'].fillna('', inplace=True)
    
    # Sort by date and then desk
    merged_df = merged_df.sort_values(['date', 'desk'])

    return merged_df