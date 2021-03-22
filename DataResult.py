import requests
from raspberry_GPIO import sevenSegment


def addData(circle_index, AnsData):
    answer = [0, 1, 2, 3, "ต้มยำ", "หม่าล่า", "ต้มยำ", "น้ำใส",
              "น้ำเงี้ยว", "น้ำยาป่า", "แห้งต้มยำ", "แห้งทรงเครื่อง", "แห้งยำพริกเผา", "เส้นมาม่า", "เส้นบะหมี่", "เส้นบะหมี่หยก", "เส้นราเมง",
              "เส้นเล็ก", "เส้นใหญ่", "ปกติ", "พิเศษ", "จัมโบ้", 1, 1, 1]
    # circle_index += 1
    # use for send data to web
    # circle No 1 - 25
    # print(circle_index + 1)
    # 1 - 4             => AnsDataSet[1]    : Spicy (0,1,2,3)
    if circle_index + 1 <= 4:
        AnsData[1] = circle_index
        return AnsData

    # 5 - 22            => AnsDataSet[0]    : Menu
    if circle_index + 1 <= 22:
        AnsData[0] = AnsData[0] + answer[circle_index]
        if circle_index + 1 <= 19:
            return AnsData

    # 20 - 22           => AnsDataSet[4]    : Price (45,60,100)
    if 20 <= circle_index + 1 <= 22:
        if circle_index + 1 == 22:
            AnsData[4] = 100
        elif circle_index + 1 == 21:
            AnsData[4] = 60
        else:
            AnsData[4] = 45

        return AnsData

    # 23                => AnsDataSet[2]    : Vegetable (กินผักมั้ย 1 คือกิน 0 คือไม่กิน)
    if circle_index + 1 == 23:
        AnsData[2] = 0
        return AnsData

    # 24 - 25           => AnsDataSet[3]    : Restaurant (กินที่ร้านมั้ย 1 คือ กินที่ร้าน 0 คือไม่)
    if 24 <= circle_index + 1 <= 25:
        if circle_index + 1 == 24:
            AnsData[3] = 0
        else:
            AnsData[3] = 1

        return AnsData

    return AnsData


# def addData_SQLite(AnsData):
#     # con = sqlite3.connect('DataMenu.sqlite')
#     con = sqlite3.connect('../WebNext JS/web/DataMenu.sqlite')
#     cursorObj = con.cursor().execute('SELECT * FROM Menu')
#     rows = cursorObj.fetchall()
#     # for row in rows:
#     #     print(row)
#     number = len(rows)+1
#     insertData = "INSERT INTO Menu VALUES( " + str(number) + ",'" + AnsData[0] + "'," + str(AnsData[1]) + "," + str(AnsData[2]) + "," + str(AnsData[3])+ "," + str(AnsData[4])+")"
#     cursorObj.execute(insertData)
#     con.commit()

#     return 0


def addData_SQLite(AnsData):

    # API
    URL = "http://localhost:3000/api/Menu"

    MenuId = requests.get(url = URL).json()
    if len(MenuId) == 0 :
        MenuId = 0
    
    else :
        MenuId = MenuId[ len(MenuId) - 1 ]['MenuId']
    
    sevenSegment(MenuId+1)

    # data = "{ AddMenu: { MenuId: " + str(MenuId) + ", Menu: " + AnsData[0] + ", Spicy: " + str(AnsData[1]) + ", Vegetable: " + str(AnsData[2]) + ", Restaurant: " + str(AnsData[3]) + ", Price: " + str(AnsData[4]) + "}}" 
    data = {'AddMenu':{'MenuId': MenuId + 1 , 'Menu': str(AnsData[0]), 'Spicy': AnsData[1], 'Vegetable': AnsData[2], 'Restaurant': AnsData[3], 'Price': AnsData[4]},'MeNu': { 'use' : 1 },'Today': { 'use' : 1 }}
    # data = json.dumps(data , ensure_ascii=False ).encode('utf-8')
    # print(data)

    # sending post request and saving response as response object
    r = requests.post( url=URL, json = data)
    print(r ,"success send data")

    # # extracting response text
    # pastebin_url = r.text
    # print("The pastebin URL is:%s" % pastebin_url)
    
    return 0
