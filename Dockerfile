FROM python:3.6

WORKDIR /MxShop

ENV MYSQL_DB ""
ENV MYSQL_USER ""
ENV MYSQL_PWD ""
ENV MYSQL_HOST ""

COPY requirements.txt /MxShop/

EXPOSE 8000

RUN pip install -i https://pypi.douban.com/simple -r requirements.txt

CMD ["uwsgi", "-i", "conf/uwsgi.ini"]

# docker build -t imxshop .

# docker run --name cmxshop -v $PWD:/MxShop -e MYSQL_DB=MxShop -e MYSQL_USER=root -e MYSQL_PWD=123456 -e MYSQL_HOST=120.78.193.99 -d imxshop

# 启动uwsgi后，查看该容器的ip为多少
# docker network inspect bridge   #172.17.0.3
# 修改nginx.conf的uwsgi server的ip
# docker run --name mxng2 -v $PWD/conf/nginx.conf:/etc/nginx/nginx.conf -v $PWD:/MxShop -p 8080:80 -d ng1.12.1

# admin admin1234
