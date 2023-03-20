import pandas as pd
import folium

filePath = './studyPython/university_locations.xlsx'
df_excel = pd.read_excel(filePath, engine='openpyxl')
df_excel.columns = ['학교명','주소','lng','lat'] # 컬럼명 가져오기

name_list =df_excel['학교명'].to_list()
addr_list = df_excel['주소'].to_list()
lng_list = df_excel['lng'].to_list()
lat_list = df_excel['lat'].to_list()

fMap = folium.Map(location=[37.553175, 126.989326], zoom_start=10)

for i in range(len(name_list)): #446번 돌면서
    if lng_list[i] != 0: # 0이면 위,경도 값이 출력을 못한다
        marker = folium.Marker([lat_list[i], lng_list[i]], popup=name_list[i], icon=folium.Icon(color='blue'))
        marker.add_to(fMap)

fMap.save('./studyPython/Korea_univerities.html')