import os
import xlrd

# 获取当前路径
work_path = os.getcwd()
case_path = work_path + "\case"
file_list = []
sheet_fields = []
department = "智能事业部"
author = "邬军"
insert_sql = '''
insert into qa_autotest_case(department,module,project,service_name,api_name,author,not_run,description,
method,protocol,url,headers,apikey,xgd_param,input_file,param,init_mysql_bc,contains_str,rep_status,
verify,mysql_verify,recover_mysql_ac,save,pre_param,sleep) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''

def listdir(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file) #获取绝对路径
        if os.path.isdir(file_path): #如果还是文件夹，就继续迭代本函数
            listdir(file_path)
        elif file_path.endswith(".xls") or file_path.endswith(".xlsx"):
            file_list.append(file_path)

def read_excel(cursor):
    listdir(case_path)
    for file in file_list:
        temp_path = file.split("import_data_to_db\\", 1)[1]
        module = "server"
        project = ""

        if temp_path.startswith("case\server\\"):
            module = "server"
            project = ""
        elif temp_path.startswith("case\web\\"):
            module = "web"
            project = temp_path.split("\\")[2]
        else:
            print("error: 请检查用例目录是否正确")

        service_name = file.rsplit("\\", 1)[1].split("-", 1)[0]

        # open file
        workbook = xlrd.open_workbook(file)
        # get all sheet
        sheet_list = workbook.sheet_names()
        # 获取表头行
        global sheet_fields
        if len(sheet_fields) == 0:
            sheet_fields = workbook.sheet_by_name(sheet_list[0]).row_values(0)

        for sheet in sheet_list:
            api_name = sheet
            # 通过sheet名字获取sheet对象
            sheet_obj = workbook.sheet_by_name(sheet)
            rows = sheet_obj.nrows
            for row in range(rows - 1):
                row_value = sheet_obj.row_values(row + 1)
                insert_value_list = [department,module,project,service_name,api_name,author]
                for field_value in row_value:
                    insert_value_list.append(field_value)
                print(insert_value_list)
                cursor.execute(insert_sql, insert_value_list)
