import os, shutil, openpyxl

# from noisegate import read_list_from_txt
# from settings import *
## 从xlsx final中读取<id, name, conflist, violist>
buttonLowerCaseTxtPath = "./button_lowercase.txt"

# 从txt文件中读取数据，替换空格，返回list
def read_list_from_txt(txtpath):
    f = open(txtpath)
    str = f.read()
    list = str.replace(' ','').split(',')
    print("Read {} success!".format(txtpath))
    f.close()
    return list

def getALLDictFromXlsx(xlsx_path):
    res_dict = {}
    wb = openpyxl.load_workbook(filename=xlsx_path)
    ws = wb["Final"]
    for i in range(2, ws.max_row+1):
        if ws.cell(row=i, column=1).value is not None:
            row_dict = {}
            id = int(ws.cell(row=i, column=1).value)
            name = str(ws.cell(row=i, column=5).value)
            comptype = str(ws.cell(row=i, column=3).value)
            if ws.cell(row=i, column=6).value is not None:
                c_list_temp = ws.cell(row=i, column=6).value.replace(' ','').split(',')
                c_list = [int(x) for x in c_list_temp if x != ''] # 清除空格v
            else:
                c_list = []
            if ws.cell(row=i, column=7).value is not None:
                v_list_temp = ws.cell(row=i, column=7).value.replace(' ','').split(',')
                v_list = [int(x) for x in v_list_temp if x != ''] # 清除空格
            else:
                v_list = []
            ## 如果name为button_no_lowercase，则从txt中读取v_list
            if name == "button_no_lowercase":
                v_list = read_list_from_txt(buttonLowerCaseTxtPath)
                v_list = [int(x) for x in v_list]
            res_dict[name] = c_list
            # row_dict["id"] = id
            # row_dict["name"] = name
            # row_dict["component"] = comptype
            # row_dict["conformanceList"] = c_list  
            # row_dict["violationList"] = v_list
            # print(row_dict)
            # res_dict["data"].append(row_dict)
    # with open(dict_path, 'w') as f:
    #     json.dump(res_dict, f, indent=4)
    
    return res_dict

if __name__ == '__main__':
    groundTruthxlsDataPath = "./Rule_Summary.xlsx"
    GTDict = getALLDictFromXlsx(groundTruthxlsDataPath)
    vioIDList = sum(list(GTDict.values()), [])
    vioIDList = set(vioIDList)
    print(len(vioIDList))
    
    

