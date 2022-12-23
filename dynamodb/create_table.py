# {
#   id: 1,
#   header: {
#     title: 'test1',
#     subheader: '2022/10/1',
#   },
#   content: {
#     message:
#       'This impressive paella is a perfect party dish and a fun meal to cook together with your guests. Add 1 cup of frozen peas along with themussels, if you like.',
#     imgName: 'cat.jpg',
#   },
#   action: {
#     good: 3,
#     bad: 0,
#   },
# },
import json
import boto3
import traceback

try:
    dynamo_db = boto3.resource(
        service_name="dynamodb",
        region_name="ap-northeast-1",
    )
    dynamo_db.create_table(
        TableName="SNS",
        KeySchema=[
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    )
except:
    print("create table error!!!")

    traceback.print_exc()
