# Behaviors — dulich2.themedep.top (trang chủ)

Theme gốc: WordPress Flatsome 3.16 + WooCommerce. Không có Lenis/Locomotive, scroll native.
Breakpoints Flatsome: small ≤549px, medium 550–849px, large ≥850px.

## Header
- **Sticky (scroll-driven):** `.header-wrapper` thêm class `stuck` khi `scrollY >= chiều cao #header` (112px desktop, 138px mobile).
  - stuck: `position:fixed; top:0; left:0; right:0`, top-bar ẩn (`display:none`), `.header-main` height 74→70px (mobile 70), logo max-height 70px.
  - animation `stuckMoveDown 0.6s ease` (translateY(-100%) → 0). Khi về top: bỏ class, không animation.
  - `#header` giữ nguyên chiều cao (placeholder) để nội dung không nhảy.
- **Nav hover:** link `#003594 → #89c440`, transition 0.2s. Top-bar link trắng → `#89c440`.
- **Dropdown "Tour du lịch" / search / giỏ hàng (hover):** `opacity 0→1, visibility`, transition `opacity .25s, visibility .25s`; ẩn bằng `left:-99999px` (ẩn tức thì khi rời chuột).
  - Box: nền trắng, radius 10px, padding 20px 0, min-width 260px, shadow `1px 1px 15px rgba(0,0,0,.15)`.
  - Item: padding 10px 5px 10px 10px, margin 0 10px, radius 10px, color rgba(102,102,102,.85), 16px/500. Hover: bg `#003594`, chữ trắng.
- **Back-to-top** (chỉ ≥850px): hiện khi `scrollY > innerHeight`: `opacity 0→1, translateY(30%)→0`, transition .3s. Click → cuộn mượt lên đầu.

## Mobile menu (≤849px, off-canvas trái)
- Click icon hamburger → overlay `#1e73be` opacity 0→0.6 (.25s); panel trượt từ trái `translateX(-270px)→0` (.2s), nền `#003594`, width 330px (≤549) / 270px (550–849), padding 15px (≤549).
- Nút đóng X (svg 28px) fixed góc phải trên, opacity .6, hover 1. Click overlay / X / Esc → đóng (overlay fade .25s, panel ẩn ngay).
- Item: uppercase 15px/500, rgba(255,255,255,.8), padding 15px 0 15px 20px; viền trên rgba(255,255,255,.2); hover/active bg rgba(0,0,0,.05).
- "Tour du lịch" có nút toggle (angle-down, opacity .6, width 45px): click → li.active, submenu hiện (opacity 0→1, translateX(-10px)→0, .3s), toggle xoay -180deg (.3s).

## Sliders (Flickity — tự viết lại bằng vanilla JS cùng physics)
| Slider | cell | align | group | autoplay | attraction/friction | drag threshold |
|---|---|---|---|---|---|---|
| Hero banner | 100% (2 ảnh) | center | không | 6000ms | 0.1 / 0.6 | 10 |
| Bạn muốn đi đâu ×2 | 25% (≤549: 70%), track lệch left 12.5% (≤549: -15%) | center | không | 4000ms | 0.1 / 0.6 | 10 |
| Tour ×4 | 33.33% (≤849: 50%, ≤549: 70%) | left | 100% | 4000ms | 0.025 / 0.28 | 5 |
| Tin tức | 33.33% (550–849: 100%, ≤549: 70%) | left | 100% | không | 0.025 / 0.28 | 5 |
- Tất cả: wrapAround, pauseAutoPlayOnHover, dừng autoplay vĩnh viễn khi người dùng kéo/bấm mũi tên.
- **Mũi tên:** mặc định opacity 0, translateX(±20%); hover slider → opacity .7, translateX(0); hover nút → opacity 1, fill `#003594`. SVG 36px nền trắng tròn, shadow `2px 2px 20px rgba(0,0,0,.19)`. Transition .3s.
  - ≥850 & slider-nav-outside (đi đâu / tour / tin tức): mũi tên nằm ngoài viewport (`right:100%` / `left:100%`).
  - Tour/Tin tức: `margin-top:-10%` (slider-nav-push). Đi đâu: `top:6%`.
  - ≤549: hero & đi đâu ẩn mũi tên; tour/tin tức: luôn hiện opacity .8, width 20px, svg padding 3px.

