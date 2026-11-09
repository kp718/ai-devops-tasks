const sum = require('./sum');

describe('Funkcja sum()', () => {
  test('powinna zwracać sumę dwóch liczb', () => {
    expect(sum(2, 3)).toBe(5);
  });
});
