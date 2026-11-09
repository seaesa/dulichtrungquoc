"""Tour tuỳ chọn tại Đà Nẵng – Hội An – Huế (mục "おすすめツアー").

Theo bảng "Tour OP (bản mới update 10.2026)". Mỗi tour có tên/lịch trình bằng tiếng Việt (gốc),
tiếng Nhật và tiếng Hàn; i18n.py lấy bản dịch từ ROWS bên dưới.
price: giá thấp nhất (USD); from_=True khi có nhiều phương án giá (hiện "〜").
"""

# (vi, ja, ko) cho nhãn chung
LABELS = [
    ('TOUR GỢI Ý', 'おすすめツアー', '추천 투어'),
    ('GỢI Ý', 'おすすめ', '추천'),
    ('Tour gợi ý', 'おすすめツアー', '추천 투어'),
    ('Thời gian:', '所要時間:', '소요 시간:'),
    ('Bữa ăn:', '食事:', '식사:'),
    ('Bữa tối', '夕食', '저녁 식사'),
    ('Bữa trưa', '昼食', '점심 식사'),
    ('Bữa trưa hoặc bữa tối', '昼食または夕食', '점심 또는 저녁'),
    ('Bữa trưa & bữa tối', '昼食＆夕食', '점심 & 저녁'),
    ('Không bao gồm', 'なし', '불포함'),
    ('Khoảng 4,5 giờ', '約4.5時間', '약 4.5시간'),
    ('Trước giờ bay', 'フライト前', '출국 전'),
    ('/2 khách', '/2名', '/2인'),
    ('Giá tham khảo tính theo USD/khách · Thanh toán bằng VND',
     '料金は1名あたりの米ドル表示（目安）・お支払いはベトナムドン（VND）のみ',
     '요금은 1인 기준 미화 표시(참고) · 결제는 베트남 동(VND)만 가능'),
    ('Thánh địa Mỹ Sơn', 'ミーソン遺跡', '미선 유적'),
]

LABELS += [
    ('RIÊNG', 'プライベート', '프라이빗'),
    ('GIA ĐÌNH', 'ファミリー', '패밀리'),
    ('ĐẶC BIỆT', '特別', '스페셜'),
    ('1 ngày', '1日', '1일'),
    ('2 ngày 1 đêm', '1泊2日', '1박 2일'),
    ('3 ngày 2 đêm', '2泊3日', '2박 3일'),
    ('4 ngày 3 đêm', '3泊4日', '3박 4일'),
    ('Theo yêu cầu', 'ご希望に応じて', '요청 시 제공'),
]