## Hover
- Thẻ "đi đâu": overlay trắng rgba(255,255,255,.343) fade-in (opacity .6s); box-image shadow `1px 1px 7px #ccc` (.3s).
- Thẻ tour: card shadow `2px 2px 20px #8080804f` (tức thì); overlay trắng fade-in .6s; tiêu đề `#003594→#89c440`; nút "Đặt tour" bg `#89c440→#146c43` (.3s).
- "Vì sao chọn": box bg `#fefefe→#89c440`, text trắng (h3 & svg giữ `#003594`), shadow `1px 1px 7px #ccc` (.3s).
- Khoảnh khắc: ảnh (trừ ảnh thứ 3) zoom scale(1.1) trong .6s.
- Footer link `#333→#89c440`. Social & nút Gửi: `box-shadow: inset 0 0 0 100px rgba(0,0,0,.2)`.

## Không có
- Không có animation xuất hiện khi scroll (không có data-animate). Ảnh lazy-load (hiện khi tải xong).

## Tuỳ biến: Banner Đà Nẵng (thay hero gốc)
- Nội dung & icon: `scripts/danang_banner.py` → chạy `python3 scripts/build-html.py`. Ảnh: `images/danang/` (nguồn/giấy phép trong `CREDITS.json`, có ghi nguồn trên từng slide).
- Dải biểu tượng: CSS animation `dn-marquee` 40s chạy vô hạn (danh sách nhân đôi, dịch -50%), dừng khi hover/focus; tắt khi prefers-reduced-motion.
- Bấm biểu tượng hoặc dot → nhảy tới slide tương ứng và dừng autoplay; biểu tượng/dot của slide hiện tại được tô xanh lá.
- Slider địa điểm: autoplay 6s, kéo/vuốt, ảnh zoom chậm (Ken Burns 7s), nội dung thẻ hiện lần lượt. ≤849px ẩn mũi tên.

## Tuỳ biến: Đa ngôn ngữ, LINE, thương hiệu
- Chỉ có 2 ngôn ngữ: tiếng Nhật (mặc định, `index.html`) và tiếng Hàn (`ko.html`). Build dựng trang tiếng Việt rồi `scripts/i18n.py` dịch theo bảng `TR`; build in ra đoạn nào chưa dịch.
- Chuyển ngôn ngữ: dropdown ở top bar (desktop), nút viên ở top bar mobile và cuối menu off-canvas. Thông báo form trong `js/main.js` (`MSGS`) theo `<html lang>`.
- Khối Zalo → LINE: màn hình điện thoại LINE dựng bằng HTML/CSS (`line_phone()`), QR thật ở `images/line-qr.jpg`.
- Tên công ty Khánh An Tourist; logo gốc `logo.png` → biểu tượng header `images/logo-emblem.png` + chữ, logo đầy đủ ở footer `images/logo-khanh-an.jpg`, favicon cắt từ logo. Đã bỏ giỏ hàng.
- Link tới trang chưa làm đều là `href="#"` và bị chặn trong JS (không chuyển trang).
- Tour golf (`#tour-golf`) và du thuyền (`#tour-du-thuyen`): dữ liệu mẫu trong `EXTRA_TOURS` (build-html.py), ảnh ở `images/tours/` (nguồn/giấy phép trong `CREDITS.json`, ghi nguồn dưới mỗi mục). Menu "Tour du lịch" có link tới 2 mục này; menu mobile tự đóng khi bấm.
- "Bạn muốn đi đâu" (khách inbound): 2 hàng — điểm nổi tiếng Đà Nẵng (`images/danang/`) và lăng tẩm Huế (`images/hue/`, ghi nguồn). Dữ liệu `DESTS` trong build-html.py.
- Tour lặn biển `#tour-lan-bien` (dữ liệu mẫu trong `EXTRA_TOURS`).
