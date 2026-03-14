import streamlit as st
import requests
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title='Weather App', page_icon='🌤️', layout='wide')

API_KEY = '0549839b4c37d0a9e0205186136acdc7'

def get_style(condition, is_night):
    if condition in ['Rain', 'Drizzle', 'Thunderstorm']:
        bg = 'linear-gradient(to bottom, #2c3e50, #3d5166, #4a6080)'
        emoji = '🌧️'
    elif condition == 'Snow':
        bg = 'linear-gradient(to bottom, #b0c4de, #d6e8f5, #eef5fb)'
        emoji = '❄️'
    elif condition == 'Clear' and is_night:
        bg = 'linear-gradient(to bottom, #0a0a2e, #1a1a4e, #2d2d6e)'
        emoji = '🌙'
    elif condition == 'Clear':
        bg = 'linear-gradient(to bottom, #1a90d9, #63c3f5, #a8dcf0)'
        emoji = '☀️'
    elif condition == 'Clouds':
        bg = 'linear-gradient(to bottom, #4a6fa5, #6a8fc5, #8aafd5)'
        emoji = '⛅'
    elif condition in ['Mist', 'Fog', 'Haze', 'Smoke', 'Dust', 'Sand']:
        bg = 'linear-gradient(to bottom, #8a9bb0, #a8b8c8, #c8d8e8)'
        emoji = '🌫️'
    else:
        bg = 'linear-gradient(to bottom, #4a6fa5, #6a8fc5, #8aafd5)'
        emoji = '🌤️'
    return bg, emoji

# Unit switcher
unit = st.radio('🌡️ Temperature Unit', ['Metric (°C, m/s)', 'Imperial (°F, mph)'], horizontal=True)
units = 'metric' if 'Metric' in unit else 'imperial'
temp_symbol = '°C' if units == 'metric' else '°F'
speed_symbol = 'm/s' if units == 'metric' else 'mph'

city = st.text_input('🔍 Enter a city name', 'London')

