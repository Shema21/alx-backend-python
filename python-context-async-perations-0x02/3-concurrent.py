import asyncio
import aiosqlite

async def async_fetch_users():
    """Fetch all users from the database asynchronously"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("All users fetched:")
            for row in results:
                print(row)
            return results

async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            print("\nUsers over 40 fetched:")
            for row in results:
                print(row)
            return results

async def fetch_concurrently():
    """Run both queries concurrently using asyncio.gather"""
    return await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    # Run the concurrent fetch
    all_users, older_users = asyncio.run(fetch_concurrently())
    print("\nConcurrent fetch completed!")
    print(f"Total users: {len(all_users)}")
    print(f"Users over 40: {len(older_users)}")