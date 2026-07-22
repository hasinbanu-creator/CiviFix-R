export const resolveImageUri = (img, apiBaseUrl) => {
  if (!img) return img;
  if (typeof img !== 'string') return img;
  if (img.startsWith('data:')) return img;
  if (/^https?:\/\//i.test(img)) return img;

  const base = apiBaseUrl || '';
  if (!base) return img;
  return `${base.replace(/\/$/, '')}${img.startsWith('/') ? '' : '/'}${img}`;
};
