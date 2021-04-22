# lambda-que-recibe
import boto3
import json
import logging
from pprint import pprint

def get_logger():
    log_format = '[%(asctime)s]: %(levelname)-4s in ' + \
                    '%(module)s:%(lineno) d[%(funcName)s]: %(message)s'
    logging.basicConfig(level=logging.ERROR, format=log_format)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    return logger

logger = get_logger()

def get_account_id_from_event(event) -> str:
    records = event.get('Records', [])
    logger.info("event.get(Records)")
    pprint(records)
    if not records:
        logger.error("[lambda-que-recibe] Empty Records")
        return ""

    if len(records) > 1:
        logger.error("[lambda-que-recibe] Multiple records in event")
        return ""

    message_body = json.loads(records[0].get('body', '{}'))
    account_id = message_body.get('accountId')
    if not account_id:
        logger.error("[lambda-que-recibe] Not account_id within message body")
        return ""


    return account_id

def lambda_handler(event, context):
    logger.info("start recibe")
    logger.info("EVENT received")
    pprint(event)
    logger.info("end EVENT")
    account_id = get_account_id_from_event(event)
    if not account_id:
        error = "Missing accountId"
        logger.error(error)
        return {"error": error}

    logger.info(f"end recibe account-id: {account_id}")

"""
{
	'Records': [
		{
		'attributes': {'ApproximateFirstReceiveTimestamp': '1619094828869',
		'ApproximateReceiveCount': '1',
		'SenderId': 'AROATKX3FEXQZPZAJZR3B:lambda-que-envia',
		'SentTimestamp': '1619094828863'},
		'awsRegion': 'us-east-2',
		'body': '{"accountId": "1234"}',
		'eventSource': 'aws:sqs',
		'eventSourceARN': 'arn:aws:sqs:us-east-2:aaaacccc:sqs-lambda-que-recibe',
		'md5OfBody': '30840356415d359f33cec2ad1682bd71',
		'messageAttributes': {},
		'messageId': '0514edc1-2048-4b12-8cc0-d6938d07101c',
		'receiptHandle': 'AQEBGxDrjg2DP0ZlWNYqU8BPJw8V7vhfZkRlzcfETOmzzQOkfqjn2x9CXiumMkHrsdbdb89euvv+krJsG2vWOXSm9AFfoMSzVQxMrvW3vt41Vf8894TUgBnJd7xjHTmnHjnifZtXbvFtQfM94CVk+kTGLln98PJ8nAwLcFlDrIwj6GiCI89mlDv8Ag5vazwndU1kpc8BRlEZc6IiSCSuuMpA7YDsN3o1kj8SJrfzT0fUkljjTLa/Sl94d5jXxT2Ygm1PuHRgFlkVE63J/RzngMaTqnPh7GuH5h45VKovl2Zp70ue3gr8TJeKDdmGEjXoes6qSHM3bOB/JyWCND661YNIbiiWz0Sw6of7vAd3D0VjzxAx4tPeQu6AlfHqTokUt+ke3drUypH+3eCaH52+ie/xzg=='
		}
	]
}
"""
