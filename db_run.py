import pymysql.cursors
from read_excel_json import read_excel

# 连接数据库
db_con = pymysql.Connect(
    host = '192.168.0.72',
    port = 9306,
    user = 'root',
    passwd = '123456',
    db = 'qadb',
    charset = 'utf8'
)

def operation_data():
    cursor = db_con.cursor()
    read_excel(cursor)
    db_con.commit()
    db_con.close()

if __name__ == "__main__":
    operation_data()