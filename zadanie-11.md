Poniżej znajdziesz prosty przykład testu jednostkowego dla funkcji `sum(a, b)` z wykorzystaniem Jest – popularnego frameworka do testowania kodu JavaScript.

## 1. Czym jest Jest?

Jest to framework do testowania JavaScript, stworzony przez Meta. Jest często wykorzystywany w projektach JavaScript i React.

Pozwala między innymi na:

- Pisanie testów jednostkowych (unit tests).
- Sprawdzanie, czy funkcje zwracają oczekiwane wyniki.
- Wykrywanie błędów w kodzie.
- Tworzenie mocków, czyli symulowanie działania innych funkcji lub modułów.
- Generowanie raportów pokrycia kodu testami (code coverage).

Przykładowy test sprawdzi, czy funkcja `sum(2, 3)` zwraca `5`.

## 2. Struktura plików projektu

Utwórz folder projektu, np. `jest-example`.

Struktura projektu będzie wyglądać następująco:

text

```text
jest-example/
│
├── package.json
├── sum.js
└── sum.test.js
```

- `package.json` – konfiguracja projektu i zależności.
- `sum.js` – plik zawierający testowaną funkcję.
- `sum.test.js` – plik zawierający test jednostkowy.

## 3. Instalacja Jest

Najpierw upewnij się, że masz zainstalowany Node.js i npm.

Utwórz folder projektu i przejdź do niego:

bash

```bash
mkdir jest-example
cd jest-example
```

Zainicjuj projekt:

bash

```bash
npm init -y
```

Zainstaluj Jest jako zależność deweloperską:

bash

```bash
npm install --save-dev jest
```

Następnie otwórz plik `package.json` i dodaj skrypt `test`:

json

```json
{
  "scripts": {
    "test": "jest"
  },
  "devDependencies": {
    "jest": "^30.0.0"
  }
}
```

Uwaga: wersja Jest w pliku może być inna, jeśli npm zainstalował nowszą wersję. Nie musisz jej ręcznie zmieniać.

## 4. Implementacja funkcji sum()

Utwórz plik `sum.js`:

javascript

```javascript
function sum(a, b) {
  return a + b;
}

module.exports = sum;
```

Dodaliśmy `module.exports`, aby można było zaimportować funkcję w pliku testowym.

## 5. Napisanie testu jednostkowego

Utwórz plik `sum.test.js`:

javascript

```javascript
const sum = require('./sum');

describe('Funkcja sum()', () => {
  test('powinna zwracać sumę dwóch liczb', () => {
    expect(sum(2, 3)).toBe(5);
  });
});
```

### Wyjaśnienie poszczególnych elementów

- `require('./sum')` – importuje testowaną funkcję.
- `describe()` – grupuje testy dotyczące określonej funkcjonalności.
- `test()` – definiuje pojedynczy test.
- `expect()` – sprawdza otrzymany wynik.
- `toBe(5)` – sprawdza, czy wynik jest równy `5`.

Możesz również dodać kolejne przypadki testowe:

javascript

```javascript
const sum = require('./sum');

describe('Funkcja sum()', () => {
  test('dodaje dwie liczby dodatnie', () => {
    expect(sum(2, 3)).toBe(5);
  });

  test('dodaje liczby ujemne', () => {
    expect(sum(-2, -3)).toBe(-5);
  });

  test('dodaje zero', () => {
    expect(sum(5, 0)).toBe(5);
  });

  test('dodaje liczbę dodatnią i ujemną', () => {
    expect(sum(10, -4)).toBe(6);
  });
});
```

## 6. Uruchomienie testów

W terminalu, będąc w głównym folderze projektu, wykonaj polecenie:

bash

```bash
npm test
```

Jest automatycznie wyszuka pliki zawierające `.test.js` lub `.spec.js` i uruchomi znajdujące się w nich testy.

Przykładowy wynik:

Wynik testów Jest

PASS

text

```text
PASS  ./sum.test.js

Funkcja sum()
  ✓ dodaje dwie liczby dodatnie
  ✓ dodaje liczby ujemne
  ✓ dodaje zero
  ✓ dodaje liczbę dodatnią i ujemną

Test Suites: 1 passed, 1 total
Tests:       4 passed, 4 total
```

Oznacza to, że wszystkie cztery testy zakończyły się powodzeniem.

## 7. Dodatkowe przydatne polecenia

| Polecenie | Działanie |
| --- | --- |
| `npm test` | Uruchamia wszystkie testy |
| `npm test -- --watch` | Uruchamia testy w trybie obserwowania zmian |
| `npm test -- --coverage` | Generuje raport pokrycia kodu testami |
| `npx jest sum.test.js` | Uruchamia konkretny plik testowy |

## 8. Podsumowanie

W naszym przykładzie:

1. Zainstalowaliśmy Jest za pomocą npm.
2. Przygotowaliśmy funkcję `sum()` w pliku `sum.js`.
3. Utworzyliśmy test jednostkowy w pliku `sum.test.js`.
4. Wykorzystaliśmy `describe()`, `test()`, `expect()` i `toBe()`.
5. Uruchomiliśmy testy poleceniem `npm test`.

Najważniejsze: test jednostkowy pozwala sprawdzić, czy pojedyncza funkcja działa zgodnie z oczekiwaniami. Dzięki Jest możemy automatycznie wykonywać takie sprawdzenia po każdej zmianie kodu, co pomaga szybciej wykrywać błędy i utrzymywać wysoką jakość projektu.