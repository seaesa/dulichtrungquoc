"""Bản dịch trang chủ: tiếng Nhật (mặc định, index.html) và tiếng Hàn (ko.html).

build-html.py dựng trang bằng tiếng Việt rồi gọi render(page, lang). Hàm này dịch chữ trong
nội dung và trong các thuộc tính alt/title/aria-label/placeholder/value/content theo bảng TR
(khớp cụm dài nhất trước, chỉ thay một lượt). Khi thêm hoặc sửa chữ tiếng Việt ở trang,
nhớ thêm bản dịch vào TR; build sẽ báo những đoạn chưa dịch.
"""
import html
import re

import option_tours
import i18n_en

LANGS = {
    'ja': dict(file='index.html', html_lang='ja', label='日本語', flag='JP'),
    'ko': dict(file='ko.html', html_lang='ko', label='한국어', flag='KR'),
    'en': dict(file='en.html', html_lang='en', label='English', flag='EN'),
}
DEFAULT = 'ja'
KIDX = {'ja': 0, 'ko': 1, 'en': 2}  # vị trí bản dịch trong các cặp (ja, ko[, en])


def en_page(ja):
    """Bản tiếng Anh của nội dung trang con (pages.py), tra theo chữ tiếng Nhật."""
    if ja in i18n_en.PAGES_EN:
        return i18n_en.PAGES_EN[ja]
    hits = [p for p in i18n_en.PAGES_EN_PREFIX if ja.startswith(p)]
    if not hits:
        raise KeyError(f'Thiếu bản dịch tiếng Anh: {ja[:40]!r}')
    return i18n_en.PAGES_EN_PREFIX[max(hits, key=len)]


def page_url(lang, slug=None):
    """URL sạch (không .html). Tiếng Nhật: /slug/ ; tiếng Hàn: /ko/slug/ ; trang chủ: / và /ko/."""
    base = '/' if lang == DEFAULT else f'/{lang}/'
    return base + (f'{slug}/' if slug else '')


def page_file(lang, slug=None):
    """Đường dẫn file ghi ra đĩa: mỗi trang là một thư mục chứa index.html."""
    return page_url(lang, slug).lstrip('/') + 'index.html'


