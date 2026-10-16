"""Bản dịch trang chủ: tiếng Nhật (mặc định, index.html) và tiếng Hàn (ko.html).

build-html.py dựng trang bằng tiếng Việt rồi gọi render(page, lang). Hàm này dịch chữ trong
nội dung và trong các thuộc tính alt/title/aria-label/placeholder/value/content theo bảng TR
(khớp cụm dài nhất trước, chỉ thay một lượt). Khi thêm hoặc sửa chữ tiếng Việt ở trang,
nhớ thêm bản dịch vào TR; build sẽ báo những đoạn chưa dịch.
"""
import html
import re

LANGS = {
    'ja': dict(file='index.html', html_lang='ja', label='日本語', flag='JP'),
    'ko': dict(file='ko.html', html_lang='ko', label='한국어', flag='KR'),
}
DEFAULT = 'ja'

# (tiếng Việt, tiếng Nhật, tiếng Hàn)
_ROWS = [
    ('Khánh An Tourist - Trang chủ', 'Khánh An Tourist - ホーム', 'Khánh An Tourist - 홈'),
    ('Khánh An Tourist — tour trong nước, tour nước ngoài, visa, vé máy bay.',
     'Khánh An Tourist — ベトナム国内ツアー・海外ツアー・ビザ・航空券。',
     'Khánh An Tourist — 베트남 국내 투어, 해외 투어, 비자, 항공권.'),
    ('Skip to content', '本文へスキップ', '본문 바로가기'),
    ('Tuyển dụng', '採用情報', '채용'),
    ('Hướng dẫn thanh toán', 'お支払い方法', '결제 안내'),
    ('Liên hệ', 'お問い合わせ', '문의하기'),
    ('Trang chủ', 'ホーム', '홈'),
    ('Giới thiệu', '会社案内', '회사 소개'),
    ('Tour du lịch', 'ツアー', '투어'),
    ('Tour nước ngoài', '海外ツアー', '해외 투어'),
    ('Tour trong nước', 'ベトナム国内ツアー', '베트남 국내 투어'),
    ('Cẩm nang du lịch Tin tức', '旅行ガイド・ニュース', '여행 가이드 · 뉴스'),
    ('Cẩm nang du lịch', '旅行ガイド', '여행 가이드'),
    ('Visa du lịch', '観光ビザ', '관광 비자'),
    ('Tin tức', 'ニュース', '뉴스'),
    ('Tìm kiếm:', '検索:', '검색:'),
    ('Tìm kiếm', '検索', '검색'),
    ('Nhập từ khóa cần tìm', 'キーワードを入力', '검색어를 입력하세요'),
    ('Khám phá Đà Nẵng', 'ダナンを探索', '다낭 탐험'),
    ('Biểu tượng', 'シンボル', '랜드마크'),
    ('Xem tour Đà Nẵng', 'ダナンツアーを見る', '다낭 투어 보기'),
    ('Đà Nẵng', 'ダナン', '다낭'),
    ('Cầu Vàng', 'ゴールデンブリッジ', '골든 브릿지'),
    ('Sun World Bà Nà Hills', 'サンワールド・バーナーヒルズ', '선월드 바나힐'),
    ('Bà Nà Hills', 'バーナーヒルズ', '바나힐'),
    ('Núi Chúa', 'チュア山', '쭈아산'),
    ('Phố cổ Hội An', 'ホイアン旧市街', '호이안 구시가지'),
    ('Hội An', 'ホイアン', '호이안'),
    ('Cầu Rồng', 'ドラゴン橋', '용다리'),
    ('Sông Hàn', 'ハン川', '한강'),
    ('Ngũ Hành Sơn', '五行山', '오행산'),
    ('Non Nước', 'ノンヌォック', '논느억'),
    ('Biển Mỹ Khê', 'ミーケービーチ', '미케 비치'),
    ('Bán đảo Sơn Trà', 'ソンチャー半島', '선짜 반도'),
    ('Sơn Trà', 'ソンチャー', '선짜'),
    ('Chùa Linh Ứng', 'リンウン寺', '린응사'),
    ('Ảnh:', '写真:', '사진:'),
    ('Cây cầu dát vàng dài khoảng 150 m uốn lượn giữa mây trời ở độ cao gần 1.400 m, được nâng đỡ bởi đôi bàn tay đá khổng lồ. Từ khi khánh thành năm 2018, Cầu Vàng trở thành biểu tượng du lịch mới của Đà Nẵng.',
     '標高約1,400mの雲の上をうねる全長約150mの金色の橋。巨大な石の両手に支えられています。2018年の開通以来、ダナン観光の新たなシンボルとなりました。',
     '해발 약 1,400m 구름 위를 굽이치는 길이 약 150m의 황금빛 다리로, 거대한 돌손이 다리를 받치고 있습니다. 2018년 개통 이후 다낭 관광의 새로운 상징이 되었습니다.'),
    ('Khu du lịch trên đỉnh núi Chúa cao 1.487 m, khí hậu mát mẻ quanh năm với trải nghiệm “4 mùa trong 1 ngày”. Hệ thống cáp treo đưa du khách tới Làng Pháp, vườn hoa Le Jardin d’Amour và khu vui chơi Fantasy Park.',
     '標高1,487mのチュア山頂にあるリゾート。一年中涼しく「1日で四季」を体験できます。ロープウェイでフレンチビレッジ、ル・ジャルダン・ダムール庭園、ファンタジーパークへ。',
     '해발 1,487m 쭈아산 정상의 리조트로, 일 년 내내 선선해 “하루에 사계절”을 경험할 수 있습니다. 케이블카를 타고 프렌치 빌리지, 르 자르댕 다무르 정원, 판타지 파크로 이동합니다.'),
    ('Thương cảng sầm uất từ thế kỷ XVI – XVII, được UNESCO công nhận Di sản Văn hóa Thế giới năm 1999. Những dãy nhà tường vàng, Chùa Cầu và đèn lồng lung linh mỗi tối tạo nên vẻ đẹp hoài cổ khó quên.',
     '16〜17世紀に栄えた交易港で、1999年にユネスコ世界文化遺産に登録。黄色い壁の家並み、日本橋（来遠橋）、夜を彩るランタンが忘れがたいノスタルジックな風景をつくります。',
     '16~17세기 번성했던 무역항으로 1999년 유네스코 세계문화유산에 등재되었습니다. 노란 벽의 옛 가옥, 내원교(일본 다리), 밤마다 빛나는 등불이 잊지 못할 고풍스러운 풍경을 만듭니다.'),
    ('Cây cầu hình rồng vàng vươn mình trên sông Hàn, dài 666 m, khánh thành năm 2013. Vào 21h tối thứ Bảy và Chủ nhật, đầu rồng phun lửa, phun nước – màn trình diễn không thể bỏ lỡ.',
     'ハン川に架かる全長666mの金色の龍の橋（2013年開通）。毎週土・日曜21時には龍の頭から火と水が噴き出す、見逃せないショーが行われます。',
     '한강 위로 솟은 길이 666m의 황금 용 모양 다리로 2013년에 개통했습니다. 매주 토·일요일 밤 9시에는 용머리에서 불과 물을 뿜는 쇼가 펼쳐집니다.'),
    ('Quần thể 5 ngọn núi đá vôi Kim, Mộc, Thủy, Hỏa, Thổ nằm cạnh biển, ẩn chứa nhiều hang động và chùa cổ như động Huyền Không, chùa Tam Thai. Dưới chân núi là làng đá mỹ nghệ Non Nước lâu đời.',
     '海辺に並ぶ金・木・水・火・土の5つの石灰岩の山々。フエンコン洞窟やタムタイ寺など多くの洞窟と古刹が点在し、麓には歴史あるノンヌォック石彫り村があります。',
     '바닷가에 자리한 금·목·수·화·토 다섯 개의 석회암 산으로, 후옌콩 동굴과 땀타이 사원 등 많은 동굴과 고찰이 있습니다. 산기슭에는 오랜 역사의 논느억 석공예 마을이 있습니다.'),
    ('Bãi biển cát trắng mịn, nước trong xanh và sóng êm, từng được tạp chí Forbes bình chọn là một trong những bãi biển quyến rũ nhất hành tinh. Lý tưởng để tắm biển, chèo SUP và ngắm bình minh.',
     '白く細かな砂、透き通った海と穏やかな波。フォーブス誌で「世界で最も魅力的なビーチ」の一つに選ばれました。海水浴やSUP、朝日鑑賞に最適です。',
     '고운 백사장과 맑은 바다, 잔잔한 파도를 갖춘 해변으로 포브스지가 선정한 세계에서 가장 매력적인 해변 중 하나입니다. 해수욕, SUP, 일출 감상에 제격입니다.'),
    ('“Lá phổi xanh” của Đà Nẵng với rừng nguyên sinh và loài voọc chà vá chân nâu quý hiếm. Chùa Linh Ứng trên bán đảo có tượng Phật Bà Quan Âm cao 67 m hướng ra biển Đông.',
     '原生林と希少なアカアシドゥクラングールが暮らす、ダナンの「緑の肺」。半島のリンウン寺には海を見守る高さ67mの観音像が立っています。',
     '원시림과 희귀한 붉은다리두크원숭이가 사는 다낭의 “녹색 허파”입니다. 반도의 린응사에는 바다를 바라보는 높이 67m의 해수관음상이 서 있습니다.'),
    ('Vị trí', '場所', '위치'),
    ('Khoảng cách', '距離', '거리'),
    ('Thời điểm đẹp', 'ベストシーズン', '추천 시기'),
    ('Sáng sớm, tháng 3 – 8', '早朝・3〜8月', '이른 아침, 3~8월'),
    ('Sáng sớm, hoàng hôn', '早朝・夕暮れ', '이른 아침, 해질녘'),
    ('Độ cao', '標高', '해발'),
    ('Nhiệt độ', '気温', '기온'),
    ('Di sản', '世界遺産', '세계유산'),
    ('Nên đi', 'おすすめ', '추천'),
    ('Chiều tối, đêm rằm', '夕方・満月の夜', '저녁, 보름밤'),
    ('Chiều dài', '全長', '길이'),
    ('Phun lửa', '火のショー', '불쇼'),
    ('21:00 T7 & CN', '土・日 21:00', '토·일 21:00'),
    ('Trung tâm thành phố', '市内中心部', '시내 중심'),
    ('Nổi bật', '見どころ', '볼거리'),
    ('Động Huyền Không', 'フエンコン洞窟', '후옌콩 동굴'),
    ('Tham quan', '所要時間', '소요 시간'),
    ('2 – 3 giờ', '2〜3時間', '2~3시간'),
    ('Mùa tắm biển', '海水浴シーズン', '해수욕 시즌'),
    ('Tháng 4 – 8', '4〜8月', '4~8월'),
    ('Đặc sản', '名物', '명물'),
    ('Hải sản tươi sống', '新鮮な海鮮', '신선한 해산물'),
    ('Tượng Quan Âm', '観音像', '해수관음상'),
    ('Cao 67 m', '高さ67m', '높이 67m'),
    ('BẠN MUỐN', 'どこへ', '어디로'),
    ('ĐI ĐÂU', '行きたい？', '떠나볼까요?'),
    ('Đã có lượt khách', '多数のお客様にご利用', '많은 여행객이 방문'),
    ('TOUR', 'ツアー', '투어'),
    ('NỔI BẬT', '注目', '추천'),
    ('NƯỚC NGOÀI', '海外', '해외'),
    ('TRONG NƯỚC', '国内', '국내'),
    ('COMBO GIÁ RẺ', 'お得なパック', '알뜰 패키지'),
    ('Khởi hành hàng tuần', '毎週出発', '매주 출발'),
    ('Mã tour:', 'ツアーコード:', '투어 코드:'),
    ('Khởi hành:', '出発地:', '출발지:'),
    ('/khách', '/名', '/인'),
    ('đã liên hệ', '件のお問い合わせ', '건 문의'),
    ('Đặt Tour', '予約する', '예약하기'),
    ('Đà Nẵng, Hà Nội, Tp Hồ Chí Minh', 'ダナン、ハノイ、ホーチミン', '다낭, 하노이, 호찌민'),
    ('Đà Nẵng, Hà Nội', 'ダナン、ハノイ', '다낭, 하노이'),
    ('Hà Nội', 'ハノイ', '하노이'),
    ('Du lịch Trung Quốc: Đảo Hải Nam – Tam Á – Hải Hoa Đảo 4N3Đ', '中国旅行：海南島・三亜・海花島 4日間', '중국 여행: 하이난섬 – 싼야 – 하이화섬 3박 4일'),
    ('Du lịch Trung Quốc: Hà Nội – Thành Đô – Đô Giang Yến – Cửu Trại Câu –Mậu Huyện – Gia Cô Sơn 6N5Đ',
     '中国旅行：ハノイ・成都・都江堰・九寨溝・茂県・甲居山 6日間',
     '중국 여행: 하노이 – 청두 – 두장옌 – 주자이거우 – 마오현 – 자쥐산 5박 6일'),
    ('Tour Du Lịch Hà Giang – Sông Nho Quế – Cao Nguyên Đá Đồng Văn 3N2Đ',
     'ハザン・ニョークエ川・ドンバン石灰岩高原ツアー 3日間',
     '하장 – 뇨꿰강 – 동반 카르스트 고원 투어 2박 3일'),
    ('Du Lịch Tây Bắc: Mù Cang Chải – Đèo Khau Phạ – Tú Lệ – Trạm Tấu 3N2Đ',
     '西北部の旅：ムーカンチャイ・カウファー峠・トゥレ・チャムタウ 3日間',
     '서북부 여행: 무캉짜이 – 카우파 고개 – 뚜레 – 짬따우 2박 3일'),
    ('Du Lịch Mộc Châu – Mai Châu – Cầu Kính Bạch Long 2N1Đ', 'モックチャウ・マイチャウ・バクロンガラス橋 2日間', '목쩌우 – 마이쩌우 – 박롱 유리다리 1박 2일'),
    ('Du Lịch Đài Loan: Đài Bắc – Đài Trung – Cao Hùng 5N4Đ', '台湾旅行：台北・台中・高雄 5日間', '대만 여행: 타이베이 – 타이중 – 가오슝 4박 5일'),
    ('Du Lịch Trung Quốc Giá Rẻ: Hà Khẩu – Bình Biên – Kiến Thủy – Mông Tự 3N2Đ',
     '格安中国旅行：河口・屏辺・建水・蒙自 3日間',
     '중국 알뜰 여행: 허커우 – 핑볜 – 젠수이 – 멍쯔 2박 3일'),
    ('Tour golf', 'ゴルフツアー', '골프 투어'),
    ('Tour du thuyền', 'クルーズツアー', '크루즈 투어'),
    ('GOLF', 'ゴルフ', '골프'),
    ('DU THUYỀN', 'クルーズ', '크루즈'),
    ('Hà Nội, Đà Nẵng', 'ハノイ、ダナン', '하노이, 다낭'),
    ('Tour Golf Đà Nẵng – Hội An: BRG Danang Golf – Montgomerie Links – Hoiana Shores 4N3Đ',
     'ダナン・ホイアン ゴルフツアー：BRGダナンゴルフ・モンゴメリーリンクス・ホイアナショアーズ 4日間',
     '다낭 – 호이안 골프 투어: BRG 다낭 골프 – 몽고메리 링크스 – 호이아나 쇼어스 3박 4일'),
    ('Tour Golf Huế – Lăng Cô: Laguna Golf Lăng Cô & sân golf Huế 3N2Đ',
     'フエ・ランコー ゴルフツアー：ラグーナゴルフ・ランコー＆フエのゴルフ場 3日間',
     '후에 – 랑꼬 골프 투어: 라구나 골프 랑꼬 & 후에 골프장 2박 3일'),
    ('Golf Bà Nà Hills Golf Club & nghỉ dưỡng biển Đà Nẵng 2N1Đ', 'バーナーヒルズ・ゴルフクラブ＆ダナンのビーチリゾート 2日間', '바나힐 골프 클럽 & 다낭 해변 휴양 1박 2일'),
    ('Tour Golf Hà Nội – Tam Đảo Golf Resort – Sky Lake 3N2Đ', 'ハノイ ゴルフツアー：タムダオ・ゴルフリゾート・スカイレイク 3日間', '하노이 골프 투어: 땀다오 골프 리조트 – 스카이 레이크 2박 3일'),
    ('Du thuyền 5 sao vịnh Hạ Long 2N1Đ', 'ハロン湾 5つ星クルーズ 2日間', '하롱베이 5성급 크루즈 1박 2일'),
    ('Du thuyền vịnh Lan Hạ – Cát Bà 3N2Đ', 'ランハー湾・カットバ島クルーズ 3日間', '란하베이 – 깟바섬 크루즈 2박 3일'),
    ('Du thuyền trong ngày vịnh Hạ Long – hang Sửng Sốt – đảo Ti Tốp',
     'ハロン湾日帰りクルーズ：スンソット洞窟・ティートップ島',
     '하롱베이 당일 크루즈: 승솟 동굴 – 티톱섬'),
    ('Du thuyền buồm truyền thống ngắm hoàng hôn vịnh Hạ Long 2N1Đ', '伝統的な帆船で楽しむハロン湾サンセットクルーズ 2日間', '전통 범선으로 즐기는 하롱베이 선셋 크루즈 1박 2일'),
    ('VÌ SAO CHỌN', '選ばれる', '선택하는'),
    ('CHÚNG TÔI', '理由', '이유'),
    ('Dịch vụ Tour nội địa và quốc tế', '国内・海外ツアーサービス', '국내·해외 투어 서비스'),
    ('Công ty lữ hành tại Việt Nam', 'ベトナムの旅行会社', '베트남 여행사'),
    ('các đơn vị làm VISA nước ngoài', '海外ビザ代行会社', '해외 비자 대행사'),
    ('ĐẶT TOUR', 'かんたん予約', '간편 예약'),
    ('Dễ dàng nhanh chóng chỉ 3 bước', 'わずか3ステップで簡単・スピーディー', '단 3단계로 쉽고 빠르게'),
    ('THANH TOÁN', 'お支払い', '결제'),
    ('Đơn giản, an toàn và linh hoạt', 'シンプル・安全・柔軟', '간편하고 안전하며 유연하게'),
    ('Trực tuyến 24/7', '24時間対応', '24시간 상담'),
    ('CÁC DỊCH VỤ', '私たちの', '우리의'),
    ('CỦA CHÚNG TÔI', 'サービス', '서비스'),
    ('Hội chợ quốc tế', '国際見本市', '국제 박람회'),
    ('Chuyên tour hội chợ quốc tế các nước trên thế giới', '世界各国の国際見本市ツアーを専門に手配', '세계 각국 국제 박람회 투어 전문'),
    ('Sim quốc tế', '海外SIM', '해외 유심'),
    ('Bán sim nghe gọi & data các nước trên thế giới', '世界各国の通話・データSIMを販売', '세계 각국 통화·데이터 유심 판매'),
    ('Dịch vụ Visa nhanh, rẻ. Visa trọn gói, thủ tục đơn giản', 'スピーディーで格安なビザ申請代行。手続きもまるごとお任せ', '빠르고 저렴한 비자 대행, 간편한 원스톱 수속'),
    ('Vé máy bay', '航空券', '항공권'),
    ('Vé máy bay giá rẻ nhất, nhiều khuyến mãi hấp dẫn', '最安値の航空券とお得なキャンペーン多数', '최저가 항공권과 다양한 프로모션'),
    ('VISA', 'ビザ', '비자'),
    ('KHOẢNH KHẮC', 'ベスト', '베스트'),
    ('ĐẸP NHẤT', 'ショット', '모먼트'),
    ('KHÁCH HÀNG NÓI GÌ', 'お客様の', '고객'),
    ('VỀ CHÚNG TÔI', '声', '후기'),
    ('Đánh giá, cảm nhận của khách hàng đã sử dụng dịch vụ của chúng tôi',
     '当社をご利用いただいたお客様からのご感想',
     '저희 서비스를 이용하신 고객님들의 후기'),
    ('Lại một lần nữa công ty SANSHIN đồng hành cùng Khánh An Tourist trong chuyến du lịch Hạ Long. Mọi thứ đều tốt đẹp, hướng dẫn viên “anh Thành” luôn chu đáo từng bữa ăn, từng chỗ ngủ trong khách sạn, đoàn chúng tôi luôn an tâm khi đi cùng Khánh An Tourist trong mọi chuyến du lịch trong và ngoài nước. Khánh An Tourist luôn trong suy nghĩ đầu tiên của chúng tôi trong mỗi lần có ý định đi du lịch. Cảm ơn Khánh An Tourist đã nhiệt tình hỗ trợ hết mình',
     '今回もSANSHINはKhánh An Touristと一緒にハロン湾旅行へ行きました。すべてが素晴らしく、ガイドの「タインさん」は毎回の食事からホテルの部屋まで細やかに気を配ってくれました。国内外どの旅行でもKhánh An Touristと一緒なら安心です。旅行を考えるとき、いつも真っ先に思い浮かぶのがKhánh An Touristです。心のこもったサポートをありがとうございました。',
     '이번에도 SANSHIN은 Khánh An Tourist와 함께 하롱베이 여행을 다녀왔습니다. 모든 것이 훌륭했고, 가이드 “타잉 씨”는 매 식사와 호텔 객실까지 세심하게 챙겨 주었습니다. 국내외 어떤 여행이든 Khánh An Tourist와 함께라면 안심입니다. 여행을 계획할 때마다 가장 먼저 떠오르는 곳이 Khánh An Tourist입니다. 정성 어린 지원에 감사드립니다.'),
    ('Công ty TNHH SANSHIN Hà Nội', 'SANSHIN ハノイ有限会社', 'SANSHIN 하노이 유한회사'),
    ('Tour Hạ Long náo nhiệt', 'にぎやかなハロン湾ツアー', '활기찬 하롱베이 투어'),
    ('Chúng tôi du lịch tới đảo Phú Quốc xinh đẹp. Được đồng hành cùng công ty du lịch Khánh An Tourist. Chúng tôi thấy được quan tâm chăm sóc tận tình từng bữa ăn giấc ngủ khi đi du lịch. Hướng dẫn viên của công ty Khánh An Tourist chu đáo, tận tình. Trước ngày đi chúng tôi còn được công ty thông báo đến từng người giờ khởi hành và những thứ cần chuẩn bị. Công ty Khánh An Tourist sẽ là lựa chọn tin tưởng nhất cho những chuyến du lịch lần sau.',
     'Khánh An Touristと一緒に美しいフーコック島へ旅行しました。旅行中は食事から睡眠まで心のこもったお世話をしていただきました。ガイドさんも親切で丁寧です。出発前には出発時刻や持ち物を一人ひとりに案内してくれました。次の旅行もKhánh An Touristにお願いしたいと思います。',
     'Khánh An Tourist와 함께 아름다운 푸꾸옥섬을 여행했습니다. 여행 내내 식사부터 숙박까지 세심한 보살핌을 받았고, 가이드도 친절하고 꼼꼼했습니다. 출발 전에는 출발 시간과 준비물을 한 사람씩 안내해 주었습니다. 다음 여행도 Khánh An Tourist에 맡기고 싶습니다.'),
    ('Cảm nhận về tour Phú Quốc do công ty tổ chức', '当社主催フーコック島ツアーのご感想', '당사 푸꾸옥 투어 이용 후기'),
    ('Tài khoản chính thức', '公式アカウント', '공식 계정'),
    ('Kết bạn', '友だち追加', '친구 추가'),
    ('Ưu đãi cho bạn bè LINE', 'LINE友だち限定クーポン', 'LINE 친구 전용 쿠폰'),
    ('Giảm % cho khách hàng kết bạn LINE chính thức của CHÚNG TÔI', 'LINE公式アカウントの友だち追加で割引！', 'LINE 공식 계정 친구 추가 시 할인!'),
    ('Đặt tour dễ dàng trên Website & LINE', 'ウェブサイト＆LINEでかんたんツアー予約', '웹사이트 & LINE으로 간편한 투어 예약'),
    ('Để lại mail chúng tôi sẽ gửi chương trình chi tiết tới bạn.', 'メールアドレスをご登録いただくと、キャンペーンの詳細をお送りします。', '이메일을 남겨 주시면 프로모션 상세 내용을 보내 드립니다.'),
    ('Quét mã QR để được tư vấn nhanh nhất', 'QRコードを読み取って今すぐ相談', 'QR 코드를 스캔하고 바로 상담하세요'),
    ('Mã QR LINE', 'LINE QRコード', 'LINE QR 코드'),
    ('TIN TỨC', '旅行', '여행'),
    ('DU LỊCH', 'ニュース', '뉴스'),
    ('Chia sẽ những thông tin du lịch triển lãm nhanh nhất & những bí quyết khi tham gia tour hội chợ',
     '展示会旅行の最新情報と見本市ツアー参加のコツをお届けします',
     '박람회 여행 최신 정보와 박람회 투어 참가 노하우를 전해 드립니다'),
    ('TOP 5 điểm vui chơi nghỉ dưỡng tuyệt vời tại Phú Quốc giới trẻ không thể bỏ lỡ',
     '若者必見！フーコック島の最高のリゾート＆遊びスポット TOP5',
     '젊은 여행자라면 놓칠 수 없는 푸꾸옥 최고의 휴양·놀거리 TOP 5'),
    ('Những địa điểm du lịch Trung Quốc không cần hộ chiếu', 'パスポート不要で行ける中国の観光地', '여권 없이 갈 수 있는 중국 여행지'),
    ('Chỉ Với Giấy Thông Hành, Đi Đâu Du Lịch Trung Quốc?', '通行証だけで行ける中国旅行先は？', '통행증만으로 갈 수 있는 중국 여행지는?'),
    ('Địa điểm vui chơi trung thu tiết kiệm nhất từ Bắc vào Nam', '北から南まで、お得に楽しめる中秋節スポット', '북부에서 남부까지, 가성비 좋은 추석 나들이 명소'),
    ('Trải nghiệm một ngày tại quận nghèo nhất hồng kông- thâm thủy bộ',
     '香港で最も庶民的な街・深水埗で過ごす一日',
     '홍콩의 서민 동네 삼수이포에서 보내는 하루'),
    ('Du Lịch Hàn Quốc: Khám Phá Khu Rừng Lá Đỏ Đầy Mê Hoặc Hwadam', '韓国旅行：魅惑の紅葉の森・花潭（ファダム）を探訪', '한국 여행: 매혹적인 단풍 숲 화담숲 탐방'),
    ('📍 Địa chỉ', '📍 住所', '📍 주소'),
    ('🏠 Chi nhánh Hoà Bình', '🏠 ホアビン支店', '🏠 호아빈 지점'),
    ('🏠 Chi nhánh Hải Phòng', '🏠 ハイフォン支店', '🏠 하이퐁 지점'),
    ('🏠 Chi nhánh Nam Định', '🏠 ナムディン支店', '🏠 남딘 지점'),
    ('☎️ Hotline', '☎️ ホットライン', '☎️ 핫라인'),
    ('✉️ Email', '✉️ メール', '✉️ 이메일'),
    ('THÔNG TIN CẦN BIẾT', 'ご案内', '이용 안내'),
    ('Hình thức thanh toán', 'お支払い方法', '결제 방법'),
    ('Chính sách hoàn hủy', 'キャンセルポリシー', '취소·환불 정책'),
    ('Chính sách bảo mật', 'プライバシーポリシー', '개인정보 처리방침'),
    ('Điều khoản giao dịch', 'ご利用規約', '이용 약관'),
    ('CHỨNG NHẬN', '認証', '인증'),
    ('ĐĂNG KÝ NHẬN BẢN TIN', 'ニュースレター登録', '뉴스레터 구독'),
    ('Nhập địa chỉ email để nhận thông tin mới nhất từ chúng tôi.', 'メールアドレスを入力して最新情報を受け取る。', '이메일을 입력하고 최신 소식을 받아 보세요.'),
    ('Giấy phép kinh doanh số 01033619401 do sở KH&ĐT TP abc cấp ngày 21/23 năm 2323',
     '事業登録番号 01033619401（abc市計画投資局 発行日 2323年21/23）',
     '사업자 등록번호 01033619401 (abc시 기획투자국 발급, 2323년 21/23)'),
    ('Giấy phép Kinh doanh Lữ hành Quốc tế số 01711D/S2015/TCDL-GPLHabc',
     '国際旅行業登録番号 01711D/S2015/TCDL-GPLHabc',
     '국제 여행업 허가번호 01711D/S2015/TCDL-GPLHabc'),
    ('Kết nối với chúng tôi', 'フォローする', '팔로우하기'),
    ('Chấp nhận thanh toán', '対応決済', '결제 수단'),
    ('Địa chỉ email...', 'メールアドレス...', '이메일 주소...'),
    ('Gửi', '送信', '보내기'),
    ('Địa điểm nổi tiếng Đà Nẵng', 'ダナンの人気スポット', '다낭 인기 명소'),
    ('Lăng tẩm Huế', 'フエの帝廟', '후에 황릉'),
    ('Lăng Khải Định', 'カイディン帝廟', '카이딘 황릉'),
    ('Lăng Tự Đức', 'トゥドゥック帝廟', '뜨득 황릉'),
    ('Lăng Minh Mạng', 'ミンマン帝廟', '민망 황릉'),
    ('Lăng Đồng Khánh', 'ドンカイン帝廟', '동카인 황릉'),
    ('Tour lặn biển', 'ダイビングツアー', '다이빙 투어'),
    ('LẶN BIỂN', 'ダイビング', '다이빙'),
    ('Đà Nẵng, Hội An', 'ダナン、ホイアン', '다낭, 호이안'),
    ('Lặn biển ngắm san hô Cù Lao Chàm – Hội An 1 ngày', 'チャム島（クーラオチャム）サンゴ礁ダイビング・ホイアン 日帰り', '참섬(꾸라오짬) 산호초 다이빙 – 호이안 당일'),
    ('Lặn ngắm san hô bán đảo Sơn Trà – Đà Nẵng nửa ngày', 'ソンチャー半島サンゴ礁ダイビング・ダナン 半日', '선짜 반도 산호초 다이빙 – 다낭 반나절'),
    ('Lặn biển Hòn Mun – vịnh Nha Trang 3N2Đ', 'ニャチャン湾 ホンムン島ダイビング 3日間', '나트랑만 혼문섬 다이빙 2박 3일'),
    ('Khóa học lặn PADI Open Water tại Đà Nẵng 3 ngày', 'ダナンで取るPADIオープンウォーター講習 3日間', '다낭 PADI 오픈워터 다이빙 코스 3일'),
]

