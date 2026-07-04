let storeData = null;
const siteSlug = window.location.pathname.split('/').filter(Boolean)[0] || 'store';
const cartKey = 'cart_' + siteSlug;
let cart = JSON.parse(localStorage.getItem(cartKey) || '[]');
let activeFilter = 'all';

async function initStore() {
  const res = await fetch('products.json');
  storeData = await res.json();
  applyTheme();
  renderHeader();
  renderHero();
  renderTrustBar();
  renderCategories();
  renderFeatured();
  renderProducts();
  renderAbout();
  document.getElementById('stat-products').textContent = storeData.products.length;
  document.getElementById('hero-eyebrow').textContent = storeData.store.tagline;
  renderFooter();
  renderPolicyLinks();
  renderLaunchBanner();
  updateCartCount();
  setupCart();
  setupContact();
  setupNewsletter();
}

function getStoreSlug() {
  return storeData?.store?.slug || siteSlug;
}

function applyTheme() {
  const t = storeData.theme;
  if (!t) return;
  const root = document.documentElement;
  if (t.primary) root.style.setProperty('--primary', t.primary);
  if (t.primaryDark) root.style.setProperty('--primary-dark', t.primaryDark);
  if (t.accent) root.style.setProperty('--accent', t.accent);
  document.title = storeData.store.name + ' — ' + storeData.store.tagline;
}

function renderHeader() {
  const s = storeData.store;
  const logo = document.getElementById('logo');
  if (logo) logo.innerHTML = s.logoHtml || s.name;
  const editPath = document.getElementById('edit-path');
  if (editPath) editPath.textContent = 'products.json';
}

function renderHero() {
  const h = storeData.hero;
  const title = document.getElementById('hero-title');
  const subtitle = document.getElementById('hero-subtitle');
  const badges = document.getElementById('hero-badges');
  if (!title) return;
  title.textContent = h.title;
  subtitle.textContent = h.subtitle;
  badges.innerHTML = h.badges.map(b => `<div class="hero-badge">✓ ${b}</div>`).join('');
}

function renderTrustBar() {
  const el = document.getElementById('trust-items');
  if (!el) return;
  el.innerHTML = storeData.trust.map(t =>
    `<div class="trust-item"><div class="trust-icon">${t.icon}</div><div><strong>${t.text}</strong></div></div>`
  ).join('');
}

function renderFeatured() {
  const grid = document.getElementById('featured-grid');
  if (!grid) return;
  const featured = storeData.products.filter(p => p.badge).slice(0, 4);
  const items = featured.length >= 4 ? featured : storeData.products.slice(0, 4);
  grid.innerHTML = items.map(p => productCardHtml(p)).join('');
}

function renderCategories() {
  const el = document.getElementById('category-filters');
  if (!el) return;
  const cats = ['all', ...new Set(storeData.products.map(p => p.category))];
  el.innerHTML = cats.map(c =>
    `<button class="filter-btn${c === 'all' ? ' active' : ''}" data-cat="${c}">${c === 'all' ? 'All Products' : c}</button>`
  ).join('');
  el.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      el.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeFilter = btn.dataset.cat;
      renderProducts();
    });
  });
}

function renderProducts(filter = '') {
  const grid = document.getElementById('products-grid');
  if (!grid) return;
  let products = storeData.products;
  if (activeFilter !== 'all') products = products.filter(p => p.category === activeFilter);
  if (filter) {
    const q = filter.toLowerCase();
    products = products.filter(p =>
      p.name.toLowerCase().includes(q) || p.description.toLowerCase().includes(q) || p.category.toLowerCase().includes(q)
    );
  }
  if (!products.length) {
    grid.innerHTML = '<p style="grid-column:1/-1;text-align:center;color:#64748b;padding:40px;">No products found.</p>';
    return;
  }
  grid.innerHTML = products.map(p => productCardHtml(p)).join('');
}

