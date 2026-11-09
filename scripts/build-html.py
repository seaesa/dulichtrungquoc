#!/usr/bin/env python3
"""Sinh index.html tĩnh từ dữ liệu đã trích xuất (docs/research/content.json, icons.json).

Chạy: python3 scripts/build-html.py
"""
import html
import json
import re
from pathlib import Path

from danang_banner import banner
import option_tours
import i18n
import pages

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / 'docs/research/content.json').read_text(encoding='utf8'))
ICONS = json.loads((ROOT / 'docs/research/icons.json').read_text(encoding='utf8'))
SITE = 'https://dulich2.themedep.top'

e = html.escape

def img(url):
    if url.startswith(('tours/', 'danang/', 'hue/')):
        return 'images/' + url
    return 'images/' + url.rsplit('/', 1)[-1]


def lazy(url, alt='', cls=''):
    """Ảnh lazy-load theo section (JS nạp khi section sắp vào viewport)."""
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} data-src="{img(url)}" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" alt="{e(alt)}" decoding="async">'


def link(href):
    return href if href.startswith('http') or href.startswith('#') or href.startswith('?') else SITE + href


ARROWS = (
    '<button class="slider-btn prev" type="button" aria-label="Previous"><svg viewBox="0 0 100 100"><path d="M 10,50 L 60,100 L 70,90 L 30,50  L 70,10 L 60,0 Z" class="arrow"></path></svg></button>'
    '<button class="slider-btn next" type="button" aria-label="Next"><svg viewBox="0 0 100 100"><path d="M 10,50 L 60,100 L 70,90 L 30,50  L 70,10 L 60,0 Z" class="arrow" transform="translate(100, 100) rotate(180) "></path></svg></button>'
)


def title(plain, strong, strong_first=False):
    if strong_first:
        return f'<h2 class="home-title"><strong>{plain}</strong> {strong}</h2>'
    return f'<h2 class="home-title">{plain} <strong>{strong}</strong></h2>'


# ---------------------------------------------------------------- sections
def destination_slider(items):
    cells = ''.join(f'''
          <div class="dm-cell">
            <div class="box has-hover box-text-bottom">
              <div class="box-image">
                <a href="{link(it['href'])}">
                  <div class="image-overlay-add image-cover">
                    {lazy(it['img'], it['title'])}
                    <div class="overlay"></div>
                  </div>
                </a>
              </div>
              <div class="box-text text-left">
                <h3>{e(it['title'])}</h3>
                <p>Đã có lượt khách</p>
              </div>
            </div>
          </div>''' for it in items)
    return f'''
        <div class="slider-wrapper slider-danh-muc">
          <div class="slider slider-nav-outside" data-slider='{{"cellAlign":"center","autoPlay":4000,"adaptiveHeight":true,"attraction":0.1,"friction":0.6,"dragThreshold":10,"equalize":".box-text"}}'>
            <div class="slider-viewport"><div class="slider-track">{cells}
            </div></div>
            {ARROWS}
          </div>
        </div>'''


def credit_line(path):
    cs = json.loads((ROOT / path).read_text(encoding='utf8'))
    links = ' · '.join(f'<a href="{c["source"]}" target="_blank" rel="noopener">{e(c["author"])}</a> ({e(c["license"])})' for c in cs)
    return f'<p class="tour-credit">Ảnh: {links} · Wikimedia Commons</p>'


def credits_for(imgs):
    """Dòng ghi nguồn cho danh sách ảnh (đường dẫn trong images/, vd. 'hue/lang-tu-duc.jpg')."""
    by_path = {}
    for folder in ('danang', 'hue', 'tours'):
        for c in json.loads((ROOT / f'images/{folder}/CREDITS.json').read_text(encoding='utf8')):
            by_path[f"{folder}/{c['file']}"] = c
    seen, links = set(), []
    for path in imgs:
        c = by_path.get(path)
        if c and c['source'] not in seen:
            seen.add(c['source'])
            links.append(f'<a href="{c["source"]}" target="_blank" rel="noopener">{e(c["author"])}</a> ({e(c["license"])})')
    return f'<p class="tour-credit">Ảnh: {" · ".join(links)} · Wikimedia Commons</p>'


def option_card(t):
    vi_title, vi_route = t['title'][0], t['route'][0]
    price = f"${t['price']:,}{'〜' if t.get('from_') else ''}"
    meal_row = (f'<div class="thong-tin-sp"><div class="khoi-hanh"><span class="label"><i class="fa-solid fa-utensils" aria-hidden="true"></i> Bữa ăn: </span><span class="value">{e(t["meal"])}</span></div></div>'
                if t.get('meal') else '')
    return f'''
          <div class="tour-cell">
            <div class="col-inner">
              <div class="product-small box has-hover box-text-bottom op-card">
                <div class="box-image">
                  <div class="image-overlay-add image-cover">
                    <a href="#" aria-label="{e(vi_title)}">{lazy(t['img'], vi_title)}</a>
                    <div class="overlay"></div>
                  </div>
                  <span class="box-ngay-khoi-hanh"><i class="fa-regular fa-clock" aria-hidden="true"></i> {e(t['time'])}</span>
                </div>
                <div class="box-text">
                  <div class="title-wrapper"><p class="product-title"><a href="#">{e(vi_title)}</a></p></div>
                  <p class="op-route">{e(vi_route)}</p>
                  {meal_row}
                  <div class="price-wrapper"><span class="price"><span class="amount">{price}</span><span class="price-suffix">{e(t.get('suffix', '/khách'))}</span></span></div>
                  <div class="add-to-cart-button"><a href="contact.html" rel="nofollow">Đặt Tour</a></div>
                </div>
              </div>
            </div>
          </div>'''