# Địa chỉ giữ nguyên tiếng Việt (không dịch lẻ từng địa danh bên trong)
for _addr in ['Quận Thanh Xuân, Hà Nội, Việt Nam']:
    _ROWS.append((_addr, _addr, _addr))

PLACE_NAMES = ['Cầu Vàng', 'Bà Nà Hills', 'Phố cổ Hội An', 'Cầu Rồng', 'Ngũ Hành Sơn', 'Biển Mỹ Khê', 'Bán đảo Sơn Trà']

TR = {vi: {'ja': ja, 'ko': ko} for vi, ja, ko in _ROWS}
for _n in PLACE_NAMES:
    TR['Xem ' + _n] = {'ja': TR[_n]['ja'] + 'を見る', 'ko': TR[_n]['ko'] + ' 보기'}

# Tên riêng / địa chỉ được giữ nguyên tiếng Việt (không báo là chưa dịch)
KEEP = ['Jean-Pierre Dalbéra', 'Khánh An', 'KHÁNH AN', 'Nguyễn Khả Tâm', 'Tòa nhà Tuấn Hạnh', 'Điện Biên Phủ', 'Bặch Đằng', 'Trần Huy Liệu']

_KEYS = sorted(TR, key=len, reverse=True)
# Chữ trong HTML đã được escape (&amp;...), nên khớp theo dạng đã escape
_HTML_KEY = {html.escape(k, quote=False): k for k in _KEYS}
_RE = re.compile(r'(?<!\w)(?:' + '|'.join(re.escape(k) for k in _HTML_KEY) + r')(?!\w)')
_VI = re.compile(r'[ăâđêôơưĂÂĐÊÔƠƯàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵÀÁẢÃẠÈÉẺẼẸÌÍỈĨỊÒÓỎÕỌÙÚỦŨỤỲÝỶỸỴ]')


