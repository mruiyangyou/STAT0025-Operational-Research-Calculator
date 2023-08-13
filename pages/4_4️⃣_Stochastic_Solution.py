import streamlit as st 
from orCal.Stocal import MarkovDp
from orCal.utils import input_preprocess
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_icon = '4️⃣',
    page_title='Stochastic Solution'
)

st.title('Markov Dynamic Programming ')

input_container, output_container = st.container(), st.container()

with input_container:
    reward_matrix = st.text_input(label='Reward Matrix', placeholder='Python three dimension list')
    
    terminal_reward = st.text_input(label = 'Terminal reward', placeholder= 'Python one dimension list')
    
    transition_matrix = st.text_input(label = 'Transition matrix', placeholder='Python three dimension list')
    
    num_of_stage = st.text_input(label = 'Number of stages', placeholder='integer')
    
    discount = st.text_input(label = 'Discount factor', placeholder='float(0,1]')
    
if reward_matrix and terminal_reward and transition_matrix and num_of_stage and discount:
    dp = MarkovDp(reward_matrix=input_preprocess(reward_matrix),
                  terminal_reward=input_preprocess(terminal_reward),
                  action_tm=input_preprocess(transition_matrix))
    
    df = dp.get_reward_df(int(num_of_stage),float(discount))
    
    with output_container:
        tab, dow = st.tabs(['Result DataFrame 📊', 'Download ⚒️'])
        with tab:
            st.dataframe(df)
        with dow:
            @st.cache_data
            def convert_df(df):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return df.to_csv().encode('utf-8')
                        
            csv = convert_df(df)

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='result.csv',
                mime='text/csv',
            )
            
            
    