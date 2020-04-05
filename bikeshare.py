
import time
import pandas as pd
import numpy as np
import datetime
import statistics
from collections import Counter



CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Choose your city (all in small case alphabets)-- chicago, new york city, washington: \n')
        if city in CITY_DATA.keys():
            break
        else:
            print('There is no information about this city.')

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('Choose the month (all in small case alphabets)-- january, february, march, april, may or june OR type all if you want to see the statistics for all of these months: \n')
        if month == 'all':
            break
        elif month in months:
            break
        else:
            print('That\'s is not a valid month')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Enter the day of week (all in small case alphabets)-- sunday, monday, tuesday or any other day or type all to include all days: \n')
        if day == 'all':
            break
        elif day in days:
            break
        else:
            print('That\'s not a valid day')

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    data_info = input('\nWould you like to see the first 5 rows of raw data? Enter yes or no.\n')
    if data_info.lower() != 'no':
        i = 5
        data = df.iloc[0:i]
        print(f'\nThe first {i} rows of data are:\n\n', data)
        while True:
            info= input('\nWould you like to see next rows of data? Enter yes or no.\n')
            if info.lower() != 'no':
                j = i + 5
                further_data = df.iloc[i:j]
                print(f'\nThe next {i} to {j} rows of data are:\n\n', further_data)
                i +=5
            else:
                print('\nProceeding to next steps for further calculating statistics.......')
                break
    else:
        print('\nSkipping printing of rows of raw data. Going further calculating statistics.......')

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        #months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) +1

        # filter by month to create the new dataframe
        df = df[df.month == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df.day_of_week == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    common_month_name = months[common_month -1].title()
    print('Most common month: ', common_month_name)

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day: ', common_day)

    # TO DO: display the most common start hour
    start_hour = df['Start Time'].dt.hour
    common_start_hour = start_hour.mode()[0]
    print('Most popular hour: ', common_start_hour)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f'Most common start station: {common_start_station}')

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f'Most common end station: {common_end_station}')

    # TO DO: display most frequent combination of start station and end station trip
    df['combination'] = list(zip(df['Start Station'], df['End Station']))
    total_combination = Counter(df['combination'])
    frequent_combination = total_combination.most_common(1)

    for i in range(len(frequent_combination)):
        print('Popular trip: ', frequent_combination[i][0])
        print('Count for most popular trip: ', frequent_combination[i][1])

    print('\nThis took %s seconds.' % (time.time() - start_time))

    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print('The total trip duration for the trip is: ', total_trip_duration)

    # TO DO: display mean travel time
    average_trip_duration = df['Trip Duration'].mean()
    print('The average trip duration for the trip is: ', average_trip_duration)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats....')
    start_time = time.time()

    # TO DO: Display counts of user types
    counts_usertypes = df['User Type'].value_counts()
    print('\nThe breakdown for user types are:\n', counts_usertypes)

    # TO DO: Display counts of gender
    if 'Gender' not in df.columns:
        print('\nThe data for gender is not available for the given city!')
    else:
        counts_gender = df['Gender'].value_counts()
        print('\nThe breakdown gender are:\n', counts_gender)

    # TO DO: Display earliest, most recent, and most common year of birth

    if 'Birth Year' not in df.columns:
        print("\nThe year of birth data is not available for the given city!")
    else:
        print('\nStatistics for year of birth .......\n')
        earliest_birthyear = df['Birth Year'].min()
        print('The oldest year of birth is : ', earliest_birthyear)

        recent_birthyear = df['Birth Year'].max()
        print('\nThe youngest year of birth is : ', recent_birthyear)

        mostcommon_birthyear = df['Birth Year'].mode()[0]
        print('\nThe popular year of birth is : ', mostcommon_birthyear)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