if st.button('Get Weather 🌍'):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}'
    data = requests.get(url).json()

    if data['cod'] == 200:
        current_time = data['dt']
        sunrise = data['sys']['sunrise']
        sunset = data['sys']['sunset']
        is_night = current_time < sunrise or current_time > sunset
        condition = data['weather'][0]['main']
        bg, icon = get_style(condition, is_night)

        # Apply background and animations
        rain_drops = ''.join([f'<div style="position:fixed;top:-20px;left:{i*3}%;width:2px;height:20px;background:linear-gradient(transparent,#a8d8f0);animation:rain {0.8+(i*0.05)%0.7:.1f}s linear {(i*0.15)%2:.1f}s infinite;z-index:0;border-radius:2px"></div>' for i in range(35)])
        snow_flakes = ''.join([f'<div style="position:fixed;top:-20px;left:{i*3}%;font-size:{12+(i%8)}px;color:white;animation:snow {2+(i*0.1)%2:.1f}s linear {(i*0.3)%3:.1f}s infinite;z-index:0">❄</div>' for i in range(30)])
        clouds_anim = '<div style="position:fixed;top:60px;left:-100px;font-size:80px;animation:drift 25s linear infinite;z-index:0;opacity:0.6">☁️</div><div style="position:fixed;top:130px;left:-200px;font-size:60px;animation:drift 35s linear 5s infinite;z-index:0;opacity:0.5">☁️</div><div style="position:fixed;top:30px;left:-150px;font-size:100px;animation:drift 30s linear 10s infinite;z-index:0;opacity:0.4">☁️</div>'
        sun_anim = '<div style="position:fixed;top:40px;right:80px;width:100px;height:100px;background:radial-gradient(circle,#ffe066,#ffb300);border-radius:50%;box-shadow:0 0 80px #ffb300,0 0 160px #ffe066;animation:pulse 3s ease-in-out infinite;z-index:0"></div>'
        moon_anim = '<div style="position:fixed;top:60px;right:100px;font-size:80px;animation:float 6s ease-in-out infinite;z-index:0">🌙</div><div style="position:fixed;top:0;left:0;width:100%;height:100%;background-image:radial-gradient(white 1px,transparent 1px);background-size:50px 50px;opacity:0.2;z-index:0"></div>'
        mist_anim = '<div style="position:fixed;top:0;left:0;width:200%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.2),transparent);animation:mistmove 8s linear infinite;z-index:0"></div>'
        lightning = '<div style="position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(255,255,200,0.15);animation:flash 4s infinite;z-index:0"></div>'

        if condition in ['Rain', 'Drizzle']:
            anim = rain_drops
        elif condition == 'Thunderstorm':
            anim = rain_drops + lightning
        elif condition == 'Snow':
            anim = snow_flakes
        elif condition == 'Clouds':
            anim = clouds_anim
        elif condition == 'Clear' and not is_night:
            anim = sun_anim
        elif condition == 'Clear' and is_night:
            anim = moon_anim
        elif condition in ['Mist', 'Fog', 'Haze', 'Smoke', 'Dust', 'Sand']:
            anim = mist_anim
        else:
            anim = clouds_anim

        st.markdown(f"""
            <style>
            .stApp {{ background: {bg}; color: white; }}
            @keyframes rain {{ 0% {{ transform:translateY(-20px);opacity:0; }} 10% {{ opacity:1; }} 100% {{ transform:translateY(100vh);opacity:0.3; }} }}
            @keyframes snow {{ 0% {{ transform:translateY(-20px) rotate(0deg);opacity:0.8; }} 100% {{ transform:translateY(100vh) rotate(360deg);opacity:0; }} }}
            @keyframes drift {{ 0% {{ transform:translateX(-200px); }} 100% {{ transform:translateX(110vw); }} }}
            @keyframes pulse {{ 0%,100% {{ box-shadow:0 0 60px #ffb300; }} 50% {{ box-shadow:0 0 120px #ffb300,0 0 200px #ffe066; }} }}
            @keyframes float {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-20px); }} }}
            @keyframes mistmove {{ 0% {{ transform:translateX(-50%); }} 100% {{ transform:translateX(0%); }} }}
            @keyframes flash {{ 0%,89%,91%,93%,100% {{ opacity:0; }} 90%,92% {{ opacity:1; }} }}
            div[data-testid="metric-container"] {{ background:rgba(255,255,255,0.15);border-radius:12px;padding:10px;border:1px solid rgba(255,255,255,0.2);position:relative;z-index:1; }}
            .stTextInput input {{ background:rgba(255,255,255,0.15);color:white;border:1px solid rgba(255,255,255,0.3);border-radius:10px; }}
            .stButton button {{ background:rgba(255,255,255,0.2);color:white;border:1px solid rgba(255,255,255,0.4);border-radius:10px; }}
            </style>
            {anim}
        """, unsafe_allow_html=True)

        st.markdown(f'<h1 style="color:white;text-shadow:0 2px 10px rgba(0,0,0,0.3);position:relative;z-index:1">📍 {data["name"]}, {data["sys"]["country"]}</h1>', unsafe_allow_html=True)
        st.markdown(f'<h3 style="color:rgba(255,255,255,0.9);position:relative;z-index:1">{icon} {data["weather"][0]["description"].title()}</h3>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric(f'🌡️ Temp', f"{data['main']['temp']}{temp_symbol}")
        col2.metric('🤔 Feels Like', f"{data['main']['feels_like']}{temp_symbol}")
        col3.metric('💧 Humidity', f"{data['main']['humidity']}%")
        col4.metric(f'💨 Wind', f"{data['wind']['speed']} {speed_symbol}")

        col5, col6, col7 = st.columns(3)
        col5.metric('⬆️ Max', f"{data['main']['temp_max']}{temp_symbol}")
        col6.metric('⬇️ Min', f"{data['main']['temp_min']}{temp_symbol}")
        col7.metric('🔵 Pressure', f"{data['main']['pressure']} hPa")

        st.divider()

        # 5 day forecast
        st.subheader('📅 5-Day Forecast')
        forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={units}'
        forecast_data = requests.get(forecast_url).json()

        dates, max_temps, min_temps = [], [], []
        for item in forecast_data['list'][::8]:
            dates.append(datetime.fromtimestamp(item['dt']).strftime('%b %d'))
            max_temps.append(item['main']['temp_max'])
            min_temps.append(item['main']['temp_min'])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=max_temps, mode='lines+markers',
                                  name='Max Temp', line=dict(color='#ff6b6b', width=3), marker=dict(size=10)))
        fig.add_trace(go.Scatter(x=dates, y=min_temps, mode='lines+markers',
                                  name='Min Temp', line=dict(color='#00d4ff', width=3), marker=dict(size=10)))
        fig.update_layout(
            title=f'5-Day Forecast for {city.title()}',
            xaxis_title='Date', yaxis_title=f'Temperature ({temp_symbol})',
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'), legend=dict(x=0, y=1.1, orientation='h')
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error('❌ City not found! Please check the spelling and try again.')
