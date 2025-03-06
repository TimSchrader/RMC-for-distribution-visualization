import streamlit as st
import pandas as pd
import scipy
from rmc import rmc

# Set the title in the Browser's tab bar.
st.set_page_config(page_title='RMC4Vis')

# -----------------------------------------------------------------------------
# Declare some useful functions.

def isNumber(someString) -> bool:
    return someString.replace('.','',1).replace('-','',1).isdigit()

def applyConstr(fromVal,toVal,percentVal,weight):
    '''adds a constraint to lists of constraints'''

    # check if input is reasonable
    if not isNumber(fromVal) or not isNumber(toVal)\
              or not isNumber(percentVal) or not isNumber(weight):
        return
    if float(percentVal) <0.0 or float(percentVal) > 100.0:
        return
    if float(fromVal) >= float(toVal):
        return
    
    # don't allow duplicates
    if fromVal in st.session_state.starts and toVal in st.session_state.ends and \
        percentVal/100.0 in st.session_state.fracts and weight in st.session_state.weights:
        return
    
    # add constraint
    st.session_state.starts.append(float(fromVal))
    st.session_state.ends.append(float(toVal))
    st.session_state.fracts.append(float(percentVal)/100.0)
    st.session_state.weights.append(float(weight))

def removeConstr(indexToRemove,dummy):
    '''removes a constraint from lists of constraints'''
    st.session_state.starts.pop(indexToRemove)
    st.session_state.ends.pop(indexToRemove)
    st.session_state.fracts.pop(indexToRemove)
    st.session_state.weights.pop(indexToRemove)

def rmcWrapper():
    '''calls the reverse Monte Carlo method'''

    # adds the total range
    wrappedStarts = st.session_state.starts + [min(st.session_state.starts)]
    wrappedEnds = st.session_state.ends + [max(st.session_state.ends)]
    wrappedFracts = st.session_state.fracts + [1.0]
    wrappedWeights = st.session_state.weights + [100] # gets ignored

    st.session_state.distr=rmc(st.session_state.size,\
                                st.session_state.steps,\
                                len(st.session_state.starts),\
                                wrappedStarts,\
                                wrappedEnds,\
                                wrappedFracts,\
                                wrappedWeights)
      
# -----------------------------------------------------------------------------
# initialization
if 'initialized' not in st.session_state \
    or not st.session_state.initialized:
    st.session_state.initialized = True
    st.session_state.starts = [0]
    st.session_state.ends = [10]
    st.session_state.fracts = [1]
    st.session_state.weights = [1]
    st.session_state.distr = [1,4,5,5,5]

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# RMC for distribution visualization

This is a simple implementation of a 
[Reverse Monte Carlo algorithm](https://en.wikipedia.org/wiki/Reverse_Monte_Carlo) 
(RMC) for visualizing a distribution using only simple constraints.
This is useful if you need to visualize a distribution while making very few 
assumptions about it.
'''

# slider for the number of data points in the distribution
min_size_allowed = 10
max_size_allowed = 1000
default_size = 20
st.session_state.size = st.slider(
    'How many points will be simulated?',
    min_value=min_size_allowed,
    max_value=max_size_allowed,
    value=default_size)

# slider for the number of steps taken by the RMC
min_steps_allowed = 100
max_steps_allowed = 100000
default_steps = 1000
st.session_state.steps = st.slider(
    'How many steps will the RMC algorithm make?',
    min_value=min_steps_allowed,
    max_value=max_steps_allowed,
    value=default_steps)

st.header('constraints', divider='gray')

# add a constraint
st.write('Please add a constraint. Think of them as a buckets in a histogram. They may overlap.')
col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1], vertical_alignment="bottom")
with col1: fromVal = st.text_input("From")
with col2: toVal = st.text_input("To")
with col3: percentVal = st.text_input("\% of Data in this bucket")
with col4: weight = st.text_input("Weight of this constraint",value="1",key="weightRange")
with col5: st.button("Apply",on_click=applyConstr,args=(fromVal,toVal,percentVal,weight))
  
# display current constraints
for i in range(len(st.session_state.starts)):
    col1, col2= st.columns([4,1], vertical_alignment="bottom")
    with col1: st.write(f"{st.session_state.fracts[i]*100} \% are between \
                        {st.session_state.starts[i]} and \
                        {st.session_state.ends[i]}. (weight: \
                        {st.session_state.weights[i]})")
    with col2: st.button("Remove",on_click=removeConstr,args=(i,"dummy"),key="remove"+str(i))


st.header('distribution', divider='gray')

# run RMC
st.button("Simulate",on_click=rmcWrapper)

# plot the results using scipy KDE for a smooth "histogram"
minxVal = min(st.session_state.starts)
maxxVal = max(st.session_state.ends)
stepSizexVal = (maxxVal - minxVal)/100 #100 points used for plotting
xVals = []
for i in range(100):
    xVals.append(minxVal+i*stepSizexVal)
kde = scipy.stats.gaussian_kde(st.session_state.distr)
yVals = kde.pdf(xVals)
distr_df=pd.DataFrame({"x":xVals,"approximated probability density":yVals})

''
st.line_chart(distr_df, x="x", y='approximated probability density')
