from src import setup

indexName = input()
setup.delete_index(indexName)
setup.dumping_property()
setup.create_indexer()
