import time
import pandas as pd


# The list of teh data files 
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# cheching input value process 
def check (data, value=[]):
    """ Check the value of the input, is it one of the values in the list or not?"""
    if data not in value:
        print('choose from the list, please!')

def check_loop(list=[],message=''):

    """loop as long as the input is not a valid value [contained in the list], once it valid, stop it """

    user_input=''
    while user_input not in list:  
        user_input= input('\n {} \n'.format(message)).lower().strip()
        check(user_input,list)
    return user_input

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print ('Please note that in this project we are only working with three data sets')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        cities=['chicago', 'new york city', 'washington']
        city=check_loop(cities,'Which city (chicago, new york city, washington) do you want to explore?')

    # get user input for month (all, january, february, ... , june)
        
        months = ['january','february','march','april','may','june','all']
        month= check_loop(months,'Which month (january, february, ... , june) do you want to filter by? in case there is no specific month write \'all\'')


    # get user input for day of week (all, monday, tuesday, ... sunday)
        
        days=['monday', 'tuesday','wednesday','thursday','friday','saturday','sunday','all']
        day= check_loop(days, 'Which day of the week do you want to filter by?  in case there is no specific day write \'all\' ')

        print('You chose {}, {}, {}'.format(city, month, day))
        
        recheck=check_loop(['yes','no'], 'Is that correct? Enter yes or no.')

        if recheck.lower() == 'yes':
            break
        
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

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = [1,2,3,4,5,6]
        dic_month={months[i]: month_num[i] for i in range(len(months))}

    
        # filter by month to create the new dataframe
        df = df[df['month'] == dic_month[month]]

    # filter by day of week if applicable
    if day != 'all':
        days=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        day_num=[0,1,2,3,4,5,6]
        dic_day={days[i]: day_num[i] for i in range(len(days))}
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==dic_day[day]]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_mon_num = df['month'].mode()[0] ##.value_counts().index.tolist()[0]
    common_mon_name = months[common_mon_num-1]
    print('The most common month is {} \n\n'.format(common_mon_name.title()))

    # display the most common day of week
    days=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    common_day_num = df['day_of_week'].value_counts().index.tolist()[0] ##.mode()[0]
    common_day_name = days[common_day_num]
    print('The most common day is {}\n\n'.format(common_day_name.title()))

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('The most common hour is {}\n\n'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts().index.tolist()[0]
    print('The most common Start Station is {} \n\n'.format(start_station))

    # display most commonly used end station
    end_station = df['End Station'].value_counts().index.tolist()[0]
    print('The most common End Station is {} \n\n'.format(end_station))


    # display most frequent combination of start station and end station trip
    df['start_end_station']='Start: '+ df['Start Station'] + ', End: ' + df['End Station']
    start_end = df['start_end_station'].value_counts().idxmax()
    print('The most frequent combination of start station and end station trip is {} \n\n'.format(start_end))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    t1=pd.to_datetime(df['Start Time']).dt.time.astype(str)
    t2=pd.to_datetime(df['End Time']).dt.time.astype(str)
    df['trip_duration'] = pd.to_timedelta(t2)-pd.to_timedelta(t1)  #timedelta doesn't work with data type time
    total_trip_duration = df['trip_duration'].sum()
    print('Total Travel duration is: {}'.format(total_trip_duration))


    # display mean travel time
    mean_trip_duration = df['trip_duration'].mean()
    print('Mean Travel duration is: {}'.format(mean_trip_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    try: 
        print('\nCalculating User Stats...\n')
        start_time = time.time()

        # Display counts of user types
        user_type_count = df['User Type'].value_counts().to_dict().items()
        for k, v in user_type_count:
            print('{} user type count is {}'.format(k,v)) 

        # Display counts of gender
        gender_count = df['Gender'].value_counts().to_dict().items()
        for k, v in gender_count :
            print('{}  count is {}'.format(k,v)) 

        # Display earliest, most recent, and most common year of birth
        early_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        print('The earliest year of birth is {}'.format(early_birth_year))
        print('The most recent year of birth is {}'.format(recent_birth_year))
        print('The most common year of birth is {}'.format(common_birth_year))
    except:
        #Washington city doesn't have gender and birth year columns
        print('\n Sorry, extra user data is not available for this city')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    """run all the above functions"""
    """
    after loading the data it will run the first two functions that have 
    some data.  
    after runing those two function the app check whether the user wants more data or not.
    it checks the input of the user (valid value entries)
    then it runs the rest functions based on the user desire 
    
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        answer = ['yes','no']
        trip_data_check = check_loop(answer,'Do you want to see trip duration data? yes or no')

        if trip_data_check == 'yes':
            trip_duration_stats(df)
            user_data_check = check_loop(answer,'Do you want to see user data? yes or no')

            if user_data_check == 'yes':
                user_stats(df)
            elif user_data_check == 'no':
                conti_nue = check_loop(answer, 'Do you want to continue? yes or no')
                if conti_nue != 'yes':
                    print('\n Thank you for using our program!')
                    break

        elif trip_data_check == 'no':
            user_data_check = check_loop(answer,'Do you want to see user data? yes or no')

            if user_data_check == 'yes':
                user_stats(df)
            elif user_data_check == 'no':
                conti_nue = check_loop(answer, 'Do you want to continue? yes or no')
                if conti_nue != 'yes':
                    print('\n Thank you for using our program!')
                    break
   
        restart = check_loop(answer, 'Do you want to restart the program? yes or no')
        if restart != 'yes':
            print('\n Thank you for using our program!')
            break


if __name__ == "__main__":
	main()
