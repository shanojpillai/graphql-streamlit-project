import streamlit as st
from graphql_client import run_query
import pandas as pd
import plotly.express as px
import sys
import os

# Add the parent directory to the path to import from pages
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pages.rest_comparison import display_rest_comparison

# Set page configuration
st.set_page_config(
    page_title="GraphQL vs REST Demo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
st.title("GraphQL vs REST API Demo")
st.markdown("""
This application demonstrates the advantages of GraphQL over traditional REST APIs
using a real-world dataset. Explore different queries and see the difference in performance
and flexibility.
""")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "GraphQL Explorer", "REST Comparison", "About"])

# GraphQL configuration
GRAPHQL_URL = "http://localhost:8000/graphql"

if page == "Home":
    st.header("Welcome to the GraphQL Demo")
    
    # Display dataset information
    st.subheader("Dataset Overview")
    
    # Sample query to get the first 5 items
    query = """
    query {
        items(limit: 5) {
            id
            name
            value
            category
        }
    }
    """
    
    with st.spinner("Loading data..."):
        try:
            result = run_query(query)
            if result and "items" in result:
                df = pd.DataFrame(result["items"])
                st.dataframe(df)
                
                # Simple visualization
                if not df.empty and "value" in df.columns and "category" in df.columns:
                    st.subheader("Sample Visualization")
                    fig = px.bar(df, x="name", y="value", color="category", title="Sample Data Visualization")
                    st.plotly_chart(fig)
            else:
                st.error("No data returned from the GraphQL API. Make sure the backend server is running.")
        except Exception as e:
            st.error(f"Error connecting to GraphQL API: {e}")
            st.info("Make sure the backend server is running on http://localhost:8000")

elif page == "GraphQL Explorer":
    st.header("GraphQL Query Explorer")
    
    # Simple GraphQL query builder
    st.subheader("Build Your Query")
    
    limit = st.slider("Limit", min_value=1, max_value=100, value=10)
    offset = st.slider("Offset", min_value=0, max_value=100, value=0)
    
    # Get all available categories
    categories = []
    try:
        # Query to get all items to extract categories
        all_items_query = """
        query {
            items(limit: 100) {
                category
            }
        }
        """
        result = run_query(all_items_query)
        if result and "items" in result:
            # Extract unique categories
            categories = list(set([item["category"] for item in result["items"] if "category" in item]))
    except Exception:
        # If there's an error, use default categories
        categories = ["A", "B", "C"]
    
    # Category filter
    category = st.selectbox("Filter by Category", options=["All"] + categories)
    category_filter = f'category: "{category}"' if category != "All" else ""
    
    # Field selection
    st.subheader("Select Fields")
    fields = ["id", "name", "value", "category"]
    selected_fields = []
    
    col1, col2 = st.columns(2)
    with col1:
        if st.checkbox("id", value=True):
            selected_fields.append("id")
        if st.checkbox("name", value=True):
            selected_fields.append("name")
    
    with col2:
        if st.checkbox("value", value=True):
            selected_fields.append("value")
        if st.checkbox("category", value=True):
            selected_fields.append("category")
    
    if not selected_fields:
        st.warning("Please select at least one field.")
        selected_fields = ["id"]  # Default to at least one field
    
    # Construct the query
    fields_str = "\n            ".join(selected_fields)
    query = f"""
    query {{
        items(
            limit: {limit}
            offset: {offset}
            {category_filter}
        ) {{
            {fields_str}
        }}
    }}
    """
    
    # Display the query
    st.subheader("Generated Query")
    st.code(query, language="graphql")
    
    # Execute the query
    if st.button("Run Query"):
        with st.spinner("Executing query..."):
            try:
                result = run_query(query)
                if result and "items" in result:
                    st.success(f"Query returned {len(result['items'])} items")
                    df = pd.DataFrame(result["items"])
                    st.dataframe(df)
                    
                    # Add visualization if certain fields are selected
                    if "value" in selected_fields and "name" in selected_fields:
                        st.subheader("Data Visualization")
                        
                        if "category" in selected_fields:
                            fig = px.bar(df, x="name", y="value", color="category", 
                                        title="Item Values by Category")
                        else:
                            fig = px.bar(df, x="name", y="value", 
                                        title="Item Values")
                            
                        st.plotly_chart(fig)
                else:
                    st.warning("No data returned from the query")
            except Exception as e:
                st.error(f"Error executing query: {e}")

elif page == "REST Comparison":
    # Call the function from the imported module
    display_rest_comparison()

elif page == "About":
    st.header("About This Project")
    
    st.markdown("""
    This project demonstrates the use of GraphQL with Python and Streamlit.
    
    **Technologies used:**
    - Backend: Python, Strawberry GraphQL, FastAPI
    - Frontend: Streamlit, Plotly
    - Data: Simple product dataset with categories
    
    **Key Features:**
    - GraphQL API with filtering and pagination
    - Interactive query builder
    - Comparison with equivalent REST API calls
    - Data visualizations
    
    **GitHub Repository:**
    [https://github.com/shanojpillai/graphql-streamlit-project](https://github.com/shanojpillai/graphql-streamlit-project)
    
    **Next Steps:**
    - Add a real-world dataset from Kaggle
    - Implement more complex GraphQL queries with nested data
    - Add mutations for data modification
    - Enhance visualizations and comparisons
    """)
    
    st.subheader("GraphQL vs REST API")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### REST API
        - Fixed endpoints for different resources
        - Returns predefined data structures
        - Often requires multiple requests
        - Versioning can be challenging
        - Widely adopted and understood
        """)
    
    with col2:
        st.markdown("""
        ### GraphQL API
        - Single endpoint for all resources
        - Client specifies exactly what data it needs
        - Can retrieve multiple resources in one request
        - Strong typing and self-documenting
        - Evolves without breaking clients
        """)