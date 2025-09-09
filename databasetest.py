from pymongo import MongoClient
import pprint # For nicely printing documents

# --- 1. Connection ---
try:
    # Connect to the local MongoDB instance running in Docker
    client = MongoClient('mongodb://localhost:27017/')
    
    # Test the connection
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB!")

except Exception as e:
    print(f"❌ Could not connect to MongoDB: {e}")
    exit()

# --- 2. Setup Database and Collection ---
db = client['mydatabase']
collection = db['users']

# Clean up previous runs
collection.delete_many({})
print("\n🧹 Cleaned up 'users' collection.")

# --- 3. CREATE ---
print("\n--- CREATE ---")
users_to_insert = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "Paris"},
    {"name": "Charlie", "age": 35, "city": "London"}
]
result = collection.insert_many(users_to_insert)
print(f"Inserted {len(result.inserted_ids)} users.")

# --- 4. READ ---
print("\n--- READ ---")
print("All users in the collection:")
for user in collection.find():
    pprint.pprint(user)

# --- 5. UPDATE ---
print("\n--- UPDATE ---")
update_filter = {"name": "Alice"}
update_operation = {"$set": {"city": "Boston"}}
result = collection.update_one(update_filter, update_operation)
print(f"Modified {result.modified_count} document.")
print("Alice's updated document:")
pprint.pprint(collection.find_one({"name": "Alice"}))

# --- 6. DELETE ---
print("\n--- DELETE ---")
delete_filter = {"name": "Bob"}
result = collection.delete_one(delete_filter)
print(f"Deleted {result.deleted_count} document.")
print("\nFinal list of users:")
for user in collection.find():
    pprint.pprint(user)

# --- 7. Close Connection ---
client.close()
print("\nConnection closed.")