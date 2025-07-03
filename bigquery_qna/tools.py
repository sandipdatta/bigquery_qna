from google.cloud import bigquery

def execute_biquery_query(query: str) -> dict:
    """Executes a BigQuery query and returns the result."""
    try:
        client = bigquery.Client()
        query_job = client.query(query)
        results = query_job.result()
        return {"status": "success", "results": [dict(row) for row in results]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def list_bigquery_datasets(filter: str = "") -> dict:
    """Lists BigQuery datasets, optionally filtering by a string."""
    try:
        client = bigquery.Client()
        datasets = list(client.list_datasets())
        dataset_ids = [dataset.dataset_id for dataset in datasets]
        if filter:
            dataset_ids = [id for id in dataset_ids if filter in id]
        return {"status": "success", "datasets": dataset_ids}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def list_bigquery_tables(dataset_id: str) -> dict:
    """Lists tables in a BigQuery dataset."""
    try:
        client = bigquery.Client()
        tables = list(client.list_tables(dataset_id))
        table_ids = [table.table_id for table in tables]
        return {"status": "success", "tables": table_ids}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_bigquery_table_schema(table_id: str) -> dict:
    """Gets the schema and metadata of a BigQuery table, including partitioning and clustering info."""
    try:
        client = bigquery.Client()
        table = client.get_table(table_id)
        schema = [{"name": field.name, "type": field.field_type} for field in table.schema]
        
        partitioning_info = None
        if table.time_partitioning:
            partitioning_info = {
                "field": table.time_partitioning.field,
                "type": table.time_partitioning.type_,
            }
            
        clustering_info = None
        if table.clustering_fields:
            clustering_info = table.clustering_fields

        return {
            "status": "success",
            "schema": schema,
            "partitioning": partitioning_info,
            "clustering": clustering_info,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}