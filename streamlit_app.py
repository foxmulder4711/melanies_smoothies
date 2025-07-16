# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize your Smoothie :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

# Define key-value pairs
#options = {"Banana": "Banana:banana:", "Strawberries": "Strawberries:strawberry:", "Peaches": "Peaches:peach:"}

#option = st.selectbox("Choose an option:", options.keys())

#st.write("You selected:", option)

# Get the corresponding value
#selected_value = options[option]

#st.write("You selected:", selected_value)

cnx = st.connection("snowflake")
session = cnx.session()

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

#st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect(
    "Choose up to 5 ingredients:"
    , my_dataframe
    , max_selections = 5
)

name_on_order = st.text_input('Name on smoothie:')
st.write('The name on the order: '+name_on_order)

if ingredient_list:
    st.write(ingredient_list)
    st.text(ingredient_list)

    ingredients_string = ''

    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

    st.write(my_insert_stmt)

    if ingredients_string:
        time_to_insert = st.button('Submit order')

        if time_to_insert:
        
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
