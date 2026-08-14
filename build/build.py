# -*- coding: utf-8 -*-
import json, os
from urllib.parse import quote, quote_plus
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
with open(os.path.join(HERE, 'map_configs.json'), encoding='utf-8') as cfg_file:
    cfgs = json.load(cfg_file)
dims = {"Woods":[1600,1543],"Shoreline":[1600,1059],"Factory":[1600,1727],
 "GroundZero":[1600,2240],"Lighthouse":[1600,2602],"Interchange":[1600,1344],
 "StreetsOfTarkov":[1600,2198],"Customs":[2400,1209]}
import datetime
BUILD_VER = datetime.date.today().strftime('v%Y.%m.%d')
JP='https://wikiwiki.jp/eft/'; EN='https://escapefromtarkov.fandom.com/wiki/'
IMG='https://www.google.com/search?tbm=isch&q='
WIKI_MAP={'Customs':'Customs','Woods':'Woods','Shoreline':'Shoreline','Factory':'Factory',
 'StreetsOfTarkov':'Streets_of_Tarkov','GroundZero':'Ground_Zero','Interchange':'Interchange','Lighthouse':'Lighthouse'}

def make_pct(mk):
    cfg=cfgs[mk]; (x1,z1),(x2,z2)=cfg['bounds']
    if mk=='Factory.svg':
        return lambda x,z:(round((z1-z)/(z1-z2)*100,2), round((x-x2)/(x1-x2)*100,2))
    return lambda x,z:(round((x1-x)/(x1-x2)*100,2), round((z-z1)/(z2-z1)*100,2))

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
 'M4A1':'Colt_M4A1_5.56x45_assault_rifle','Dorm room 314 marked key':'Dorm_room_314_marked_key','Kiba Arms外扉':'Kiba_Arms_International_outer_door_key','Tarcone Director\'s officeキー':'Tarcone_Director\'s_office_room_key','HK MP5':'HK_MP5_9x19_submachine_gun_(Navy_3_Round_Burst)',
}
def linkify(items):
    out = items
    for k in sorted(ITEM_LINKS, key=len, reverse=True):
        if k in out:
            out = out.replace(k, f'<a class="il" href="{EN}{quote(ITEM_LINKS[k])}" target="_blank" rel="noopener">{k}</a>')
    return out

