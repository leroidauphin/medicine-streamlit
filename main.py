import pandas as pd
import streamlit as st

from config import people_file_path, medicines_file_path
from doses import add

# read static metadata
people = pd.read_csv(people_file_path)
medicines = pd.read_csv(medicines_file_path)

# add new dose
def _add_new_dose(people_name, medicine_name):
    person_id = people[people["name"] == people_name].index[0]
    medicine_id = medicines[medicines["name"] == medicine_name].index[0]
    add(person_id, medicine_id)

columns = st.columns(3)

with columns[0]:
    person = st.selectbox("Who", people["name"])

with columns[1]:
    medicine = st.selectbox("What", medicines["name"])

with columns[2]:
    st.button("Add", on_click=_add_new_dose, args=(person, medicine))




