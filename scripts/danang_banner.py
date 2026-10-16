"""Banner Đà Nẵng: dải biểu tượng chạy liên tục + slider địa điểm kèm thông tin.

Sửa nội dung trong PLACES rồi chạy lại: python3 scripts/build-html.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CREDITS = {c['slug']: c for c in json.loads((ROOT / 'images/danang/CREDITS.json').read_text(encoding='utf8'))}
TOUR_URL = 'https://dulich2.themedep.top/tour-trong-nuoc/'

# Biểu tượng nét vẽ (viewBox 64×64). Class "acc" = nét màu xanh lá nhấn.
ICONS = {
    'cau-vang': '''<path d="M3 23 Q32 11 61 23"/><path class="acc" d="M3 27.5 Q32 15.5 61 27.5"/>
      <path d="M12 61V34a2 2 0 0 1 4 0V30a2 2 0 0 1 4 0V29a2 2 0 0 1 4 0V32a2 2 0 0 1 4 0V61M16 46V34M20 46V30M24 46V32"/>
      <path d="M52 61V34a2 2 0 0 0-4 0V30a2 2 0 0 0-4 0V29a2 2 0 0 0-4 0V32a2 2 0 0 0-4 0V61M48 46V34M44 46V30M40 46V32"/>''',
    'ba-na-hills': '''<path class="acc" d="M3 9l58 13"/><path d="M32 15.5V24"/><rect x="21" y="24" width="22" height="18" rx="4"/><path d="M21 32h22M32 32v10"/>
      <path d="M2 61l15-15 9 8 14-16 22 23"/>''',
    'hoi-an': '''<path d="M32 3v7M25 10h14"/><path d="M25 14Q13 29 25 46h14q12-17 0-32z"/><path class="acc" d="M32 14v32M28 14q-6 16 0 32M36 14q6 16 0 32"/>
      <path d="M26 48h12M32 49v9M29 61h6"/>''',
    'cau-rong': '''<path d="M2 44h60"/><path d="M5 44Q11 26 17 44M17 44Q23 26 29 44M29 44Q35 26 41 44"/>
      <path d="M41 44Q44 33 50 31Q56 29 61 32L56 35Q54 37 51 36"/><path d="M50 31l-2-5M54 30l1-5"/><circle cx="55" cy="32" r=".6"/>
      <path class="acc" d="M4 54q4-4 8 0t8 0 8 0 8 0 8 0 8 0 8 0"/>''',
    'ngu-hanh-son': '''<path d="M2 54l12-20 7 9 11-24 10 18 7-9 13 26z"/><path class="acc" d="M29 19l3-7 3 7M28 24h8"/><path d="M2 60h60"/>''',
    'my-khe': '''<circle class="acc" cx="50" cy="14" r="6"/><path d="M20 60q3-18-3-33"/><path d="M17 27Q7 21 3 28M17 27q11-8 18-2M17 27Q13 15 5 14M17 27q6-14 15-14"/>
      <path class="acc" d="M28 48q5-4 10 0t10 0 10 0"/><path d="M2 60h60"/>''',
    'son-tra': '''<circle class="acc" cx="32" cy="12" r="7.5"/><circle cx="32" cy="12" r="3.5"/>
      <path d="M27.5 20Q24 35 22 48h20q-2-13-5.5-28Q32 17 27.5 20z"/><path d="M27 30q5 4 10 0"/>
      <path class="acc" d="M17 49q7 7 15 0 8 7 15 0"/><path d="M15 59h34M20 55h24"/>''',
}

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


def icon_svg(slug):
    return f'<svg class="dn-icon-svg" viewBox="0 0 64 64" aria-hidden="true">{ICONS[slug]}</svg>'


def marquee():
    items = ''.join(
        f'<li><button type="button" class="dn-icon" data-goto="{i}" aria-label="Xem {e(p["name"])}">{icon_svg(p["slug"])}<span>{e(p["name"])}</span></button></li>'
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
    c = CREDITS[p['slug']]
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
                <a class="dn-link" href="tel:0936336389"><i class="fa-solid fa-phone" aria-hidden="true"></i> 0936 336 389</a>
              </div>
            </div>
          </div>
          <a class="dn-credit" href="{c['source']}" target="_blank" rel="noopener">Ảnh: {e(c['author'])} · {e(c['license'])}</a>
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