function productCardHtml(p) {
  const s = storeData.store;
  const savings = p.originalPrice ? Math.round((1 - p.price / p.originalPrice) * 100) : 0;
  const vat = vatLabel(s);
  return `
    <div class="product-card" data-id="${p.id}">
      <a href="product.html?id=${p.id}" class="product-image">
        ${p.badge ? `<span class="product-badge">${p.badge}</span>` : ''}
        <img src="${p.image}" alt="${p.name}" loading="lazy">
      </a>
      <div class="product-info">
        <div class="product-category">${p.category}</div>
        <h3 class="product-name"><a href="product.html?id=${p.id}">${p.name}</a></h3>
        <p class="product-desc">${p.description}</p>
        <div class="product-pricing">
          <span class="price-current">${formatPrice(p.price, s)}</span>
          ${p.originalPrice ? `<span class="price-original">${formatPrice(p.originalPrice, s)}</span>` : ''}
          ${savings ? `<span class="price-save">Save ${savings}%</span>` : ''}
          ${vat ? `<span class="price-vat" style="display:block;font-size:0.75rem;color:var(--text-muted);margin-top:2px">${vat}</span>` : ''}
        </div>
        <button class="add-to-cart" onclick="addToCart(${p.id})">Add to Cart</button>
        <a href="product.html?id=${p.id}" class="view-link">View Details →</a>
      </div>
    </div>`;
}

function renderAbout() {
  const a = storeData.about;
  const title = document.getElementById('about-title');
  if (!title) return;
  title.textContent = a.title;
  document.getElementById('about-text').innerHTML = a.paragraphs.map(p => `<p>${p}</p>`).join('');
  document.getElementById('features-list').innerHTML = a.features.map(f =>
    `<div class="feature-item"><div class="feature-icon">${f.icon}</div><span>${f.text}</span></div>`
  ).join('');
}

function renderFooter() {
  const s = storeData.store;
  const brand = document.getElementById('footer-brand');
  if (!brand) return;
  brand.innerHTML = `<span class="logo">${s.logoHtml || s.name}</span><p>${s.description}</p>`;
  const email = document.getElementById('footer-email');
  const phone = document.getElementById('footer-phone');
  if (email) { email.textContent = s.email; email.href = 'mailto:' + s.email; }
  if (phone) { phone.textContent = s.phone; phone.href = 'tel:' + s.phone.replace(/\D/g,''); }
  document.getElementById('footer-year').textContent = new Date().getFullYear();
  document.getElementById('footer-name').textContent = s.name;
}

function renderPolicyLinks() {
  document.querySelectorAll('.policy-footer-link').forEach(el => {
    const type = el.dataset.policy;
    el.href = `policies.html?type=${type}`;
  });
}

function renderLaunchBanner() {
  if (storeData.launchReady !== false) return;
  const bar = document.getElementById('announce-bar');
  if (!bar) return;
  bar.innerHTML = '⚠️ <strong>Preview mode</strong> — This store is not yet live. Fill in legal details in <code>products.json</code> before launching.';
  bar.style.background = 'linear-gradient(90deg, #b45309, #d97706)';
}

function addToCart(id) {
  const product = storeData.products.find(p => p.id === id);
  const existing = cart.find(c => c.id === id);
  if (existing) existing.qty++;
  else cart.push({ id, name: product.name, price: product.price, image: product.image, qty: 1 });
  localStorage.setItem(cartKey, JSON.stringify(cart));
  updateCartCount();
  showCartNotification();
}

function updateCartCount() {
  const el = document.getElementById('cart-count');
  if (el) el.textContent = cart.reduce((s, c) => s + c.qty, 0);
}

function showCartNotification() {
  const btn = document.querySelector('.cart-btn');
  if (!btn) return;
  const orig = btn.innerHTML;
  btn.innerHTML = '✓ Added!';
  setTimeout(() => { btn.innerHTML = orig; updateCartCount(); }, 1200);
}

