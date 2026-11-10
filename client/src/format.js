// 8.25 -> '8.3'. Returns null for missing or zero ratings.
export function formatRating(value) {
  const rating = Number(value);
  return Number.isFinite(rating) && rating > 0 ? rating.toFixed(1) : null;
}

const compactNumber = new Intl.NumberFormat('en-US', { notation: 'compact' });

// 1109824 -> '1.1M votes'
export function voteLabel(count) {
  const votes = Number(count) || 0;
  return `${compactNumber.format(votes)} ${votes === 1 ? 'vote' : 'votes'}`;
}

// '2023-01-01' -> '2023'
export function yearOf(date) {
  return date ? String(date).slice(0, 4) : '';
}

// Posters and photos are stored as the string 'None' when there is no image.
export function imageUrl(value) {
  return value && value !== 'None' ? value : undefined;
}
