import asyncio

def main():
    """Entry point for tau command"""
    # Import here to avoid circular import
    import client.main as client_main
    asyncio.run(client_main.main())