# (tiếng Việt, tiếng Nhật, tiếng Hàn)
_ROWS = [
    ('Khánh An Tourism - Trang chủ', 'Khánh An Tourism - ホーム', 'Khánh An Tourism - 홈'),
    ('Khánh An Tourism — tour trong nước, tour nước ngoài, visa, vé máy bay.',
     'Khánh An Tourism — ベトナム国内ツアー・海外ツアー・ビザ・航空券。',
     'Khánh An Tourism — 베트남 국내 투어, 해외 투어, 비자, 항공권.'),
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
    ('Thánh địa Mỹ Sơn', 'ミーソン聖地', '미선 성지'),
    ('Duy Xuyên', 'ズイスエン', '주이쑤옌'),
    ('Sáng sớm', '早朝', '이른 아침'),
    ('Quần thể đền tháp Chăm Pa từ thế kỷ IV – XIII, được UNESCO công nhận Di sản Văn hóa Thế giới năm 1999. Những tháp gạch đỏ nằm giữa thung lũng xanh là chứng tích của một nền văn minh rực rỡ.',
     '4〜13世紀に築かれたチャンパ王国の寺院群で、1999年にユネスコ世界文化遺産に登録されました。緑の谷間に立つ赤レンガの塔は、栄華を誇った文明の証です。',
     '4~13세기에 지어진 참파 왕국의 사원 유적군으로, 1999년 유네스코 세계문화유산으로 등재되었습니다. 푸른 계곡 속에 선 붉은 벽돌 탑은 찬란했던 문명의 증거입니다.'),
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
    ('NỔI BẬT', '注目', '인기'),
    ('NƯỚC NGOÀI', '海外', '해외'),
    ('TRONG NƯỚC', '国内', '국내'),
    ('COMBO GIÁ RẺ', 'お得なパック', '알뜰 패키지'),
    ('Khởi hành hàng tuần', '毎週出発', '매주 출발'),
    ('Mã tour:', 'ツアーコード:', '투어 코드:'),
    ('Khởi hành:', '出発地:', '출발지:'),
    ('/khách', '/名', '/인'),
    ('đã liên hệ', '件のお問い合わせ', '건 문의'),
    ('Đặt Tour', '予約する', '예약하기'),
    ('Du lịch Trung Quốc: Đảo Hải Nam – Tam Á – Hải Hoa Đảo 4N3Đ', '中国旅行：海南島・三亜・海花島 4日間', '중국 여행: 하이난섬 – 싼야 – 하이화섬 3박 4일'),
    ('Du Lịch Đài Loan: Đài Bắc – Đài Trung – Cao Hùng 5N4Đ', '台湾旅行：台北・台中・高雄 5日間', '대만 여행: 타이베이 – 타이중 – 가오슝 4박 5일'),
    ('Du Lịch Trung Quốc Giá Rẻ: Hà Khẩu – Bình Biên – Kiến Thủy – Mông Tự 3N2Đ',
     '格安中国旅行：河口・屏辺・建水・蒙自 3日間',
     '중국 알뜰 여행: 허커우 – 핑볜 – 젠수이 – 멍쯔 2박 3일'),
    ('Tour golf', 'ゴルフツアー', '골프 투어'),
    ('GOLF', 'ゴルフ', '골프'),
    ('Tour Golf Huế – Lăng Cô: Laguna Golf Lăng Cô & sân golf Huế 3N2Đ',
     'フエ・ランコー ゴルフツアー：ラグーナゴルフ・ランコー＆フエのゴルフ場 3日間',
     '후에 – 랑꼬 골프 투어: 라구나 골프 랑꼬 & 후에 골프장 2박 3일'),
    ('Golf Bà Nà Hills Golf Club & nghỉ dưỡng biển Đà Nẵng 2N1Đ', 'バーナーヒルズ・ゴルフクラブ＆ダナンのビーチリゾート 2日間', '바나힐 골프 클럽 & 다낭 해변 휴양 1박 2일'),
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
    ('KHÁCH HÀNG', 'お客様と', '고객과'),
    ('ĐỒNG HÀNH', '歩む旅', '함께한 여행'),
    ('Những khoảnh khắc của du khách trên hành trình cùng Khánh An Tourism', 'Khánh An Tourismと旅したお客様の素敵な瞬間', 'Khánh An Tourism과 함께한 여행객들의 소중한 순간'),
    ('VỀ CHÚNG TÔI', '声', '후기'),
    ('Đánh giá, cảm nhận của khách hàng đã sử dụng dịch vụ của chúng tôi',
     '当社をご利用いただいたお客様からのご感想',
     '저희 서비스를 이용하신 고객님들의 후기'),
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
    ('☎️ Hotline', '☎️ ホットライン', '☎️ 핫라인'),
    ('✉️ Email', '✉️ メール', '✉️ 이메일'),
    ('THÔNG TIN CẦN BIẾT', 'ご案内', '이용 안내'),
    ('Hình thức thanh toán', 'お支払い方法', '결제 방법'),
    ('Chính sách hoàn hủy', 'キャンセルポリシー', '취소·환불 정책'),
    ('Chính sách bảo mật', 'プライバシーポリシー', '개인정보 처리방침'),
    ('Điều khoản giao dịch', 'ご利用規約', '이용 약관'),
    ('ĐĂNG KÝ NHẬN BẢN TIN', 'ニュースレター登録', '뉴스레터 구독'),
    ('Nhập địa chỉ email để nhận thông tin mới nhất từ chúng tôi.', 'メールアドレスを入力して最新情報を受け取る。', '이메일을 입력하고 최신 소식을 받아 보세요.'),
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
    ('Đà Nẵng, Hội An', 'ダナン、ホイアン', '다낭, 호이안'),
    ('Lặn biển ngắm san hô Cù Lao Chàm – Hội An 1 ngày', 'チャム島（クーラオチャム）サンゴ礁ダイビング・ホイアン 日帰り', '참섬(꾸라오짬) 산호초 다이빙 – 호이안 당일'),
    ('Đà Nẵng, Huế', 'ダナン、フエ', '다낭, 후에'),
    ('Đà Nẵng, Tp Hồ Chí Minh', 'ダナン、ホーチミン', '다낭, 호찌민'),
    ('Du lịch Trung Quốc: Đà Nẵng – Thành Đô – Đô Giang Yến – Cửu Trại Câu –Mậu Huyện – Gia Cô Sơn 6N5Đ', '中国旅行：ダナン・成都・都江堰・九寨溝・茂県・甲居山 6日間', '중국 여행: 다낭 – 청두 – 두장옌 – 주자이거우 – 마오현 – 자쥐산 5박 6일'),
    ('Golf BRG Danang Golf Resort & nghỉ dưỡng biển Đà Nẵng 2N1Đ', 'BRGダナン・ゴルフリゾート＆ダナンのビーチリゾート 2日間', 'BRG 다낭 골프 리조트 & 다낭 해변 휴양 1박 2일'),
    ('Golf Montgomerie Links – sân golf ven biển Hội An 2N1Đ', 'モンゴメリー・リンクス（ホイアン海沿いのゴルフ場） 2日間', '몽고메리 링크스 – 호이안 해안 골프장 1박 2일'),
    ('Tour suối nước nóng', '温泉ツアー', '온천 투어'),
    ('SUỐI NƯỚC NÓNG', '温泉', '온천'),
    ('Tour lặn biển & núi rừng', 'ダイビング＆ジャングルツアー', '다이빙 & 정글 투어'),
    ('LẶN BIỂN & KHÁM PHÁ NÚI RỪNG', 'ダイビング＆ジャングル探検', '다이빙 & 정글 탐험'),
    ('Tắm khoáng nóng Núi Thần Tài – Đà Nẵng nửa ngày', 'タンタイ山ミネラル温泉・ダナン 半日', '턴타이산 미네랄 온천 – 다낭 반나절'),
    ('Tắm khoáng nóng Núi Thần Tài & phố cổ Hội An về đêm 1 ngày', 'タンタイ山ミネラル温泉＆夜のホイアン旧市街 日帰り', '턴타이산 미네랄 온천 & 야간 호이안 구시가지 당일'),
    ('Nghỉ dưỡng tắm khoáng nóng & Bà Nà Hills 2N1Đ', '温泉リゾート＆バーナーヒルズ 2日間', '온천 휴양 & 바나힐 1박 2일'),
    ('Cù Lao Chàm cano cao tốc: bãi Xếp – bãi Ông, lặn ngắm san hô 1 ngày', 'チャム島 スピードボートで巡るビーチ＆サンゴ礁ダイビング 日帰り', '참섬 스피드보트: 해변 투어 & 산호초 다이빙 당일'),
    ('Trekking rừng Bạch Mã – tắm suối, thác Đỗ Quyên 1 ngày', 'バックマー国立公園トレッキング・渓流水浴び・ドークエン滝 日帰り', '바익마 국립공원 트레킹 – 계곡 물놀이, 도꾸옌 폭포 당일'),
    ('Khám phá suối Mơ – rừng Bà Nà Hills 1 ngày', 'モー渓流とバーナーヒルズの森を探検 日帰り', '바나힐 숲과 모 계곡 탐험 당일'),
    ('Trekking rừng nguyên sinh bán đảo Sơn Trà 1 ngày', 'ソンチャー半島 原生林トレッキング 日帰り', '선짜 반도 원시림 트레킹 당일'),
    ('Lại một lần nữa công ty SANSHIN đồng hành cùng Khánh An Tourism trong chuyến du lịch Hội An. Mọi thứ đều tốt đẹp, hướng dẫn viên “anh Thành” luôn chu đáo từng bữa ăn, từng chỗ ngủ trong khách sạn, đoàn chúng tôi luôn an tâm khi đi cùng Khánh An Tourism trong mọi chuyến du lịch. Khánh An Tourism luôn trong suy nghĩ đầu tiên của chúng tôi trong mỗi lần có ý định đi du lịch. Cảm ơn Khánh An Tourism đã nhiệt tình hỗ trợ hết mình', '今回もSANSHINはKhánh An Tourismと一緒にホイアン旅行へ行きました。すべてが素晴らしく、ガイドの「タインさん」は毎回の食事からホテルの部屋まで細やかに気を配ってくれました。どの旅行でもKhánh An Tourismと一緒なら安心です。旅行を考えるとき、いつも真っ先に思い浮かぶのがKhánh An Tourismです。心のこもったサポートをありがとうございました。', '이번에도 SANSHIN은 Khánh An Tourism와 함께 호이안 여행을 다녀왔습니다. 모든 것이 훌륭했고, 가이드 “타잉 씨”는 매 식사와 호텔 객실까지 세심하게 챙겨 주었습니다. 어떤 여행이든 Khánh An Tourism와 함께라면 안심입니다. 여행을 계획할 때마다 가장 먼저 떠오르는 곳이 Khánh An Tourism입니다. 정성 어린 지원에 감사드립니다.'),
    ('Công ty TNHH SANSHIN', 'SANSHIN有限会社', 'SANSHIN 유한회사'),
    ('Tour Hội An lung linh', 'きらめくホイアンツアー', '반짝이는 호이안 투어'),
    ('Chúng tôi du lịch tới Bà Nà Hills xinh đẹp. Được đồng hành cùng công ty du lịch Khánh An Tourism. Chúng tôi thấy được quan tâm chăm sóc tận tình từng bữa ăn giấc ngủ khi đi du lịch. Hướng dẫn viên của công ty Khánh An Tourism chu đáo, tận tình. Trước ngày đi chúng tôi còn được công ty thông báo đến từng người giờ khởi hành và những thứ cần chuẩn bị. Công ty Khánh An Tourism sẽ là lựa chọn tin tưởng nhất cho những chuyến du lịch lần sau.', 'Khánh An Tourismと一緒に美しいバーナーヒルズへ旅行しました。旅行中は食事から睡眠まで心のこもったお世話をしていただきました。ガイドさんも親切で丁寧です。出発前には出発時刻や持ち物を一人ひとりに案内してくれました。次の旅行もKhánh An Tourismにお願いしたいと思います。', 'Khánh An Tourism와 함께 아름다운 바나힐을 여행했습니다. 여행 내내 식사부터 숙박까지 세심한 보살핌을 받았고, 가이드도 친절하고 꼼꼼했습니다. 출발 전에는 출발 시간과 준비물을 한 사람씩 안내해 주었습니다. 다음 여행도 Khánh An Tourism에 맡기고 싶습니다.'),
    ('Cảm nhận về tour Bà Nà Hills do công ty tổ chức', '当社主催バーナーヒルズツアーのご感想', '당사 바나힐 투어 이용 후기'),
]

