import tkinter as tk
import tkinter.ttk as ttk
import requests
try:
    from secrets import owm_key  # get your own key (free) at https://openweathermap.org/appid
except Exception:
    owm_key = False
from copy import deepcopy
# https://openweathermap.org/weather-conditions
# https://openweathermap.org/current#current_JSON


class WeatherWidget(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.API_URL = 'https://api.openweathermap.org/data/2.5/weather'
        self.params = {'APPID': owm_key}  # when button is pressed, user options are collected and appended here
        self.response = None
        self.units = tk.IntVar()
        self.units_mapping = {0: 'standard', 1: 'metric', 2: 'imperial'}
        self.languages = {
            'Arabic': 'AR', 'Bulgarian': 'BG', 'Catalan': 'CA', 'Czech': 'CZ', 'German': 'DE', 'Greek': 'EL',
            'English': 'EN', 'Persian (Farsi)': 'FA', 'Finnish': 'FI', 'French': 'FR', 'Galician': 'GL',
            'Croatian': 'HR', 'Hungarian': 'HU', 'Italian': 'IT', 'Japanese': 'JA', 'Korean': 'KR', 'Latvian': 'LA',
            'Lithuanian': 'LT', 'Macedonian': 'MK', 'Dutch': 'NL', 'Polish': 'PL', 'Portuguese': 'PT', 'Romanian': 'RO',
            'Russian': 'RU', 'Swedish': 'SE', 'Slovak': 'SK', 'Slovenian': 'SL', 'Spanish': 'ES', 'Turkish': 'TR',
            'Ukrainian': 'UA', 'Vietnamese': 'VI', 'Chinese Simplified': 'ZH_CN', 'Chinese Traditional': 'ZH_TW'}
        self.last_request_mapping = {'1': 'yellow', '2': 'green2', '3': 'yellow', '4': 'red', '5': 'purple'}
        self.gui()
        self.dynamic_mixins = {
            self.temp_display: [' K', ' °C', ' °F'],
            self.min_temp_display: [' K', ' °C', ' °F'],
            self.max_temp_display: [' K', ' °C', ' °F'],
            self.wind_speed_display: [' m/s', ' m/s', ' mph']
        }
        self.display_fields = {  # maps display widgets to data path in JSON response for use in self.fill_fields()
            self.city_name_display: [['name']],
            self.country_name_display: [['sys', 'country']],
            self.lat_display: [['coord', 'lat'], '°'],  # ° is a "static mixin" - appended regardless of metric / imperl
            self.lon_display: [['coord', 'lon'], '°'],

            self.weather_name_display: [['weather', 0, 'main']],
            self.weather_detail_display: [['weather', 0, 'description']],

            self.temp_display: [['main', 'temp']],
            self.min_temp_display: [['main', 'temp_min']],
            self.max_temp_display: [['main', 'temp_max']],

            self.wind_speed_display: [['wind', 'speed']],
            self.wind_direction_display: [['wind', 'deg'], '°'],
            self.cloudiness_display: [['clouds', 'all'], '%'],
            self.humidity_display: [['main', 'humidity'], '%'],

            self.pressure_display: [['main', 'pressure'], ' hPa'],
            self.sea_pressure_display: [['main', 'sea_level'], ' hPA'],  # these two data points are described in API
            self.ground_pressure_display: [['main', 'grnd_level'], ' hPa'],  # docs but are not present in any city

            self.rain1_display: [['rain', '1h'], ' mm'],
            self.rain3_display: [['rain', '3h'], ' mm'],  # these are very rare also but can be found; try Bombay
            self.snow1_display: [['snow', '1h'], ' mm'],  #
            self.snow3_display: [['snow', '3h'], ' mm'],  #

            self.sunrise_display: [['sys', 'sunrise']],
            self.sunset_display: [['sys', 'sunset']],
            self.data_timestamp_display: [['dt']]
        }

    def gui(self):
        choice_frame = tk.Frame(self)
        choice_frame.pack(side='top', fill='x')

        choose_city_txt = tk.Label(choice_frame, text='Choose a city: ')
        choose_city_txt.pack(side='left')

        self.choose_city_input = tk.Entry(choice_frame, bg='pink3')
        self.choose_city_input.pack(side='left')

        choose_language_txt = tk.Label(choice_frame, text='Choose a language: ')
        choose_language_txt.pack(side='left')

        self.choose_language_input = ttk.Combobox(choice_frame, values=list(self.languages))
        self.choose_language_input.pack(side='left')

        separator_choice_0 = tk.Frame(self, height=1, width=500, bg="black")
        separator_choice_0.pack(side='top', pady=5)

        row0_frame = tk.Frame(self)
        row0_frame.pack(side='top', fill='x')

        standard = tk.Radiobutton(row0_frame, text='Standard', variable=self.units, value=0, bg='chocolate1', activebackground='chocolate1')
        standard.pack(side='left')

        metric = tk.Radiobutton(row0_frame, text='Metric', variable=self.units, value=1, bg='chocolate1', activebackground='chocolate1')
        metric.pack(side='left')

        imperial = tk.Radiobutton(row0_frame, text='Imperial', variable=self.units, value=2, bg='chocolate1', activebackground='chocolate1')
        imperial.pack(side='left')

        choose_city_button = tk.Button(row0_frame, text='Get weather data', command=self.do_request, bg='green2')
        choose_city_button.pack(side='left')

        last_request_txt = tk.Label(row0_frame, text='Previous request code: ')
        last_request_txt.pack(side='left')

        self.last_request_display = tk.Label(row0_frame, relief=tk.RIDGE, text='   N/A   ', bg='yellow')
        self.last_request_display.pack(side='left')

        separator_0_1 = tk.Frame(self, height=1, width=500, bg="black")
        separator_0_1.pack(side='top', pady=5)

        row1_frame = tk.Frame(self)
        row1_frame.pack(side='top', fill='x')

        city_name_txt = tk.Label(row1_frame, text='City: ')
        city_name_txt.pack(side='left')

        self.city_name_display = tk.Button(row1_frame, relief=tk.SUNKEN, width=20, bg='pink3', state='disabled')
        self.city_name_display.pack(side='left')

        country_name_txt = tk.Label(row1_frame, text='Country: ')
        country_name_txt.pack(side='left')

        self.country_name_display = tk.Button(row1_frame, relief=tk.SUNKEN, width=3, bg='white', state='disabled')
        self.country_name_display.pack(side='left')

        lat_txt = tk.Label(row1_frame, text='Latitude: ')
        lat_txt.pack(side='left')

        self.lat_display = tk.Button(row1_frame, relief=tk.SUNKEN, width=5, bg='white', state='disabled')
        self.lat_display.pack(side='left')

        lon_txt = tk.Label(row1_frame, text='Longitude: ')
        lon_txt.pack(side='left')

        self.lon_display = tk.Button(row1_frame, relief=tk.SUNKEN, width=5, bg='white', state='disabled')
        self.lon_display.pack(side='left')

        separator_1_2 = tk.Frame(self, height=1, width=500, bg="black")
        separator_1_2.pack(side='top', pady=5)

        row2_frame = tk.Frame(self)
        row2_frame.pack(side='top', fill='x')

        weather_name_txt = tk.Label(row2_frame, text='Weather type: ')
        weather_name_txt.pack(side='left')

        self.weather_name_display = tk.Button(row2_frame, relief=tk.SUNKEN, width=20, bg='white', state='disabled')
        self.weather_name_display.pack(side='left')

        weather_detail_txt = tk.Label(row2_frame, text='Weather detail: ')
        weather_detail_txt.pack(side='left')

        self.weather_detail_display = tk.Button(row2_frame, relief=tk.SUNKEN, width=20, bg='gold', state='disabled')
        self.weather_detail_display.pack(side='left')

        separator_2_3 = tk.Frame(self, height=1, width=500, bg="black")
        separator_2_3.pack(side='top', pady=5)

        row3_frame = tk.Frame(self)
        row3_frame.pack(side='top', fill='x')

        temperature_txt = tk.Label(row3_frame, text='Temperature: ')
        temperature_txt.pack(side='left')

        self.temp_display = tk.Button(row3_frame, relief=tk.SUNKEN, width=7, bg='chocolate1', state='disabled')
        self.temp_display.pack(side='left')

        min_temperature_txt = tk.Label(row3_frame, text='Min. temperature: ')
        min_temperature_txt.pack(side='left')

        self.min_temp_display = tk.Button(row3_frame, relief=tk.SUNKEN, width=7, bg='chocolate1', state='disabled')
        self.min_temp_display.pack(side='left')

        max_temperature_txt = tk.Label(row3_frame, text='Max. temperature: ')
        max_temperature_txt.pack(side='left')

        self.max_temp_display = tk.Button(row3_frame, relief=tk.SUNKEN, width=7, bg='chocolate1', state='disabled')
        self.max_temp_display.pack(side='left')

        separator_3_4 = tk.Frame(self, height=1, width=500, bg="black")
        separator_3_4.pack(side='top', pady=5)

        row4_frame = tk.Frame(self)
        row4_frame.pack(side='top', fill='x')

        wind_speed_txt = tk.Label(row4_frame, text='Wind speed: ')
        wind_speed_txt.pack(side='left')

        self.wind_speed_display = tk.Button(row4_frame, relief=tk.SUNKEN, width=7, bg='chocolate1', state='disabled')
        self.wind_speed_display.pack(side='left')

        wind_direction_txt = tk.Label(row4_frame, text='Wind direction: ')
        wind_direction_txt.pack(side='left')

        self.wind_direction_display = tk.Button(row4_frame, relief=tk.SUNKEN, width=5, bg='white', state='disabled')
        self.wind_direction_display.pack(side='left')

        cloudiness_txt = tk.Label(row4_frame, text='Cloudiness: ')
        cloudiness_txt.pack(side='left')

        self.cloudiness_display = tk.Button(row4_frame, relief=tk.SUNKEN, width=4, bg='white', state='disabled')
        self.cloudiness_display.pack(side='left')

        humidity_txt = tk.Label(row4_frame, text='Humidity: ')
        humidity_txt.pack(side='left')

        self.humidity_display = tk.Button(row4_frame, relief=tk.SUNKEN, width=4, bg='white', state='disabled')
        self.humidity_display.pack(side='left')

        separator_4_5 = tk.Frame(self, height=1, width=500, bg="black")
        separator_4_5.pack(side='top', pady=5)

        row5_frame = tk.Frame(self)
        row5_frame.pack(side='top', fill='x')

        pressure_txt = tk.Label(row5_frame, text='Pressure: ')
        pressure_txt.pack(side='left')

        self.pressure_display = tk.Button(row5_frame, relief=tk.SUNKEN, width=7, bg='white', state='disabled')
        self.pressure_display.pack(side='left')

        sea_pressure_txt = tk.Label(row5_frame, text='Sea level pressure: ')
        sea_pressure_txt.pack(side='left')

        self.sea_pressure_display = tk.Button(row5_frame, relief=tk.SUNKEN, width=7, bg='white', state='disabled')
        self.sea_pressure_display.pack(side='left')

        ground_pressure_txt = tk.Label(row5_frame, text='Ground level pressure: ')
        ground_pressure_txt.pack(side='left')

        self.ground_pressure_display = tk.Button(row5_frame, relief=tk.SUNKEN, width=7, bg='white', state='disabled')
        self.ground_pressure_display.pack(side='left')

        separator_5_6 = tk.Frame(self, height=1, width=500, bg="black")
        separator_5_6.pack(side='top', pady=5)

        row6_frame = tk.Frame(self)
        row6_frame.pack(side='top', fill='x')

        rain1_txt = tk.Label(row6_frame, text='Rain 1 hr: ')
        rain1_txt.pack(side='left')

        self.rain1_display = tk.Button(row6_frame, relief=tk.SUNKEN, width=8, bg='white', state='disabled')
        self.rain1_display.pack(side='left')

        rain3_txt = tk.Label(row6_frame, text='/ 3 hrs: ')
        rain3_txt.pack(side='left')

        self.rain3_display = tk.Button(row6_frame, relief=tk.SUNKEN, width=8, bg='white', state='disabled')
        self.rain3_display.pack(side='left')

        snow1_txt = tk.Label(row6_frame, text='Snow 1 hr: ')
        snow1_txt.pack(side='left')

        self.snow1_display = tk.Button(row6_frame, relief=tk.SUNKEN, width=8, bg='white', state='disabled')
        self.snow1_display.pack(side='left')

        snow3_txt = tk.Label(row6_frame, text='/ 3 hrs: ')
        snow3_txt.pack(side='left')

        self.snow3_display = tk.Button(row6_frame, relief=tk.SUNKEN, width=8, bg='white', state='disabled')
        self.snow3_display.pack(side='left')

        separator_6_7 = tk.Frame(self, height=1, width=500, bg="black")
        separator_6_7.pack(side='top', pady=5)

        row7_frame = tk.Frame(self)
        row7_frame.pack(side='top', fill='x')

        sunrise_txt = tk.Label(row7_frame, text='Sunrise: ')
        sunrise_txt.pack(side='left')

        self.sunrise_display = tk.Button(row7_frame, relief=tk.SUNKEN, width=10, bg='white', state='disabled')
        self.sunrise_display.pack(side='left')

        sunset_txt = tk.Label(row7_frame, text='Sunset: ')
        sunset_txt.pack(side='left')

        self.sunset_display = tk.Button(row7_frame, relief=tk.SUNKEN, width=10, bg='white', state='disabled')
        self.sunset_display.pack(side='left')

        data_timestamp_txt = tk.Label(row7_frame, text='Data timestamp: ')
        data_timestamp_txt.pack(side='left')

        self.data_timestamp_display = tk.Button(row7_frame, relief=tk.SUNKEN, width=10, bg='white', state='disabled')
        self.data_timestamp_display.pack(side='left')

        separator_7_8 = tk.Frame(self, height=1, width=500, bg="black")
        separator_7_8.pack(side='top', pady=5)

        row8_frame = tk.Frame(self)
        row8_frame.pack(side='top', fill='x')

        status_txt = tk.Label(row8_frame, text='Status: ')
        status_txt.pack(side='left')

        self.status_display = tk.Label(row8_frame, relief=tk.RIDGE, width=63, bg='green2', text='Write a city name in English in the top-left box and press "Get weather data".')
        self.status_display.pack(side='left')

    def do_request(self):
        self.params['q'] = self.choose_city_input.get()

        if self.units.get() in (1, 2):
            self.params['units'] = self.units_mapping[self.units.get()]
        else:
            try:
                del self.params['units']
            except KeyError:
                pass

        if self.choose_language_input.get() in self.languages:
            self.params['lang'] = self.languages[self.choose_language_input.get()]
        else:
            self.params['lang'] = 'EN'
            self.choose_language_input.set('English')

        self.response = requests.get(self.API_URL, params=self.params).json()
        self.fill_fields()

    def fill_fields(self):
        """This is spaghetti, isn't it?"""
        self.last_request_display['text'] = '   ' + str(self.response['cod']) + '   '
        self.last_request_display['bg'] = self.last_request_mapping[str(self.response['cod'])[0]]
        self.status_display['text'] = dict(self.response).get('message', 'No message.')
        self.status_display['bg'] = self.last_request_mapping[str(self.response['cod'])[0]]

        for display in self.display_fields:
            product = deepcopy(self.response)
            for layer in self.display_fields[display][0]:
                try:
                    product = product[layer]
                except KeyError:
                    display.config(text='N/A', bg='yellow')
                    break
                else:
                    if display['text'] != 'N/A' and len(self.display_fields[display]) == 2:
                        display.config(text=(str(product) + self.display_fields[display][1]))
                    elif display is self.city_name_display:
                        display.config(text=product, bg='pink3')
                    else:
                        display.config(text=product, bg=('gold' if display is self.weather_detail_display else 'white'))
        for item in self.dynamic_mixins:
            if item['text'] != 'N/A':
                item['text'] = str(item['text']) + self.dynamic_mixins[item][self.units.get()]
                item['bg'] = 'chocolate1'


def main():
    root = tk.Tk()
    root.geometry('500x355')
    root.title('Weather Widget')
    root.resizable(False, False)
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TCombobox', fieldbackground='gold')
    WeatherWidget(root).pack(side="top")
    root.mainloop()


if __name__ == '__main__':
    main()
