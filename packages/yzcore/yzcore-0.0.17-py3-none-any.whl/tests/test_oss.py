#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2021/2/25
@desc: ...
"""
import oss2
from yzcore.extensions.aliyun_oss import OssManager
oss_conf = dict(
    access_key_id="LTAI4GA13VDvJPYnRa1yW17Q",
    access_key_secret="AAYIEX0UVR3sDNr4DQFa68525mTMdp",
    # access_key_id="LTAI4GCahbN1hoc4DBpwoYuK",
    # access_key_secret="TpVOzSha6dsyksgZWwTnm7BcAGqqUh",
    endpoint="oss-cn-shenzhen.aliyuncs.com",
    # endpoint="oss-cn-shenzhen-internal.aliyuncs.com",
    bucket_name="cmlcmlcmkfksjfkjaks-test",
    cache_path="/tmp/realicloud/fm/cache"
)
if __name__ == '__main__':
    oss = OssManager(**oss_conf)
    # print(oss.bucket.delete_bucket())
    # oss.create_bucket()
    import time
    start = time.time()
    print(oss.upload("/Users/edz/Downloads/666260 《可伸缩服务架构：框架与中间件》- 完整书签.pdf", "可伸缩服务架构-框架与中间件.pdf"))
    print(time.time() -start)
    # print(oss.download("test/狗1"))
    # print(oss.bucket.sign_url('GET', "《可伸缩服务架构：框架与中间件》- 完整书签.pdf", 5))
