import json
import traceback
import os
import boto3
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv
from decimal import Decimal

load_dotenv()


class Websocket:
    # connection apigateway
    def connect_apigw():
        try:
            apigw_management = boto3.client(
                "apigatewaymanagementapi",
                endpoint_url=os.getenv("ENDPOINT_URL"),
            )
            print("endpoint = ", os.getenv("ENDPOINT_URL"))
            return apigw_management
        except:
            print("connection apigateway error")
            traceback.print_exc()

    # get table of websocket
    def get_websocket_table():
        try:
            dynamo_db = boto3.resource(
                service_name="dynamodb", region_name="ap-northeast-1"
            )
            table = dynamo_db.Table("WebSocket")
            return table
        except:
            print("get item of websocket error!!!")
            traceback.print_exc()

    # get connection_id from websocketTable
    def get_connection_id(table, partitionKey):
        try:
            # partitionKeyを指定して接続中のidを取得
            connection_id = table.query(
                KeyConditionExpression=Key("connection_id").eq(partitionKey)
            )
            id = connection_id["Items"]
            return id
        except:
            print("get connection id error")
            traceback.print_exc()

    # dynamoDBからの数値のレスポンスDecimal("0")という形で帰ってくるので変換
    def decimal_to_int(obj):
        if isinstance(obj, Decimal):
            return int(obj)

    # websocketの接続元にレスポンスを返す
    def post_to_connection(apigw_management, connection_id, res_data):
        try:
            convert_res_data = json.dumps(res_data, default=decimal_to_int)
            print("res", convert_res_data)
            apigw_management.post_to_connection(
                ConnectionId=connection_id, Data=convert_res_data
            )
        except:
            print("post_to_connection error")
            traceback.print_exc()