# Bài viết / tin tức miền Trung
_ROWS += [
    ('Kinh nghiệm và thông tin du lịch Đà Nẵng, Hội An, Huế dành cho du khách Nhật Bản và Hàn Quốc',
     'ダナン・ホイアン・フエを旅する日本・韓国のお客様向けの旅行情報とヒントをお届けします。',
     '다낭·호이안·후에를 여행하는 일본·한국 고객을 위한 여행 정보와 팁을 전해 드립니다.'),
    ('Cầu Vàng Bà Nà Hills: kinh nghiệm đi cáp treo và giờ đẹp để ngắm cảnh',
     'バーナーヒルズのゴールデンブリッジ：ケーブルカーの乗り方と景色が美しい時間帯',
     '바나힐 골든 브리지: 케이블카 이용 팁과 풍경이 가장 아름다운 시간대'),
    ('Hội An về đêm: thả đèn hoa đăng và những món ăn nên thử',
     '夜のホイアン：灯篭流しと食べておきたい名物料理',
     '야경의 호이안: 등불 띄우기와 꼭 먹어봐야 할 명물 요리'),
    ('Thánh địa Mỹ Sơn: vì sao nên đi vào buổi sáng',
     'ミーソン遺跡：午前中の訪問がおすすめな理由',
     '미선 유적: 오전 방문을 추천하는 이유'),
    ('Khám phá lăng Khải Định, lăng Tự Đức và Đại Nội trong một ngày ở Huế',
     'フエ1日観光：カイディン帝廟・トゥドゥック帝廟・グエン朝王宮を巡る',
     '후에 하루 여행: 카이딘 황릉·뜨득 황릉·응우옌 왕궁 둘러보기'),
    ('Cầu Rồng phun lửa và du thuyền sông Hàn: lịch trình buổi tối ở Đà Nẵng',
     'ドラゴン橋の火のショーとハン川クルーズ：ダナンの夜の過ごし方',
     '용다리 불쇼와 한강 크루즈: 다낭의 저녁 일정'),
    ('Ngũ Hành Sơn, biển Mỹ Khê và chùa Linh Ứng: nửa ngày tham quan Đà Nẵng',
     '五行山・ミーケービーチ・リンウン寺：ダナン半日観光モデルコース',
     '오행산·미케 비치·린응사: 다낭 반나절 관광 코스'),
]

