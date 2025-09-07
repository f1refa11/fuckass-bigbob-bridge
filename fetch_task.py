import asyncio
import utils.sferum


async def fetch_task():
	while True:
		await utils.sferum.get_last_messages()
		
		# Wait for 10 seconds before the next iteration
		await asyncio.sleep(10)