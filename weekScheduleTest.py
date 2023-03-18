import streamlit as st

# Default configuration options
config_options = {

    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Function to update the configuration options
def update_config_options(option, value):
    config_options[option] = value
    st.set_page_config(**config_options)

# Add a button to update the configuration options
if st.button("Update Configuration Options"):
    option = st.selectbox("Select Option", list(config_options.keys()))
    value = st.text_input("Enter Value", config_options[option])
    update_config_options(option, value)

# Add content to the app
st.title("My Streamlit App")
st.write("This is an example of how to change the configuration of a Streamlit app.")
