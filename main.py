import streamlit
import pandas as pd


def main() -> None:
    fruit_list = (
        pd
            .read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
            .set_index("Fruit")
    )
    
    streamlit.header("Breakfast Menu")
    streamlit.text("Omega 3 & Blueberry Oatmeal")
    streamlit.text("Kale, Spinach & Rocket Smoothie")
    streamlit.text("Hard-Boiled Free-Range Egg")
    
    fruit_selection = streamlit.multiselect("Pick some fruits:", list(fruit_list.index), ["Avocado", "Strawberries"])
    streamlit.dataframe(fruit_list.loc[fruit_selection, :])


if __name__ == "__main__":
    main()
