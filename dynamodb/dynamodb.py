import boto3
from boto3.dynamodb.conditions import Key
import traceback


class Dynamodb:
    def connect_db():
        try:
            dynamo_db = boto3.resource(
                service_name="dynamodb",
                region_name="ap-northeast-1",
            )
            return dynamo_db
        except:
            print("connect db error")
            traceback.print_exc()

    # 全権取得
    def scan(table):
        try:
            scanData = table.scan()
            items = scanData["Items"]
            return items
        except:
            print("scan error")
            traceback.print_exc()

    # レコード検索
    def query(table, partitionKey):
        try:
            queryData = table.query(KeyConditionExpression=Key("id").eq(partitionKey))
            item = queryData["Items"]
            return item
        except:
            print("query error")
            traceback.print_exc()

    # レコード追加・更新
    def put(table, partitionKey, columns):
        try:
            # putRes = table.put_item(Item={"id": partitionKey})
            putRes = table.put_item(
                Item={
                    "id": partitionKey,
                    "header": {
                        "user_name": columns["header"]["user_name"],
                        "subheader": columns["header"]["subheader"],
                    },
                    "content": {
                        "message": columns["content"]["message"],
                        "imgName": columns["content"]["imgName"],
                        "imgUrl": columns["content"]["imgUrl"],
                    },
                    "action": {
                        "good": columns["action"]["good"],
                        "bad": columns["action"]["bad"],
                    },
                    "user_id": columns["user_id"],
                }
            )
            if putRes["ResponseMetadata"]["HTTPStatusCode"] != 200:
                print(putRes)
            else:
                print("PUT Successed.")
            return putRes
        except:
            print("put error")
            traceback.print_exc()

    # レコード削除
    def delete(table, partitionKey):
        try:
            delRes = table.delete_item(Key={"id": partitionKey})
            if delRes["ResponseMetadata"]["HTTPStatusCode"] != 200:
                print(delRes)
            else:
                print("Delete Successed.")
            return delRes
        except:
            print("delete error")
            traceback.print_exc()
