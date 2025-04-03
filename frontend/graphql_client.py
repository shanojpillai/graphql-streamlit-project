import requests
import json
from typing import Dict, Any, Optional

# GraphQL API endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

def run_query(query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Execute a GraphQL query against the API
    
    Args:
        query: The GraphQL query string
        variables: Optional variables for the query
        
    Returns:
        Dict containing the query results
    
    Raises:
        Exception: If there's an error with the request or query
    """
    # Prepare the request payload
    payload = {
        "query": query
    }
    
    if variables:
        payload["variables"] = variables
    
    # Make the request to the GraphQL API
    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the response
        result = response.json()
        
        # Check for GraphQL errors
        if "errors" in result:
            error_message = result["errors"][0]["message"]
            raise Exception(f"GraphQL Error: {error_message}")
        
        # Return the data if available
        if "data" in result:
            return result["data"]
        else:
            return {}
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request Error: {e}")
    except json.JSONDecodeError:
        raise Exception("Invalid JSON response from the server")
    except Exception as e:
        raise Exception(f"Error: {e}")

def measure_query_performance(query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Execute a GraphQL query and measure its performance
    
    Args:
        query: The GraphQL query string
        variables: Optional variables for the query
        
    Returns:
        Dict containing the query results and performance metrics
    """
    import time
    
    start_time = time.time()
    result = run_query(query, variables)
    end_time = time.time()
    
    return {
        "data": result,
        "execution_time": round((end_time - start_time) * 1000, 2),  # in milliseconds
        "timestamp": time.time()
    }