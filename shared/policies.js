let storeData = null;

async function initPoliciesPage() {
  const res = await fetch('products.json');
  storeData = await res.json();
  const params = new URLSearchParams(window.location.search);
  const type = params.get('type') || 'returns';

  applyTheme();
  renderHeader();
  renderPolicies(type);
  renderFooter();
}

function applyTheme() {
  const t = storeData.theme;
  if (!t) return;
  const root = document.documentElement;
  if (t.primary) root.style.setProperty('--primary', t.primary);
  if (t.primaryDark) root.style.setProperty('--primary-dark', t.primaryDark);
  if (t.accent) root.style.setProperty('--accent', t.accent);
}

function renderHeader() {
  const s = storeData.store;
  document.getElementById('logo').innerHTML = s.logoHtml || s.name;
  document.title = storeData.store.name + ' — Policies';
}

function renderPolicies(activeType) {
  const policies = storeData.policies;
  const types = Object.keys(policies);

  document.getElementById('policy-nav').innerHTML = types.map(t =>
    `<a href="policies.html?type=${t}" class="${t === activeType ? 'active' : ''}">${policies[t].title}</a>`
  ).join('');

  const policy = policies[activeType] || policies.returns;
  const s = storeData.store;

  document.getElementById('policy-content').innerHTML = `
    <h1>${policy.title}</h1>
    <p style="color:var(--text-muted);margin-bottom:8px">Last updated: July 2026 · ${s.name}</p>
    <div class="policy-summary">${policy.summary}</div>
    ${policy.sections.map(sec => `
      <div class="policy-section">
        <h2>${sec.heading}</h2>
        <p>${sec.text}</p>
      </div>`).join('')}
    <div class="policy-section" style="background:var(--bg);padding:20px;border-radius:12px;margin-top:32px">
      <h2>Contact Us About This Policy</h2>
      <p>Email <a href="mailto:${s.email}" style="color:var(--primary)">${s.email}</a> or call ${s.phone}. We respond within 2 business days.</p>
    </div>
    <p style="font-size:0.85rem;color:var(--text-muted);margin-top:24px">
      These policies are designed to protect both customers and ${s.name} as an independent online retailer sourcing products from third-party suppliers.
    </p>`;
}

function renderFooter() {
  const s = storeData.store;
  document.getElementById('footer-brand').innerHTML = `<span class="logo">${s.logoHtml || s.name}</span><p>${s.description}</p>`;
  document.getElementById('footer-year').textContent = new Date().getFullYear();
  document.getElementById('footer-name').textContent = s.name;
}

document.addEventListener('DOMContentLoaded', initPoliciesPage);