def option_section():
    cards = ''.join(option_card(t) for t in option_tours.TOURS)
    return f'''
  <section class="section section3" id="recommended">
    <div class="section-content">
      <div class="row row-small">
        <div class="col small-12 large-12"><div class="col-inner">
          {title('TOUR', 'GỢI Ý')}
          <div class="slider row-slider tour-slider slider-nav-outside slider-nav-push" data-slider='{{"cellAlign":"left","groupCells":true,"autoPlay":4000,"dragThreshold":5,"equalize":".box-text"}}'>
            <div class="slider-viewport"><div class="slider-track">{cards}
            </div></div>
            {ARROWS}
          </div>
          <p class="op-note"><i class="fa-solid fa-circle-info" aria-hidden="true"></i> Giá tham khảo tính theo USD/khách · Thanh toán bằng VND</p>
          {credits_for([t['img'] for t in option_tours.TOURS])}
        </div></div>
      </div>
    </div>
  </section>'''


def cta_section():
    return f'''
  <section class="section section-cta">
    <div class="section-content">
      <div class="row row-small">
        <div class="col small-12 large-12"><div class="col-inner text-center">
          {title('NHẬN BÁO GIÁ', 'TRONG 24 GIỜ')}
          <p class="lead">Cho chúng tôi biết ngày đi, số người, có trẻ nhỏ hoặc người cao tuổi đi cùng hay không. Chúng tôi sẽ gửi lịch trình và báo giá trong vòng 24 giờ.</p>
          <a class="button primary" href="contact.html">Yêu cầu báo giá</a>
        </div></div>
      </div>
    </div>
  </section>'''


# "Bạn muốn đi đâu": khách inbound → điểm nổi tiếng Đà Nẵng và lăng tẩm Huế
DESTS = [
    [dict(href='#', img=f'danang/{slug}.jpg', title=t) for slug, t in [
        ('cau-vang', 'Cầu Vàng'), ('ba-na-hills', 'Bà Nà Hills'), ('cau-rong', 'Cầu Rồng'), ('ngu-hanh-son', 'Ngũ Hành Sơn'),
        ('my-khe', 'Biển Mỹ Khê'), ('son-tra', 'Bán đảo Sơn Trà'), ('hoi-an', 'Phố cổ Hội An'), ('my-son', 'Thánh địa Mỹ Sơn')]],
    [dict(href='#', img=f'hue/{slug}.jpg', title=t) for slug, t in [
        ('lang-khai-dinh', 'Lăng Khải Định'), ('lang-tu-duc', 'Lăng Tự Đức'), ('lang-minh-mang', 'Lăng Minh Mạng'),
        ('lang-dong-khanh', 'Lăng Đồng Khánh')]],
]


WHY = [
    ('TOUR RIÊNG', 'Thiết kế lịch trình theo yêu cầu, xe riêng 4–16 chỗ'),
    ('HƯỚNG DẪN VIÊN', 'Hỗ trợ tiếng Nhật và tiếng Hàn'),
    ('BÁO GIÁ 24 GIỜ', 'Báo giá rõ ràng, minh bạch qua email hoặc LINE'),
    ('ĐẶT TOUR', 'Dễ dàng nhanh chóng chỉ 3 bước'),
    ('THANH TOÁN', 'Đơn giản, an toàn và linh hoạt'),
    ('HOTLINE', '0326 978 689 Trực tuyến 24/7'),
]
SERVICES = [
    ('#fd6666', 'Đón tiễn sân bay', 'Xe 4–16 chỗ, đón theo giờ bay, hỗ trợ qua LINE'),
    ('#003594', 'Thuê xe có tài xế', 'Xe riêng kèm tài xế, linh hoạt theo lịch trình'),
    ('#fd8008', 'Khách sạn &amp; nhà hàng', 'Đặt phòng, đặt bàn, set menu riêng cho khách'),
    ('#89c440', 'Phiên dịch', 'Phiên dịch tiếng Nhật, tiếng Hàn cho tour và công tác'),
]
NEWS = [dict(href='#', img=f'danang/{i}.jpg' if f else f'{i}.jpg', cat=c, date='03/11/2026', title=t) for i, f, c, t in [
    ('cau-vang', 1, 'Cẩm nang du lịch', 'Cầu Vàng Bà Nà Hills: kinh nghiệm đi cáp treo và giờ đẹp để ngắm cảnh'),
    ('hoi-an', 1, 'Cẩm nang du lịch Tin tức', 'Hội An về đêm: thả đèn hoa đăng và những món ăn nên thử'),
    ('my-son', 1, 'Cẩm nang du lịch', 'Thánh địa Mỹ Sơn: vì sao nên đi vào buổi sáng'),
    ('hue/lang-khai-dinh', 0, 'Cẩm nang du lịch Tin tức', 'Khám phá lăng Khải Định, lăng Tự Đức và Đại Nội trong một ngày ở Huế'),
    ('cau-rong', 1, 'Cẩm nang du lịch', 'Cầu Rồng phun lửa và du thuyền sông Hàn: lịch trình buổi tối ở Đà Nẵng'),
    ('ngu-hanh-son', 1, 'Cẩm nang du lịch Tin tức', 'Ngũ Hành Sơn, biển Mỹ Khê và chùa Linh Ứng: nửa ngày tham quan Đà Nẵng'),
]]

