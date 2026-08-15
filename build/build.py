# -*- coding: utf-8 -*-
import json, os
from urllib.parse import quote, quote_plus
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
with open(os.path.join(HERE, 'map_configs.json'), encoding='utf-8') as cfg_file:
    cfgs = json.load(cfg_file)
dims = {
 "Customs":[1062.4827,535.17401], "Woods":[1472.7926,1420.5995],
 "Shoreline":[1559.5717,1032.4935], "Factory":[130.81831,141.23242],
 "StreetsOfTarkov":[605.32395,831.57753], "GroundZero":[348.92543,488.44792],
 "Interchange":[1127.6852,947.02582], "Lighthouse":[1059.3752,1722.9499],
 "Reserve":[827.28742,761.16437],
}
import datetime
BUILD_VER = datetime.date.today().strftime('v%Y.%m.%d')
JP='https://wikiwiki.jp/eft/'; EN='https://escapefromtarkov.fandom.com/wiki/'
IMG='https://www.google.com/search?tbm=isch&q='
WIKI_MAP={'Customs':'Customs','Woods':'Woods','Shoreline':'Shoreline','Factory':'Factory',
 'StreetsOfTarkov':'Streets_of_Tarkov','GroundZero':'Ground_Zero','Interchange':'Interchange','Lighthouse':'Lighthouse','Reserve':'Reserve'}

# Interchange's source SVG already contains three separate vector groups. Crop
# the indoor exports to the mall so each floor fills the viewer instead of
# appearing as a small island in the middle of the outdoor map.
INTERCHANGE_FLOOR_CROPS = {
    'basement': (400, 100, 600, 760),
    'first': (400, 100, 600, 760),
    # The second-floor footprint is much smaller than the first floor. Give it
    # its own tighter viewport so it is readable at the same viewer size.
    'second': (460, 290, 500, 300),
}

def interchange_crop_pct(x, y, floor):
    crop_x, crop_y, crop_w, crop_h = INTERCHANGE_FLOOR_CROPS[floor]
    return (round((x / 100 * dims['Interchange'][0] - crop_x) / crop_w * 100, 2),
            round((y / 100 * dims['Interchange'][1] - crop_y) / crop_h * 100, 2))

def build_interchange_floor_assets():
    source_path = os.path.join(ROOT, 'map_Interchange.svg')
    with open(source_path, encoding='utf-8') as source_file:
        source = source_file.read()
    exports = {
        'Basement': ('basement', '#First_Floor,#Second_Floor{display:none}'),
        '1F': ('first', '#Second_Floor{display:none}'),
        '2F': ('second', '#First_Floor{display:none}'),
    }
    for suffix, (floor, rule) in exports.items():
        crop_x, crop_y, crop_w, crop_h = INTERCHANGE_FLOOR_CROPS[floor]
        floor_svg = source.replace('viewBox="0 0 1127.6852 947.02582"',
                                   f'viewBox="{crop_x} {crop_y} {crop_w} {crop_h}"', 1)
        floor_svg = floor_svg.replace('>', f'><style id="floor_filter">{rule}</style>', 1)
        with open(os.path.join(ROOT, f'map_Interchange_{suffix}.svg'), 'w', encoding='utf-8') as floor_file:
            floor_file.write(floor_svg)

build_interchange_floor_assets()

def make_pct(mk):
    cfg=cfgs[mk]; (x1,z1),(x2,z2)=cfg['bounds']
    if mk=='Factory.svg':
        return lambda x,z:(round((z1-z)/(z1-z2)*100,2), round((x-x2)/(x1-x2)*100,2))
    return lambda x,z:(round((x1-x)/(x1-x2)*100,2), round((z-z1)/(z2-z1)*100,2))

def anchor_pct(project, anchor):
    """Resolve either legacy game coordinates or exact image percentages."""
    if len(anchor) == 3 and anchor[0] == 'pct':
        return anchor[1], anchor[2]
    return project(*anchor)

ITEM_LINKS = {
 'MS2000マーカー':'MS2000_Marker','グリーンフレア':'RSP-30_reactive_signal_cartridge_(Green)',
 'Dorm room 220キー':'Dorm_room_220_key',"Company director's room key":"Company_director's_room_key",
 'Health Resort office key':'Health_Resort_office_key_with_a_blue_tape',
 'Pinewood hotel room 215 key':'Pinewood_hotel_room_215_key','Relaxation room key':'Relaxation_room_key',
 '6L31 60連':'AK-74_5.45x39_6L31_60-round_magazine','Ghostバラクラバ':'Ghost_balaclava',
 '緑シュマグ':'Shemagh_(Green)','RayBench':'RayBench_Hipster_Reserve_sunglasses',
 '丸フレームサングラス':'Round_frame_sunglasses','7.62x51パック':'7.62x51mm_M80_ammo_pack_(20_pcs)',
 '7.62x51弾パック':'7.62x51mm_M80_ammo_pack_(20_pcs)','ELCAN':'Elcan_SpecterDR_1x/4x_scope',
 'REAP-IR':'Trijicon_REAP-IR_thermal_scope','AUG':'Steyr_AUG_A3_5.56x45_assault_rifle',
 '6B43':'6B43_Zabralo-Sh_body_armor','Kiver-M':'Kiver-M_bulletproof_helmet',
 'M4A1':'Colt_M4A1_5.56x45_assault_rifle','Dorm room 314 marked key':'Dorm_room_314_marked_key','Kiba Arms外扉':'Kiba_Arms_International_outer_door_key','Kiba Arms内扉':'Kiba_Arms_inner_grate_door_key','Tarcone Director\'s officeキー':'Tarcone_Director\'s_office_room_key','HK MP5':'HK_MP5_9x19_submachine_gun_(Navy_3_Round_Burst)',
 'Object 11SR keycard':'Object_11SR_keycard','Object 14 keycard':'Object_14_keycard',
 'EMERCOM medical unit key':'EMERCOM_medical_unit_key','ULTRA medical storage key':'ULTRA_medical_storage_key',
}
def linkify(items):
    out = items
    for k in sorted(ITEM_LINKS, key=len, reverse=True):
        if k in out:
            out = out.replace(k, f'<a class="il" href="{EN}{quote(ITEM_LINKS[k])}" target="_blank" rel="noopener">{k}</a>')
    return out

EXTRACTS = {
 'Customs': [
  ('ZB-1011','常設(スポーンサイド依存)。西端の地下壕','a',(628,-131)),
  ('ZB-1012','条件: バンカーのランプ点灯時のみ','c',(465,-116)),
  ('ZB-1013','条件: W4のレバーで電源ON+Factory exit key','c',(206,-148)),
  ('Old Gas Station','条件付き(合図がある時)','c',(311,-186)),
  ('Crossroads','常設・両陣営共有。東端','a',(-350,-45)),
  ('Trailer Park','常設(サイド依存)。北東端','a',(-255,-245)),
  ('RUAF Roadblock','条件: ランプ点灯時のみ','c',(-42,-172)),
  ('Dorms V-EX','条件: 車両脱出 7,000RUB・最大4人','c',(200,199)),
  ("Smuggler's Boat",'条件: 焚き火点灯時のみ','c',(-80,80)),
  ('Railroad Passage','条件: グリーンフレアで開通','c',(212,-186)),
 ],
 'Woods': [
  ('Outskirts','常設(サイド依存)。南西の角','a',('pct',22.7,92.1)),
  ('UN Roadblock','常設(サイド依存)。南東の検問','a',('pct',84.5,87.3)),
  ('Northern UN Roadblock','常設(サイド依存)。東の道路沿い','a',('pct',86.8,64.5)),
  ('RUAF Gate / RUAF Roadblock','常設・両陣営。南の道路','a',('pct',52.5,93.8)),
  ('ZB-016','常設。東側・Eastern Rocks付近の地下壕','a',('pct',73.8,67.4)),
  ('ZB-014','条件: ZB-014キーが必要','c',('pct',16.6,73.0)),
  ('Bridge V-EX','条件: 車両脱出 5,000RUB。北東の川の橋','c',('pct',79.7,30.9)),
  ('Power Line Passage','条件: シグナルゾーン内で緑フレアを真上に発射','c',('pct',7.7,61.1)),
  ('Friendship Bridge','条件: PMCとScavの協力脱出。北の橋','c',('pct',40.5,6.8)),
  ('Railway Bridge to Tarkov','条件: 地雷原マップが必要。東の鉄道橋','c',('pct',93.4,74.0)),
 ],
 'Shoreline': [
  ('Tunnel','常設(サイド依存)。南西の海岸道路のトンネル','a',('pct',6.6,76.6)),
  ('Path to Lighthouse','常設+トランジット。北西エリア','a',('pct',5.7,38.6)),
  ('Road to Customs','常設(サイド依存)。東端の道路・川の手前','a',('pct',70.9,55.5)),
  ('Railway Bridge','常設。東端の鉄道橋','a',('pct',79.4,73.9)),
  ("Smuggler's Path",'条件: PMCとScavの協力。北東の桟橋','c',('pct',64.4,35.8)),
  ("Climber's Trail",'条件: Red Rebel+パラコード必要。北の崖の下','c',('pct',36.3,29.1)),
  ('Mountain Bunker','条件: 合言葉アイテム(Heartbeat)必要。北の崖の下','c',('pct',43.6,29.5)),
  ('Road to North V-EX','条件: 車両脱出 5,000RUB。北','c',('pct',54.6,26.9)),
  ('Pier Boat','条件: ボートがある時のみ。桟橋','c',('pct',41.5,95.0)),
 ],
 'Factory': [
  ('Gate 3','常設。北西側のゲート','a',('pct',13.2,12.2)),
  ('Cellars','条件: Factory emergency exit keyが必要','c',('pct',60.0,7.8)),
  ('Gate 0','条件: Factory emergency exit keyが必要','c',('pct',19.3,96.8)),
  ('Office Window','条件付き。オフィス3Fの窓','c',('pct',64.5,53.1)),
  ('Camera Bunker Door','地下トンネル側の脱出口','a',('pct',27.0,63.3)),
 ],
 'StreetsOfTarkov': [
  ('Expo Checkpoint','常設。北西','a',('pct',36.6,23.9)),
  ('Cardinal Apartment Parking','常設・両陣営。北端の駐車場','a',('pct',47.4,18.9)),
  ('Stylobate Building Elevator','常設。北東ビルの3Fエレベーター','a',('pct',65.9,22.2)),
  ('Klimov Shopping Mall Exfil','常設。モール1F','a',('pct',68.5,35.0)),
  ('Sewer River','常設。東側の川','a',('pct',76.1,57.8)),
  ('Damaged House','常設。東側','a',('pct',74.8,71.5)),
  ('Collapsed Crane','常設。西の工事現場','a',('pct',32.8,63.6)),
  ('Crash Site','常設。南西','a',('pct',30.4,77.6)),
  ('Klimov Street','条件: 緑フレアを指定エリアで真上へ発射。通りの東端','c',('pct',74.7,40.2)),
  ("Smuggler's Basement",'条件: 合言葉アイテム(Onyx)必要','c',('pct',45.1,37.3)),
  ('Pinewood Basement','条件: PMCとScavの協力','c',('pct',61.0,39.5)),
  ('Primorsky Ave Taxi V-EX','条件: 車両脱出 5,000RUB。南端','c',('pct',54.9,84.9)),
  ('Courtyard','条件: 緑スモークが無い時は閉鎖','c',('pct',65.7,89.9)),
 ],
 'GroundZero': [
  ('Nakatani Basement Stairs','常設。Nakataniビル地下階段','a',(-29,298)),
  ('Emercom Checkpoint','常設。西側の道路','a',(217,-26)),
  ('Mira Prospect','常設。北の大通り','a',(26,-61)),
  ('Police Checkpoint','常設。中央北の検問','a',(120,262)),
 ],
 'Interchange': [
  ('Railway','常設(サイド依存)。北西の線路側','a',('pct',4.9,5.5)),
  ('Emercom Checkpoint','常設(サイド依存)。南東の道路','a',('pct',93.2,85.0)),
  ('Power Station V-EX','条件: 車両脱出・支払い。北東','c',('pct',84.0,16.0)),
 ],
 'Lighthouse': [
  ('Northern Checkpoint','常設。北端・トレインヤード西の道路','a',('pct',37.8,10.3)),
  ('Southern Road','常設。南東の海岸道路','a',('pct',71.7,82.7)),
  ('Path to Shoreline','常設・両陣営。東側中央の山道','a',('pct',71.5,54.0)),
  ('Road to Military Base','常設系。北東の道路','a',('pct',77.8,20.2)),
  ('Mountain Pass','条件: Red Rebel+パラコード必要。山道','c',('pct',53.2,62.6)),
  ('Side Tunnel','条件: Scav友好時など。中央南のトンネル','c',('pct',48.7,77.5)),
  ('Armored Train','条件: 装甲列車の到着時刻のみ','c',('pct',46.6,17.6)),
 ],
 'Reserve': [
  ('Armored Train','条件: 列車到着時のみ','c',('pct',13.2,27.0)),
  ('Bunker Hermetic Door','条件: レバー操作後、サイレン作動中','c',('pct',61.4,9.0)),
  ('Cliff Descent','条件: Red Rebel+パラコード、アーマーベスト不可','c',('pct',38.0,90.0)),
  ('D-2','条件: 地下司令部で電源を入れて扉ボタンを押す','c',('pct',94.0,38.0)),
  ('Exit to Woods','条件: Minefield map (Reserve)が必要','c',('pct',22.6,11.5)),
  ('Scav Lands (Co-Op)','条件: PMCとScavの協力脱出','c',('pct',39.0,11.0)),
  ('Sewer Manhole','条件: バックパック装備不可','c',('pct',29.0,61.0)),
 ],
}
SCAV_EX = {
 'Customs': [('Factory Shacks',(352,-18)),('Warehouse 4',(333,-50)),('Old Road Gate',(255,218)),('Sniper Roadblock',(145,180)),('Railroad to Port',(-140,-30)),('Railroad to Tarkov',(-160,-230)),('Administration Gate',(655,-40)),('Military Base CP',(585,205)),('Passage Between Rocks',(622,222))],
 'Woods': [('Scav Bunker(北西)',('pct',30.8,19.6)),('Scav House(南西)',('pct',18.2,83.1)),('The Boat(湖岸)',('pct',35.0,82.0)),("Dead Man's Place",('pct',34.0,84.0)),('Mountain Stash(両陣営)',('pct',61.0,52.0)),('Eastern Rocks',('pct',84.0,65.0)),('Old Railway Depot',('pct',84.0,77.0))],
 'Shoreline': [('Ruined Road(南西・Tunnelのすぐ南)',('pct',5.0,79.0)),('RWing Gym Entrance(リゾート)',('pct',49.0,39.0)),('Admin Basement(リゾート)',('pct',38.0,38.0)),('Lighthouse(南の灯台)',('pct',50.0,95.0))],
 'Factory': [('Camera Bunker Door',('pct',27.0,63.3))],
 'StreetsOfTarkov': [('Near Kamchatskaya Arch(西)',('pct',34.7,40.8)),('Sewer Manhole',('pct',27.8,72.8)),('Ventilation Shaft',('pct',61.4,85.3)),('Entrance to Catacombs(東)',('pct',80.2,61.6))],
 'GroundZero': [('Scav Checkpoint',(217,140))],
 'Interchange': [('Scav Camp(西の駐車場)',('pct',28.0,48.0)),('Hole in the Fence(東)',('pct',81.0,47.0))],
 'Lighthouse': [('Scav Hideout at the Grotto(西海岸)',('pct',21.0,36.0)),('Industrial Zone Gates',('pct',52.0,21.0)),('Hideout under the Landing Stage(南西海岸)',('pct',25.0,74.0)),('South Road Landside',('pct',74.0,84.0))],
 'Reserve': [('Heating Pipe',('pct',29.0,15.0)),('Checkpoint Fence',('pct',29.0,75.0)),('Depot Hermetic Door',('pct',58.0,32.0)),('Hole in the Wall by the Mountains',('pct',57.0,57.0))],
}
SCAV_EX['Factory'] = [('Camera Bunker Door',('pct',27.0,63.3))]
LOOT = {
 'Customs': [('寮(マークドルーム/金庫)','鍵部屋と金庫。PvP多め','任意: Dorm room 314 marked key(高額)/203・214等の寮キー',(205,150)),('Big Red事務所','PC・インテリ書類・重役室','Tarcone Director\'s officeキー(奥はドア破壊可)',(-215,-119)),('新ガソスタ','レジ・医療・キー湧き','鍵不要',(404,31)),('旧ガソスタ2F','USECスタッシュ・武器','鍵不要',(331,-173)),('Fortress','武器箱多数+スカブ湧き','鍵不要',(201,-127))],
 'Woods': [('製材所','木箱多数+シュトゥルマンのレアキー','鍵不要',(10,-3)),('USEC Camp','武器・ミリタリー系','鍵不要',(290,-475)),('Convoy','車列・ミリタリールート','鍵不要',(200,-606)),('Scav House周辺','ジャケット・雑貨','鍵不要',(413.7,242.2))],
 'Shoreline': [('リゾート東西棟','鍵部屋にLEDX等の医療レア','要: 各部屋キー(216/226/321など。西321・東226が定番)',(-258.2,-71.2)),('Village','ツールボックス・工業系','鍵不要',(418.4,118)),('Gas Station','レジ・医療','鍵不要(事務所は鍵)',(-189.3,420)),('Scav Island','武器箱・スタッシュ','鍵不要',(216,424))],
 'Factory': [('オフィス','金庫・ファイルキャビネット','一部Factory系キー(メインは鍵不要)',(21,39)),('Rafters(3F通路)','武器箱','鍵不要',(18,4)),('Med Tent','医療系','鍵不要',(-18,-29))],
 'StreetsOfTarkov': [('Kilmovモール','店舗ルート広範囲','鍵不要',(-128,-35)),('LERM Expo','カバンのレアドロップ+車部品','鍵不要',(239,-60)),('Lexos','車部品・工業','一部部屋キーあり',(66,305)),('Cinema','雑貨・金策','鍵不要',(-175,400)),('Pinewoodホテル','鍵部屋多数','要: Pinewood各部屋キー(215など)',(-35,64))],
 'GroundZero': [('TerraGroup本社','インテリ・オフィスルート','一部オフィスキー',(-50,0)),('Tarbank','金庫・金策','一部キー(金庫室)',(43,150))],
 'Interchange': [],
 'Lighthouse': [('浄水場','高級ルート(ローグ注意)','鍵不要エリア多め',(-65,-600)),('Cottages','金庫・レア','要: コテージ各キー',(-162,-225)),('Train Yard','工業・武器','鍵不要',(-30,-882)),('VPX候補: Southern Villa / Hillside / 浄水場','VPX・Virtex・COFDM系の軍用電子品スポーン','一部キー部屋あり',(-151,-243))],
 'Reserve': [('White Kingサーバー','VPXなど軍用電子品のルーズルート','鍵不要',(-49.5,15.5)),('D-2サーバー室','VPX・COFDM・Virtex候補','電源投入・待ち伏せ注意',('pct',69.3,81.7)),('RB-PKPTS','VPXの有力候補。鍵部屋','RB-PKPTS key',('pct',70.0,30.0))],
}

