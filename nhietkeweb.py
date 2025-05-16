import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# Tạo giao diện nhập thời gian
st.title("Ứng dụng mô phỏng nhiệt độ & độ ẩm 🚀")

start_date = st.text_input("Ngày bắt đầu (DD/MM/YYYY):")
start_time = st.text_input("Giờ bắt đầu (HH:MM:SS):")
end_date = st.text_input("Ngày kết thúc (DD/MM/YYYY):")
end_time = st.text_input("Giờ kết thúc (HH:MM:SS):")

if st.button("Tạo dữ liệu"):
    try:
        start_datetime_str = f"{start_date} {start_time}"
        end_datetime_str = f"{end_date} {end_time}"

        start_time = datetime.strptime(start_datetime_str, "%d/%m/%Y %H:%M:%S")
        end_time = datetime.strptime(end_datetime_str, "%d/%m/%Y %H:%M:%S")

        if start_time >= end_time:
            st.error("Thời gian bắt đầu phải nhỏ hơn thời gian kết thúc!")
        else:
            month = start_time.month
            season = "mưa" if 5 <= month <= 10 else "khô"
            base_temperature = random.uniform(24, 26) if season == "mưa" else random.uniform(25, 27)
            base_humidity = random.uniform(50, 70) if season == "mưa" else random.uniform(40, 60)

            data = []
            current_time = start_time
            while current_time <= end_time:
                hour = current_time.hour
                temperature = base_temperature + random.uniform(-1, 2) if 10 <= hour < 15 else base_temperature + random.uniform(-1, 1)
                humidity_variation = random.uniform(-2, 2)
                humidity = base_humidity - (temperature - base_temperature) * 1.2 + humidity_variation

                temperature = round(min(max(temperature, 22), 28), 1)
                humidity = round(min(max(humidity, 40), 80), 1)

                data.append([current_time, temperature, humidity])
                current_time += timedelta(minutes=30)

            df = pd.DataFrame(data, columns=['Ngày tháng', 'Nhiệt độ (°C)', 'Độ ẩm (%)'])

            st.success("Dữ liệu đã được tạo thành công!")
            st.dataframe(df)

            csv = df.to_csv(index=False)
            st.download_button(label="Tải xuống dữ liệu Excel", data=csv, file_name="nhietke_data.csv", mime="text/csv")

    except ValueError:
        st.error("Vui lòng nhập ngày và giờ đúng định dạng!")