import time
import pandas as pd
import numpy as np
import json

# Constants for city data
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv'
}

# Spinning text animation class for loading visuals
class Spinner:
     """
    here
        Animates a spinning text visual to simulate a loading spinner.

        Args:
            string (str): The text message to display during the spin.
            iterations (int): Number of times the spinner will cycle through the animation. here
        """
    def spin(self, string, iterations):
        clear = "\b" * (8 + len(string))
        for _ in range(iterations):
            for ch in '-\\|/':
                print(f'__({ch}){string}({ch})__', end='', flush=True)
                time.sleep(0.1)
                print(clear, end='', flush=True)

def print_spinner(message, iterations):
    spinner = Spinner()
    spinner.spin(message, iterations)

# Function to get user input filters
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns: (str) city, (str) month, (str) day
    """
    print('\n')
    print_spinner('Bikeshare', 8)
    print('_(/)_Bikeshare_(/)'.center(78, '_'))
    print('Hello! Let\'s explore some US bikeshare data!'.center(78, '='))

    # City filter
    city_filter = ['chicago', 'new york', 'washington']
    city = input_choice("city", city_filter, "Chicago, New York or Washington")

    # Month filter
    month_filter = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input_choice("month", month_filter, "all, january, february, march, etc.")

    # Day filter
    day_filter = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    day = input_choice("day of the week", day_filter, "all, sunday, monday, etc.")

    print('-'*78)
    return city, month, day

def input_choice(filter_type, valid_options, prompt):
    """
    Helper function to handle input validation for filters.
    """
    choice = None
    while choice not in valid_options:
        choice = input(f"\nFilter data by {filter_type}\n[{prompt}] : ").lower()
    return choice

# Function to load data based on filters
def load_data(city, month, day):
    """
    Loads and filters bikeshare data based on user input.
    Args: (str) city, (str) month, (str) day
    Returns: df (Pandas DataFrame)
    """
    print("\nFilters applied: [{}]".format(", ".join([city, month, day]).center(78, '*')))
    if city == 'washington':
        print("Warning: Washington dataset lacks 'Gender' and 'Birth Year' information.")

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(month) + 1
        df = df[df['month'] == month_index]

    # Filter by day
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

# Function to display time statistics
def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    """
    print('\nCalculating The Most Frequent Times of Travel'.center(78, '='))
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    print('Most common Month'.ljust(40, '.'), df['month'].mode()[0])
    print('Most common Day'.ljust(40, '.'), df['day_of_week'].mode()[0])
    print('Most common Start Hour'.ljust(40, '.'), df['Start Time'].dt.hour.mode()[0])

    print(f"\nThis took {time.time() - start_time:.4f} seconds.")
    print('-'*78)

# Function to display station statistics
def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    """
    print('\nCalculating The Most Popular Stations and Trip'.center(78, '='))
    start_time = time.time()

    if 'Start Station' in df.columns:
        print('Most common Start Station'.ljust(40, '.'), df['Start Station'].mode()[0])

    if 'End Station' in df.columns:
        print('Most common End Station'.ljust(40, '.'), df['End Station'].mode()[0])

    if 'Start Station' in df.columns and 'End Station' in df.columns:
        df['route'] = df['Start Station'] + ' -> ' + df['End Station']
        print('Most common route'.ljust(40, '.'), df['route'].mode()[0])

    print(f"\nThis took {time.time() - start_time:.4f} seconds.")
    print('-'*78)

# Function to display trip duration statistics
def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    """
    print('\nCalculating Trip Duration'.center(78, '='))
    start_time = time.time()
    try:
        if 'Trip Duration' in df.columns:
            print('Max Travel Time'.ljust(40, '.'), df['Trip Duration'].max())
            print('Min Travel Time'.ljust(40, '.'), df['Trip Duration'].min())
            print('Avg Travel Time'.ljust(40, '.'), df['Trip Duration'].mean())
            print('Total Travel Time'.ljust(40, '.'), df['Trip Duration'].sum())
        else:
            print("Error: 'Trip Duration' column is missing from the dataset.")
    except Exception as e:
        print(f"Exception occurred while calculating trip duration: {e}")

    print(f"\nThis took {time.time() - start_time:.4f} seconds.")
    print('-'*78)

# Function to display user statistics
def user_stats(df):
    """
    Displays statistics on bikeshare users.
    """
    print('\nCalculating User Stats'.center(78, '='))
    start_time = time.time()

    if 'User Type' in df.columns:
        print('User Types:'.center(78, '-'))
        print(df['User Type'].value_counts())

    if 'Gender' in df.columns:
        print('Gender Stats:'.center(78, '-'))
        df['Gender'].fillna('Not disclosed', inplace=True)
        print(df['Gender'].value_counts())

    if 'Birth Year' in df.columns:
        print('Birth Year Stats:'.center(78, '-'))
        print('Earliest Birth Year'.ljust(40, '.'), int(df['Birth Year'].min()))
        print('Most Recent Birth Year'.ljust(40, '.'), int(df['Birth Year'].max()))
        print('Most Common Birth Year'.ljust(40, '.'), int(df['Birth Year'].mode()[0]))

    print(f"\nThis took {time.time() - start_time:.4f} seconds.")
    print('-'*78)

# Main function to run the program
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Display raw data if requested
        row = 5
        while input('\nWould you like to see raw data? (yes/no): ').lower() == 'yes':
            print(df.head(row).to_dict('index'))
            row += 5

        if input('\nWould you like to restart? (yes/no): ').lower() != 'yes':
            print('Python Script Terminated'.center(78, '*'))
            break

if __name__ == "__main__":
    main()

