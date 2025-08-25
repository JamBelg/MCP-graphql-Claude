from mcp.server.fastmcp import FastMCP
import requests
import sys
from typing import Optional, Dict, Any, List
import json
from datetime import datetime

# GraphQL API URL
GRAPHQL_ENDPOINT = "http://127.0.0.1:5001/graphql"

# Create server
mcp = FastMCP("sales-graphql-mcp")

# ----------------------------
# Helper Functions
# ----------------------------
def make_graphql_request(query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Make a GraphQL request and handle errors consistently."""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    
    try:
        response = requests.post(
            GRAPHQL_ENDPOINT, 
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        # Check for GraphQL errors
        if "errors" in result:
            return {"error": f"GraphQL errors: {result['errors']}", "success": False}
        
        return result
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}", "success": False}
    except json.JSONDecodeError as e:
        return {"error": f"JSON decode error: {str(e)}", "raw": response.text if 'response' in locals() else None, "success": False}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}", "success": False}

# ----------------------------
# Core GraphQL Tools
# ----------------------------
@mcp.tool()
def graphql_query(query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Run a raw GraphQL query against the sales API.
    
    Args:
        query: The GraphQL query string
        variables: Optional variables for the query
    
    Returns:
        Dict containing the GraphQL response or error information
    """
    return make_graphql_request(query, variables)

@mcp.tool()
def test_connection() -> Dict[str, Any]:
    """
    Test the connection to the GraphQL endpoint.
    
    Returns:
        Dict containing connection status
    """
    query = """
    query TestQuery {
        __typename
    }
    """
    
    response = make_graphql_request(query)
    
    if "error" in response:
        return {"connected": False, "error": response["error"]}
    else:
        return {"connected": True, "endpoint": GRAPHQL_ENDPOINT, "response": response}

# ----------------------------
# Order Query Tools
# ----------------------------
@mcp.tool()
def get_all_orders() -> Dict[str, Any]:
    """
    Retrieve all orders with complete details.
    
    Returns:
        Dict containing all orders or error information
    """
    query = """
    query GetAllOrders {
        orders {
            orderDetails {
                orderId
                orderDate
                totalPrice
            }
            customerDetails {
                customerId
                customerName
            }
            employeeDetails {
                employeeName
            }
            shipmentDetails {
                shipName
                shipAddress
                shipCity
                shipRegion
                shipPostalCode
                shipCountry
                shipperId
                shipperName
                shippedDate
            }
            products {
                product
                quantity
                unitPrice
                total
            }
        }
    }
    """
    
    response = make_graphql_request(query)
    
    if "error" in response:
        return response
    
    if "data" not in response or "orders" not in response.get("data", {}):
        return {"error": "Unexpected response structure", "response": response, "success": False}
    
    orders = response["data"]["orders"]
    return {
        "orders": orders,
        "total_count": len(orders),
        "success": True
    }

@mcp.tool()
def get_order_by_id(order_id: str) -> Dict[str, Any]:
    """
    Retrieve a specific order by its ID.
    
    Args:
        order_id: The order ID to search for
    
    Returns:
        Dict containing the order details or error information
    """
    query = """
    query GetOrderById($orderId: String!) {
        orderById(orderId: $orderId) {
            orderDetails {
                orderId
                orderDate
                totalPrice
            }
            customerDetails {
                customerId
                customerName
            }
            employeeDetails {
                employeeName
            }
            shipmentDetails {
                shipName
                shipAddress
                shipCity
                shipRegion
                shipPostalCode
                shipCountry
                shipperId
                shipperName
                shippedDate
            }
            products {
                product
                quantity
                unitPrice
                total
            }
        }
    }
    """
    
    response = make_graphql_request(query, {"orderId": order_id})
    
    if "error" in response:
        return response
    
    if "data" not in response:
        return {"error": "Unexpected response structure", "response": response, "success": False}
    
    order = response["data"].get("orderById")
    if order is None:
        return {"error": f"Order with ID '{order_id}' not found", "success": False}
    
    return {"order": order, "success": True}

# ----------------------------
# Customer Query Tools  
# ----------------------------
@mcp.tool()
def get_orders_by_customer_name(customer_name: str) -> Dict[str, Any]:
    """
    Retrieve all orders for a specific customer by name.
    
    Args:
        customer_name: The customer name to search for
    
    Returns:
        Dict containing the customer's orders or error information
    """
    query = """
    query GetOrdersByCustomerName($customerName: String!) {
        ordersByCustomerName(customerName: $customerName) {
            orderDetails {
                orderId
                orderDate
                totalPrice
            }
            customerDetails {
                customerId
                customerName
            }
            employeeDetails {
                employeeName
            }
            shipmentDetails {
                shipName
                shipAddress
                shipCity
                shipRegion
                shipPostalCode
                shipCountry
                shipperId
                shipperName
                shippedDate
            }
            products {
                product
                quantity
                unitPrice
                total
            }
        }
    }
    """
    
    response = make_graphql_request(query, {"customerName": customer_name})
    
    if "error" in response:
        return response
    
    if "data" not in response or "ordersByCustomerName" not in response.get("data", {}):
        return {"error": "Unexpected response structure", "response": response, "success": False}
    
    orders = response["data"]["ordersByCustomerName"]
    return {
        "orders": orders,
        "customer_name": customer_name,
        "total_count": len(orders),
        "success": True
    }

@mcp.tool()
def get_orders_by_customer_id(customer_id: str) -> Dict[str, Any]:
    """
    Retrieve all orders for a specific customer by ID.
    
    Args:
        customer_id: The customer ID to search for
    
    Returns:
        Dict containing the customer's orders or error information
    """
    query = """
    query GetOrdersByCustomerId($customerId: String!) {
        ordersByCustomerId(customerId: $customerId) {
            orderDetails {
                orderId
                orderDate
                totalPrice
            }
            customerDetails {
                customerId
                customerName
            }
            employeeDetails {
                employeeName
            }
            shipmentDetails {
                shipName
                shipAddress
                shipCity
                shipRegion
                shipPostalCode
                shipCountry
                shipperId
                shipperName
                shippedDate
            }
            products {
                product
                quantity
                unitPrice
                total
            }
        }
    }
    """
    
    response = make_graphql_request(query, {"customerId": customer_id})
    
    if "error" in response:
        return response
    
    if "data" not in response or "ordersByCustomerId" not in response.get("data", {}):
        return {"error": "Unexpected response structure", "response": response, "success": False}
    
    orders = response["data"]["ordersByCustomerId"]
    return {
        "orders": orders,
        "customer_id": customer_id,
        "total_count": len(orders),
        "success": True
    }

@mcp.tool()
def get_total_spent_by_customer(customer_name: str) -> Dict[str, Any]:
    """
    Get the total amount spent by a customer.
    
    Args:
        customer_name: The customer name to calculate total spending for
    
    Returns:
        Dict containing the total spent or error information
    """
    query = """
    query GetTotalSpentByCustomer($customerName: String!) {
        totalSpentByCustomer(customerName: $customerName)
    }
    """
    
    response = make_graphql_request(query, {"customerName": customer_name})
    
    if "error" in response:
        return response
    
    if "data" not in response or "totalSpentByCustomer" not in response.get("data", {}):
        return {"error": "Unexpected response structure", "response": response, "success": False}
    
    total_spent = response["data"]["totalSpentByCustomer"]
    return {
        "customer_name": customer_name,
        "total_spent": total_spent,
        "success": True
    }

# ----------------------------
# Date Filtering Tools
# ----------------------------
@mcp.tool()
def orders_after_date(date: str) -> Dict[str, Any]:
    """
    Retrieve all orders after a given date (YYYY-MM-DD).
    Note: This filters locally since the GraphQL schema doesn't have date filters.
    
    Args:
        date: Date string in YYYY-MM-DD format
    
    Returns:
        Dict containing filtered orders or error information
    """
    # Validate date format
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Please use YYYY-MM-DD", "success": False}
    
    # Get all orders first
    all_orders_response = get_all_orders()
    
    if "error" in all_orders_response:
        return all_orders_response
    
    orders = all_orders_response["orders"]
    
    try:
        filtered = []
        for order in orders:
            if "orderDetails" in order and "orderDate" in order["orderDetails"]:
                order_date = order["orderDetails"]["orderDate"]
                # Compare dates as strings (assuming YYYY-MM-DD format)
                if order_date > date:
                    filtered.append(order)
        
        return {
            "orders": filtered,
            "filter_date": date,
            "total_count": len(filtered),
            "success": True
        }
    
    except Exception as e:
        return {"error": f"Error filtering orders: {str(e)}", "success": False}

@mcp.tool()
def orders_between_dates(start_date: str, end_date: str) -> Dict[str, Any]:
    """
    Retrieve all orders between two dates (inclusive).
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        Dict containing filtered orders or error information
    """
    # Validate date formats
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Please use YYYY-MM-DD", "success": False}
    
    if start_date > end_date:
        return {"error": "Start date must be before or equal to end date", "success": False}
    
    # Get all orders first
    all_orders_response = get_all_orders()
    
    if "error" in all_orders_response:
        return all_orders_response
    
    orders = all_orders_response["orders"]
    
    try:
        filtered = []
        for order in orders:
            if "orderDetails" in order and "orderDate" in order["orderDetails"]:
                order_date = order["orderDetails"]["orderDate"]
                # Compare dates as strings (assuming YYYY-MM-DD format)
                if start_date <= order_date <= end_date:
                    filtered.append(order)
        
        return {
            "orders": filtered,
            "start_date": start_date,
            "end_date": end_date,
            "total_count": len(filtered),
            "success": True
        }
    
    except Exception as e:
        return {"error": f"Error filtering orders: {str(e)}", "success": False}

# ----------------------------
# Analysis Tools
# ----------------------------
@mcp.tool()
def get_order_summary() -> Dict[str, Any]:
    """
    Get a summary of all orders including counts and totals.
    
    Returns:
        Dict containing order summary statistics
    """
    all_orders_response = get_all_orders()
    
    if "error" in all_orders_response:
        return all_orders_response
    
    orders = all_orders_response["orders"]
    
    try:
        total_orders = len(orders)
        total_revenue = sum(order["orderDetails"]["totalPrice"] for order in orders)
        
        # Get unique customers
        customers = set()
        for order in orders:
            customers.add(order["customerDetails"]["customerName"])
        
        # Get product counts
        product_quantities = {}
        for order in orders:
            for product in order.get("products", []):
                product_name = product["product"]
                quantity = product["quantity"]
                product_quantities[product_name] = product_quantities.get(product_name, 0) + quantity
        
        return {
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "unique_customers": len(customers),
            "average_order_value": total_revenue / total_orders if total_orders > 0 else 0,
            "top_products": sorted(product_quantities.items(), key=lambda x: x[1], reverse=True)[:10],
            "success": True
        }
    
    except Exception as e:
        return {"error": f"Error calculating summary: {str(e)}", "success": False}

