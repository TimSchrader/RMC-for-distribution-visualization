import streamlit as st
import pandas as pd
import math
#from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='RMC4Vis',
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

def isNumber(someString) -> bool:
    return someString.replace('.','',1).isdigit()
# -----------------------------------------------------------------------------
# initialization
if 'initialized' not in st.session_state \
    or not st.session_state.initialized:
    st.session_state.initialized = True
    st.session_state.constraints=[]
# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# RMC4Vis

This is a simple implementation of a [Reverse Monte Carlo algorithm](https://en.wikipedia.org/wiki/Reverse_Monte_Carlo) for visualizing a distribution using only simple constraints.
This is useful if you need to visualize a distribution while making very few assumptions about it.
'''

min_size_allowed = 10
max_size_allowed = 10000
default_size = 20

size = st.slider(
    'How many data points should be simulated for the distribution? (faster for few data points, more accurate for more data points)',
    min_value=min_size_allowed,
    max_value=max_size_allowed,
    value=default_size)

st.header('constrains', divider='gray')
# This section is written in way that makes it easy to add new constraints,
# even when this leads to duplicate code.

addedConstraint=st.selectbox("Add a constraint",\
                             ("Minimum","Maximum","Mean","Standard Deviation","Range"))

if (addedConstraint=="Minimum"):
    col1, col2 = st.columns([1,1], vertical_alignment="bottom")
    with col1: minValue = st.text_input("Minimum")
    with col2: weight = st.text_input("Weight of this constraint",value="100",key="weightMin")
    if isNumber(minValue):
        st.session_state.constraints.append({"type":"min","value":minValue,"weight":weight})
elif (addedConstraint=="Maximum"):
    col1, col2 = st.columns([1,1], vertical_alignment="bottom")
    with col1: maxValue = st.text_input("Maximum")
    with col2: weight = st.text_input("Weight of this constraint",value="100",key="weightMax")
    if isNumber(maxValue):
        st.session_state.constraints.append({"type":"max","value":maxValue,"weight":weight})
elif (addedConstraint=="Mean"):
    col1, col2 = st.columns([1,1], vertical_alignment="bottom")
    with col1: meanValue = st.text_input("Mean")
    with col2: weight = st.text_input("Weight of this constraint",value="1",key="weightMean")
    if isNumber(meanValue):
        st.session_state.constraints.append({"type":"mean","value":meanValue,"weight":weight})
elif (addedConstraint=="Standard Deviation"):
    col1, col2 = st.columns([1,1], vertical_alignment="bottom")
    with col1: stdValue = st.text_input("Standard Deviation")
    with col2: weight = st.text_input("Weight of this constraint",value="1",key="weightStdDev")
    if isNumber(stdValue):
        st.session_state.constraints.append({"type":"std","value":stdValue,"weight":weight})
elif (addedConstraint=="Range"):
    col1, col2, col3, col4 = st.columns([1,1,1,1], vertical_alignment="bottom")
    with col1: fromValue = st.text_input("From")
    with col2: toValue = st.text_input("To")
    with col3: amountValue = st.text_input("Amount")
    with col4: weight = st.text_input("Weight of this constraint",value="1",key="weightRange")
    if isNumber(fromValue) and isNumber(toValue) and isNumber(amountValue):
        st.session_state.constraints.append({"type":"range","fromValue":fromValue,"toValue":toValue,"value":amountValue,"weight":weight})

constrText = ""
for constr in st.session_state.constraints:
    if constr["type"]=="max":
        constrText += f"The maximum is {constr['value']} (weight: {constr['weight']})\n\n"
    elif constr["type"]=="min":
        constrText += f"The minimum is {constr['value']} (weight: {constr['weight']})\n\n"
    elif constr["type"]=="mean":
        constrText += f"The mean is {constr['value']} (weight: {constr['weight']})\n\n"
    elif constr["type"]=="std":
        constrText += f"The standard deviation is {constr['value']} (weight: {constr['weight']})\n\n"
    elif constr["type"]=="range":
        constrText += f"{constr['value']} data points are between {constr['fromValue']} and {constr['toValue']} (weight: {constr['weight']})\n\n"
st.write(constrText)

st.header('distribution', divider='gray')

distr_df=pd.DataFrame({"x":[1,2,3,4,5,6,7,8,9],"y":[1,2,3,6,6,6,3,2,1]})

''

st.line_chart(
    distr_df,
    x="x",
    y='y',
)
