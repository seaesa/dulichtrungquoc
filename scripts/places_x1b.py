"""Mục bổ sung (lịch trình gợi ý) cho các trang đợt 1. Chèn trước mục 'mẹo'."""
ITIN = ('おすすめのモデルコース', '추천 모델 코스', 'A suggested itinerary')
ADD = {
 'ba-na-hills': [(ITIN, [
   ('午前8時ごろにダナンを出発し、9時前後に到着してロープウェイで山頂へ向かうのが定番です。まずゴールデンブリッジで写真を撮り、そのままフレンチビレッジへ。昼食は園内で取り、午後は庭園の散策やファンタジーパークでゆっくり過ごします。夕方前に下山を始めれば、ダナン市内に戻って夕食を楽しめます。',
    '오전 8시쯤 다낭을 출발해 9시 전후에 도착, 케이블카로 정상에 오르는 것이 정석입니다. 먼저 골든 브리지에서 사진을 찍고 프렌치 빌리지로 이동합니다. 점심은 공원 안에서 먹고 오후에는 정원 산책이나 판타지 파크에서 여유롭게 보냅니다. 저녁 전에 하산을 시작하면 다낭 시내로 돌아와 저녁을 즐길 수 있습니다.',
    'A classic plan is to leave Da Nang around 8 am, arrive about 9 and ride the cable car to the top. Start with photos on the Golden Bridge, then move on to the French Village. Have lunch in the park and spend the afternoon in the gardens or Fantasy Park. If you start down before evening you can be back in Da Nang for dinner.')])],
 'cau-rong': [(ITIN, [
   ('夕方5〜6時ごろにハン川沿いを散歩し、日没後のライトアップを眺めます。その後、川沿いのレストランで夕食を取り、ショーの時間に合わせて橋のたもとへ。ショー終了後は、ナイトクルーズやカフェで余韻に浸るのがおすすめです。週末以外は火のショーはありませんが、ライトアップだけでも十分に楽しめます。',
    '저녁 5~6시쯤 한강변을 산책하며 해 질 무렵 조명이 켜지는 모습을 봅니다. 이후 강변 레스토랑에서 저녁을 먹고 쇼 시간에 맞춰 다리 근처로 이동합니다. 쇼가 끝난 뒤에는 야간 크루즈나 카페에서 여운을 즐기는 것을 추천합니다. 주말이 아니면 불 쇼는 없지만 조명만으로도 충분히 즐길 수 있습니다.',
    'Stroll along the Han River around 5 to 6 pm and watch the lights come on after sunset. Then have dinner at a riverside restaurant and head to the bridge in time for the show. Afterwards, a night cruise or a coffee shop is a nice way to wind down. There is no fire show on weekdays, but the lighting alone is well worth seeing.')])],
 'ngu-hanh-son': [(ITIN, [
   ('朝の涼しい時間に到着し、まずトゥイーソンの洞窟と展望台を回ります。所要時間は約1時間半から2時間が目安です。その後、麓の石彫りの工房を見学し、近くのミーケービーチで海を眺めながら昼食を取ると、無理のない半日コースになります。時間に余裕があれば、リンウン寺まで足を延ばしても良いでしょう。見学の合間には、麓の売店で冷たい飲み物を買い、日陰で休憩を取ると快適です。',
    '아침 선선한 시간에 도착해 먼저 투이선의 동굴과 전망대를 돕니다. 소요 시간은 약 1시간 반에서 2시간이 기준입니다. 이후 산기슭의 석조 공방을 구경하고 근처 미케 해변에서 바다를 보며 점심을 먹으면 무리 없는 반나절 코스가 됩니다. 시간이 있으면 린응사까지 가 봐도 좋습니다. 관람 중간에는 산기슭 가게에서 시원한 음료를 사 그늘에서 쉬면 쾌적합니다.',
    'Arrive in the cool of the morning and start with the caves and viewpoints of Thuy Son, which take about 1.5 to 2 hours. Then visit the stone-carving workshops at the foot of the hills and have lunch by the sea at nearby My Khe Beach for an easy half-day. If you have time, extend the trip to Linh Ung Pagoda. Between visits, buy a cold drink from a stall at the foot of the hills and rest in the shade.')])],
 'my-khe': [(('知っておくと便利なこと', '알아두면 좋은 점', 'Good to know'), [
   ('ミーケービーチはホテルから徒歩圏内のことも多く、タクシーやGrabで気軽に行けます。ビーチ沿いにはシャワーやトイレ、更衣室を備えた施設もあり、着替えや砂を洗い流すのに便利です。日中は強い日差しを避けるため、午前10時から午後3時ごろは木陰や屋内で休むのがおすすめです。',
    '미케 해변은 호텔에서 도보 거리인 경우가 많고 택시나 Grab으로 부담 없이 갈 수 있습니다. 해변 주변에는 샤워실, 화장실, 탈의실을 갖춘 시설도 있어 옷을 갈아입거나 모래를 씻어 내기에 편리합니다. 낮에는 강한 햇볕을 피하기 위해 오전 10시부터 오후 3시경에는 나무 그늘이나 실내에서 쉬는 것을 추천합니다.',
    'My Khe is often within walking distance of hotels and easy to reach by taxi or Grab. Some places along the beach offer showers, toilets and changing rooms, handy for changing and rinsing off the sand. To avoid the strongest sun, rest in the shade or indoors between about 10 am and 3 pm.')])],
 'son-tra': [(('知っておくと便利なこと', '알아두면 좋은 점', 'Good to know'), [
   ('ソンチャー半島は、ダナン市街から車で約20分から30分と、思いのほか近い場所にあります。ダナンの空港や市街のホテルからも行きやすく、短い滞在でも立ち寄りやすいのが魅力です。天気のよい日は、頂上付近から海と街が見え、旅の思い出になる景色に出会えます。',
    '선짜 반도는 다낭 시내에서 차로 약 20분에서 30분으로 생각보다 가까운 곳에 있습니다. 다낭 공항이나 시내 호텔에서도 가기 쉬워 짧은 체류에도 들르기 좋은 점이 매력입니다. 날씨가 좋은 날에는 정상 부근에서 바다와 도시가 보여 여행의 추억이 될 경치를 만날 수 있습니다.',
    'Son Tra is closer than you might expect, about 20 to 30 minutes by car from central Da Nang. It is easy to reach from the airport and city hotels, which makes it a good stop even on a short stay. On a clear day the sea and city are visible from near the top, a view that makes a lasting memory.')])],
 'my-son': [(('知っておくと便利なこと', '알아두면 좋은 점', 'Good to know'), [
   ('ミーソン聖地は、写真を撮るのにも最適な場所です。朝の柔らかな光に照らされた赤いレンガの塔は、特に美しく写ります。遺跡の保護のため、塔の上に登ったり、壁に落書きをしたりすることは厳しく禁止されています。マナーを守って、静かに見学しましょう。',
    '미선 성지는 사진 찍기에도 최적의 장소입니다. 아침의 부드러운 빛을 받은 붉은 벽돌 탑이 특히 아름답게 찍힙니다. 유적 보호를 위해 탑 위에 오르거나 벽에 낙서하는 행위는 엄격히 금지되어 있습니다. 매너를 지키며 조용히 관람하세요.',
    'My Son is a great place for photos, and the red-brick towers look especially beautiful in the soft morning light. To protect the ruins, climbing the towers or writing on the walls is strictly forbidden. Please be respectful and visit quietly.')])],

 'lang-khai-dinh': [
 (('撮影のコツと周辺の楽しみ方', '촬영 팁과 주변 즐기기', 'Photo tips and nearby stops'), [
   ('カイディン帝廟では、階段の途中から振り返って谷を入れた構図や、内部のモザイクの細部を狙った写真が人気です。人が少ない朝の時間帯なら、階段全体をすっきり撮影できます。見学のあとは、近くの村で素朴なフエの食堂に立ち寄り、地元の味を楽しむのもおすすめです。', '카이딘 황릉에서는 계단 중간에서 뒤돌아 골짜기를 담은 구도나 내부 모자이크의 디테일을 노린 사진이 인기입니다. 사람이 적은 아침 시간대라면 계단 전체를 깔끔하게 촬영할 수 있습니다. 관람 후에는 근처 마을의 소박한 후에 식당에 들러 현지 맛을 즐기는 것도 추천합니다.', 'At Khai Dinh’s Tomb, popular shots include looking back from partway up the steps with the valley in frame, and close-ups of the interior mosaics. In the quiet morning you can photograph the whole staircase cleanly. Afterwards, stop at a simple local Hue eatery in a nearby village to enjoy the regional flavours.'),
   ('また、この廟は規模がコンパクトなため、小さなお子様連れやご年配の方にも比較的見学しやすい場所です。ただし階段は急なので、手すりを使い、ゆっくり進んでください。', '또한 이 능은 규모가 아담해 어린이 동반이나 연세 드신 분께도 비교적 관람하기 쉬운 곳입니다. 다만 계단이 가파르니 난간을 이용해 천천히 오르세요.', 'Because the tomb is compact, it is also relatively manageable for families with children and older travellers. The steps are steep, however, so use the handrails and take your time.'),
  ]),
 ],
 'lang-tu-duc': [
 (('散策と季節の楽しみ方', '산책과 계절 즐기기', 'Strolling and the seasons'), [
   ('トゥドゥック帝廟は、急いで回るよりも、湖畔のベンチや東屋で腰を下ろし、静かな景色を味わうのに向いています。早朝は霧がかかることもあり、幻想的な雰囲気の写真が撮れる場合があります。', '뜨득 황릉은 서둘러 도는 것보다 호숫가 벤치나 정자에 앉아 고요한 경치를 음미하기에 알맞습니다. 이른 아침에는 안개가 끼기도 해 환상적인 분위기의 사진을 찍을 수 있습니다.', 'Tu Duc’s Tomb suits sitting on a bench or in a pavilion by the lake and savouring the calm view rather than rushing. Early mornings can bring mist, which sometimes makes for dreamy photographs.'),
   ('雨の季節には緑がいっそう濃くなり、湖面を雨粒が揺らす様子も風情があります。ただし足元がぬかるむことがあるため、滑りにくい靴がおすすめです。', '우기에는 초록이 한층 짙어지고 호수 위로 빗방울이 번지는 모습도 운치가 있습니다. 다만 땅이 질척해질 수 있으니 미끄럽지 않은 신발을 추천합니다.', 'In the rainy season the greenery deepens and raindrops rippling the lake have their own charm. The ground can get muddy, so non-slip shoes are recommended.'),
  ]),
 ],
 'lang-minh-mang': [
 (('ミンマン帝廟の歩き方', '민망 황릉 걷는 법', 'Walking Minh Mang’s Tomb'), [
   ('ミンマン帝廟では、入口の大紅門から最奥の墓所まで、一直線に歩きながら建物の配置を意識すると、設計の意図がよくわかります。途中の橋や池で足を止め、左右対称の景色を見比べるのも面白い楽しみ方です。', '민망 황릉에서는 입구의 대홍문에서 가장 안쪽 묘소까지 일직선으로 걸으며 건물 배치를 의식하면 설계 의도를 잘 이해할 수 있습니다. 중간의 다리와 연못에서 걸음을 멈추고 좌우 대칭 풍경을 비교해 보는 것도 재미있습니다.', 'At Minh Mang’s Tomb, walking the straight line from the main gate to the burial mound while noticing the layout helps you understand the design. Pausing at the bridges and ponds to compare the symmetrical views is a fun way to look.'),
   ('敷地が広いため、体力に自信がない方は、車で近くまで送迎してもらえるプランを選ぶと楽です。また、日中は暑くなるため、涼しい時間に奥まで歩くのがおすすめです。', '부지가 넓어 체력에 자신이 없는 분은 차로 가까운 곳까지 송영해 주는 플랜을 고르면 편합니다. 또한 낮에는 더우니 선선한 시간에 안쪽까지 걷는 것을 추천합니다.', 'The grounds are large, so if stamina is a concern, choose a plan with a car transfer close to the entrance. It also gets hot by day, so walk to the far end during the cooler hours.'),
  ]),
 ],
 'lang-dong-khanh': [
 (('小さな廟だからこその魅力', '작은 능이라서 더 매력적인 이유', 'The charm of a small tomb'), [
   ('ドンカイン帝廟は、小さな廟だからこそ、建物の細部をじっくり眺められるのが魅力です。柱や壁の模様、屋根の飾りなど、見るたびに新しい発見があります。大きな帝廟で人混みに疲れた方にも、静かに過ごせる場所としておすすめです。工芸がお好きな方や、慌ただしい観光の合間に30分ほどのんびりしたい方が、フエ旅行で思いがけないお気に入りに挙げることも多い場所です。', '동카인 황릉은 작은 능이라서 건물의 디테일을 차분히 볼 수 있는 점이 매력입니다. 기둥과 벽의 문양, 지붕 장식 등 볼 때마다 새로운 발견이 있습니다. 큰 황릉에서 인파에 지친 분께도 조용히 지낼 수 있는 곳으로 추천합니다. 공예를 좋아하는 분이나 바쁜 관광 사이에 30분 정도 여유를 원하는 분이 후에 여행에서 뜻밖의 즐겨찾는 곳로 꼽는 경우가 많습니다.', 'Precisely because it is small, Dong Khanh’s Tomb lets you study the details at leisure. Patterns on columns and walls and the roof ornaments reveal something new each time. It is also a quiet place for those tired of the crowds at the larger tombs. Visitors who enjoy craftsmanship, or who simply want an unhurried half hour away from busy sightseeing, often name this tomb as an unexpected favourite of their Hue trip.'),
   ('廟の周りには素朴な田舎の風景が広がり、自転車や車でゆっくり巡る楽しみもあります。フエの暮らしの一端に触れながら、帝廟めぐりを締めくくる場所として最適です。', '능 주변에는 소박한 시골 풍경이 펼쳐져 자전거나 차로 천천히 둘러보는 즐거움도 있습니다. 후에 생활의 한 자락을 접하며 황릉 투어를 마무리하는 장소로 알맞습니다.', 'Around the tomb lies simple countryside that is pleasant to explore slowly by bicycle or car. It is a fine place to end a royal-tomb tour while glimpsing everyday life in Hue.'),
  ]),
 ],
}
