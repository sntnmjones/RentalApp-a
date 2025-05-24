import boto3
client = boto3.client(
    'dynamodb', 
    endpoint_url='http://localhost:8000',
    region_name='us-west-2'
)


def initialize_local_tables():
    table_name = 'rental-app-reviews'
    try:
        response = client.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    # partition key
                    'AttributeName': 'address',
                    'KeyType': 'HASH'
                },
                {
                    # sort key
                    'AttributeName': 'publishTimeUTC',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'address',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'publishTimeUTC',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 25,
                'WriteCapacityUnits': 25
            }
        )
        print(f"Table created successfully: {response}")
    except Exception as e:
        print(f"Error creating table: [{e}]", exc_info=True)


initialize_local_tables()
client.list_tables()
