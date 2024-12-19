import streamlit as st
import mysql.connector
import pandas as pd

# Function to connect to MySQL database
def connect_to_mysql():
    return mysql.connector.connect(
        host='localhost',  # Replace with your MySQL host
        user='root',  # Replace with your MySQL username
        password='T1e2s3t4',  # Replace with your MySQL password
        database='my_database'  # Replace with your MySQL database name
    )

# Initialize session state for tracking dropdowns
if 'myown_selected_question' not in st.session_state:
    st.session_state.myown_selected_question = None
if 'guvi_selected_question' not in st.session_state:
    st.session_state.guvi_selected_question = None

# Function to reset second dropdown
def reset_dropdown2():
    st.session_state.guvi_selected_question = None
    #selected_question = st.session_state.myown_selected_question #
   # print(st.session_state.myown_selected_question)

# Function to reset second dropdown
def reset_dropdown1():
    st.session_state.myown_selected_question = None
    #selected_question = st.session_state.guvi_selected_question #
   # print(st.session_state.guvi_selected_question)

# SQL queries for each question
def get_top_10_highest_revenue():
    query = """
    SELECT 
        od.product_id,
        SUM(od.sale_price * od.quantity) AS total_revenue
    FROM 
        order_details od
    GROUP BY 
        od.product_id
    ORDER BY 
        total_revenue DESC
    LIMIT 10;
    """
    return query

def get_top_5_cities_with_highest_profit_margins():
    query = """
    SELECT 
        o.city,
        SUM(od.profit) AS total_profit_margin
    FROM 
        order_details od
    JOIN 
        orders o ON od.order_id = o.order_id
    GROUP BY 
        o.city
    ORDER BY 
        total_profit_margin DESC
    LIMIT 5;
    """
    return query

def get_total_discount_per_category():
    query = """
    SELECT 
        od.category,
        SUM(od.discount) AS total_discount
    FROM 
        order_details od
    GROUP BY 
        od.category;
    """
    return query

def get_average_sale_price_per_category():
    query = """
    SELECT 
        od.category,
        AVG(od.sale_price) AS average_sale_price
    FROM 
        order_details od
    GROUP BY 
        od.category;
    """
    return query

def get_region_with_highest_average_sale_price():
    query = """
    SELECT 
        o.region,
        AVG(od.sale_price) AS average_sale_price
    FROM 
        order_details od
    JOIN 
        orders o ON od.order_id = o.order_id
    GROUP BY 
        o.region
    ORDER BY 
        average_sale_price DESC
    LIMIT 1;
    """
    return query

def get_total_profit_per_category():
    query = """
    SELECT 
        od.category,
        SUM(od.profit) AS total_profit
    FROM 
        order_details od
    GROUP BY 
        od.category;
    """
    return query

def get_top_3_segments_with_highest_quantity():
    query = """
     SELECT 
        o.segment,
        SUM(od.quantity) AS total_quantity
    FROM 
        order_details od
    JOIN 
        orders o ON od.order_id = o.order_id
    GROUP BY 
        o.segment
    ORDER BY 
        total_quantity DESC
    LIMIT 3;
    """
    return query

def get_average_discount_percentage_per_region():
    query = """
    SELECT 
        o.region,
        AVG(od.discount_percent) AS average_discount_percentage
    FROM 
        order_details od
    JOIN 
        orders o ON od.order_id = o.order_id
    GROUP BY 
        o.region;
    """
    return query

def get_product_category_with_highest_total_profit():
    query = """
    SELECT 
        od.category,
        SUM(od.profit) AS total_profit
    FROM 
        order_details od
    GROUP BY 
        od.category
    ORDER BY 
        total_profit DESC
    LIMIT 1;
    """
    return query

def get_total_revenue_per_year():
    query = """
    SELECT 
        YEAR(o.order_date) AS year,
        SUM(od.sale_price * od.quantity) AS total_revenue
    FROM 
        order_details od
    JOIN 
        orders o ON od.order_id = o.order_id
    GROUP BY 
        YEAR(o.order_date)
    ORDER BY 
        year;
    """
    return query

def get_all_orders_US():
    query = """
    SELECT 
	    o.order_id, o.order_date, o.ship_mode, o.segment, o.country, o.city, o.state, o.postal_code, o.region,
        od.product_id, od.category, od.sub_category, od.cost_price, od.list_price, od.quantity, od.discount_percent, od.discount, od.sale_price, od.profit
    FROM 
	    orders o
    JOIN 
	    order_details od ON o.order_id = od.order_id
    WHERE 
        o.country = 'United States';
    """
    return query