# Streets scav money-run overlay. Coordinates are percentages on the
# tarkov.dev Streets SVG and intentionally use broad landmark centers.
STREETS_SCAV_SPOTS = [
 ('safe','Expo / LERM裏','工具箱・ダッフル・棚を短時間で確認。北西端で退路を作りやすい','鍵不要',('pct',18.0,24.0)),
 ('valuable','Cardinal Apartments','室内の貴重品湧き、引き出し、ジャケット。窓際を長く横切らない','鍵不要',('pct',36.5,27.0)),
 ('body','Cardinal北の死体','道路側のスカブ死体候補。周囲を確認してから漁る','鍵不要',('pct',39.5,20.0)),
 ('safe','Beluga裏～北モール','食料・工具・バッグを拾い、表通りを避けて建物沿いに移動','鍵不要',('pct',62.0,30.0)),
 ('valuable','Pinewood / Basement周辺','引き出し・バッグ・ルーズ品が密集。ホテル内の足音に注意','一部部屋は鍵',('pct',60.0,43.5)),
 ('body','Pinewood南の路上死体','道路脇の死体候補。開けた交差点なので短時間で確認','鍵不要',('pct',58.0,50.0)),
 ('safe','Post Office裏','引き出し・バッグ・日用品。建物内をつないで南へ抜けやすい','鍵不要',('pct',46.5,47.5)),
 ('safe','Construction / Collapsed Crane','工具箱・技術箱・建築資材。外周側から入って外周へ戻る','鍵不要',('pct',16.0,70.0)),
 ('body','Concordia西の死体','壁際の死体候補。中央道路から射線が通るので先に音を確認','鍵不要',('pct',25.0,76.0)),
 ('valuable','Concordia / Sparja','地下・店舗の工具、バッグ、食料、ルーズ品。部屋を欲張りすぎない','一部部屋は鍵',('pct',31.0,77.0)),
 ('safe','Family Market裏','食料・飲料・ジャケット。南東側の脱出へ寄せやすい','鍵不要',('pct',86.5,72.0)),
 ('valuable','Cinema裏～Ventilation','バッグ・工具・ルーズ品。Ventilation Shaft方面へ離脱しやすい','鍵不要',('pct',79.0,85.0)),
]

STREETS_SCAV_ROUTES = [
 ('北コース','#ff6a2a',[(18,24),(36.5,27),(47,31),(62,30),(60,43.5),(46.5,47.5)]),
 ('南コース','#31c9e8',[(2.5,84),(16,70),(25,76),(31,77),(48,82),(68,88),(79,85),(86.5,72)]),
]

INTERCHANGE_FLOOR_NAMES = {'basement':'地下駐車場','first':'1階','second':'2階'}
INTERCHANGE_LABEL_FLOORS = {
 'overview': {'Power Station','Go Kart','Four Camp','Cargo Containers','Wall Break','Oli Tower','Idea Tower','Scav Camp','Highway Construction'},
 'basement': {'Ramps','Garage A','Garage B','Garage C','Garage D'},
 'first': {'IDEA','Goshan','OLI','Nortex','TRend','Mode7','TTS','Book Store','Dino Clothes','EMERCOM','Kostin','Bizarro','Spiel','Voyage','Viking','Mantis','German','The National','Brutal','Kiba','Pretty Lights','Telespot','Revis','ADIK','Generic','Top Brand','Sports','Yushka','Rasmussen','Avokado','Boots 4 Life','Texho','Dom'},
 'second': {'Father & Sons','Tarkovstar','Eastland','Arena','ТАРЗДРАВ','МЕБЕЛЬ МК','Intourist','Burger Spot','FCK','McDaniels','Tarducks','Coffee Joy','Jacob & Jacob','ПУШКИН','Sushi Huyushi','Underway','Burger House','Philly Cute','Shiccos','МУЗЕЙ ИСТОРИИ','Papillon','ЗАКРЫТО НА РЕМОНТ','НА-СВЯЗИ','СКОРО ОТКРЫТИЕ','Figaro','АПТЕКА','SARA','Urban Clothes','TECHLIGHT','Fashion Store'},
}

# floor, risk, name, description, requirement, SVG/game anchor
INTERCHANGE_FLOOR_LOOT = [
 ('basement','steady','Garage A（IDEA下）','武器箱・工具箱・ダッフルを拾いながら北側ランプへ抜ける。中央より射線が短め','鍵不要',(33,-222)),
 ('basement','steady','Garage B / C','柱沿いの武器箱・工具箱・ダッフル。暗所なのでライトと音を優先','鍵不要',(30,-35)),
 ('basement','steady','Garage D（OLI下）','工具・工業品・武器箱を確認してOLI側ランプへ。SCAVの帰路に組み込みやすい','鍵不要',(20,138)),
 ('basement','valuable','Saferoom / Object 14方面','コンテナ・武器系の高額候補。電源とキーカード条件があり、待ち伏せに注意','Object 11SR keycard / Object 14 keycard',('pct',58.0,57.5)),
 ('first','steady','IDEA事務所・倉庫','PCブロック、工具、家電、貴重品候補。正面入口より裏通路から入ると比較的安全','鍵不要',(-34,-235)),
 ('first','steady','Goshan食料棚・裏倉庫','食料を大量確保しつつ、裏側の武器箱・工具箱を確認','鍵不要',(-115,-45)),
 ('first','steady','OLI裏棚・事務所','水フィルター、モーター、燃料など隠れ家用の工業品とPCブロック','鍵不要',(-28,140)),
 ('first','valuable','Rasmussen / Texho','GPU・テトリスなど電子部品候補。短時間で棚を見て上階の射線から離れる','鍵不要',(40,38)),
 ('first','danger','KIBA Arms','武器・アタッチメントの高額部屋。電源と2本の鍵が必要で中央モールの激戦地','Kiba Arms外扉 + Kiba Arms内扉',(-18,-25)),
 ('first','valuable','Mantis / EMERCOM','医療品、注射器、LEDX候補。EMERCOM側は鍵が必要','EMERCOM medical unit key（Mantisは鍵不要）',(15,-85)),
 ('second','valuable','TECHLIGHT','GPU・テトリス・電子部品の最重要候補。開幕は特に激戦','鍵不要',(91,54)),
 ('second','danger','ULTRA Medical Storage','LEDX・高級医療品候補。電源投入後に開錠でき、Techlight前で非常に危険','ULTRA medical storage key',(54,-128)),
 ('second','steady','薬局 / TARZDRAV','医療品と消耗品。Techlightへ直行せず周辺店舗を拾う安定寄りルート','鍵不要',(71,-128)),
 ('second','steady','フードコート / Burger Spot','レジ・食料・ダッフルを確認。中央吹き抜けの射線を切りながら移動','鍵不要',(-27,-103)),
]