MOMENTS = [
    ('danang/ba-na-hills.jpg', True),
    ('danang/hoi-an.jpg', False),
    ('danang/my-khe.jpg', True),
    ('danang/son-tra.jpg', False),
]
TESTIMONIALS = [
    ('Lại một lần nữa công ty SANSHIN đồng hành cùng Khánh An Tourism trong chuyến du lịch Hội An. Mọi thứ đều tốt đẹp, hướng dẫn viên “anh Thành” luôn chu đáo từng bữa ăn, từng chỗ ngủ trong khách sạn, đoàn chúng tôi luôn an tâm khi đi cùng Khánh An Tourism trong mọi chuyến du lịch. Khánh An Tourism luôn trong suy nghĩ đầu tiên của chúng tôi trong mỗi lần có ý định đi du lịch. Cảm ơn Khánh An Tourism đã nhiệt tình hỗ trợ hết mình',
     'Screenshot-2024-03-18-130615.png', 'Công ty TNHH SANSHIN', 'Tour Hội An lung linh'),
    ('Chúng tôi du lịch tới Bà Nà Hills xinh đẹp. Được đồng hành cùng công ty du lịch Khánh An Tourism. Chúng tôi thấy được quan tâm chăm sóc tận tình từng bữa ăn giấc ngủ khi đi du lịch. Hướng dẫn viên của công ty Khánh An Tourism chu đáo, tận tình. Trước ngày đi chúng tôi còn được công ty thông báo đến từng người giờ khởi hành và những thứ cần chuẩn bị. Công ty Khánh An Tourism sẽ là lựa chọn tin tưởng nhất cho những chuyến du lịch lần sau.',
     'Screenshot-2024-03-18-130622.png', 'Nguyễn Khả Tâm', 'Cảm nhận về tour Bà Nà Hills do công ty tổ chức'),
]
NAV = [
    ('Trang chủ', 'index.html'),
    ('Giới thiệu', 'about.html'),
    ('Tour du lịch', 'tours.html'),
    ('Cẩm nang du lịch', 'travel-guide.html'),
    ('Visa du lịch', 'visa.html'),
    ('Tin tức', 'news.html'),
    ('Liên hệ', 'contact.html'),
]
SUBNAV = []


def search_form(fid):
    return f'''<form class="searchform" role="search" method="get" action="{SITE}/">
                  <div class="flex-row">
                    <div class="flex-col flex-grow">
                      <label class="screen-reader-text" for="{fid}">Tìm kiếm:</label>
                      <input type="search" id="{fid}" class="search-field" placeholder="Nhập từ khóa cần tìm" name="s">
                      <input type="hidden" name="post_type" value="product">
                    </div>
                    <div class="flex-col">
                      <button type="submit" class="submit-button" aria-label="Submit"><i class="icon-search"></i></button>
                    </div>
                  </div>
                </form>'''


def email_form(fid):
    return f'''<form class="email-form" novalidate>
                  <div class="row row-small form-email">
                    <div class="col large-9"><input type="email" id="{fid}" name="email" placeholder="Địa chỉ email..." aria-required="true"></div>
                    <div class="col large-3"><input type="submit" value="Gửi"></div>
                  </div>
                  <div class="form-response" hidden></div>
                </form>'''


# Biểu tượng cắt từ logo.png (logo đầy đủ: images/logo-khanh-an.jpg)
BRAND_MARK = '<img class="brand-mark" src="images/logo-emblem.png" width="225" height="160" alt="">'


def header():
    contact = '''<li><a href="mailto:nguyelyhungdd@gmail.com"><i class="icon-envelop"></i><span>nguyelyhungdd@gmail.com</span></a></li>
              <li><a href="tel:0326978689"><i class="icon-phone"></i><span>0326 978 689</span></a></li>'''
    main_nav = []
    for label, href in NAV:
        if label == 'Tour du lịch' and SUBNAV:
            subs = ''.join(f'<li><a href="{h}">{l}</a></li>' for l, h in SUBNAV)
            main_nav.append(f'<li class="has-dropdown"><a href="{href}">{label}<i class="icon-angle-down"></i></a><ul class="nav-dropdown">{subs}</ul></li>')
        else:
            main_nav.append(f'<li><a href="{href}">{label}</a></li>')
    main_nav = '\n            '.join(main_nav)
    return f'''
<header id="header" class="header">
  <div class="header-wrapper">
    <div id="top-bar" class="header-top hide-for-sticky">
      <div class="flex-row container">
        <div class="flex-col hide-for-medium flex-left">
          <ul class="nav nav-left header-contact">
              {contact}
          </ul>
        </div>
        <div class="flex-col hide-for-medium flex-right">
          <ul class="nav nav-right top-bar-nav">
            <li><a href="careers.html"><img class="ux-menu-icon" src="images/user-id-svgrepo-com.svg" width="22" height="22" alt="">Tuyển dụng</a></li>
            <li><a href="payment.html"><img class="ux-menu-icon" src="images/pay-svgrepo-com.svg" width="22" height="22" alt="">Hướng dẫn thanh toán</a></li>
            <li><a href="contact.html"><img class="ux-menu-icon" src="images/contact-us-svgrepo-com.svg" width="22" height="22" alt="">Liên hệ</a></li>
            <!--LANG_SWITCH-->
          </ul>
        </div>
        <div class="flex-col show-for-medium flex-grow mobile-contact-wrap">
          <ul class="nav header-contact mobile-contact">
              {contact}
          </ul>
          <!--LANG_SWITCH_MOBILE-->
        </div>
      </div>
    </div>
    <div id="masthead" class="header-main">
      <div class="header-inner flex-row">
        <div id="logo" class="flex-col logo">
          <a href="index.html" title="Khánh An Tourism" rel="home" class="brand">{BRAND_MARK}<span class="brand-text"><strong>KHÁNH AN</strong><small>TOURISM</small></span></a>
        </div>
        <div class="flex-col show-for-medium mobile-left">
          <ul class="nav nav-left mobile-nav">
            <li><a href="#" class="js-open-menu" aria-label="Menu" aria-controls="main-menu" aria-expanded="false"><i class="icon-menu"></i></a></li>
          </ul>
        </div>
        <div class="flex-col hide-for-medium flex-right">
          <ul class="nav nav-right header-nav-main">
            {main_nav}
            <li class="header-search has-dropdown"><a href="#" aria-label="Tìm kiếm"><i class="icon-search"></i></a>
              <ul class="nav-dropdown"><li class="header-search-form">
                {search_form('search-desktop')}
              </li></ul>
            </li>
          </ul>
        </div>
        <div class="flex-col show-for-medium mobile-right">
          <ul class="nav nav-right mobile-nav"></ul>
        </div>
      </div>
    </div>
  </div>
</header>'''


