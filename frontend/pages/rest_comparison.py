import streamlit as st
import pandas as pd
import time
import requests
import json
from graphql_client import run_query, GRAPHQL_URL

def display_rest_comparison():
    """
    Display a comparison between GraphQL and REST API approaches
    """
    st.title("GraphQL vs REST Comparison")
    
    st.markdown("""
    ### The Problem with REST APIs
    
    REST APIs are great for many use cases, but they have some limitations:
    
    1. **Over-fetching**: REST endpoints return fixed data structures, often including more data than needed
    2. **Under-fetching**: Multiple requests are needed to get related data
    3. **Multiple round trips**: Client needs to make multiple API calls
    4. **Versioning challenges**: API changes can break clients
    
    ### How GraphQL Solves These Problems
    
    GraphQL provides a more flexible approach:
    
    1. **Request only what you need**: Clients specify exactly what data they want
    2. **Single request**: Get multiple resources in a single query
    3. **Strong typing**: Schema defines available data and operations
    4. **Introspection**: API is self-documenting
    
    Let's see this in action with a performance comparison:
    """)
    
    # Demo setup
    st.subheader("Live Comparison Demo")
    
    # Define example scenarios
    scenarios = [
        {
            "name": "Basic Data Retrieval",
            "description": "Get a list of 10 items with basic information",
            "graphql_query": """
                query {
                    items(limit: 10) {
                        id
                        name
                        value
                    }
                }
            """,
            "rest_endpoints": ["/api/items?limit=10"]
        },
        {
            "name": "Filtered Data with Specific Fields",
            "description": "Get only items in category 'A' with specific fields",
            "graphql_query": """
                query {
                    items(limit: 10, category: "A") {
                        id
                        name
                        value
                    }
                }
            """,
            "rest_endpoints": ["/api/items?limit=10&category=A"]
        },
        {
            "name": "Related Data Retrieval",
            "description": "Get items and related details in a single request",
            "graphql_query": """
                query {
                    items(limit: 5) {
                        id
                        name
                        category
                        value
                    }
                }
            """,
            "rest_endpoints": [
                "/api/items?limit=5", 
                "/api/items/1/details",
                "/api/items/2/details",
                "/api/items/3/details",
                "/api/items/4/details",
                "/api/items/5/details"
            ]
        }
    ]
    
    # Select scenario
    selected_scenario = st.selectbox(
        "Select a comparison scenario:", 
        options=[s["name"] for s in scenarios],
        index=0
    )
    
    # Get the selected scenario details
    scenario = next(s for s in scenarios if s["name"] == selected_scenario)
    
    # Display scenario details
    st.markdown(f"**{scenario['description']}**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### GraphQL Approach")
        st.code(scenario["graphql_query"], language="graphql")
        
        # Execute GraphQL query with timing
        if st.button("Run GraphQL Query"):
            with st.spinner("Executing GraphQL query..."):
                start_time = time.time()
                
                try:
                    result = run_query(scenario["graphql_query"])
                    end_time = time.time()
                    execution_time = (end_time - start_time) * 1000  # in ms
                    
                    st.success(f"Query executed in {execution_time:.2f} ms")
                    st.json(result)
                    
                    # Store metrics for comparison
                    st.session_state.graphql_time = execution_time
                    st.session_state.graphql_requests = 1
                    st.session_state.graphql_data_size = len(json.dumps(result))
                except Exception as e:
                    st.error(f"Error executing GraphQL query: {e}")
    
    with col2:
        st.markdown("### REST Approach")
        for endpoint in scenario["rest_endpoints"]:
            st.code(endpoint, language="text")
        
        # Simulate REST API calls with timing
        if st.button("Simulate REST API Calls"):
            with st.spinner("Simulating REST API calls..."):
                start_time = time.time()
                total_data_size = 0
                
                try:
                    # Simulate multiple REST API calls
                    results = []
                    base_url = "http://localhost:8000"  # would be the REST API base URL
                    
                    for endpoint in scenario["rest_endpoints"]:
                        # Just simulate the timing, don't actually make the request
                        # since we're demonstrating the concept
                        time.sleep(0.2)  # simulate network latency for each request
                        
                        # Create detailed dummy responses based on endpoint
                        if "/details" in endpoint:
                            item_id = endpoint.split("/")[-2]
                            dummy_response = {
                                "id": item_id,
                                "name": f"Item {item_id}",
                                "details": {
                                    "description": f"Detailed description for item {item_id}",
                                    "created_at": "2023-05-10T14:30:00Z",
                                    "updated_at": "2023-05-15T09:45:00Z",
                                    "extra_info": "Additional data that comes with every request"
                                },
                                "endpoint": endpoint
                            }
                        else:
                            # General listing endpoint
                            dummy_response = {
                                "data": [
                                    {"id": "1", "name": "Item 1", "value": 10.5, "category": "A", 
                                     "created_at": "2023-05-10T14:30:00Z", "extra_field1": "value1", "extra_field2": "value2"},
                                    {"id": "2", "name": "Item 2", "value": 20.0, "category": "B",
                                     "created_at": "2023-05-11T10:15:00Z", "extra_field1": "value3", "extra_field2": "value4"}
                                ],
                                "pagination": {
                                    "total": 10,
                                    "page": 1,
                                    "limit": 10
                                },
                                "endpoint": endpoint
                            }
                        
                        results.append(dummy_response)
                        total_data_size += len(json.dumps(dummy_response))
                    
                    end_time = time.time()
                    execution_time = (end_time - start_time) * 1000  # in ms
                    
                    st.success(f"{len(scenario['rest_endpoints'])} API calls executed in {execution_time:.2f} ms")
                    
                    # Display the results (limit to first few to avoid clutter)
                    display_limit = min(3, len(results))
                    for i in range(display_limit):
                        st.markdown(f"**Response {i+1}/{len(results)}:**")
                        st.json(results[i])
                    
                    if len(results) > display_limit:
                        st.info(f"... and {len(results) - display_limit} more responses (not shown for brevity)")
                    
                    # Store metrics for comparison
                    st.session_state.rest_time = execution_time
                    st.session_state.rest_requests = len(scenario["rest_endpoints"])
                    st.session_state.rest_data_size = total_data_size
                except Exception as e:
                    st.error(f"Error simulating REST API calls: {e}")
    
    # Show comparison results if both methods have been executed
    if hasattr(st.session_state, 'graphql_time') and hasattr(st.session_state, 'rest_time'):
        st.subheader("Performance Comparison")
        
        comparison_data = {
            "Metric": ["Total Execution Time (ms)", "Number of API Requests", "Data Size (bytes)"],
            "GraphQL": [
                f"{st.session_state.graphql_time:.2f}",
                st.session_state.graphql_requests,
                st.session_state.graphql_data_size
            ],
            "REST": [
                f"{st.session_state.rest_time:.2f}",
                st.session_state.rest_requests,
                st.session_state.rest_data_size
            ]
        }
        
        df = pd.DataFrame(comparison_data)
        st.table(df)
        
        # Calculate and display efficiency gains
        time_improvement = (st.session_state.rest_time - st.session_state.graphql_time) / st.session_state.rest_time * 100
        request_reduction = ((st.session_state.rest_requests - st.session_state.graphql_requests) / 
                             st.session_state.rest_requests * 100)
        data_efficiency = ((st.session_state.rest_data_size - st.session_state.graphql_data_size) / 
                          st.session_state.rest_data_size * 100)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Time Saved", f"{time_improvement:.1f}%", "faster")
        with col2:
            st.metric("Requests Reduced", f"{request_reduction:.1f}%", "fewer")
        with col3:
            st.metric("Data Efficiency", f"{data_efficiency:.1f}%", "less data")
        
        st.markdown("""
        ### Key Takeaways
        
        - **GraphQL reduces network overhead** by minimizing the number of requests
        - **GraphQL is more efficient** by only fetching the required data
        - **GraphQL provides more flexibility** for clients to specify their data needs
        - **GraphQL evolves better over time** with backward-compatible schema changes
        
        ### Real-world Impact
        
        These efficiency gains can lead to:
        - Faster loading times for users
        - Reduced bandwidth usage (important for mobile users)
        - Lower server load and infrastructure costs
        - Better developer experience with a more flexible API
        """)

        # Example code comparison
        st.subheader("Code Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### GraphQL Client Code")
            st.code("""
// Single request fetches exactly what we need
const getData = async () => {
  const response = await client.query({
    query: gql`
      query {
        items(limit: 5) {
          id
          name
          value
          category
        }
      }
    `
  });
  
  return response.data.items;
};
            """, language="javascript")
            
        with col2:
            st.markdown("#### REST Client Code")
            st.code("""
// Multiple requests needed for the same data
const getData = async () => {
  // Get basic item data
  const itemsResponse = await fetch('/api/items?limit=5');
  const items = await itemsResponse.json();
  
  // Get details for each item with separate requests
  const itemDetails = await Promise.all(
    items.data.map(async (item) => {
      const detailsResponse = await fetch(
        `/api/items/${item.id}/details`
      );
      const details = await detailsResponse.json();
      return { ...item, ...details };
    })
  );
  
  return itemDetails;
};
            """, language="javascript")

if __name__ == "__main__":
    display_rest_comparison()