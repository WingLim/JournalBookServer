FROM python:3.7.7-alpine

# 使用清华镜像源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories

WORKDIR /root

COPY . .

RUN apk add --no-cache gcc musl-dev\
    &&pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 清理缓存
RUN rm -rf /tmp/* /var/cache/apk/*

ENTRYPOINT [ "gunicorn", "api:app", "-c", "gunicorn.conf.py"]