# tasks: (name, trader, diff, imp, place, desc, items, en_slug, anchor)
MAPS = {}
MAPS['Customs'] = [
 ('Abandoned Cargo','Therapist',1,'中','ターミナル周辺','TerraGroupロゴ入りパレット7か所のどれか1つをマーク','MS2000マーカー×1','Abandoned_Cargo',(10,-70)),
 ('The Extortionist','Skier',2,'高','Crackhouse付近の茂み→Warehouse3脇の小屋','死体からUnknown Key→施錠小屋の床の服からカーゴ回収→生還','なし(鍵はレイド内)','The_Extortionist',(45,-140)),
 ('Shipment Tracking','Therapist',2,'中','ボイラー棟2F重役室(Repair Shop隣)','赤いドアを開錠し積荷リスト回収→生還','Company director\'s room key','Shipment_Tracking',(100,-38)),
 ('The Courier','Mechanic',2,'中','新ガソスタ裏のゴミ箱','支給REAP-IRを設置(セキュア不可・ロスト注意)','REAP-IR(支給済)','The_Courier',(404,38)),
 ('Chemical - Part 1','Skier',2,'高','西側の線路上の貨車(目安)','貨車内のフォルダ回収→生還→220キーと共に納品','Dorm room 220キー(納品用)','Chemical_-_Part_1',(540,-105)),
 ('The Punisher - Part 1','Prapor',3,'高','マップ全域','Customsでスカブを規定数討伐(Punisherチェーン開始。目標欄参照)','戦闘装備','The_Punisher_-_Part_1',None),
 ('Break the Deal','Ragman',3,'中','ボイラー(3本パイプ工場)の足場','DVL(マグ外す)→マグ→ELCAN→7.62x51弾パックの順に4点設置','ELCAN(所持済)・7.62x51パック','Break_the_Deal',(112,-58)),
 ('Huntsman Path - Trophy','Jaeger',5,'高','寮/新ガソスタ/工事現場/W4棟のどこか','ボスのレシャラを討伐し金TT-33をFIR回収(セキュア不可)','なし(フィギュア救済あり)','The_Huntsman_Path_-_Trophy',(300,-40)),
]
MAPS['Woods'] = [
 ('Hiking (80%)','Peacekeeper',2,'低','Woods内の指定地点(目標欄参照)','残り1〜2か所を訪問するだけ。Woods行くついでに完了','なし','Hiking',None),
 ('Ice Cream Cones (16%)','Prapor',2,'中','バス停周辺のバス(目安)','6L31 60連マガジン×2を指定ポイントに設置','6L31 60連×2','Ice_Cream_Cones',(-234,357)),
 ('Metal Birds','Peacekeeper',2,'中','ヘリ関連地点(目標欄参照)','設置/納品系。詳細はゲーム内目標参照','対象アイテム(目標欄参照)','Metal_Birds',None),
 ('Supply Plans','Therapist',2,'中','小屋(目標欄のマーカー参照)','補給計画のメモを回収して納品','なし','Supply_Plans',None),
 ('A Helping Hand','Mechanic',2,'中','Woods内(目標欄参照)','発見/回収系。詳細は目標欄とwikiを確認','なし','A_Helping_Hand',None),
 ('Shipping Delay - Part 1','Prapor',3,'中','Convoy(車列)周辺が有力(目標欄参照)','積荷関連の回収/確認系。詳細は目標欄参照','なし','Shipping_Delay_-_Part_1',(168,-600)),
 ('Gratitude','Ragman',3,'高','製材所の湖側の木製桟橋(樽の間)','衣類4点を設置。1点20秒×4で無防備、夜レイド推奨','Ghostバラクラバ・緑シュマグ・RayBench・丸フレームサングラス','Gratitude',(-45,15)),
 ('Huntsman Path - Woods Keeper','Jaeger',5,'高','製材所(Sawmill)','ボスのシュトゥルマンを討伐しドロップ品を納品','対ボス装備','The_Huntsman_Path_-_Woods_Keeper',(10,-3)),
 ('Swift','Jaeger',5,'低','マップ全域','アーマー・ヘルメット無しでPMCを15キル','防具なし縛り','Swift',None),
]
MAPS['Shoreline'] = [
 ('Master Key','Peacekeeper',2,'高','リゾート北のバンカー','椅子の上の鍵を回収→生還して納品(死亡で取り直し)','なし','Master_Key',(-153,-290)),
 ('Anesthesia','Prapor',2,'高','沼〜村エリアのサニタール取引所3か所','白いテーブルに薬瓶+血痕が目印。3か所にMS2000を設置(Prapor評判+0.25)','MS2000マーカー×3','Anesthesia',(326,-118.5)),
 ('Health Care Privacy - Part 2','Therapist',2,'中','リゾート周辺ほか(目標欄参照)','P1の続き。対象をMS2000でマーク(対象は目標欄で確認)','MS2000マーカー×1〜2','Health_Care_Privacy_-_Part_2',(-258.2,-71.2)),
 ('Eagle Eye','Peacekeeper',2,'中','Shoreline内(目標欄参照)','発見/監視系。詳細は目標欄とwikiを確認','なし','Eagle_Eye',None),
 ('Ill-Wisher','Mechanic',3,'中','電波塔方面(目安)','アンテナ2基を同一レイドで発見→そのレイド内で脱出まで必須','なし','Ill-Wisher',(-708.9,93.91)),
 ('No Swiping (10%)','Skier',4,'中','密輸業者基地(北エリア)','密輸業者基地で敵を10キル(残り9)','戦闘装備','No_Swiping',(-350,-270)),
 ('Wet Job - Part 1','Peacekeeper',4,'中','マップ全域','サプ付きM4A1/ADAR/TX-15でスカブ10キル','サプ付きM4A1系','Wet_Job_-_Part_1',None),
 ('Thirsty - Hounds','Jaeger',4,'中','マップ全域(22:00-7:00)','夜間限定でスカブ12キル。5時までに入るのが目安','夜戦装備','Thirsty_-_Hounds',None),
]
MAPS['Factory'] = [
 ('Black Swan','Mechanic',2,'中','地下トンネル','熱交換器3基をMS2000でマーク','MS2000マーカー×3','Black_Swan',(-2,-24.5)),
 ('All Is Revealed','Therapist',2,'中','タンクコンテナ#28(目安)','破損タンクから化学サンプルを採取','なし','All_Is_Revealed',(4.5,10.5)),
 ('Exit Here','Skier',2,'低','Factory内(目標欄参照)','脱出/場所発見系。目標欄参照','なし','Exit_Here',None),
 ('Dragnet','Jaeger',3,'中','地下のTerraGroup倉庫(Camera Bunker Door付近)','化学コンテナを回収→生還→納品','なし','Dragnet',(-20.5,23)),
 ('The Good Times - Part 1 (20%)','Prapor',5,'中','マップ全域','M4A1/M16+6B43+Kiver-M装備でPMCを10キル','M4A1 or M16・6B43・Kiver-M','The_Good_Times_-_Part_1',None),
 ('One-Way Ticket','Peacekeeper',5,'低','マップ全域','AUG使用でヘッドショット15キル','AUG','One-Way_Ticket',None),
]
MAPS['StreetsOfTarkov'] = [
 ('Cease Fire!','Jaeger',2,'中','Klimov Street脱出(通りの東端)','脱出エリア内で緑フレアを上空に発射→Survived脱出。RSP-30はメール支給','グリーンフレア(支給あり)','Cease_Fire!',(-233,33)),
 ('Audit','Ragman',2,'中','ФИНАНС(FINANCE)ビル2F','2F右手最初のオフィス、床の赤いファイルから会計メモ回収','なし','Audit',None),
 ('Population Census','Therapist',2,'中','住宅管理局の建物','住民記録のジャーナルを回収(建物内複数湧き)','なし','Population_Census',None),
 ('Beyond the Red Meat','Skier',3,'中','Belugaレストラン','シェフの日記を回収(2Fバーの棚など複数湧き)','なし(鍵は任意)','Beyond_the_Red_Meat',(-45,-52)),
 ('Glory to CPSU','Prapor',3,'中','博物館2F(任意でChekannaya 15)','プラポルの友人のジャーナルを回収→生還','なし','Glory_to_CPSU',None),
 ('Watching You','Mechanic',3,'中','Pinewoodホテル北棟 215号室','監視部屋のフラッシュドライブを回収','Pinewood hotel room 215 key','Watching_You',(-35,64)),
 ('The Secret to Productivity','Mechanic',3,'中','Hive(Malevicha 5)','水タバコラウンジに入る(死亡で最初からやり直し)','Relaxation room key','The_Secret_to_Productivity',(-212,300)),
 ('Urban Medicine','Therapist',3,'中','薬局など医療系施設(目標欄参照)','医療系の回収/納品タスク。詳細は目標欄参照','なし','Urban_Medicine',None),
 ("You've Got Mail",'Prapor',3,'中','郵便局(Post Office)エリア','郵便物/目標物を回収→生還。詳細は目標欄参照','なし',"You've_Got_Mail",None),
 ('District Patrol','Prapor',3,'中','マップ全域','Streetsでの討伐系。目標欄参照','戦闘装備','District_Patrol',None),
 ('Dandies','Ragman',3,'低','Streets内(目標欄参照)','詳細は目標欄/wiki参照','なし','Dandies',None),
 ('Secret Message','Prapor',3,'中','Streets内(目標欄参照)','回収/設置系。詳細は目標欄とwikiを確認','なし','Secret_Message',None),
 ('Revision - Streets of Tarkov','Skier',2,'中','指定された脱出ポイント','目標欄で指定された脱出から脱出するだけ。脱出リスト(下)で場所を確認','なし','Revision_-_Streets_of_Tarkov',None),
 ('Road Closed','Skier',2,'中','指定された脱出関連(目標欄参照)','脱出系タスク。Revisionと同レイドで消化しやすい','なし','Road_Closed',None),
 ('Humanitarian Supplies','Prapor',3,'中','支援物資の地点(目標欄参照)','マーク/設置系の可能性が高い。MS2000を持参推奨','MS2000マーカー(念のため)','Humanitarian_Supplies',None),
 ('Huntsman Path - Big Game','Jaeger',5,'高','LERM Expo(車ディーラー)','ボスのカバンを討伐(護衛多数、要ガチ装備)','対ボス装備','The_Huntsman_Path_-_Big_Game',(239,-60)),
]
MAPS['GroundZero'] = [
 ('Shady Contractor','Mechanic',2,'中','TerraGroup本社ビル(目安)','指定の書類/情報を回収する系。目標欄参照','なし','Shady_Contractor',(-50,0)),
 ('[KORD BREACH] Unanswered Calls','Therapist',3,'中','Ground Zero内(目標欄参照)','シーズン1タスク。発見系、目標欄参照','なし','Unanswered_Calls',None),
]
MAPS['Interchange'] = [
 ('Long Line','Ragman',3,'中','モール内外','スカブを規定数討伐(目標欄参照)。モール内が効率的','戦闘装備','Long_Line',None),
]
MAPS['Lighthouse'] = [
 ('Broadcast - Part 1','Mechanic',3,'中','Hillside〜シャレー周辺の戸建て(目安)','放送スタジオを発見(民家の地下)。ローグ地帯に注意','なし','Broadcast_-_Part_1',(-151,-243)),
]
ANYMAP = [
 ('Fall Ailment (20%)','Therapist',2,'中','指定医療品の収集・納品系。目標欄参照','Fall_Ailment'),
 ('Aid Stations (40%)','Therapist',2,'中','医療品の納品系。目標欄参照','Aid_Stations'),
 ('General Wares','Therapist',2,'中','日用品系の納品/脱出タスク。目標欄参照','General_Wares'),
 ('Bad Habit (73%)','Mechanic',2,'中','納品系。残りわずか、目標欄参照','Bad_Habit'),
 ('Rough Tarkov (50%)','Jaeger',2,'低','発見系。目標欄参照','Rough_Tarkov'),
 ('Every Hunter Knows This (50%)','Jaeger',2,'低','発見系。目標欄参照','Every_Hunter_Knows_This'),
 ('Seizing the Initiative','Peacekeeper',2,'低','脱出系。目標欄参照','Seizing_the_Initiative'),
 ('The Tarkov Shooter - Part 1','Jaeger',3,'中','ボルトアクションでスカブを規定数キル(どのマップでも可)','The_Tarkov_Shooter_-_Part_1'),
 ('Polikhim Hobo (4%)','Skier',3,'中','スカブ討伐系。目標欄参照','Polikhim_Hobo'),
 ('Balancing - Part 1 [Season PvP]','Fence',3,'中','シーズンPvPタスク。目標欄参照','Balancing_-_Part_1'),
 ('Capturing Outposts','Prapor',3,'中','拠点エリアでの討伐系。目標欄参照','Capturing_Outposts'),
 ('Power of Persuasion','Prapor',3,'低','討伐系。目標欄参照','Power_of_Persuasion'),
 ('[KORD BREACH] Uninvited Guests - Part 2','Prapor',3,'中','シーズン1タスク。指定地点訪問系','Uninvited_Guests_-_Part_2'),
 ('Hell on Earth - Part 1','Prapor',3,'中','ストーリー系。目標欄参照','Hell_on_Earth_-_Part_1'),
 ('Chumming','Skier',3,'低','脱出系。目標欄参照','Chumming'),
 ('Grenadier','Prapor',4,'中','グレネードで敵を規定数キル。Factoryのスカブ相手が効率的','Grenadier'),
]
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
  ('Outskirts','常設(サイド依存)。南西の角','a',(328,329)),
  ('UN Roadblock','常設(サイド依存)。南東の検問','a',(-527,229)),
  ('Northern UN Roadblock','常設(サイド依存)。東の道路沿い','a',(-553,-23)),
  ('RUAF Gate / RUAF Roadblock','常設・両陣営。南の道路','a',(-114,388)),
  ('ZB-016','常設。東側・Eastern Rocks付近の地下壕','a',(-383,0)),
  ('ZB-014','条件: ZB-014キーが必要','c',(410,45)),
  ('Bridge V-EX','条件: 車両脱出 5,000RUB。北東の川の橋','c',(-472,-491)),
  ('Power Line Passage','条件: シグナルゾーン内で緑フレアを真上に発射','c',(530,-85)),
  ('Friendship Bridge','条件: PMCとScavの協力脱出。北の橋','c',(27,-813)),
  ('Railway Bridge to Tarkov','条件: 地雷原マップが必要。東の鉄道橋','c',(-734,115)),
 ],
 'Shoreline': [
  ('Tunnel','常設(サイド依存)。南西の海岸道路のトンネル','a',(390,400)),
  ('Path to Lighthouse','常設+トランジット。北西エリア','a',(415,-60)),
  ('Road to Customs','常設(サイド依存)。東端の道路・川の手前','a',(-890,-35)),
  ('Railway Bridge','常設。東端の鉄道橋','a',(-1034,275)),
  ("Smuggler's Path",'条件: PMCとScavの協力。北東の桟橋','c',(-755,-195)),
  ("Climber's Trail",'条件: Red Rebel+パラコード必要。北の崖の下','c',(-58,-305)),
  ('Mountain Bunker','条件: 合言葉アイテム(Heartbeat)必要。北の崖の下','c',(-200,-305)),
  ('Road to North V-EX','条件: 車両脱出 5,000RUB。北','c',(-310,-305)),
  ('Pier Boat','条件: ボートがある時のみ。桟橋','c',(-338.6,560)),
 ],
 'Factory': [
  ('Gate 3','常設。ガラス廊下を抜けた先','a',(60,-58)),
  ('Cellars','常設。地下セラー','a',(-45,-40)),
  ('Gate 0','条件は現地確認。西側','c',(-55,60)),
  ('Office Window','条件付き。オフィス3Fの窓','c',(15,45)),
  ('Med Tent Gate','条件: 鍵が必要','c',(-18,-35)),
 ],
 'StreetsOfTarkov': [
  ('Expo Checkpoint','常設。北西','a',(232,-150)),
  ('Cardinal Apartment Parking','常設・両陣営。北端の駐車場','a',(179,-208)),
  ('Stylobate Building Elevator','常設。北東ビルの3Fエレベーター','a',(-52,-125)),
  ('Klimov Shopping Mall Exfil','常設。モール1F','a',(-72,-48)),
  ('Sewer River','常設。東側の川','a',(-144,151)),
  ('Damaged House','常設。東側','a',(-146,272)),
  ('Collapsed Crane','常設。西の工事現場','a',(232,248)),
  ('Crash Site','常設。南西','a',(296,355)),
  ('Klimov Street','条件: 緑フレアで開通(Cease Fire!と同時)。通りの東端','c',(-233,33)),
  ("Smuggler's Basement",'条件: 合言葉アイテム(Onyx)必要','c',(135,-26)),
  ('Pinewood Basement','条件: PMCとScavの協力','c',(-28,-7)),
  ('Primorsky Ave Taxi V-EX','条件: 車両脱出 5,000RUB。南端','c',(11,478)),
  ('Courtyard','条件: 緑スモークが無い時は閉鎖','c',(-57,442)),
 ],
 'GroundZero': [
  ('Nakatani Basement Stairs','常設。Nakataniビル地下階段','a',(-29,298)),
  ('Emercom Checkpoint','常設。西側の道路','a',(217,-26)),
  ('Mira Prospect','常設。北の大通り','a',(26,-61)),
  ('Police Checkpoint','常設。中央北の検問','a',(120,262)),
 ],
 'Interchange': [
  ('Railway','常設(サイド依存)。北西の線路側','a',(480,-360)),
  ('Emercom Checkpoint','常設(サイド依存)。南東の道路','a',(-330,350)),
  ('Power Station V-EX','条件: 車両脱出・支払い。北東','c',(-186.4,-318.7)),
 ],
 'Lighthouse': [
  ('Northern Checkpoint','常設。北端・トレインヤード西の道路','a',(110,-962)),
  ('Southern Road','常設。南東の海岸道路','a',(-180,450)),
  ('Path to Shoreline','常設・両陣営。東側中央の山道','a',(-260,-40)),
  ('Road to Military Base','常設系。北東の道路','a',(-250,-850)),
  ('Mountain Pass','条件: Red Rebel+パラコード必要。山道','c',(-140,100)),
  ('Side Tunnel','条件: Scav友好時など。中央南のトンネル','c',(20,330)),
  ('Armored Train','条件: 装甲列車の到着時刻のみ','c',(-30,-900)),
 ],
}
SCAV_EX = {
 'Customs': [('Factory Shacks',(352,-18)),('Warehouse 4',(333,-50)),('Old Road Gate',(255,218)),('Sniper Roadblock',(145,180)),('Railroad to Port',(-140,-30)),('Railroad to Tarkov',(-160,-230)),('Administration Gate',(655,-40)),('Military Base CP',(585,205)),('Passage Between Rocks',(622,222))],
 'Woods': [('Scav Bunker(北西)',(212,-657)),('Scav House(南西)',(381,207)),('The Boat(湖岸)',(164,202)),("Dead Man's Place",(170,235)),('Mountain Stash(両陣営)',(-212,-166)),('Eastern Rocks',(-495,-11)),('Old Railway Depot',(-440,193))],
 'Shoreline': [('Ruined Road(南西・Tunnelのすぐ南)',(400,435)),('RWing Gym Entrance(リゾート)',(-190,-70)),('Admin Basement(リゾート)',(-252,-60)),('Lighthouse(南の灯台)',(-420,590))],
 'Factory': [('Camera Bunker Door','') ,],
 'StreetsOfTarkov': [('Near Kamchatskaya Arch(西)',(283,9)),('Sewer Manhole',(279,321)),('Ventilation Shaft',(-18,408)),('Entrance to Catacombs(東)',(-146,197))],
 'GroundZero': [('Scav Checkpoint',(217,140))],
 'Interchange': [('Scav Camp(西の駐車場)',(400,-20)),('Hole in the Fence(東)',(-390,20))],
 'Lighthouse': [('Scav Hideout at the Grotto(西海岸)',(280,-380)),('Industrial Zone Gates',(-90,-840)),('Hideout under the Landing Stage(南西海岸)',(235,315)),('South Road Landside',(-230,455))],
}
SCAV_EX['Factory'] = [('Camera Bunker Door',(-20,25))]
LOOT = {
 'Customs': [('寮(マークドルーム/金庫)','鍵部屋と金庫。PvP多め','任意: Dorm room 314 marked key(高額)/203・214等の寮キー',(205,150)),('Big Red事務所','PC・インテリ書類・重役室','Tarcone Director\'s officeキー(奥はドア破壊可)',(-215,-119)),('新ガソスタ','レジ・医療・キー湧き','鍵不要',(404,31)),('旧ガソスタ2F','USECスタッシュ・武器','鍵不要',(331,-173)),('Fortress','武器箱多数+スカブ湧き','鍵不要',(201,-127))],
 'Woods': [('製材所','木箱多数+シュトゥルマンのレアキー','鍵不要',(10,-3)),('USEC Camp','武器・ミリタリー系','鍵不要',(299,-415)),('Convoy','車列・ミリタリールート','鍵不要',(168,-600)),('Scav House周辺','ジャケット・雑貨','鍵不要',(381,207))],
 'Shoreline': [('リゾート東西棟','鍵部屋にLEDX等の医療レア','要: 各部屋キー(216/226/321など。西321・東226が定番)',(-252,-100)),('Village','ツールボックス・工業系','鍵不要',(418,118)),('Gas Station','レジ・医療','鍵不要(事務所は鍵)',(-189,420)),('Scav Island','武器箱・スタッシュ','鍵不要',(216,424))],
 'Factory': [('オフィス','金庫・ファイルキャビネット','一部Factory系キー(メインは鍵不要)',(21,39)),('Rafters(3F通路)','武器箱','鍵不要',(18,4)),('Med Tent','医療系','鍵不要',(-18,-29))],
 'StreetsOfTarkov': [('Kilmovモール','店舗ルート広範囲','鍵不要',(-128,-35)),('LERM Expo','カバンのレアドロップ+車部品','鍵不要',(239,-60)),('Lexos','車部品・工業','一部部屋キーあり',(66,305)),('Cinema','雑貨・金策','鍵不要',(-175,400)),('Pinewoodホテル','鍵部屋多数','要: Pinewood各部屋キー(215など)',(-35,64))],
 'GroundZero': [('TerraGroup本社','インテリ・オフィスルート','一部オフィスキー',(-50,0)),('Tarbank','金庫・金策','一部キー(金庫室)',(43,150))],
 'Interchange': [('Techlight','電子部品(高額)','鍵不要',(91,54)),('Kiba','銃器店','要: Kiba Arms外扉+内扉キーの2本',(-18,-25)),('Goshan/IDEA/OLI','食料・雑貨・広範囲','鍵不要',(-115,-45)),('Ultra Medical','医療','鍵不要',(54,-128))],
 'Lighthouse': [('浄水場','高級ルート(ローグ注意)','鍵不要エリア多め',(-65,-600)),('Cottages','金庫・レア','要: コテージ各キー',(-162,-225)),('Train Yard','工業・武器','鍵不要',(-30,-882))],
}
EXTRA_EXNOTE = {
 'StreetsOfTarkov':'Streetsは脱出が多く位置の個体差も大きい。上記は代表例+目安。必ずOキー2連打で自分のリストを確認。',
 'Interchange':'他にRailway・Emercom Checkpoint・Saferoom(条件)などあり。位置はOキー2連打で確認。',
 'Lighthouse':'他にSide Tunnel等あり。ローグ地帯(浄水場)を通るルートは注意。',
 'GroundZero':'他にScav側共有の脱出あり。',
}

