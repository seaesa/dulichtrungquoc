"""Bản dịch trang chủ: tiếng Nhật (mặc định, index.html) và tiếng Trung giản thể (zh.html).

build-html.py dựng trang bằng tiếng Việt rồi gọi render(page, lang). Hàm này dịch chữ trong
nội dung và trong các thuộc tính alt/title/aria-label/placeholder/value/content theo bảng TR
(khớp cụm dài nhất trước, chỉ thay một lượt). Khi thêm hoặc sửa chữ tiếng Việt ở trang,
nhớ thêm bản dịch vào TR; build sẽ báo những đoạn chưa dịch.
"""
import html
import re

LANGS = {
    'ja': dict(file='index.html', html_lang='ja', label='日本語', flag='JP'),
    'zh': dict(file='zh.html', html_lang='zh-CN', label='中文', flag='CN'),
}
DEFAULT = 'ja'

# (tiếng Việt, tiếng Nhật, tiếng Trung)
_ROWS = [
    # --- chung / header
    ('Khánh An Tourist - Trang chủ', 'Khánh An Tourist - ホーム', 'Khánh An Tourist - 首页'),
    ('Khánh An Tourist — tour trong nước, tour nước ngoài, visa, vé máy bay.',
     'Khánh An Tourist — ベトナム国内ツアー・海外ツアー・ビザ・航空券。',
     'Khánh An Tourist — 越南国内游、出境游、签证、机票。'),
    ('Skip to content', '本文へスキップ', '跳到正文'),
    ('Tuyển dụng', '採用情報', '招聘'),
    ('Hướng dẫn thanh toán', 'お支払い方法', '付款指南'),
    ('Liên hệ', 'お問い合わせ', '联系我们'),
    ('Giỏ hàng', 'カート', '购物车'),
    ('Chưa có sản phẩm trong giỏ hàng.', 'カートに商品はありません。', '购物车中还没有商品。'),
    ('Trang chủ', 'ホーム', '首页'),
    ('Giới thiệu', '会社案内', '关于我们'),
    ('Tour du lịch', 'ツアー', '旅游线路'),
    ('Tour nước ngoài', '海外ツアー', '出境游'),
    ('Tour trong nước', 'ベトナム国内ツアー', '越南国内游'),
    ('Cẩm nang du lịch Tin tức', '旅行ガイド・ニュース', '旅游攻略 · 新闻'),
    ('Cẩm nang du lịch', '旅行ガイド', '旅游攻略'),
    ('Visa du lịch', '観光ビザ', '旅游签证'),
    ('Tin tức', 'ニュース', '新闻'),
    ('Tìm kiếm:', '検索:', '搜索：'),
    ('Tìm kiếm', '検索', '搜索'),
    ('Nhập từ khóa cần tìm', 'キーワードを入力', '请输入关键词'),

    # --- banner Đà Nẵng
    ('Khám phá Đà Nẵng', 'ダナンを探索', '探索岘港'),
    ('Biểu tượng', 'シンボル', '地标'),
    ('Xem tour Đà Nẵng', 'ダナンツアーを見る', '查看岘港线路'),
    ('Đà Nẵng', 'ダナン', '岘港'),
    ('Cầu Vàng', 'ゴールデンブリッジ', '金桥'),
    ('Sun World Bà Nà Hills', 'サンワールド・バーナーヒルズ', '太阳世界巴拿山'),
    ('Bà Nà Hills', 'バーナーヒルズ', '巴拿山'),
    ('Núi Chúa', 'チュア山', '主山'),
    ('Phố cổ Hội An', 'ホイアン旧市街', '会安古镇'),
    ('Hội An', 'ホイアン', '会安'),
    ('Cầu Rồng', 'ドラゴン橋', '龙桥'),
    ('Sông Hàn', 'ハン川', '汉江'),
    ('Ngũ Hành Sơn', '五行山', '五行山'),
    ('Non Nước', 'ノンヌォック', '仁水'),
    ('Biển Mỹ Khê', 'ミーケービーチ', '美溪海滩'),
    ('Bán đảo Sơn Trà', 'ソンチャー半島', '山茶半岛'),
    ('Sơn Trà', 'ソンチャー', '山茶'),
    ('Chùa Linh Ứng', 'リンウン寺', '灵应寺'),
    ('Ảnh:', '写真:', '图片：'),
    ('Cây cầu dát vàng dài khoảng 150 m uốn lượn giữa mây trời ở độ cao gần 1.400 m, được nâng đỡ bởi đôi bàn tay đá khổng lồ. Từ khi khánh thành năm 2018, Cầu Vàng trở thành biểu tượng du lịch mới của Đà Nẵng.',
     '標高約1,400mの雲の上をうねる全長約150mの金色の橋。巨大な石の両手に支えられています。2018年の開通以来、ダナン観光の新たなシンボルとなりました。',
     '这座长约150米的金色桥梁蜿蜒于海拔近1400米的云海之间，由一双巨大的石手托起。自2018年开通以来，金桥已成为岘港旅游的新地标。'),
    ('Khu du lịch trên đỉnh núi Chúa cao 1.487 m, khí hậu mát mẻ quanh năm với trải nghiệm “4 mùa trong 1 ngày”. Hệ thống cáp treo đưa du khách tới Làng Pháp, vườn hoa Le Jardin d’Amour và khu vui chơi Fantasy Park.',
     '標高1,487mのチュア山頂にあるリゾート。一年中涼しく「1日で四季」を体験できます。ロープウェイでフレンチビレッジ、ル・ジャルダン・ダムール庭園、ファンタジーパークへ。',
     '位于海拔1487米主山山顶的度假区，全年气候凉爽，可体验“一日四季”。乘坐缆车即可抵达法国村、爱情花园和梦幻乐园。'),
    ('Thương cảng sầm uất từ thế kỷ XVI – XVII, được UNESCO công nhận Di sản Văn hóa Thế giới năm 1999. Những dãy nhà tường vàng, Chùa Cầu và đèn lồng lung linh mỗi tối tạo nên vẻ đẹp hoài cổ khó quên.',
     '16〜17世紀に栄えた交易港で、1999年にユネスコ世界文化遺産に登録。黄色い壁の家並み、日本橋（来遠橋）、夜を彩るランタンが忘れがたいノスタルジックな風景をつくります。',
     '16至17世纪繁华的贸易港口，1999年被联合国教科文组织列为世界文化遗产。黄墙老屋、日本桥（来远桥）和每晚闪烁的灯笼，构成令人难忘的怀旧风情。'),
    ('Cây cầu hình rồng vàng vươn mình trên sông Hàn, dài 666 m, khánh thành năm 2013. Vào 21h tối thứ Bảy và Chủ nhật, đầu rồng phun lửa, phun nước – màn trình diễn không thể bỏ lỡ.',
     'ハン川に架かる全長666mの金色の龍の橋（2013年開通）。毎週土・日曜21時には龍の頭から火と水が噴き出す、見逃せないショーが行われます。',
     '横跨汉江的金色巨龙大桥，全长666米，2013年通车。每周六、周日晚上9点，龙头喷火喷水，表演不容错过。'),
    ('Quần thể 5 ngọn núi đá vôi Kim, Mộc, Thủy, Hỏa, Thổ nằm cạnh biển, ẩn chứa nhiều hang động và chùa cổ như động Huyền Không, chùa Tam Thai. Dưới chân núi là làng đá mỹ nghệ Non Nước lâu đời.',
     '海辺に並ぶ金・木・水・火・土の5つの石灰岩の山々。フエンコン洞窟やタムタイ寺など多くの洞窟と古刹が点在し、麓には歴史あるノンヌォック石彫り村があります。',
     '金、木、水、火、土五座石灰岩山临海而立，藏有玄空洞、三台寺等众多洞穴与古寺。山脚下是历史悠久的仁水石雕村。'),
    ('Bãi biển cát trắng mịn, nước trong xanh và sóng êm, từng được tạp chí Forbes bình chọn là một trong những bãi biển quyến rũ nhất hành tinh. Lý tưởng để tắm biển, chèo SUP và ngắm bình minh.',
     '白く細かな砂、透き通った海と穏やかな波。フォーブス誌で「世界で最も魅力的なビーチ」の一つに選ばれました。海水浴やSUP、朝日鑑賞に最適です。',
     '细白的沙滩、清澈的海水和平缓的海浪，曾被《福布斯》评为全球最迷人的海滩之一。非常适合游泳、桨板和观赏日出。'),
    ('“Lá phổi xanh” của Đà Nẵng với rừng nguyên sinh và loài voọc chà vá chân nâu quý hiếm. Chùa Linh Ứng trên bán đảo có tượng Phật Bà Quan Âm cao 67 m hướng ra biển Đông.',
     '原生林と希少なアカアシドゥクラングールが暮らす、ダナンの「緑の肺」。半島のリンウン寺には海を見守る高さ67mの観音像が立っています。',
     '岘港的“绿肺”，拥有原始森林和珍稀的红腿白臀叶猴。半岛上的灵应寺矗立着一尊面朝大海、高67米的观音像。'),
    ('Vị trí', '場所', '位置'),
    ('Khoảng cách', '距離', '距离'),
    ('Thời điểm đẹp', 'ベストシーズン', '最佳时间'),
    ('Sáng sớm, tháng 3 – 8', '早朝・3〜8月', '清晨，3–8月'),
    ('Sáng sớm, hoàng hôn', '早朝・夕暮れ', '清晨、黄昏'),
    ('Độ cao', '標高', '海拔'),
    ('Nhiệt độ', '気温', '气温'),
    ('Di sản', '世界遺産', '遗产'),
    ('Nên đi', 'おすすめ', '推荐时段'),
    ('Chiều tối, đêm rằm', '夕方・満月の夜', '傍晚、月圆之夜'),
    ('Chiều dài', '全長', '长度'),
    ('Phun lửa', '火のショー', '喷火表演'),
    ('21:00 T7 & CN', '土・日 21:00', '周六、日 21:00'),
    ('Trung tâm thành phố', '市内中心部', '市中心'),
    ('Nổi bật', '見どころ', '亮点'),
    ('Động Huyền Không', 'フエンコン洞窟', '玄空洞'),
    ('Tham quan', '所要時間', '游览时长'),
    ('2 – 3 giờ', '2〜3時間', '2–3小时'),
    ('Mùa tắm biển', '海水浴シーズン', '游泳季节'),
    ('Tháng 4 – 8', '4〜8月', '4–8月'),
    ('Đặc sản', '名物', '特产'),
    ('Hải sản tươi sống', '新鮮な海鮮', '生猛海鲜'),
    ('Tượng Quan Âm', '観音像', '观音像'),
    ('Cao 67 m', '高さ67m', '高67米'),

    # --- bạn muốn đi đâu
    ('BẠN MUỐN', 'どこへ', '您想'),
    ('ĐI ĐÂU', '行きたい？', '去哪里'),
    ('Đã có lượt khách', '多数のお客様にご利用', '已有众多游客'),
    ('Đài Loan', '台湾', '台湾'),
    ('Nhật Bản', '日本', '日本'),
    ('Hàn Quốc', '韓国', '韩国'),
    ('Thái Lan', 'タイ', '泰国'),
    ('Trung Quốc', '中国', '中国'),
    ('Miền Tây Sông Nước', 'メコンデルタ', '湄公河三角洲'),
    ('Miền Bắc hùng vỹ', '雄大な北部', '壮美北越'),
    ('Đà Lạt – Tây Nguyên', 'ダラット・中部高原', '大叻 – 西原'),
    ('Phú Quốc mộng mơ', '夢のフーコック島', '梦幻富国岛'),
    ('Biển trời Miền Trung', '中部の海と空', '中部海天'),

    # --- thẻ tour
    ('TOUR', 'ツアー', '线路'),
    ('NỔI BẬT', '注目', '精选'),
    ('NƯỚC NGOÀI', '海外', '出境'),
    ('TRONG NƯỚC', '国内', '国内'),
    ('COMBO GIÁ RẺ', 'お得なパック', '超值套餐'),
    ('Khởi hành hàng tuần', '毎週出発', '每周出发'),
    ('Mã tour:', 'ツアーコード:', '线路编号：'),
    ('Khởi hành:', '出発地:', '出发地：'),
    ('/khách', '/名', '/人'),
    ('đã liên hệ', '件のお問い合わせ', '人已咨询'),
    ('Đặt Tour', '予約する', '立即预订'),
    ('Đà Nẵng, Hà Nội, Tp Hồ Chí Minh', 'ダナン、ハノイ、ホーチミン', '岘港、河内、胡志明市'),
    ('Đà Nẵng, Hà Nội', 'ダナン、ハノイ', '岘港、河内'),
    ('Hà Nội', 'ハノイ', '河内'),
    ('Du lịch Trung Quốc: Đảo Hải Nam – Tam Á – Hải Hoa Đảo 4N3Đ',
     '中国旅行：海南島・三亜・海花島 4日間', '中国游：海南岛 – 三亚 – 海花岛 4天3晚'),
    ('Du lịch Trung Quốc: Hà Nội – Thành Đô – Đô Giang Yến – Cửu Trại Câu –Mậu Huyện – Gia Cô Sơn 6N5Đ',
     '中国旅行：ハノイ・成都・都江堰・九寨溝・茂県・甲居山 6日間', '中国游：河内 – 成都 – 都江堰 – 九寨沟 – 茂县 – 甲居山 6天5晚'),
    ('Tour Du Lịch Hà Giang – Sông Nho Quế – Cao Nguyên Đá Đồng Văn 3N2Đ',
     'ハザン・ニョークエ川・ドンバン石灰岩高原ツアー 3日間', '河江 – 娥桂江 – 同文石高原之旅 3天2晚'),
    ('Du Lịch Tây Bắc: Mù Cang Chải – Đèo Khau Phạ – Tú Lệ – Trạm Tấu 3N2Đ',
     '西北部の旅：ムーカンチャイ・カウファー峠・トゥレ・チャムタウ 3日間', '西北游：木江界 – 考法山口 – 秀丽 – 站秀 3天2晚'),
    ('Du Lịch Mộc Châu – Mai Châu – Cầu Kính Bạch Long 2N1Đ',
     'モックチャウ・マイチャウ・バクロンガラス橋 2日間', '木州 – 梅州 – 白龙玻璃桥 2天1晚'),
    ('Du Lịch Đài Loan: Đài Bắc – Đài Trung – Cao Hùng 5N4Đ',
     '台湾旅行：台北・台中・高雄 5日間', '台湾游：台北 – 台中 – 高雄 5天4晚'),
    ('Du Lịch Trung Quốc Giá Rẻ: Hà Khẩu – Bình Biên – Kiến Thủy – Mông Tự 3N2Đ',
     '格安中国旅行：河口・屏辺・建水・蒙自 3日間', '中国特价游：河口 – 屏边 – 建水 – 蒙自 3天2晚'),

    # --- tour golf & du thuyền
    ('Tour golf', 'ゴルフツアー', '高尔夫线路'),
    ('Tour du thuyền', 'クルーズツアー', '游轮线路'),
    ('GOLF', 'ゴルフ', '高尔夫'),
    ('DU THUYỀN', 'クルーズ', '游轮'),
    ('Hà Nội, Đà Nẵng', 'ハノイ、ダナン', '河内、岘港'),
    ('Đà Nẵng', 'ダナン', '岘港'),
    ('Tour Golf Đà Nẵng – Hội An: BRG Danang Golf – Montgomerie Links – Hoiana Shores 4N3Đ',
     'ダナン・ホイアン ゴルフツアー：BRGダナンゴルフ・モンゴメリーリンクス・ホイアナショアーズ 4日間',
     '岘港 – 会安高尔夫之旅：BRG岘港高尔夫 – 蒙哥马利林克斯 – 会安娜海岸 4天3晚'),
    ('Tour Golf Huế – Lăng Cô: Laguna Golf Lăng Cô & sân golf Huế 3N2Đ',
     'フエ・ランコー ゴルフツアー：ラグーナゴルフ・ランコー＆フエのゴルフ場 3日間',
     '顺化 – 朗姑高尔夫之旅：朗姑拉古娜高尔夫 & 顺化球场 3天2晚'),
    ('Golf Bà Nà Hills Golf Club & nghỉ dưỡng biển Đà Nẵng 2N1Đ',
     'バーナーヒルズ・ゴルフクラブ＆ダナンのビーチリゾート 2日間',
     '巴拿山高尔夫俱乐部 & 岘港海滨度假 2天1晚'),
    ('Tour Golf Hà Nội – Tam Đảo Golf Resort – Sky Lake 3N2Đ',
     'ハノイ ゴルフツアー：タムダオ・ゴルフリゾート・スカイレイク 3日間',
     '河内高尔夫之旅：三岛高尔夫度假村 – 天湖 3天2晚'),
    ('Du thuyền 5 sao vịnh Hạ Long 2N1Đ', 'ハロン湾 5つ星クルーズ 2日間', '下龙湾五星游轮 2天1晚'),
    ('Du thuyền vịnh Lan Hạ – Cát Bà 3N2Đ', 'ランハー湾・カットバ島クルーズ 3日間', '兰下湾 – 吉婆岛游轮 3天2晚'),
    ('Du thuyền trong ngày vịnh Hạ Long – hang Sửng Sốt – đảo Ti Tốp',
     'ハロン湾日帰りクルーズ：スンソット洞窟・ティートップ島', '下龙湾一日游轮：惊讶洞 – 天堂岛'),
    ('Du thuyền buồm truyền thống ngắm hoàng hôn vịnh Hạ Long 2N1Đ',
     '伝統的な帆船で楽しむハロン湾サンセットクルーズ 2日間', '传统帆船游下龙湾赏日落 2天1晚'),

    # --- vì sao chọn / dịch vụ
    ('VÌ SAO CHỌN', '選ばれる', '为什么选择'),
    ('CHÚNG TÔI', '理由', '我们'),
    ('Dịch vụ Tour nội địa và quốc tế', '国内・海外ツアーサービス', '国内及国际旅游服务'),
    ('Công ty lữ hành tại Việt Nam', 'ベトナムの旅行会社', '越南旅行社'),
    ('các đơn vị làm VISA nước ngoài', '海外ビザ代行会社', '海外签证代办机构'),
    ('ĐẶT TOUR', 'かんたん予約', '轻松预订'),
    ('Dễ dàng nhanh chóng chỉ 3 bước', 'わずか3ステップで簡単・スピーディー', '只需3步，简单快捷'),
    ('THANH TOÁN', 'お支払い', '付款'),
    ('Đơn giản, an toàn và linh hoạt', 'シンプル・安全・柔軟', '简单、安全、灵活'),
    ('Trực tuyến 24/7', '24時間対応', '24小时在线'),
    ('CÁC DỊCH VỤ', '私たちの', '我们的'),
    ('CỦA CHÚNG TÔI', 'サービス', '服务'),
    ('Hội chợ quốc tế', '国際見本市', '国际展会'),
    ('Chuyên tour hội chợ quốc tế các nước trên thế giới', '世界各国の国際見本市ツアーを専門に手配', '专营全球各国国际展会线路'),
    ('Sim quốc tế', '海外SIM', '国际SIM卡'),
    ('Bán sim nghe gọi & data các nước trên thế giới', '世界各国の通話・データSIMを販売', '销售全球各国通话及流量SIM卡'),
    ('Dịch vụ Visa nhanh, rẻ. Visa trọn gói, thủ tục đơn giản', 'スピーディーで格安なビザ申請代行。手続きもまるごとお任せ', '签证快速实惠，全包服务，手续简便'),
    ('Vé máy bay', '航空券', '机票'),
    ('Vé máy bay giá rẻ nhất, nhiều khuyến mãi hấp dẫn', '最安値の航空券とお得なキャンペーン多数', '超低价机票，优惠多多'),
    ('VISA', 'ビザ', '签证'),

    # --- khoảnh khắc / khách hàng
    ('KHOẢNH KHẮC', 'ベスト', '最美'),
    ('ĐẸP NHẤT', 'ショット', '瞬间'),
    ('KHÁCH HÀNG NÓI GÌ', 'お客様の', '客户'),
    ('VỀ CHÚNG TÔI', '声', '评价'),
    ('Đánh giá, cảm nhận của khách hàng đã sử dụng dịch vụ của chúng tôi', '当社をご利用いただいたお客様からのご感想', '使用过我们服务的客户的评价与感受'),
    ('Lại một lần nữa công ty SANSHIN đồng hành cùng Khánh An Tourist trong chuyến du lịch Hạ Long. Mọi thứ đều tốt đẹp, hướng dẫn viên “anh Thành” luôn chu đáo từng bữa ăn, từng chỗ ngủ trong khách sạn, đoàn chúng tôi luôn an tâm khi đi cùng Khánh An Tourist trong mọi chuyến du lịch trong và ngoài nước. Khánh An Tourist luôn trong suy nghĩ đầu tiên của chúng tôi trong mỗi lần có ý định đi du lịch. Cảm ơn Khánh An Tourist đã nhiệt tình hỗ trợ hết mình',
     '今回もSANSHINはKhánh An Touristと一緒にハロン湾旅行へ行きました。すべてが素晴らしく、ガイドの「タインさん」は毎回の食事からホテルの部屋まで細やかに気を配ってくれました。国内外どの旅行でもKhánh An Touristと一緒なら安心です。旅行を考えるとき、いつも真っ先に思い浮かぶのがKhánh An Touristです。心のこもったサポートをありがとうございました。',
     'SANSHIN公司再次与Khánh An Tourist一起踏上下龙湾之旅。一切都非常完美，导游“阿成”对每一餐、每一间酒店客房都照顾得无微不至。无论国内还是出境游，和Khánh An Tourist同行我们都很放心。每次计划旅行，我们首先想到的就是Khánh An Tourist。感谢Khánh An Tourist的热情支持！'),
    ('Công ty TNHH SANSHIN Hà Nội', 'SANSHIN ハノイ有限会社', 'SANSHIN河内有限公司'),
    ('Tour Hạ Long náo nhiệt', 'にぎやかなハロン湾ツアー', '热闹的下龙湾之旅'),
    ('Chúng tôi du lịch tới đảo Phú Quốc xinh đẹp. Được đồng hành cùng công ty du lịch Khánh An Tourist. Chúng tôi thấy được quan tâm chăm sóc tận tình từng bữa ăn giấc ngủ khi đi du lịch. Hướng dẫn viên của công ty Khánh An Tourist chu đáo, tận tình. Trước ngày đi chúng tôi còn được công ty thông báo đến từng người giờ khởi hành và những thứ cần chuẩn bị. Công ty Khánh An Tourist sẽ là lựa chọn tin tưởng nhất cho những chuyến du lịch lần sau.',
     'Khánh An Touristと一緒に美しいフーコック島へ旅行しました。旅行中は食事から睡眠まで心のこもったお世話をしていただきました。ガイドさんも親切で丁寧です。出発前には出発時刻や持ち物を一人ひとりに案内してくれました。次の旅行もKhánh An Touristにお願いしたいと思います。',
     '我们和Khánh An Tourist一起去了美丽的富国岛。旅途中从饮食到住宿都受到了细致周到的照顾，导游热情又贴心。出发前，公司还逐一通知每个人出发时间和需要准备的物品。下次旅行，Khánh An Tourist仍是我们最信赖的选择。'),
    ('Cảm nhận về tour Phú Quốc do công ty tổ chức', '当社主催フーコック島ツアーのご感想', '对本公司富国岛线路的评价'),

    # --- LINE
    ('Tài khoản chính thức', '公式アカウント', '官方账号'),
    ('Kết bạn', '友だち追加', '加为好友'),
    ('Ưu đãi cho bạn bè LINE', 'LINE友だち限定クーポン', 'LINE好友专享优惠'),
    ('Giảm % cho khách hàng kết bạn LINE chính thức của CHÚNG TÔI', 'LINE公式アカウントの友だち追加で割引！', '添加我们的LINE官方账号即享折扣！'),
    ('Đặt tour dễ dàng trên Website & LINE', 'ウェブサイト＆LINEでかんたんツアー予約', '通过网站和LINE轻松预订线路'),
    ('Để lại mail chúng tôi sẽ gửi chương trình chi tiết tới bạn.', 'メールアドレスをご登録いただくと、キャンペーンの詳細をお送りします。', '留下邮箱，我们将把活动详情发送给您。'),
    ('Quét mã QR để được tư vấn nhanh nhất', 'QRコードを読み取って今すぐ相談', '扫描二维码，快速咨询'),
    ('Mã QR LINE', 'LINE QRコード', 'LINE二维码'),

    # --- tin tức
    ('TIN TỨC', '旅行', '旅游'),
    ('DU LỊCH', 'ニュース', '资讯'),
    ('Chia sẽ những thông tin du lịch triển lãm nhanh nhất & những bí quyết khi tham gia tour hội chợ', '展示会旅行の最新情報と見本市ツアー参加のコツをお届けします', '分享最新的展会旅游资讯及参加展会线路的小窍门'),
    ('TOP 5 điểm vui chơi nghỉ dưỡng tuyệt vời tại Phú Quốc giới trẻ không thể bỏ lỡ', '若者必見！フーコック島の最高のリゾート＆遊びスポット TOP5', '年轻人不可错过的富国岛五大玩乐度假胜地'),
    ('Những địa điểm du lịch Trung Quốc không cần hộ chiếu', 'パスポート不要で行ける中国の観光地', '无需护照即可前往的中国旅游景点'),
    ('Chỉ Với Giấy Thông Hành, Đi Đâu Du Lịch Trung Quốc?', '通行証だけで行ける中国旅行先は？', '只凭通行证，能去中国哪里旅游？'),
    ('Địa điểm vui chơi trung thu tiết kiệm nhất từ Bắc vào Nam', '北から南まで、お得に楽しめる中秋節スポット', '从北到南最省钱的中秋游玩地点'),
    ('Trải nghiệm một ngày tại quận nghèo nhất hồng kông- thâm thủy bộ', '香港で最も庶民的な街・深水埗で過ごす一日', '在香港最贫困的地区——深水埗体验一天'),
    ('Du Lịch Hàn Quốc: Khám Phá Khu Rừng Lá Đỏ Đầy Mê Hoặc Hwadam', '韓国旅行：魅惑の紅葉の森・花潭（ファダム）を探訪', '韩国游：探索迷人的红叶森林花潭'),

    # --- footer
    ('📍 Địa chỉ', '📍 住所', '📍 地址'),
    ('🏠 Chi nhánh Hoà Bình', '🏠 ホアビン支店', '🏠 和平分公司'),
    ('🏠 Chi nhánh Hải Phòng', '🏠 ハイフォン支店', '🏠 海防分公司'),
    ('🏠 Chi nhánh Nam Định', '🏠 ナムディン支店', '🏠 南定分公司'),
    ('☎️ Hotline', '☎️ ホットライン', '☎️ 热线'),
    ('✉️ Email', '✉️ メール', '✉️ 邮箱'),
    ('THÔNG TIN CẦN BIẾT', 'ご案内', '须知信息'),
    ('Hình thức thanh toán', 'お支払い方法', '付款方式'),
    ('Chính sách hoàn hủy', 'キャンセルポリシー', '退改政策'),
    ('Chính sách bảo mật', 'プライバシーポリシー', '隐私政策'),
    ('Điều khoản giao dịch', 'ご利用規約', '交易条款'),
    ('CHỨNG NHẬN', '認証', '认证'),
    ('ĐĂNG KÝ NHẬN BẢN TIN', 'ニュースレター登録', '订阅资讯'),
    ('Nhập địa chỉ email để nhận thông tin mới nhất từ chúng tôi.', 'メールアドレスを入力して最新情報を受け取る。', '输入邮箱，获取我们的最新资讯。'),
    ('Giấy phép kinh doanh số 01033619401 do sở KH&ĐT TP abc cấp ngày 21/23 năm 2323', '事業登録番号 01033619401（abc市計画投資局 発行日 2323年21/23）', '营业执照编号 01033619401（abc市计划投资厅 于2323年21/23签发）'),
    ('Giấy phép Kinh doanh Lữ hành Quốc tế số 01711D/S2015/TCDL-GPLHabc', '国際旅行業登録番号 01711D/S2015/TCDL-GPLHabc', '国际旅行社经营许可证编号 01711D/S2015/TCDL-GPLHabc'),
    ('Kết nối với chúng tôi', 'フォローする', '关注我们'),
    ('Chấp nhận thanh toán', '対応決済', '支持的付款方式'),
    ('Địa chỉ email...', 'メールアドレス...', '电子邮箱...'),
    ('Gửi', '送信', '发送'),
]

