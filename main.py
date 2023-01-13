import streamlit
import pandas as pd


def main() -> None:
    fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
    
    streamlit.header('Breakfast Menu')
    streamlit.text('Omega 3 & Blueberry Oatmeal')
    streamlit.text('Kale, Spinach & Rocket Smoothie')
    streamlit.text('Hard-Boiled Free-Range Egg')
    streamlit.dataframe(fruit_list)


if __name__ == "__main__":
    main()
