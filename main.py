from datetime import datetime, timedelta
import pandas as pd
import streamlit as st

from config import people_file_path, medicines_file_path
from doses import add, doses_last_24hrs

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

doses = doses_last_24hrs()
doses_with_persons = doses.merge(people, left_on="people_id", right_index=True)
full_df = doses_with_persons.merge(medicines, left_on="medicines_id", right_index=True)
summary = full_df.groupby(['people_id', 'medicines_id']).agg(['min', 'max', 'size'])
display_df = full_df.drop(["people_id", "medicines_id"], axis=1)

for i, row in summary.iterrows():
    person_name = row["name_x"]["max"]
    medicine_name = row["name_y"]["max"]

    daily_doses_agg = row["max_per_24hrs"]
    if daily_doses_agg["size"] >= daily_doses_agg["max"]:
        next_dose = row["dose_datetime"]["min"]
    elif row["dose_datetime"]["max"] + timedelta(hours=4) >= datetime.now():
        next_dose = row["dose_datetime"]["max"] + timedelta(hours=4)

    st.text(f"{person_name} next dose of {medicine_name} at {next_dose}.")
