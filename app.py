import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import requests
import os
import sys
from datetime import datetime, timedelta
from cognite.client.utils import datetime_to_ms, ms_to_datetime
from pathlib import Path
import utils.auth as cauth


# -------------- SETTINGS --------------

page_title = "Cognite Accenture Tiger Instance ML models tracker"
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
page_icon = ":twisted_rightwards_arrows:"
layout = "centered"
# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- NAVIGATION MENU ---
option = option_menu(
    menu_title=None,
    options=["Rate of Penetration Prediction", "Machine Maintenance"],
    icons=["pencil-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)


# Create Cognite Client
c = cauth.create_cognite_client('client-secret')
print(c.login.status())

st.header(option)

if option == 'Rate of Penetration Prediction':

    st.subheader("Utah Forge Well Site")

    st.write("""
                  The U.S. Department of Energy’s Frontier Observatory for Research in Geothermal  Energy (FORGE)
                  is a field laboratory that offers opportunities to research, develop, and test
                  new technologies for enhanced geothermal systems.

                  """)

    image_labels = {
        "Image_3": "Image_1: Forge Site Location",
        "Image_4": "Image_2: Geological map of the FORGE Utah site",
        "Image_5": "Image_3: Cross section of the FORGE Utah site"
    }

    for index in range(3, 6):
        file_obj = c.files.retrieve(
            external_id=f"rop_well5832_energies-15-04288-g00{index}.png")
        # Lord Image to Memory
        file = c.files.download_bytes(id=file_obj.id)

        st.image(file)

        st.write(image_labels[f"Image_{index}"])

    st.subheader("Machine Readings of equipments Sequence data")
    st.write("Dataset used to fit rate of penetration (rop) model")

    c.data_sets.retrieve(external_id="rop_wells")
    dataset_id = c.data_sets.retrieve(external_id="rop_wells").id
    data_plot = c.sequences.data.retrieve_dataframe(
        external_id="well5832_sequence", start=0, end=-1)
    st.dataframe(data_plot)

    st.subheader("ROP Prediction Result")

    data_plot = c.sequences.data.retrieve_dataframe(
        external_id="well5832_sequence_model", start=0, end=-1)
    st.write(data_plot)

    st.line_chart(data=data_plot, x="Depth(m)", width=900, height=450)

    # st.subheader("Cognite Well Architecture")
    #
    # file_obj = c.files.retrieve(id=3791052376112203)
    # st.write(file_obj)
    # # Lord Image to Memory
    # file = c.files.download_bytes(id=file_obj.id)
    #
    # st.image(file)

if option == 'Machine Maintenance':
    st.subheader("Predictive Equipment Failures -- ConocoPhillips")

    st.subheader("Background")

    bg = '''80% of producing oil wells in the United States are classified as stripper wells. Stripper wells produce low volumes at the well level, but at an aggregate level these wells are responsible for a significant percentage of domestic oil production.

Stripper wells are attractive to a company due to their low operational costs and low capital intensity - ultimately providing a source of steady cash flow to fund operations that require more funds to get off the ground.

At ConocoPhillips, our West Texas Conventional operations serve as a source of organic cash flow to fund more expensive projects in the Delaware Basin and other unconventional plays across the United States. As a company, it is vital that this steady, low cost form of cash has a constant presence.

As with all mechanical equipment, things break and when things break money is lost in the form of repairs and lost oil production. When costs go up cash goes down, but how can we predict when equipment will fail and use this information to drive down our costs?'''

    st.write(bg)

    st.write("Use equipment sensor data to prediction equipment failure.")

    file_obj = c.files.retrieve(external_id="cp_wells_diag")
    # st.write(file_obj)
    # Lord Image to Memory
    file = c.files.download_bytes(id=file_obj.id)

    st.image(file)

    st.subheader("The Challenge")

    challenge = '''A data set has been provided that has documented failure events that occurred on surface equipment and down-hole equipment. For each failure event, data has been collected from over 107 sensors that collect a variety of physical information both on the surface and below the ground.

Using this data, can we predict failures that occur both on the surface and below the ground? Using this information, how can we minimize costs associated with failures?

The goal of this challenge will be to predict surface and down-hole failures using the data set provided. This information can be used to send crews out to a well location to fix equipment on the surface or send a workover rig to the well to pull down-hole equipment and address the failure.'''

    st.write(challenge)

    st.subheader(
        "Cognite CP_WELL Well Sensor list used for prediction of machine failure")
    res_ts = c.time_series.search(name="sensor", limit=200)
    df_ts = res_ts.to_pandas()
    st.write(df_ts)

    st.subheader(
        "Cognite CP_WELL Well Architecture maintenance Prediction Event")
    start_date = datetime_to_ms(datetime(2021, 7, 1))
    print(start_date)
    data_for_func = {"start_date": start_date, "days": 15}
    start_date = ms_to_datetime(data_for_func['start_date'])
    duration = data_for_func['days']
    # 30 days of training data chosen arbitrarily
    end_date = start_date + timedelta(days=duration)
    ts_equip_obj = c.time_series.retrieve(
        external_id="equipment_failure_status")
    data_for_evaluation = c.datapoints.retrieve_dataframe(
        id=ts_equip_obj.id,
        start=start_date,
        end=end_date,
        column_names="id"
    )
    # pull the ground truth for evaluation
    # st.write(data_for_evaluation)
    st.write(f"{ts_equip_obj.id}: ground truth")
    st.line_chart(data_for_evaluation)
    ts_equip_pred = c.time_series.retrieve(
        external_id="equipment_failure_prediction")
    data_for_pred = c.datapoints.retrieve_dataframe(
        id=ts_equip_pred.id,
        start=start_date,
        end=end_date,
        column_names="id"
    )

    {"ground truth": ts_equip_obj.id, "prediction": ts_equip_pred.id}

    # data_for_pred[str(ts_equip_obj.id)
    #               ] = data_for_evaluation[str(ts_equip_obj.id)]
    # pull the ground truth for evaluation
    # st.write(data_for_pred)
    st.line_chart(data_for_pred)


# if option == 'grafana dashboard':
    st.subheader("Grafana Dashboard Time Series Data")
    html_pred = """
                    <iframe src="http://localhost:3000/d-solo/6w9BGZf4k/ml-maintenance?orgId=1&from=1625057812673&to=1627098764657&theme=dark&panelId=123127" width="450" height="200" frameborder="0"></iframe>
                  """

    st.markdown(html_pred, unsafe_allow_html=True)

    html_failure = """
                    <iframe src="http://localhost:3000/d-solo/6w9BGZf4k/ml-maintenance?orgId=1&from=1625057812673&to=1627098764657&theme=dark&panelId=123125" width="450" height="200" frameborder="0"></iframe>
                  """

    st.markdown(html_failure, unsafe_allow_html=True)
