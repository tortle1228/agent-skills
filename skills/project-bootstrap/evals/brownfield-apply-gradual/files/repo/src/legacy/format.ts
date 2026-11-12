export function formatWon(value) {
  return value.toLocaleString('ko-KR') + '원';
}

export function pick(obj, keys) {
  const out = {};
  for (const k of keys) out[k] = obj[k];
  return out;
}