def offcanvas():
    items = []
    for label, href in NAV:
        if label == 'Tour du lịch' and SUBNAV:
            subs = ''.join(f'<li><a href="{h}">{l}</a></li>' for l, h in SUBNAV)
            items.append(f'<li class="menu-item has-child"><a href="{href}">{label}</a><button class="toggle" type="button" aria-label="Toggle" aria-expanded="false"><i class="icon-angle-down"></i></button><ul class="sub-menu">{subs}</ul></li>')
        else:
            items.append(f'<li class="menu-item"><a href="{href}">{label}</a></li>')
    items = '\n          '.join(items)
    return f'''
<div class="mfp-bg" hidden></div>
<div class="mfp-wrap" id="main-menu" hidden tabindex="-1">
  <div class="mfp-container">
    <div class="mfp-content">
      <div class="sidebar-menu">
        <ul class="nav-sidebar">
          <li class="html">
                {search_form('search-mobile')}
          </li>
          {items}
          <!--LANG_SWITCH_SIDEBAR-->
        </ul>
      </div>
    </div>
  </div>
  <button title="Close (Esc)" type="button" class="mfp-close"><svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></button>
</div>'''


def line_phone():
    """Màn hình tài khoản LINE chính thức dựng bằng HTML/CSS (thay ảnh chụp Zalo cũ)."""
    return '''<div class="line-phone" aria-hidden="true">
                    <div class="lp-screen">
                      <div class="lp-status"><span>9:41</span><span><i class="fa-solid fa-signal"></i> <i class="fa-solid fa-wifi"></i> <i class="fa-solid fa-battery-full"></i></span></div>
                      <div class="lp-bar"><i class="fa-solid fa-chevron-left"></i><span>Khánh An Tourism</span><i class="fa-solid fa-ellipsis"></i></div>
                      <div class="lp-cover"><img src="images/danang/thumbs/cau-vang.jpg" alt="" loading="lazy"></div>
                      <div class="lp-profile">
                        <span class="lp-avatar">''' + BRAND_MARK + '''</span>
                        <strong>Khánh An Tourism <i class="fa-solid fa-circle-check"></i></strong>
                        <small>Tài khoản chính thức</small>
                      </div>
                      <span class="lp-add"><i class="fa-solid fa-user-plus"></i> Kết bạn</span>
                      <ul class="lp-info">
                        <li><i class="fa-solid fa-phone"></i> 0326 978 689</li>
                        <li><i class="fa-regular fa-clock"></i> 8:00 – 18:00</li>
                        <li><i class="fa-solid fa-ticket"></i> Ưu đãi cho bạn bè LINE</li>
                      </ul>
                    </div>
                  </div>'''


def post_cards(items):
    return ''.join(f'''
          <div class="post-item">
            <a href="{p['href']}" class="plain">
              <div class="box box-blog-post has-hover">
                <div class="box-image"><div class="image-cover">{lazy(p['img'], p['title'])}</div></div>
                <div class="box-text text-left">
                  <p class="cat-label">{e(p['cat'])} <span class="post-meta"><i class="fa-solid fa-calendar-days"></i> {p['date']}</span></p>
                  <h5 class="post-title">{e(p['title'])}</h5>
                </div>
              </div>
            </a>
          </div>''' for p in items)


