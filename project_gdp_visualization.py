#coding:utf-8
"""
综合项目:世行历史数据基本分类及其可视化
作者：周磊
日期:2020.06.16
注意: 请将isp_gdp.csv文件放在与本程序相同的文件夹下
"""

#导入第三方库
import pygal                #用于可视化
import pygal_maps_world     #用于展示地图
import csv                   #用于读取csv文件
import math                 #数学符号计算


#定义readcsv函数
"""
功能介绍：
用于读取文件名为filename、键名为kefield、分割符为separator、引用符为quote的csv文件
输出数据的格式为字典
"""
def readcsv(filename, keyfield, separator, quote): 
    result={}

    with open(filename,newline="")as csvfile:
        csvreader=csv.DictReader(csvfile,delimiter=separator,quotechar=quote)
        for row in csvreader:
            rowid=row[keyfield]
            result[rowid]=row

    return result

#定义reconcile函数
"""
功能介绍:返回元组格式
plot_countries为国家代码数据
gdp_countries:各国数据

"""
def reconcile(plot_countries, gdp_countries): 
    dict_1 = {}
    set_1  = set()

    for pygal_country_code in plot_countries :
        if plot_countries[pygal_country_code] in gdp_countries : 
            dict_1[pygal_country_code] = plot_countries[pygal_country_code]
            gdp_countries.pop(gdp_countries.index(plot_countries[pygal_country_code]))

    set_1 = set(gdp_countries)
    tuple_1 = (dict_1,set_1)

    return tuple_1
#build_map函数
"""
功能介绍:输出一个字典+二个集合的元组数据
gdpinfo: gdp为信息字典
plot_countries为国家代码数据
year: 年份

"""
def build_map(gdpinfo, plot_countries, year):
    countries_year_gdp = {}
    set_2 = set()
    set_3 = dict()
    
    years_gdp = []
    
    for plot_countries_code in plot_countries :
        for isp_country_code in gdpinfo :
            
            if gdpinfo[isp_country_code]["Country Name"] == plot_countries[plot_countries_code] :
                
                gdp_number = ''
                country_imformations = []
                
                for country_imformation in gdpinfo[isp_country_code] :
                    country_imformations.append(country_imformation)
                
                for year_1 in country_imformations[4:-1] :
                    gdp_number += gdpinfo[isp_country_code][year_1]
                    
                if gdp_number == '' :
                    set_2.add(plot_countries_code)
                    
                else :
                    if gdpinfo[isp_country_code][year] != '' :
                        
                        gdp_num = math.log10(float((gdpinfo[isp_country_code][year])))
                        countries_year_gdp[plot_countries_code] = gdp_num

                    else :
                        set_3[plot_countries_code] = '该年暂无数据'
                continue

    
    isp_countries = []
    
    for isp_country_code in gdpinfo :
        isp_countries.append(gdpinfo[isp_country_code]["Country Name"])
        
    
    in_countries, not_in_countries = reconcile(plot_countries, isp_countries)
    
    # set_2 = not_in_countries
    tuple_2 = (countries_year_gdp,set_2,set_3)
    
    return tuple_2

#定义render_map
"""
功能介绍:将指定某年的世界各国GDP数据在世界地图上显示
gdpinfo:gdp信息字典
plot_countires:国家代码数据
year为年份数据
map_file:输出图片名

"""

def render_map(gdpinfo, plot_countries, year, map_file): 
    
    A_countries,B_countries,C_countries = build_map(gdpinfo, plot_countries, year)

    worldmap_chart = pygal.maps.world.World()
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = '世行%s年国家GDP数据'%(year)
    worldmap_chart.add('该年在绘图库及世行有数据的国家及其GDP数据', A_countries)
    worldmap_chart.add('在绘图库中没有数据的国家',B_countries)
    worldmap_chart.add('该年在世行没有GDP数据的国家',C_countries)
    worldmap_chart.render()

    worldmap_chart.render_to_file(map_file)


"""
定义测试函数test_map

"""
def test_map(year):  
    
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    } 
    
    
    
    gdp_csv = readcsv(gdpinfo['gdpfile'], gdpinfo['country_code'], gdpinfo['separator'], gdpinfo['quote'])

    pygal_countries = pygal.maps.world.COUNTRIES   
    
    isp_countries = []
    for isp_country_code in gdp_csv :
        isp_countries.append(gdp_csv[isp_country_code]["Country Name"])
        
    in_countries, not_in_countries = reconcile(pygal_countries, isp_countries)

    render_map(gdp_csv, in_countries, year, "isp_gdp_world_name_%s.svg"%(year))


print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.")
year=input("请输入需查询的具体年份:")

while float(year) < 1960 or float(year) > 2015 :
    print('查询不到该年的数据')
    print()
    year=input("输入查询年份:")
    
else :
    test_map(year)
