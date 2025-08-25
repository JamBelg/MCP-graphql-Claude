# MCP GraphQL Sales Server

A Model Context Protocol (MCP) server that provides access to sales data through GraphQL queries. This server allows AI assistants like Claude to interact with a Northwind-style sales database through natural language queries.

## 🚀 Features

- **GraphQL API** with comprehensive sales data queries
- **MCP Server** compatible with Claude Desktop and other MCP clients
- **Rich Analytics** including customer summaries, product analytics, and order statistics
- **Date-based Filtering** for time-range queries
- **FastMCP** integration for easy tool development

## 📊 Available Data & Queries

### Core Entities
- **Orders** - Complete order information with details, shipping, and line items
- **Customers** - Customer information and purchase history
- **Products** - Product catalog with pricing and sales data
- **Employees** - Employee information linked to orders

### Query Capabilities
- Get all orders or specific orders by ID
- Filter orders by customer (name or ID)
- Calculate customer spending totals and order counts
- Generate sales summaries for customers and products
- Date-range filtering and analytics
- Top products by quantity or revenue

## 🛠 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Claude Desktop (for MCP integration)

### 1. Clone the Repository

```bash
git clone https://github.com/JamBelg/MCP-graphql-Claude.git
cd mcp-graphql-sales-server
```

### 2. Set up Python Environment

```bash
# Create virtual environment and install dependencies
uv venv
uv pip install -r requirements.txt
```

### 3. Prepare Data

Ensure you have your sales data file at `sales/data.json`. The data should follow the Northwind database structure with orders containing:

```json
{
  "Order Details": {
    "Order ID": "10248",
    "Order Date": "1996-07-04",
    "Total Price": "440.00"
  },
  "Customer Details": {
    "Customer ID": "VINET",
    "Customer Name": "Vins et alcools Chevalier"
  },
  "Products": [
    {
      "Product": "Queso Cabrales",
      "Quantity": 12,
      "Unit Price": 14.0,
      "Total": 168.0
    }
  ]
}
```

### 4. Environment Configuration

Create a `.env` file (optional):

```env
GRAPHQL_ENDPOINT=http://127.0.0.1:5001/graphql
LOG_LEVEL=INFO
```

## 🚦 Running the Application

### Option 1: Start Both Servers

**Terminal 1 - GraphQL Server:**
```bash
python graphql_client/client.py
```

**Terminal 2 - MCP Server:**
```bash
python main.py
```

### Option 2: Using uv

```bash
# GraphQL Server
uv run graphql_client/client.py

# MCP Server  
uv run main.py
```

## 🔌 Claude Desktop Integration

### 1. Locate Claude Desktop Config

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

### 2. Add MCP Server Configuration

```json
{
  "mcpServers": {
    "sales-graphql": {
      "command": "/path/to/.local/bin/uv",
      "args": [
        "--directory",
        "/full/path/to/mcp-graphql-sales-server",
        "run",
        "main.py"
      ]
    }
  }
}
```

**Important:** Replace `/full/path/to/mcp-graphql-sales-server` with the actual absolute path to your project directory.

### 3. Restart Claude Desktop

Completely quit and restart Claude Desktop to load the new configuration.

## 💬 Usage Examples

Once integrated with Claude Desktop, you can ask questions like:

```
"Can you get all orders from the sales database?"
"Show me orders for customer 'ALFKI'"
"What's the total spent by customer 'Antonio Moreno'?"
"Get me the top 10 customers by sales volume"
"Show me order summary statistics"
"Find all orders from July 1996"
"Which products sell the most by quantity?"
```

### 📊 Live Demo - Interactive Sales Report

Check out this **interactive visualization** showing the top 10 customers by sales and order count:
**[Top 10 Customers Sales Report](https://claude.ai/public/artifacts/ff106e0d-7f81-42ba-905c-ca048bde8798)**

This report demonstrates the kind of rich analytics and visualizations you can generate using this MCP server with Claude's data analysis capabilities.

## 🔍 GraphQL Playground

Access the GraphQL playground at: http://127.0.0.1:5001/graphql

### Example Queries

```graphql
# Get comprehensive order statistics
{
  orderSummaryStats {
    totalOrders
    totalRevenue
    uniqueCustomers
    averageOrderValue
    dateRange
  }
}

# Get customer sales summary
{
  customersSalesSummary(limit: 5, sortBy: TOTAL_SALES) {
    customerName
    totalSales
    orderCount
  }
}

# Get specific customer's orders
{
  ordersByCustomerName(customerName: "Alfreds Futterkiste") {
    orderDetails {
      orderId
      orderDate
      totalPrice
    }
    products {
      product
      quantity
      unitPrice
      total
    }
  }
}
```

## 📁 Project Structure

```
mcp-graphql-sales-server/
├── README.md
├── requirements.txt
├── .env.example
├── main.py                    # Entry point
├── mcp_server/
│   ├── __init__.py
│   ├── server.py             # MCP server setup
│   └── tools/
│       ├── __init__.py
│       └── graphql_tools.py  # MCP tools for GraphQL queries
├── graphql_client/
│   ├── __init__.py
│   ├── client.py            # GraphQL server & schema
│   └── queries.py           # Additional GraphQL utilities
├── config/
│   ├── __init__.py
│   └── settings.py          # Configuration management
├── sales/
│   └── data.json           # Sales data file
└── tests/
    └── test_tools.py
```

## 🛠 Available MCP Tools

The server provides these tools for AI interaction:

- `graphql_query` - Execute raw GraphQL queries
- `test_connection` - Test GraphQL endpoint connectivity
- `get_all_orders` - Retrieve all orders with complete details
- `get_order_by_id` - Get specific order by ID
- `get_orders_by_customer_name` - Get customer's orders by name
- `get_orders_by_customer_id` - Get customer's orders by ID
- `get_total_spent_by_customer` - Calculate customer total spending
- `orders_after_date` - Filter orders after specific date
- `orders_between_dates` - Filter orders within date range
- `get_order_summary` - Get comprehensive order statistics

## 🐛 Troubleshooting

### Common Issues

1. **400 Bad Request errors**: Ensure GraphQL server is running on port 5001
2. **MCP tools not showing**: Check Claude Desktop config path and restart the application
3. **Data file errors**: Verify `sales/data.json` exists and is properly formatted
4. **Permission errors**: Ensure all files are readable and paths are correct

### Debug Logs

Check logs at: `/tmp/mcp_sales_server.log`

### Testing GraphQL Directly

```bash
curl -X POST http://127.0.0.1:5001/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ orders { orderDetails { orderId } } }"}'
```

## 📄 Requirements

```txt
fastmcp>=0.9.0
requests>=2.31.0
python-dotenv>=1.0.0
flask>=2.3.0
flask-graphql>=2.0.1
graphene>=3.3.0
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp) for easy MCP server development
- Uses [Graphene](https://graphene-python.org/) for GraphQL schema generation
- Inspired by the Northwind database sample data structure

---

**Need help?** Open an issue on GitHub or check the troubleshooting section above.