EXTRA_EXNOTE = {
 'StreetsOfTarkov':'Streetsは脱出が多く位置の個体差も大きい。上記は代表例+目安。必ずOキー2連打で自分のリストを確認。',
 'Interchange':'他にRailway・Emercom Checkpoint・Saferoom(条件)などあり。位置はOキー2連打で確認。',
 'Lighthouse':'他にSide Tunnel等あり。ローグ地帯(浄水場)を通るルートは注意。',
 'GroundZero':'他にScav側共有の脱出あり。',
 'Reserve':'D-2は待ち伏せが多い。Armored TrainとHermetic Doorは作動条件を必ず確認。',
}

# Marker percentages derived from tarkov.dev's current world-coordinate data
# and the matching SVG transforms. These override the old raster-map positions.
EXTRACT_PIN_PCT = {
 'Customs': {
  'ZB-1011':(7.1,32.8), 'ZB-1012':(21.9,35.8), 'ZB-1013':(46.5,28.3),
  'Old Gas Station':(36.3,24.4), 'Crossroads':(96.5,40.3), 'Trailer Park':(94.6,13.6),
  'RUAF Roadblock':(66.2,31.0), 'Dorms V-EX':(48.3,95.6), "Smuggler's Boat":(69.1,79.0),
  'Railroad Passage':(52.2,1.0),
 },
 'Woods': {
  'Outskirts':(21.1,93.8), 'UN Roadblock':(84.0,88.6), 'Northern UN Roadblock':(85.5,62.5),
  'RUAF Gate / RUAF Roadblock':(56.0,99.0), 'ZB-016':(73.6,68.2), 'ZB-014':(14.1,71.6),
  'Bridge V-EX':(80.4,30.2), 'Power Line Passage':(5.1,61.1), 'Friendship Bridge':(39.3,5.2),
  'Railway Bridge to Tarkov':(97.8,76.9),
 },
 'Shoreline': {
  'Tunnel':(8.2,71.1), 'Path to Lighthouse':(3.5,15.5), 'Road to Customs':(87.4,40.2),
  'Railway Bridge':(98.3,70.0), "Smuggler's Path":(79.1,15.5), "Climber's Trail":(46.0,5.2),
  'Mountain Bunker':(57.4,2.8), 'Road to North V-EX':(67.1,3.4), 'Pier Boat':(53.6,94.5),
 },
 'Factory': {
  'Gate 3':(3.1,13.0), 'Cellars':(73.1,2.2), 'Gate 0':(8.7,98.7),
  'Office Window':(20.9,41.5), 'Camera Bunker Door':(20.7,65.1),
 },
 'StreetsOfTarkov': {
  'Expo Checkpoint':(18.2,23.0), 'Cardinal Apartment Parking':(36.2,16.2),
  'Stylobate Building Elevator':(61.0,26.9), 'Klimov Shopping Mall Exfil':(80.7,35.0),
  'Sewer River':(97.9,62.2), 'Damaged House':(94.9,77.3), 'Collapsed Crane':(17.7,68.6),
  'Crash Site':(1.7,84.8), 'Klimov Street':(97.2,40.9), "Smuggler's Basement":(41.0,41.7),
  'Pinewood Basement':(72.5,43.5), 'Primorsky Ave Taxi V-EX':(53.9,91.4), 'Courtyard':(78.3,96.1),
 },
 'GroundZero': {
  'Nakatani Basement Stairs':(76.2,94.1), 'Emercom Checkpoint':(28.0,5.4),
  'Mira Prospect':(8.8,17.5), 'Police Checkpoint':(77.2,49.0),
 },
 'Interchange': {
  'Railway':(12.2,1.4), 'Emercom Checkpoint':(89.2,81.7), 'Power Station V-EX':(82.4,8.6),
 },
 'Lighthouse': {
  'Northern Checkpoint':(37.9,0.5), 'Southern Road':(76.5,82.3), 'Path to Shoreline':(83.0,50.9),
  'Road to Military Base':(79.6,12.4), 'Mountain Pass':(64.8,57.6), 'Side Tunnel':(55.0,76.4),
  'Armored Train':(48.0,7.2),
 },
 'Reserve': {
  'Armored Train':(24.3,23.2), 'Bunker Hermetic Door':(38.4,15.3), 'Cliff Descent':(50.4,88.4),
  'D-2':(69.3,81.7), 'Exit to Woods':(42.6,9.6), 'Scav Lands (Co-Op)':(70.4,24.1),
  'Sewer Manhole':(42.0,64.2),
 },
}

SCAV_PIN_PCT = {
 'Customs': {
  'Factory Shacks':(46.0,57.0), 'Warehouse 4':(33.3,51.7), 'Old Road Gate':(48.2,95.8),
  'Sniper Roadblock':(63.8,79.6), 'Railroad to Port':(79.2,65.0), 'Railroad to Tarkov':(80.5,16.5),
  'Administration Gate':(2.5,46.4), 'Military Base CP':(5.0,79.8), 'Passage Between Rocks':(14.8,93.3),
 },
 'Woods': {
  'Scav Bunker(北西)':(30.2,15.4), 'Scav House(南西)':(16.5,85.3), 'The Boat(湖岸)':(33.4,83.3),
  "Dead Man's Place":(32.0,86.5), 'Mountain Stash(両陣営)':(60.9,51.7), 'Eastern Rocks':(82.1,64.8),
  'Old Railway Depot':(82.7,78.4),
 },
 'Shoreline': {
  'Ruined Road(南西・Tunnelのすぐ南)':(8.8,72.4), 'RWing Gym Entrance(リゾート)':(51.3,30.4),
  'Admin Basement(リゾート)':(48.8,25.7), 'Lighthouse(南の灯台)':(61.7,95.1),
 },
 'Factory': {'Camera Bunker Door':(20.7,65.1)},
 'StreetsOfTarkov': {
  'Near Kamchatskaya Arch(西)':(10.5,41.6), 'Sewer Manhole':(7.8,77.4),
  'Ventilation Shaft':(74.2,86.9), 'Entrance to Catacombs(東)':(94.9,65.2),
 },
 'GroundZero': {'Scav Checkpoint':(64.3,9.1)},
 'Interchange': {'Scav Camp(西の駐車場)':(31.0,47.4), 'Hole in the Fence(東)':(79.3,46.7)},
 'Lighthouse': {
  'Scav Hideout at the Grotto(西海岸)':(31.5,29.7), 'Industrial Zone Gates':(63.0,11.8),
  'Hideout under the Landing Stage(南西海岸)':(36.0,74.6), 'South Road Landside':(75.1,82.3),
 },
 'Reserve': {
  'Heating Pipe':(54.8,17.2), 'Checkpoint Fence':(38.3,74.8),
  'Depot Hermetic Door':(28.4,28.1), 'Hole in the Wall by the Mountains':(93.0,59.1),
 },
}

MAP_JA={'Customs':'CUSTOMS','Woods':'WOODS','Shoreline':'SHORELINE','Factory':'FACTORY','StreetsOfTarkov':'STREETS','GroundZero':'GROUND ZERO','Interchange':'INTERCHANGE','Lighthouse':'LIGHTHOUSE','Reserve':'RESERVE'}

# User's current Factory tasks (checked against the live tarkov.dev task pages).
# Marks use percentage coordinates on the RE3MR Factory 1.7C composite interior map.
FACTORY_TASKS=[
 ('scout','Scout','Mechanic','4脱出口（Gate 0 / Gate 3 / Cellars / Med Tent Gate）を訪問し、生還する。','Factory emergency exit key（施錠出口用）を持参推奨','固定地点あり'),
 ('postman-pat-part-1','Postman Pat - Part 1','Prapor','地下バンカーの死亡した配達人から手紙を回収し、生還する。手紙はTherapistへ渡す。','鍵不要。死亡するとクエスト品を失う','固定地点あり'),
 ('stirrup','Stirrup','Skier','Factoryでピストルを使い、任意の敵を10人倒す。','任意のピストル＋予備弾','Factory全域'),
 ('sanitary-standards-part-1','Sanitary Standards - Part 1','Therapist','レイド内発見のGas analyzerを1個入手し、Therapistへ渡す。','Gas analyzer（FIR）×1','固定地点なし'),
 ('chemical-part-3','Chemical - Part 3','Skier','Factory上層の事務所で薬品入り注射器を回収し、Skierへ渡す。','鍵不要。死亡するとクエスト品を失う','固定地点あり'),
 ('dragnet','Dragnet','Jaeger','地下のTerraGroup倉庫からchemical containerを回収し、Jaegerへ渡す。','TerraGroup storage room keycard（Polikhim）必須','固定地点あり'),
 ('the-good-times-part-1','The Good Times - Part 1','Prapor','6B43アーマーとKiver-Mヘルメットを装備してFactoryでPMCを5人倒す。','6B43＋Kiver-M（武器指定なし）','Factory全域'),
 ('black-swan','Black Swan','Mechanic','地下トンネルの熱交換器をMS2000でマークする。候補3地点を表示。','MS2000 Marker（安全のため3個を特殊スロットへ）','固定地点あり'),
 ('one-way-ticket','One-Way Ticket','Peacekeeper','FactoryでSteyr AUGを使い、任意の敵をヘッドショットで15人倒す。','AUG A1 / A3＋予備弾','Factory全域'),
 ('exit-here','Exit Here','Skier','Courtyard Gate（main exit）から「生還」判定で脱出する。','鍵不要。ランスルーは不可','固定地点あり'),
]
FACTORY_TASK_MARKS=[
 ('scout','Gate 0',55.2,55.5),('scout','Gate 3',59.0,29.0),('scout','Cellars',58.2,19.0),('scout','Med Tent Gate',70.8,52.0),
 ('postman-pat-part-1','配達人の遺体',55.4,43.5),('chemical-part-3','薬品入り注射器',17.0,31.0),
 ('dragnet','TerraGroup倉庫',84.0,48.0),
 ('black-swan','熱交換器 A',82.0,35.0),('black-swan','熱交換器 B',88.0,46.0),('black-swan','熱交換器 C',93.0,56.0),
 ('exit-here','Courtyard Gate',55.0,29.0),
]

