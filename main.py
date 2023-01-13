"""
Simple streamlit application created as part of the Snowflake Data Application Builders Workshop.
"""
import pandas as pd
import requests
import snowflake.connector
import streamlit
import urllib.error


def add_text() -> None:
    """
    Add the text at the top of the application.
    """
    streamlit.header("Breakfast Menu")
    streamlit.text("Omega 3 & Blueberry Oatmeal")
    streamlit.text("Kale, Spinach & Rocket Smoothie")
    streamlit.text("Hard-Boiled Free-Range Egg")

    
def add_fruit_selection() -> None:
    """
    Add a fruit table with a fruit picker above it.
    """
    fruit_list = (
        pd
            .read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
            .set_index("Fruit")
    )
    fruit_selection = streamlit.multiselect("Pick some fruits:", list(fruit_list.index), ["Avocado", "Strawberries"])
    streamlit.dataframe(fruit_list.loc[fruit_selection, :])
    

def add_fruityvice_table() -> None:
    """
    Call the Fruityvice API and display the response.
    """
    streamlit.header("Fruityvice Data")
    
    try:
        fruit_choice = streamlit.text_input("Which fruit would you like information about?", "Kiwi")
        if not fruit_choice:
            streamlit.error("Please select a fruit.")
        else:
            endpoint = f"https://fruityvice.com/api/fruit/{fruit_choice}"

            fruityvice_normalized = pd.json_normalize(requests.get(endpoint).json())
            streamlit.dataframe(fruityvice_normalized)
    except urllib.error.URLError as e:
        streamlit.error()

            
def add_snowflake_user_details(cursor) -> None:
    """
    Writie details about the Snowflake user currently connected.
    """
    cursor.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")

    streamlit.text("Hello from Snowflake:")
    streamlit.text(cursor.fetchone())
    
    
def add_fruit_load_list(cursor) -> None:
    """
    Display the fruit load list from the database.
    """
    cursor.execute("SELECT * FROM PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
    
    streamlit.text("Fruit load list contents:")
    streamlit.dataframe(cursor.fetchall())
    
    
def add_fruit_to_load_list(cursor) -> None:
    """
    Display the fruit load list from the database.
    """
    fruit_choice = streamlit.text_input("Which fruit would you like to add to the list?", "Jackfruit")
    
    streamlit.write(f"Thanks for adding {fruit_choice}")
    cursor.execute(f"""
        INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST
        VALUES ('{fruit_choice}')
    """)
    
    
def main() -> None:
    """
    Entry point into the application.
    """
    snow_conn = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    snow_curr = snow_conn.cursor()
    
    add_text()
    add_fruit_selection()
    add_fruityvice_table()
    add_snowflake_user_details(cursor=snow_curr)
    if streamlit.button("Get fruit load list"):
        add_fruit_load_list(cursor=snow_curr)

    fruit_choice = streamlit.text_input("Which fruit would you like to add to the list?", "Jackfruit")
    if streamlit.button("Get fruit load list"):
        add_fruit_to_load_list(cursor=snow_curr)


if __name__ == "__main__":
    main()