function setupCart() {
  document.getElementById('cart-btn')?.addEventListener('click', openCart);
  document.getElementById('cart-close')?.addEventListener('click', closeCart);
  document.getElementById('cart-overlay')?.addEventListener('click', e => {
    if (e.target.id === 'cart-overlay') closeCart();
  });
  document.getElementById('checkout-btn')?.addEventListener('click', openCheckout);
  document.getElementById('checkout-close')?.addEventListener('click', closeCheckout);
  document.getElementById('checkout-overlay')?.addEventListener('click', e => {
    if (e.target.id === 'checkout-overlay') closeCheckout();
  });
  document.getElementById('checkout-form')?.addEventListener('submit', submitOrder);
  document.getElementById('search-input')?.addEventListener('input', e => renderProducts(e.target.value));
  document.getElementById('shop-now')?.addEventListener('click', () => {
    document.getElementById('products')?.scrollIntoView({ behavior: 'smooth' });
  });
}

function openCart() {
  const s = storeData.store;
  const overlay = document.getElementById('cart-overlay');
  const items = document.getElementById('cart-items');
  if (!cart.length) {
    items.innerHTML = '<div class="empty-cart">Your cart is empty</div>';
    document.getElementById('cart-total-price').textContent = formatPrice(0, s);
  } else {
    items.innerHTML = cart.map(c => `
      <div class="cart-item">
        <img src="${c.image}" alt="${c.name}">
        <div>
          <div style="font-weight:600">${c.name}</div>
          <div style="color:#64748b;font-size:0.85rem">Qty: ${c.qty} × ${formatPrice(c.price, s)}</div>
        </div>
      </div>`).join('');
    const total = cart.reduce((sum, c) => sum + c.price * c.qty, 0);
    document.getElementById('cart-total-price').textContent = formatPrice(total, s);
  }
  overlay.classList.add('open');
}

function closeCart() { document.getElementById('cart-overlay')?.classList.remove('open'); }

function openCheckout() {
  if (!cart.length) return;
  closeCart();
  document.getElementById('checkout-overlay')?.classList.add('open');
  document.getElementById('checkout-form-view').style.display = 'block';
  document.getElementById('checkout-success-view').style.display = 'none';
}

function closeCheckout() { document.getElementById('checkout-overlay')?.classList.remove('open'); }

async function submitOrder(e) {
  e.preventDefault();
  const form = e.target;
  const total = cart.reduce((s, c) => s + c.price * c.qty, 0);
  const order = {
    store: getStoreSlug(),
    name: form.name.value,
    email: form.email.value,
    phone: form.phone.value,
    address: form.address.value,
    city: form.city.value,
    state: form.state.value,
    zip: form.zip.value,
    notes: form.notes.value,
    items: cart.map(c => ({ id: c.id, name: c.name, price: c.price, qty: c.qty })),
    total,
    currency: storeData.store.currency || 'USD',
  };
  try {
    const res = await fetch('/api/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(order),
    });
    const data = await res.json();
    if (data.ok) {
      document.getElementById('checkout-form-view').style.display = 'none';
      document.getElementById('checkout-success-view').style.display = 'block';
      document.getElementById('order-id-display').textContent = data.orderId;
      cart = [];
      localStorage.setItem(cartKey, '[]');
      updateCartCount();
      form.reset();
    }
  } catch (err) {
    alert('Could not submit order. Make sure the server is running (python3 server.py).');
  }
}

function setupContact() {
  document.getElementById('contact-form')?.addEventListener('submit', async e => {
    e.preventDefault();
    const form = e.target;
    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          store: getStoreSlug(),
          name: form.name.value,
          email: form.email.value,
          subject: form.subject.value,
          message: form.message.value,
        }),
      });
      if ((await res.json()).ok) {
        const success = document.getElementById('contact-success');
        success.style.display = 'block';
        form.reset();
      }
    } catch (err) {
      alert('Could not send message. Make sure the server is running.');
    }
  });
}

function setupNewsletter() {
  document.getElementById('newsletter-form')?.addEventListener('submit', async e => {
    e.preventDefault();
    const email = e.target.email.value;
    try {
      await fetch('/api/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ store: getStoreSlug(), email }),
      });
      e.target.innerHTML = '<p style="color:white">✓ Subscribed! Check your inbox for deals.</p>';
    } catch (err) { /* silent */ }
  });
}

document.addEventListener('DOMContentLoaded', initStore);