modal_data={}  # id -> dict
sections=[]; tabs=[]
for mkey in MAP_JA:
    p=make_pct(mkey+'.svg')
    labelpins=[]; building_labelpins=[]; building_pins=[]
    for (lx,lz),label,size in cfgs[mkey+'.svg'].get('labels',[]):
        x,y=p(lx,lz)
        floor_attr=''
        floor_hidden=''
        if mkey == 'Interchange':
            floor=next((key for key,names in INTERCHANGE_LABEL_FLOORS.items() if label in names), 'basement')
            if floor == 'overview':
                labelpins.append(f'<span class="labelpin" style="left:{x}%;top:{y}%">{label}</span>')
            else:
                x,y=interchange_crop_pct(x,y,floor)
                floor_attr=f' data-floor="{floor}"'
                floor_hidden='' if floor == 'first' else ' hid'
                building_labelpins.append(f'<span class="labelpin{floor_hidden}"{floor_attr} style="left:{x}%;top:{y}%">{label}</span>')
            continue
        labelpins.append(f'<span class="labelpin" style="left:{x}%;top:{y}%">{label}</span>')
    scavloot=[]; scavrows=[]; route_svg=''; scav_toggle=''
    if mkey == 'StreetsOfTarkov':
        route_parts=[]
        for route_name,color,points in STREETS_SCAV_ROUTES:
            pts=' '.join(f'{x},{y}' for x,y in points)
            route_parts.append(f'<polyline points="{pts}" style="--route:{color}"/>')
            scavloot.append(f'<span class="scavloot slroute-label hid" style="left:{points[2][0]}%;top:{points[2][1]-3}%;--route:{color}">{route_name}</span>')
        route_svg=f'<svg class="scavloot scavroute hid" viewBox="0 0 100 100" preserveAspectRatio="none">{"".join(route_parts)}</svg>'
        kind_label={'safe':'比較的安全','valuable':'高額候補','body':'死体候補'}
        kind_mark={'safe':'安','valuable':'★','body':'骸'}
        for j,(kind,name,desc,key,anchor) in enumerate(STREETS_SCAV_SPOTS,1):
            sid=f'{mkey}_sl{j}'
            x,y=anchor_pct(p,anchor)
            q=quote_plus(f'Escape from Tarkov Streets of Tarkov {name} loot')
            modal_data[sid]={'title':f'SCAV金策: {name}','sub':kind_label[kind],'place':'StreetsOfTarkov','desc':desc,
              'items':key,'img':IMG+q,'map':mkey,'wl':'https://www.tarkov.dev/map/streets-of-tarkov',
              'wt':'🗺 tarkov.devのStreetsマップ','pt':'scavloot','pn':kind_mark[kind],'x':x,'y':y}
            scavloot.append(f'<button class="pin scavloot slpin sl-{kind} hid" style="left:{x}%;top:{y}%" data-m="{sid}"><span class="sldot">{kind_mark[kind]}</span><span class="sllbl">{name}</span></button>')
            scavrows.append(f'<div class="exrow slrow slrow-{kind}"><span class="exbadge slbadge-{kind}">{kind_label[kind]}</span><b>{name}</b> — {desc}<br><small>{key}</small></div>')
        scav_toggle='<button class="mbtn tgl" data-g="scavloot"><i class="sw" style="--c:#35d6f2"></i>SCAV金策</button>'
    expins=[]; exrows=[]
    for j,(ename,method,etype,anchor) in enumerate(EXTRACTS.get(mkey,[]),1):
        anchor=('pct', *EXTRACT_PIN_PCT[mkey][ename])
        eid=f'{mkey}_e{j}'
        cls='exa' if etype=='a' else 'exc'
        tag='常設' if etype=='a' else '条件'
        q=quote_plus(f'Escape from Tarkov {mkey} {ename} extraction')
        modal_data[eid]={'title':f'PMC脱出: {ename}','sub':('常設脱出' if etype=='a' else '条件付き/ランダム脱出'),'place':mkey,'desc':method,'items':'','img':IMG+q,'map':mkey,
          'wl':EN+WIKI_MAP[mkey]+'#Extractions','wt':f'🖼 wikiの{mkey} 脱出セクション(写真あり)','pt':('exa' if etype=='a' else 'exc'),'pn':'EX'}
        if anchor:
            x,y=anchor_pct(p, anchor)
            modal_data[eid]['x']=x; modal_data[eid]['y']=y
            lbl = f'<span class="exlbl{'' if etype=='a' else ' exlblc'}">{ename}</span>'
            expins.append(f'<button class="pin {'exapin' if etype=='a' else 'excpin'}" style="left:{x}%;top:{y}%" data-m="{eid}"><span class="exdot {cls}">EX</span>{lbl}</button>')
        exrows.append(f'<div class="exrow {cls}r"><span class="exbadge {cls}">{tag}</span><b>{ename}</b> — {method}</div>')
    for j,(ename,anchor) in enumerate(SCAV_EX.get(mkey,[]),1):
        anchor=('pct', *SCAV_PIN_PCT[mkey][ename])
        sid=f'{mkey}_s{j}'
        q=quote_plus(f'Escape from Tarkov {mkey} {ename} scav extraction')
        modal_data[sid]={'title':f'SCAV脱出: {ename}','sub':'スカブ専用/共有脱出(位置は目安)','place':mkey,'desc':'スカブで出た時の脱出候補。リストはOキー2連打で確認','items':'','img':IMG+q,'map':mkey,
          'wl':EN+WIKI_MAP[mkey]+'#Extractions','wt':f'🖼 wikiの{mkey} 脱出セクション(写真あり)','pt':'scav','pn':'S'}
        if anchor:
            x,y=anchor_pct(p, anchor)
            modal_data[sid]['x']=x; modal_data[sid]['y']=y
            expins.append(f'<button class="pin scavpin hid" style="left:{x}%;top:{y}%" data-m="{sid}"><span class="exdot exs">S</span><span class="exlbl exlbls">{ename}</span></button>')
    lootrows=[]
    if mkey == 'Interchange':
        risk_label={'steady':'安定','valuable':'高額','danger':'激戦'}
        for j,(floor,risk,lname,ldesc,lkey,anchor) in enumerate(INTERCHANGE_FLOOR_LOOT,1):
            lid=f'{mkey}_fl{j}'
            x,y=anchor_pct(p,anchor)
            x,y=interchange_crop_pct(x,y,floor)
            q=quote_plus(f'Escape from Tarkov Interchange {lname} loot')
            modal_data[lid]={'title':f'{INTERCHANGE_FLOOR_NAMES[floor]}金策: {lname}',
              'sub':f'{risk_label[risk]}スポット','place':f'Interchange / {INTERCHANGE_FLOOR_NAMES[floor]}',
              'desc':ldesc,'items':linkify(lkey),'img':IMG+q,'map':mkey,
              'wl':'https://www.tarkov.dev/map/interchange','wt':'🗺 tarkov.devのInterchangeマップ',
              'pt':'loot','pn':'$','x':x,'y':y}
            building_pins.append(f'<button class="pin lootpin flpin fl-{risk} hid" data-floor="{floor}" style="left:{x}%;top:{y}%" data-m="{lid}"><span class="sldot">$</span><span class="sllbl">{lname}</span></button>')
            row_hidden='' if floor == 'first' else ' hid'
            lootrows.append(f'<div class="exrow floor-list flrow flrow-{risk}{row_hidden}" data-floor="{floor}"><span class="exbadge flbadge-{risk}">{INTERCHANGE_FLOOR_NAMES[floor]}・{risk_label[risk]}</span><b>{lname}</b> — {ldesc}<br><small>条件: {linkify(lkey)}</small></div>')
    for j,(lname,ldesc,lkey,anchor) in enumerate(LOOT.get(mkey,[]),1):
        lid=f'{mkey}_l{j}'
        q=quote_plus(f'Escape from Tarkov {mkey} {lname} loot')
        modal_data[lid]={'title':f'金策: {lname}','sub':'アイテム漁りスポット','place':mkey,'desc':ldesc,'items':linkify(lkey),'img':IMG+q,'map':mkey,
          'wl':EN+WIKI_MAP[mkey],'wt':f'🖼 wikiの{mkey} マップページ','pt':'loot','pn':'$'}
        x,y=anchor_pct(p, anchor)
        modal_data[lid]['x']=x; modal_data[lid]['y']=y
        expins.append(f'<button class="pin lootpin hid" style="left:{x}%;top:{y}%" data-m="{lid}"><span class="exdot exl">$</span></button>')
        lootrows.append(f'<div class="exrow lootr"><span class="exbadge exl2">$</span><b>{lname}</b> — {ldesc}<br><small>鍵: {linkify(lkey)}</small></div>')
    taskrows=[]; task_toggle=''
    if mkey == 'Factory':
        task_by_slug={}
        for j,(slug,tname,trader,objective,need,kind) in enumerate(FACTORY_TASKS,1):
            tid=f'Factory_t{j}'; task_by_slug[slug]=tid
            task_url=('https://escapefromtarkov.fandom.com/wiki/Sanitary_Standards_-_Part_1' if slug=='sanitary-standards-part-1' else f'https://tarkov.dev/task/{slug}')
            wiki_url=f'https://escapefromtarkov.fandom.com/wiki/{quote(tname.replace(" ", "_"))}'
            modal_data[tid]={'title':f'TASK: {tname}','sub':f'{trader} / {kind}','place':'Factory',
              'desc':objective,'items':f'<b>必要:</b> {need}','img':IMG+quote_plus(f'Escape from Tarkov {tname} Factory quest'),
              'map':mkey,'wl':task_url,'wt':f'✓ {tname}のデータを確認','pt':'task','pn':'Q'}
            taskrows.append(f'<div class="exrow taskrow"><span class="exbadge taskbadge">Q</span><b>{tname}</b> <small>{trader}・{kind}</small><br>{objective}<br><small><b>必要:</b> {need}</small><span class="tasklinks"><a class="tasklink" href="{task_url}" target="_blank" rel="noopener">現行条件</a><a class="tasklink wiki" href="{wiki_url}" target="_blank" rel="noopener">WIKI</a></span></div>')
        for slug,mark,x,y in FACTORY_TASK_MARKS:
            tid=task_by_slug[slug]
            building_pins.append(f'<button class="pin taskpin" style="left:{x}%;top:{y}%" data-m="{tid}"><span class="taskdot">Q</span><span class="sllbl tasklbl">{mark}</span></button>')
        task_toggle='<button class="mbtn tgl on" data-g="taskpin"><i class="sw sq" style="--c:#b76cff"></i>タスク</button>'
    exnote=EXTRA_EXNOTE.get(mkey,'')
    W,H=dims[mkey]
    map_ratio=f'{W}/{H}'
    map_image=f'<img loading="lazy" src="map_{mkey}.svg" alt="{mkey}">'
    building_html=''
    building_specs={
      'Customs':('寮内部（2階建て・3階建て）','interior_Customs_Dorms.webp','4000/4561','RE3MR Customs Dorms 2D 1.1B','https://reemr.se/customs/'),
      'Factory':('Factory館内（地上・中層・上層・地下）','interior_Factory_RE3MR.webp','5000/2476','RE3MR Factory 1.7C','https://reemr.se/Factory/'),
      'Shoreline':('保養所内部（東棟・西棟・管理棟）','interior_Shoreline_Resort.webp','5000/2813','RE3MR Shoreline Resort 1.0B','https://reemr.se/shoreline/'),
    }
    if mkey in building_specs:
        btitle,bsrc,bratio,bcredit,burl=building_specs[mkey]
        building_html=f'''<aside class="building-panel">
<div class="building-head"><div class="building-name"><small>主要建物</small><b>{btitle}</b></div><span class="building-help">ドラッグ移動・ホイール拡大</span><div class="building-tools"><button class="mbtn bfit">全体</button><button class="mbtn bzout">−</button><button class="mbtn bzin">＋</button><button class="mbtn bfs">⛶</button></div></div>
<div class="building-wrap"><div class="building-canvas" style="aspect-ratio:{bratio}"><img loading="lazy" src="{bsrc}" alt="{btitle}">{''.join(building_pins)}</div></div>
<div class="building-credit"><a href="{burl}" target="_blank" rel="noopener">Map: {bcredit} / CC BY-NC-SA 4.0</a></div>
</aside>'''
    if mkey == 'Interchange':
        first_crop=INTERCHANGE_FLOOR_CROPS['first']; second_crop=INTERCHANGE_FLOOR_CROPS['second']
        basement_crop=INTERCHANGE_FLOOR_CROPS['basement']
        floor_controls='''<div class="grp floor-switch" aria-label="館内階層"><span class="floor-caption">階層</span><button class="mbtn floorbtn" data-floor="basement">地下</button><button class="mbtn floorbtn on" data-floor="first">1階</button><button class="mbtn floorbtn" data-floor="second">2階</button></div>'''
        building_html=f'''<aside class="building-panel">
<div class="building-head"><div class="building-name"><small>主要建物</small><b>IDEA・OLI・Goshan 館内</b></div><span class="building-help">ドラッグ移動・ホイール拡大</span>{floor_controls}<div class="building-tools"><button class="mbtn bfit">全体</button><button class="mbtn bzout">−</button><button class="mbtn bzin">＋</button><button class="mbtn bfs">⛶</button></div></div>
<div class="building-wrap"><div class="building-canvas" style="aspect-ratio:{first_crop[2]}/{first_crop[3]}"><img class="floor-map" loading="lazy" src="map_Interchange_1F.svg?v=2" alt="Interchange 1階" data-src-basement="map_Interchange_Basement.svg?v=2" data-src-first="map_Interchange_1F.svg?v=2" data-src-second="map_Interchange_2F.svg?v=2" data-ratio-basement="{basement_crop[2]}/{basement_crop[3]}" data-ratio-first="{first_crop[2]}/{first_crop[3]}" data-ratio-second="{second_crop[2]}/{second_crop[3]}">{''.join(building_labelpins)}{''.join(building_pins)}</div></div>
<div class="building-credit"><a href="https://tarkov.dev/maps" target="_blank" rel="noopener">Map source: tarkov.dev SVG Maps</a></div>
</aside>'''
    building_toggle='<button class="mbtn building-toggle" aria-expanded="false">▣ 館内マップ</button>' if building_html else ''
    loot_heading_small='右の館内図で地下・1階・2階を切替。「金策」で現在階の位置表示' if mkey == 'Interchange' else 'マップの「金策」レイヤーで位置表示'
    tabs.append(f'<button class="tab" data-t="{mkey}">{MAP_JA[mkey]}</button>')
    sections.append(f'''<section id="{mkey}" class="mapsec">
<div class="mapbar">
<div class="grp"><button class="mbtn zout">−</button><button class="mbtn zin">＋</button><button class="mbtn fsb" title="全画面で拡大" aria-label="全画面で拡大">⛶ 全画面</button></div>
{building_toggle}
<div class="grp layers">
<button class="mbtn tgl on" data-g="labelpin"><i class="sw" style="--c:#d4c6a5"></i>地名</button>
<button class="mbtn tgl on" data-g="exapin"><i class="sw sq" style="--c:#1eae4e"></i>常設EX</button>
<button class="mbtn tgl on" data-g="excpin"><i class="sw sq" style="--c:#e8a33d"></i>条件EX</button>
<button class="mbtn tgl" data-g="scavpin"><i class="sw" style="--c:#2f86d6"></i>SCAV</button>
<button class="mbtn tgl" data-g="lootpin"><i class="sw" style="--c:#d9a521"></i>金策</button>
{task_toggle}
{scav_toggle}
</div></div>
<div class="map-layout"><div class="primary-view"><div class="map-wrap"><div class="map" data-map="{mkey}" style="aspect-ratio:{map_ratio}">{map_image}{route_svg}{''.join(labelpins)}{''.join(scavloot)}{''.join(expins)}</div></div></div>{building_html}</div>
<div class="list"><h3>脱出ポイントと方法 <small>※位置は目安あり。レイド中にOキー2連打で必ず確認</small></h3>
<p class="note"><a class="il" href="{EN}{WIKI_MAP[mkey]}#Extractions" target="_blank" rel="noopener">🖼 wikiの{mkey} 脱出セクションを開く(全脱出の写真つき一覧)</a></p>{''.join(exrows)}{f'<p class="note">{exnote}</p>' if exnote else ''}
<h3>金策スポットと必要な鍵 <small>{loot_heading_small}</small></h3>{''.join(lootrows)}
{f'<h3>画像のFactoryタスク <small>「館内マップ」→「タスク」で固定地点を表示</small></h3>{"".join(taskrows)}' if taskrows else ''}
{f'<h3>SCAV向け安全寄り金策 <small>「SCAV金策」で北・南コースを表示</small></h3><p class="note scavnote">安全は保証できません。残り時間・銃声・自分の脱出口を優先し、Lexos正面と大通りは避けて建物の裏をつないでください。</p>{"".join(scavrows)}' if scavrows else ''}</div></section>''')

