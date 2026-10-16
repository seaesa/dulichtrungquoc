/* Clone trang chủ dulich2.themedep.top — vanilla JS */
(function () {
  'use strict';

  var MQ_LARGE = window.matchMedia('(min-width: 850px)');
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ------------------------------------------------------------------
   * Lazy-load ảnh theo section (giống flatsome-lazy-load)
   * ------------------------------------------------------------------ */
  function loadImages(root) {
    root.querySelectorAll('img[data-src]').forEach(function (img) {
      img.src = img.getAttribute('data-src');
      img.removeAttribute('data-src');
    });
  }
  var lazyRoots = document.querySelectorAll('main > section, main > .slider-wrapper, footer');
  if ('IntersectionObserver' in window) {
    var lazyIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          loadImages(entry.target);
          lazyIO.unobserve(entry.target);
        }
      });
    }, { rootMargin: '300px 0px' });
    lazyRoots.forEach(function (el) { lazyIO.observe(el); });
  } else {
    loadImages(document);
  }

  /* ------------------------------------------------------------------
   * Slider — tái hiện Flickity (wrapAround, physics attraction/friction,
   * groupCells, autoplay, drag, adaptiveHeight)
   * ------------------------------------------------------------------ */
  function Slider(el) {
    var opts = JSON.parse(el.getAttribute('data-slider') || '{}');
    this.el = el;
    el._slider = this;
    this.opts = {
      cellAlign: opts.cellAlign || 'center',
      groupCells: !!opts.groupCells,
      autoPlay: opts.autoPlay || 0,
      adaptiveHeight: !!opts.adaptiveHeight,
      attraction: opts.attraction || 0.025,
      friction: opts.friction || 0.28,
      dragThreshold: opts.dragThreshold || 3,
      equalize: opts.equalize || null
    };
    this.viewport = el.querySelector('.slider-viewport');
    this.track = el.querySelector('.slider-track');
    this.cells = Array.prototype.slice.call(this.track.children);
    this.x = 0;
    this.velocity = 0;
    this.selectedIndex = 0;
    this.isAnimating = false;
    this.isPointerDown = false;
    this.playerStopped = false;
    this.hovered = false;
    el.classList.add('is-draggable');
    if (this.opts.adaptiveHeight) el.classList.add('is-adaptive');
    this.bind();
    this.layout();
    this.x = this.targetFor(0);
    this.render();
    this.markSelected();
    this.play();
  }

  Slider.prototype.align = function () {
    return this.opts.cellAlign === 'left' ? 0 : 0.5;
  };

  Slider.prototype.layout = function () {
    var self = this;
    if (this.opts.equalize) {
      var boxes = this.track.querySelectorAll(this.opts.equalize);
      boxes.forEach(function (b) { b.style.height = ''; });
      var max = 0;
      boxes.forEach(function (b) { max = Math.max(max, b.getBoundingClientRect().height); });
      boxes.forEach(function (b) { b.style.height = max + 'px'; });
    }
    this.vw = this.viewport.clientWidth;
    // khoảng lệch của track (left: 12.5% / -15% ...) tính theo px
    this.trackOffset = this.track.offsetLeft;
    var pos = 0;
    this.cellX = [];
    this.cellW = [];
    this.cells.forEach(function (cell) {
      var w = cell.getBoundingClientRect().width;
      self.cellX.push(pos);
      self.cellW.push(w);
      pos += w;
    });
    this.total = pos;
    // slides (nhóm cell)
    this.slides = [];
    var current = null;
    this.cells.forEach(function (cell, i) {
      var w = self.cellW[i];
      if (!current || !self.opts.groupCells || (current.width + w > self.vw + 1)) {
        current = { first: i, cells: [i], x: self.cellX[i], width: w };
        self.slides.push(current);
      } else {
        current.cells.push(i);
        current.width += w;
      }
    });
    var a = this.align();
    this.slides.forEach(function (s) {
      s.target = self.vw * a - (s.x + s.width * a);
    });
    if (this.selectedIndex >= this.slides.length) this.selectedIndex = this.slides.length - 1;
    this.updateHeight();
  };

  Slider.prototype.updateHeight = function () {
    var self = this;
    var h = 0;
    if (this.opts.adaptiveHeight) {
      var slide = this.slides[this.selectedIndex];
      slide.cells.forEach(function (i) { h = Math.max(h, self.cells[i].getBoundingClientRect().height); });
    } else {
      this.cells.forEach(function (c) { h = Math.max(h, c.getBoundingClientRect().height); });
    }
    this.viewport.style.height = h + 'px';
  };

  // vị trí x (wrap) gần nhất với x hiện tại cho slide index
  Slider.prototype.targetFor = function (index, from) {
    var t = this.slides[index].target;
    if (from === undefined) return t;
    var T = this.total;
    var k = Math.round((from - t) / T);
    return t + k * T;
  };

  Slider.prototype.render = function () {
    var T = this.total, vw = this.vw, self = this;
    var minCell = Math.min.apply(null, this.cellW);
    var spare = Math.max(0, T - vw - minCell);
    var L = -minCell - spare / 2;
    // track đứng yên, dịch trực tiếp từng cell (tránh Chrome bỏ vẽ track nằm ngoài viewport)
    this.cells.forEach(function (cell, i) {
      var e = self.cellX[i] + self.x + self.trackOffset;
      var shift = Math.floor((e - L) / T) * T; // đưa cell về dải [L, L+T)
      cell.style.transform = 'translateX(' + (self.cellX[i] + self.x - shift) + 'px)';
    });
  };

  Slider.prototype.startAnimation = function () {
    if (this.isAnimating) return;
    this.isAnimating = true;
    var self = this;
    function frame() {
      self.animateFrame();
      if (self.isAnimating) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  };

  Slider.prototype.animateFrame = function () {
    var prevX = this.x;
    if (this.isPointerDown) {
      // kéo: x bám theo con trỏ
      this.velocity += (this.dragX - this.x) - this.velocity;
    } else {
      var target = this.targetX;
      this.velocity += (target - this.x) * this.opts.attraction;
    }
    this.x += this.velocity;
    this.velocity *= (1 - this.opts.friction);
    this.render();
    if (!this.isPointerDown && Math.round(this.x * 100) === Math.round(prevX * 100)) {
      this.isAnimating = false;
      this.x = this.targetX;
      // chuẩn hoá để x không trôi vô hạn
      var base = this.slides[this.selectedIndex].target;
      this.x = base; this.targetX = base;
      this.render();
    }
  };

  Slider.prototype.select = function (index, instant) {
    var n = this.slides.length;
    index = ((index % n) + n) % n;
    this.selectedIndex = index;
    this.targetX = this.targetFor(index, this.x);
    this.updateHeight();
    this.markSelected();
    if (instant || reduceMotion) {
      this.x = this.targetX;
      this.velocity = 0;
      this.render();
      return;
    }
    this.startAnimation();
  };

  // gắn class is-selected cho cell đang chọn + phát sự kiện để UI khác đồng bộ
  Slider.prototype.markSelected = function () {
    var self = this;
    var current = this.slides[this.selectedIndex].cells;
    this.cells.forEach(function (cell, i) { cell.classList.toggle('is-selected', current.indexOf(i) !== -1); });
    this.el.dispatchEvent(new CustomEvent('slider:select', { detail: { index: self.selectedIndex } }));
  };

  Slider.prototype.next = function () { this.select(this.selectedIndex + 1); };
  Slider.prototype.prev = function () { this.select(this.selectedIndex - 1); };

  // tìm slide gần nhất với vị trí x
  Slider.prototype.closestIndex = function (x) {
    var best = 0, bestD = Infinity, self = this;
    this.slides.forEach(function (s, i) {
      var d = Math.abs(self.targetFor(i, x) - x);
      if (d < bestD) { bestD = d; best = i; }
    });
    return best;
  };

  /* autoplay */
  Slider.prototype.play = function () {
    var self = this;
    if (!this.opts.autoPlay || this.playerStopped) return;
    clearTimeout(this.timer);
    this.timer = setTimeout(function tick() {
      if (!self.hovered && !document.hidden) self.next();
      self.timer = setTimeout(tick, self.opts.autoPlay);
    }, this.opts.autoPlay);
  };
  Slider.prototype.pause = function () { clearTimeout(this.timer); };
  Slider.prototype.stopPlayer = function () { this.playerStopped = true; clearTimeout(this.timer); };

  Slider.prototype.bind = function () {
    var self = this;
    var prev = this.el.querySelector('.slider-btn.prev');
    var next = this.el.querySelector('.slider-btn.next');
    if (prev) prev.addEventListener('click', function () { self.stopPlayer(); self.prev(); });
    if (next) next.addEventListener('click', function () { self.stopPlayer(); self.next(); });

    this.el.addEventListener('mouseenter', function () { self.hovered = true; self.pause(); });
    this.el.addEventListener('mouseleave', function () { self.hovered = false; self.play(); });

    // ---- drag ----
    var startX = 0, startY = 0, dragStartX = 0, isDragging = false, lastMoveTime = 0, pointerId = null;
    var vp = this.viewport;
    vp.addEventListener('pointerdown', function (ev) {
      if (ev.button !== 0) return;
      if (ev.pointerType === 'mouse') ev.preventDefault();
      self.stopPlayer();
      pointerId = ev.pointerId;
      startX = ev.clientX; startY = ev.clientY;
      dragStartX = self.x;
      isDragging = false;
      self.wasDragged = false;
      self.isPointerDown = true;
      self.dragX = self.x;
      self.el.classList.add('is-pointer-down');
      window.addEventListener('pointermove', onMove);
      window.addEventListener('pointerup', onUp);
      window.addEventListener('pointercancel', onUp);
    });
    function onMove(ev) {
      if (ev.pointerId !== pointerId) return;
      var dx = ev.clientX - startX, dy = ev.clientY - startY;
      if (!isDragging) {
        if (Math.abs(dx) < self.opts.dragThreshold) {
          if (Math.abs(dy) > self.opts.dragThreshold) onUp(ev, true); // cuộn dọc
          return;
        }
        isDragging = true;
        self.wasDragged = true;
        self.el.classList.add('is-dragging');
        self.startAnimation();
      }
      self.dragX = dragStartX + dx;
      lastMoveTime = Date.now();
    }
    function onUp(ev, cancelled) {
      if (ev.pointerId !== pointerId) return;
      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('pointerup', onUp);
      window.removeEventListener('pointercancel', onUp);
      self.isPointerDown = false;
      self.el.classList.remove('is-pointer-down');
      if (!isDragging || cancelled === true) {
        if (isDragging) self.select(self.selectedIndex);
        return;
      }
      isDragging = false;
      setTimeout(function () { self.el.classList.remove('is-dragging'); }, 0);
      // vị trí nghỉ dự đoán theo quán tính (giống Flickity)
      var resting = self.x + self.velocity / self.opts.friction;
      var index = self.closestIndex(resting);
      if (index === self.selectedIndex && Date.now() - lastMoveTime < 150) {
        var delta = self.dragX - dragStartX;
        if (delta < 0) index += 1; else if (delta > 0) index -= 1;
      }
      self.select(index);
    }
    // chặn click link sau khi kéo
    this.el.addEventListener('click', function (ev) {
      if (self.wasDragged) { ev.preventDefault(); ev.stopPropagation(); self.wasDragged = false; }
    }, true);
    this.el.addEventListener('dragstart', function (ev) { ev.preventDefault(); });
  };

  Slider.prototype.resize = function () {
    this.layout();
    this.x = this.slides[this.selectedIndex].target;
    this.targetX = this.x;
    this.velocity = 0;
    this.render();
  };

  var sliders = [];
  document.querySelectorAll('[data-slider]').forEach(function (el) {
    sliders.push(new Slider(el));
  });
  function relayoutSliders() { sliders.forEach(function (s) { s.resize(); }); }
  var resizeTimer;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(relayoutSliders, 100);
  });
  window.addEventListener('load', relayoutSliders);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(relayoutSliders);
  // cập nhật chiều cao khi ảnh trong slider tải xong
  document.querySelectorAll('[data-slider] img').forEach(function (img) {
    img.addEventListener('load', function () {
      var el = img.closest('[data-slider]');
      sliders.forEach(function (s) { if (s.el === el) s.updateHeight(); });
    });
  });
  document.addEventListener('visibilitychange', function () {
    if (!document.hidden) sliders.forEach(function (s) { if (!s.hovered) s.play(); });
  });

  /* ------------------------------------------------------------------
   * Banner Đà Nẵng: dải biểu tượng + dots điều khiển slider địa điểm
   * ------------------------------------------------------------------ */
  var dnBanner = document.querySelector('.dn-banner');
  if (dnBanner) {
    var dnSliderEl = dnBanner.querySelector('[data-slider]');
    var dnSlider = dnSliderEl._slider;
    var dnControls = dnBanner.querySelectorAll('[data-goto]');
    var loadSlideImage = function (slideEl) {
      var img = slideEl && slideEl.querySelector('img[data-src-deferred]');
      if (img) { img.src = img.getAttribute('data-src-deferred'); img.removeAttribute('data-src-deferred'); }
    };
    var syncDn = function (index) {
      dnControls.forEach(function (c) {
        var on = Number(c.getAttribute('data-goto')) === index;
        c.classList.toggle('is-active', on);
        if (c.classList.contains('dn-dot')) c.setAttribute('aria-current', on ? 'true' : 'false');
      });
      loadSlideImage(dnSlider.cells[index]);
      loadSlideImage(dnSlider.cells[(index + 1) % dnSlider.cells.length]);
    };
    dnSliderEl.addEventListener('slider:select', function (ev) { syncDn(ev.detail.index); });
    dnControls.forEach(function (c) {
      c.addEventListener('click', function () {
        dnSlider.stopPlayer();
        dnSlider.select(Number(c.getAttribute('data-goto')));
      });
    });
    syncDn(dnSlider.selectedIndex);
    // tải nốt ảnh các slide còn lại sau khi trang tải xong
    window.addEventListener('load', function () { dnSlider.cells.forEach(loadSlideImage); });
  }

  /* ------------------------------------------------------------------
   * Header sticky (sticky-jump) + back-to-top
   * ------------------------------------------------------------------ */
  var header = document.getElementById('header');
  var wrapper = header.querySelector('.header-wrapper');
  var backTop = document.querySelector('.back-to-top');
  var headerHeight = header.offsetHeight;
  var stuck = false;

  function measureHeader() {
    if (stuck) return;
    header.style.height = '';
    headerHeight = header.offsetHeight;
  }
  function onScroll() {
    var y = window.pageYOffset || document.documentElement.scrollTop;
    var shouldStick = y >= headerHeight && headerHeight > 0;
    if (shouldStick !== stuck) {
      stuck = shouldStick;
      if (stuck) {
        header.style.height = headerHeight + 'px';
        wrapper.classList.add('stuck');
      } else {
        wrapper.classList.remove('stuck');
        header.style.height = '';
      }
    }
    if (backTop) backTop.classList.toggle('active', y > window.innerHeight);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { measureHeader(); onScroll(); });
  window.addEventListener('load', measureHeader);
  onScroll();

  if (backTop) {
    backTop.addEventListener('click', function (ev) {
      ev.preventDefault();
      window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
    });
  }

  /* ------------------------------------------------------------------
   * Dropdown header: đóng khi bấm link "#" (search) — không nhảy trang
   * ------------------------------------------------------------------ */
  document.querySelectorAll('.header-search > a').forEach(function (a) {
    a.addEventListener('click', function (ev) {
      ev.preventDefault();
      var input = a.parentNode.querySelector('.search-field');
      if (input) input.focus();
    });
  });

  /* ------------------------------------------------------------------
   * Off-canvas menu (mobile)
   * ------------------------------------------------------------------ */
  var menuBg = document.querySelector('.mfp-bg');
  var menuWrap = document.getElementById('main-menu');
  var openBtn = document.querySelector('.js-open-menu');
  var closeTimer;

  function openMenu(ev) {
    if (ev) ev.preventDefault();
    clearTimeout(closeTimer);
    menuBg.hidden = false;
    menuWrap.hidden = false;
    menuBg.classList.remove('mfp-removing');
    menuWrap.classList.remove('mfp-removing');
    document.documentElement.classList.add('has-off-canvas');
    void menuWrap.offsetWidth; // reflow để transition chạy
    menuBg.classList.add('mfp-ready');
    menuWrap.classList.add('mfp-ready');
    openBtn.setAttribute('aria-expanded', 'true');
    menuWrap.focus({ preventScroll: true });
  }
  function closeMenu() {
    if (menuWrap.hidden) return;
    menuBg.classList.add('mfp-removing');
    menuWrap.classList.add('mfp-removing');
    openBtn.setAttribute('aria-expanded', 'false');
    closeTimer = setTimeout(function () {
      menuBg.hidden = true;
      menuWrap.hidden = true;
      menuBg.classList.remove('mfp-ready', 'mfp-removing');
      menuWrap.classList.remove('mfp-ready', 'mfp-removing');
      document.documentElement.classList.remove('has-off-canvas');
    }, 300);
  }
  if (openBtn) openBtn.addEventListener('click', openMenu);
  menuWrap.querySelector('.mfp-close').addEventListener('click', closeMenu);
  menuWrap.querySelector('.mfp-container').addEventListener('click', function (ev) {
    if (!ev.target.closest('.mfp-content')) closeMenu();
  });
  document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') closeMenu(); });
  MQ_LARGE.addEventListener && MQ_LARGE.addEventListener('change', function (m) { if (m.matches) closeMenu(); });

  // Link tới một mục trong trang (vd. #tour-golf): đóng menu rồi cuộn tới mục đó
  menuWrap.querySelectorAll('.nav-sidebar a[href^="#"]:not([href="#"])').forEach(function (a) {
    a.addEventListener('click', closeMenu);
  });

  menuWrap.querySelectorAll('.nav-sidebar .toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var li = btn.parentNode;
      var open = li.classList.toggle('active');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  /* ------------------------------------------------------------------
   * Form email (giả lập Contact Form 7: validate + thông báo)
   * ------------------------------------------------------------------ */
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  /* Thông báo form theo ngôn ngữ trang (<html lang>): ja mặc định, zh */
  var MSGS = {
    ja: {
      required: 'この項目は必須です。',
      email: 'メールアドレスを入力してください。',
      invalid: '入力内容に誤りがあります。確認してもう一度お試しください。',
      sent: 'ご登録ありがとうございます。送信が完了しました。'
    },
    zh: {
      required: '请填写此栏。',
      email: '请输入电子邮箱地址。',
      invalid: '有一项或多项输入有误，请检查后重试。',
      sent: '感谢您的提交，信息已发送。'
    }
  };
  var MSG = MSGS[(document.documentElement.lang || 'ja').slice(0, 2)] || MSGS.ja;
  document.querySelectorAll('.email-form').forEach(function (form) {
    var input = form.querySelector('input[type="email"]');
    var out = form.querySelector('.form-response');
    var submitted = false;

    function setTip(msg) {
      var tip = form.querySelector('.form-tip');
      if (!msg) {
        if (tip) tip.remove();
        input.classList.remove('is-invalid');
        input.removeAttribute('aria-invalid');
        return;
      }
      if (!tip) {
        tip = document.createElement('span');
        tip.className = 'form-tip';
        tip.setAttribute('aria-hidden', 'true');
        input.insertAdjacentElement('afterend', tip);
      }
      tip.textContent = msg;
      input.classList.add('is-invalid');
      input.setAttribute('aria-invalid', 'true');
    }
    function validate() {
      var v = input.value.trim();
      if (!v) return MSG.required;
      if (!EMAIL_RE.test(v)) return MSG.email;
      return '';
    }
    input.addEventListener('input', function () {
      if (submitted) setTip(validate());
    });
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      submitted = true;
      var err = validate();
      setTip(err);
      out.hidden = false;
      out.classList.toggle('is-sent', !err);
      out.textContent = err
        ? MSG.invalid
        : MSG.sent;
      if (!err) { input.value = ''; submitted = false; }
    });
  });

  /* ---------- Trang chưa làm: link href="#" và form tìm kiếm không dẫn đi đâu ---------- */
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a[href="#"]');
    if (a) ev.preventDefault();
  });
  document.querySelectorAll('form.searchform').forEach(function (form) {
    form.addEventListener('submit', function (ev) { ev.preventDefault(); });
  });
})();