_ROWS += [
    ('Golf Đà Nẵng: Bà Nà Hills, Montgomerie Links và những sân golf nên chơi',
     'ダナンのゴルフ：バーナーヒルズ、モンゴメリーリンクスなどおすすめコース',
     '다낭 골프: 바나힐, 몽고메리 링크스 등 추천 골프장'),
    ('Núi Thần Tài: tắm khoáng nóng, tắm bùn và kinh nghiệm đi trong ngày',
     'ヌイタンタイ：温泉・泥風呂と日帰りで楽しむコツ',
     '누이턴따이: 온천·머드 목욕과 당일 여행 팁'),
    ('VinWonders Nam Hội An: giá vé, giờ mở cửa và kinh nghiệm vui chơi',
     'ヴィンワンダーズ・ナムホイアン：チケット料金・営業時間・遊び方のコツ',
     '빈원더스 남호이안: 입장권 요금·운영 시간·이용 팁'),
]

_ROWS += option_tours.ROWS

# Địa chỉ giữ nguyên tiếng Việt (không dịch lẻ từng địa danh bên trong)
for _addr in ['108, Phạm Xuân Ẩn, Cẩm Lệ, Đà Nẵng']:
    _ROWS.append((_addr, _addr, _addr))

PLACE_NAMES = ['Cầu Vàng', 'Bà Nà Hills', 'Phố cổ Hội An', 'Cầu Rồng', 'Ngũ Hành Sơn', 'Biển Mỹ Khê', 'Bán đảo Sơn Trà']

