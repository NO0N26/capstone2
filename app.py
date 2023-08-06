import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
import os
import numpy as np
import time



# Function to display the image based on the selected crop and year
def display_image(crop, year):
    # Load the data based on the selected crop
    if crop == 'Carrot':
        df = pd.read_excel('finalcarrot.xlsx')
    elif crop == 'Cassava':
        df = pd.read_excel('finalcassava.xlsx')
    elif crop == 'Gabi':
        df = pd.read_excel('gabifinal.xlsx')
    elif crop == 'Potato':
        df = pd.read_excel('potatofinal.xlsx')
    elif crop == 'SweetPotato':
        df = pd.read_excel('sweetpotatofinal.xlsx')

    # Perform data manipulation
    df.set_index(pd.Index(['Month', 'Price (per kg)']), inplace=True)
    df = df.T
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Date'}, inplace=True)
    df['Date'].replace(r'^Unnamed.*', pd.NA, regex=True, inplace=True)
    df['Date'].fillna(method='ffill', inplace=True)
    df['Date'] = df['Date'].astype(int)
    df['Date'] = df['Date'].astype(str)
    df['Date'] = df['Date'] + " " + df['Month']
    df.drop(columns=['Month'], inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y %B')
    df.set_index('Date', inplace=True)
    dates = pd.date_range(start=df.index[0], end=df.index[-1], freq='MS')
    dates = dates.to_period('D').to_timestamp()
    df['Price (per kg)'] = df['Price (per kg)'].astype(float)

    # Create two columns
    col1, col2 = st.columns(2)

    # In the left column (col1), display the data
    with col1:
        st.dataframe(df, width=300, height = 385)

    # In the right column (col2), display the image
    with col2:
        # Convert crop to lowercase and replace space with underscore for folder name
        folder_name = crop.lower().replace(" ", "_")
        image_folder = f"{folder_name}/"
        
        # Check if the folder for the selected crop exists
        if not os.path.exists(image_folder):
            st.warning(f"Image folder for {crop} not found.")
            return

        # Construct the image path based on the selected year
        if year == 'All':
            image_path = os.path.join(image_folder, f"{folder_name}_all.png")
        else:
            image_path = os.path.join(image_folder, f"{folder_name}_{year}.png")

        # Check if the image file exists
        if not os.path.exists(image_path):
            st.warning(f"Image for {crop} in {year} not found.")
            return

        img = Image.open(image_path)

        # Specify the desired width and height for resizing
        desired_width = 400
        desired_height = 400

        # Resize the image to the desired size
        resized_img = img.resize((desired_width, desired_height))

        # Center the image on the page using CSS
        st.markdown(
            f'<div style="display: flex; justify-content: center;"><img src="data:image/png;base64,{image_to_base64(resized_img)}" style="width:{desired_width}px; height:{desired_height}px;"></div>',
            unsafe_allow_html=True
        )

     # Add some spacing (line break) after the image
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)




     # Add the label after the image
    st.markdown(
        f'<p style="font-size: 30px; color: black;"><strong>Forecasted Value</strong></p>',
        unsafe_allow_html=True
    )
     # Load the Excel data into a DataFrame based on the selected crop
    if crop.lower() == 'carrot':
        file_path = 'finalcarrot.xlsx'
    elif crop.lower() == 'sweetpotato':
        file_path = 'sweetpotatofinal.xlsx'
    elif crop.lower() == 'cassava':
        file_path = 'finalcassava.xlsx'
    elif crop.lower() == 'gabi':
        file_path = 'gabifinal.xlsx'
    elif crop.lower() == 'potato':
        file_path = 'potatofinal.xlsx'
    sheet_name = 'forecast'
    # Load the Excel data into a DataFrame
    try:
        col1, col2 = st.columns(2)
        # In the left column, display the DataFrame
        with col1:
            df = pd.read_excel(file_path, sheet_name=sheet_name, index_col=0)
            st.dataframe(df, width=300, height = 420)  # Adjust the height as needed
        # In the right column, plot the data as a graph
        with col2:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            plt.figure(figsize=(6.7, 9))
            plt.plot(df['Date'], df['Price (per kg)'], marker='o', color='blue')
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.title('PRICE FORECAST')
            plt.xticks(rotation=45)
            # Pass the Matplotlib figure to st.pyplot()
            st.pyplot(plt)

    except FileNotFoundError:
        st.error("Error: File not found. Please check the file path and try again.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
# Custom CSS styles to adjust the width of specific select boxes
    custom_styles = """
    <style>
    /* Adjust the width of specific select boxes as needed */
    .custom-selectbox1 .st-ax {
        width: 200px;
    }
    .custom-selectbox2 .st-ax {
        width: 250px;
    }
    /* Add more custom styles for other select boxes as needed */
    </style>
    """
    st.markdown(custom_styles, unsafe_allow_html=True)


def main():
    # Set page configuration
    # HTML snippet for the centered "Select Crops" text
    st.markdown(
        f'<p style="font-size: 30px; color: black;"><strong>National Capital Region (NCR)</strong></p>',
        unsafe_allow_html=True
    )
    # List of crops for the first dropdown
    options_1 = ["Carrot", "Cassava", "Gabi", "Potato", "SweetPotato"]
    # List of years from 2012 to 2023 and 'All' for the second dropdown
    options_2 = [str(year) for year in range(2012, 2024)]
    options_2.append('All')

    # Create two columns
    col1, col2 = st.columns(2)

    # In the first column, create the first dropdown
    with col1:
        
        st.markdown('<div class="custom-selectbox1">', unsafe_allow_html=True)
        selected_crop = st.selectbox('Select Commodity:', options_1)
        st.markdown('</div>', unsafe_allow_html=True)

    # In the second column, create the second dropdown
    with col2:
        st.markdown('<div class="custom-selectbox2">', unsafe_allow_html=True)
        selected_year = st.selectbox('Select a Year:', options_2)
        st.markdown('</div>', unsafe_allow_html=True)

    # Display the image based on the selected crop and year
    display_image(selected_crop, selected_year)

def image_to_base64(img):
    from io import BytesIO
    import base64

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    
    return base64.b64encode(buffered.getvalue()).decode()

if __name__ == '__main__':
    main()