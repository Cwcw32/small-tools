# 测试翻译调用
import json
from huaweicloud_nlp.NlpfClient import NlpfClient
from huaweicloud_nlp.HWNlpClientAKSK import HWNlpClientAKSK

akskClient = HWNlpClientAKSK("8M6K1TP0QZFUPKK591RU",  # 用户的ak
                             "CS7GTtMcTwQG7amGn3i3O7YFQQKwyJDOogD0w4hs",  # 用户的sk
                             "cn-north-4",  # region值
                             "0d98f3544580f2af2fadc0008ed248d3")  # projectId
# proxy = {"http": "http://username:password@proxy.com", "https": "http://username:password@proxy.com"} # 如果需要，可以使用http代理，否则不需要
# akskClient.set_proxy(proxy) # 如果需要，可以使用http代理，否则不需要
nlpfClient = NlpfClient(akskClient)
from huaweicloud_nlp.MtClient import MtClient

mtClient = MtClient(akskClient)
# 根据初始化Client章节选择认证方式构造完成mtClient后调用
response = mtClient.translate_text("how are you", "en", "zh", "common")
# 结果为code和json结构体
print(response.code)
# print(json.dumps(response.res,ensure_ascii=False))
print(response.res.get('src_text'))#keys())
