FROM python:3.7.7-alpine

WORKDIR /root

COPY . .

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 清理缓存
RUN rm -rf /tmp/* /var/cache/apk/*

ENTRYPOINT [ "python", "api.py" ]