GUN = lambda slug,name: f'<a class="il" href="{EN}{quote(slug)}" target="_blank" rel="noopener">{name}</a>'
weapons_html = f"""<section id="weapons" class="mapsec"><div class="list">
<p class="note">レベル15前後・トレーダーLL2(Skier LL3未解放)・フリマは一部アイテムのみ購入可、の前提。トレーダー在庫と解放条件はパッチで変わるので、無ければパーツ名でフリマ検索→レベル表記を確認。</p>

<h3>弾薬早見表(口径別おすすめ) <small>貫通値はおおよそ。上=今すぐ買える / 下=解放されたら移行</small></h3>
<p class="note"><b>5.45x39(AK-74系):</b> 今→ <b>PS</b>(貫通~28・クラス3まで) / 次→ <b>PP</b>(~30前後) / 目標→ <b>BT</b>(~40台・クラス4安定)→<b>BS</b>(最上位・Prapor LL3バーター)。フルオート適性が高くマグのスタック詰め(上に貫通弾)と好相性</p>
<p class="note"><b>7.62x39(AKM/SKS):</b> 今→ <b>PS</b>(貫通~32・序盤最強の安弾) / 目標→ <b>BP</b>(~45前後・高火力貫通)。一発の肉ダメージが重く、タップ撃ちで真価</p>
<p class="note"><b>9x19(MPX/MP5/ピストル):</b> 今→ <b>PST gzh</b>(~20・非装甲/脚用) / 目標→ <b>AP 6.3</b>(~30・ようやく装甲に届く)。装甲相手は脚か顔限定と割り切る</p>
<p class="note"><b>12ゲージ(ショットガン):</b> 今→ <b>フレシェット</b>(~26×8粒・近距離で装甲ごと溶かす) / スラグなら <b>AP-20</b>(~37・単発高貫通)。屋内最強枠</p>
<p class="note"><b>7.62x54R(モシン/SVD):</b> 今→ <b>LPS gzh</b>(~37・ヘルメット貫通ワンパン狙い) / 目標→ <b>SNB</b>(~60台・対重装甲)。頭を狙う武器なので安弾でも仕事する</p>
<p class="note"><b>5.56x45(M4/ADAR/AUG):</b> 今→ <b>M855</b>(~27) / 目標→ <b>M855A1</b>(~40台)→<b>M995</b>(最上位)</p>
<p class="note"><b>.366(VPO系・番外):</b> <b>AP-M</b>(~40台)が「安い銃で高貫通」の抜け道枠。低予算で装甲PMCに対抗したい時の選択肢</p>
<p class="note" style="border-left:3px solid #c98f2c"><b>原則:</b> 迷ったら「貫通30以上を上に5〜10発+安弾を下に」のスタック詰め。貫通が敵アーマークラス×10を超えてれば概ね抜ける、が目安</p>
<h3>① メイン: AK-74N「現行ビルド」 <small>反動61 / エルゴ49.8 — 完成済み</small></h3>
<p class="note"><b>構成:</b> {GUN('Kalashnikov_AK-74N_5.45x39_assault_rifle','AK-74N')} + RRD-4Cマズル(拾い物・死亡ロスト注意) + M-LOKハンドガード + RK-4フォアグリップ + SAWグリップ + EKP-1S-03サイト + 6L20 30連<br>
<b>弾:</b> 5.45 PS(貫通28)。PP/BT弾が解放され次第マグ上部にスタック積み<br>
<b>運用:</b> 通常レイド用。Prapor保険必須。プリセット登録してロスト時の復旧を楽に<br>
<b>強み:</b> 反動61は9.3万の店売りプリセット(65)より上。この構成が現状の最適解</p>

<h3>② 節約サブ: AK-74/74N 素組み <small>約5〜6万 / 使い捨て用</small></h3>
<p class="note"><b>構成:</b> 素体(店売り42,864 or ≠5バーターのAK-74M) + 純正マズルのまま + {GUN("TAPCO_SAW-Style_pistol_grip",'SAWグリップ')}(Mechanic LL2) + {GUN('Kobra_EKP-8-02_reflex_sight_(Dovetail)','Kobra EKP-8-02 ドヴテイル')}(直付け) + 30連×2<br>
<b>後で追加:</b> {GUN('AK_GP-25_accessory_kit_recoil_pad','GP-25リコイルパッド')}(Prapor/クエスト解放待ち)、DTK-1(Skier LL3 or フリマ)<br>
<b>運用:</b> スカブ狩り・偵察・危険エリア用の「死んでもいい1本」。①と2本体制で回す</p>

<h3>③ つなぎ火力: AKM 7.62x39 <small>PP/BT無し期間の対アーマー最強</small></h3>
<p class="note"><b>構成:</b> {GUN('Kalashnikov_AKM_7.62x39_assault_rifle','AKM')}(店売り53,803 or ≠3バーター) + DTK-1(7.62/5.45両対応) + SAWグリップ<br>
<b>弾:</b> 7.62x39 PS(貫通32) — 5.45 PSより硬い相手に強い。トレーダーで安定供給<br>
<b>運用:</b> タップ〜短バースト。BT/PP解放までのメイン候補。反動キツめなので近〜中距離</p>

<h3>④ 寮・屋内用: MP-153/155 ショットガン <small>約3〜4万</small></h3>
<p class="note"><b>構成:</b> {GUN('MP-153_12ga_semi-automatic_shotgun','MP-153')}ほぼ素のままでOK<br>
<b>弾:</b> 12ゲージ フレシェット — 近距離なら胴撃ちでアーマーごと溶ける<br>
<b>運用:</b> 寮・Factory・屋内CQB向け。近距離のPMC戦と相性◎</p>

<h3>⑤ 遠距離用: モシン <small>2万以下 / コスパ最強スナイパー</small></h3>
<p class="note"><b>構成:</b> {GUN('Mosin_7.62x54R_bolt-action_rifle_(Sniper)','モシン(スナイパー)')}素のまま or PUスコープ<br>
<b>弾:</b> 7.62x54R LPS Gzh — 頭に当てればヘルメット貫通でワンパン<br>
<b>運用:</b> メインロード監視・待ち伏せ。安価な遠距離用として使いやすい</p>

<h3>⑥ 番外: MPX 脚撃ち <small>装甲PMC相手は脚 or 顔限定</small></h3>
<p class="note"><b>弾:</b> 9x19の安弾は貫通20前後で装甲に無力。高レートで脚を溶かすレグメタ運用専用<br>
<b>運用:</b> 屋内の割り切り運用のみ。基本は③AKMを推奨</p>

<h3>共通の原則</h3>
<p class="note">「銃より弾」。マガジンは上5〜10発に貫通弾+下に安弾のスタック詰めが基本。良パーツ(RRD-4C等)は消耗品と割り切り、保険は毎レイド必ず。武器はプリセット保存しておくと再構築が一瞬</p>
</div></section>"""
sections.append(weapons_html)
tabs.append('<button class="tab" data-t="weapons">WEAPONS</button>')

meds_html = f"""<section id="meds" class="mapsec"><div class="list">
<h3>携行セット(毎レイドこれだけ持てばOK)</h3>
<p class="note">{GUN('Salewa_first_aid_kit','Salewa')}×1 + {GUN('Army_bandage','軍用バンデージ')}×2 + {GUN('Esmarch_tourniquet','Esmarch止血帯')}×2 + {GUN('Immobilizing_splint','スプリント')}×1 + {GUN('Golden_Star_balm','ゴールデンスター')}×1 をポーチ/リグに。骨折と重出血を現地で処理できる構成</p>
<h3>医療品Tier(回復キット)</h3>
<p class="note"><b>S(目標):</b> {GUN('Grizzly_medical_kit','Grizzly')} — 全状態異常対応の万能。高いのでガチレイド用<br>
<b>A(定番・今の主力):</b> {GUN('Salewa_first_aid_kit','Salewa')} — 回復量/価格/重出血対応のバランス最良。{GUN('IFAK_individual_first_aid_kit','IFAK')}は1マスで重出血対応の上位互換枠<br>
<b>B(節約):</b> {GUN('Car_first_aid_kit','Car medkit')} — 激安。重出血を止められない点だけ注意(Esmarch併用)<br>
<b>C:</b> AI-2 — 保険外の緊急用。単体運用は非推奨</p>
<h3>状態異常の対処</h3>
<p class="note">軽出血=バンデージ / <b>重出血=Esmarch・CALOK-B</b>(バンデージ不可) / 骨折=スプリント({GUN('Aluminum_splint','アルミスプリント')}が上位) / 鎮痛={GUN('Golden_Star_balm','ゴールデンスター')}(効果時間長くコスパ神。{GUN('Analgin_painkillers','アナルギン')}は安いが短い) / 黒足で走る前に鎮痛必須</p>
<h3>手術キット</h3>
<p class="note">{GUN('CMS_surgical_kit','CMS')} — 黒部位(ゼロHP)を復活させる必需品。Surv12スキル不要のこれを常備。上位の{GUN('Surv12_field_surgical_kit','Surv12')}は回復量ペナルティが少ない高級版</p>
<h3>注射器Tier</h3>
<p class="note"><b>S(キープ/ガチ用):</b> {GUN('eTG-change_regenerative_stimulant_injector','eTG-change')}(継続回復)、{GUN('Zagustin_hemostatic_drug_injector','Zagustin')}(重出血予防)、{GUN('Adrenaline_injector','アドレナリン')}(交戦直前)<br>
<b>A(実用):</b> {GUN('Propital_regenerative_stimulant_injector','Propital')}(回復+鎮痛でラッシュ用)、{GUN('SJ6_TGLabs_combat_stimulant_injector','SJ6')}(スタミナ強化=長距離移動)<br>
<b>B(売却/保管):</b> その他の注射器は基本フリマ売りかハイドアウト用にキープ。<b>注射器ケース</b>が作れるようになったら集める価値が跳ね上がる</p>
<p class="note" style="border-left:3px solid #c98f2c">運用メモ: 回復キットはセキュアコンテナへ(死んでも残る)。レイド中に拾った注射器もセキュアに入れる癖をつけると事故らない</p>
</div></section>"""
sections.append(meds_html)
tabs.append('<button class="tab" data-t="meds">MEDS</button>')

keep_html = f"""<section id="keep" class="mapsec"><div class="list">
<h3>絶対キープ(超高額・見つけたら即セキュア)</h3>
<p class="note">{GUN('Graphics_card','GPU(グラボ)')} — 換金もビットコインファームも最強 / {GUN('LEDX_Skin_Transilluminator','LEDX')} — 医療レア筆頭 / {GUN('Physical_Bitcoin','ビットコイン')} / {GUN('Intelligence_folder','インテリジェンスフォルダ')} / {GUN('Tetriz_portable_game_console','テトリス')} / {GUN('Bronze_lion_figurine','ライオン像')}などの置物系 / {GUN('Ophthalmoscope','検眼鏡')}</p>
<h3>カルトサークル用(価値密度が高い)</h3>
<p class="note">{GUN('SSD_drive','SSDドライブ')} / {GUN('SAS_drive','SASドライブ')} — 400k儀式の主材料。フリマ相場が安い時に確保</p>
<h3>ハイドアウト強化用(序盤は捨てないで)</h3>
<p class="note">{GUN('Bolts','ボルト')}・{GUN('Screw_nuts','ナット')}・{GUN('Pack_of_screws','ネジ')} / {GUN('Wires','電線')}・{GUN('CPU_fan','CPUファン')}(ファームで大量必要) / {GUN('Metal_spare_parts','金属部品')}・{GUN('Electric_motor','電動モーター')} / 工具類({GUN('Pliers','ペンチ')}・{GUN('Screwdriver','ドライバー')}) — 倉庫圧迫するけどLv2施設まではキープ推奨</p>
<h3>用途が多いアイテム(見つけたらキープ)</h3>
<p class="note">{GUN('Gas_analyzer','ガスアナライザー')} / {GUN('Corrugated_hose','コルゲートホース')} / {GUN('Military_power_filter','軍用フィルター類')} / {GUN('Fire_control_computer','FireControl系電子機器')} / ドッグタッグ / 各種キー(使い道不明でも一旦キープ→wikiで確認)</p>
<h3>バーター素材(トレーダー交換で化ける)</h3>
<p class="note">タバコ({GUN('Pack_of_Malboro_cigarettes','マルボロ')}等)・{GUN('Condensed_milk','コンデンスミルク')}・{GUN('Emelya_rye_croutons','クルトン')}などの食品 / {GUN('Golden_neck_chain','金のチェーン')}・{GUN('Chainlet','チェーンレット')}などの貴金属 — 換金前にトレーダーのバーター一覧を確認すると得することが多い</p>
<p class="note" style="border-left:3px solid #c98f2c">判断に迷ったら: アイテム検査画面の「関連品目を検索」でハイドアウト/バーターの用途を確認。1スロあたり2万ルーブル以上なら持ち帰り優先</p>
</div></section>"""
sections.append(keep_html)
tabs.append('<button class="tab" data-t="keep">KEEP</button>')

