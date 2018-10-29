import requests
from lxml import etree
import csv
import pymysql
#伪装浏览器的请求头信息，避免服务器识别我们是爬虫
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

url = "http://maoyan.com/board/4"
response = requests.get(url, headers = headers)
html = response.text

#初始化
html = etree.HTML(html)
#提取电影：霸王别姬
result_bawangbieji = html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd[1]/div/div/div[1]/p[1]/a')
print(result_bawangbieji[0].text)
#提取所有电影名
result_all = html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/div/div/div[1]/p[1]/a')
print("all_movie: ")
for one in result_all:
	print(one.text)

# 1.保存至文件:'a'以追加方式写入文件
# with open('film_name.text','a') as f:
# 	for one in result_all:
# 		f.write(one.text + '\n')

# 2.保存为csv文件
# with open('file_name.csv','a',newline='') as f:
# 	csv_file = csv.writer(f)
# 	for one in result_all:
# 		csv_file.writerow([one.text])

#3.保存至mysql数据库中
#3.1打开数据库连接，应确保mysql中已有spider库
db = pymysql.connect(host='localhost',user='root',password='root123',
	port=3306, db='spider',use_unicode=True, charset = 'utf8')
#3.2获取游标
cursor = db.cursor()
for one in result_all:
	try:
		sql = 'INSERT INTO film_info(film_name) values (%s)'
		#3.3执行
		cursor.execute(sql, (one.text))
		db.commit()
	except:
		db.rollback()
#3.4关闭资源
db.close()



