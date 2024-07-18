## 统计类别

from groud_truth_xlsx_extractor import getALLDictFromXlsx, read_list_from_txt
import ujson as json
import pandas as pd

def count_categories(id_list, id_to_package_name_dict, package_name_to_category):
    category_count = {}
    for id_ in id_list:
        # 获取对应的 package_name
        package_name = id_to_package_name_dict.get(str(id_))
        if package_name:
            # 获取对应的 category
            category = package_name_to_category.get(package_name)
            if category:
                # 更新 category_count 字典
                if category not in category_count:
                    category_count[category] = 0
                category_count[category] += 1
    
    return category_count

def calculate_percentage(category_count, total_count):
    category_percentage = {category: (count / total_count) * 100 for category, count in category_count.items()}
    return category_percentage

def write_sorted_categories_to_file(sorted_categories, category_percentage, output_file_path):
    with open(output_file_path, 'w') as file:
        for category, count in sorted_categories:
            file.write(f"{category}:{count},{category_percentage[category]:.2f}\n")


# 文件路径
csv_file_path = "./app_details.csv"
# 属性列表： ['App Package Name', 'Play Store Name', 'Category', 'Average Rating', 'Number of Ratings', 'Number of Downloads', 'Date Updated', 'Icon URL']
id2app_filename = "./id2PackageName.json"
output_file_path = "./sampling_category.txt"

sample_c_list = read_list_from_txt("./sampling_c_result.txt")
sample_v_list = read_list_from_txt("./sampling_v_result.txt")
sample_oth_list = read_list_from_txt("./sampling_oth_result.txt")

sample_all_list = sample_c_list + sample_v_list + sample_oth_list
print("sample_all_list_len: ", len(sample_all_list))
print("sample_all_list_len: ", len(set(sample_all_list)))


# 加载 id 到 package_name 的映射
with open(id2app_filename, mode='r', encoding='utf-8') as file:
    id_to_package_name_dict = json.load(file)
# 加载CSV数据
df = pd.read_csv(csv_file_path)
# 获取 package_name 到 category 的映射
package_name_to_category = dict(zip(df['App Package Name'], df['Category']))
# 统计每个 category 的数量
category_count = count_categories(set(sample_all_list), id_to_package_name_dict, package_name_to_category)
# 计算总数量，也是涉及的样本数量
total_count = sum(category_count.values())
# 计算每个 category 的占比
category_percentage = calculate_percentage(category_count, total_count)
# 按占比降序排序并输出结果
sorted_categories = sorted(category_count.items(), key=lambda x: category_percentage[x[0]], reverse=True)
# 输出结果
# for category, count in sorted_categories:
#     print(f"{category}:{count},{category_percentage[category]:.2f}")

# 输出到文件
# write_sorted_categories_to_file(sorted_categories, category_percentage, output_file_path)