PLACE_NAMES = ['Cầu Vàng', 'Bà Nà Hills', 'Phố cổ Hội An', 'Cầu Rồng', 'Ngũ Hành Sơn', 'Biển Mỹ Khê', 'Bán đảo Sơn Trà']

TR = {vi: {'ja': ja, 'zh': zh} for vi, ja, zh in _ROWS}
for _n in PLACE_NAMES:
    TR['Xem ' + _n] = {'ja': TR[_n]['ja'] + 'を見る', 'zh': '查看' + TR[_n]['zh']}

# Tên riêng / địa chỉ được giữ nguyên tiếng Việt (không báo là chưa dịch)
KEEP = ['Khánh An', 'KHÁNH AN', 'Nguyễn Khả Tâm', 'Tòa nhà Tuấn Hạnh', 'Điện Biên Phủ', 'Bặch Đằng', 'Trần Huy Liệu']

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
    # Tiêu đề "TOUR <strong>X</strong>": tiếng Nhật/Trung đặt chữ "ツアー/线路" ra sau (ゴルフツアー, 游轮线路)
    word = TR['TOUR'][lang]
    page = re.sub(rf'<h2 class="home-title">{word} <strong>([^<]+)</strong></h2>',
                  rf'<h2 class="home-title"><strong>\1</strong>{word}</h2>', page)
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
