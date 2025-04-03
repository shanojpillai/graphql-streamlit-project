import streamlit as st
from graphql_client import run_query
import pandas as pd
import plotly.express as px

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
    category = st.text_input("Filter by Category (optional)")
    
    # Construct the query
    query = """
    query {
        items(
            limit: %d
            offset: %d
            %s
        ) {
            id
            name
            value
            category
        }
    }
    """ % (limit, offset, f'category: "{category}"' if category else '')
    
    # Display the query
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
                else:
                    st.warning("No data returned from the query")
            except Exception as e:
                st.error(f"Error executing query: {e}")

elif page == "REST Comparison":
    st.header("GraphQL vs REST Comparison")
    
    st.markdown("""
    This page demonstrates how GraphQL solves some common issues with REST APIs:
    
    1. **Over-fetching** - REST APIs often return more data than needed
    2. **Under-fetching** - Multiple REST API calls needed to get related data
    3. **Flexibility** - REST APIs have fixed response structures
    
    Let's see this in action:
    """)
    
    # Comparison demo to be implemented
    st.info("This section will be implemented once we have a dataset selected.")

elif page == "About":
    st.header("About This Project")
    
    st.markdown("""
    This project demonstrates the use of GraphQL with Python and Streamlit.
    
    **Technologies used:**
    - Backend: Python, Strawberry GraphQL, FastAPI
    - Frontend: Streamlit, Plotly
    - Data: [Dataset description will go here]
    
    **Key Features:**
    - GraphQL API with filtering and pagination
    - Interactive query builder
    - Comparison with equivalent REST API calls
    - Data visualizations
    
    **GitHub Repository:**
    [https://github.com/shanojpillai/graphql-streamlit-project](https://github.com/shanojpillai/graphql-streamlit-project)
    """)