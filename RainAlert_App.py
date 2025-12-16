import tkinter as tk
import requests
from tkinter import messagebox

# ---------------- API CONFIG ---------------- #
OPEN_WEATHER_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"

# ---------------- WEATHER FUNCTION ---------------- #
def check_rain():
    city = city_entry.get()
    api_key = api_entry.get()

    if city == "" or api_key == "":
        messagebox.showerror(
            "Input Error",
            "Please enter both City Name and API Key"
        )
        return

    weather_params = {
        "q": city,
        "appid": api_key,
        "cnt": 4  # next 12 hours
    }

    try:
        response = requests.get(OPEN_WEATHER_ENDPOINT, params=weather_params)
        response.raise_for_status()
        weather_data = response.json()

        will_rain = False

        for hour_data in weather_data["list"]:
            condition_code = hour_data["weather"][0]["id"]
            if condition_code < 700:
                will_rain = True
                break

        if will_rain:
            result_label.config(
                text="🌧️ Rain expected in the next 12 hours.\nBring an Umbrella ☔",
                fg="blue"
            )
        else:
            result_label.config(
                text="☀️ No rain expected in the next 12 hours.",
                fg="green"
            )

    except requests.exceptions.HTTPError:
        messagebox.showerror(
            "Error",
            "Invalid City or API Key.\nPlease check and try again."
        )
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------------- TKINTER UI ---------------- #
window = tk.Tk()
window.title("Rain Alert App")
window.geometry("420x320")
window.resizable(False, False)

# Title
title_label = tk.Label(
    window,
    text="🌦️ Rain Alert App",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=10)

# City input
city_label = tk.Label(window, text="Enter City Name:")
city_label.pack()

city_entry = tk.Entry(window, width=35)
city_entry.pack(pady=5)

# API Key input
api_label = tk.Label(window, text="Enter OpenWeather API Key:")
api_label.pack()

api_entry = tk.Entry(window, width=35, show="*")
api_entry.pack(pady=5)

# Button
check_button = tk.Button(
    window,
    text="Check Rain Forecast",
    command=check_rain,
    bg="#1e90ff",
    fg="white",
    width=22
)
check_button.pack(pady=15)

# Result label
result_label = tk.Label(window, text="", font=("Arial", 12))
result_label.pack(pady=10)

# Run app
window.mainloop()
