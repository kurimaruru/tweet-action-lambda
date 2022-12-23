import json
import traceback
from dynamodb import Dynamodb

# from websocket import (
#     connect_apigw,
#     get_websocket_table,
#     get_connection_id,
#     post_to_connection,
# )
from websocket import Websocket


def handler(event, context):
    print("event = ", json.dumps(event))
    # connection table
    dynamodb = Dynamodb.connect_db()
    table = dynamodb.Table("SNS")
    # websocket connection_id
    connect_id = event["requestContext"]["connectionId"]
    # websocket接続情報取得
    websocket_table = Websocket.get_websocket_table()
    id = Websocket.get_connection_id(websocket_table, connect_id)
    print("connection id = ", id)
    if id is None:
        print("can not connect")
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"result": 1}, ensure_ascii=False),
        }

    dict_body = json.loads(event["body"])
    operationType = dict_body["data"]["OperationType"]
    if operationType != "SCAN":
        partitionKey = dict_body["data"]["keys"]["partitionKey"]
        # キー項目以外の値
        if operationType == "PUT":
            columns = dict_body["data"]["columns"]
            print("columns = ", columns)
    try:
        # api gateway接続(websocket)
        apigw_management = Websocket.connect_apigw()
        if operationType == "SCAN":
            res = Dynamodb.scan(table)
            res_data = {"key": "tweet", "data": res}
            Websocket.post_to_connection(
                apigw_management, id[0]["connection_id"], res_data
            )
        elif operationType == "QUERY":
            res = Dynamodb.query(table, partitionKey)
            res_data = {"key": "tweet", "data": res}
            Websocket.post_to_connection(
                apigw_management, id[0]["connection_id"], res_data
            )
        # insert or update
        elif operationType == "PUT":
            Dynamodb.put(table, partitionKey, columns)
            res = Dynamodb.scan(table)
            res_data = {"key": "tweet", "data": res}
            Websocket.post_to_connection(
                apigw_management, id[0]["connection_id"], res_data
            )
        # delete
        elif operationType == "DELETE":
            Dynamodb.delete(table, partitionKey)
            res = Dynamodb.scan(table)
            res_data = {"key": "tweet", "data": res}
            Websocket.post_to_connection(
                apigw_management, id[0]["connection_id"], res_data
            )
        else:
            print("Operateion type error!!!")
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"result": 0}, ensure_ascii=False),
        }
    except:
        print("error!!!")
        traceback.print_exc()
