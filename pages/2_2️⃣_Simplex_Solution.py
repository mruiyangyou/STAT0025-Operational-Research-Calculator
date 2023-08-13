import streamlit as st 
from orCal.utils import input_preprocess
from orCal.Simplex import *


st.set_page_config(
    page_icon = '2️⃣',
    page_title='BigM Solution'
)

st.title('Simplex Method Calculator')

# input = SimplexInput(
#     objective = 'max',
#     num_of_products = 4,
#     cost_coef = [1,2,1,1],
#     resources_coef = [[2,1,3,4], [2,3,0,4], [3,1,1,0]],
#     resources = [8, 12, 18]
# )

input_container, output_container = st.container(), st.container()

with input_container:
    
    obj = st.text_input(label='Objective', placeholder="String(min'/'max')")
    
    num_of_pro = st.text_input(label='Number Of Products', placeholder='integer')

    cost_coefficient = st.text_input(label = 'Cost Coefficient', placeholder='Python one dimension list')

    resources_coefficient = st.text_input(label = 'Resources Coefficient', placeholder='Python two dimension list')

    resources_limit = st.text_input(label='Resources Limit', placeholder='Python one dimension list')


if num_of_pro and cost_coefficient and resources_coefficient and resources_limit and obj:
    input = None
    try:
        input = SimplexInput(
        num_of_products = int(num_of_pro),
        cost_coef = input_preprocess(cost_coefficient),
        resources_coef = input_preprocess(resources_coefficient),
        resources = input_preprocess(resources_limit),
        objective= str(obj)
        )
    except ValueError as e:
        with output_container:
            error_message = 'Error: ' + str(e) + '!' 
            st.markdown(f'<div style="color: red; font-weight: bold font-size: 60px;">{error_message}</div>', unsafe_allow_html=True)

        
    if input:
        output, df, buffer = Simplex_loop(input)
        with output_container:
            
            tab, dow = st.tabs(['Final Result DataFrame 📊', 'Download ⚒️'])
            with tab:
                st.dataframe(df)
                with st.expander('See result explaination'):
                    st.write(output)
                
            with dow:
                st.download_button(
                    label="Download data as Excel",
                    data=buffer,
                    file_name='result.xlsx',
                    mime='application/vnd.ms-excel',
                )
                
               