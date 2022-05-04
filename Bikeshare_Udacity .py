import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

def check_input(input_str,input_type):
    """
    check the validity of user input.
    input_str: is the input of the user
    input_type: is the type of input: 1 = city, 2 = month, 3 = day
    """
    while True:
        input_read = input(input_str)
        try:
            if input_read in ['chicago','new york city','washington'] and input_type == 1:
                break
            elif input_read in ['january', 'february', 'march', 'april', 'may', 'june','all'] and input_type == 2:
                break
            elif input_read in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all'] and input_type == 3:
                break
            else:
                if input_type == 1:
                    print("Sorry, your input should be: chicago, new york city or washington without space ")
                if input_type == 2:
                    print("Sorry, your input should be: january, february, march, april, may, june or all")
                if input_type == 3:
                    print("Sorry, your input should be: a day name of week or all")
        except ValueError:
            print("Sorry, your input is wrong")
    return input_read

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    city = check_input('type a city name to analyze (chicago, new york city or washington):',1).lower()
    month = check_input('choose a desired month (january- june or all):',2).lower()
    day = check_input('choose day of week (sunday - saturday or all):',3).lower()

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

    # extract month, day of week, hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

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

    # display the most common month
    # display the most common day of week
    # display the most common start hour

    popular_month = df['month'].mode()[0]
    print('the most common month:',popular_month)
    popular_day = df['day_of_week'].mode()[0]
    print('the most common day of week',popular_day)
    popular_hour = df['hour'].mode()[0]
    print('display the most common start hour',popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('commonly used start station:',common_start_station)
    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('most commonly used end station:', common_end_station)
    # display most frequent combination of start station and end station trip
    group_field = df.groupby(['Start Station', 'End Station'])
    popular_combination_station = group_field.size().sort_values(ascending=False).head(1)
    print('most frequent combination of start station and end station trip:',popular_combination_station)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('total travel time', total_travel_time)
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('average travel time', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('count of user types:',df['User Type'].value_counts())
    # Display counts of gender
    if city != 'washington':
       print('count of gender:',df['Gender'].value_counts())
       # Display earliest, most recent, and most common year of birth
       print('year of birth status:')
       earliest_birth = df['Birth Year'].min()
       print('earliest year of Birth:', earliest_birth)
       most_recent_birth = df['Birth Year'].max()
       print ('most recent year of birth is:',most_recent_birth)
       most_common_birth= df['Birth Year'].mode()[0]
       print('most common year of birth', most_common_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
        start_loc = 0
        keep_asking = True
        while (keep_asking):
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            view_display = input("Do you wish to continue?: ").lower()
            if view_display == "no":
                keep_asking = False

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
 main()