DIFF_COLOR={1:'#4ade80',2:'#a3e635',3:'#facc15',4:'#fb923c',5:'#f87171'}
SUBSPOTS = {
 ('Customs','The Extortionist'): [((372,-86),'納品カーゴの施錠小屋(Unknown Keyで開錠)')],
 ('Customs','Huntsman Path - Trophy'): [((205,140),'レシャラ湧き: 寮'),((398,25),'レシャラ湧き: 新ガソスタ'),((88,-15),'レシャラ湧き: 工事現場'),((330,-72),'レシャラ湧き: Warehouse 4棟')],
}
MAP_JA={'Customs':'CUSTOMS','Woods':'WOODS','Shoreline':'SHORELINE','Factory':'FACTORY','StreetsOfTarkov':'STREETS','GroundZero':'GROUND ZERO','Interchange':'INTERCHANGE','Lighthouse':'LIGHTHOUSE'}
def jp_url(tr,slug): return JP+quote(f"{tr}/{slug.replace('_',' ')}")

modal_data={}  # id -> dict
taskdata=[]  # for planner
sections=[]; tabs=[]
for mkey,tasks in MAPS.items():
    tasks=sorted(tasks,key=lambda t:t[2])
    p=make_pct(mkey+'.svg')
    pins=[]; rows=[]
    for i,(name,tr,diff,imp,place,desc,items,slug,anchor) in enumerate(tasks,1):
        col=DIFF_COLOR[diff]; stars='★'*diff+'☆'*(5-diff)
        tid=f'{mkey}_t{i}'
        q = quote_plus(f'Escape from Tarkov {name} location')
        modal_data[tid]={'title':f'{i}. {name}','sub':f'〔{tr}〕 難易度 {stars} / 重要度 {imp}','place':place,'desc':desc,
                         'items':linkify(items),'img':IMG+q,'map':mkey,
                         'wl':EN+quote(slug),'wt':'🖼 このタスクのwiki(写真あり)','pt':'task','pn':str(i),'pc':col}
        if anchor:
            x,y=p(*anchor)
            modal_data[tid]['x']=x; modal_data[tid]['y']=y
            pins.append(f'<button class="pin taskpin" style="left:{x}%;top:{y}%;--c:{col}" data-m="{tid}"><span class="dot">{i}</span></button>')
            for (sx,sz),slabel in SUBSPOTS.get((mkey,name),[]):
                sxp,syp = p(sx,sz)
                sid2=f'{tid}_sub{sxp}'
                modal_data[sid2]=dict(modal_data[tid]); modal_data[sid2]['sub']=slabel; modal_data[sid2]['title']=f'{i}. {name}(関連地点)'; modal_data[sid2]['place']=slabel
                pins.append(f'<button class="pin taskpin" style="left:{sxp}%;top:{syp}%;--c:{col}" data-m="{sid2}"><span class="dot sub">{i}</span></button>')
        import re as _re
        taskdata.append({'id':tid,'map':mkey,'name':name,'diff':diff,'imp':imp,'items':_re.sub('<[^>]+>','',items),'place':place})
        chk=f'<input type="checkbox" class="done" data-k="{tid}"><button class="plan" data-k="{tid}" title="レイドプランに追加">＋</button>'
        loc='' if anchor else '<span class="nopin">ピン無し</span>'
        rows.append(f'''<div class="row" data-k="{tid}">{chk}<div class="main"><span class="badge" style="--c:{col}">{i}</span><div class="tinfo"><span class="tname">{name} <small>〔{tr}〕 {loc}</small></span><span class="tmeta">難易度 <b style="color:{col}">{stars}</b>　重要度 <b>{imp}</b>　場所: {place}</span><span class="tdesc">{desc}</span><span class="tdesc"><b>必要:</b> {linkify(items)}</span></div></div><div class="links"><a href="{jp_url(tr,slug)}" target="_blank" rel="noopener">wiki</a><a href="{EN}{quote(slug)}" target="_blank" rel="noopener">EN</a></div></div>''')
    expins=[]; exrows=[]
    for j,(ename,method,etype,anchor) in enumerate(EXTRACTS.get(mkey,[]),1):
        eid=f'{mkey}_e{j}'
        cls='exa' if etype=='a' else 'exc'
        tag='常設' if etype=='a' else '条件'
        q=quote_plus(f'Escape from Tarkov {mkey} {ename} extraction')
        modal_data[eid]={'title':f'PMC脱出: {ename}','sub':('常設脱出' if etype=='a' else '条件付き/ランダム脱出'),'place':mkey,'desc':method,'items':'','img':IMG+q,'map':mkey,
          'wl':EN+WIKI_MAP[mkey]+'#Extractions','wt':f'🖼 wikiの{mkey} 脱出セクション(写真あり)','pt':('exa' if etype=='a' else 'exc'),'pn':'EX'}
        if anchor:
            x,y=p(*anchor)
            modal_data[eid]['x']=x; modal_data[eid]['y']=y
            lbl = f'<span class="exlbl{'' if etype=='a' else ' exlblc'}">{ename}</span>'
            expins.append(f'<button class="pin {'exapin' if etype=='a' else 'excpin'}" style="left:{x}%;top:{y}%" data-m="{eid}"><span class="exdot {cls}">EX</span>{lbl}</button>')
        exrows.append(f'<div class="exrow {cls}r"><span class="exbadge {cls}">{tag}</span><b>{ename}</b> — {method}</div>')
    for j,(ename,anchor) in enumerate(SCAV_EX.get(mkey,[]),1):
        sid=f'{mkey}_s{j}'
        q=quote_plus(f'Escape from Tarkov {mkey} {ename} scav extraction')
        modal_data[sid]={'title':f'SCAV脱出: {ename}','sub':'スカブ専用/共有脱出(位置は目安)','place':mkey,'desc':'スカブで出た時の脱出候補。リストはOキー2連打で確認','items':'','img':IMG+q,'map':mkey,
          'wl':EN+WIKI_MAP[mkey]+'#Extractions','wt':f'🖼 wikiの{mkey} 脱出セクション(写真あり)','pt':'scav','pn':'S'}
        if anchor:
            x,y=p(*anchor)
            modal_data[sid]['x']=x; modal_data[sid]['y']=y
            expins.append(f'<button class="pin scavpin hid" style="left:{x}%;top:{y}%" data-m="{sid}"><span class="exdot exs">S</span><span class="exlbl exlbls">{ename}</span></button>')
    lootrows=[]
    for j,(lname,ldesc,lkey,anchor) in enumerate(LOOT.get(mkey,[]),1):
        lid=f'{mkey}_l{j}'
        q=quote_plus(f'Escape from Tarkov {mkey} {lname} loot')
        modal_data[lid]={'title':f'金策: {lname}','sub':'アイテム漁りスポット','place':mkey,'desc':ldesc,'items':linkify(lkey),'img':IMG+q,'map':mkey,
          'wl':EN+WIKI_MAP[mkey],'wt':f'🖼 wikiの{mkey} マップページ','pt':'loot','pn':'$'}
        x,y=p(*anchor)
        modal_data[lid]['x']=x; modal_data[lid]['y']=y
        expins.append(f'<button class="pin lootpin hid" style="left:{x}%;top:{y}%" data-m="{lid}"><span class="exdot exl">$</span></button>')
        lootrows.append(f'<div class="exrow lootr"><span class="exbadge exl2">$</span><b>{lname}</b> — {ldesc}<br><small>鍵: {linkify(lkey)}</small></div>')
    exnote=EXTRA_EXNOTE.get(mkey,'')
    W,H=dims[mkey]
    tabs.append(f'<button class="tab" data-t="{mkey}">{MAP_JA[mkey]}<small>({len(tasks)})</small></button>')
    sections.append(f'''<section id="{mkey}" class="mapsec">
<div class="mapbar">
<div class="grp"><button class="mbtn zout">−</button><button class="mbtn zin">＋</button><button class="mbtn fsb">⛶</button></div>
<div class="grp layers">
<button class="mbtn tgl on" data-g="taskpin"><i class="sw" style="--c:#a3e635"></i>タスク</button>
<button class="mbtn tgl on" data-g="exapin"><i class="sw sq" style="--c:#1eae4e"></i>常設EX</button>
<button class="mbtn tgl on" data-g="excpin"><i class="sw sq" style="--c:#e8a33d"></i>条件EX</button>
<button class="mbtn tgl" data-g="scavpin"><i class="sw" style="--c:#2f86d6"></i>SCAV</button>
<button class="mbtn tgl" data-g="lootpin"><i class="sw" style="--c:#d9a521"></i>金策</button>
</div></div>
<div class="map-wrap"><div class="map" data-map="{mkey}" style="aspect-ratio:{W}/{H}"><img loading="lazy" src="map_{mkey}.jpg" alt="{mkey}">{''.join(pins)}{''.join(expins)}</div></div>
<div class="list"><h3>タスク一覧(難易度順) <small>チェックで完了管理 / wikiリンクはここから</small></h3>{''.join(rows)}
<h3>脱出ポイントと方法 <small>※位置は目安あり。レイド中にOキー2連打で必ず確認</small></h3>
<p class="note"><a class="il" href="{EN}{WIKI_MAP[mkey]}#Extractions" target="_blank" rel="noopener">🖼 wikiの{mkey} 脱出セクションを開く(全脱出の写真つき一覧)</a></p>{''.join(exrows)}{f'<p class="note">{exnote}</p>' if exnote else ''}
<h3>金策スポットと必要な鍵 <small>マップの「金策」レイヤーで位置表示</small></h3>{''.join(lootrows)}</div></section>''')