LABELS += [
    ('TOUR RIÊNG', 'オーダーメイドの専用ツアー', '맞춤형 프라이빗 투어'),
    ('Thiết kế lịch trình theo yêu cầu, xe riêng 4–16 chỗ', 'ご希望に合わせた日程設計。4〜16人乗りの専用車', '요청에 맞춘 일정 설계, 4~16인승 전용 차량'),
    ('HƯỚNG DẪN VIÊN', '日本語・韓国語ガイド', '일본어·한국어 가이드'),
    ('Hỗ trợ tiếng Nhật và tiếng Hàn', '日本語・韓国語に対応', '일본어·한국어 지원'),
    ('BÁO GIÁ 24 GIỜ', '24時間以内にお見積もり', '24시간 내 견적'),
    ('Báo giá rõ ràng, minh bạch qua email hoặc LINE', 'メールまたはLINEで、明朗なお見積もりをお届け', '이메일 또는 LINE으로 투명한 견적 제공'),
    ('Đón tiễn sân bay', '空港送迎', '공항 송영'),
    ('Xe 4–16 chỗ, đón theo giờ bay, hỗ trợ qua LINE', '4〜16人乗り。フライトに合わせて送迎、LINEでサポート', '4~16인승, 항공편에 맞춘 송영, LINE 지원'),
    ('Thuê xe có tài xế', '運転手付きレンタカー', '기사 포함 차량 대여'),
    ('Xe riêng kèm tài xế, linh hoạt theo lịch trình', '専用車＋ドライバー。日程に合わせて柔軟に対応', '전용 차량과 기사, 일정에 맞춰 유연하게'),
    ('Khách sạn & nhà hàng', 'ホテル＆レストラン', '호텔 & 레스토랑'),
    ('Đặt phòng, đặt bàn, set menu riêng cho khách', 'お部屋・お席の予約、お客様専用のセットメニュー', '객실·좌석 예약, 고객 맞춤 세트 메뉴'),
    ('Phiên dịch', '通訳', '통역'),
    ('Phiên dịch tiếng Nhật, tiếng Hàn cho tour và công tác', 'ツアーや出張のための日本語・韓国語通訳', '투어와 출장을 위한 일본어·한국어 통역'),
    ('NHẬN BÁO GIÁ', 'お見積もりを', '견적을'),
    ('TRONG 24 GIỜ', '24時間以内にお届け', '24시간 내 받아보세요'),
    ('Cho chúng tôi biết ngày đi, số người, có trẻ nhỏ hoặc người cao tuổi đi cùng hay không. Chúng tôi sẽ gửi lịch trình và báo giá trong vòng 24 giờ.',
     '出発日・人数・お子様やご年配の方のご同行の有無をお知らせください。24時間以内に日程案とお見積もりをお送りします。',
     '출발일, 인원, 어린이나 어르신 동반 여부를 알려 주세요. 24시간 이내에 일정안과 견적을 보내 드립니다.'),
    ('Yêu cầu báo giá', '見積もりを依頼する', '견적 요청하기'),
    ('Khánh An Tourism — tour Đà Nẵng – Hội An – Huế, đưa đón và hướng dẫn viên tiếng Nhật, tiếng Hàn.',
     'Khánh An Tourism — ダナン・ホイアン・フエのオプショナルツアー、送迎、ガイド手配。',
     'Khánh An Tourism — 다낭·호이안·후에 옵션 투어, 송영, 가이드 수배.'),
]


