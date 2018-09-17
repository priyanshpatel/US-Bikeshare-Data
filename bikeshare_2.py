import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Arguments: None
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    global CITY_DATA
    city_lower = ''
    while city_lower not in CITY_DATA.keys():
        city = input('Enter the city\'s name for which you want to see the bikeshare data of: New York City, Chicago or Washington?\n')
        city_lower = city.lower()
        if city_lower in CITY_DATA.keys():
           city = city_lower
        else :
            print('Please enter either New York, Chicago or Washington.\n')
    # TO DO: get user input for month (all, january, february, ... , june)
    month_lower = ''
    months = ['january','february','march','april','may','june','all']
    while month_lower not in months:
        month = input('For which month would you like to see the data for? January, February, March, April, May, June or all?\n')
        month_lower = month.lower()
        if month_lower in months:
            month = month_lower
        else:
            print('Please enter a month between January and June. Enter "all" if you want to see the data for all months.\n')
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']
    day_lower = ''
    while day_lower not in days:
        day = input('For which day would you like to see the data for? Enter "all" if you would like to see the data for all days.\n')
        day_lower = day.lower()
        if day_lower not in days:
            print('Please enter a valid day. Enter "all" if you want to see the data for all days.\n')
        else:
            day = day_lower
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january','february','march','april','may','june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    months = ['january','february','march','april','may','june']
    print('\nMost common month: {} (Count: {})'.format(months[common_month-1].title(),df['month'].value_counts().tolist()[0]))

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('\nMost common day of week: {} (Count: {})'.format(common_day,df['day_of_week'].value_counts().tolist()[0]))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('\nMost commonly used start station: '+ common_start_station+ ' (Count: '+str(df['Start Station'].value_counts().tolist()[0])+')')

    # TO DO: display most commonly used end station
    commmon_end_station = df['End Station'].mode()[0]
    print('\nMost commonly used end station: {} (Count: {})'.format(common_start_station, df['End Station'].value_counts().tolist()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] +' - '+ df['End Station']
    frequent_combination = df['combination'].mode()[0]
    print('\nMost frequent combination of start station and end station trip: {} (Count: {})'.format(frequent_combination, df['combination'].value_counts().tolist()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print('\nTotal travel time: '+str(total_trip_duration)+' seconds')
    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nMean travel time: '+str(mean_travel_time)+' seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('\nNumber of user type: \n'+str(df['User Type'].value_counts().rename_axis(None).rename(None)))

    if city != 'washington':
    # TO DO: Display counts of gender
        print('\nCounts of gender: \n'+str(df['Gender'].value_counts().rename_axis(None).rename(None)))

    # TO DO: Display earliest, most recent, and most common year of birth
        print('\nEarliest birth year: '+str(int(df['Birth Year'].min())))
        print('\nMost recent birth year: '+str(int(df['Birth Year'].max())))
        print('\nMost common birth year: {} (Count: {})'.format(int(df['Birth Year'].mode()[0]), df['Birth Year'].value_counts().tolist()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    """
    Displays raw data from csv file.

    Arg(s): df - Pandas DataFrame containing city data filtered by month and day

    Returns: None
    """

    row_count = 0
    df = df.drop(['month', 'day_of_week', 'hour', 'combination'], axis = 1)
    total_rows = df.shape[0]
    view_data = input("\nWould you like to see individual trip data? Type 'yes' or 'no'.\n")
    while True:
        if view_data.lower() == 'yes':
            if row_count <= total_rows:
                print(df[row_count: row_count+5])
                row_count += 5
            else:
                print("\nReached end of file.")
        elif view_data.lower() == 'no':
            return
        else:
            print("\nInvalid input. Input taken as 'no'")
            return
        view_data = input("\nWould you like to see a few more rows of individual trip data? Type 'yes' or 'no'.\n")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        input('\nPress Enter key to display time statistics for filters:- City: {}| Month(s): {}| Day(s): {}'.format(city.title(), month.title(), day.title()))
        time_stats(df)
        input('\nPress Enter key to display station statistics for filters:- City: {}| Month(s): {}| Day(s): {}'.format(city.title(), month.title(), day.title()))
        station_stats(df)
        input('\nPress Enter key to display time duration statistics for filters:- City: {}| Month(s): {}| Day(s): {}'.format(city.title(), month.title(), day.title()))
        trip_duration_stats(df)
        input('\nPress Enter key to display user statistics for filters:- City: {}| Month(s): {}| Day(s): {}'.format(city.title(), month.title(), day.title()))
        user_stats(df,city)

        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