def main_content():
    tours = DATA['section3']
    why = ''.join(f'''
            <div class="col why-col medium-2 small-12 large-2"><div class="col-inner">
              <div class="icon-box icon-box-center">
                <div class="icon-box-img">{ICONS[f'section4_{i}']}</div>
                <div class="icon-box-text last-reset"><h3>{t}</h3><p>{d}</p></div>
              </div>
            </div></div>''' for i, (t, d) in enumerate(WHY))
    services = ''.join(f'''
        <div class="col svc medium-3 small-12 large-3"><div class="col-inner" style="background-color:{bg};">
          <div class="icon-box icon-box-left">
            <div class="icon-box-img">{ICONS[f'section5_{i + 6}']}</div>
            <div class="icon-box-text last-reset"><h3>{t}</h3><p>{d}</p></div>
          </div>
        </div></div>''' for i, (bg, t, d) in enumerate(SERVICES))
    moments = ''.join(f'''
              <div class="col small-img medium-6 small-12 large-6"><div class="col-inner">
                <div class="img has-hover"><div class="img-inner{' image-zoom' if zoom else ''} image-cover" style="padding-top:75%;">{lazy(f)}</div></div>
              </div></div>''' for f, zoom in MOMENTS)
    testimonials = ''.join(f'''
        <div class="col medium-6 small-12 large-6"><div class="col-inner">
          <blockquote><p>{q}</p></blockquote>
          <div class="icon-box icon-box-left">
            <div class="icon-box-img">{lazy(f'/{a}', n)}</div>
            <div class="icon-box-text last-reset">
              <h3>{n}</h3>
              <p>{'<i class="fa-solid fa-star"></i>' * 5}</p>
              <p>{r}</p>
            </div>
          </div>
        </div></div>''' for q, a, n, r in TESTIMONIALS)
    posts = post_cards(NEWS)

    return f'''
<main id="main">
{banner(ARROWS)}

  <!-- section1: bộ lọc tour (để trống như bản gốc) -->
  <section class="section section1">
    <div class="section-content">
      <div class="row row-small">
        <div class="col medium-5 small-12 large-5"><div class="col-inner"></div></div>
        <div class="col medium-3 small-12 large-3"><div class="col-inner"></div></div>
        <div class="col medium-2 small-12 large-2"><div class="col-inner"></div></div>
        <div class="col medium-2 small-12 large-2"><div class="col-inner"></div></div>
      </div>
    </div>
  </section>

  <!-- section2: Bạn muốn đi đâu -->
  <section class="section section2">
    <div class="section-content">
      <div class="row row-small">
        <div class="col small-12 large-12"><div class="col-inner">
          {title('BẠN MUỐN', 'ĐI ĐÂU')}
          <h3 class="dest-label"><i class="fa-solid fa-location-dot" aria-hidden="true"></i> Địa điểm nổi tiếng Đà Nẵng</h3>
          {destination_slider(DESTS[0])}
          <div class="gap-15"></div>
          <h3 class="dest-label"><i class="fa-solid fa-landmark" aria-hidden="true"></i> Lăng tẩm Huế</h3>
          {destination_slider(DESTS[1])}
          {credits_for(['danang/my-son.jpg'] + [d['img'] for d in DESTS[1]])}
        </div></div>
      </div>
    </div>
  </section>

  <!-- section4: Vì sao chọn chúng tôi -->
  <section class="section section4">
    <div class="section-content">
      <div class="row row-small">
        <div class="col small-12 large-12"><div class="col-inner why-inner">
          {title('VÌ SAO CHỌN', 'CHÚNG TÔI', strong_first=True)}
          <div class="row row-small">{why}
          </div>
        </div></div>
      </div>
    </div>
  </section>

  {option_section()}
  {cta_section()}

  <!-- section5: Các dịch vụ -->
  <section class="section section5">
    <div class="section-content">
      <div class="row row-small">
        <div class="col small-12 large-12"><div class="col-inner">
          {title('CÁC DỊCH VỤ', 'CỦA CHÚNG TÔI')}
        </div></div>{services}
      </div>
    </div>
  </section>

  <!-- section9: Khoảnh khắc đẹp nhất -->
  <section class="section section9">
    <div class="section-content">
      <div class="row row-small">
        <div class="col small-12 large-12"><div class="col-inner">
          {title('KHOẢNH KHẮC', 'ĐẸP NHẤT')}
        </div></div>
        <div class="col medium-7 small-12 large-7"><div class="col-inner">
          <div class="img has-hover"><div class="img-inner image-zoom image-cover" style="padding-top:53.7%;">{lazy('danang/cau-rong.jpg')}</div></div>
        </div></div>
        <div class="col medium-5 small-12 large-5"><div class="col-inner">
          <div class="row row-small">{moments}
          </div>
        </div></div>
      </div>
    </div>
  </section>

  <!-- section-kh: Khách hàng đồng hành -->
  <section class="section section-kh">
    <div class="section-content">
      <div class="row row-small">
        <div class="col small-12 large-12"><div class="col-inner">
          {title('KHÁCH HÀNG', 'ĐỒNG HÀNH')}
          <p class="lead">Những khoảnh khắc của du khách trên hành trình cùng Khánh An Tourism</p>
          <div class="kh-grid"><a class="kh-item" href="images/khach-hang/kh-01.jpg"><img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" data-src="images/khach-hang/kh-01.jpg" width="900" height="675" alt="" decoding="async"></a><a class="kh-item" href="images/khach-hang/kh-02.jpg"><img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" data-src="images/khach-hang/kh-02.jpg" width="900" height="675" alt="" decoding="async"></a><a class="kh-item" href="images/khach-hang/kh-03.jpg"><img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" data-src="images/khach-hang/kh-03.jpg" width="675" height="900" alt="" decoding="async"></a><a class="kh-item" href="images/khach-hang/kh-04.jpg"><img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" data-src="images/khach-hang/kh-04.jpg" width="675" height="900" alt="" decoding="async"></a><a class="kh-item" href="images/khach-hang/kh-05.jpg"><img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" data-src="images/khach-hang/kh-05.jpg" width="675" height="900" alt="" decoding="async"></a><a class="kh-item" href="images/khach-hang/kh-06.jpg"><img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" data-src="images/khach-hang/kh-06.jpg" width="900" height="675" alt="" decoding="async"></a><a class="kh-item" href="images/khach-hang/kh-07.jpg"><img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" data-src="images/khach-hang/kh-07.jpg" width="900" height="675" alt="" decoding="async"></a><a class="kh-item" href="images/khach-hang/kh-08.jpg"><img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" data-src="images/khach-hang/kh-08.jpg" width="900" height="675" alt="" decoding="async"></a><a class="kh-item" href="images/khach-hang/kh-09.jpg"><img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" data-src="images/khach-hang/kh-09.jpg" width="900" height="675" alt="" decoding="async"></a></div>
        </div></div>
      </div>
    </div>
  </section>

  <!-- section10: Khách hàng nói gì -->
  <section class="section section10">
    <div class="section-content">
      <div class="row row-small">
        <div class="col small-12 large-12"><div class="col-inner">
          {title('KHÁCH HÀNG NÓI GÌ', 'VỀ CHÚNG TÔI')}
          <p class="lead">Đánh giá, cảm nhận của khách hàng đã sử dụng dịch vụ của chúng tôi</p>
        </div></div>{testimonials}
      </div>
    </div>
  </section>

  <!-- section11: LINE (thay Zalo OA) -->
  <section class="section section11">
    <div class="section-content">
      <div class="row">
        <div class="col small-12 large-12"><div class="col-inner zalo-bg">
          <div class="row row-collapse">
            <div class="col zalo-col medium-8 small-12 large-8"><div class="col-inner zalo-box">
              <div class="row row-small">
                <div class="col phone-col medium-4 small-12 large-4"><div class="col-inner">
                  {line_phone()}
                </div></div>
                <div class="col medium-8 small-12 large-8"><div class="col-inner">
                  <h2>Giảm % cho khách hàng kết bạn LINE chính thức của CHÚNG TÔI</h2>
                  <p>Đặt tour dễ dàng trên Website &amp; LINE</p>
                  <div class="row row-small row-divided">
                    <div class="col medium-8 small-12 large-8"><div class="col-inner">
                      <p>Để lại mail chúng tôi sẽ gửi chương trình chi tiết tới bạn.</p>
                      {email_form('email-zalo')}
                    </div></div>
                    <div class="col qr-col medium-4 small-12 large-4"><div class="col-inner">
                      <p><span>Quét mã QR để được tư vấn nhanh nhất</span></p>
                      <img class="line-qr" src="images/line-qr.jpg" width="644" height="645" alt="Mã QR LINE Khánh An Tourism" loading="lazy">
                    </div></div>
                  </div>
                </div></div>
              </div>
            </div></div>
          </div>
        </div></div>
      </div>
    </div>
  </section>

  <!-- section12: Tin tức du lịch -->
  <section class="section section12">
    <div class="section-content">
      <div class="row">
        <div class="col small-12 large-12"><div class="col-inner">
          {title('TIN TỨC', 'DU LỊCH')}
          <p class="lead">Kinh nghiệm và thông tin du lịch Đà Nẵng, Hội An, Huế dành cho du khách Nhật Bản và Hàn Quốc</p>
          <div class="gap-10"></div>
          <div class="slider row-slider list-post slider-nav-outside slider-nav-push" data-slider='{{"cellAlign":"left","groupCells":true,"autoPlay":0,"dragThreshold":5,"equalize":".box-text"}}'>
            <div class="slider-viewport"><div class="slider-track">{posts}
            </div></div>
            {ARROWS}
          </div>
        </div></div>
      </div>
    </div>
  </section>
</main>'''