keys_html = f"""<section id="keys" class="mapsec"><div class="list">
<h3>汎用性が高い「買って損しない」鍵</h3>
<p class="note"><b>{GUN('Factory_exit_key','Factory exit key')}</b> — 最重要。CustomsのZB-1013脱出とFactoryの脱出で使える。使用回数制なので予備も視野<br>
<b>{GUN("Tarcone_Director's_office_room_key","Tarcone Director office key")}</b> — Big Red事務所(PC・インテリ)<br>
<b>{GUN('Dorm_room_314_marked_key','Dorm room 314 Marked key')}</b> — Customs寮のマークドルーム。高額だがレア武器・ケース抽選。金策フェーズ向け<br>
<b>{GUN('Machinery_key','Machinery key')}</b> — Customsで使用。レイド内(寮205ジャケット)で無料入手可</p>
<h3>マップ別・金策鍵の定番</h3>
<p class="note"><b>Shoreline:</b> リゾート部屋キー(西321・東226・東310あたりが定番。LEDX/医療レア抽選)— 相場と回転率をフリマで確認してから<br>
<b>Interchange:</b> {GUN('Kiba_Arms_International_outer_door_key','Kiba外扉')}+{GUN('Kiba_Arms_inner_grate_door_key','Kiba内扉')}の2本セットで銃器店<br>
<b>Woods:</b> {GUN('ZB-014_key','ZB-014')} — 脱出兼スタッシュ<br>
<b>Lighthouse:</b> コテージ各キー(金庫・レア) / <b>Streets:</b> アパート系キーは当たり外れ大きいので後回しでOK</p>
<h3>レイド内で拾う系(買わない)</h3>
<p class="note">Machinery key(寮205) / その他「用途不明の鍵」は一旦キープ→検査画面の「関連品目を検索」かwikiで開く扉を確認してから売る</p>
<h3>鍵の管理術</h3>
<p class="note">① 鍵は死んでも失わない<b>セキュアコンテナ</b>へ。使う分だけ持ち込む ② {GUN('Documents_case','ドキュメントケース')}や{GUN('Key_tool','キーツール')}(鍵専用4x4)を入手したら倉庫圧迫が解決 ③ フリマで買う時は<b>使用回数の残り</b>を確認(中古は安いが回数減) ④ 使用回数のある鍵(Factory exit等)は残数を時々チェック</p>
</div></section>"""
sections.append(keys_html)
tabs.append('<button class="tab" data-t="keys">KEYS</button>')

hideout_html = f"""<section id="hideout" class="mapsec"><div class="list">
<p class="note">序盤〜中盤のハイドアウト強化で要求されがちなアイテムの逆引き。正確な個数はアップデートで変わるので、ゲーム内の各ステーション画面か、アイテム検査の「関連品目を検索」で最終確認を。</p>
<h3>最優先で貯めるもの(複数ステーションで大量要求)</h3>
<p class="note">{GUN('Bolts','ボルト')}・{GUN('Screw_nuts','ナット')}・{GUN('Pack_of_screws','ネジ')} — ワークベンチ/セキュリティ/水収集ほぼ全部 / {GUN('Wires','電線')}+{GUN('Light_bulb','電球')} — 照明・セキュリティ・換気 / {GUN('Metal_spare_parts','金属部品')} — 各種 / {GUN('Duct_tape','ダクトテープ')}・{GUN('Shustrilo_sealing_foam','シーリングフォーム')}・{GUN('FP-100_filter_absorber','フィルター類')} — 建設の定番消耗枠</p>
<h3>工具(1個ずつは必ずキープ)</h3>
<p class="note">{GUN('Screwdriver','ドライバー')} / {GUN('Pliers','ペンチ')} / {GUN('Set_of_files_Master','ヤスリセット')} / {GUN('Leatherman_Multitool','マルチツール')} / {GUN('Electric_drill','電動ドリル')} / {GUN('Toolset','ツールセット')} — ワークベンチ・水収集・栄養ユニット等の建設素材。売ると後で買い直す羽目になる筆頭</p>
<h3>金策系ステーション用(投資回収が大きい)</h3>
<p class="note"><b>ビットコインファーム:</b> {GUN('Graphics_card','GPU')}(枚数分だけ生産速度UP)+{GUN('CPU_fan','CPUファン')}を大量 — CPUファンは見つけたら全部持ち帰り推奨<br>
<b>インテリセンター:</b> 電子系({GUN('Phased_array_element','電子部品類')}・{GUN('Military_cable','ミリタリーケーブル')})+家具系。Lv2でスカブ帰還短縮<br>
<b>水収集器+栄養ユニット:</b> {GUN('Water_filter','浄水フィルター')}(建設+稼働の両方で消費。フリマで見たら買い)+{GUN('Corrugated_hose','コルゲートホース')} — 浄水(Superwater)生産は序盤の安定金策</p>
<h3>快適系(急がないが素材はキープ)</h3>
<p class="note"><b>換気/空気清浄:</b> エアフィルター類 / <b>セキュリティLv2-3:</b> 電線・{GUN('Analog_thermometer','計器類')}・軍用電子系 / <b>暖房・照明Lv上げ:</b> 電球・{GUN('Dry_fuel','燃料類')} — {GUN('Metal_fuel_tank','燃料タンク')}と{GUN('Expeditionary_fuel_tank','遠征燃料タンク')}は発電機の稼働に常時必要なので、空でもキープして詰め替え運用</p>
<h3>運用のコツ</h3>
<p class="note">① 倉庫を「ハイドアウト素材箱」として1列確保して上記を集約 ② 各ステーションの要求はゲーム内で📌ピン留めすると採集リストに出て便利 ③ 迷ったら検査画面の「関連品目を検索」→HIDEOUTタブで使用先が見える ④ 売っていいのは「同じ物が3個以上余ってる時の余剰分」だけ、が安全ルール</p>
</div></section>"""
sections.append(hideout_html)
tabs.append('<button class="tab" data-t="hideout">HIDEOUT</button>')




