import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city='empty'
    #month='empty'
    #month='empty'
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city != 'chicago' and city != 'new york city' and city != 'washington':
        city = input("Please enter one of these cities (chicago, new york city, washington]): ").lower()

    # get user input for month (all, january, february, ... , june)

    while True:
        month = input("Please enter number of month between 1 and 6 (0 for all month): ")
        if month =='0' or month == '1' or month == '2' or month == '3' or month == '4' or month == '5' or month == '6':
            months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
            month = months[int(month)]
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please enter day of week between 1 to 7 (0 for all days): ")
        if day =='0' or day == '1' or day == '2' or day == '3' or day == '4' or day == '5' or day == '6' or day == '7':
            days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            day = days[int(day)]
            break

    print("You selected {} / {} / {}".format(city, month, day))

    print('-'*40)
    city = CITY_DATA.get(city) 
    return city, month, day


def load_data(city, month, day):
    """loads the data for the given city, month and day

    Args:
        city ([string]): city
        month ([int]): I think so
        day ([int]): I think so

    Returns:
        pandas dataframe: filtered for day month, city
    """
    # load data file into a dataframe
    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    df['day_of_week_int'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month =  (df.groupby(['month'])['month'].count().idxmax())
    #months = ['january', 'february', 'march', 'april', 'may', 'june']
    #month = months.index(month)+1
    print('Most popular month: {}'.format(common_month))

    # display the most common day of week
    common_day =  (df.groupby(['day_of_week'])['day_of_week'].count().idxmax())
    print('Most popular day of week: {}'.format(common_day))

    # display the most common start hour
    popular_hour =  (df.groupby(['hour'])['hour'].count().idxmax())
    print('Most popular hour: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start =  (df.groupby(['Start Station'])['Start Station'].count().idxmax())
    print('Most popular start station: {}'.format(common_start))

    # display most commonly used end station
    common_end =  (df.groupby(['End Station'])['End Station'].count().idxmax())
    print('Most popular end station: {}'.format(common_end))

    # display most frequent combination of start station and end station trip
    df['common_trip'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip =  (df.groupby(['common_trip'])['common_trip'].count().idxmax())
    print('Most popular trip: {}'.format(common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Total travel'] = df['End Time'] - df['Start Time']
    # display total travel time
    print('Total travel time: {}'.format(df['Total travel'].sum()))

    # display mean travel time
    print('Average travel time: {}'.format(df['Total travel'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User types:')
    print(user_types)
    print()

    if 'Gender' in df:
        # Display counts of gender
        user_types = df['Gender'].value_counts()
        print('Gender: ')
        print(user_types)

    if 'Birth Year' in df:
        # Display earliest, most recent, and most common year of birth
        min_year= df['Birth Year'].min()
        max_year= df['Birth Year'].max()
        common_year= df['Birth Year'].mode()[0]
        avg_year= df['Birth Year'].mean()
        print('Youngest: {}, Oldest: {}, Common year: {}, average year: {}'.format(int(min_year), int(max_year), int(common_year), int(avg_year)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        zeile=0

        raw_data = input('\nWould you like to see some raw data? Enter yes or no.\n')
        if raw_data.lower() != 'no':
            while True:
                print(df.iloc[zeile:zeile+5])
                more_data = input('\nMore data? Enter yes or no.\n')
                zeile =+ 5
                if more_data != 'yes':
                    break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