def _tr_text(text, lang):
    return _RE.sub(lambda m: html.escape(TR[_HTML_KEY[m.group(0)]][lang], quote=False), text)


def _switch(lang, cls):
    active = ' class="active" aria-current="true"'
    items = ''.join(
        f'<li><a href="{c["file"]}" hreflang="{c["html_lang"]}" lang="{c["html_lang"]}"{active if k == lang else ""}>'
        f'<span class="lang-code">{c["flag"]}</span>{c["label"]}</a></li>'
        for k, c in LANGS.items())
    cur = LANGS[lang]
    if cls == 'top':
        return (f'<li class="has-dropdown lang-switch"><a href="#" aria-label="Language"><i class="fa-solid fa-globe" aria-hidden="true"></i>{cur["label"]}'
                f'<i class="icon-angle-down"></i></a><ul class="nav-dropdown">{items}</ul></li>')
    if cls == 'mobile':
        return f'<ul class="lang-pills" aria-label="Language">{items}</ul>'
    return f'<li class="html lang-sidebar"><ul class="lang-pills" aria-label="Language">{items}</ul></li>'


def render(page, lang):
    parts = re.split(r'(<script[\s\S]*?</script>|<[^>]+>)', page)
    out = []
    for p in parts:
        if not p:
            continue
        if p.startswith('<script'):
            out.append(p)
        elif p.startswith('<'):
            out.append(re.sub(r'\b(alt|title|aria-label|placeholder|value|content)="([^"]*)"',
                              lambda m: f'{m.group(1)}="{_tr_text(m.group(2), lang)}"', p))
        else:
            out.append(_tr_text(p, lang))
    page = ''.join(out)
    # Tiêu đề "TOUR <strong>X</strong>": đặt chữ "ツアー/투어" ra sau (ゴルフツアー, 골프 투어)
    word = TR['TOUR'][lang]
    sep = ' ' if lang == 'ko' else ''
    page = re.sub(rf'<h2 class="home-title">{word} <strong>([^<]+)</strong></h2>',
                  rf'<h2 class="home-title"><strong>\1</strong>{sep}{word}</h2>', page)
    page = page.replace('<html lang="vi">', f'<html lang="{LANGS[lang]["html_lang"]}">')
    alts = ''.join(f'<link rel="alternate" hreflang="{c["html_lang"]}" href="{c["file"]}">' for c in LANGS.values())
    page = page.replace('</head>', alts + '\n</head>', 1)
    page = (page.replace('<!--LANG_SWITCH-->', _switch(lang, 'top'))
                .replace('<!--LANG_SWITCH_MOBILE-->', _switch(lang, 'mobile'))
                .replace('<!--LANG_SWITCH_SIDEBAR-->', _switch(lang, 'sidebar')))
    return page


def leftovers(page):
    """Các đoạn chữ còn tiếng Việt (bỏ qua tên riêng/địa chỉ trong KEEP)."""
    found = []
    for t in re.findall(r'>([^<]+)<|\b(?:alt|title|aria-label|placeholder|value|content)="([^"]*)"', page):
        t = html.unescape(''.join(t)).strip()
        if not t:
            continue
        rest = t
        for k in KEEP:
            rest = rest.replace(k, '')
        if t.startswith(':') and ',' in t:  # địa chỉ ở footer
            continue
        if _VI.search(rest):
            found.append(t)
    return found
