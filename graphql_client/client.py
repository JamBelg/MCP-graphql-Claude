import json
from flask import Flask
from flask_graphql import GraphQLView
import graphene
from datetime import datetime

# Load JSON file
with open("sales/data.json", "r", encoding="utf-8") as f:
    orders_data = json.load(f)

# -------------------------------
# GraphQL Schema Definitions
# -------------------------------

class ProductType(graphene.ObjectType):
    product = graphene.String()
    quantity = graphene.Int()
    unit_price = graphene.Float()
    total = graphene.Float()

    def resolve_product(parent, info):
        return parent.get("Product")

    def resolve_quantity(parent, info):
        return parent.get("Quantity")

    def resolve_unit_price(parent, info):
        return parent.get("Unit Price")

    def resolve_total(parent, info):
        return parent.get("Total")


class OrderDetailsType(graphene.ObjectType):
    order_id = graphene.String()
    order_date = graphene.String()
    total_price = graphene.Float()  # Changed from sales_by_order to total_price for clarity
    
    def resolve_order_id(parent, info):
        return parent.get("Order ID")

    def resolve_order_date(parent, info):
        return parent.get("Order Date")

    def resolve_total_price(parent, info):
        return float(parent.get("Total Price", 0.0))


class ShipmentDetailsType(graphene.ObjectType):
    ship_name = graphene.String()
    ship_address = graphene.String()
    ship_city = graphene.String()
    ship_region = graphene.String()
    ship_postal_code = graphene.String()
    ship_country = graphene.String()
    shipper_id = graphene.String()
    shipper_name = graphene.String()
    shipped_date = graphene.String()

    def resolve_ship_name(parent, info): 
        return parent.get("Ship Name")
    
    def resolve_ship_address(parent, info): 
        return parent.get("Ship Address")
    
    def resolve_ship_city(parent, info): 
        return parent.get("Ship City")
    
    def resolve_ship_region(parent, info): 
        return parent.get("Ship Region")
    
    def resolve_ship_postal_code(parent, info): 
        return parent.get("Ship Postal Code")
    
    def resolve_ship_country(parent, info): 
        return parent.get("Ship Country")
    
    def resolve_shipper_id(parent, info): 
        return parent.get("Shipper ID")
    
    def resolve_shipper_name(parent, info): 
        return parent.get("Shipper Name")
    
    def resolve_shipped_date(parent, info): 
        return parent.get("Shipped Date")


class CustomerDetailsType(graphene.ObjectType):
    customer_id = graphene.String()
    customer_name = graphene.String()

    def resolve_customer_id(parent, info):
        return parent.get("Customer ID")

    def resolve_customer_name(parent, info):
        return parent.get("Customer Name")


class EmployeeDetailsType(graphene.ObjectType):
    employee_name = graphene.String()

    def resolve_employee_name(parent, info):
        return parent.get("Employee Name")


class OrderType(graphene.ObjectType):
    order_details = graphene.Field(OrderDetailsType)
    shipment_details = graphene.Field(ShipmentDetailsType)
    customer_details = graphene.Field(CustomerDetailsType)
    employee_details = graphene.Field(EmployeeDetailsType)
    products = graphene.List(ProductType)

    def resolve_order_details(parent, info):
        return parent.get("Order Details")

    def resolve_shipment_details(parent, info):
        return parent.get("Shipment Details")

    def resolve_customer_details(parent, info):
        return parent.get("Customer Details")

    def resolve_employee_details(parent, info):
        return parent.get("Employee Details")

    def resolve_products(parent, info):
        return parent.get("Products")


class CustomerSalesSummaryType(graphene.ObjectType):
    customer_name = graphene.String()
    customer_id = graphene.String()
    total_sales = graphene.Float()
    order_count = graphene.Int()


class ProductSalesSummaryType(graphene.ObjectType):
    product = graphene.String()
    unit_price = graphene.Float()
    total_sales = graphene.Float()
    total_quantity = graphene.Int()


# New types for better organization
class OrderSummaryStatsType(graphene.ObjectType):
    total_orders = graphene.Int()
    total_revenue = graphene.Float()
    unique_customers = graphene.Int()
    average_order_value = graphene.Float()
    date_range = graphene.String()


class TopProductType(graphene.ObjectType):
    product = graphene.String()
    total_quantity = graphene.Int()
    rank = graphene.Int()


