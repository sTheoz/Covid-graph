from elasticsearch import Elasticsearch
import time

def inject_es(df, data):
    # text-index = table
    es = Elasticsearch(
        ['http://odfe-node1:9200'],
        http_auth=("admin", "admin"),
        timeout=60,
    )
    es.cluster.health(wait_for_status='green', request_timeout=1)
    start_time = time.time()
    for single_data in data['data']:
        res = es.index(index="test-index", body=single_data)
    #es.indices.refresh(index="test-index")
    return (time.time() - start_time)