def footer():
    return f'''
<footer id="footer" class="footer-wrapper">
  <section class="section footer-section">
    <div class="section-content">
      <div class="row row-small">
        <div class="col medium-5 small-12 large-5"><div class="col-inner">
          <img class="footer-logo" src="images/logo-khanh-an.jpg" width="600" height="600" alt="Khánh An Tourism" loading="lazy">
          <h3>KHÁNH AN TOURISM</h3>
          <p><strong>📍 Địa chỉ</strong>: 108, Phạm Xuân Ẩn, Cẩm Lệ, Đà Nẵng</p>
          <p><strong>☎️ Hotline</strong>: <a href="tel:0326978689">0326 978 689</a></p>
          <p><strong>💬 Zalo</strong>: <a href="https://zalo.me/0326978689" target="_blank" rel="noopener">0326 978 689</a></p>
          <p><strong>✉️ Email</strong>: <a href="mailto:nguyelyhungdd@gmail.com">nguyelyhungdd@gmail.com</a></p>
        </div></div>
        <div class="col medium-7 small-12 large-7"><div class="col-inner">
          <div class="row row-small">
            <div class="col medium-6 small-12 large-6"><div class="col-inner">
              <h3>THÔNG TIN CẦN BIẾT</h3>
              <ul>
                <li><a href="about.html">Giới thiệu</a></li>
                <li><a href="contact.html">Liên hệ</a></li>
                <li><a href="payment.html">Hình thức thanh toán</a></li>
                <li><a href="refund-policy.html">Chính sách hoàn hủy</a></li>
                <li><a href="privacy-policy.html">Chính sách bảo mật</a></li>
                <li><a href="terms.html">Điều khoản giao dịch</a></li>
              </ul>
            </div></div>
            <div class="col medium-6 small-12 large-6"><div class="col-inner">
              <h3>ĐĂNG KÝ NHẬN BẢN TIN</h3>
              <p>Nhập địa chỉ email để nhận thông tin mới nhất từ chúng tôi.</p>
              {email_form('email-footer')}
            </div></div>
          </div>
        </div></div>
        <div class="col hide-for-small medium-7 small-12 large-7"><div class="col-inner">
          <div class="row row-small">
            <div class="col medium-4 small-12 large-4"><div class="col-inner">
              <h3>Kết nối với chúng tôi</h3>
              <div class="social-icons">
                <a href="http://url" target="_blank" rel="noopener nofollow" class="button icon facebook" title="Follow on Facebook" aria-label="Follow on Facebook"><i class="icon-facebook"></i></a><a href="http://url" target="_blank" rel="noopener nofollow" class="button icon instagram" title="Follow on Instagram" aria-label="Follow on Instagram"><i class="icon-instagram"></i></a><a href="http://url" target="_blank" rel="noopener nofollow" class="button icon twitter" title="Follow on Twitter" aria-label="Follow on Twitter"><i class="icon-twitter"></i></a><a href="mailto:nguyelyhungdd@gmail.com" target="_blank" rel="nofollow" class="button icon email" title="Send us an email" aria-label="Send us an email"><i class="icon-envelop"></i></a>
              </div>
            </div></div>
            <div class="col medium-4 small-12 large-4"><div class="col-inner">
              <h3>Chấp nhận thanh toán</h3>
              <div class="payment-img"><img src="images/thanhtoan.jpg" width="418" height="62" alt="Chấp nhận thanh toán" loading="lazy"></div>
            </div></div>
          </div>
        </div></div>
      </div>
    </div>
  </section>
  <div class="absolute-footer">
    <div class="container">
      <div class="footer-primary">
        <div class="copyright-footer">Copyright 2026 © Khánh An Tourism</div>
      </div>
    </div>
  </div>
  <a href="#top" class="back-to-top hide-for-medium" aria-label="Go to top"><i class="icon-angle-up"></i></a>
</footer>'''