def get_total_price_furniture_category():
    query = """
    SELECT 
        od.product_id, SUM(od.sale_price) AS total_sales, o.order_id, o.order_date, o.ship_mode, o.segment, o.country, o.city, o.state, o.postal_code, o.region
    FROM 
        order_details od
    JOIN 
        orders o ON od.order_id = o.order_id
    WHERE 
        od.category = 'Furniture'
    GROUP BY 
        od.product_id, o.order_id;
    """
    return query

def get_total_profit_shipped_first_class():
    query = """
    SELECT 
        o.region, SUM(od.profit) AS total_profit
    FROM 
        orders o
    JOIN 
        order_details od ON o.order_id = od.order_id
    WHERE 
        o.ship_mode = 'First Class'
    GROUP BY 
        o.region;
    """
    return query

def get_highest_lowest_sale_with_order_date():
    query = """
    SELECT 
        o.order_id, o.order_date, 
        MAX(od.sale_price) AS highest_sale_price, 
        MIN(od.sale_price) AS lowest_sale_price
    FROM 
        orders o
    JOIN 
        order_details od ON o.order_id = od.order_id
    GROUP BY 
        o.order_id, o.order_date;
    """
    return query

def get_order_placed_from_California():
    query = """
    SELECT 
        o.city, COUNT(o.order_id) AS order_count
    FROM 
        orders o
    WHERE 
        o.state = 'California'
    GROUP BY 
        o.city;
    """
    return query

def get_total_cost_price_total_sale_price():
    query = """
    SELECT 
        o.order_id, SUM(od.cost_price * od.quantity) AS total_cost_price, SUM(od.sale_price * od.quantity) AS total_sale_price
    FROM 
        orders o
    JOIN 
        order_details od ON o.order_id = od.order_id
    GROUP BY 
        o.order_id;
    """
    return query

def get_orders_with_category():
    query = """
    SELECT 
        o.order_id, o.order_date, o.ship_mode, o.segment, o.country, o.city, o.state, o.postal_code, o.region,
        od.product_id, od.category, od.sub_category, od.cost_price, od.list_price, od.quantity, od.discount_percent, od.discount, od.sale_price, od.profit
    FROM 
        orders o
    JOIN 
        order_details od ON o.order_id = od.order_id
    WHERE 
        od.sale_price > 500;
    """
    return query

def get_highest_total_profit_per_region():
    query = """
    SELECT 
        o.region, SUM(od.profit) AS total_profit
    FROM 
        orders o
    JOIN 
        order_details od ON o.order_id = od.order_id
    GROUP BY 
        o.region
    ORDER BY 
        total_profit DESC
    LIMIT 1;
    """
    return query

def get_total_quantity_dicount_amount_in_office_supplies_category():
    query = """
    SELECT  
        od.product_id, SUM(od.quantity) AS total_quantity, SUM(od.discount) AS total_discount
    FROM 
        order_details od
    JOIN 
        orders o ON od.order_id = o.order_id
    WHERE 
        od.sub_category = 'Supplies'
    GROUP BY 
        od.product_id;
    """
    return query

def get_month_over_month_comparison_sales():
    query = """
    WITH cte AS (
    SELECT EXTRACT(YEAR FROM o.order_date) AS order_year,
           EXTRACT(MONTH FROM o.order_date) AS order_month,
           SUM(od.sale_price) AS sales
    FROM 
        order_details od
    JOIN 
        orders o on od.order_id = o.order_id    
    GROUP BY 
        EXTRACT(YEAR FROM o.order_date), EXTRACT(MONTH FROM o.order_date)
    )
    SELECT 
        order_month,
       SUM(CASE WHEN order_year = 2022 THEN sales ELSE 0 END) AS sales_2022,
       SUM(CASE WHEN order_year = 2023 THEN sales ELSE 0 END) AS sales_2023
    FROM 
        cte 
    GROUP BY 
        order_month
    ORDER BY 
        order_month;
    """
    return query

# Function to execute the query and fetch results
def fetch_data(query):
    conn = connect_to_mysql()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    
    # Convert the result into a DataFrame
    df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
    
    cursor.close()
    conn.close()

    return df

