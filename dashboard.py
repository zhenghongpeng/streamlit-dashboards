import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
import sys
from datetime import datetime, timedelta
from cognite.client.utils import datetime_to_ms, ms_to_datetime
from pathlib import Path
import matplotlib.pyplot as plt
import utils.auth as cauth

# Create Cognite Client
c = cauth.create_cognite_client('client-secret')
print(c.login.status())

option = st.sidebar.selectbox("Which Dashboard?", ('welldiagram','machinereadings', 'mlresults', 'cognite', "cp_well", 'cp_well_maintenance_prediction', 'cp_well_sensor_list'), 3)

st.header(option)

if option == 'machinereadings':
    st.subheader("Machine Readings of equipments Sequence data")

    c.data_sets.retrieve(external_id="rop_wells")
    dataset_id =c.data_sets.retrieve(external_id="rop_wells").id
    data_plot = c.sequences.data.retrieve_dataframe(external_id="well5832_sequence",start=0,end=-1)
    st.write(data_plot)

if option == 'mlresults':
    st.subheader("ROP Prediction Result")

    data_plot = c.sequences.data.retrieve_dataframe(external_id="well5832_sequence_model",start=0,end=-1)
    st.write(data_plot)

    st.line_chart(data=data_plot, x="Depth(m)")

if option == 'cognite':
    st.subheader("Cognite Utah Well Site")

    for index in range(3,6):
        file_obj =  c.files.retrieve(external_id=f"rop_well5832_energies-15-04288-g00{index}.png")
        st.write(file_obj)
        ## Lord Image to Memory
        file = c.files.download_bytes(id=file_obj.id)

        st.image(file)

if option == 'welldiagram':
    st.subheader("Cognite Well Architecture")

    file_obj =  c.files.retrieve(id=3791052376112203)
    st.write(file_obj)
    ## Lord Image to Memory
    file = c.files.download_bytes(id=file_obj.id)

    st.image(file)

if option == 'cp_well':
    st.subheader("Cognite CP_WELL Well Architecture maintenance Diagram")
    file_obj =  c.files.retrieve(external_id="cp_wells_diag")
    st.write(file_obj)
    ## Lord Image to Memory
    file = c.files.download_bytes(id=file_obj.id)

    st.image(file)

if option == 'cp_well_maintenance_prediction':
    st.subheader("Cognite CP_WELL Well Architecture maintenance Prediction Event")
    start_date = datetime_to_ms(datetime(2021, 7, 1))
    print(start_date)
    data_for_func= {"start_date":start_date, "days":15}
    start_date =  ms_to_datetime(data_for_func['start_date'])
    duration = data_for_func['days']
    # 30 days of training data chosen arbitrarily
    end_date = start_date + timedelta(days=duration)
    ts_equip_obj = c.time_series.retrieve(external_id="equipment_failure_status")


    data_for_evaluation = c.datapoints.retrieve_dataframe(
        id=ts_equip_obj.id,
        start=start_date,
        end=end_date,
        column_names="id"
    )
    # pull the ground truth for evaluation
    st.write(data_for_evaluation)
    st.line_chart(data_for_evaluation)

    ts_equip_obj = c.time_series.retrieve(external_id="equipment_failure_prediction")


    data_for_pred = c.datapoints.retrieve_dataframe(
        id=ts_equip_obj.id,
        start=start_date,
        end=end_date,
        column_names="id"
    )
    data_for_pred["6046610976207022"]=data_for_evaluation["6046610976207022"]
    # pull the ground truth for evaluation
    st.write(data_for_pred)
    st.line_chart(data_for_pred)


if option == 'cp_well_sensor_list':
    st.subheader("Cognite CP_WELL Well Sensor list used for prediction of machine failure")
    res_ts =c.time_series.search(name="sensor", limit =200)
    df_ts = res_ts.to_pandas()
    st.write(df_ts)






