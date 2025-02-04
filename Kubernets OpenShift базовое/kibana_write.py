from elasticsearch import Elasticsearch

es = Elasticsearch(
    ["http://localhost:9200"],
    basic_auth=("elastic", "your_password_here"),
)

if not es.ping():
    raise ValueError("Connection failed")

print("Connected to Elasticsearch!")

index_name = "test_index"
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)
    print(f"Index '{index_name}' created.")

def add_document(index, doc_id, data):
    try:
        response = es.index(index=index, id=doc_id, document=data)
        print(f"Document {doc_id} added: {response['result']}")
    except Exception as e:
        print(f"Error adding document {doc_id}: {e}")

documents = [
    {"name": "John Doe", "age": 30, "city": "New York"},
    {"name": "Jane Smith", "age": 25, "city": "San Francisco"},
    {"name": "Alice Johnson", "age": 28, "city": "Los Angeles"},
]

for i, doc in enumerate(documents, start=1):
    add_document(index_name, i, doc)

print("Data successfully sent to Elasticsearch!")

