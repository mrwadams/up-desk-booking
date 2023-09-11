import pandas as pd
import os

# Add this function to save bookings to a CSV file
def save_bookings_to_csv(all_bookings, filename="all_bookings.csv"):
    bookings_list = []
    for name, bookings in all_bookings.items():
        for booking in bookings:
            booking["name"] = name
            bookings_list.append(booking)
    
    df = pd.DataFrame(bookings_list)
    df.to_csv(filename, index=False)



# Add this function to load bookings from a CSV file
def load_bookings_from_csv(filename="all_bookings.csv"):
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        all_bookings = {}
        for _, row in df.iterrows():
            name = row['name']
            if name not in all_bookings:
                all_bookings[name] = []
            all_bookings[name].append({
                'date': row['date'],
                'desk': row['desk'],
                'startTime': row['startTime'],
                'endTime': row['endTime']
            })
        return all_bookings
    else:
        return {}