css='''
:root{--bg:#101215;--panel:#191c21;--line:#2c3038;--tan:#b8ad92;--tanb:#e2d8bd;--amber:#c98f2c;--ex:#1eae4e}
*{box-sizing:border-box;margin:0;-webkit-tap-highlight-color:transparent}
body{background:var(--bg);color:var(--tan);font-family:"Hiragino Kaku Gothic ProN","Noto Sans JP",system-ui,sans-serif}
header{padding:10px 16px 8px;border-bottom:2px solid var(--amber);background:linear-gradient(180deg,#15181d,#101215)}
h1{font-size:17px;letter-spacing:.18em;color:var(--tanb);text-transform:uppercase}
h1::before{content:"▸ ";color:var(--amber)}
header p{font-size:11.5px;margin-top:4px;color:#8a8375;line-height:1.6}
nav{display:flex;gap:6px;padding:8px 10px;border-bottom:1px solid var(--line);position:sticky;top:0;background:#101215f2;z-index:20;overflow-x:auto;-webkit-overflow-scrolling:touch}
.tab{flex:0 0 auto;background:var(--panel);color:var(--tan);border:1px solid var(--line);border-radius:3px;padding:8px 12px;font-size:13px;cursor:pointer;letter-spacing:.05em}
.tab small{color:#8a8375;margin-left:2px}
.tab.on{border-color:var(--amber);color:var(--tanb);background:#22262c;box-shadow:inset 0 -2px 0 var(--amber)}
.mapsec{display:none;padding:10px}
.mapsec.on{display:block}
.mapbar{display:flex;align-items:center;gap:10px;max-width:1700px;margin:0 auto 8px;flex-wrap:wrap}
.mbtn{background:var(--panel);border:1px solid var(--line);color:var(--tanb);border-radius:4px;height:36px;padding:0 12px;font-size:12.5px;cursor:pointer;display:inline-flex;align-items:center;gap:6px;white-space:nowrap}
.mbtn:active{border-color:var(--amber)}
.zin,.zout{min-width:42px;justify-content:center;font-size:17px}
.fsb{min-width:42px;justify-content:center;font-size:15px}
.grp{display:flex;gap:6px}
.layers{flex-wrap:wrap}
.sw{width:11px;height:11px;border-radius:50%;background:var(--c);display:inline-block;border:1.5px solid #000}
.sw.sq{border-radius:2px}
.mbtn.tgl{opacity:.55}
.mbtn.tgl.on{opacity:1;border-color:var(--amber);background:#242a24}
.floor-switch{padding:3px;border:1px solid var(--line);border-radius:5px;background:#0d0f12}
.floor-caption{display:inline-flex;align-items:center;padding:0 6px;color:#79e9fa;font-size:10px;font-weight:800;letter-spacing:.08em}
.floorbtn{height:30px;min-width:48px;justify-content:center;padding:0 10px}
.floorbtn.on{border-color:#35d6f2;color:#dffbff;background:#17333a;box-shadow:inset 0 0 0 1px #35d6f244}
.hint{font-size:10.5px;color:#8a8375}
.map-layout{display:grid;grid-template-columns:1fr;gap:10px;max-width:1900px;margin:0 auto;align-items:start}
.map-layout.building-open{grid-template-columns:minmax(0,1.4fr) minmax(420px,1fr)}
.primary-view,.building-panel{min-width:0}
.building-panel{display:none;border:1px solid var(--line);border-radius:4px;background:#121519;overflow:hidden}.map-layout.building-open .building-panel{display:block}
.building-toggle.on{border-color:#35d6f2;color:#dffbff;background:#17333a}
.building-head{display:flex;align-items:center;gap:8px;justify-content:space-between;flex-wrap:wrap;padding:7px;background:#171b20;border-bottom:1px solid var(--line)}
.building-name{display:flex;flex-direction:column;line-height:1.25}.building-name small{font-size:9px;color:var(--amber);font-weight:800;letter-spacing:.12em}.building-name b{font-size:12px;color:var(--tanb)}
.building-help{font-size:9px;color:#777f89;white-space:nowrap}
.building-tools{display:flex;gap:5px}.building-tools .mbtn{height:30px;min-width:36px;padding:0 9px;justify-content:center}
.building-wrap{position:relative;overflow:auto;height:74vh;background:#0a0c0e;overscroll-behavior:contain;cursor:grab}
.building-canvas{position:relative;width:100%;min-width:100%;transform-origin:0 0}
.building-canvas img{display:block;width:100%;height:auto;pointer-events:none;user-select:none;-webkit-user-drag:none}
.building-wrap.fs{position:fixed;inset:0;z-index:45;height:100dvh;background:#090b0d;border:none}.building-wrap.fs .building-canvas{margin:auto}
.building-credit{padding:4px 8px;font-size:9px;text-align:right;background:#101318}.building-credit a{color:#817a6c;text-decoration:none}
.map-wrap{position:relative;overflow:hidden;height:74vh;border:1px solid var(--line);border-radius:4px;touch-action:none;overscroll-behavior:contain;cursor:grab;background:#0a0c0e}
.map-wrap.fs{position:fixed;inset:0;z-index:45;height:100dvh;max-height:none;border:none;border-radius:0}
.map-wrap.fs.rot{width:100dvh;height:100dvw;inset:auto;top:50%;left:50%;transform:translate(-50%,-50%) rotate(90deg)}
#fsx{display:none;position:fixed;top:calc(10px + env(safe-area-inset-top));right:12px;z-index:49;width:46px;height:46px;border-radius:50%;background:#000d;border:1px solid var(--amber);color:#fff;font-size:20px}
body.fsmode #fsx{display:block}
.map-wrap.fs #fsx,.building-wrap.fs #fsx{display:block}
body.fsmode #modal{align-items:flex-start;justify-content:flex-start;padding:10px}
body.fsmode .mbox{max-width:330px;max-height:72vh;font-size:12px}
.map-wrap.fs .fsclose{display:none}
.fsclose{display:none;position:fixed;top:12px;right:12px;z-index:46;width:44px;height:44px;border-radius:50%;background:#000c;border:1px solid var(--amber);color:#fff;font-size:20px}
.map-wrap.fs .fsclose{display:block}
.map{position:absolute;left:0;top:0;width:100%;transform-origin:0 0;will-change:transform}
.map img{display:block;width:100%;height:auto;pointer-events:none;user-select:none;-webkit-user-drag:none}
.pin{position:absolute;transform:translate(-50%,-50%);background:none;border:none;padding:6px;cursor:pointer;z-index:2}
.exdot{display:flex;align-items:center;justify-content:center;width:22px;height:22px;color:#fff;font-weight:800;font-size:10px;border:2px solid #fff;border-radius:3px;box-shadow:0 2px 6px rgba(0,0,0,.6)}
.exa{background:#1eae4e}.exc{background:#e8a33d;color:#111}
.exs{background:#2f86d6;border-radius:50%}.exl{background:#d9a521;color:#111;border-radius:50%;font-size:12px}
.exar{border-left-color:#1eae4e}.excr{border-left-color:#e8a33d}
.exbadge.exa{background:#1eae4e}.exbadge.exc{background:#e8a33d;color:#111}
.hid{display:none}
.exlbl{position:absolute;left:calc(100% - 3px);top:50%;transform:translateY(-50%);font-size:10.5px;font-weight:700;color:#7dffab;white-space:nowrap;text-shadow:0 1px 2px #000,0 -1px 2px #000,1px 0 2px #000,-1px 0 2px #000;pointer-events:none}
.exlblc{color:#ffc46b}
.exlbls{color:#8ec9ff}
.labelpin{position:absolute;transform:translate(-50%,-50%) scale(calc(1/var(--s,1)));transform-origin:center;color:#f1e7c9;background:#101215c9;border:1px solid #706852;border-radius:3px;padding:2px 5px;font-size:9px;font-weight:700;line-height:1;white-space:nowrap;text-shadow:0 1px 2px #000;pointer-events:none;z-index:1}
.scavroute{position:absolute;inset:0;width:100%;height:100%;z-index:2;pointer-events:none;overflow:visible}
.scavroute polyline{fill:none;stroke:var(--route);stroke-width:.75;stroke-dasharray:2.2 1.3;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 0 .7px #000)}
.slroute-label{position:absolute;transform:translate(-50%,-50%) scale(calc(1/var(--s,1)));transform-origin:center;border:2px solid var(--route);background:#111e;color:#fff;border-radius:4px;padding:3px 7px;font-size:11px;font-weight:900;white-space:nowrap;text-shadow:0 1px 2px #000;pointer-events:none;z-index:3}
.slpin{z-index:4}
.sldot{display:flex;align-items:center;justify-content:center;width:25px;height:25px;border:2px solid #fff;border-radius:5px;color:#111;font-size:11px;font-weight:900;box-shadow:0 2px 7px #000}
.sl-safe .sldot{background:#49d17d}.sl-valuable .sldot{background:#ffd33d}.sl-body .sldot{background:#62a9ff;color:#07111d}
.flpin{z-index:4}.flpin .sldot{border-radius:50%}
.taskpin{z-index:6}.taskdot{display:flex;align-items:center;justify-content:center;width:25px;height:25px;border:2px solid #fff;border-radius:6px;background:#a64ee5;color:#fff;font-size:11px;font-weight:900;box-shadow:0 2px 8px #000}.tasklbl{background:#291438e8;border:1px solid #b76cff;color:#f2dfff}.taskrow{border-left-color:#a64ee5}.taskbadge{background:#a64ee5!important;color:#fff!important}
.tasklinks{display:inline-flex;gap:5px;margin-left:8px;vertical-align:middle}.tasklink{display:inline-flex;align-items:center;padding:2px 7px;border:1px solid #555d68;border-radius:4px;color:#d5dbe4;background:#20242a;text-decoration:none;font-size:9px;font-weight:800}.tasklink.wiki{border-color:#6687b9;color:#c7dcff;background:#182433}.tasklink:hover{border-color:var(--amber);color:#fff}
.fl-steady .sldot{background:#49d17d}.fl-valuable .sldot{background:#ffd33d}.fl-danger .sldot{background:#ff5b56;color:#fff}
.flpin[data-m="Interchange_fl12"] .sllbl{left:auto;right:calc(100% - 3px)}
.sllbl{position:absolute;left:calc(100% - 3px);top:50%;transform:translateY(-50%);font-size:10px;font-weight:800;color:#fff;white-space:nowrap;background:#111d;border-radius:3px;padding:2px 4px;text-shadow:0 1px 2px #000;pointer-events:none}
.slrow-safe{border-left-color:#49d17d}.slrow-valuable{border-left-color:#ffd33d}.slrow-body{border-left-color:#62a9ff}
.slbadge-safe{background:#49d17d!important;color:#111!important}.slbadge-valuable{background:#ffd33d!important;color:#111!important}.slbadge-body{background:#62a9ff!important;color:#07111d!important}
.scavnote{border-left:3px solid #35d6f2!important}
.flrow-steady{border-left-color:#49d17d}.flrow-valuable{border-left-color:#ffd33d}.flrow-danger{border-left-color:#ff5b56}
.flbadge-steady{background:#49d17d!important;color:#111!important}.flbadge-valuable{background:#ffd33d!important;color:#111!important}.flbadge-danger{background:#ff5b56!important;color:#fff!important}
@media(max-width:900px){.map-layout.building-open{grid-template-columns:1fr}.building-wrap{height:62vh}.building-panel{margin-top:2px}}
@media(max-width:640px){.exlbl{font-size:9px}.building-head{align-items:flex-start}.floor-switch{order:3;width:100%;overflow-x:auto}.building-tools{margin-left:auto}}

.pin:active .exdot,.pin:hover .exdot{transform:scale(1.35)}
.list{max-width:1100px;margin:14px auto 26px;padding:0 2px}
.list h3{font-size:12px;letter-spacing:.15em;color:var(--tanb);margin:16px 0 8px;border-left:3px solid var(--amber);padding-left:8px}
.list h3 small{color:#8a8375;font-weight:400;letter-spacing:0}
.il{color:var(--amber);text-decoration:underline;text-underline-offset:2px}
.exrow{font-size:12px;padding:6px 9px;border:1px solid var(--line);border-left:3px solid var(--ex);border-radius:3px;background:var(--panel);margin-bottom:5px;line-height:1.55}
.exbadge{display:inline-block;background:var(--ex);color:#fff;font-size:9.5px;font-weight:800;border-radius:2px;padding:1px 5px;margin-right:7px}
.exbadge.exl2{background:#d9a521;color:#111}
.lootr{border-left-color:#d9a521}
.note{font-size:11.5px;line-height:1.7;color:var(--tan);background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:8px 11px;margin:6px 0}
#modal{position:fixed;inset:0;background:#000c;display:none;z-index:50;align-items:center;justify-content:center;padding:14px}
#modal.on{display:flex}
.mbox{background:#15181d;border:1px solid var(--amber);border-radius:6px;max-width:560px;width:100%;max-height:92vh;overflow:auto;box-shadow:0 10px 40px #000}
.mhead{padding:12px 14px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:start;gap:8px}
.mhead b{color:var(--tanb);font-size:15px;display:block}
.mhead small{color:#8a8375;font-size:11.5px}
.mclose{background:none;border:1px solid var(--line);color:var(--tan);border-radius:3px;font-size:16px;padding:2px 10px;cursor:pointer}
.mbody{padding:12px 14px;font-size:12.5px;line-height:1.7}
.mbody .lbl{color:#8a8375;font-size:10.5px;letter-spacing:.1em}
.mfoot{padding:0 14px 14px;display:flex;gap:8px;flex-wrap:wrap}
.mfoot a{flex:1;text-align:center;border:1px solid var(--amber);border-radius:4px;color:var(--tanb);background:#22262c;text-decoration:none;font-size:12.5px;padding:9px 10px}
@media(max-width:640px){
#modal{align-items:flex-end;padding:0}
.mbox{max-width:100%;border-radius:12px 12px 0 0;border-bottom:none;max-height:86vh}
.exdot{width:25px;height:25px}
.hint{display:none}
.mapbar{gap:6px}
.map-wrap{height:72vh}
.mapsec{padding:6px}
}
'''

css += '''
#q{flex:0 0 170px;background:#0d0f12;border:1px solid var(--line);border-radius:4px;color:var(--tanb);padding:0 10px;height:36px;font-size:16px}
#q:focus{outline:none;border-color:var(--amber)}
#qdrop{position:fixed;top:52px;left:10px;right:10px;max-width:520px;background:#15181d;border:1px solid var(--amber);border-radius:6px;z-index:60;display:none;max-height:50vh;overflow:auto}
#qdrop .qi{display:block;width:100%;text-align:left;background:none;border:none;border-bottom:1px solid var(--line);color:var(--tanb);padding:10px 12px;font-size:13px}
#qdrop .qi small{color:#8a8375;margin-left:6px}
.pin{transform:translate(-50%,-50%) scale(calc(1/var(--s,1)))}
@media(max-width:640px){#q{flex:1 1 140px}}
'''

