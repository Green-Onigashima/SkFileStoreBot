#(©)Rapid_bots



import motor.motor_asyncio
from config import DB_URI, DB_NAME


class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.user

    def new_user(self, id):
        return dict(
            _id=int(id),
            id=id,
            verify=None
        )

    async def add_user(self, b, m):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.new_user(u.id)
            await self.col.insert_one(user)            

    async def is_user_exist(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return bool(user)


    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'_id': int(user_id)})

    async def update_user_info(self, user_id, value: dict, tag="$set"):
        myquery = {"id": user_id}
        newvalues = {tag: value}
        await self.col.update_one(myquery, newvalues, upsert=True)

    async def get_userdata(self, user_id):
        user_data = await self.col.find_one({"id": user_id})
        return user_data
        
db = Database(DB_URI, DB_NAME)



