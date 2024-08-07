import streamlit as st
import plotly.graph_objs as go
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# Predator Prey model (Lotka-Volterra)

st.markdown("""
<style>
h1 {
    font-size: 24px; 
}
h3{
    text-align: center;
}
p{
    text-align: center;
}
            
</style>
""", unsafe_allow_html=True)

st.title("Predator-Prey Model Simulator (Lokta-Volterra)")

with st.sidebar:
    st.subheader('Context')
    st.write('From the early 1800s to 1900s, the Hudson Bay company kept careful records of all furs, which can be used a representation of wild lynx (predator) and hare (prey) populations. Below is graph that shows distinct oscillations in 12-year periods.')
    st.image('hudson.jpeg')
    st.write('In 1912, American Biologist Alfred Lotka developed a mathematical model descrbing this cyclical nature. This population dynamics model is used to describe the species dynamics in an ecosystem where one species acts as a predator and the other as a prey.')
    st.image('lynxhare.jpeg')
    st.write('Assumptions: Exponential growth of prey, predator dependence on prey, constant encounter rate, static conversion efficiency, no environmental factors or genetic variation, and closed system.')
col1, col2, col3 = st.columns([1,1,2])

with col1:
    x = st.slider('Starting number of prey (x)', 0, 100, 50, 1)
    y = st.slider('Starting number of predators (y)', 0, 100, 20, 1)
    t = st.slider('Number of generations', 1, 50, 30, 1)
    alpha = st.slider('Prey growth rate (α)', 1.0, 2.0, 1.2, 0.05)

with col2:
    beta = st.slider('Predation rate coefficient (β)', 0.01, 0.5, 0.1, 0.05)
    delta = st.slider('Predator reproduction rate coefficient (δ)', 0.01, 0.2, 0.05, 0.01)
    gamma = st.slider('Predator natural dying rate (γ)', 0.1, 1.5, 1.0, 0.05)
    

def model (z, t, alpha, beta, delta, gamma):
    x, y = z
    dxdt = (alpha * x) - (beta * x * y)
    dydt = (delta * x * y) - (gamma * y)
    
    return [dxdt, dydt]


#t = end point of time
#x is prey, y is predator
def model_run(x, y, t, alpha, beta, delta, gamma):
    z0 = [x, y]

    num_points = 8*t
    t0 = np.linspace(0, t, num_points)
    #Creates a NumPy 2d array representing a system of differential equations. Each row is a different time point and the two columns 
    # are prey and predator
    sol = odeint(model, z0, t0, args=(alpha, beta, delta, gamma))

    prey, predator = sol[:, 0], sol[:, 1]


    fig = go.Figure()

    fig.add_trace(go.Scatter(x=t0, y=prey, mode='lines', name='Prey',line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=t0, y=predator, mode='lines', name='Predator', line=dict(color='orange')))

    fig.update_layout(
        xaxis_title='Time (generations)',
        yaxis_title='Population',
        legend_title='Species'
    )

    return fig

with col3:
    LVfig = model_run(x, y, t, alpha, beta, delta, gamma)

    st.plotly_chart(LVfig)

st.divider()

col4, col5 = st.columns([1 ,2.5])

with col4:
    st.subheader('Equations')
    st.latex(r'''
        \frac{dx}{dt} = \alpha x - \beta xy
    ''')
    st.latex(r'''
        \frac{dy}{dt} = \delta xy - \gamma y
    ''')

with col5:
    st.subheader('Parameters')
    st.write('x: Number of Prey')
    st.write('y: Number of Predators')
    st.write('α (Prey Growth Rate): The growth rate of prey in the absence of predators ')
    st.write('β (Predation Rate Coefficient): How effectively predators are able to consume prey ')
    st.write('δ (Predator Reproduction Rate Coefficient): How efficient predators convert prey into new predators')
    st.write('γ: Predator Natural Dying Rate: Rate at which predators die in the absence of prey')


#    cd "/Users/alanwang/VSCode/AW-BIOL174_Homework/Final Project"
#    streamlit run finalproject.py