TOURS = [
    dict(img='danang/ngu-hanh-son.jpg', time='12:00 – 16:30', meal='Không bao gồm', price=45,
         title=('Tham quan Đà Nẵng nửa ngày (buổi chiều)', 'ダナン市内半日観光【午後発】', '다낭 시내 반나절 관광(오후 출발)'),
         route=('Ngũ Hành Sơn – biển Mỹ Khê – chùa Linh Ứng – Cầu Rồng – bảo tàng Chăm – chợ Hàn – nhà thờ Đà Nẵng',
                '五行山・ミーケービーチ・リンウン寺・ドラゴン橋・チャム彫刻博物館・ハン市場・ダナン大聖堂',
                '오행산 – 미케 비치 – 린응사 – 용다리 – 참 조각 박물관 – 한 시장 – 다낭 대성당')),
    dict(img='tours/op-han-market.jpg', time='Khoảng 4,5 giờ', meal='Bữa trưa hoặc bữa tối', price=100, from_=True,
         title=('Đà Nẵng ngày cuối (tour riêng)', 'ダナン最終日プラン（プライベート）', '다낭 마지막 날 플랜(프라이빗)'),
         route=('Massage dầu 60 phút – mua quà lưu niệm – chợ Hàn, siêu thị – chocolate Marou – bữa ăn – ra sân bay',
                'オイルマッサージ60分・お土産ショッピング・ハン市場／スーパー・マルゥチョコレート・食事・空港へ',
                '오일 마사지 60분 – 기념품 쇼핑 – 한 시장·마트 – 마루 초콜릿 – 식사 – 공항 이동')),
    dict(img='tours/op-han-river.jpg', time='19:00 – 22:00', meal='Bữa tối', price=85,
         title=('Du thuyền sông Hàn & bữa tối', 'ハン川クルーズと夕食ツアー', '한강 크루즈 & 디너 투어'),
         route=('Du thuyền Poseidon trên sông Hàn kèm bữa tối món Âu, đưa đón khách sạn 2 chiều',
                'ポセイドンクルーズでハン川を周遊、ヨーロッパ料理の夕食・ホテル往復送迎付き',
                '포세이돈 크루즈로 한강 유람, 유럽식 저녁·호텔 왕복 픽업 포함')),
    dict(img='danang/cau-vang.jpg', time='8:00 – 15:00', meal='Bữa trưa', price=135,
         title=('Bà Nà Hills nửa ngày', 'バーナーヒルズ半日観光', '바나힐 반나절 관광'),
         route=('Tham quan Bà Nà Hills (vé Wow Pass) – buffet trưa trên núi',
                'バーナーヒルズ観光（ワウパス付き）・山上でのランチビュッフェ',
                '바나힐 관광(와우패스 포함) – 산 위 점심 뷔페')),
    dict(img='tours/op-hoi-an-river.jpg', time='12:00 – 21:30', meal='Bữa tối', price=150, from_=True,
         title=('Bà Nà Hills & Hội An về đêm (buổi chiều)', '【午後発】バーナーヒルズ＆ナイトホイアン観光', '바나힐 & 호이안 야경 투어(오후 출발)'),
         route=('Bà Nà Hills – phố cổ Hội An về đêm – ăn tối đặc sản Hội An – thả đèn hoa đăng – chợ đêm',
                'バーナーヒルズ・夜のホイアン旧市街・ホイアン名物料理の夕食・灯篭流し・ナイトマーケット',
                '바나힐 – 호이안 구시가지 야경 – 호이안 명물 저녁 – 등불 띄우기 – 야시장')),
    dict(img='tours/op-basket-boat.jpg', time='13:00 – 21:00', meal='Bữa tối', price=115,
         title=('Hội An về đêm: thuyền thúng & làm đồ tre', 'ココナッツボート＆バンブークラフト付きホイアンナイトツアー', '바구니배 & 대나무 공예 호이안 야경 투어'),
         route=('Thuyền thúng rừng dừa – làm đồ tre – dạo phố cổ – ăn tối – thả đèn hoa đăng – chợ đêm',
                'ココナッツボート・バンブークラフト体験・旧市街散策・夕食・灯篭流し・ナイトマーケット',
                '코코넛 숲 바구니배 – 대나무 공예 – 구시가지 산책 – 저녁 – 등불 띄우기 – 야시장')),
    dict(img='danang/my-son.jpg', time='8:30 – 21:00', meal='Bữa trưa & bữa tối', price=125,
         title=('Mỹ Sơn & Hội An cả ngày', 'ミーソン遺跡＆ホイアン終日観光', '미선 유적 & 호이안 종일 관광'),
         route=('Thánh địa Mỹ Sơn – ăn trưa mì Quảng – làm đèn lồng – phố cổ Hội An – ăn tối – thả đèn hoa đăng',
                'ミーソン遺跡・ミークアンの昼食・ランタン作り・ホイアン旧市街・夕食・灯篭流し',
                '미선 유적 – 미꽝 점심 – 등불 만들기 – 호이안 구시가지 – 저녁 – 등불 띄우기')),
    dict(img='hue/lang-khai-dinh.jpg', time='8:00 – 18:30', meal='Bữa trưa', price=140,
         title=('Huế cả ngày (đón tại Đà Nẵng, Hội An)', 'フエ終日観光（ダナン・ホイアン発）', '후에 종일 관광(다낭·호이안 출발)'),
         route=('Lăng Tự Đức – lăng Khải Định – ăn trưa món cung đình – Đại Nội – chùa Thiên Mụ',
                'トゥドゥック帝廟・カイディン帝廟・宮廷料理のランチ・グエン朝王宮・ティエンムー寺',
                '뜨득 황릉 – 카이딘 황릉 – 궁중 요리 점심 – 응우옌 왕궁 – 티엔무 사원')),
]

