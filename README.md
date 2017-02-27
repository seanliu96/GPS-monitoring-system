### 常量部分

ERVER_IP = "127.0.0.1"
SERVER_PORT = "8000"
SERVER_ROOT_URL = "http://" + SERVER_IP + ":" + SERVER_PORT

### API

- INDEX_API = SERVER_ROOT_URL + "/"

  主页地址，大家可以忽略

- LOGIN_API = SERVER_ROOT_URL + "/api/login"

  登陆的api，需要传入两个参数"user_name", "password"

  如果登录成功，返回"code" = 1和"id"=某个值，否则返回"code" = 0和"id" = -1

- REGISTER_API = SERVER_ROOT_URL + "/api/register"

  不实现

- GET_CARS_INFO_API = SERVER_ROOT_URL + "/api/get_cars_info"

  获得车的信息，需要传入参数"id"

  返回"code" = 1，并且返回"data"数组，数组的每个元素为{"id": row.CI_user_id, "SN": row.CI_SN, "SelfN": row.SelfN}，分别为车id、车牌号、车品牌

- GET_GPS_INFO_API = SERVER_ROOT_URL + "/api/get_gps_info"

  获得gps的信息，需要传入参数"begin_time"，"end_time"

  返回"code" = 1，并且返回"data"数组，数组的每个元素为{"lng": row.Longitude, "lat": row.Latitude, "id": row.MobileID, "time": row.RecvTime}，分别为纬度、经度、车id、时间

###数据库要用到的表格信息 

- 登陆、注册
  - dbo.UserInfo 用户权限表
    - User_Id 用户ID
    - User_Name 用户姓名
    - User_Pwd 用户密码
    - User_Type 用户类型
    - User_WatchRangeType 【UNKNOWN】
    - User_RangerList 【UNKNOWN】
    - User_CreateTime 创建时间
    - User_CanWebQuery 是否可以网页请求
    - IsForbidden 是否被禁
    - Subjection 隶属
    - UIF_Version1 版本-1
    - UIF_Version2 版本-2
    - UIF_Version3 版本-3
- 汽车信息
  - dbo.CarList【空表】
    - id
    - Mobile_Consumer ID
    - Mobile_ID
    - Mobile_Type
    - Mobile_Sim
    - Mobile_SN
    - Mobile_AddTag
    - Mobile_EditTag
    - CanWebQuery
    - CreateDate
    - Attribute
    - UpStr
    - Mobile_VehicleRegistration
    - Users
    - DelSign
  - dbo.CarList1 汽车列表
    - CI_ID id
    - CI_SN 汽车车牌号
    - CI_SelfN 车辆型号
    - CI_RunN 汽车载重、汽车座位
    - CI_CarID 汽车id
    - CI_RunType 汽车载重、汽车座位
    - CI_TypeN 车辆类型
    - CI_OutDate 【UNKNOWN】
    - CI_RunDate 【UNKNOWN】
    - CI_Miles 【UNKNOWN】
    - CI_TheoryOilCost 理论油耗
    - CI_CarryM 【UNKNOWN】
    - CI_TotalM 【UNKNOWN】
    - CI_Figure 【UNKNOWN】
    - CI_Driver 车辆驾驶员
    - CI_EngineType 引擎类型
    - CI_RatingPower 额定功率
    - CI_MaxWring 最大扭矩
    - CI_OilType 用油类型
    - CI_EngineN 引擎缸数
    - CI_BottomN 【UNKNOWN】
    - CI_OutLook 外观
    - CI_Memo 备忘
    - CI_Other1
    - CI_Other2
    - CreateTime
- GPS位置信息
  - dbo.Gpslog[YYYYMMDD] Gps日志表
    - GpsId 表id
    - MobileID 汽车id

