import boto3, time, json
from decimal import Decimal


def lambda_handler(event, context):
    timestamp = Decimal(time.time())
    table = boto3.resource('dynamodb').Table('collective-intelligence')
    with table.batch_writer() as batch:
        def put(tag, tags):
            batch.put_item(Item={
                'tag': tag,
                'tags': tags,
                'timestamp': timestamp
            })
        tag, tags = event['tag'], set(event['tags'])
        put(tag, tags)
        [put(t, {tag}) for t in tags]
    return {'statusCode': 201}


def test():
    return {
        "tag": "python",
        "tags": [
            "プログラミング言語",
            "python2",
            "python3"
        ]
    }