def shell(main, title, desc, lang_attr='vi'):
    return f'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="images/favicon-32.png" sizes="32x32">
<link rel="icon" href="images/favicon-192.png" sizes="192x192">
<link rel="apple-touch-icon" href="images/favicon-180.png">
<link rel="preload" href="fonts/GoogleSans-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/GoogleSans-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer">
<link rel="stylesheet" href="css/style.css">
</head>
<body id="top">
<a class="screen-reader-text" href="#main">Skip to content</a>
{header()}
{main}
{footer()}
{offcanvas()}
<script src="js/main.js"></script>
</body>
</html>
'''


def finish(page):
    """Link ngoài chưa làm → '#'. Nút Đặt Tour → trang liên hệ."""
    page = re.sub(r'href="\?add-to-cart=\d+"', 'href="contact.html"', page)
    page = re.sub(r'href="(?:https?://(?:dulich2\.themedep\.top|dulich2\.khothemewp\.vn|khothemewp\.vn)[^"]*|http://url)"', 'href="#"', page)
    return page.replace(f'action="{SITE}/"', 'action="#"')


# ---------------------------------------------------------------- trang con
SLUGS = list(pages.PAGES)


def localize(page, lang, slug=None):
    """Link nội bộ → URL sạch theo ngôn ngữ; đường dẫn tài nguyên → tuyệt đối (trang nằm trong thư mục con)."""
    home = i18n.page_url(lang)
    if slug is None:
        page = page.replace('href="index.html#', 'href="#')
    for s in SLUGS:
        page = page.replace(f'href="{s}.html"', f'href="{i18n.page_url(lang, s)}"')
    page = page.replace('href="index.html#', f'href="{home}#').replace('href="index.html"', f'href="{home}"')
    return re.sub(r'(\b(?:src|href|data-src|data-src-deferred)=")((?:images|css|js|fonts)/)', r'\1/\2', page)


def tour_group(plain, strong, inner, credit=''):
    return f'<div class="page-group">{title(plain, strong)}{inner}{credit}</div>'


def tours_block(kind):
    out = []
    groups = [('GỢI Ý', option_tours.TOURS)] + list(option_tours.GROUPS)
    for i, (name, tours) in enumerate(groups):
        cards = ''.join(option_card(t) for t in tours)
        note = ('\n<p class="op-note"><i class="fa-solid fa-circle-info" aria-hidden="true"></i> Giá tham khảo tính theo USD/khách · Thanh toán bằng VND</p>'
                if i == 0 else '')
        out.append(tour_group('TOUR', name, f'<div class="tour-grid">{cards}</div>{note}',
                              credits_for([t['img'] for t in tours])))
    return ''.join(out)


def contact_block(k):
    rows = [('fa-location-dot', ('住所', '주소'), ADDR), ('fa-phone', ('ホットライン', '핫라인'), f'<a href="tel:0326978689">{pages.PHONE}</a>'),
            ('fa-envelope', ('メール', '이메일'), f'<a href="mailto:{pages.EMAIL}">{pages.EMAIL}</a>'),
            ('fa-clock', ('営業時間', '영업시간'), ('毎日 8:00 – 18:00（ホットラインは24時間）', '매일 8:00 – 18:00 (핫라인은 24시간)'))]
    items = ''.join(f'<li><i class="fa-solid {ic}" aria-hidden="true"></i><div><strong>{lab[k]}</strong><span>{val if isinstance(val, str) else val[k]}</span></div></li>' for ic, lab, val in rows)
    maps = ('Googleマップで見る', 'Google 지도에서 보기')[k]
    msg = ('メールアドレスをご入力ください。担当者より24時間以内にご連絡します。', '이메일 주소를 입력해 주세요. 담당자가 24시간 이내에 연락드립니다.')[k]
    ask = (('お見積もりのためにお知らせいただきたいこと', '견적을 위해 알려 주세요'),
           [('出発日・滞在日数', '출발일·체류 일수'), ('ご参加人数（お子様・ご年配の方の有無）', '참가 인원(어린이·어르신 동반 여부)'),
            ('ご希望のホテルのグレード', '희망 호텔 등급'), ('ご興味のある観光地・体験', '관심 있는 관광지·체험')])
    askhtml = f'<h3 class="ask-h">{ask[0][k]}</h3><ul class="page-list">' + ''.join(f'<li>{x[k]}</li>' for x in ask[1]) + '</ul>'
    qr = ('QRコードをスキャンして、LINEでご相談ください。', 'QR 코드를 스캔해 LINE으로 상담하세요.')[k]
    return f'''<div class="row row-small contact-grid">
  <div class="col medium-6 small-12 large-6"><div class="col-inner">
    <ul class="contact-list">{items}</ul>
    {askhtml}
    <a class="button primary" href="https://www.google.com/maps/search/?api=1&amp;query=108+Ph%E1%BA%A1m+Xu%C3%A2n+%E1%BA%A8n+C%E1%BA%A9m+L%E1%BB%87+%C4%90%C3%A0+N%E1%BA%B5ng" target="_blank" rel="noopener">{maps}</a>
  </div></div>
  <div class="col medium-6 small-12 large-6"><div class="col-inner contact-side">
    <p>{msg}</p>
    {email_form('email-contact')}
    <p class="qr-text">{qr}</p>
    <img class="line-qr" src="images/line-qr.jpg" width="644" height="645" alt="Mã QR LINE Khánh An Tourism" loading="lazy">
  </div></div>
