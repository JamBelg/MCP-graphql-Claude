"""Configuration settings for the MCP GraphQL server"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# GraphQL API configuration
GRAPHQL_ENDPOINT = os.getenv("GRAPHQL_ENDPOINT", "http://127.0.0.1:5001/graphql")

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")