# Tour riêng: chỉ 1 ngày (theo yêu cầu)
PRIVATE_TOURS = [
    dict(img='danang/cau-rong.jpg', time='1 ngày', meal='Theo yêu cầu', price=190, from_=True, suffix='/2 khách',
         title=('Tour riêng Đà Nẵng 1 ngày', 'ダナン市内 プライベートツアー 1日', '다낭 시내 프라이빗 투어 1일'),
         route=('Ngũ Hành Sơn – biển Mỹ Khê – chùa Linh Ứng – Cầu Rồng – bảo tàng Chăm – chợ Hàn – nhà thờ Đà Nẵng',
                '五行山・ミーケービーチ・リンウン寺・ドラゴン橋・チャム彫刻博物館・ハン市場・ダナン大聖堂',
                '오행산 – 미케 비치 – 린응사 – 용다리 – 참 조각 박물관 – 한 시장 – 다낭 대성당')),
    dict(img='danang/ba-na-hills.jpg', time='1 ngày', meal='Theo yêu cầu', price=230, from_=True, suffix='/2 khách',
         title=('Tour riêng Bà Nà Hills 1 ngày', 'バーナーヒルズ プライベートツアー 1日', '바나힐 프라이빗 투어 1일'),
         route=('Bà Nà Hills (vé Wow Pass) – Làng Pháp – vườn hoa Le Jardin – Cầu Vàng – buffet trưa',
                'バーナーヒルズ（ワウパス付き）・フランス村・ル・ジャルダン庭園・ゴールデンブリッジ・ランチビュッフェ',
                '바나힐(와우패스 포함) – 프랑스 마을 – 르 자르댕 정원 – 골든브릿지 – 점심 뷔페')),
    dict(img='tours/op-lanterns.jpg', time='1 ngày', meal='Theo yêu cầu', price=200, from_=True, suffix='/2 khách',
         title=('Tour riêng Hội An & rừng dừa Cẩm Thanh 1 ngày', 'ホイアン＆カムタン ココナッツ林 プライベートツアー 1日', '호이안 & 깜타인 코코넛 숲 프라이빗 투어 1일'),
         route=('Phố cổ Hội An – thuyền thúng rừng dừa Cẩm Thanh – làng nghề truyền thống – chợ đêm',
                'ホイアン旧市街・カムタン ココナッツ林のバスケットボート・伝統工芸村・ナイトマーケット',
                '호이안 구시가지 – 깜타인 코코넛 숲 바구니배 – 전통 공예 마을 – 야시장')),
    dict(img='danang/my-son.jpg', time='1 ngày', meal='Theo yêu cầu', price=220, from_=True, suffix='/2 khách',
         title=('Tour riêng Mỹ Sơn & Hội An 1 ngày', 'ミーソン遺跡＆ホイアン プライベートツアー 1日', '미선 유적 & 호이안 프라이빗 투어 1일'),
         route=('Thánh địa Mỹ Sơn – làng gốm Thanh Hà – phố cổ Hội An – thả đèn hoa đăng',
                'ミーソン遺跡・タインハー陶芸村・ホイアン旧市街・灯篭流し',
                '미선 유적 – 타인하 도자기 마을 – 호이안 구시가지 – 등불 띄우기')),
    dict(img='hue/lang-tu-duc.jpg', time='1 ngày', meal='Theo yêu cầu', price=260, from_=True, suffix='/2 khách',
         title=('Tour riêng Huế – Đà Nẵng 1 ngày', 'フエ～ダナン プライベートツアー 1日', '후에~다낭 프라이빗 투어 1일'),
         route=('Lăng Tự Đức – lăng Khải Định – Đại Nội – chùa Thiên Mụ – đèo Hải Vân',
                'トゥドゥック帝廟・カイディン帝廟・グエン朝王宮・ティエンムー寺・ハイヴァン峠',
                '뜨득 황릉 – 카이딘 황릉 – 응우옌 왕궁 – 티엔무 사원 – 하이반 고개')),
]

# Tour gia đình: 2 ngày 1 đêm, 3 ngày 2 đêm, 4 ngày 3 đêm
FAMILY_TOURS = [
    dict(img='danang/cau-vang.jpg', time='2 ngày 1 đêm', price=300,
         title=('Tour gia đình Đà Nẵng – Hội An 2 ngày 1 đêm', 'ダナン・ホイアン ファミリーツアー 1泊2日', '다낭·호이안 패밀리 투어 1박 2일'),
         route=('Bà Nà Hills – phố cổ Hội An – thuyền thúng rừng dừa – chợ đêm Hội An',
                'バーナーヒルズ・ホイアン旧市街・ココナッツボート・ホイアンナイトマーケット',
                '바나힐 – 호이안 구시가지 – 코코넛 바구니배 – 호이안 야시장')),
    dict(img='danang/hoi-an.jpg', time='3 ngày 2 đêm', price=400,
         title=('Tour gia đình Đà Nẵng – Hội An – Huế 3 ngày 2 đêm', 'ダナン・ホイアン・フエ ファミリーツアー 2泊3日', '다낭·호이안·후에 패밀리 투어 2박 3일'),
         route=('Bà Nà Hills – Hội An – Mỹ Sơn – Huế – biển Mỹ Khê',
                'バーナーヒルズ・ホイアン・ミーソン遺跡・フエ・ミーケービーチ',
                '바나힐 – 호이안 – 미선 유적 – 후에 – 미케 비치')),
    dict(img='hue/lang-khai-dinh.jpg', time='4 ngày 3 đêm', price=500,
         title=('Tour gia đình miền Trung 4 ngày 3 đêm', 'ベトナム中部 ファミリーツアー 3泊4日', '베트남 중부 패밀리 투어 3박 4일'),
         route=('Đà Nẵng – Bà Nà Hills – Hội An – Mỹ Sơn – Huế – biển Mỹ Khê',
                'ダナン・バーナーヒルズ・ホイアン・ミーソン遺跡・フエ・ミーケービーチ',
                '다낭 – 바나힐 – 호이안 – 미선 유적 – 후에 – 미케 비치')),
]

