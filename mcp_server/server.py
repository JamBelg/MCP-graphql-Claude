"""
MCP Server setup for GraphQL tools
"""
import logging
import sys
from mcp_server.tools.graphql_tools import mcp

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/mcp_sales_server.log'), 
        logging.StreamHandler(sys.stderr)
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main entry point for the MCP server"""
    logger.info("Starting Sales GraphQL MCP Server")
    
    try:
        # Use stdio transport for MCP compatibility
        mcp.run(transport='stdio')
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error running server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()