import pandas as pd
import plotly.graph_objs as go
import streamlit as st

# Function to read and prepare data
def prepare_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Weekday'] = df['Date'].dt.day_name()
    return df

# Function to create candlestick chart for a specific day
def create_candlestick_chart(df, day):
    day_data = df[df['Weekday'] == day]
    fig = go.Figure(data=[go.Candlestick(
        x=day_data['Date'],
        open=day_data['Open'],
        high=day_data['High'],
        low=day_data['Low'],
        close=day_data['Close'],
        name=f'Candlestick ({day})',
        increasing_line_color='green',
        decreasing_line_color='red'
    )])

    # Add annotation for the y-axis title
    fig.add_annotation(
        xref='paper', yref='paper',
        x=0.05, y=0.95,
        text=day,
        showarrow=False,
        font=dict(size=16, color='black')
    )

    fig.update_layout(
        title=f'Candlestick Chart for {day}',
        xaxis_title='Date',
        yaxis_title=f'{day}',
        xaxis_rangeslider_visible=False,
        template='plotly_dark'
    )

    return fig

# Prepare data for both Nifty 50 and Nifty Bank
df_nifty50 = prepare_data('nifty50.csv')
df_nifty_bank = prepare_data('niftyBank.csv')

# Define the order of days
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

# Streamlit app layout
st.title('Candlestick Charts for Nifty 50 and Nifty Bank')

# Select a dataset
selected_dataset = st.selectbox("Select Dataset", ['Nifty 50', 'Nifty Bank'])

# Depending on the selection, choose the appropriate dataframe
if selected_dataset == 'Nifty 50':
    df = df_nifty50
else:
    df = df_nifty_bank

# Display charts for each day
for day in days_order:
    st.subheader(f'{selected_dataset} - {day}')
    fig = create_candlestick_chart(df, day)
    st.plotly_chart(fig)