def _en(vi):
    if vi in i18n_en.EN:
        return i18n_en.EN[vi]
    hits = [p for p in i18n_en.EN_PREFIX if vi.startswith(p)]
    if not hits:
        raise KeyError(f'Thiếu bản dịch tiếng Anh: {vi[:70]!r}')
    return i18n_en.EN_PREFIX[max(hits, key=len)]


TR = {vi: {'ja': ja, 'ko': ko, 'en': _en(vi)} for vi, ja, ko in _ROWS}
for _n in PLACE_NAMES:
    TR['Xem ' + _n] = {'ja': TR[_n]['ja'] + 'を見る', 'ko': TR[_n]['ko'] + ' 보기', 'en': 'View ' + TR[_n]['en']}

# Tên riêng / địa chỉ được giữ nguyên tiếng Việt (không báo là chưa dịch)
KEEP = ['108, Phạm Xuân Ẩn, Cẩm Lệ, Đà Nẵng', 'Jean-Pierre Dalbéra', 'Khánh An', 'KHÁNH AN', 'Nguyễn Khả Tâm', 'Phạm Xuân Ẩn', 'Trần Thanh Minh Khuê']

_KEYS = sorted(TR, key=len, reverse=True)
# Chữ trong HTML đã được escape (&amp;...), nên khớp theo dạng đã escape
_HTML_KEY = {html.escape(k, quote=False): k for k in _KEYS}
_RE = re.compile(r'(?<!\w)(?:' + '|'.join(re.escape(k) for k in _HTML_KEY) + r')(?!\w)')
_VI = re.compile(r'[ăâđêôơưĂÂĐÊÔƠƯàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵÀÁẢÃẠÈÉẺẼẸÌÍỈĨỊÒÓỎÕỌÙÚỦŨỤỲÝỶỸỴ]')


def _tr_text(text, lang):
    return _RE.sub(lambda m: html.escape(TR[_HTML_KEY[m.group(0)]][lang], quote=False), text)


def _switch(lang, cls, slug=None):
    active = ' class="active" aria-current="true"'
    items = ''.join(
        f'<li><a href="{page_url(k, slug)}" hreflang="{c["html_lang"]}" lang="{c["html_lang"]}"{active if k == lang else ""}>'
        f'<span class="lang-code">{c["flag"]}</span>{c["label"]}</a></li>'
        for k, c in LANGS.items())
    cur = LANGS[lang]
    if cls == 'top':
        return (f'<li class="has-dropdown lang-switch"><a href="#" aria-label="Language"><i class="fa-solid fa-globe" aria-hidden="true"></i>{cur["label"]}'
                f'<i class="icon-angle-down"></i></a><ul class="nav-dropdown">{items}</ul></li>')
    if cls == 'mobile':
        return f'<ul class="lang-pills" aria-label="Language">{items}</ul>'
    return f'<li class="html lang-sidebar"><ul class="lang-pills" aria-label="Language">{items}</ul></li>'


def render(page, lang, slug=None):
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
    sep = ' ' if lang in ('ko', 'en') else ''
    page = re.sub(rf'<h2 class="home-title">{word} <strong>([^<]+)</strong></h2>',
                  rf'<h2 class="home-title"><strong>\1</strong>{sep}{word}</h2>', page)
    if lang == 'en':
        page = page.replace('〜', '+')
    page = page.replace('<html lang="vi">', f'<html lang="{LANGS[lang]["html_lang"]}">')
    alts = ''.join(f'<link rel="alternate" hreflang="{c["html_lang"]}" href="{page_url(k, slug)}">' for k, c in LANGS.items())
    page = page.replace('</head>', alts + '\n</head>', 1)
    page = (page.replace('<!--LANG_SWITCH-->', _switch(lang, 'top', slug))
                .replace('<!--LANG_SWITCH_MOBILE-->', _switch(lang, 'mobile', slug))
                .replace('<!--LANG_SWITCH_SIDEBAR-->', _switch(lang, 'sidebar', slug)))
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
