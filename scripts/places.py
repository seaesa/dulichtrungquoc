"""Trang riêng cho từng điểm đến (mục "Bạn muốn đi đâu"): Đà Nẵng, Hội An, Mỹ Sơn, Huế.

Mỗi điểm đến: slug, tiêu đề (vi), ảnh, lead, 3 ô thông tin (icon, nhãn, giá trị), các điểm nổi bật, mẹo.
Mọi chữ là bộ ba (ja, ko, en). `PLACE_PAGES` ghép vào pages.PAGES (cặp ja/ko); bản tiếng Anh nạp vào i18n_en.PAGES_EN.
Thông tin giá vé/giờ mở cửa chỉ mang tính tham khảo, có thể thay đổi.
"""
import i18n_en

HEAD = ('見どころ', '볼거리', 'Highlights')
INFO = ('基本情報', '기본 정보', 'At a glance')
CTA = ('このスポットを含むツアーのご相談・お見積もりはお気軽にどうぞ。', '이 명소가 포함된 투어 상담·견적은 언제든 문의해 주세요.', 'Ask us for a tour or a quote that includes this stop.')

# (slug, vi, ảnh, lead, [(icon, nhãn, giá trị)], [điểm nổi bật], mẹo)
P = [
 ('cau-vang', 'Cầu Vàng', 'danang/cau-vang.jpg',
  ('バーナーヒルズにある、巨大な石の両手に支えられた金色の歩道橋です。', '바나힐에 있는, 거대한 돌손이 받치고 있는 황금빛 보행교입니다.', 'A golden footbridge held up by two giant stone hands, high in the hills at Ba Na.'),
  [('fa-location-dot', ('場所', '위치', 'Location'), ('バーナーヒルズ（ダナン市街から約25km）', '바나힐 (다낭 시내에서 약 25km)', 'Ba Na Hills, about 25 km from central Da Nang')),
   ('fa-clock', ('目安の所要時間', '소요 시간', 'Time needed'), ('橋のみ約1〜2時間、バーナーヒルズ全体で半日〜1日', '다리만 약 1~2시간, 바나힐 전체는 반나절~하루', '1–2 hours for the bridge, half to a full day for all of Ba Na')),
   ('fa-sun', ('おすすめ時間帯', '추천 시간대', 'Best time'), ('混雑を避けるなら開園直後', '혼잡을 피하려면 개장 직후', 'Right after opening, to beat the crowds'))],
  [('全長約150m、標高約1,400mの高さにある金色の橋', '길이 약 150m, 해발 약 1,400m에 있는 황금빛 다리', 'About 150 m long, at roughly 1,400 m above sea level'),
   ('石の巨大な手が橋を支える、フォトジェニックな景観', '돌로 만든 거대한 손이 다리를 받치는 포토제닉한 풍경', 'Huge stone hands hold the bridge, a favourite photo spot'),
   ('ロープウェイで上がり、山々とダナンの眺望を楽しめます', '케이블카로 올라가 산과 다낭 전망을 즐길 수 있습니다', 'Take the cable car up for mountain and Da Nang views')],
  ('山の上は霧が出やすく、朝のほうが景色がよく見えます。上着が1枚あると安心です。', '산 위는 안개가 끼기 쉬워 아침에 경치가 더 잘 보입니다. 가벼운 겉옷을 챙기세요.', 'Mist is common up the mountain and mornings are clearer. Bring a light jacket.')),
 ('ba-na-hills', 'Bà Nà Hills', 'danang/ba-na-hills.jpg',
  ('標高約1,487mのチュア山にある、涼しい山岳リゾートです。', '해발 약 1,487m 쭈아산에 있는 선선한 산악 리조트입니다.', 'A cool mountain resort on Chua Mountain, about 1,487 m above sea level.'),
  [('fa-location-dot', ('場所', '위치', 'Location'), ('ダナン市街から車で約40分', '다낭 시내에서 차로 약 40분', 'About 40 minutes by car from central Da Nang')),
   ('fa-clock', ('目安の所要時間', '소요 시간', 'Time needed'), ('半日〜1日', '반나절~하루', 'Half to a full day')),
   ('fa-ticket', ('入場料の目安', '입장료 (참고)', 'Ticket (guide)'), ('ロープウェイ込みで大人 約1,000,000VND前後（変更の可能性あり）', '케이블카 포함 성인 약 1,000,000동 안팎 (변동 가능)', 'Around 1,000,000 VND for adults incl. cable car (may change)'))],
  [('世界有数の長さのロープウェイで山頂へ', '세계적인 길이의 케이블카로 정상까지', 'One of the world’s longest cable car rides up the mountain'),
   ('フレンチビレッジ、ル・ジャルダン・ダムール庭園、ファンタジーパーク', '프렌치 빌리지, 르 자르댕 다무르 정원, 판타지 파크', 'French Village, Le Jardin d’Amour gardens and Fantasy Park'),
   ('ゴールデンブリッジ（ゴールデンハンド）もここにあります', '골든 브리지(황금 손 다리)도 이곳에 있습니다', 'The Golden Bridge is here too')],
  ('山頂は平地より気温が低めです。歩きやすい靴と薄手の上着がおすすめです。', '정상은 평지보다 기온이 낮습니다. 편한 신발과 얇은 겉옷을 추천합니다.', 'It is cooler at the top. Wear comfortable shoes and bring a thin jacket.')),
 ('cau-rong', 'Cầu Rồng', 'danang/cau-rong.jpg',
  ('ハン川に架かる、龍をかたどった橋です。週末の夜には火と水のショーが行われます。', '한강에 놓인 용 모양의 다리로, 주말 밤에는 불과 물 쇼가 열립니다.', 'A dragon-shaped bridge over the Han River, with a fire-and-water show on weekend nights.'),
  [('fa-location-dot', ('場所', '위치', 'Location'), ('ダナン市内、ハン川沿い', '다낭 시내, 한강변', 'Central Da Nang, on the Han River')),
   ('fa-clock', ('目安の所要時間', '소요 시간', 'Time needed'), ('約1時間（ショー観賞を含む）', '약 1시간 (쇼 관람 포함)', 'About 1 hour including the show')),
   ('fa-moon', ('おすすめ時間帯', '추천 시간대', 'Best time'), ('夜。ショーは主に土・日曜の夜（変更の可能性あり）', '밤. 쇼는 주로 토·일요일 밤 (변동 가능)', 'Evenings. The show is mainly on Saturday and Sunday nights (may change)'))],
  [('全長約666mの龍の橋、夜はライトアップされます', '길이 약 666m의 용 다리, 밤에는 조명이 켜집니다', 'A dragon bridge about 666 m long, lit up at night'),
   ('龍の頭から火や水が噴き出すショー', '용의 머리에서 불과 물이 뿜어져 나오는 쇼', 'The dragon’s head breathes fire and water'),
   ('周辺にはカフェやナイトクルーズの乗り場があります', '주변에 카페와 나이트 크루즈 승선장이 있습니다', 'Coffee shops and night-cruise piers are close by')],
  ('ショーは混雑します。橋の近くの川沿いで、早めに場所を取ると見やすくなります。', '쇼는 붐비니 다리 근처 강변에서 일찍 자리를 잡으세요.', 'It gets crowded. Claim a spot along the riverbank early.')),
 ('ngu-hanh-son', 'Ngũ Hành Sơn', 'danang/ngu-hanh-son.jpg',
  ('五行（金・木・水・火・土）の名を持つ5つの石灰岩の山で、洞窟や寺院があります。', '오행(금·목·수·화·토)의 이름을 가진 5개의 석회암 산으로, 동굴과 사원이 있습니다.', 'Five limestone hills named after the five elements, with caves and pagodas.'),
  [('fa-location-dot', ('場所', '위치', 'Location'), ('ダナン市街から約8km', '다낭 시내에서 약 8km', 'About 8 km from central Da Nang')),
   ('fa-clock', ('目安の所要時間', '소요 시간', 'Time needed'), ('約1.5〜2時間', '약 1.5~2시간', '1.5–2 hours')),
   ('fa-ticket', ('入場料の目安', '입장료 (참고)', 'Ticket (guide)'), ('入場 約40,000VND、エレベーターは別料金（変更の可能性あり）', '입장 약 40,000동, 엘리베이터는 별도 (변동 가능)', 'About 40,000 VND entry, lift extra (may change)'))],
  [('最も大きいトゥイーソン山に洞窟と仏像が点在', '가장 큰 투이선 산에 동굴과 불상이 곳곳에 있습니다', 'Thuy Son, the largest hill, has caves and Buddha statues'),
   ('山頂付近からの海と街の眺め', '정상 부근에서 보는 바다와 도시 전망', 'Sea and city views from near the top'),
   ('麓には石の彫刻の工房が並びます', '산 아래에는 석조 공방이 늘어서 있습니다', 'Stone-carving workshops line the foot of the hills')],
  ('階段が多いので歩きやすい靴で。暑い時間帯を避け、朝か夕方がおすすめです。', '계단이 많으니 편한 신발로. 더운 시간대를 피해 아침이나 저녁이 좋습니다.', 'Many steps, so wear good shoes. Go in the morning or late afternoon to avoid the heat.')),
 ('my-khe', 'Biển Mỹ Khê', 'danang/my-khe.jpg',
  ('ダナンを代表する、白い砂浜が続く美しいビーチです。', '다낭을 대표하는 흰 모래사장이 이어지는 아름다운 해변입니다.', 'Da Nang’s signature beach, a long stretch of white sand.'),
  [('fa-location-dot', ('場所', '위치', 'Location'), ('ダナン市街から約3km', '다낭 시내에서 약 3km', 'About 3 km from central Da Nang')),
   ('fa-clock', ('目安の所要時間', '소요 시간', 'Time needed'), ('1〜3時間（のんびり過ごす場合）', '1~3시간 (여유롭게 보낼 경우)', '1–3 hours, longer if you relax')),
   ('fa-sun', ('おすすめ時間帯', '추천 시간대', 'Best time'), ('朝の散歩か夕暮れ時。海水浴は4〜9月が目安', '아침 산책이나 해질녘. 해수욕은 4~9월이 적기', 'Morning walks or sunset; swimming season is roughly April–September'))],
  [('穏やかな波と広い砂浜', '잔잔한 파도와 넓은 모래사장', 'Gentle waves and a wide beach'),
   ('周辺にシーフードレストランやホテルが多数', '주변에 해산물 식당과 호텔이 많습니다', 'Plenty of seafood restaurants and hotels nearby'),
   ('早朝は地元の人の海水浴や運動で賑わいます', '이른 아침에는 현지인들의 해수욕과 운동으로 활기찹니다', 'Early mornings are lively with locals swimming and exercising')],
  ('日差しが強いので日焼け止めを。波が高い日は遊泳禁止の旗に従ってください。', '햇볕이 강하니 선크림을 챙기세요. 파도가 높은 날은 수영 금지 깃발을 따르세요.', 'Bring sunscreen. On rough days follow the no-swimming flags.')),
 ('son-tra', 'Bán đảo Sơn Trà', 'danang/son-tra.jpg',
  ('原生林と海に囲まれた半島で、リンウン寺の巨大な観音像で知られます。', '원시림과 바다로 둘러싸인 반도로, 린응사의 거대한 해수관음상으로 유명합니다.', 'A forested peninsula by the sea, known for the giant Lady Buddha at Linh Ung Pagoda.'),
  [('fa-location-dot', ('場所', '위치', 'Location'), ('ダナン市街から約10km', '다낭 시내에서 약 10km', 'About 10 km from central Da Nang')),
   ('fa-clock', ('目安の所要時間', '소요 시간', 'Time needed'), ('約2〜3時間', '약 2~3시간', '2–3 hours')),
   ('fa-sun', ('おすすめ時間帯', '추천 시간대', 'Best time'), ('朝または夕方', '아침 또는 저녁', 'Morning or late afternoon'))],
  [('高さ約67mのリンウン寺の観音像が海を見守ります', '높이 약 67m의 린응사 해수관음상이 바다를 바라봅니다', 'The roughly 67 m Lady Buddha at Linh Ung Pagoda looks out to sea'),
   ('「ダナンの緑の肺」と呼ばれる豊かな自然', '‘다낭의 녹색 허파’라 불리는 풍부한 자연', 'Known as the “green lung” of Da Nang'),
   ('貴重なドゥクラングール（サル）が生息します', '귀중한 붉은 정강이 랑구르 원숭이가 서식합니다', 'Home to the rare red-shanked douc langur')],
  ('寺院を訪れるときは、肩と膝が隠れる服装でお越しください。', '사원을 방문할 때는 어깨와 무릎을 가리는 복장으로 오세요.', 'Cover your shoulders and knees when visiting the pagoda.')),
 ('hoi-an', 'Phố cổ Hội An', 'danang/hoi-an.jpg',
  ('ランタンが灯る、ユネスコ世界遺産の古い港町です。', '등불이 켜지는 유네스코 세계유산의 옛 항구 도시입니다.', 'A UNESCO-listed old trading port, glowing with lanterns at night.'),
  [('fa-location-dot', ('場所', '위치', 'Location'), ('ダナン市街から車で約40分', '다낭 시내에서 차로 약 40분', 'About 40 minutes by car from central Da Nang')),
   ('fa-clock', ('目安の所要時間', '소요 시간', 'Time needed'), ('半日〜1日（夜まで滞在がおすすめ）', '반나절~하루 (밤까지 머무는 것을 추천)', 'Half to a full day, ideally until evening')),
   ('fa-ticket', ('旧市街の入場券', '구시가 입장권', 'Old Town ticket'), ('観光用チケットが必要（変更の可能性あり）', '관광용 티켓 필요 (변동 가능)', 'A sightseeing ticket is required (may change)'))],
  [('日本橋（来遠橋）や古い商家、会館の街並み', '일본교(내원교)와 옛 상가, 회관이 늘어선 거리', 'The Japanese Covered Bridge, old merchant houses and assembly halls'),
   ('夜はホアイ川でランタン流しと小舟の遊覧', '밤에는 호아이강에서 등불 띄우기와 보트 유람', 'Lantern releases and boat rides on the Hoai River at night'),
   ('カオラウやバインミーなどの名物グルメ', '까오러우, 반미 등 명물 음식', 'Local dishes such as cao lau and banh mi')],
  ('夕方から夜が一番雰囲気があります。日中は暑いので帽子と水を忘れずに。', '저녁부터 밤이 가장 분위기가 좋습니다. 낮에는 더우니 모자와 물을 챙기세요.', 'Evening is the most atmospheric. It is hot by day, so bring a hat and water.')),
 ('my-son', 'Thánh địa Mỹ Sơn', 'danang/my-son.jpg',
  ('4〜13世紀頃のチャンパ王国のヒンドゥー教遺跡群で、世界遺産です。', '4~13세기경 참파 왕국의 힌두교 유적군으로 세계유산입니다.', 'A UNESCO World Heritage group of Hindu temple ruins from the Champa kingdom.'),
  [('fa-location-dot', ('場所', '위치', 'Location'), ('ホイアンから約40km、ダナンから約70km', '호이안에서 약 40km, 다낭에서 약 70km', 'About 40 km from Hoi An, 70 km from Da Nang')),
   ('fa-clock', ('目安の所要時間', '소요 시간', 'Time needed'), ('見学1.5〜2時間（往復含め半日）', '관람 1.5~2시간 (왕복 포함 반나절)', '1.5–2 hours on site, half a day with transport')),
   ('fa-sun', ('おすすめ時間帯', '추천 시간대', 'Best time'), ('涼しく空いている午前中', '시원하고 한적한 오전', 'Morning, when it is cooler and quieter'))],
  [('ジャングルの谷に残る、レンガ造りの塔の遺跡', '정글 계곡에 남아 있는 벽돌 탑 유적', 'Brick towers standing in a jungle valley'),
   ('チャンパ文化の彫刻や石像', '참파 문화의 조각과 석상', 'Carvings and statues of Cham culture'),
   ('ホイアンとのセットツアーが人気', '호이안과 함께하는 투어가 인기입니다', 'Often combined with Hoi An in one tour')],
  ('日陰が少ないので、帽子・日焼け止め・飲み物を必ず持参してください。', '그늘이 적으니 모자·선크림·음료를 꼭 챙기세요.', 'There is little shade, so bring a hat, sunscreen and drinks.')),
 ('dai-noi', 'Đại Nội Huế', 'hue/dai-noi.jpg',
  ('阮朝の王宮だった、フエの王城（フエ皇城）です。世界遺産のフエの建造物群の中心です。', '응우옌 왕조의 궁궐이었던 후에 황성입니다. 세계유산 후에 유적군의 중심입니다.', 'The Nguyen dynasty’s imperial citadel in Hue, the heart of the UNESCO-listed monuments.'),
  [('fa-location-dot', ('場所', '위치', 'Location'), ('フエ市内（ダナンから車で約2時間〜）', '후에 시내 (다낭에서 차로 약 2시간~)', 'Central Hue, about 2 hours from Da Nang by car')),
   ('fa-clock', ('目安の所要時間', '소요 시간', 'Time needed'), ('約2〜3時間', '약 2~3시간', '2–3 hours')),
   ('fa-ticket', ('入場料の目安', '입장료 (참고)', 'Ticket (guide)'), ('大人 約200,000VND（変更の可能性あり）', '성인 약 200,000동 (변동 가능)', 'About 200,000 VND for adults (may change)'))],
  [('正門の午門（ゴモン）と、皇帝の即位式が行われた太和殿', '정문인 오문(응오몬)과 황제의 즉위식이 열린 태화전', 'The Meridian Gate and the Thai Hoa Palace for imperial ceremonies'),
   ('紫禁城跡や歴代皇帝を祀る廟など、広い敷地', '자금성 터와 역대 황제를 모신 사당 등 넓은 부지', 'A large site with the Forbidden City remains and ancestral temples'),
   ('王宮の衣装での記念撮影も人気です', '궁중 의상을 입고 찍는 기념 촬영도 인기입니다', 'Photos in royal costumes are popular')],
  ('敷地が広く日陰が少ないので、歩きやすい靴と日除けを。ガイドと回ると歴史がよくわかります。', '부지가 넓고 그늘이 적으니 편한 신발과 햇볕 차단 용품을 챙기세요. 가이드와 함께하면 역사를 잘 알 수 있습니다.', 'The site is large with little shade. Wear good shoes, and a guide helps bring the history to life.')),
 ('lang-khai-dinh', 'Lăng Khải Định', 'hue/lang-khai-dinh.jpg',
  ('第12代皇帝カイディンの廟で、西洋と東洋の様式が混ざった装飾が特徴です。', '제12대 황제 카이딘의 능으로, 동서양 양식이 섞인 장식이 특징입니다.', 'The tomb of the 12th emperor, known for its blend of Eastern and Western decoration.'),
  [('fa-location-dot', ('場所', '위치', 'Location'), ('フエ市街から約10km', '후에 시내에서 약 10km', 'About 10 km from Hue city')),
   ('fa-clock', ('目安の所要時間', '소요 시간', 'Time needed'), ('約1時間', '약 1시간', 'About 1 hour')),
   ('fa-ticket', ('入場料の目安', '입장료 (참고)', 'Ticket (guide)'), ('大人 約150,000VND（変更の可能性あり）', '성인 약 150,000동 (변동 가능)', 'About 150,000 VND for adults (may change)'))],
  [('陶器やガラスの破片で飾られた、きらびやかな内部', '도자기와 유리 조각으로 장식한 화려한 내부', 'An ornate interior decorated with ceramic and glass pieces'),
   ('丘の斜面に築かれた、コンパクトで急な階段の廟', '언덕 경사면에 지어진 아담하고 계단이 가파른 능', 'A compact tomb built up a hillside with steep steps'),
   ('フエの廟の中でも特に個性的な建築', '후에의 능 중에서도 특히 개성적인 건축', 'One of the most distinctive tombs in Hue')],
  ('階段が多く、足元が滑りやすいことがあります。雨の日は特にご注意ください。', '계단이 많고 미끄러울 수 있으니 비 오는 날은 특히 주의하세요.', 'Many steps that can be slippery, especially in the rain.')),
 ('lang-tu-duc', 'Lăng Tự Đức', 'hue/lang-tu-duc.jpg',
  ('第4代皇帝トゥドゥックの廟で、湖や松林に囲まれた、庭園のように美しい廟です。', '제4대 황제 뜨득의 능으로, 호수와 소나무 숲에 둘러싸인 정원 같은 능입니다.', 'The tomb of the 4th emperor, set among lakes and pine groves like a garden.'),
  [('fa-location-dot', ('場所', '위치', 'Location'), ('フエ市街から約6km', '후에 시내에서 약 6km', 'About 6 km from Hue city')),
   ('fa-clock', ('目安の所要時間', '소요 시간', 'Time needed'), ('約1〜1.5時間', '약 1~1.5시간', '1–1.5 hours')),
   ('fa-ticket', ('入場料の目安', '입장료 (참고)', 'Ticket (guide)'), ('大人 約150,000VND（変更の可能性あり）', '성인 약 150,000동 (변동 가능)', 'About 150,000 VND for adults (may change)'))],
  [('蓮の池や東屋のある、のんびりとした庭園の景観', '연못과 정자가 있는 한가로운 정원 풍경', 'Peaceful grounds with a lotus lake and pavilions'),
   ('皇帝が生前に過ごした宮殿的な建物群', '황제가 생전에 지내던 궁전 같은 건물군', 'Palace-like buildings where the emperor spent his later years'),
   ('フエの廟の中でも落ち着いた雰囲気で人気', '후에의 능 중에서도 차분한 분위기로 인기', 'A calm atmosphere that makes it a visitor favourite')],
  ('敷地は広く、ゆっくり歩いて回るのがおすすめです。写真は午前中が撮りやすいです。', '부지가 넓어 천천히 걸으며 둘러보기를 추천합니다. 사진은 오전이 찍기 좋습니다.', 'The grounds are large, so take your time. Mornings are good for photos.')),
 ('lang-minh-mang', 'Lăng Minh Mạng', 'hue/lang-minh-mang.jpg',
  ('第2代皇帝ミンマンの廟で、左右対称の整った配置と、湖と森の景観が見どころです。', '제2대 황제 민망의 능으로, 좌우 대칭의 정돈된 배치와 호수·숲 경관이 볼거리입니다.', 'The tomb of the 2nd emperor, admired for its symmetrical layout and its lake and forest setting.'),
  [('fa-location-dot', ('場所', '위치', 'Location'), ('フエ市街から約12km、香江沿い', '후에 시내에서 약 12km, 향강변', 'About 12 km from Hue city, by the Perfume River')),
   ('fa-clock', ('目安の所要時間', '소요 시간', 'Time needed'), ('約1〜1.5時間', '약 1~1.5시간', '1–1.5 hours')),
   ('fa-ticket', ('入場料の目安', '입장료 (참고)', 'Ticket (guide)'), ('大人 約150,000VND（変更の可能性あり）', '성인 약 150,000동 (변동 가능)', 'About 150,000 VND for adults (may change)'))],
  [('一直線に並ぶ門・中庭・楼閣・橋の美しい構成', '일직선으로 늘어선 문·정원·누각·다리의 아름다운 구성', 'Gates, courtyards, pavilions and bridges lined up along one axis'),
   ('湖に映る建物と、緑豊かな松林', '호수에 비치는 건물과 푸른 소나무 숲', 'Buildings reflected in the lake among green pines'),
   ('香江のクルーズと組み合わせても人気', '향강 크루즈와 함께하는 코스도 인기', 'Often paired with a Perfume River cruise')],
  ('敷地が広く、奥まで歩くと距離があります。歩きやすい靴でどうぞ。', '부지가 넓어 안쪽까지 걷는 거리가 있습니다. 편한 신발을 신으세요.', 'It is a long walk to the far end, so wear comfortable shoes.')),
 ('lang-dong-khanh', 'Lăng Đồng Khánh', 'hue/lang-dong-khanh.jpg',
  ('第9代皇帝ドンカインの廟で、規模は小さめですが、フエの廟の中でも装飾が細やかです。', '제9대 황제 동카인의 능으로, 규모는 작지만 후에의 능 중에서도 장식이 정교합니다.', 'The tomb of the 9th emperor: smaller in scale, but finely decorated.'),
  [('fa-location-dot', ('場所', '위치', 'Location'), ('フエ市街から約8km', '후에 시내에서 약 8km', 'About 8 km from Hue city')),
   ('fa-clock', ('目安の所要時間', '소요 시간', 'Time needed'), ('約45分〜1時間', '약 45분~1시간', '45 minutes to 1 hour')),
   ('fa-ticket', ('入場料の目安', '입장료 (참고)', 'Ticket (guide)'), ('大人 約150,000VND（変更の可能性あり）', '성인 약 150,000동 (변동 가능)', 'About 150,000 VND for adults (may change)'))],
  [('コンパクトで、短時間で見学できる廟', '아담해서 짧은 시간에 둘러볼 수 있는 능', 'Compact and easy to see in a short visit'),
   ('内部の壁や天井の細かな装飾', '내부 벽과 천장의 섬세한 장식', 'Intricate decoration on interior walls and ceilings'),
   ('他の廟と合わせて回る行程に入れやすい', '다른 능과 함께 도는 일정에 넣기 좋습니다', 'Easy to add to a tomb-hopping itinerary')],
  ('他の廟とセットで巡ると、それぞれの違いが分かって楽しめます。', '다른 능과 함께 돌면 각각의 차이를 알 수 있어 즐겁습니다.', 'Visiting several tombs together makes the differences easy to see.')),
]