js='''
const MD=__MD__;
const modalHome=document.body;
function moveFullscreenUiInto(el){const m=document.getElementById("modal"),x=document.getElementById("fsx");if(m&&el&&m.parentElement!==el)el.appendChild(m);if(x&&el&&x.parentElement!==el)el.appendChild(x)}
function restoreModalHome(){const m=document.getElementById("modal"),x=document.getElementById("fsx");if(m&&m.parentElement!==modalHome)modalHome.appendChild(m);if(x&&x.parentElement!==modalHome)modalHome.appendChild(x)}
document.addEventListener("fullscreenchange",()=>{if(!document.fullscreenElement)restoreModalHome()});
const tabs=[...document.querySelectorAll(".tab")],secs=[...document.querySelectorAll(".mapsec")];
tabs.forEach(t=>t.addEventListener("click",()=>{tabs.forEach(x=>x.classList.remove("on"));secs.forEach(s=>s.classList.remove("on"));t.classList.add("on");document.getElementById(t.dataset.t).classList.add("on");window.scrollTo({top:0});}));
tabs[0].click();
// zoom & fullscreen per map section
document.querySelectorAll(".mapsec").forEach(sec=>{
 const map=sec.querySelector(".map"); if(!map)return;
 const wrap=sec.querySelector(".map-wrap");
 let s=1,tx=0,ty=0;
 const mh=()=>map.getBoundingClientRect().height/s;
 const clamp=()=>{const W=wrap.clientWidth,H=wrap.clientHeight,mw=W*s,mhh=map.offsetHeight*s;
  tx=Math.min(Math.max(tx,Math.min(0,W-mw)- W*0.3), W*0.3);
  ty=Math.min(Math.max(ty,Math.min(0,H-mhh)-H*0.3), H*0.3);};
 const apply=()=>{clamp();map.style.transform=`translate(${tx}px,${ty}px) scale(${s})`;map.style.setProperty("--s",s);map.classList.toggle("zoomout",s<0.95)};
 const zoomAt=(cx,cy,f)=>{const ns=Math.min(9,Math.max(0.5,s*f));f=ns/s;
  tx=cx-(cx-tx)*f; ty=cy-(cy-ty)*f; s=ns; apply();};
 // init: mobile starts zoomed-in a bit, centered
 requestAnimationFrame(()=>{
  const H=wrap.clientHeight, mhh=map.offsetHeight;
  if(map.dataset.map==="Interchange"&&mhh>H){ty=(H-mhh)/2}
  else if(mhh<H){ty=(H-mhh)/2}
  if(window.innerWidth<640){zoomAt(wrap.clientWidth/2,wrap.clientHeight/2,1.8)}else{apply()}
 });
 wrap.addEventListener("floorchange",()=>requestAnimationFrame(()=>{
  s=1;tx=0;const H=wrap.clientHeight,mhh=map.offsetHeight;ty=(H-mhh)/2;apply();
 }));
 wrap.addEventListener("layoutchange",()=>requestAnimationFrame(()=>{s=1;tx=0;const H=wrap.clientHeight,mhh=map.offsetHeight;ty=(H-mhh)/2;apply()}));
 sec.querySelector(".zin")?.addEventListener("click",()=>zoomAt(wrap.clientWidth/2,wrap.clientHeight/2,1.35));
 sec.querySelector(".zout")?.addEventListener("click",()=>zoomAt(wrap.clientWidth/2,wrap.clientHeight/2,1/1.35));
 sec.querySelector(".fsb")?.addEventListener("click",()=>{
  wrap.classList.add("fs");document.body.style.overflow="hidden";document.body.classList.add("fsmode");
  moveFullscreenUiInto(wrap);
  apply();
 });
 window.addEventListener("resize",()=>{if(wrap.classList.contains("fs"))apply()});
 const cvt=(cx,cy)=>{const r=wrap.getBoundingClientRect();
  if(wrap.classList.contains("rot")){const scx=(r.left+r.right)/2,scy=(r.top+r.bottom)/2;
   return[wrap.clientWidth/2+(cy-scy),wrap.clientHeight/2-(cx-scx)]}
  return[cx-r.left,cy-r.top]};
 const pos=e=>cvt(e.clientX,e.clientY);
 const tpos=t=>cvt(t.clientX,t.clientY);
 const dist=e=>Math.hypot(e.touches[0].clientX-e.touches[1].clientX,e.touches[0].clientY-e.touches[1].clientY);
 let pan=null,pinch=null;
 wrap.addEventListener("touchstart",e=>{
  if(e.touches.length===1){const[x,y]=tpos(e.touches[0]);pan={x,y,tx,ty}}
  if(e.touches.length===2){pan=null;
   const[ax,ay]=tpos(e.touches[0]),[bx,by]=tpos(e.touches[1]);
   pinch={d:dist(e),cx:(ax+bx)/2,cy:(ay+by)/2}}
 },{passive:true});
 wrap.addEventListener("touchmove",e=>{
  if(pinch&&e.touches.length===2){e.preventDefault();
   const nd=dist(e);const[ax,ay]=tpos(e.touches[0]),[bx,by]=tpos(e.touches[1]);
   const ncx=(ax+bx)/2,ncy=(ay+by)/2;
   zoomAt(pinch.cx,pinch.cy,nd/pinch.d);
   tx+=ncx-pinch.cx;ty+=ncy-pinch.cy;apply();
   pinch={d:nd,cx:ncx,cy:ncy};return}
  if(pan&&e.touches.length===1){e.preventDefault();
   const[x,y]=tpos(e.touches[0]);
   tx=pan.tx+(x-pan.x);ty=pan.ty+(y-pan.y);apply()}
 },{passive:false});
 wrap.addEventListener("touchend",e=>{
  if(e.touches.length<2)pinch=null;
  if(e.touches.length===1){const[x,y]=tpos(e.touches[0]);pan={x,y,tx,ty}}
  if(e.touches.length===0)pan=null});
 let mdrag=null;
 wrap.addEventListener("pointerdown",e=>{if(e.pointerType!=="mouse"||e.button!==0||e.target.closest(".pin")||e.target.closest(".fsclose"))return;
  const[x,y]=pos(e);mdrag={id:e.pointerId,x,y,tx,ty};wrap.setPointerCapture(e.pointerId);wrap.style.cursor="grabbing";e.preventDefault()});
 wrap.addEventListener("pointermove",e=>{if(!mdrag||e.pointerId!==mdrag.id)return;const[x,y]=pos(e);tx=mdrag.tx+(x-mdrag.x);ty=mdrag.ty+(y-mdrag.y);apply()});
 const endDrag=e=>{if(mdrag&&(!e||e.pointerId===mdrag.id)){mdrag=null;wrap.style.cursor="grab"}};
 wrap.addEventListener("pointerup",endDrag);wrap.addEventListener("pointercancel",endDrag);wrap.addEventListener("lostpointercapture",endDrag);
 wrap.addEventListener("dragstart",e=>e.preventDefault());
 wrap.addEventListener("wheel",e=>{e.preventDefault();const[x,y]=pos(e);zoomAt(x,y,e.deltaY<0?1.15:1/1.15)},{passive:false});
});
document.querySelectorAll(".building-panel").forEach(panel=>{
 const wrap=panel.querySelector(".building-wrap"),canvas=panel.querySelector(".building-canvas");let bs=1;
 const apply=()=>canvas.style.width=`${bs*100}%`;
 const zoom=f=>{const ox=(wrap.scrollLeft+wrap.clientWidth/2)/(canvas.offsetWidth||1),oy=(wrap.scrollTop+wrap.clientHeight/2)/(canvas.offsetHeight||1);bs=Math.max(1,Math.min(5,bs*f));apply();wrap.scrollLeft=ox*canvas.offsetWidth-wrap.clientWidth/2;wrap.scrollTop=oy*canvas.offsetHeight-wrap.clientHeight/2};
 const readable=()=>{bs=1;apply();requestAnimationFrame(()=>{bs=Math.max(1,Math.min(5,wrap.clientHeight*.94/(canvas.offsetHeight||1)));apply();wrap.scrollLeft=Math.max(0,(canvas.offsetWidth-wrap.clientWidth)/2);wrap.scrollTop=0})};
 panel.querySelector(".bzin").onclick=()=>zoom(1.25);panel.querySelector(".bzout").onclick=()=>zoom(1/1.25);
 panel.querySelector(".bfit").onclick=()=>{bs=1;apply();wrap.scrollTo(0,0)};
 panel.querySelector(".bfs").onclick=()=>{wrap.classList.add("fs");document.body.style.overflow="hidden";document.body.classList.add("fsmode");moveFullscreenUiInto(wrap)};
 wrap.addEventListener("wheel",e=>{e.preventDefault();zoom(e.deltaY<0?1.18:1/1.18)},{passive:false});
 wrap.addEventListener("buildingfloorchange",readable);wrap.addEventListener("buildingopen",readable);
 let bd=null;
 wrap.addEventListener("pointerdown",e=>{if(e.pointerType!=="mouse"||e.button!==0||e.target.closest("button"))return;bd={id:e.pointerId,x:e.clientX,y:e.clientY,left:wrap.scrollLeft,top:wrap.scrollTop};wrap.setPointerCapture(e.pointerId);wrap.style.cursor="grabbing";e.preventDefault()});
 wrap.addEventListener("pointermove",e=>{if(!bd||e.pointerId!==bd.id)return;wrap.scrollLeft=bd.left-(e.clientX-bd.x);wrap.scrollTop=bd.top-(e.clientY-bd.y)});
 const bend=e=>{if(bd&&(!e||e.pointerId===bd.id)){bd=null;wrap.style.cursor="grab"}};wrap.addEventListener("pointerup",bend);wrap.addEventListener("pointercancel",bend);wrap.addEventListener("lostpointercapture",bend);wrap.addEventListener("dragstart",e=>e.preventDefault());
 apply();
});
document.querySelectorAll(".building-toggle").forEach(btn=>btn.addEventListener("click",()=>{
 const sec=btn.closest(".mapsec"),layout=sec.querySelector(".map-layout"),open=layout.classList.toggle("building-open");btn.classList.toggle("on",open);btn.setAttribute("aria-expanded",open);requestAnimationFrame(()=>{sec.querySelector(".map-wrap")?.dispatchEvent(new Event("layoutchange"));if(open)sec.querySelector(".building-wrap")?.dispatchEvent(new Event("buildingopen"))});
}));
document.querySelectorAll(".floor-switch").forEach(sw=>{
 const sec=sw.closest(".mapsec"),panel=sw.closest(".building-panel"),img=panel.querySelector(".floor-map"),map=panel.querySelector(".building-canvas"),wrap=panel.querySelector(".building-wrap");
 const recenter=()=>wrap.dispatchEvent(new Event('buildingfloorchange'));
 img.addEventListener('load',recenter);
 const setFloor=floor=>{
  sec.dataset.floor=floor;
  sw.querySelectorAll(".floorbtn").forEach(b=>b.classList.toggle("on",b.dataset.floor===floor));
  img.src=img.dataset["src"+floor[0].toUpperCase()+floor.slice(1)];
  map.style.aspectRatio=img.dataset["ratio"+floor[0].toUpperCase()+floor.slice(1)];
  img.alt=`Interchange ${floor==="overview"?"全体":floor==="basement"?"地下":floor==="first"?"1階":"2階"}`;
  ['labelpin','lootpin'].forEach(group=>{
   const groupOn=sec.querySelector(`.tgl[data-g="${group}"]`)?.classList.contains("on");
   sec.querySelectorAll(`.${group}[data-floor]`).forEach(p=>p.classList.toggle("hid",!groupOn||p.dataset.floor!==floor));
  });
  sec.querySelectorAll('.floor-list').forEach(r=>r.classList.toggle("hid",r.dataset.floor!==floor));
  recenter();setTimeout(recenter,80);
 };
 sw.querySelectorAll(".floorbtn").forEach(b=>b.addEventListener("click",()=>setFloor(b.dataset.floor)));
 setFloor("first");
});
document.querySelectorAll(".tgl").forEach(b=>b.addEventListener("click",()=>{
 const sec=b.closest(".mapsec");b.classList.toggle("on");
 sec.querySelectorAll("."+b.dataset.g).forEach(p=>{
  const wrongFloor=p.dataset.floor&&sec.dataset.floor&&p.dataset.floor!==sec.dataset.floor;
  p.classList.toggle("hid",!b.classList.contains("on")||wrongFloor);
 });
}));
// modal
const modal=document.getElementById("modal"),mt=document.getElementById("mt"),ms=document.getElementById("ms"),
 mp=document.getElementById("mp"),mdsc=document.getElementById("mdsc"),
 mit=document.getElementById("mit"),mimg=document.getElementById("mimg"),mitwrap=document.getElementById("mitwrap");
function showM(d){
 mt.textContent=d.title;ms.textContent=d.sub;mp.textContent=d.place;mdsc.textContent=d.desc;
 mit.innerHTML=d.items||"";mitwrap.style.display=d.items?"block":"none";
 mimg.href=d.img;
 const wl=document.getElementById("mwl");
 if(d.wl){wl.href=d.wl;wl.textContent=d.wt||"🖼 wikiで写真を見る";wl.style.display="block"}else{wl.style.display="none"}
 modal.classList.add("on");
}
document.querySelectorAll(".pin").forEach(p=>p.addEventListener("click",e=>{
 e.stopPropagation();const d=MD[p.dataset.m];if(d)showM(d);
}));
// fullscreen global UI
const fsx=document.createElement("button");fsx.id="fsx";fsx.textContent="✕";document.body.appendChild(fsx);
fsx.onclick=()=>{document.querySelectorAll(".map-wrap.fs,.building-wrap.fs").forEach(w=>w.classList.remove("fs","rot"));document.body.style.overflow="";document.body.classList.remove("fsmode");restoreModalHome()};
modal.addEventListener("click",e=>{if(e.target===modal)modal.classList.remove("on")});
document.getElementById("mc").addEventListener("click",()=>modal.classList.remove("on"));
'''
md_json=json.dumps(modal_data,ensure_ascii=False)
js = js + '''
// ---- service worker ----
if("serviceWorker" in navigator){navigator.serviceWorker.register("sw.js").catch(()=>{})}
function openTab(t){document.querySelector(`.tab[data-t="${t}"]`)?.click()}
// ---- search ----
const q=document.getElementById("q"),qd=document.getElementById("qdrop");
const INDEX=[];
document.querySelectorAll(".mapsec").forEach(sec=>{
 const tab=sec.id;
 sec.querySelectorAll(".exrow").forEach(r=>INDEX.push({t:r.textContent.trim().slice(0,60),tab,el:r,kind:"脱出/金策"}));
 sec.querySelectorAll(".il").forEach(a=>INDEX.push({t:a.textContent.trim(),tab,el:a.closest("p")||a,kind:"アイテム/鍵"}));
});
q.addEventListener("input",()=>{
 const v=q.value.trim().toLowerCase();qd.innerHTML="";
 if(v.length<2){qd.style.display="none";return}
 const hits=INDEX.filter(i=>i.t.toLowerCase().includes(v)).slice(0,15);
 if(!hits.length){qd.style.display="none";return}
 hits.forEach(h=>{const b=document.createElement("button");b.className="qi";
  b.innerHTML=`${h.t}<small>${h.kind} / ${h.tab}</small>`;
  b.onclick=()=>{openTab(h.tab);qd.style.display="none";q.blur();
   setTimeout(()=>{h.el.scrollIntoView({block:"center"});h.el.style.outline="2px solid #c98f2c";
    setTimeout(()=>h.el.style.outline="",2200)},150)};
  qd.appendChild(b)});
 qd.style.display="block";
});
document.addEventListener("click",e=>{if(!e.target.closest("#qdrop")&&e.target!==q)qd.style.display="none"});
'''
html=f'''<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<link rel="manifest" href="manifest.json"><meta name="theme-color" content="#14161a">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="apple-touch-icon" href="icon-192.png"><title>Tarkov 脱出マップ</title><style>{css}</style></head><body>
<header><h1>Tarkov Extract Map <small style="color:#8a8375;font-size:11px;letter-spacing:0">{BUILD_VER}</small></h1></header>
<nav><input id="q" type="search" placeholder="検索: 鍵/脱出/アイテム" autocomplete="off">{''.join(tabs)}</nav>
<div id="qdrop"></div>

{''.join(sections)}
<footer style="padding:18px;text-align:center;font-size:10px;color:#8a8375">Map artwork: <a class="il" href="https://github.com/the-hideout/tarkov-dev-svg-maps" target="_blank" rel="noopener">tarkov-dev SVG Maps</a> · <a class="il" href="https://github.com/the-hideout/tarkov-dev-svg-maps/blob/main/LICENSE.md" target="_blank" rel="noopener">CC BY-NC-SA 4.0</a></footer>
<div id="modal"><div class="mbox"><div class="mhead"><div><b id="mt"></b><small id="ms"></small></div><button class="mclose" id="mc">×</button></div>
<div class="mbody"><div class="lbl">場所</div><div id="mp"></div><div class="lbl" style="margin-top:8px">やり方</div><div id="mdsc"></div><div id="mitwrap"><div class="lbl" style="margin-top:8px">必要アイテム(下線=wiki)</div><div id="mit"></div></div></div>
<div class="mfoot"><a id="mwl" href="#" target="_blank" rel="noopener">🖼 wikiで写真を見る</a><a id="mimg" href="#" target="_blank" rel="noopener">📷 画像検索</a></div></div></div>
<script>const __MDPH__=0;</script>
<script>{js.replace("__MD__", md_json)}</script>
</body></html>'''
with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8') as output_file:
    output_file.write(html)
print('built index.html', len(html)//1024, 'KB', BUILD_VER)
