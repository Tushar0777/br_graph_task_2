from opensearchpy import OpenSearch


class OpenSearchVectorStore:

    def __init__(self, host="http://localhost:9200"):
        self.client = OpenSearch(host)

    def index_rule(self, rule_id, vector):

        body = {
            "vector": vector
        }

        self.client.index(
            index="rules",
            id=rule_id,
            body=body
        )

    def search_similar(self, vector, k=5):

        query = {
            "size": k,
            "query": {
                "knn": {
                    "vector": {
                        "vector": vector,
                        "k": k
                    }
                }
            }
        }

        res = self.client.search(index="rules", body=query)

        return [
            {
                "id": hit["_id"],
                "score": hit.get("_score", 0.0)
            }
            for hit in res["hits"]["hits"]
        ]