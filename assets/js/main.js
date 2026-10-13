// Sliding highlight behind the nav links (rests on the current page).
(() => {
  const nav = document.querySelector('[data-nav]');
  if (!nav) return;
  const hl = nav.querySelector('.nav-hl');
  const links = [...nav.querySelectorAll('.nav-link')];
  const active = nav.querySelector('.is-active');
  const moveTo = (el) => {
    if (!el) { hl.style.opacity = 0; return; }
    hl.style.opacity = 1;
    hl.style.width = el.offsetWidth + 'px';
    hl.style.transform = `translateX(${el.offsetLeft}px)`;
  };
  // place instantly on load, then animate on hover
  hl.style.transition = 'none';
  moveTo(active);
  requestAnimationFrame(() => requestAnimationFrame(() => (hl.style.transition = '')));
  links.forEach((a) => {
    a.addEventListener('mouseenter', () => moveTo(a));
    a.addEventListener('focus', () => moveTo(a));
  });
  nav.addEventListener('mouseleave', () => moveTo(active));
  nav.addEventListener('focusout', (e) => { if (!nav.contains(e.relatedTarget)) moveTo(active); });
  addEventListener('resize', () => moveTo(active));
  document.fonts?.ready.then(() => moveTo(active));
})();

// Art page: medium filters + lightbox.
(() => {
  const gallery = document.querySelector('[data-gallery]');
  if (!gallery) return;
  const pieces = [...gallery.querySelectorAll('.piece')];
  const chips = [...document.querySelectorAll('.chip')];
  const box = document.querySelector('[data-lightbox]');
  const img = box.querySelector('img');
  const [title, medium] = box.querySelectorAll('figcaption strong, figcaption span');
  const desc = box.querySelector('figcaption p');
  let current = -1;

  const visible = () => pieces.filter((p) => !p.hidden);

  const filter = (key) => {
    chips.forEach((c) => {
      const on = c.dataset.filter === key;
      c.classList.toggle('is-on', on);
      c.setAttribute('aria-pressed', on);
    });
    pieces.forEach((p) => (p.hidden = key !== 'all' && p.dataset.cat !== key));
  };
  chips.forEach((c) => c.addEventListener('click', () => filter(c.dataset.filter)));

  const show = (piece) => {
    const b = piece.querySelector('.piece-btn');
    current = visible().indexOf(piece);
    img.src = b.dataset.full;
    img.alt = b.dataset.title;
    title.textContent = b.dataset.title;
    medium.textContent = b.dataset.medium;
    desc.textContent = b.dataset.desc;
    if (!box.open) box.showModal();
    history.replaceState(null, '', '#' + piece.id);
  };
  const step = (d) => {
    const v = visible();
    if (v.length) show(v[(current + d + v.length) % v.length]);
  };
  const close = () => {
    box.close();
  };

  pieces.forEach((p) => p.querySelector('.piece-btn').addEventListener('click', () => show(p)));
  box.querySelector('[data-prev]').addEventListener('click', () => step(-1));
  box.querySelector('[data-next]').addEventListener('click', () => step(1));
  box.querySelector('[data-close]').addEventListener('click', close);
  box.addEventListener('click', (e) => { if (e.target === box || e.target.tagName === 'FIGURE') close(); });
  box.addEventListener('close', () => history.replaceState(null, '', location.pathname));
  box.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') step(-1);
    if (e.key === 'ArrowRight') step(1);
  });

  // Deep links: /art/#giraffe opens that piece.
  const fromHash = () => {
    const el = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (el && el.classList.contains('piece')) show(el);
  };
  fromHash();
  addEventListener('hashchange', fromHash);
})();
