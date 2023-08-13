import streamlit as st 
from orCal.utils import input_preprocess
from orCal.GraphicSol import GraphicSol_Input, SolveGraphicSolution


st.set_page_config(
    page_icon = '1️⃣',
    page_title='Graphic Solution'
    
)

# data = GraphicSol_Input(
#         cost_coef = [3,8],
#         resources_coef = [[2,4],[6,2],[0,1]],
#         resources = [1600,1800,350],
#         product_name = ["x1","x2"],
#         resource_name = ["l1","l2","l3"],
#         num_of_products = 2
# )

st.title('Graphic Solution Calculator')
input_container, output_container = st.container(), st.container()

with input_container:
    
    num_of_pro = st.text_input(label='Number Of Products', placeholder='integer')

    cost_coefficient = st.text_input(label = 'Cost Coefficient', placeholder='Python one dimension list')

    resources_coefficient = st.text_input(label = 'Resources Coefficient', placeholder='Python two dimension list')

    resources_limit = st.text_input(label='Resources Limit', placeholder='Python one dimension list')

    product_name = st.text_input(label='Product Name', placeholder='Python one dimension list')

    resource_name = st.text_input(label='Resources Name', placeholder='Python one dimension list')

if num_of_pro and cost_coefficient and resources_coefficient and resources_limit and product_name and resource_name:
    input = None
    try:
        input = GraphicSol_Input(
        num_of_products = input_preprocess(num_of_pro),
        cost_coef = input_preprocess(cost_coefficient),
        resources_coef = input_preprocess(resources_coefficient),
        resources = input_preprocess(resources_limit),
        product_name = input_preprocess(product_name),
        resource_name = input_preprocess(resource_name)
        )
    except ValueError as e:
        with output_container:
            error_message = 'Error: ' + str(e) + '!' 
            st.markdown(f'<div style="color: red; font-weight: bold font-size: 60px;">{error_message}</div>', unsafe_allow_html=True)

        
    if input:
        solve = SolveGraphicSolution()
        x, value = solve.solve_lp(input)
        df = solve.to_frame(input, x, value)
        x_max, y_max, res, doc = solve.get_minmax(input)
        fig = solve.create_plot(
             input,x_max, y_max, res, doc, x, value
            )
        with output_container:
            tab1, tab2 = st.tabs(['Result DataFrame 📊', 'Graphic Solution 📝'])
            with tab1:
                st.header('Result DataFrame:')
                st.dataframe(df)
            with tab2:
                st.header('Graphic Solution')
                st.pyplot(fig)
                