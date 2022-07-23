from wg_functions import *
import pandas as pd
import os.path


PATH = "C:\Program Files (x86)\geckodriver.exe"
area = ['san-clemente', 'san-diego', 'los-angeles'] # Area as it appears on the wunderground website
station = ['KCASANCL94', 'KCASANDI4511', 'KCALOSAN698'] # Name of the personal weather station (PWS)

df_header = ['previous', 'previous_high', 'previous_low', 
            'day1', 'day1_high', 'day1_low', 'day2', 'day2_high', 'day2_low',
            'day3', 'day3_high', 'day3_low','day4', 'day4_high', 'day4_low',
            'day5', 'day5_high', 'day5_low', 'day6', 'day6_high', 'day6_low',
            'day7', 'day7_high', 'day7_low']

def main():
    prev_temp = past_weather(area, station)
    forecast_dict = forecast(area, station, PATH)

    for a in area:    
        my_dict = forecast_dict[a] # forecasted temperature
        mylist = [str(get_date(-1)), prev_temp[a][0], prev_temp[a][1]] # yesterdays temperature
        for i in range(1,8):
            mylist.append(str(get_date(i)))
            mylist.append(my_dict[0][i])
            mylist.append(my_dict[1][i])
        df = pd.DataFrame(columns=df_header)
        for idx, col in enumerate(df_header):
            df.loc[0, col] = mylist[idx]

        rplace = a.replace('-', '_')
        file_name = f'{rplace}_forecast.csv'    
        file_exists = os.path.exists(file_name)
        if file_exists is True:
            df.to_csv(file_name, mode='a', index=False, header=False)
        elif file_exists is False:   # <--------- Prefered format when creating first file
            df.loc[0, 'previous_high'] = 0              
            df.loc[0, 'previous_low'] = 0
            df.to_csv(file_name, index=False)
if __name__ == "__main__":
    main()

