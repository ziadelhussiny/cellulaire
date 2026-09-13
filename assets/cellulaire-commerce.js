export function selectVariant(variants, options) {
  return variants.find(variant => variant.options.length === options.length && variant.options.every((option,index) => option === options[index])) || null;
}
export function cartUpdate(key, quantity) {
  const number = Number(quantity);
  if (!key || !Number.isInteger(number) || number < 0) throw new Error('Enter a valid quantity.');
  return { id:key, quantity:number };
}
export function productError(response) {
  return response.description || response.message || 'Something went wrong. Please try again.';
}
