function formatPrice(amount, store) {
  const currency = store?.currency || 'USD';
  const value = Number(amount);
  if (currency === 'SEK') {
    return new Intl.NumberFormat('sv-SE', {
      style: 'currency',
      currency: 'SEK',
      minimumFractionDigits: value % 1 === 0 ? 0 : 2,
      maximumFractionDigits: 2,
    }).format(value);
  }
  return '$' + value.toFixed(2);
}

function vatLabel(store) {
  if (!store?.pricesIncludeVat) return '';
  const rate = store.vatRatePct ? ` (${store.vatRatePct}% moms)` : '';
  return `incl. VAT${rate}`;
}