import copy
import json
from decimal import Decimal
from typing import Optional

import boto3
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer
from botocore import exceptions


class InsufficientArgumentsException(Exception):
    pass


class IndexNotValidException(Exception):
    pass


class InvalidArgumentsException(Exception):
    pass


class ConditionalCheckFailedException(Exception):
    pass


class DynamoDBDataStore(object):
    serializer = TypeSerializer()
    deserializer = TypeDeserializer()

    def __init__(self, table_name, hash_key='PK', sort_key='SK', use_default_index_keys=True, endpoint_url=None):

        DB_SETTINGS = {
            'TableName': table_name,
            'HashKeyName': hash_key,
            'SortKeyName': sort_key
        }

        self.table_name = DB_SETTINGS['TableName']
        self.hash_key_name = DB_SETTINGS['HashKeyName']
        self.sort_key_name = DB_SETTINGS.get('SortKeyName', None)
        self.index_keys = [
            self.hash_key_name,
            self.sort_key_name
        ]
        if use_default_index_keys:
            self.add_index_keys([
                'GSI1PK',
                'GSI1SK',
                'GSI2PK',
                'GSI2SK',
            ])

        self.client = boto3.client('dynamodb', endpoint_url=endpoint_url)

    def add_index_keys(self, keys_to_add: list):
        if type(keys_to_add) != list:
            raise TypeError('Expected a list but received ', type(keys_to_add))
        for key in keys_to_add:
            self.add_index_key(key)

    def add_index_key(self, key_to_add: str):
        if type(key_to_add) != str:
            raise TypeError('Expected a string but received ', type(key_to_add))
        self.index_keys.append(key_to_add)

    def save_document(self, document, index=None, parameters=None):
        if parameters is None:
            parameters = {}

        document = copy.deepcopy(document)

        if len(index) not in [1, 2]:
            raise IndexNotValidException

        if len(index) == 1:
            self._save_document_using_hash_key(document, hash_key=index[0], parameters=parameters)
        else:
            self._save_document_using_composite_key(document, hash_key=index[0], sort_key=index[1],
                                                    parameters=parameters)

    def _save_document_using_composite_key(self, document, hash_key, sort_key, parameters=None):
        if parameters is None:
            parameters = {}
        document[self.hash_key_name] = hash_key
        document[self.sort_key_name] = sort_key

        document = json.loads(json.dumps(document), parse_float=Decimal)

        document = self.serialize(document)
        self._put_item(document, parameters=parameters)

    def _save_document_using_hash_key(self, document, hash_key, parameters=None):
        if parameters is None:
            parameters = {}
        document[self.hash_key_name] = hash_key

        document = json.loads(json.dumps(document), parse_float=Decimal)

        document = self.serialize(document)

        self._put_item(document, parameters=parameters)

    def _put_item(self, item, parameters=None):

        if parameters is None:
            parameters = {}
        params = {
            'TableName': self.table_name,
            'Item': item,
            **parameters
        }

        try:
            self.client.put_item(**params)
        except exceptions.ClientError as e:
            if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                raise e
            raise ConditionalCheckFailedException

    def get_document(self, index=None, return_index=False, consistent_read=False):
        if len(index) not in [1, 2]:
            raise IndexNotValidException

        key = {
            self.hash_key_name: {'S': index[0]}
        }

        if len(index) == 2:
            key[self.sort_key_name] = {'S': index[1]}

        item = self.client.get_item(
            TableName=self.table_name,
            Key=key,
            ConsistentRead=consistent_read
        ).get('Item', None)

        if not item:
            return None

        deserialized_item = self.deserialize(item)

        if not return_index:
            deserialized_item.pop(self.hash_key_name, None)
            deserialized_item.pop(self.sort_key_name, None)

        return deserialized_item

    def serialize(self, document):
        return DynamoDBDataStore.serializer.serialize(document)['M']

    def deserialize(self, document):
        return DynamoDBDataStore.deserializer.deserialize({'M': document})

    def paginate(self, parameters: dict = None, paginator_type='query'):
        if not parameters:
            parameters = {}

        parameters['TableName'] = self.table_name

        paginator = self.client.get_paginator(paginator_type)
        return paginator.paginate(**parameters)

    def update_document(self, index=None, parameters=None):

        if parameters is None:
            parameters = {}
        if len(index) not in [1, 2]:
            raise IndexNotValidException

        key = {
            self.hash_key_name: {'S': index[0]}
        }

        if len(index) == 2:
            key[self.sort_key_name] = {'S': index[1]}

        params = {
            'TableName': self.table_name,
            'Key': key,
            **parameters
        }

        try:
            self.client.update_item(**params)
        except exceptions.ClientError as e:
            if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                raise e
            raise ConditionalCheckFailedException

    def delete_document(self, index=None, parameters=None):
        if parameters is None:
            parameters = {}
        if len(index) not in [1, 2]:
            raise IndexNotValidException

        key = {
            self.hash_key_name: {'S': index[0]}
        }

        if len(index) == 2:
            key[self.sort_key_name] = {'S': index[1]}

        params = {
            'TableName': self.table_name,
            'Key': key,
            **parameters
        }

        try:
            self.client.delete_item(**params)
        except exceptions.ClientError as e:
            if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                raise e
            raise ConditionalCheckFailedException

    def batch_request(self, request_items):
        if not request_items:
            raise InsufficientArgumentsException('You must provide request_items')

        self.client.batch_write_item(RequestItems={
            self.table_name: request_items
        })

    def get_documents(self, query: dict = None, return_index: bool = False, scan: bool = False) -> Optional[list]:
        """
        Perform a SCAN or a QUERY on a DynamoDB Table by setting the scan flag or providing query parameters.
        Optionally return the index keys by setting the return_index flag.

        :param query: A query dict containing DynamoDB query parameters
        :type query: dict

        :param return_index: A flag indicating if the indexes for the document should be returned with the document
        :type return_index: bool

        :param scan: A flag to indicate that the table should be scanned. cannot be used in conjunction with query
        :type scan: bool

        :return: The documents returned as a list of dicts or None if no documents were returned or in case of an error
        """

        if not query and not scan:
            raise InsufficientArgumentsException('You must provide a query')
        if query and scan:
            raise InvalidArgumentsException('You cannot specify a query when performing a scan. '
                                            'Set scan to False if you wish to perform a query '
                                            'or leave out the query parameter to perform a scan')

        try:
            paginator_type = 'scan' if scan else 'query'
            pages = self.paginate(query, paginator_type)
            documents = []

            for page in pages:
                items = page['Items']

                for item in items:
                    document = self.deserialize(item)
                    if not return_index:
                        for key in self.index_keys:
                            document.pop(key, None)

                    documents.append(document)

            return documents
        except Exception as e:
            print(e)
            return None

    def transaction_write(self, batch_items, transaction_id):
        self.client.transact_write_items(
            TransactItems=batch_items,
            ClientRequestToken=transaction_id
        )
