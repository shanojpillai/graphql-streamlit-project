import streamlit as st
from typing import Dict, List, Any, Optional

def query_builder(fields: List[str], 
                  filters: Optional[Dict[str, List[Any]]] = None,
                  pagination: bool = True):
    """
    Interactive GraphQL query builder component
    
    Args:
        fields: List of fields available for selection
        filters: Optional dictionary of filter options {field_name: [possible_values]}
        pagination: Whether to include pagination options
        
    Returns:
        Dict containing the selected query parameters
    """
    # Container for selected options
    query_options = {}
    
    # Select fields to include in the query
    st.subheader("Select Fields")
    selected_fields = []
    for field in fields:
        if st.checkbox(field, value=True):
            selected_fields.append(field)
    
    query_options["fields"] = selected_fields
    
    # Add filters if provided
    if filters:
        st.subheader("Filters")
        query_filters = {}
        
        for field, values in filters.items():
            if isinstance(values[0], str):
                # For string values, use a selectbox
                selected_value = st.selectbox(f"Filter by {field}", options=["Any"] + values)
                if selected_value != "Any":
                    query_filters[field] = selected_value
            elif isinstance(values[0], (int, float)):
                # For numeric values, use a slider
                min_val, max_val = min(values), max(values)
                selected_range = st.slider(f"Filter by {field}", min_val, max_val, (min_val, max_val))
                if selected_range != (min_val, max_val):
                    query_filters[field] = {"min": selected_range[0], "max": selected_range[1]}
        
        query_options["filters"] = query_filters
    
    # Add pagination options if enabled
    if pagination:
        st.subheader("Pagination")
        col1, col2 = st.columns(2)
        with col1:
            limit = st.number_input("Limit", min_value=1, max_value=100, value=10)
        with col2:
            offset = st.number_input("Offset", min_value=0, value=0)
        
        query_options["pagination"] = {"limit": limit, "offset": offset}
    
    # Generate the GraphQL query string
    query_string = generate_query_string(query_options)
    
    # Display the generated query
    st.subheader("Generated Query")
    st.code(query_string, language="graphql")
    
    return query_options, query_string

def generate_query_string(query_options: Dict[str, Any]) -> str:
    """
    Generate a GraphQL query string from the selected options
    
    Args:
        query_options: Dict containing the selected query parameters
        
    Returns:
        String containing the GraphQL query
    """
    fields = query_options.get("fields", [])
    filters = query_options.get("filters", {})
    pagination = query_options.get("pagination", {"limit": 10, "offset": 0})
    
    # Build query parameters
    params = []
    
    # Add pagination parameters
    if pagination:
        params.append(f"limit: {pagination['limit']}")
        params.append(f"offset: {pagination['offset']}")
    
    # Add filter parameters
    for field, value in filters.items():
        if isinstance(value, dict) and "min" in value and "max" in value:
            # Range filter
            params.append(f"{field}_min: {value['min']}")
            params.append(f"{field}_max: {value['max']}")
        elif isinstance(value, str):
            # String filter
            params.append(f'{field}: "{value}"')
        else:
            # Other filters
            params.append(f"{field}: {value}")
    
    # Construct the query string
    params_str = ", ".join(params)
    fields_str = "\n            ".join(fields)
    
    query = f"""
    query {{
        items({params_str}) {{
            {fields_str}
        }}
    }}
    """
    
    return query