anyrows=[]
for i,(name,tr,diff,imp,desc,slug) in enumerate(sorted(ANYMAP,key=lambda t:t[2]),1):
    col=DIFF_COLOR[diff]; stars='★'*diff+'☆'*(5-diff); tid=f'any_t{i}'
    anyrows.append(f'''<div class="row" data-k="{tid}"><input type="checkbox" class="done" data-k="{tid}"><div class="main"><span class="badge" style="--c:{col}">{i}</span><div class="tinfo"><span class="tname">{name} <small>〔{tr}〕</small></span><span class="tmeta">難易度 <b style="color:{col}">{stars}</b>　重要度 <b>{imp}</b></span><span class="tdesc">{desc}</span></div></div><div class="links"><a href="{jp_url(tr,slug)}" target="_blank" rel="noopener">wiki</a><a href="{EN}{quote(slug)}" target="_blank" rel="noopener">EN</a></div></div>''')
tabs.append(f'<button class="tab" data-t="anymap">ANY MAP<small>({len(ANYMAP)})</small></button>')
sections.append(f'<section id="anymap" class="mapsec"><div class="list"><p class="note">場所指定なし。各マップと並行で自然に進むものが多い。新タスクはリンク先とゲーム内目標欄を正として。</p>{"".join(anyrows)}</div></section>')

