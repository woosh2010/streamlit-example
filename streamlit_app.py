import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import folium

# 读取Excel文件
df = pd.read_excel('/Users/cyrus/PycharmProjects/pythonProject/比亚迪经销商明细批量获取并对比/map.xlsx',
                   engine='openpyxl')

# 创建省份下拉框
provinces = ['全部'] + sorted(list(df['所属省份'].unique()), key=lambda x: len(df[df['所属省份'] == x]), reverse=True)
province_name = st.selectbox('选择省份', provinces, format_func=lambda x: f"{x} ({len(df[df['所属省份'] == x])})")

# 创建城市下拉框，只显示所选省份的城市
filtered_df = df[df['所属省份'] == province_name] if province_name != '全部' else df.copy()
cities = ['全部'] + sorted(list(filtered_df['所属城市'].unique()),
                           key=lambda x: len(filtered_df[filtered_df['所属城市'] == x]), reverse=True)
city_name = st.selectbox('选择城市', cities,
                         format_func=lambda x: f"{x} ({len(filtered_df[filtered_df['所属城市'] == x])})")
if city_name != '全部':
    filtered_df = filtered_df[filtered_df['所属城市'] == city_name]

# 创建区县下拉框，只显示所选城市的区县
counties = ['全部'] + sorted(list(filtered_df['所属区县'].unique()),
                             key=lambda x: len(filtered_df[filtered_df['所属区县'] == x]), reverse=True)
county_name = st.selectbox('选择区县', counties,
                           format_func=lambda x: f"{x} ({len(filtered_df[filtered_df['所属区县'] == x])})")
if county_name != '全部':
    filtered_df = filtered_df[filtered_df['所属区县'] == county_name]

# 创建所属集团、品牌和类型下拉框
groups = ['全部'] + sorted(list(filtered_df['所属集团'].unique()),
                           key=lambda x: len(filtered_df[filtered_df['所属集团'] == x]), reverse=True)
brands = ['全部'] + sorted(list(filtered_df['品牌'].unique()), key=lambda x: len(filtered_df[filtered_df['品牌'] == x]),
                           reverse=True)
types = ['全部'] + sorted(list(filtered_df['类型'].unique()), key=lambda x: len(filtered_df[filtered_df['类型'] == x]),
                          reverse=True)

group_name = st.selectbox('选择所属集团', groups,
                          format_func=lambda x: f"{x} ({len(filtered_df[filtered_df['所属集团'] == x])})")
if group_name != '全部':
    filtered_df = filtered_df[filtered_df['所属集团'] == group_name]
brand_name = st.selectbox('选择品牌', brands,
                          format_func=lambda x: f"{x} ({len(filtered_df[filtered_df['品牌'] == x])})")
if brand_name != '全部':
    filtered_df = filtered_df[filtered_df['品牌'] == brand_name]
type_name = st.selectbox('选择类型', types, format_func=lambda x: f"{x} ({len(filtered_df[filtered_df['类型'] == x])})")
if type_name != '全部':
    filtered_df = filtered_df[filtered_df['类型'] == type_name]

# 显示每个选项的数据数量
selected_province_count = len(df[df['所属省份'] == province_name]) if province_name != '全部' else len(df)
selected_city_count = len(filtered_df[filtered_df['所属城市'] == city_name]) if city_name != '全部' else len(
    filtered_df)
selected_county_count = len(filtered_df[filtered_df['所属区县'] == county_name]) if county_name != '全部' else len(
    filtered_df)
selected_group_count = len(filtered_df[filtered_df['所属集团'] == group_name]) if group_name != '全部' else len(
    filtered_df)
selected_brand_count = len(filtered_df[filtered_df['品牌'] == brand_name]) if brand_name != '全部' else len(filtered_df)
selected_type_count = len(filtered_df[filtered_df['类型'] == type_name]) if type_name != '全部' else len(filtered_df)

st.write(f"省份数量：{selected_province_count}", f"城市数量：{selected_city_count}", f"区县数量：{selected_county_count}")
st.write(f"所属集团数量：{selected_group_count}", f"品牌数量：{selected_brand_count}", f"类型数量：{selected_type_count}")

# 创建地图模式下拉框
map_modes = ['folium', 'streamlit']
map_mode = st.selectbox('选择地图模式', map_modes)

# 创建地图
if len(filtered_df) > 0:
    if map_mode == 'folium':
        # 创建Folium地图
        m = folium.Map(location=[filtered_df['lat'].mean(), filtered_df['lng'].mean()], zoom_start=13)

        # 在地图上添加标记
        for idx, row in filtered_df.iterrows():
            folium.Marker([row['lat'], row['lng']], popup=row['join_shop_name']).add_to(m)

        # 在Streamlit应用中显示地图
        folium_static(m)
    elif map_mode == 'streamlit':
        # 将'lng'列重命名为'longitude'
        filtered_df = filtered_df.rename(columns={'lng': 'longitude'})

        # 创建Streamlit地图
        st.map(filtered_df)
else:
    st.write("未找到匹配的经销商数据")
