"""Banner Đà Nẵng: dải biểu tượng chạy liên tục + slider địa điểm kèm thông tin.

Sửa nội dung trong PLACES rồi chạy lại: python3 scripts/build-html.py
"""
import html

TOUR_URL = '#'  # trang tour chưa làm

PLACES = [
    dict(slug='cau-vang', name='Cầu Vàng', area='Bà Nà Hills',
         desc='Cây cầu dát vàng dài khoảng 150 m uốn lượn giữa mây trời ở độ cao gần 1.400 m, được nâng đỡ bởi đôi bàn tay đá khổng lồ. Từ khi khánh thành năm 2018, Cầu Vàng trở thành biểu tượng du lịch mới của Đà Nẵng.',
         facts=[('fa-location-dot', 'Vị trí', 'Sun World Bà Nà Hills'), ('fa-route', 'Khoảng cách', '~25 km'), ('fa-sun', 'Thời điểm đẹp', 'Sáng sớm, tháng 3 – 8')]),
    dict(slug='ba-na-hills', name='Bà Nà Hills', area='Núi Chúa',
         desc='Khu du lịch trên đỉnh núi Chúa cao 1.487 m, khí hậu mát mẻ quanh năm với trải nghiệm “4 mùa trong 1 ngày”. Hệ thống cáp treo đưa du khách tới Làng Pháp, vườn hoa Le Jardin d’Amour và khu vui chơi Fantasy Park.',
         facts=[('fa-mountain', 'Độ cao', '1.487 m'), ('fa-route', 'Khoảng cách', '~25 km'), ('fa-temperature-half', 'Nhiệt độ', '15 – 20°C')]),
    dict(slug='hoi-an', name='Phố cổ Hội An', area='Hội An',
         desc='Thương cảng sầm uất từ thế kỷ XVI – XVII, được UNESCO công nhận Di sản Văn hóa Thế giới năm 1999. Những dãy nhà tường vàng, Chùa Cầu và đèn lồng lung linh mỗi tối tạo nên vẻ đẹp hoài cổ khó quên.',
         facts=[('fa-landmark', 'Di sản', 'UNESCO 1999'), ('fa-route', 'Khoảng cách', '~30 km'), ('fa-moon', 'Nên đi', 'Chiều tối, đêm rằm')]),
    dict(slug='cau-rong', name='Cầu Rồng', area='Sông Hàn',
         desc='Cây cầu hình rồng vàng vươn mình trên sông Hàn, dài 666 m, khánh thành năm 2013. Vào 21h tối thứ Bảy và Chủ nhật, đầu rồng phun lửa, phun nước – màn trình diễn không thể bỏ lỡ.',
         facts=[('fa-ruler-horizontal', 'Chiều dài', '666 m'), ('fa-fire', 'Phun lửa', '21:00 T7 & CN'), ('fa-location-dot', 'Vị trí', 'Trung tâm thành phố')]),
    dict(slug='ngu-hanh-son', name='Ngũ Hành Sơn', area='Non Nước',
         desc='Quần thể 5 ngọn núi đá vôi Kim, Mộc, Thủy, Hỏa, Thổ nằm cạnh biển, ẩn chứa nhiều hang động và chùa cổ như động Huyền Không, chùa Tam Thai. Dưới chân núi là làng đá mỹ nghệ Non Nước lâu đời.',
         facts=[('fa-route', 'Khoảng cách', '~8 km'), ('fa-dungeon', 'Nổi bật', 'Động Huyền Không'), ('fa-clock', 'Tham quan', '2 – 3 giờ')]),
    dict(slug='my-khe', name='Biển Mỹ Khê', area='Sơn Trà',
         desc='Bãi biển cát trắng mịn, nước trong xanh và sóng êm, từng được tạp chí Forbes bình chọn là một trong những bãi biển quyến rũ nhất hành tinh. Lý tưởng để tắm biển, chèo SUP và ngắm bình minh.',
         facts=[('fa-route', 'Khoảng cách', '~3 km'), ('fa-umbrella-beach', 'Mùa tắm biển', 'Tháng 4 – 8'), ('fa-fish', 'Đặc sản', 'Hải sản tươi sống')]),
    dict(slug='son-tra', name='Bán đảo Sơn Trà', area='Chùa Linh Ứng',
         desc='“Lá phổi xanh” của Đà Nẵng với rừng nguyên sinh và loài voọc chà vá chân nâu quý hiếm. Chùa Linh Ứng trên bán đảo có tượng Phật Bà Quan Âm cao 67 m hướng ra biển Đông.',
         facts=[('fa-monument', 'Tượng Quan Âm', 'Cao 67 m'), ('fa-route', 'Khoảng cách', '~10 km'), ('fa-camera', 'Nên đi', 'Sáng sớm, hoàng hôn')]),
]

