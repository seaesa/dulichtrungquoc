// Đối chiếu box & style giữa bản gốc và bản clone (chạy qua Playwright browser_run_code, filename=scripts/compare.js)
async (page) => {
  const pairs = [["#top-bar", "#top-bar"], [".header-top .nav-left li:first-child a", ".header-top .header-contact li:first-child a"], [".top-bar-nav > li:first-child > a", ".top-bar-nav > li:first-child > a"], [".top-bar-nav .header-cart-title", ".top-bar-nav .header-cart-title"], ["#logo img", "#logo img"], [".header-nav-main.nav-right > li:first-child > a", ".header-nav-main > li:first-child > a"], ["#menu-item-44 > a", ".header-nav-main > li.has-dropdown > a"], [".header-search > a", ".header-search > a"], [".slider-section", ".hero"], [".section1", ".section1"], [".section2", ".section2"], [".section2 h2", ".section2 h2"], [".slider-danh-muc .flickity-viewport", ".slider-danh-muc .slider-viewport"], [".slider-danh-muc .box-image", ".slider-danh-muc .box-image"], [".slider-danh-muc h3", ".slider-danh-muc h3"], [".slider-danh-muc p", ".slider-danh-muc .box-text p"], [".section3", ".section3"], [".section3 h2", ".section3 h2"], [".section3 .flickity-viewport", ".section3 .slider-viewport"], [".section3 .box-image", ".section3 .box-image"], [".section3 .box-ngay-khoi-hanh", ".section3 .box-ngay-khoi-hanh"], [".section3 .box-text", ".section3 .box-text"], [".section3 .product-title a", ".section3 .product-title a"], [".section3 .ma-tour", ".section3 .ma-tour"], [".section3 .khoi-hanh", ".section3 .khoi-hanh"], [".section3 .price-wrapper", ".section3 .price-wrapper"], [".section3 .amount", ".section3 .amount"], [".section3 .box-nguoi-lien-he", ".section3 .box-nguoi-lien-he"], [".section3 .add-to-cart-button a", ".section3 .add-to-cart-button a"], [".section4", ".section4"], [".section4 h2", ".section4 h2"], [".section4 .icon-box", ".section4 .icon-box"], [".section4 .icon-box svg", ".section4 .icon-box svg"], [".section4 .icon-box h3", ".section4 .icon-box h3"], [".section4 .icon-box p", ".section4 .icon-box p"], [".section5", ".section5"], [".section5 .cot1 > .col-inner", ".section5 .svc > .col-inner"], [".section5 .cot1 svg", ".section5 .svc svg"], [".section5 .cot1 h3", ".section5 .svc h3"], [".section5 .cot1 p", ".section5 .svc p"], [".section9", ".section9"], [".section9 .large-7 img", ".section9 .large-7 img"], [".section9 .large-5 img", ".section9 .large-5 img"], [".section10", ".section10"], [".sec_customer p", ".section10 .lead"], [".section10 blockquote", ".section10 blockquote"], [".section10 .icon-box-img img", ".section10 .icon-box-img img"], [".section10 h3", ".section10 .icon-box h3"], [".section10 .fa-star", ".section10 .fa-star"], [".section11", ".section11"], [".section11 .row-collapse > .large-8 > .col-inner", ".section11 .zalo-box"], [".section11 .large-8 .large-4 img", ".section11 .phone-col img"], [".section11 h2", ".section11 h2"], [".section11 input[type=email]", ".section11 input[type=email]"], [".section11 input[type=submit]", ".section11 input[type=submit]"], [".section11 .row-divided > .large-4 img", ".section11 .qr-col img"], [".section12", ".section12"], [".section12 .flickity-viewport", ".section12 .slider-viewport"], [".section12 .image-cover", ".section12 .image-cover"], [".section12 .cat-label", ".section12 .cat-label"], [".section12 .post-title", ".section12 .post-title"], [".footer-section", ".footer-section"], [".footer-section h3", ".footer-section h3"], [".footer-section .large-5 p", ".footer-section .large-5 p"], [".footer-section ul li a", ".footer-section ul li a"], [".footer-section input[type=email]", ".footer-section input[type=email]"], [".footer-section .social-icons a", ".footer-section .social-icons a"], [".footer-section .img-inner img", ".footer-section .payment-img img"], [".absolute-footer", ".absolute-footer"], [".copyright-footer", ".copyright-footer"]];
  const W = (await page.viewportSize()).width;
  const ctx = page.context();
  const measure = async (url, sels) => {
    const p = await ctx.newPage();
    await p.setViewportSize({ width: W, height: 900 });
    await p.goto(url);
    await p.waitForTimeout(1200);
    for (let y = 0; y < 12000; y += 600) { await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(60); }
    await p.evaluate(() => window.scrollTo(0, 0));
    await p.waitForTimeout(1500);
    const r = await p.evaluate((sels) => sels.map(s => {
      const el = [...document.querySelectorAll(s)].find(e => { const b = e.getBoundingClientRect(); return b.width > 0 && b.height > 0 && b.left >= -5 && b.left < innerWidth; });
      if (!el) return null;
      const b = el.getBoundingClientRect(); const cs = getComputedStyle(el);
      return { y: Math.round(b.top + scrollY), x: Math.round(b.left), w: Math.round(b.width * 10) / 10, h: Math.round(b.height * 10) / 10, fs: cs.fontSize, lh: cs.lineHeight, fw: cs.fontWeight, c: cs.color };
    }), sels);
    await p.close();
    return r;
  };
  const a = await measure('https://dulich2.themedep.top/', pairs.map(p => p[0]));
  const b = await measure('http://localhost:8765/', pairs.map(p => p[1]));
  const out = [];
  pairs.forEach((p, i) => {
    const A = a[i], B = b[i];
    if (!A || !B) { out.push(`${p[1]}: MISSING orig=${!!A} clone=${!!B}`); return; }
    const d = [];
    ['y', 'x', 'w', 'h'].forEach(k => { if (Math.abs(A[k] - B[k]) > 1.5) d.push(`${k} ${A[k]}→${B[k]}`); });
    ['fs', 'lh', 'fw', 'c'].forEach(k => { if (A[k] !== B[k]) d.push(`${k} ${A[k]}→${B[k]}`); });
    out.push(`${d.length ? '✗' : '✓'} ${p[1]}${d.length ? ': ' + d.join(', ') : ''}`);
  });
  return `W=${W}\n` + out.join('\n');
}
