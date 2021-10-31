# coding: utf-8

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkocr.v1.region.ocr_region import OcrRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkocr.v1 import *
import json
if __name__ == "__main__":
    ak = "8M6K1TP0QZFUPKK591RU"
    sk = "CS7GTtMcTwQG7amGn3i3O7YFQQKwyJDOogD0w4hs"
    pid="0d98f3544580f2af2fadc0008ed248d3"
    credentials = BasicCredentials(ak, sk,pid) \

    client = OcrClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(OcrRegion.value_of("cn-north-4")) \
        .build()

    try:
        request = RecognizeGeneralTextRequest()
        request.body = GeneralTextRequestBody(
            quick_mode=False,
            detect_direction=False,
            image="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"
)
        response = client.recognize_general_text(request)
        result=json.loads(str(response))
        print(result)
        print(result.get('result').get('words_block_list')[0].get('words'))

      #  print(response.res.get('result'))

    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)