# Tour đặc biệt: golf, trekking, lặn biển, trải nghiệm đời sống địa phương
SPECIAL_TOURS = [
    dict(img='tours/golf-palm-path.jpg', time='2 ngày 1 đêm', price=350, from_=True,
         title=('Tour golf Bà Nà Hills 2 ngày 1 đêm', 'バーナーヒルズ ゴルフツアー 1泊2日', '바나힐 골프 투어 1박 2일'),
         route=('18 lỗ tại sân golf Bà Nà Hills – caddie – xe đưa đón – khách sạn 4 sao',
                'バーナーヒルズゴルフコース18ホール・キャディー・送迎・4つ星ホテル',
                '바나힐 골프장 18홀 – 캐디 – 송영 – 4성급 호텔')),
    dict(img='tours/forest-son-tra.jpg', time='1 ngày', price=75,
         title=('Trekking bán đảo Sơn Trà 1 ngày', 'ソンチャー半島 トレッキング 1日', '선짜 반도 트레킹 1일'),
         route=('Rừng nguyên sinh Sơn Trà – ngắm vịnh Đà Nẵng – bãi biển hoang sơ – hải đăng',
                'ソンチャー原生林・ダナン湾の眺め・手つかずのビーチ・灯台',
                '선짜 원시림 – 다낭만 전망 – 자연 그대로의 해변 – 등대')),
    dict(img='tours/dive-cu-lao-cham.jpg', time='1 ngày', price=68,
         title=('Lặn biển ngắm san hô Cù Lao Chàm 1 ngày', 'クーラオチャム サンゴ礁ダイビング 1日', '꾸라오짬 산호초 다이빙 1일'),
         route=('Cano cao tốc ra Cù Lao Chàm – lặn ngắm san hô – bãi Ông – bữa trưa hải sản',
                'スピードボートでクーラオチャムへ・サンゴ礁ダイビング・バイオンビーチ・シーフードランチ',
                '스피드보트로 꾸라오짬 이동 – 산호초 다이빙 – 바이옹 해변 – 해산물 점심')),
    dict(img='tours/op-basket-boat.jpg', time='1 ngày', price=55,
         title=('Trải nghiệm đời sống địa phương Hội An 1 ngày', 'ホイアン ローカル生活体験 1日', '호이안 현지 생활 체험 1일'),
         route=('Đi chợ sớm – nấu món Việt – thuyền thúng rừng dừa – thăm nhà dân – làm nghề truyền thống',
                '朝市散策・ベトナム料理作り・ココナッツボート・地元の家訪問・伝統工芸体験',
                '아침 시장 – 베트남 요리 만들기 – 코코넛 바구니배 – 현지 가정 방문 – 전통 공예 체험')),
]

GROUPS = [
    ('RIÊNG', PRIVATE_TOURS),
    ('GIA ĐÌNH', FAMILY_TOURS),
    ('ĐẶC BIỆT', SPECIAL_TOURS),
]

ALL_TOURS = TOURS + PRIVATE_TOURS + FAMILY_TOURS + SPECIAL_TOURS

ROWS = LABELS + [t['title'] for t in ALL_TOURS] + [t['route'] for t in ALL_TOURS]

