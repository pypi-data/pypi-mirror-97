"""This module creates the database."""
import boto3
from os import environ
from typing import List


class Database:
    """The database class."""

    def __init__(self, db_url: str = '', region_name: str = 'us-east-2'):
        """Initialize Database class.

        :param str db_url: URL endpoint for DynamoDB source
        :param str region_name: default AWS region
        """
        if db_url:
            self.ddb = boto3.resource('dynamodb', region_name=region_name,
                                      endpoint_url=db_url)
            self.ddb_client = boto3.client('dynamodb',
                                           region_name=region_name,
                                           endpoint_url=db_url)
        elif 'GENE_NORM_DB_URL' in environ.keys():
            db_url = environ['GENE_NORM_DB_URL']
            self.ddb = boto3.resource('dynamodb', region_name=region_name,
                                      endpoint_url=db_url)
            self.ddb_client = boto3.client('dynamodb',
                                           region_name=region_name,
                                           endpoint_url=db_url)
        else:
            self.ddb = boto3.resource('dynamodb', region_name=region_name)
            self.ddb_client = boto3.client('dynamodb',
                                           region_name=region_name)

        if db_url or 'GENE_NORM_DB_URL' in environ.keys():
            existing_tables = self.ddb_client.list_tables()['TableNames']
            self.create_genes_table(existing_tables)
            self.create_meta_data_table(existing_tables)

        self.genes = self.ddb.Table('gene_concepts')
        self.metadata = self.ddb.Table('gene_metadata')
        self.cached_sources = {}

    def create_genes_table(self, existing_tables: List[str]):
        """Create Genes table if non-existent.

        :param List[str] existing_tables: table names already in DB
        """
        table_name = 'gene_concepts'
        if table_name not in existing_tables:
            self.ddb.create_table(
                TableName=table_name,
                KeySchema=[
                    {
                        'AttributeName': 'label_and_type',
                        'KeyType': 'HASH'  # Partition key
                    },
                    {
                        'AttributeName': 'concept_id',
                        'KeyType': 'RANGE'  # Sort key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'label_and_type',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'concept_id',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'src_name',
                        'AttributeType': 'S'
                    }

                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'src_index',
                        'KeySchema': [
                            {
                                'AttributeName': 'src_name',
                                'KeyType': 'HASH'
                            }
                        ],
                        'Projection': {
                            'ProjectionType': 'KEYS_ONLY'
                        },
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 10,
                            'WriteCapacityUnits': 10
                        }
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )

    def create_meta_data_table(self, existing_tables: List[str]):
        """Create MetaData table if non-existent.

        :param List[str] existing_tables: table names already in DB
        """
        table_name = 'gene_metadata'
        if table_name not in existing_tables:
            self.ddb.create_table(
                TableName=table_name,
                KeySchema=[
                    {
                        'AttributeName': 'src_name',
                        'KeyType': 'HASH'  # Partition key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'src_name',
                        'AttributeType': 'S'
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
