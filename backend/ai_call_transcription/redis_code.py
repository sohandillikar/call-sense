# redis_vector_api_key.py
import redis
import array

# -------- CONFIG --------
REDIS_HOST = "redis-12066.c16.us-east-1-2.ec2.redns.redis-cloud.com"
REDIS_PORT = 12066
REDIS_API_KEY = ""
INDEX_NAME = "doc_idx"
VECTOR_DIM = 4  # size of your vectors
VECTOR_FIELD = "vector"
KNN = 2  # number of nearest neighbors to retrieve

# -------- CONNECT USING API KEY --------
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    username="default",         # keep default for ACL
    password=REDIS_API_KEY,    # API key used as password
    decode_responses=False      # False because vectors are binary
)

# Test connection
try:
    print("Connected:", r.ping())
except redis.AuthenticationError as e:
    print("Authentication failed:", e)
    exit(1)

# -------- CREATE INDEX (raw FT.CREATE) --------
try:
    r.execute_command(
        "FT.CREATE", INDEX_NAME,
        "ON", "HASH",
        "PREFIX", "1", "doc:",
        "SCHEMA",
        "content", "TEXT",
        VECTOR_FIELD, "VECTOR", "FLAT", "6",
        "TYPE", "FLOAT32",
        "DIM", VECTOR_DIM,
        "DISTANCE_METRIC", "COSINE"
    )
    print("Index created!")
except redis.ResponseError as e:
    if "Index already exists" in str(e):
        print("Index already exists")
    else:
        raise e

# -------- ADD DOCUMENTS --------
def add_document(doc_id, content, vector):
    vector_bytes = bytes(array.array('f', vector))  # FLOAT32 bytes
    r.hset(f"doc:{doc_id}", mapping={
        "content": content.encode("utf-8"),
        VECTOR_FIELD: vector_bytes
    })

# Example documents

# -------- QUERY SIMILAR VECTORS (raw FT.SEARCH) --------
query_vector = [0.1, 0.2, 0.3, 0.4]
query_vector_bytes = bytes(array.array('f', query_vector))

knn_query = f"*=>[KNN {KNN} @{VECTOR_FIELD} $vec AS score]"

results = r.execute_command(
    "FT.SEARCH", INDEX_NAME,
    knn_query,
    "PARAMS", "2", "vec", query_vector_bytes,
    "RETURN", "2", "content", VECTOR_FIELD
)

# -------- PRINT RESULTS --------
total = results[0]
print(f"\nTop {KNN} matches (total indexed: {total}):")
for i in range(1, len(results), 2):
    key = results[i].decode("utf-8")
    fields = results[i + 1]
    content = fields[b'content'].decode("utf-8")
    print(f"ID: {key}, Content: {content}")
