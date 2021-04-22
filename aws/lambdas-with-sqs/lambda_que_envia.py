# lambda-que-envia
import boto3
import json
import logging
from pprint import pprint


def get_config(key:str) -> str:
    config = {
        "account": "xxx",
        "region": "eu-west-1",
    }
    return config[key]


def get_logger():
    #[INFO]	2021-04-22T19:10:08.779Z	417574f5-e7ba-4770-9cfe-50bf66afc117
    log_format = '[%(asctime)s]: %(levelname)-4s in ' + \
                    '%(module)s:%(lineno) d[%(funcName)s]: %(message)s'
    logging.basicConfig(level=logging.ERROR, format=log_format)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    return logger


logger = get_logger()


def lambda_handler(event, context):
    logger.info("start")

    sqs_url = f"https://sqs.{get_config('region')}.amazonaws.com/{get_config('account')}/sqs-trigger-lambda-que-recibe"

    sqs_client = boto3.client(
        'sqs',
        region_name=get_config("region")
    )

    response = sqs_client.send_message_batch(
        QueueUrl=sqs_url,
        Entries=[{
            "Id": "1",
            "MessageBody": json.dumps({
                "accountId": "3456"
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

