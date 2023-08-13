import streamlit as st 
from orCal.BigM import * 
from orCal.utils import input_preprocess

st.set_page_config(
    page_icon = '3️⃣',
    page_title='BigM Solution'
)

st.title('BigM Method Calculator')


# input = BigMInput(
#     objective = 'max',
#     num_of_products = 2,
#     cost_coef = [-1, 5],
#     resources_coef = [[3,2], [0, 2], [1, 0]],
#     resources = [18, 12, 4],
#     constraint_char = [">=", "<=", "<="]
# )

input_container, output_container = st.container(), st.container()

with input_container:
    
    obj = st.text_input(label='Objective', placeholder="String(min'/'max')")
    
    num_of_pro = st.text_input(label='Number Of Products', placeholder='integer')

    cost_coefficient = st.text_input(label = 'Cost Coefficient', placeholder='Python one dimension list')

    resources_coefficient = st.text_input(label = 'Resources Coefficient', placeholder='Python two dimension list')

    resources_limit = st.text_input(label='Resources Limit', placeholder='Python one dimension list')
    
    constraint_char = st.text_input(label='Constraint Characters', placeholder='Python one dimension list')
    


if num_of_pro and cost_coefficient and resources_coefficient and resources_limit and obj and constraint_char:
    input = None
    try:
        input = BigMInput(
        num_of_products = int(num_of_pro),
        cost_coef = input_preprocess(cost_coefficient),
        resources_coef = input_preprocess(resources_coefficient),
        resources = input_preprocess(resources_limit),
        objective= str(obj),
        constraint_char=input_preprocess(constraint_char)
        )
    except ValueError as e:
        with output_container:
            error_message = 'Error: ' + str(e) + '!' 
            st.markdown(f'<div style="color: red; font-weight: bold font-size: 60px;">{error_message}</div>', unsafe_allow_html=True)

        
    if input:
        output, df, buffer = BigM_loop(input)
        with output_container:
            
            tab, dow = st.tabs(['Result DataFrame 📊', 'Download ⚒️'])
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