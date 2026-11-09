Twój algorytm znajduje wszystkie pary elementów tablicy, których suma jest równa `targetSum`. Jest poprawny, ale można go zoptymalizować zarówno pod względem czasu, jak i — w zależności od wymagań — pamięci.

## 1. Złożoność obecnego algorytmu

### Złożoność czasowa: O(n²)

Masz dwie zagnieżdżone pętle:

javascript

```javascript
for (let i = 0; i < arr.length; i++) {
  for (let j = i + 1; j < arr.length; j++) {
```

- Pętla zewnętrzna wykonuje się `n` razy.
- Pętla wewnętrzna wykonuje łącznie około `n(n-1)/2` iteracji.
- Każda iteracja wykonuje porównanie w czasie O(1).

W rezultacie:

$$
T(n) = \frac{n(n-1)}{2} = O(n^2)
$$

### Złożoność pamięciowa: O(k)

Gdzie `k` oznacza liczbę znalezionych par.

- `pairs` przechowuje wszystkie znalezione pary.
- Pozostałe zmienne zajmują O(1) pamięci.

W najgorszym przypadku liczba par może wynosić O(n²), więc:

- Pamięć pomocnicza: O(1).
- Całkowita pamięć wraz z wynikiem: O(n²).

## 2. Optymalizacja – wykorzystanie Set

Możemy zastosować strukturę `Set`, która pozwala sprawdzać, czy poszukiwany element już wystąpił, w średnim czasie O(1).

Zamiast porównywać każdy element z każdym, obliczamy brakującą wartość:

$$
complement = targetSum - arr[i]
$$

Jeśli znajduje się ona w zbiorze, znaleźliśmy parę.

Zoptymalizowana implementacja:

javascript

```javascript

function findPairs(arr, targetSum) {
  const pairs = [];
  const seen = new Set();

  for (const num of arr) {
    const complement = targetSum - num;

    if (seen.has(complement)) {
      pairs.push([complement, num]);
    }

    seen.add(num);
  }

  return pairs;
}
```

Przykład:

javascript

```javascript
findPairs([2, 7, 4, 5, 3, 6], 9);

// [[2, 7], [4, 5], [3, 6]]
```

### Złożoność zoptymalizowanego algorytmu

| Rodzaj | Złożoność |
| --- | --- |
| Czasowa – średnia | O(n + k) |
| Pamięciowa pomocnicza | O(n) |
| Całkowita pamięciowa | O(n + k) |

Gdzie `k` to liczba znalezionych par.

Dowiedz się więcej

## 3. Alternatywa – sortowanie i dwa wskaźniki

Możemy również posortować tablicę i zastosować technikę Two Pointers.

javascript

```javascript

function findPairs(arr, targetSum) {
  const sorted = [...arr].sort((a, b) => a - b);
  const pairs = [];

  let left = 0;
  let right = sorted.length - 1;

  while (left < right) {
    const sum = sorted[left] + sorted[right];

    if (sum === targetSum) {
      pairs.push([sorted[left], sorted[right]]);
      left++;
      right--;
    } else if (sum < targetSum) {
      left++;
    } else {
      right--;
    }
  }

  return pairs;
}
```

Złożoność:

- Sortowanie: O(n log n).
- Przejście dwoma wskaźnikami: O(n).
- Łącznie: O(n log n).
- Pamięć: O(n) w tej implementacji (kopia tablicy).

Uwaga: Ta implementacja zwraca pary wartości, a nie wszystkie możliwe kombinacje indeksów. Przy powtarzających się wartościach może pomijać poprawne pary.

## 4. Porównanie rozwiązań

| Algorytm | Czasowa | Pamięciowa |
| --- | --- | --- |
| Dwie pętle | O(n²) | O(k) |
| Set (Hash Set) | O(n + k) | O(n + k) |
| Sortowanie + Two Pointers | O(n log n) | O(n + k) |

## 5. Które rozwiązanie wybrać?

Moja rekomendacja:

- Set – najlepszy wybór, jeśli zależy Ci na szybkości i chcesz znaleźć wszystkie pary indeksów (z zachowaniem wielokrotnych wystąpień).
- Two Pointers – dobry wybór, jeśli tablica jest już posortowana lub możesz ją posortować i interesują Cię unikalne pary wartości.
- Dwie pętle – najprostsze rozwiązanie, dobre dla małych tablic.

Ważny szczegół: jeśli wymaganiem jest znalezienie wszystkich par, to samo O(n) nie zawsze jest możliwe. Gdy wynik zawiera O(n²) par, samo ich wygenerowanie wymaga O(n²) czasu.

Na rozmowie rekrutacyjnej polecałbym przedstawić rozwiązanie z `Set` i wyjaśnić kompromis: zmniejszamy złożoność czasową z O(n²) do O(n + k), kosztem dodatkowej pamięci O(n).