shop = f'''<section id="shop" class="mapsec"><div class="list">
<h3>共通消耗品</h3><p class="note">{linkify('MS2000マーカー')}×7以上(Customs1・Woods2・Shoreline1・Factory3/スペシャルスロット推奨)　/　{linkify('グリーンフレア')}×1(Cease Fire!はメール支給あり、無い時の予備)</p>
<h3>鍵</h3><p class="note">{linkify('Dorm room 220キー')}(Chemical納品用)　/　{linkify("Company director's room key")}(Shipment)　/　{linkify('Health Resort office key')}(Chemistry Closet)　/　{linkify('Pinewood hotel room 215 key')}(Watching You)　/　{linkify('Relaxation room key')}(Productivity)</p>
<h3>設置・納品アイテム</h3><p class="note">{linkify('6L31 60連')}×2(Ice Cream Cones)　/　{linkify('Ghostバラクラバ')}+{linkify('緑シュマグ')}+{linkify('RayBench')}+{linkify('丸フレームサングラス')}(Gratitude)　/　{linkify('7.62x51パック')}×1(Break the Deal。ELCANは所持済)</p>
<h3>装備指定タスク用(後回しOK)</h3><p class="note">サプ付き{linkify('M4A1')}/ADAR(Wet Job)　/　{linkify('M4A1')} or M16+{linkify('6B43')}+{linkify('Kiver-M')}(Good Times)　/　{linkify('AUG')}(One-Way Ticket)　/　ボルトアクション(Tarkov Shooter)　/　{linkify('HK MP5')}+パーツ(Gunsmith)</p>
<h3>優先攻略順の目安</h3><p class="note">① Customsの緑ピン消化 → ② Woodsの設置系を1〜2レイド → ③ ShorelineのMaster Key(PKレピュ+0.1)+リゾート系 → ④ Factory地下マーク系を1レイド → ⑤ Streets回収系 → ★5ボス系は装備と資金が整ってから</p>
</div></section>'''

GUN = lambda slug,name: f'<a class="il" href="{EN}{quote(slug)}" target="_blank" rel="noopener">{name}</a>'
weapons_html = f"""<section id="weapons" class="mapsec"><div class="list">
<p class="note">レベル15前後・トレーダーLL2(Skier LL3未解放)・フリマは一部アイテムのみ購入可、の前提。トレーダー在庫と解放条件はパッチで変わるので、無ければパーツ名でフリマ検索→レベル表記を確認。</p>

<h3>弾薬早見表(口径別おすすめ) <small>貫通値はおおよそ。上=今すぐ買える / 下=解放されたら移行</small></h3>
<p class="note"><b>5.45x39(AK-74系):</b> 今→ <b>PS</b>(貫通~28・クラス3まで) / 次→ <b>PP</b>(~30前後) / 目標→ <b>BT</b>(~40台・クラス4安定)→<b>BS</b>(最上位・Prapor LL3バーター)。フルオート適性が高くマグのスタック詰め(上に貫通弾)と好相性</p>
<p class="note"><b>7.62x39(AKM/SKS):</b> 今→ <b>PS</b>(貫通~32・序盤最強の安弾) / 目標→ <b>BP</b>(~45前後・高火力貫通)。一発の肉ダメージが重く、タップ撃ちで真価</p>
<p class="note"><b>9x19(MPX/MP5/ピストル):</b> 今→ <b>PST gzh</b>(~20・非装甲/脚用) / 目標→ <b>AP 6.3</b>(~30・ようやく装甲に届く)。装甲相手は脚か顔限定と割り切る</p>
<p class="note"><b>12ゲージ(ショットガン):</b> 今→ <b>フレシェット</b>(~26×8粒・近距離で装甲ごと溶かす) / スラグなら <b>AP-20</b>(~37・単発高貫通)。屋内最強枠</p>
<p class="note"><b>7.62x54R(モシン/SVD):</b> 今→ <b>LPS gzh</b>(~37・ヘルメット貫通ワンパン狙い) / 目標→ <b>SNB</b>(~60台・対重装甲)。頭を狙う武器なので安弾でも仕事する</p>
<p class="note"><b>5.56x45(M4/ADAR/AUG):</b> 今→ <b>M855</b>(~27) / 目標→ <b>M855A1</b>(~40台)→<b>M995</b>(最上位)。Wet Job/One-Way Ticket着手時に用意</p>
<p class="note"><b>.366(VPO系・番外):</b> <b>AP-M</b>(~40台)が「安い銃で高貫通」の抜け道枠。低予算で装甲PMCに対抗したい時の選択肢</p>
<p class="note" style="border-left:3px solid #c98f2c"><b>原則:</b> 迷ったら「貫通30以上を上に5〜10発+安弾を下に」のスタック詰め。貫通が敵アーマークラス×10を超えてれば概ね抜ける、が目安</p>
<h3>① メイン: AK-74N「現行ビルド」 <small>反動61 / エルゴ49.8 — 完成済み</small></h3>
<p class="note"><b>構成:</b> {GUN('Kalashnikov_AK-74N_5.45x39_assault_rifle','AK-74N')} + RRD-4Cマズル(拾い物・死亡ロスト注意) + M-LOKハンドガード + RK-4フォアグリップ + SAWグリップ + EKP-1S-03サイト + 6L20 30連<br>
<b>弾:</b> 5.45 PS(貫通28)。PP/BT弾が解放され次第マグ上部にスタック積み<br>
<b>運用:</b> タスク攻略レイド用。Prapor保険必須。プリセット登録してロスト時の復旧を楽に<br>
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
<b>運用:</b> 寮タスク・Factory・屋内CQB。Angry Watchman系のPMC狩りと相性◎</p>

<h3>⑤ 遠距離+タスク兼用: モシン <small>2万以下 / コスパ最強スナイパー</small></h3>
<p class="note"><b>構成:</b> {GUN('Mosin_7.62x54R_bolt-action_rifle_(Sniper)','モシン(スナイパー)')}素のまま or PUスコープ<br>
<b>弾:</b> 7.62x54R LPS Gzh — 頭に当てればヘルメット貫通でワンパン<br>
<b>運用:</b> メインロード監視・待ち伏せ。The Tarkov Shooter Part 1(ボルトアクションでスカブキル)がそのまま進む一石二鳥枠</p>

<h3>⑥ 番外: MPX 脚撃ち <small>装甲PMC相手は脚 or 顔限定</small></h3>
<p class="note"><b>弾:</b> 9x19の安弾は貫通20前後で装甲に無力。高レートで脚を溶かすレグメタ運用専用<br>
<b>運用:</b> 屋内の割り切り運用のみ。基本は③AKMを推奨</p>

<h3>⑦ タスク装備メモ(揃えるのは後でOK)</h3>
<p class="note">Wet Job P1 = サプ付き{GUN('Colt_M4A1_5.56x45_assault_rifle','M4A1')}/ADAR系でスカブ10 / One-Way Ticket = {GUN('Steyr_AUG_A3_5.56x45_assault_rifle','AUG')}でHS15 / Good Times P1 = M4orM16 + {GUN('6B43_Zabralo-Sh_body_armor','6B43')} + {GUN('Kiver-M_bulletproof_helmet','Kiver-M')}でPMC10 / Gunsmith = {GUN('HK_MP5_9x19_submachine_gun_(Navy_3_Round_Burst)','HK MP5')}改造 — いずれも装備コストが重いので、レベルと資金が乗ってから着手</p>

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
<b>B(売却/納品):</b> その他の注射器は基本フリマ売り or タスク・ハイドアウト(スティム系要求)用にキープ。<b>注射器ケース</b>が作れるようになったら集める価値が跳ね上がる</p>
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
<h3>タスク納品で頻出(見つけたらキープ)</h3>
<p class="note">{GUN('Gas_analyzer','ガスアナライザー')} / {GUN('Corrugated_hose','コルゲートホース')} / {GUN('Military_power_filter','軍用フィルター類')} / {GUN('Fire_control_computer','FireControl系電子機器')} / ドッグタッグ(Skierタスク・BDタグはサークル用) / 各種キー(使い道不明でも一旦キープ→wikiで確認)</p>
<h3>バーター素材(トレーダー交換で化ける)</h3>
<p class="note">タバコ({GUN('Pack_of_Malboro_cigarettes','マルボロ')}等)・{GUN('Condensed_milk','コンデンスミルク')}・{GUN('Emelya_rye_croutons','クルトン')}などの食品 / {GUN('Golden_neck_chain','金のチェーン')}・{GUN('Chainlet','チェーンレット')}などの貴金属 — 換金前にトレーダーのバーター一覧を確認すると得することが多い</p>
<p class="note" style="border-left:3px solid #c98f2c">判断に迷ったら: アイテム検査画面の「関連品目を検索」でタスク/ハイドアウト/バーターの用途が見られる。1スロあたり2万ルーブル以上なら持ち帰り優先</p>
</div></section>"""
sections.append(keep_html)
tabs.append('<button class="tab" data-t="keep">KEEP</button>')

