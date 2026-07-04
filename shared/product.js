let storeData = null;
const siteSlug = window.location.pathname.split('/').filter(Boolean)[0] || 'store';
const cartKey = 'cart_' + siteSlug;
let cart = JSON.parse(localStorage.getItem(cartKey) || '[]');

async function initProductPage() {
  const params = new URLSearchParams(window.location.search);
  const id = parseInt(params.get('id'));
  if (!id) { window.location.href = 'index.html'; return; }

  const res = await fetch('products.json');
  storeData = await res.json();
  const product = storeData.products.find(p => p.id === id);
  if (!product) { window.location.href = 'index.html'; return; }

  applyTheme();
  renderProductHeader();
  renderProduct(product);
  renderFooter();
  updateCartCount();
  setupCart();
}

function applyTheme() {
  const t = storeData.theme;
  if (!t) return;
  const root = document.documentElement;
  if (t.primary) root.style.setProperty('--primary', t.primary);
  if (t.primaryDark) root.style.setProperty('--primary-dark', t.primaryDark);
  if (t.accent) root.style.setProperty('--accent', t.accent);
}

function renderProductHeader() {
  const s = storeData.store;
  document.getElementById('logo').innerHTML = s.logoHtml || s.name;
}

function renderProduct(p) {
  const s = storeData.store;
  document.title = s.name + ' — ' + p.name;
  const savings = p.originalPrice ? Math.round((1 - p.price / p.originalPrice) * 100) : 0;
  const vat = vatLabel(s);

  document.getElementById('breadcrumb').innerHTML =
    `<a href="index.html">Home</a> › <a href="index.html#products">${p.category}</a> › ${p.name}`;

  document.getElementById('product-detail').innerHTML = `
    <div class="product-gallery">
      <img src="${p.image}" alt="${p.name}">
    </div>
    <div class="product-detail-info">
      <div class="product-category">${p.category}</div>
      <h1>${p.name}</h1>
      ${p.badge ? `<span class="product-badge" style="position:static;display:inline-block;margin-bottom:12px">${p.badge}</span>` : ''}
      <div class="product-pricing" style="margin:16px 0">
        <span class="price-current">${formatPrice(p.price, s)}</span>
        ${p.originalPrice ? `<span class="price-original">${formatPrice(p.originalPrice, s)}</span>` : ''}
        ${savings ? `<span class="price-save">Save ${savings}%</span>` : ''}
        ${vat ? `<span style="display:block;font-size:0.8rem;color:var(--text-muted);margin-top:4px">${vat}</span>` : ''}
      </div>
      <p style="color:var(--text-muted);margin-bottom:16px">${p.description}</p>
      <div class="product-meta">
        <span>SKU: ${p.sku || 'N/A'}</span>
        <span>✓ In Stock</span>
        <span>🚚 ${p.shippingDays || '7-14 business days'}</span>
        <span>📦 Ships from supplier warehouse</span>
      </div>
      <button class="add-to-cart" style="max-width:280px;margin-bottom:16px" onclick="addToCart(${p.id})">Add to Cart — ${formatPrice(p.price, s)}</button>
      <div class="product-details-box">
        <h3>Product Details</h3>
        <p style="color:var(--text-muted);line-height:1.8">${p.details || p.description}</p>
      </div>
      <div class="policy-links">
        <a href="policies.html?type=returns" class="policy-link">Return Policy</a>
        <a href="policies.html?type=shipping" class="policy-link">Shipping Info</a>
        <a href="policies.html?type=terms" class="policy-link">Terms of Service</a>
      </div>
      <p style="font-size:0.8rem;color:var(--text-muted);margin-top:16px">
        Product images are representative. Minor variations in color or packaging may occur due to supplier batches.
        By purchasing you agree to our <a href="policies.html?type=terms" style="color:var(--primary)">Terms of Service</a>.
      </p>
    </div>`;
}

function renderFooter() {
  const s = storeData.store;
  document.getElementById('footer-brand').innerHTML = `<span class="logo">${s.logoHtml || s.name}</span><p>${s.description}</p>`;
  document.getElementById('footer-email').textContent = s.email;
  document.getElementById('footer-email').href = 'mailto:' + s.email;
  document.getElementById('footer-year').textContent = new Date().getFullYear();
  document.getElementById('footer-name').textContent = s.name;
}

function addToCart(id) {
  const product = storeData.products.find(p => p.id === id);
  const existing = cart.find(c => c.id === id);
  if (existing) existing.qty++;
  else cart.push({ id, name: product.name, price: product.price, image: product.image, qty: 1 });
  localStorage.setItem(cartKey, JSON.stringify(cart));
  updateCartCount();
  const btn = document.querySelector('.add-to-cart');
  const orig = btn.textContent;
  btn.textContent = '✓ Added to Cart!';
  setTimeout(() => btn.textContent = orig, 1500);
}

function updateCartCount() {
  const el = document.getElementById('cart-count');
  if (el) el.textContent = cart.reduce((s, c) => s + c.qty, 0);
}

function setupCart() {
  document.getElementById('cart-btn')?.addEventListener('click', () => {
    window.location.href = 'index.html';
  });
}

document.addEventListener('DOMContentLoaded', initProductPage);