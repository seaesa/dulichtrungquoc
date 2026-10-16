#!/usr/bin/env python3
"""Sinh index.html tĩnh từ dữ liệu đã trích xuất (docs/research/content.json, icons.json).

Chạy: python3 scripts/build-html.py
"""
import html
import json
import re
from pathlib import Path

from danang_banner import banner
import i18n

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / 'docs/research/content.json').read_text(encoding='utf8'))
ICONS = json.loads((ROOT / 'docs/research/icons.json').read_text(encoding='utf8'))
SITE = 'https://dulich2.themedep.top'

e = html.escape


def img(url):
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
          <div class="slider slider-nav-outside" data-slider='{{"cellAlign":"center","autoPlay":4000,"adaptiveHeight":true,"attraction":0.1,"friction":0.6,"dragThreshold":10}}'>
            <div class="slider-viewport"><div class="slider-track">{cells}
            </div></div>
            {ARROWS}
          </div>
        </div>'''


def tour_card(p):
    href = p['href']
    return f'''
          <div class="tour-cell">
            <div class="col-inner">
              <div class="product-small box has-hover box-text-bottom">
                <div class="box-image">
                  <div class="image-overlay-add image-cover">
                    <a href="{href}" aria-label="{e(p['title'])}">{lazy(p['img'], p['title'])}</a>
                    <div class="overlay"></div>
                  </div>
                  <span class="box-ngay-khoi-hanh"><i class="fa-solid fa-calendar-days" aria-hidden="true"></i> Khởi hành hàng tuần</span>
                </div>
                <div class="box-text">
                  <div class="title-wrapper"><p class="product-title"><a href="{href}">{e(p['title'])}</a></p></div>
                  <div class="thong-tin-sp">
                    <div class="ma-tour"><span class="label"><i class="fa-solid fa-qrcode"></i> Mã tour: </span><span class="value">{e(p['ma'])}</span></div>
                    <div class="khoi-hanh"><span class="label"><i class="fa-solid fa-location-dot" aria-hidden="true"></i> Khởi hành: </span><span class="value">{e(p['kh'])} </span></div>
                  </div>
                  <div class="price-wrapper"><span class="price"><span class="amount">{e(p['price'])}&nbsp;<span class="currency">&#8363;</span></span><span class="price-suffix">/khách</span></span></div>
                  <div class="box-nguoi-lien-he"><i class="fa-solid fa-user" aria-hidden="true"></i> <span class="value">{e(p['lh'])}</span><span class="label"> đã liên hệ</span></div>
                  <div class="add-to-cart-button"><a href="{p['cart']}" rel="nofollow">Đặt Tour</a></div>
                </div>
              </div>
            </div>
          </div>'''


def tour_section(block, first=False):
    plain, strong = block['title'].split(' ', 1)
    cards = ''.join(tour_card(p) for p in block['prods'])
    return f'''
  <section class="section section3{' pb-30' if first else ''}">
    <div class="section-content">
      <div class="row row-small">
        <div class="col small-12 large-12"><div class="col-inner">
          {title(plain, strong)}
          <div class="slider row-slider tour-slider slider-nav-outside slider-nav-push" data-slider='{{"cellAlign":"left","groupCells":true,"autoPlay":4000,"dragThreshold":5,"equalize":".box-text"}}'>
            <div class="slider-viewport"><div class="slider-track">{cards}
            </div></div>
            {ARROWS}
          </div>
        </div></div>
      </div>
    </div>
  </section>'''


WHY = [
    ('TOP 1', 'Dịch vụ Tour nội địa và quốc tế'),
    ('TOP 5', 'Công ty lữ hành tại Việt Nam'),
    ('TOP 7', 'các đơn vị làm VISA nước ngoài'),
    ('ĐẶT TOUR', 'Dễ dàng nhanh chóng chỉ 3 bước'),
    ('THANH TOÁN', 'Đơn giản, an toàn và linh hoạt'),
    ('HOTLINE', '0982 277 493 Trực tuyến 24/7'),
]
SERVICES = [
    ('#fd6666', 'Hội chợ quốc tế', 'Chuyên tour hội chợ quốc tế các nước trên thế giới'),
    ('#003594', 'Sim quốc tế', 'Bán sim nghe gọi &amp; data các nước trên thế giới'),
    ('#fd8008', 'VISA', 'Dịch vụ Visa nhanh, rẻ. Visa trọn gói, thủ tục đơn giản'),
    ('#89c440', 'Vé máy bay', 'Vé máy bay giá rẻ nhất, nhiều khuyến mãi hấp dẫn'),
]
MOMENTS = [
    ('8655-7e9b-4f2e-a427-18087594164f_1704267988.jpg', True),
    ('kinh-nghiem-du-lich-thanh-do-trung-quoc-day-du-chi-tiet-nhat-5ffd498ad1d5f_1704267988.jpg', False),
    ('dia-diem-du-lich-thai-lan-1.jpg', True),
]
TESTIMONIALS = [
    ('Lại một lần nữa công ty SANSHIN đồng hành cùng Khánh An Tourist trong chuyến du lịch Hạ Long. Mọi thứ đều tốt đẹp, hướng dẫn viên “anh Thành” luôn chu đáo từng bữa ăn, từng chỗ ngủ trong khách sạn, đoàn chúng tôi luôn an tâm khi đi cùng Khánh An Tourist trong mọi chuyến du lịch trong và ngoài nước. Khánh An Tourist luôn trong suy nghĩ đầu tiên của chúng tôi trong mỗi lần có ý định đi du lịch. Cảm ơn Khánh An Tourist đã nhiệt tình hỗ trợ hết mình',
     'Screenshot-2024-03-18-130615.png', 'Công ty TNHH SANSHIN Hà Nội', 'Tour Hạ Long náo nhiệt'),
    ('Chúng tôi du lịch tới đảo Phú Quốc xinh đẹp. Được đồng hành cùng công ty du lịch Khánh An Tourist. Chúng tôi thấy được quan tâm chăm sóc tận tình từng bữa ăn giấc ngủ khi đi du lịch. Hướng dẫn viên của công ty Khánh An Tourist chu đáo, tận tình. Trước ngày đi chúng tôi còn được công ty thông báo đến từng người giờ khởi hành và những thứ cần chuẩn bị. Công ty Khánh An Tourist sẽ là lựa chọn tin tưởng nhất cho những chuyến du lịch lần sau.',
     'Screenshot-2024-03-18-130622.png', 'Nguyễn Khả Tâm', 'Cảm nhận về tour Phú Quốc do công ty tổ chức'),
]
NAV = [
    ('Trang chủ', 'http://dulich2.khothemewp.vn/'),
    ('Giới thiệu', SITE + '/gioi-thieu/'),
    ('Tour du lịch', SITE + '/tour/'),
    ('Cẩm nang du lịch', SITE + '/cam-nang-du-lich/'),
    ('Visa du lịch', '#'),
    ('Tin tức', SITE + '/tin-tuc/'),
    ('Liên hệ', SITE + '/lien-he/'),
]
SUBNAV = [('Tour nước ngoài', SITE + '/tour-nuoc-ngoai/'), ('Tour trong nước', SITE + '/tour-trong-nuoc/')]


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


BRAND_MARK = ('<svg class="brand-mark" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="22" fill="#003594"/>'
              '<path d="M7 33l10-12 7 8 6-6 11 10z" fill="#89c440"/><circle cx="33" cy="15" r="4" fill="#ffd257"/>'
              '<path d="M9 37q15-6 30 0" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/></svg>')


def header():
    contact = '''<li><a href="mailto:truongvutienphuoc@gmail.com"><i class="icon-envelop"></i><span>truongvutienphuoc@gmail.com</span></a></li>
              <li><a href="tel:0982277493"><i class="icon-phone"></i><span>0982 277 493</span></a></li>'''
    main_nav = []
    for label, href in NAV:
        if label == 'Tour du lịch':
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
            <li><a href="#"><img class="ux-menu-icon" src="images/user-id-svgrepo-com.svg" width="22" height="22" alt="">Tuyển dụng</a></li>
            <li><a href="{SITE}/huong-dan-thanh-toan/"><img class="ux-menu-icon" src="images/pay-svgrepo-com.svg" width="22" height="22" alt="">Hướng dẫn thanh toán</a></li>
            <li><a href="{SITE}/lien-he/"><img class="ux-menu-icon" src="images/contact-us-svgrepo-com.svg" width="22" height="22" alt="">Liên hệ</a></li>
            <li class="has-dropdown"><a href="{SITE}/gio-hang/" class="header-cart-link"><span class="header-cart-title">Giỏ hàng</span><i class="icon-shopping-cart"></i></a>
              <ul class="nav-dropdown"><li class="html"><p class="mini-cart-empty">Chưa có sản phẩm trong giỏ hàng.</p></li></ul>
            </li>
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
          <a href="./" title="Khánh An Tourist" rel="home" class="brand">{BRAND_MARK}<span class="brand-text"><strong>KHÁNH AN</strong><small>TOURIST</small></span></a>
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
          <ul class="nav nav-right mobile-nav">
            <li><a href="{SITE}/gio-hang/" aria-label="Giỏ hàng"><i class="icon-shopping-cart"></i></a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</header>'''


