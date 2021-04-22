# lambda-que-envia
import boto3
import json
import logging
from pprint import pprint

def get_config() -> dict:
    return {
        "account": "aaaacccc",
        "region": "eu-west-1",
    }

def get_logger():
    log_format = '[%(asctime)s]: %(levelname)-4s in ' + \
                    '%(module)s:%(lineno) d[%(funcName)s]: %(message)s'
    logging.basicConfig(level=logging.ERROR, format=log_format)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    return logger

logger = get_logger()



def lambda_handler(event, context):
    logger.info("start")

    account_id="1234"
    sqs_url = "https://sqs.eu-west-1.amazonaws.com/aaaacccc/sqs-trigger-lambda-que-recibe"

    sqs_client = boto3.client('sqs', region_name="eu-west-1")
    response = sqs_client.send_message_batch(
        QueueUrl=sqs_url,
        Entries=[{
            "Id": "1",
            "MessageBody": json.dumps({
                "accountId": account_id
            }),
        }]
    )
    logger.info("response sqs")
    pprint(response)
    logger.info("end")

"""
{
	'ResponseMetadata': {
    'HTTPHeaders': {
      'content-length': '467',
      'content-type': 'text/xml',
      'date': 'Thu, 22 Apr 2021 12:20:03 GMT',
      'x-amzn-requestid': '4da969ec-10d8-51f8-8263-31177ceb3503'
    },
    'HTTPStatusCode': 200,
    'RequestId': '4da969ec-10d8-51f8-8263-31177ceb3503',
    'RetryAttempts': 0
  },
	'Successful': [
      {
        'Id': '1',
	      'MD5OfMessageBody': '30840356415d359f33cec2ad1682bd71',
	      'MessageId': 'f60ac369-85fa-44a4-96de-fa5c4da0bee3'
      }
  ]
}

Response
{
  "errorMessage": "An error occurred (AWS.SimpleQueueService.NonExistentQueue) when calling the SendMessageBatch operation: The specified queue does not exist for this wsdl version.",
  "errorType": "QueueDoesNotExist",
  "stackTrace": [
    [
      "/var/task/lambda_function.py",
      29,
      "lambda_handler",
      "\"accountId\": account_id"
    ],
    [
      "/var/runtime/botocore/client.py",
      357,
      "_api_call",
      "return self._make_api_call(operation_name, kwargs)"
    ],
    [
      "/var/runtime/botocore/client.py",
      676,
      "_make_api_call",
      "raise error_class(parsed_response, operation_name)"
    ]
  ]
}
"""

