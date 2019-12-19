import os
import xlrd

# 获取当前路径
work_path = os.getcwd()
case_path = work_path + "\case"
file_list = []
sheet_fields = []
department = "智能事业部"
author = "邬军"
pre_insert_sql = "insert into qa_autotest_case (department,module,project,service_name,api_name,author,"

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
        db_sheet_fields = ",".join(sheet_fields)

        for sheet in sheet_list:
            api_name = sheet
            # 通过sheet名字获取sheet对象
            sheet_obj = workbook.sheet_by_name(sheet)
            rows = sheet_obj.nrows
            for row in range(rows - 1):
                row_value = sheet_obj.row_values(row + 1)
                db_row_value = ",".join("\'" + str(field_value) + "\'" for field_value in row_value)
                # 替换sleep字段的值为0
                db_row_value = db_row_value.rsplit(",", 1)[0] + ",'0'"
                global pre_insert_sql
                pre_insert_values = department + "\',\'" + module + "\',\'" + project + "\',\'" + service_name + "\',\'" + api_name + "\',\'" + author + "\',"
                insert_sql = pre_insert_sql + db_sheet_fields + ") values (\'" + pre_insert_values + db_row_value + ")"
                print(insert_sql)
                cursor.execute(insert_sql)
