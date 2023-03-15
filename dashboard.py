import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
import sys
from cognite.client.utils import datetime_to_ms
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import utils.auth as cauth


# Create Cognite Client
c = cauth.create_cognite_client('client-secret')
print(c.login.status())

option = st.sidebar.selectbox("Which Dashboard?", ('rop','machinereadings', 'mlresults', 'cognite'), 3)

st.header(option)

if option == 'machinereadings':
    st.subheader("Machine Readings of equipments Sequence data")

    c.data_sets.retrieve(external_id="rop_wells")
    dataset_id =c.data_sets.retrieve(external_id="rop_wells").id
    data_plot = c.sequences.data.retrieve_dataframe(external_id="well5832_sequence",start=0,end=-1)
    st.write(data_plot)



if option == 'mlresults':
    st.subheader("ROP Prediction Result")

    c.data_sets.retrieve(external_id="rop_wells")
    dataset_id =c.data_sets.retrieve(external_id="rop_wells").id
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

if option == 'rop':
    st.subheader("Cognite Well Architecture")

    file_obj =  c.files.retrieve(id=3791052376112203)
    st.write(file_obj)
    ## Lord Image to Memory
    file = c.files.download_bytes(id=file_obj.id)

    st.image(file)