keys_html = f"""<section id="keys" class="mapsec"><div class="list">
<h3>今のタスクで必要な鍵(最優先で確保)</h3>
<p class="note">{GUN('Dorm_room_220_key','Dorm room 220')} — Chemical P1の納品用(Customs) / {GUN("Company_director's_room_key","Company director room key")} — Shipment Tracking(Customsボイラー棟2F) / {GUN('Health_Resort_office_key_with_a_blue_tape','Health Resort office 青テープ')} — Chemistry Closet(Shorelineリゾート東110) / {GUN('Pinewood_hotel_room_215_key','Pinewood hotel 215')} — Watching You(Streets) / {GUN('Relaxation_room_key','Relaxation room')} — The Secret to Productivity(Streets/Hive)。いずれもフリマ購入可・使っても消えないのでセキュア常備</p>
<h3>汎用性が高い「買って損しない」鍵</h3>
<p class="note"><b>{GUN('Factory_exit_key','Factory exit key')}</b> — 最重要。CustomsのZB-1013脱出+Factoryの脱出+複数タスクで使う万能鍵。使用回数制なので予備も視野<br>
<b>{GUN("Tarcone_Director's_office_room_key","Tarcone Director office key")}</b> — Big Red事務所(PC・インテリ)。Farming系タスクでも再登場しがち<br>
<b>{GUN('Dorm_room_314_marked_key','Dorm room 314 Marked key')}</b> — Customs寮のマークドルーム。高額だがレア武器・ケース抽選。金策フェーズ向け<br>
<b>{GUN('Machinery_key','Machinery key')}</b> — Customs各所+タスク再利用。レイド内(寮205ジャケット)で無料入手可</p>
<h3>マップ別・金策鍵の定番</h3>
<p class="note"><b>Shoreline:</b> リゾート部屋キー(西321・東226・東310あたりが定番。LEDX/医療レア抽選)— 相場と回転率をフリマで確認してから<br>
<b>Interchange:</b> {GUN('Kiba_Arms_International_outer_door_key','Kiba外扉')}+{GUN('Kiba_Arms_inner_grate_door_key','Kiba内扉')}の2本セットで銃器店<br>
<b>Woods:</b> {GUN('ZB-014_key','ZB-014')} — 脱出兼スタッシュ<br>
<b>Lighthouse:</b> コテージ各キー(金庫・レア) / <b>Streets:</b> アパート系キーは当たり外れ大きいので後回しでOK</p>
<h3>レイド内で拾う系(買わない)</h3>
<p class="note">{GUN('Unknown_key','Unknown key')} — Extortionist(死体から) / Machinery key(寮205) / その他「用途不明の鍵」は一旦キープ→検査画面の「関連品目を検索」かwikiで開く扉を確認してから売る</p>
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
<b>インテリセンター:</b> 電子系({GUN('Phased_array_element','電子部品類')}・{GUN('Military_cable','ミリタリーケーブル')})+家具系。Lv2でタスク報酬+5%とスカブ帰還短縮の神施設<br>
<b>水収集器+栄養ユニット:</b> {GUN('Water_filter','浄水フィルター')}(建設+稼働の両方で消費。フリマで見たら買い)+{GUN('Corrugated_hose','コルゲートホース')} — 浄水(Superwater)生産は序盤の安定金策</p>
<h3>快適系(急がないが素材はキープ)</h3>
<p class="note"><b>換気/空気清浄:</b> エアフィルター類 / <b>セキュリティLv2-3:</b> 電線・{GUN('Analog_thermometer','計器類')}・軍用電子系 / <b>暖房・照明Lv上げ:</b> 電球・{GUN('Dry_fuel','燃料類')} — {GUN('Metal_fuel_tank','燃料タンク')}と{GUN('Expeditionary_fuel_tank','遠征燃料タンク')}は発電機の稼働に常時必要なので、空でもキープして詰め替え運用</p>
<h3>運用のコツ</h3>
<p class="note">① 倉庫を「ハイドアウト素材箱」として1列確保して上記を集約 ② 各ステーションの要求はゲーム内で📌ピン留めすると採集リストに出て便利 ③ 迷ったら検査画面の「関連品目を検索」→HIDEOUTタブで使用先が見える ④ 売っていいのは「同じ物が3個以上余ってる時の余剰分」だけ、が安全ルール</p>
</div></section>"""
sections.append(hideout_html)
tabs.append('<button class="tab" data-t="hideout">HIDEOUT</button>')




