import test from 'node:test';
import assert from 'node:assert/strict';
import { selectVariant, cartUpdate, productError } from '../assets/cellulaire-commerce.js';

test('selects the exact option combination including unavailable variants', () => {
  const variants = [{ id:1, options:['50 ml','Single'], available:true }, { id:2, options:['100 ml','Single'], available:false }];
  assert.equal(selectVariant(variants, ['100 ml','Single']).id, 2);
  assert.equal(selectVariant(variants, ['50 ml','Bundle']), null);
});
test('cart updates retain Shopify line keys and accept removal', () => {
  assert.deepEqual(cartUpdate('123:abc', '0'), { id:'123:abc', quantity:0 });
  assert.throws(() => cartUpdate('123:abc', '-1'));
  assert.throws(() => cartUpdate('123:abc', '1.5'));
  assert.throws(() => cartUpdate('', '2'));
});
test('surfaces inventory errors instead of a false success', () => {
  assert.equal(productError({ description:'Only 2 available' }), 'Only 2 available');
  assert.equal(productError({ message:'Sold out' }), 'Sold out');
});