def offcanvas():
    items = []
    for label, href in NAV:
        if label == 'Tour du lịch':
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
                      <div class="lp-bar"><i class="fa-solid fa-chevron-left"></i><span>Khánh An Tourist</span><i class="fa-solid fa-ellipsis"></i></div>
                      <div class="lp-cover"><img src="images/danang/thumbs/cau-vang.jpg" alt="" loading="lazy"></div>
                      <div class="lp-profile">
                        <span class="lp-avatar">''' + BRAND_MARK + '''</span>
                        <strong>Khánh An Tourist <i class="fa-solid fa-circle-check"></i></strong>
                        <small>Tài khoản chính thức</small>
                      </div>
                      <span class="lp-add"><i class="fa-solid fa-user-plus"></i> Kết bạn</span>
                      <ul class="lp-info">
                        <li><i class="fa-solid fa-phone"></i> 0982 277 493</li>
                        <li><i class="fa-regular fa-clock"></i> 8:00 – 18:00</li>
                        <li><i class="fa-solid fa-ticket"></i> Ưu đãi cho bạn bè LINE</li>
                      </ul>
                    </div>
                  </div>'''


def main_content():
    s2 = DATA['section2']
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
                <div class="img has-hover"><div class="img-inner{' image-zoom' if zoom else ''} image-cover" style="padding-top:75%;">{lazy(f'/{f}')}</div></div>
              </div></div>''' for f, zoom in [('phuquoc.jpg', True)] + MOMENTS)
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
    posts = ''.join(f'''
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
          </div>''' for p in DATA['section12'])

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
          {destination_slider(s2[0])}
          <div class="gap-15 hide-for-small"></div>
          {destination_slider(s2[1])}
        </div></div>
      </div>
    </div>
  </section>

  {tour_section(tours[0], first=True)}

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

  {tour_section(tours[1])}
  {tour_section(tours[2])}
  {tour_section(tours[3])}

  <!-- section9: Khoảnh khắc đẹp nhất -->
  <section class="section section9">
    <div class="section-content">
      <div class="row row-small">
        <div class="col small-12 large-12"><div class="col-inner">
          {title('KHOẢNH KHẮC', 'ĐẸP NHẤT')}
        </div></div>
        <div class="col medium-7 small-12 large-7"><div class="col-inner">
          <div class="img has-hover"><div class="img-inner image-zoom image-cover" style="padding-top:53.7%;">{lazy('/dai-loan.jpg')}</div></div>
        </div></div>
        <div class="col medium-5 small-12 large-5"><div class="col-inner">
          <div class="row row-small">{moments}
          </div>
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
                      <img class="line-qr" src="images/line-qr.jpg" width="644" height="645" alt="Mã QR LINE Khánh An Tourist" loading="lazy">
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
          <p class="lead">Chia sẽ những thông tin du lịch triển lãm nhanh nhất &amp; những bí quyết khi tham gia tour hội chợ</p>
          <div class="gap-10"></div>
          <div class="slider row-slider list-post slider-nav-outside slider-nav-push" data-slider='{{"cellAlign":"left","groupCells":true,"autoPlay":0,"dragThreshold":5}}'>
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
          <h3>KHÁNH AN TOURIST</h3>
          <p><strong>📍 Địa chỉ</strong>: Tòa nhà Tuấn Hạnh, Số 832, Ngõ 1126, Phố Nhân Hòa, Phường Nhân Chính, Quận Thanh Xuân, Hà Nội, Việt Nam</p>
          <p><strong>🏠 Chi nhánh Hoà Bình</strong>: Số 2430, Điện Biên Phủ, Phương Lâm, Hòa Bình</p>
          <p><strong>🏠 Chi nhánh Hải Phòng</strong>: Số 1235, Bặch Đằng, Thủy Nguyên, Hải Phòng</p>
          <p><strong>🏠 Chi nhánh Nam Định</strong>: D12P317 ngõ 189 Trần Huy Liệu, Phường Văn Miếu, Thành Phố Nam Định</p>
          <p><strong>☎️ Hotline</strong>: <a href="tel:0982277493">0982 277 493</a></p>
          <p><strong>💬 Zalo</strong>: <a href="https://zalo.me/0982277493" target="_blank" rel="noopener">0982 277 493</a></p>
          <p><strong>✉️ Email</strong>: <a href="mailto:truongvutienphuoc@gmail.com">truongvutienphuoc@gmail.com</a></p>
        </div></div>
        <div class="col medium-7 small-12 large-7"><div class="col-inner">
          <div class="row row-small">
            <div class="col medium-4 small-12 large-4"><div class="col-inner">
              <h3>THÔNG TIN CẦN BIẾT</h3>
              <ul>
                <li><a href="{SITE}/gioi-thieu">Giới thiệu</a></li>
                <li><a href="{SITE}/lien-he">Liên hệ</a></li>
                <li><a href="#">Hình thức thanh toán</a></li>
                <li><a href="#">Chính sách hoàn hủy</a></li>
                <li><a href="#">Chính sách bảo mật</a></li>
                <li><a href="#">Điều khoản giao dịch</a></li>
              </ul>
            </div></div>
            <div class="col hide-for-small medium-4 small-12 large-4"><div class="col-inner">
              <h3>CHỨNG NHẬN</h3>
            </div></div>
            <div class="col medium-4 small-12 large-4"><div class="col-inner">
              <h3>ĐĂNG KÝ NHẬN BẢN TIN</h3>
              <p>Nhập địa chỉ email để nhận thông tin mới nhất từ chúng tôi.</p>
              {email_form('email-footer')}
            </div></div>
          </div>
        </div></div>
        <div class="col hide-for-small medium-5 small-12 large-5"><div class="col-inner">
          <p>Giấy phép kinh doanh số 01033619401 do sở KH&amp;ĐT TP abc cấp ngày 21/23 năm 2323<br>Giấy phép Kinh doanh Lữ hành Quốc tế số 01711D/S2015/TCDL-GPLHabc</p>
        </div></div>
        <div class="col hide-for-small medium-7 small-12 large-7"><div class="col-inner">
          <div class="row row-small">
            <div class="col medium-4 small-12 large-4"><div class="col-inner">
              <h3>Kết nối với chúng tôi</h3>
              <div class="social-icons">
                <a href="http://url" target="_blank" rel="noopener nofollow" class="button icon facebook" title="Follow on Facebook" aria-label="Follow on Facebook"><i class="icon-facebook"></i></a><a href="http://url" target="_blank" rel="noopener nofollow" class="button icon instagram" title="Follow on Instagram" aria-label="Follow on Instagram"><i class="icon-instagram"></i></a><a href="http://url" target="_blank" rel="noopener nofollow" class="button icon twitter" title="Follow on Twitter" aria-label="Follow on Twitter"><i class="icon-twitter"></i></a><a href="mailto:truongvutienphuoc@gmail.com" target="_blank" rel="nofollow" class="button icon email" title="Send us an email" aria-label="Send us an email"><i class="icon-envelop"></i></a>
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
        <div class="copyright-footer">Copyright 2026 © Khánh An Tourist</div>
      </div>
    </div>
  </div>
  <a href="#top" class="back-to-top hide-for-medium" aria-label="Go to top"><i class="icon-angle-up"></i></a>
</footer>'''


PAGE = f'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Khánh An Tourist - Trang chủ</title>
<meta name="description" content="Khánh An Tourist — tour trong nước, tour nước ngoài, visa, vé máy bay.">
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
{main_content()}
{footer()}
{offcanvas()}
<script src="js/main.js"></script>
</body>
</html>
'''

# Các trang con chưa làm: không dẫn đi đâu (không chuyển về web gốc). JS chặn click vào href="#".
PAGE = re.sub(r'href="(?:https?://(?:dulich2\.themedep\.top|dulich2\.khothemewp\.vn|khothemewp\.vn)[^"]*|http://url|\?add-to-cart=\d+)"', 'href="#"', PAGE)
PAGE = PAGE.replace(f'action="{SITE}/"', 'action="#"')

# Trang chỉ có tiếng Nhật (mặc định, index.html) và tiếng Trung (zh.html)
for lang, conf in i18n.LANGS.items():
    out = i18n.render(PAGE, lang)
    (ROOT / conf['file']).write_text(out, encoding='utf8')
    print(f"{conf['file']}: {len(out)} bytes")
    for t in i18n.leftovers(out):
        print(f'  [{lang}] chưa dịch: {t[:90]}')
