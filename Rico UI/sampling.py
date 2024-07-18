# -*- coding: utf-8 -*-
# 1. 从app_details筛选特定下载量packageName和更新时间
# 2. 从id2PackageName获得rico id和packageName对应关系，过滤出考虑范围内的rico ID
# 3. 从rule_summary得到rico id的violation情况，算一下总数，然后采样多少个，检测出多少个问题，多少个是正确的，计算P、R、F1
import csv, random
import re
import ujson as json
from groud_truth_xlsx_extractor import getALLDictFromXlsx, read_list_from_txt

# 文件路径
csv_file_path = "./app_details.csv"
# 属性列表： ['App Package Name', 'Play Store Name', 'Category', 'Average Rating', 'Number of Ratings', 'Number of Downloads', 'Date Updated', 'Icon URL']
id2app_filename = "./id2PackageName.json"
groundTruthxlsDataPath = "./Rule_Summary.xlsx"

def parse_download_range(download_range):
    # 使用正则表达式提取下载范围的下限和上限
    match = re.match(r'\s*(\d{1,3}(?:,\d{3})*)\s*-\s*(\d{1,3}(?:,\d{3})*)\s*', download_range)
    if match:
        lower = int(match.group(1).replace(',', '').strip())
        upper = int(match.group(2).replace(',', '').strip())
        return (lower, upper)
    return (0, 0)
# 测试parse_download_range输入输出
# print(parse_download_range("  500,000,000 - 1,000,000,000  "))
# print(parse_download_range("January 10, 2015"))

def filter_downloads_by_threshold(csv_file_path, threshold):
    # 打开CSV文件
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        # 创建一个CSV读取器
        csv_reader = csv.DictReader(file)
        
        # 获取属性列表（第一行）
        fieldnames = csv_reader.fieldnames
        # print("属性列表：", fieldnames)
        
        # 存储结果的列表
        filtered_entries = []
        app_package_names = []
        total_count = 0
        
        # 过滤符合条件的条目
        for row in csv_reader:
            total_count += 1
            download_range = row['Number of Downloads']
            lower, _ = parse_download_range(download_range)
            if lower > threshold:
                filtered_entries.append(row)
                app_package_names.append(row['App Package Name'])
        
        return filtered_entries, len(filtered_entries), total_count, app_package_names

def get_package_name_to_id(id2app_filename, package_names):
    # 读取JSON文件
    with open(id2app_filename, mode='r', encoding='utf-8') as file:
        id_to_package_name_dict = json.load(file)
    
    # 反转字典以便通过package_name查找id列表
    pkgname_to_id_dict = {}
    for id, package_name in id_to_package_name_dict.items():
        if package_name in package_names:
            if package_name in pkgname_to_id_dict:
                pkgname_to_id_dict[package_name].append(id)
            else:
                pkgname_to_id_dict[package_name] = [id]
    
    return pkgname_to_id_dict

## 从GTDict中选取前三个 ID
def select_c_v_ids(GTDict, id_set):
    # 最终选出的ID列表
    selected_ids = []
    
    # 遍历 GTDict 中的每个 name
    for name, ids in GTDict.items():
        valid_ids = []
        count = 0
        # 过滤出存在于 id_set 中的前三个有效ID
        for id_ in ids:
            if id_ in id_set:
                valid_ids.append(id_)
                count += 1
                if count == 3:
                    break
        
        # 添加有效ID到最终选出的ID列表
        selected_ids.extend(valid_ids)
    
    return selected_ids

def random_sampling_ids(id_list, excluded_ids, sample_size=203):
    filtered_ids = [id_ for id_ in id_list if id_ not in excluded_ids]
    # 随机选择203个ID
    if len(filtered_ids) < sample_size:
        raise ValueError("Filtered ID list is smaller than the required sample size")
    selected_ids = random.sample(filtered_ids, sample_size)
    
    return selected_ids

# 下载量阈值设置
threshold = 500000

entries, filtered_count, total_count, app_package_names = filter_downloads_by_threshold(csv_file_path, threshold)
percentage = (filtered_count / total_count) * 100
print(f"下载量大于{threshold}的App数量：{filtered_count}/{total_count}，占比：{percentage:.2f}%")
#print("符合条件的 App Package Names 列表：", app_package_names)


# 从JSON文件中提取对应的id列表
package_name2id = get_package_name_to_id(id2app_filename, app_package_names)
# print("对应的 package_name2id 字典：")
# print(list(package_name2id.keys ())[10], package_name2id[list(package_name2id.keys ())[10]])
filter_ui_count = sum(len(v) for v in package_name2id.values())
filter_ui_id = sum(package_name2id.values(), [])
filter_ui_id = set(map(int, filter_ui_id))
ui_percentage = (filter_ui_count / 66261) * 100
print(f"下载量大于{threshold}的UI数量：{filter_ui_count}，占比：{ui_percentage:.2f}%")


# 示例 GTDict
GTDict = getALLDictFromXlsx(groundTruthxlsDataPath)
# GTDict = {"button": ["id1", "id2", "id3"],}

# # 调用函数进行筛选
# selected_ids = select_c_v_ids(GTDict, filter_ui_id)
# selected_ids.sort()
# # 输出结果
# print(f"选出的ID数量：{len(selected_ids)}")
# print(f"选出的ID列表：{selected_ids}")

sample_c_list = read_list_from_txt("./sampling_c_result.txt")
sample_v_list = read_list_from_txt("./sampling_v_result.txt")
sample_oth_list = read_list_from_txt("./sampling_oth_result.txt")

sample_all_list = sample_c_list + sample_v_list + sample_oth_list

excluded_ids = set(sample_all_list)

random_sampling_ids = random_sampling_ids(filter_ui_id, excluded_ids, 13)
random_sampling_ids.sort()
print(f"随机采样的ID数量：{len(random_sampling_ids)}")
print(f"随机采样的ID列表：{random_sampling_ids}")