</div>'''


ADDR = pages.ADDRESS


def sub_blocks(slug, lang):
    k = 0 if lang == 'ja' else 1
    out = []
    for b in pages.PAGES[slug]['blocks']:
        kind = b[0]
        if kind == 'h':
            out.append(f'<h2 class="page-h">{e(b[1][k])}</h2>')
        elif kind == 'p':
            out.append(f'<p>{e(b[1][k])}</p>')
        elif kind == 'ul':
            out.append('<ul class="page-list">' + ''.join(f'<li>{e(x[k])}</li>' for x in b[1]) + '</ul>')
        elif kind == 'note':
            out.append(f'<p class="page-note"><i class="fa-solid fa-circle-info" aria-hidden="true"></i> {e(b[1][k])}</p>')
        elif kind == 'cards':
            out.append('<div class="info-cards">' + ''.join(
                f'<div class="info-card"><i class="fa-solid {ic}" aria-hidden="true"></i><h3>{e(ti[k])}</h3><p>{e(de[k])}</p></div>' for ic, ti, de in b[1]) + '</div>')
        elif kind == 'steps':
            out.append('<ol class="steps">' + ''.join(
                f'<li><span class="step-no">{n}</span><div><h3>{e(ti[k])}</h3><p>{e(de[k])}</p></div></li>' for n, (ti, de) in enumerate(b[1], 1)) + '</ol>')
        elif kind == 'jobs':
            out.append('<div class="info-cards jobs">' + ''.join(
                f'<div class="info-card"><i class="fa-solid fa-briefcase" aria-hidden="true"></i><h3>{e(ti[k])}</h3><p>{e(de[k])}</p></div>' for ti, de in b[1]) + '</div>')
        elif kind == 'tours':
            out.append(tours_block(b[1]))
        elif kind == 'posts':
            items = NEWS if b[1] == 'all' else [p for p in NEWS if p['cat'].startswith('Cẩm nang du lịch')]
            out.append(f'<div class="list-post post-grid">{post_cards(items)}</div>')
        elif kind == 'contact':
            out.append(contact_block(k))
        elif kind == 'contact_cta':
            out.append(f'<p><a class="button primary" href="contact.html">{("お問い合わせはこちら", "문의하기")[k]}</a></p>')
        elif kind == 'pay':
            out.append('<div class="payment-img"><img src="images/thanhtoan.jpg" width="418" height="62" alt="Chấp nhận thanh toán" loading="lazy"></div>')
    return '\n'.join(out)


def sub_main(slug, lang):
    pg = pages.PAGES[slug]
    k = 0 if lang == 'ja' else 1
    return f'''
<main id="main">
  <section class="section page-hero">
    <div class="section-content">
      <div class="row row-small">
        <div class="col small-12 large-12"><div class="col-inner">
          <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Trang chủ</a> <i class="fa-solid fa-chevron-right" aria-hidden="true"></i> <span>{pg['title']}</span></nav>
          <h1>{pg['title']}</h1>
          <p class="lead">{e(pg['lead'][k])}</p>
        </div></div>
      </div>
    </div>
  </section>
  <section class="section page-body">
    <div class="section-content">
      <div class="row row-small">
        <div class="col small-12 large-12"><div class="col-inner">
{sub_blocks(slug, lang)}
        </div></div>
      </div>
    </div>
  </section>
</main>'''


HOME_DESC = 'Khánh An Tourism — tour Đà Nẵng – Hội An – Huế, đưa đón và hướng dẫn viên tiếng Nhật, tiếng Hàn.'
HOME = finish(shell(main_content(), 'Khánh An Tourism - Trang chủ', HOME_DESC))

# Trang chỉ có tiếng Nhật (mặc định) và tiếng Hàn
for lang, conf in i18n.LANGS.items():
    jobs = [(None, localize(HOME, lang), HOME_DESC)]
    for slug, pg in pages.PAGES.items():
        k = 0 if lang == 'ja' else 1
        ttl = i18n.TR[pg['title']][lang] + ' - Khánh An Tourism'
        jobs.append((slug, localize(finish(shell(sub_main(slug, lang), ttl, e(pg['lead'][k]))), lang, slug), None))
    for slug, page, _ in jobs:
        out = i18n.render(page, lang, slug)
        name = i18n.page_file(lang, slug)
        (ROOT / name).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / name).write_text(out, encoding='utf8')
        print(f'{name}: {len(out)} bytes')
        for x in i18n.leftovers(out):
            print(f'  [{name}] chưa dịch: {x[:90]}')