# Enum for sorting options
class SortByEnum(graphene.Enum):
    TOTAL_SALES = "total_sales"
    TOTAL_QUANTITY = "total_quantity"
    ORDER_COUNT = "order_count"


# -------------------------------
# Root Query
# -------------------------------
class Query(graphene.ObjectType):
    
    # Basic order queries
    orders = graphene.List(OrderType)
    order_by_id = graphene.Field(OrderType, order_id=graphene.String(required=True))
    
    # Customer-based queries
    orders_by_customer_name = graphene.List(OrderType, customer_name=graphene.String(required=True))
    orders_by_customer_id = graphene.List(OrderType, customer_id=graphene.String(required=True))
    total_spent_by_customer = graphene.Float(customer_name=graphene.String(required=True))
    total_spent_by_customer_id = graphene.Float(customer_id=graphene.String(required=True))
    orders_count_by_customer_name = graphene.Int(customer_name=graphene.String(required=True))
    orders_count_by_customer_id = graphene.Int(customer_id=graphene.String(required=True))
    
    # Analytics and summaries
    customers_sales_summary = graphene.List(
        CustomerSalesSummaryType,
        sort_by=graphene.Argument(SortByEnum, default_value=SortByEnum.TOTAL_SALES),
        limit=graphene.Int()
    )
    
    products_sales_summary = graphene.List(
        ProductSalesSummaryType,
        sort_by=graphene.Argument(SortByEnum, default_value=SortByEnum.TOTAL_SALES),
        limit=graphene.Int()
    )
    
    # New comprehensive summary
    order_summary_stats = graphene.Field(OrderSummaryStatsType)
    
    # Date-based queries
    orders_after_date = graphene.List(OrderType, date=graphene.String(required=True))
    orders_between_dates = graphene.List(
        OrderType, 
        start_date=graphene.String(required=True),
        end_date=graphene.String(required=True)
    )
    
    # Top products query
    top_products_by_quantity = graphene.List(TopProductType, limit=graphene.Int(default_value=10))

    def resolve_orders(root, info):
        return orders_data

    def resolve_order_by_id(root, info, order_id):
        for order in orders_data:
            if order["Order Details"]["Order ID"] == order_id:
                return order
        return None

    def resolve_orders_by_customer_id(root, info, customer_id):
        return [
            order for order in orders_data
            if order["Customer Details"]["Customer ID"] == customer_id
        ]
    
    def resolve_orders_by_customer_name(root, info, customer_name):
        return [
            order for order in orders_data
            if order["Customer Details"]["Customer Name"] == customer_name
        ]
    
    def resolve_total_spent_by_customer(root, info, customer_name):
        total = 0.0
        for order in orders_data:
            if order["Customer Details"]["Customer Name"] == customer_name:
                total += float(order["Order Details"]["Total Price"])
        return round(total, 2)
    
    def resolve_total_spent_by_customer_id(root, info, customer_id):
        total = 0.0
        for order in orders_data:
            if order["Customer Details"]["Customer ID"] == customer_id:
                total += float(order["Order Details"]["Total Price"])
        return round(total, 2)
    
    def resolve_orders_count_by_customer_name(root, info, customer_name):
        return sum(1 for order in orders_data if order["Customer Details"]["Customer Name"] == customer_name)

    def resolve_orders_count_by_customer_id(root, info, customer_id):
        return sum(1 for order in orders_data if order["Customer Details"]["Customer ID"] == customer_id)

    def resolve_customers_sales_summary(root, info, sort_by=SortByEnum.TOTAL_SALES, limit=None):
        """Calculate comprehensive customer sales summary with improved sorting."""
        sales_summary = {}

        for order in orders_data:
            customer_name = order["Customer Details"]["Customer Name"]
            customer_id = order["Customer Details"]["Customer ID"]
            total_price = float(order["Order Details"]["Total Price"])
            
            if customer_id not in sales_summary:
                sales_summary[customer_id] = {
                    "customer_id": customer_id,
                    "customer_name": customer_name,
                    "total_sales": 0.0,
                    "order_count": 0
                }
            
            sales_summary[customer_id]["total_sales"] += total_price
            sales_summary[customer_id]["order_count"] += 1

        # Convert to list and sort
        customers_list = [
            {
                "customer_name": data["customer_name"],
                "customer_id": data["customer_id"],
                "total_sales": round(data["total_sales"], 2),
                "order_count": data["order_count"]
            }
            for data in sales_summary.values()
        ]

        # Sort based on the provided field
        if sort_by == SortByEnum.ORDER_COUNT:
            customers_list.sort(key=lambda x: x["order_count"], reverse=True)
        else:  # Default to total_sales
            customers_list.sort(key=lambda x: x["total_sales"], reverse=True)

        # Apply limit if provided
        if limit and limit > 0:
            customers_list = customers_list[:limit]

        return customers_list

    def resolve_products_sales_summary(root, info, sort_by=SortByEnum.TOTAL_SALES, limit=None):
        """Calculate comprehensive product sales summary with improved sorting."""
        product_summary = {}

        for order in orders_data:
            for product in order.get("Products", []):
                product_name = product["Product"]
                unit_price = float(product["Unit Price"])
                quantity = int(product["Quantity"])
                total_sales = float(product["Total"])

                if product_name not in product_summary:
                    product_summary[product_name] = {
                        "unit_price": unit_price,
                        "total_sales": 0.0,
                        "total_quantity": 0
                    }

                product_summary[product_name]["total_sales"] += total_sales
                product_summary[product_name]["total_quantity"] += quantity

        # Convert to list
        products_list = [
            {
                "product": name,
                "unit_price": data["unit_price"],
                "total_sales": round(data["total_sales"], 2),
                "total_quantity": data["total_quantity"]
            }
            for name, data in product_summary.items()
        ]

        # Sort based on the provided field
        if sort_by == SortByEnum.TOTAL_QUANTITY:
            products_list.sort(key=lambda x: x["total_quantity"], reverse=True)
        else:  # Default to total_sales
            products_list.sort(key=lambda x: x["total_sales"], reverse=True)

        # Apply limit if provided
        if limit and limit > 0:
            products_list = products_list[:limit]

        return products_list

    def resolve_order_summary_stats(root, info):
        """Comprehensive order statistics."""
        if not orders_data:
            return {
                "total_orders": 0,
                "total_revenue": 0.0,
                "unique_customers": 0,
                "average_order_value": 0.0,
                "date_range": "No data available"
            }

        total_orders = len(orders_data)
        total_revenue = sum(float(order["Order Details"]["Total Price"]) for order in orders_data)
        
        # Get unique customers
        unique_customers = len(set(
            order["Customer Details"]["Customer ID"] for order in orders_data
        ))
        
        # Calculate average order value
        average_order_value = total_revenue / total_orders if total_orders > 0 else 0.0

        # Get date range
        dates = [order["Order Details"]["Order Date"] for order in orders_data if order["Order Details"].get("Order Date")]
        date_range = f"{min(dates)} to {max(dates)}" if dates else "Unknown"

        return {
            "total_orders": total_orders,
            "total_revenue": round(total_revenue, 2),
            "unique_customers": unique_customers,
            "average_order_value": round(average_order_value, 2),
            "date_range": date_range
        }

    def resolve_orders_after_date(root, info, date):
        """Get orders after a specific date."""
        try:
            # Validate date format
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return []

        return [
            order for order in orders_data
            if order["Order Details"].get("Order Date", "") > date
        ]

    def resolve_orders_between_dates(root, info, start_date, end_date):
        """Get orders between two dates (inclusive)."""
        try:
            # Validate date formats
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return []

        if start_date > end_date:
            return []

        return [
            order for order in orders_data
            if start_date <= order["Order Details"].get("Order Date", "") <= end_date
        ]

    def resolve_top_products_by_quantity(root, info, limit=10):
        """Get top products by total quantity sold."""
        product_quantities = {}

        for order in orders_data:
            for product in order.get("Products", []):
                product_name = product["Product"]
                quantity = int(product["Quantity"])
                product_quantities[product_name] = product_quantities.get(product_name, 0) + quantity

        # Sort and rank
        sorted_products = sorted(
            product_quantities.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:limit]

        return [
            {
                "product": product_name,
                "total_quantity": quantity,
                "rank": index + 1
            }
            for index, (product_name, quantity) in enumerate(sorted_products)
        ]


schema = graphene.Schema(query=Query)

# -------------------------------
# Flask App
# -------------------------------
app = Flask(__name__)
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

if __name__ == "__main__":
    app.run(port=5001, debug=True)