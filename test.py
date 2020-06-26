import pandas as pd

provinces_of_china = ['Fujian', 'Guangdong', 'Gansu', 'Guangxi', 'Guizhou', 'Henan', 'Hubei', 'Hebei', 'Hainan',
                      'Heilongjiang', 'Hunan', 'Jilin', 'Jiangsu', 'Jiangxi', 'Liaoning', 'NeiMengGu', 'Ningxia',
                      'Qinghai', 'Sichuan', 'Shandong', 'Shaanxi', 'Shanxi', 'Tianjin', 'Xinjiang', 'Xizang', 'Yunnan',
                      'Zhejiang']

abc = pd.DataFrame(index = provinces_of_china)

print(abc)
