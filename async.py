import asyncio

async def async_task():
    print("Task started...")
    await asyncio.sleep(3)  # Non-blocking wait
    print("Task completed!")

async def main():
    await asyncio.gather(async_task(), async_task())  # Run both tasks concurrently

asyncio.run(main())