import importlib
EXTRA = {}
for _m in ('places_x1', 'places_x2', 'places_x3', 'places_x4', 'places_x5'):
    try:
        EXTRA.update(importlib.import_module(_m).X)
    except ModuleNotFoundError:
        pass
try:  # phần bổ sung: chèn trước mục cuối (mẹo)
    for _k, _secs in importlib.import_module('places_x1b').ADD.items():
        EXTRA[_k][-1:-1] = _secs
except ModuleNotFoundError:
    pass

PLACE_PAGES = {}
for slug, vi, img, lead, info, hl, tip in P:
    PLACE_PAGES[slug] = dict(
        title=vi, img=img, lead=lead[:2],
        blocks=[('place_img', img), ('h', INFO[:2]), ('cards', [(ic, lb[:2], v[:2]) for ic, lb, v in info]),
                ('h', HEAD[:2]), ('ul', [x[:2] for x in hl])]
               + [b for h, ps in EXTRA.get(slug, []) for b in [('h', h[:2])] + [('p', q[:2]) for q in ps]]
               + [('note', tip[:2]), ('contact_cta',)])
    # tiếng Anh tra theo chữ tiếng Nhật
    en = {lead[0]: lead[2], INFO[0]: INFO[2], HEAD[0]: HEAD[2], tip[0]: tip[2]}
    for ic, lb, v in info:
        en[lb[0]] = lb[2]; en[v[0]] = v[2]
    for x in hl:
        en[x[0]] = x[2]
    for h, ps in EXTRA.get(slug, []):
        en[h[0]] = h[2]
        for q in ps:
            en[q[0]] = q[2]
    for ja, e_ in en.items():
        if i18n_en.PAGES_EN.get(ja, e_) != e_:
            raise ValueError(f'Trùng khoá tiếng Nhật, khác bản tiếng Anh: {ja[:30]}')
        i18n_en.PAGES_EN[ja] = e_