tabs.append('<button class="tab" data-t="shop">ITEMS</button>')
sections.append(shop)

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
.hint{font-size:10.5px;color:#8a8375}
.map-wrap{position:relative;overflow:hidden;height:74vh;border:1px solid var(--line);border-radius:4px;touch-action:none;overscroll-behavior:contain;cursor:grab;background:#0a0c0e}
.map-wrap.fs{position:fixed;inset:0;z-index:45;height:100dvh;max-height:none;border:none;border-radius:0}
.map-wrap.fs.rot{width:100dvh;height:100dvw;inset:auto;top:50%;left:50%;transform:translate(-50%,-50%) rotate(90deg)}
#fsx{display:none;position:fixed;top:calc(10px + env(safe-area-inset-top));right:12px;z-index:49;width:46px;height:46px;border-radius:50%;background:#000d;border:1px solid var(--amber);color:#fff;font-size:20px}
body.fsmode #fsx{display:block}
#fstab{display:none;position:fixed;top:50%;right:0;transform:translateY(-50%);z-index:48;background:#15181dee;border:1px solid var(--amber);border-right:none;border-radius:8px 0 0 8px;color:var(--tanb);padding:14px 7px;font-size:12px;writing-mode:vertical-rl;letter-spacing:.2em}
body.fsmode #fstab{display:block}
#fsdrawer{position:fixed;top:0;right:-290px;bottom:0;width:278px;z-index:48;background:#15181df7;border-left:1px solid var(--amber);overflow:auto;transition:right .18s;padding:calc(12px + env(safe-area-inset-top)) 10px 24px}
#fsdrawer.open{right:0}
#fsdrawer h5{color:var(--amber);font-size:11px;letter-spacing:.2em;margin:0 0 6px}
#fsdrawer .fi{display:flex;gap:9px;padding:9px 6px;border:none;border-bottom:1px solid var(--line);align-items:flex-start;width:100%;background:none;color:var(--tanb);text-align:left;font-size:12px;line-height:1.45}
#fsdrawer .fb{flex:0 0 22px;height:22px;border-radius:50%;color:#111;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:11px;margin-top:1px}
#fsdrawer .fi small{display:block;color:#9a927e;font-size:10.5px}
body.fsmode #modal{align-items:flex-start;justify-content:flex-start;padding:10px}
body.fsmode .mbox{max-width:330px;max-height:72vh;font-size:12px}
.map-wrap.fs .fsclose{display:none}
.fsclose{display:none;position:fixed;top:12px;right:12px;z-index:46;width:44px;height:44px;border-radius:50%;background:#000c;border:1px solid var(--amber);color:#fff;font-size:20px}
.map-wrap.fs .fsclose{display:block}
.map{position:absolute;left:0;top:0;width:100%;transform-origin:0 0;will-change:transform}
.map img{display:block;width:100%;height:auto}
.pin{position:absolute;transform:translate(-50%,-50%);background:none;border:none;padding:6px;cursor:pointer;z-index:2}
.pin .dot.sub{width:19px;height:19px;font-size:10.5px;background:transparent;color:var(--c);border:2px dashed var(--c);box-shadow:0 0 0 1px #000}
.pin .dot{display:flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;background:var(--c);color:#111;font-weight:800;font-size:12.5px;border:2px solid #111;box-shadow:0 0 0 1.5px rgba(255,255,255,.6),0 2px 6px rgba(0,0,0,.6)}
.pin:active .dot,.pin:hover .dot{transform:scale(1.35)}
.exdot{display:flex;align-items:center;justify-content:center;width:22px;height:22px;color:#fff;font-weight:800;font-size:10px;border:2px solid #fff;border-radius:3px;box-shadow:0 2px 6px rgba(0,0,0,.6)}
.exa{background:#1eae4e}.exc{background:#e8a33d;color:#111}
.exs{background:#2f86d6;border-radius:50%}.exl{background:#d9a521;color:#111;border-radius:50%;font-size:12px}
.exar{border-left-color:#1eae4e}.excr{border-left-color:#e8a33d}
.exbadge.exa{background:#1eae4e}.exbadge.exc{background:#e8a33d;color:#111}
.hid{display:none}
.exlbl{position:absolute;left:calc(100% - 3px);top:50%;transform:translateY(-50%);font-size:10.5px;font-weight:700;color:#7dffab;white-space:nowrap;text-shadow:0 1px 2px #000,0 -1px 2px #000,1px 0 2px #000,-1px 0 2px #000;pointer-events:none}
.exlblc{color:#ffc46b}
.exlbls{color:#8ec9ff}
@media(max-width:640px){.exlbl{font-size:9px}}

.pin:active .exdot,.pin:hover .exdot{transform:scale(1.35)}
.list{max-width:1100px;margin:14px auto 26px;padding:0 2px}
.list h3{font-size:12px;letter-spacing:.15em;color:var(--tanb);margin:16px 0 8px;border-left:3px solid var(--amber);padding-left:8px}
.list h3 small{color:#8a8375;font-weight:400;letter-spacing:0}
.row{display:flex;gap:8px;margin-bottom:6px;align-items:stretch}
.row.off{opacity:.38}
.done{width:22px;height:22px;margin-top:10px;accent-color:var(--amber);flex:0 0 auto}
.main{flex:1;display:flex;gap:10px;padding:8px 10px;border:1px solid var(--line);border-radius:4px;background:var(--panel)}
.badge{flex:0 0 25px;height:25px;border-radius:50%;background:var(--c);color:#111;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;margin-top:2px}
.tinfo{display:flex;flex-direction:column;gap:2px;min-width:0}
.tname{color:var(--tanb);font-weight:700;font-size:13.5px}
.tname small{color:#8a8375;font-weight:400}
.tmeta{font-size:11.5px}
.tdesc{font-size:11.5px;color:#9a927e;line-height:1.55}
.links{display:flex;flex-direction:column;gap:4px;justify-content:center}
.links a{display:block;text-align:center;border:1px solid var(--line);border-radius:3px;color:var(--amber);font-size:11px;text-decoration:none;padding:4px 9px;background:var(--panel)}
.links a:active,.links a:hover{border-color:var(--amber)}
.il{color:var(--amber);text-decoration:underline;text-underline-offset:2px}
.nopin{color:#6b6455;font-size:10px;border:1px solid #3a3e46;border-radius:3px;padding:0 4px}
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
.tname small{display:block;margin-top:1px}
.row{flex-wrap:wrap}.links{flex-direction:row;width:100%;justify-content:flex-end}
#modal{align-items:flex-end;padding:0}
.mbox{max-width:100%;border-radius:12px 12px 0 0;border-bottom:none;max-height:86vh}
.pin .dot{width:27px;height:27px;font-size:13.5px}
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
.plan{width:34px;height:34px;margin-top:4px;border-radius:4px;border:1px solid var(--line);background:var(--panel);color:#8a8375;font-size:16px;flex:0 0 auto;cursor:pointer}
.plan.on{border-color:#3ddc78;color:#3ddc78;background:#16241b}
#planbar{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(12px + env(safe-area-inset-bottom));z-index:44;display:none;gap:8px;align-items:center;background:#15181df2;border:1px solid var(--amber);border-radius:24px;padding:8px 14px;box-shadow:0 6px 20px #000a;max-width:94vw;flex-wrap:wrap;justify-content:center}
#planbar button{background:#242a24;border:1px solid #3ddc78;color:#d9f5e2;border-radius:16px;padding:6px 12px;font-size:12px}
#plancount{color:var(--tanb);font-size:12.5px;font-weight:700}
#planpanel{position:fixed;left:0;right:0;bottom:0;max-height:80vh;overflow:auto;background:#15181d;border-top:2px solid var(--amber);z-index:55;display:none;border-radius:12px 12px 0 0;box-shadow:0 -8px 30px #000c}
.pp-head{display:flex;justify-content:space-between;align-items:center;padding:12px 16px;border-bottom:1px solid var(--line);color:var(--tanb)}
.pp-head button{background:none;border:1px solid var(--line);color:var(--tan);border-radius:4px;font-size:18px;padding:6px 14px;min-width:44px}
#planbody,.pp-body{padding:12px 16px calc(24px + env(safe-area-inset-bottom))}
#planbody h4{color:var(--amber);font-size:13px;margin:10px 0 6px;letter-spacing:.1em}
#planbody .pt{font-size:12.5px;color:var(--tanb);padding:4px 0;border-bottom:1px dashed var(--line)}
#planbody .pt small{color:#9a927e;display:block}
#planbody .items{background:#0d0f12;border:1px solid var(--line);border-radius:5px;padding:9px 11px;font-size:12.5px;line-height:1.7;margin-top:8px;color:var(--tanb)}
.pp-btns{display:flex;gap:8px;margin-top:8px}
.pp-btns button{flex:1;height:38px;background:#242a24;border:1px solid var(--amber);color:var(--tanb);border-radius:4px;font-size:13px}
.pin{transform:translate(-50%,-50%) scale(calc(1/var(--s,1)))}
.map.zoomout .exlbl{display:none}
@media(max-width:640px){#q{flex:1 1 140px}}
'''

js='''
const S=(()=>{try{const t=window.localStorage;t.setItem("_t","1");t.removeItem("_t");return t}catch(e){return null}})();
const MD=__MD__;
const TD=__TD__;
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
  if(mhh<H){ty=(H-mhh)/2}
  if(window.innerWidth<640){zoomAt(wrap.clientWidth/2,wrap.clientHeight/2,1.8)}else{apply()}
 });
 sec.querySelector(".zin")?.addEventListener("click",()=>zoomAt(wrap.clientWidth/2,wrap.clientHeight/2,1.35));
 sec.querySelector(".zout")?.addEventListener("click",()=>zoomAt(wrap.clientWidth/2,wrap.clientHeight/2,1/1.35));
 const updRot=()=>{wrap.classList.toggle("rot",
   wrap.classList.contains("fs")&&!document.fullscreenElement&&window.innerHeight>window.innerWidth)};
 sec.querySelector(".fsb")?.addEventListener("click",async()=>{
  wrap.classList.add("fs");document.body.style.overflow="hidden";document.body.classList.add("fsmode");
  window._fsExit=exitFs;fillDrawer(sec.id);
  try{await wrap.requestFullscreen();}catch(e){}
  try{await screen.orientation.lock("landscape");}catch(e){}
  updRot();apply();
 });
 const exitFs=()=>{wrap.classList.remove("fs","rot");document.body.style.overflow="";document.body.classList.remove("fsmode");
  document.getElementById("fsdrawer").classList.remove("open");
  try{screen.orientation.unlock&&screen.orientation.unlock()}catch(e){}
  if(document.fullscreenElement){document.exitFullscreen().catch(()=>{})}
  apply();};
 window.addEventListener("resize",()=>{if(wrap.classList.contains("fs")){updRot();apply()}});
 document.addEventListener("fullscreenchange",()=>{if(wrap.classList.contains("fs")){updRot();
  if(!document.fullscreenElement&&!document.body.classList.contains("fsmode")){wrap.classList.remove("fs","rot")}}});
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
 wrap.addEventListener("mousedown",e=>{if(e.target.closest(".pin")||e.target.closest(".fsclose"))return;
  const[x,y]=pos(e);mdrag={x,y,tx,ty};wrap.style.cursor="grabbing"});
 window.addEventListener("mousemove",e=>{if(mdrag){const[x,y]=pos(e);tx=mdrag.tx+(x-mdrag.x);ty=mdrag.ty+(y-mdrag.y);apply()}});
 window.addEventListener("mouseup",()=>{mdrag=null;wrap.style.cursor="grab"});
 wrap.addEventListener("wheel",e=>{e.preventDefault();const[x,y]=pos(e);zoomAt(x,y,e.deltaY<0?1.15:1/1.15)},{passive:false});
});
document.querySelectorAll(".tgl").forEach(b=>b.addEventListener("click",()=>{
 const sec=b.closest(".mapsec");b.classList.toggle("on");
 sec.querySelectorAll("."+b.dataset.g).forEach(p=>p.classList.toggle("hid",!b.classList.contains("on")));
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
const DC={1:"#4ade80",2:"#a3e635",3:"#facc15",4:"#fb923c",5:"#f87171"};
const fsx=document.createElement("button");fsx.id="fsx";fsx.textContent="✕";document.body.appendChild(fsx);
fsx.onclick=()=>window._fsExit&&window._fsExit();
const fstab=document.createElement("button");fstab.id="fstab";fstab.textContent="タスク一覧";document.body.appendChild(fstab);
const fsdrawer=document.createElement("div");fsdrawer.id="fsdrawer";document.body.appendChild(fsdrawer);
fstab.onclick=()=>fsdrawer.classList.toggle("open");
function fillDrawer(mkey){
 const list=TD.filter(t=>t.map===mkey).sort((a,b)=>a.diff-b.diff);
 fsdrawer.innerHTML="<h5>"+mkey+" TASKS</h5>";
 list.forEach((t,i)=>{const b=document.createElement("button");b.className="fi";
  b.innerHTML=`<span class="fb" style="background:${DC[t.diff]}">${i+1}</span><span>${t.name}<small>${t.place}</small></span>`;
  b.onclick=()=>{const d=MD[t.id];if(d)showM(d);fsdrawer.classList.remove("open")};
  fsdrawer.appendChild(b)});
 if(!list.length)fsdrawer.innerHTML+='<p style="font-size:12px;color:#8a8375">このマップのタスクは無し</p>';
}
modal.addEventListener("click",e=>{if(e.target===modal)modal.classList.remove("on")});
document.getElementById("mc").addEventListener("click",()=>modal.classList.remove("on"));
// progress checkboxes
document.querySelectorAll(".done").forEach(c=>{
 const k="eft_"+c.dataset.k;
 if(S&&S.getItem(k)==="1"){c.checked=true;c.closest(".row").classList.add("off")}
 c.addEventListener("change",()=>{c.closest(".row").classList.toggle("off",c.checked);if(S){c.checked?S.setItem(k,"1"):S.removeItem(k)}});
});
'''
md_json=json.dumps(modal_data,ensure_ascii=False)
js = js + '''
// ---- service worker ----
if("serviceWorker" in navigator){navigator.serviceWorker.register("sw.js").catch(()=>{})}
// ---- helpers ----
const store={get:k=>{try{return localStorage.getItem(k)}catch(e){return null}},
 set:(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}},del:k=>{try{localStorage.removeItem(k)}catch(e){}},
 keys:()=>{try{return Object.keys(localStorage).filter(k=>k.startsWith("eft_"))}catch(e){return[]}}};
function openTab(t){document.querySelector(`.tab[data-t="${t}"]`)?.click()}
// ---- search ----
const q=document.getElementById("q"),qd=document.getElementById("qdrop");
const INDEX=[];
document.querySelectorAll(".mapsec").forEach(sec=>{
 const tab=sec.id;
 sec.querySelectorAll(".row").forEach(r=>{const n=r.querySelector(".tname");if(n)INDEX.push({t:n.textContent.trim(),tab,el:r,kind:"タスク"})});
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
// ---- raid planner ----
const planbar=document.getElementById("planbar"),plancount=document.getElementById("plancount"),
 planpanel=document.getElementById("planpanel"),planbody=document.getElementById("planbody");
const planSet=new Set((store.get("eft_plan")||"").split(",").filter(Boolean));
function planSave(){store.set("eft_plan",[...planSet].join(","))}
function planRefresh(){
 document.querySelectorAll(".plan").forEach(b=>b.classList.toggle("on",planSet.has(b.dataset.k)));
 planbar.style.display=planSet.size?"flex":"none";
 plancount.textContent=`プラン: ${planSet.size}件`;
 // filter pins when plan active? keep all visible; highlight planned
 document.querySelectorAll(".pin.taskpin").forEach(p=>{
  const base=p.dataset.m.split("_sub")[0];
  p.style.opacity=(planSet.size&&!planSet.has(base))?".28":"1"});
}
document.querySelectorAll(".plan").forEach(b=>b.addEventListener("click",()=>{
 const k=b.dataset.k;planSet.has(k)?planSet.delete(k):planSet.add(k);planSave();planRefresh()}));
function renderPlan(list,title){
 const byMap={};list.forEach(t=>{(byMap[t.map]=byMap[t.map]||[]).push(t)});
 let html=`<h4>${title}</h4>`;const items=new Set();
 for(const m in byMap){html+=`<h4>▸ ${m}</h4>`;
  byMap[m].sort((a,b)=>a.diff-b.diff).forEach(t=>{
   html+=`<div class="pt">${"★".repeat(t.diff)} ${t.name}<small>${t.place} / 重要度${t.imp}</small></div>`;
   if(t.items&&t.items!=="なし")t.items.split(/[・、\\/]|(?:　)/).forEach(x=>{x=x.trim();if(x&&!x.startsWith("なし"))items.add(x)});
  })}
 html+=`<div class="items"><b>持ち物まとめ:</b><br>${[...items].map(i=>"・"+i).join("<br>")||"特になし"}</div>`;
 planbody.innerHTML=html;planpanel.style.display="block";
}
document.getElementById("planopen").onclick=()=>{
 renderPlan(TD.filter(t=>planSet.has(t.id)),"選択中のタスク")};
document.getElementById("planclose").onclick=()=>planpanel.style.display="none";
// ---- auto recommendation ----
document.getElementById("planreco").onclick=()=>{
 const undone=TD.filter(t=>store.get("eft_"+t.id)!=="1");
 const score={};undone.forEach(t=>{score[t.map]=(score[t.map]||0)+(6-t.diff)+(t.imp==="高"?2:t.imp==="中"?1:0)});
 const best=Object.entries(score).sort((a,b)=>b[1]-a[1])[0];
 if(!best){planbody.innerHTML="<h4>未完了タスクなし!全部終わってる🎉</h4>";planpanel.style.display="block";return}
 const picks=undone.filter(t=>t.map===best[0]).sort((a,b)=>a.diff-b.diff).slice(0,6);
 renderPlan(picks,`おすすめ: ${best[0]} レイド(未完了${undone.filter(t=>t.map===best[0]).length}件から易しい順)`);
 openTab(best[0]);
};
planRefresh();
'''
md_td = json.dumps(taskdata, ensure_ascii=False)
html=f'''<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<link rel="manifest" href="manifest.json"><meta name="theme-color" content="#14161a">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="apple-touch-icon" href="icon-192.png"><title>Tarkov タスク&脱出マップ</title><style>{css}</style></head><body>
<header><h1>Tarkov Task &amp; Extract Map <small style="color:#8a8375;font-size:11px;letter-spacing:0">{BUILD_VER}</small></h1></header>
<nav><input id="q" type="search" placeholder="検索: タスク/鍵/脱出/アイテム" autocomplete="off">{''.join(tabs)}</nav>
<div id="qdrop"></div>
<div id="planbar"><span id="plancount"></span><button id="planopen">プランを見る</button><button id="planreco">おすすめレイド提案</button></div>
<div id="planpanel"><div class="pp-head"><b>レイドプラン</b><button id="planclose">×</button></div><div id="planbody"></div></div>

{''.join(sections)}
<div id="modal"><div class="mbox"><div class="mhead"><div><b id="mt"></b><small id="ms"></small></div><button class="mclose" id="mc">×</button></div>
<div class="mbody"><div class="lbl">場所</div><div id="mp"></div><div class="lbl" style="margin-top:8px">やり方</div><div id="mdsc"></div><div id="mitwrap"><div class="lbl" style="margin-top:8px">必要アイテム(下線=wiki)</div><div id="mit"></div></div></div>
<div class="mfoot"><a id="mwl" href="#" target="_blank" rel="noopener">🖼 wikiで写真を見る</a><a id="mimg" href="#" target="_blank" rel="noopener">📷 画像検索</a></div></div></div>
<script>const __MDPH__=0;</script>
<script>{js.replace("__MD__", md_json).replace("__TD__", md_td)}</script>
</body></html>'''
with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8') as output_file:
    output_file.write(html)
print('built index.html', len(html)//1024, 'KB', BUILD_VER)
