import time
import pandas as pd
import numpy as np

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
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = str.lower(input('Please select the city to analyze. Choices are "Chicago, New York City or Washington" \n'))
        if city in ('chicago','new york city','washington'):
            break
        else: print('Please enter one of the three cities exactly as stated above \n\n')

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = str.lower(input('\nPlease select the month to analyze. Choices are "All, January, February, March, April, May, June" \n'))
        if month in ('all, january, february, march, april, may, june'):
            break
        else: print('Please enter one of the choices exactly as stated above \n\n')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str.lower(input('\nPlease select the day of the week to analyze. Choices are "All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday" \n'))
        if day in ('all, monday, tuesday, wednesday, thursday, friday, saturday or sunday'):
            break
        else: print('Please enter one of the choices exactly as stated above \n')
        #lower case the day with .lower and an in to check if correct input is chosen

    print('These are the values you picked:\n City = {} \n Month = {} \n Day = {} \n'.format(city,month,day))
        #Consider putting in a confirmation statement that summarizes the input and asks the user to confirm

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

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

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

    # TO DO: display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    common_month = months[df['month'].mode()[0]-1]
    print('The most common month is {}\n'.format(common_month))

    # TO DO: display the most common day of week
    print('The most common day of the week is {}\n'.format(df['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour

    df['hour'] = df['Start Time'].dt.hour

    print('The most common start hour is {}\n'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most commonly used start station is {}\n'.format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print('The most commonly used end station is {}\n'.format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip

    df['trip'] = 'from ' + df['Start Station'] + ' to ' + df['End Station']
    print('The most common trip is {}\n'.format(df['trip'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('The total travel time is {} minutes\n'.format(df['Trip Duration'].sum()//60))

    # TO DO: display mean travel time
    print('The average travel time is {} minutes\n'.format(df['Trip Duration'].mean()//60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()

    print(user_types)

    # TO DO: Display counts of gender
    try:
        print(df['Gender'].value_counts())
    except:
        print('Apologies but gender information is not available for Washington')

    try:
        year=df['Birth Year'].dropna(axis = 0)

        print('Earliest year of birth: ', year.min())

        print('Most recent year of birth: ', year.max())

        print('Most common year of birth: ',year.mode())
    except:
        print('Apologies but year of birth information is not available for Washington')

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

        raw_data = load_data(city, month, day)
        raw_counter = 0
        while True:
            raw = input('\nWould you like to see some raw data? Enter yes or no.\n')
            if raw.lower() == 'yes':
                print(raw_data.iloc[raw_counter:raw_counter+5])
                raw_counter += 5
            else:
                break

        restart = input('\nEnter "yes" if you would like to restart. Any other input will end the program.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
