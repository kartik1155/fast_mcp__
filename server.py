from fastmcp import FastMCP, Context
import asyncpg
import os
from dotenv import load_dotenv
load_dotenv()
mcp = FastMCP("PostgreSQL MCP Server")

@mcp.tool()
async def run_query(sql: str, ctx: Context) -> str:
    """Execute a SQL query and return results as string."""
    try:
        conn = await asyncpg.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        rows = await conn.fetch(sql)
        await conn.close()
        return "\n".join(str(dict(row)) for row in rows)
    except Exception as e:
        ctx.error(f"Query failed: {e}")
        return f"Error: {e}"
