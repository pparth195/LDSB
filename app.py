import streamlit as st
from multiapp import MultiApp
from apps import home, Upload, Combine # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("Extract Image", home.app)
app.add_app("Upload Data", Upload.app)
app.add_app("Combine Files", Combine.app)

# The main app
app.run()