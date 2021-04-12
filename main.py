import os
from requests_aws4auth import AWS4Auth
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, RequestsHttpConnection
import curator


def printenv():
	print("AWS_ACCESS_KEY=" + os.getenv("AWS_ACCESS_KEY"))
	print("AWS_REGION=" + os.getenv("AWS_REGION"))
	print("CASSIA_ALIAS=" + os.getenv("CASSIA_ALIAS"))
	print("CASSIA_ALIAS_INDEX_NAME=" + os.getenv("CASSIA_ALIAS_INDEX_NAME"))
	print("ELASTIC_SEARCH_HOST=" + os.getenv("ELASTIC_SEARCH_HOST"))
	print("ELASTIC_SEARCH_INDEX=" + os.getenv("ELASTIC_SEARCH_INDEX"))
	print()

def handler():
	awsauth = AWS4Auth(os.getenv("AWS_ACCESS_KEY"), os.getenv("AWS_SECRET_KEY"), os.getenv("AWS_REGION"), 'es')
	es = Elasticsearch(

		hosts=[{'host': os.getenv("ELASTIC_SEARCH_HOST"), 'port': 443}],
		http_auth=awsauth,
		use_ssl=True,
		verify_certs=True,
		connection_class=RequestsHttpConnection
	)
	index_list = curator.IndexList(es)
	index_list.filter_by_age(source='creation_date', direction='older', unit='days', unit_count=7)

	print("Found %s indices to delete" % len(index_list.indices))
	if index_list.indices:
		curator.DeleteIndices(index_list).do_action()

	result = es.indices.update_aliases({
		"actions": [
			{"add": {"index": os.getenv("CASSIA_ALIAS_INDEX_NAME"), "alias": os.getenv("CASSIA_ALIAS")}},
		]
	})
	return result


if __name__ == '__main__':
	load_dotenv()  # take environment variables from .env.
	printenv()
	handler()