e = html.escape


def thumb(p):
    return f'<img class="dn-thumb" src="images/danang/thumbs/{p["slug"]}.jpg" alt="" width="56" height="56" decoding="async">'


def marquee():
    items = ''.join(
        f'<li><button type="button" class="dn-icon" data-goto="{i}" aria-label="Xem {e(p["name"])}">{thumb(p)}<span class="dn-icon-text"><strong>{e(p["name"])}</strong><small>{e(p["area"])}</small></span></button></li>'
        for i, p in enumerate(PLACES))
    # lặp 2 lần để vòng chạy liền mạch; bản thứ 2 ẩn với trình đọc màn hình
    return f'''
    <div class="dn-marquee">
      <div class="dn-marquee-label"><span>Biểu tượng</span><strong>Đà Nẵng</strong></div>
      <div class="dn-marquee-viewport">
        <div class="dn-marquee-track">
          <ul class="dn-marquee-list">{items}</ul>
          <ul class="dn-marquee-list" aria-hidden="true">{items.replace('<button type="button"', '<button type="button" tabindex="-1"')}</ul>
        </div>
      </div>
    </div>'''


def slide(i, p):
    src = f'images/danang/{p["slug"]}.jpg'
    img = (f'<img class="dn-photo" src="{src}" alt="{e(p["name"])}" fetchpriority="high">' if i == 0
           else f'<img class="dn-photo" data-src-deferred="{src}" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" alt="{e(p["name"])}">')
    facts = ''.join(f'<li><i class="fa-solid {ic}" aria-hidden="true"></i><span><small>{lb}</small>{v}</span></li>' for ic, lb, v in p['facts'])
    return f'''
        <div class="dn-slide dn-{p['slug']}">
          <div class="dn-media">{img}</div>
          <div class="dn-content container">
            <div class="dn-card">
              <span class="dn-tag">{i + 1:02d} / {len(PLACES):02d} · {e(p['area'])}</span>
              <h2 class="dn-title">{e(p['name'])}</h2>
              <p class="dn-desc">{e(p['desc'])}</p>
              <ul class="dn-facts">{facts}</ul>
              <div class="dn-actions">
                <a class="dn-btn" href="{TOUR_URL}">Xem tour Đà Nẵng <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
                <a class="dn-link" href="tel:0326978689"><i class="fa-solid fa-phone" aria-hidden="true"></i> 0326 978 689</a>
              </div>
            </div>
          </div>
        </div>'''


def banner(arrows):
    slides = ''.join(slide(i, p) for i, p in enumerate(PLACES))
    dots = ''.join(f'<button type="button" class="dn-dot" data-goto="{i}" aria-label="{e(p["name"])}"></button>' for i, p in enumerate(PLACES))
    return f'''
  <!-- BANNER ĐÀ NẴNG -->
  <section class="dn-banner" aria-label="Khám phá Đà Nẵng">
    {marquee()}
    <div class="slider-wrapper dn-places">
      <div class="slider" data-slider='{{"cellAlign":"center","autoPlay":6000,"adaptiveHeight":true,"attraction":0.1,"friction":0.6,"dragThreshold":10}}'>
        <div class="slider-viewport"><div class="slider-track">{slides}
        </div></div>
        {arrows}
        <div class="dn-dots">{dots}</div>
      </div>
    </div>
  </section>'''
