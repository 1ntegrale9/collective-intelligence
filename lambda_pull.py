import boto3
from functools import reduce
from operator import and_
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('collective-intelligence')
    responses = (table.query(KeyConditionExpression=Key('tag').eq(tag)) for tag in event['tags'])
    tags_set = (set(tag for item in response['Items'] for tag in item['tags']) for response in responses)
    tags = list(reduce(and_, tags_set))
    return {
        'statusCode': 200,
        'body': tags,
    }


def test():
    return {
        "tags": [
            "python2",
            "python3"
        ]
    }