# Streamlit app
def main():
    st.title('Retail Order Data Analysis')
    
    # Define the list of questions
    own_questions = [
        "1.Find all the orders placed in 'United States' along with their corresponding details",
        "2.List the total sales (sale_price) for each product in the 'Furniture' category along with the order details.",
        "3.What is the total profit generated from orders shipped via 'First Class' for all regions?",
        "4.Show the highest and lowest sale price for each order, along with the order_date",
        "5.How many orders have been placed from each city in 'California'?",
        "6.Find the total cost price and total sale price for each order_id.",
        "7.List all orders with the category of products where the sale price is greater than $500",
        "8.Which regions have the highest total profit, and what is the profit amount?",
        "9.Get the total quantity and discount amount for each product in the 'Office Supplies' sub-category",
        "10.Find month-over-month growth comparison for 2022 and 2023 sales"
    ]

    guvi_questions = [
        "1.Find top 10 highest revenue generating products",
        "2.Find the top 5 cities with the highest profit margins",
        "3.Calculate the total discount given for each category",
        "4.Find the average sale price per product category",
        "5.Find the region with the highest average sale price",
        "6.Find the total profit per category",
        "7.Identify the top 3 segments with the highest quantity of orders",
        "8.Determine the average discount percentage given per region",
        "9.Find the product category with the highest total profit",
        "10.Calculate the total revenue generated per year"
    ]

    myown_selected_question = guvi_selected_question = ''
    col1, col2 = st.columns([1,1])
    with col1:
        # Dropdown for selecting a question
        myown_selected_question = st.selectbox("Select my own question", own_questions, key = 'myown_selected_question', on_change=reset_dropdown2)

    with col2:
        # Dropdown for selecting a question
        guvi_selected_question = st.selectbox("Select guvi provided question", guvi_questions, key = 'guvi_selected_question', on_change=reset_dropdown1)
    selected_question = ''
    if len(str(myown_selected_question)) > 5:
        selected_question = myown_selected_question
    if len(str(guvi_selected_question)) > 5:
        selected_question = guvi_selected_question

    # Execute the corresponding query based on the selected question
    if guvi_selected_question == "1.Find top 10 highest revenue generating products":
        query = get_top_10_highest_revenue()
    elif guvi_selected_question == "2.Find the top 5 cities with the highest profit margins":
        query = get_top_5_cities_with_highest_profit_margins()
    elif guvi_selected_question == "3.Calculate the total discount given for each category":
        query = get_total_discount_per_category()
    elif guvi_selected_question == "4.Find the average sale price per product category":
        query = get_average_sale_price_per_category()
    elif guvi_selected_question == "5.Find the region with the highest average sale price":
        query = get_region_with_highest_average_sale_price()
    elif guvi_selected_question == "6.Find the total profit per category":
        query = get_total_profit_per_category()
    elif guvi_selected_question == "7.Identify the top 3 segments with the highest quantity of orders":
        query = get_top_3_segments_with_highest_quantity()
    elif guvi_selected_question == "8.Determine the average discount percentage given per region":
        query = get_average_discount_percentage_per_region()
    elif guvi_selected_question == "9.Find the product category with the highest total profit":
        query = get_product_category_with_highest_total_profit()
    elif guvi_selected_question == "10.Calculate the total revenue generated per year":
        query = get_total_revenue_per_year()

     # Execute the corresponding query based on the selected question
    if myown_selected_question == "1.Find all the orders placed in 'United States' along with their corresponding details":
        query = get_all_orders_US()
    elif myown_selected_question == "2.List the total sales (sale_price) for each product in the 'Furniture' category along with the order details.":
        query = get_total_price_furniture_category()
    elif myown_selected_question == "3.What is the total profit generated from orders shipped via 'First Class' for all regions?":
        query = get_total_profit_shipped_first_class()
    elif myown_selected_question == "4.Show the highest and lowest sale price for each order, along with the order_date":
        query = get_highest_lowest_sale_with_order_date()
    elif myown_selected_question == "5.How many orders have been placed from each city in 'California'?":
        query = get_order_placed_from_California()
    elif myown_selected_question == "6.Find the total cost price and total sale price for each order_id.":
        query = get_total_cost_price_total_sale_price()
    elif myown_selected_question == "7.List all orders with the category of products where the sale price is greater than $500":
        query = get_orders_with_category()
    elif myown_selected_question == "8.Which regions have the highest total profit, and what is the profit amount?":
        query = get_highest_total_profit_per_region()
    elif myown_selected_question == "9.Get the total quantity and discount amount for each product in the 'Office Supplies' sub-category":
        query = get_total_quantity_dicount_amount_in_office_supplies_category()
    elif myown_selected_question == "10.Find month-over-month growth comparison for 2022 and 2023 sales":
        query = get_month_over_month_comparison_sales()

    
        #selected_question = guvi_selected_question
 
        #selected_question = myown_selected_question
   
    st.markdown("""
    <style>
        .center-button {
            display: flex;
            justify-content: center;
            margin-top: 50px;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        #st.markdown('<div class="center-button">', unsafe_allow_html=True)
        # Fetch the data and display it
        if st.button('Get Results'):
            if(len(str(selected_question)) > 5):                
                df = fetch_data(query)
                st.write(f"Results for: {selected_question}")
                st.markdown("""
                    <style>
                        .streamlit-expanderHeader {
                        border: 2px solid black;
                        border-radius: 10px;
                        }
                        .dataframe {
                        border: 2px solid black;
                        border-radius: 10px;
                        padding: 10px;
                        width: 1000px;
                        overflow-x: auto;
                        }
                    </style>
                    """, unsafe_allow_html=True)
                st.dataframe(df, width=1000)
        #st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
