Do walidacji adresu IPv4 możesz użyć następującego wyrażenia regularnego (regex):

## 1. Wyrażenie regularne

regex

```regex
^(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}$
```

To wyrażenie sprawdza, czy adres składa się z dokładnie czterech liczb oddzielonych kropkami, a każda liczba mieści się w zakresie od `0` do `255`.

## 2. Jak działa regex?

Rozłóżmy go na części:

| Fragment | Znaczenie |
| --- | --- |
| `^` | Początek tekstu |
| `25[0-5]` | Liczby od 250 do 255 |
| `2[0-4][0-9]` | Liczby od 200 do 249 |
| `1[0-9]{2}` | Liczby od 100 do 199 |
| `[1-9]?[0-9]` | Liczby od 0 do 99 |
| `\.` | Dosłowna kropka oddzielająca oktety |
| `(...)` | Grupa alternatyw |
| `{3}` | Powtórzenie poprzedniej grupy dokładnie 3 razy |
| `$` | Koniec tekstu |

Najważniejszy fragment:

regex

```regex
(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])
```

Odpowiada on za walidację pojedynczego oktetu, czyli jednej z czterech liczb adresu IPv4.

Dzięki temu:

- `192` jest poprawne.
- `255` jest poprawne.
- `0` jest poprawne.
- `256` jest niepoprawne.
- `999` jest niepoprawne.

## 3. Testowanie na przykładach

Poniżej przykładowe adresy i oczekiwane wyniki:

| Adres IPv4 | Wynik | Uzasadnienie |
| --- | --- | --- |
| `192.168.1.1` | Poprawny | Wszystkie oktety są w zakresie 0–255 |
| `127.0.0.1` | Poprawny | Poprawny adres loopback |
| `255.255.255.255` | Poprawny | Maksymalna wartość każdego oktetu |
| `0.0.0.0` | Poprawny | Minimalna wartość każdego oktetu |
| `192.168.1.256` | Niepoprawny | 256 przekracza dopuszczalny zakres |
| `192.168.1` | Niepoprawny | Brakuje czwartego oktetu |
| `192.168.1.1.1` | Niepoprawny | Pięć oktetów zamiast czterech |
| `192.168.-1.1` | Niepoprawny | Ujemna wartość |
| `192.168.1.abc` | Niepoprawny | Zawiera litery |
| `300.168.1.1` | Niepoprawny | 300 przekracza zakres |

## 4. Przykład użycia w JavaScript

Możesz wykorzystać regex w JavaScript za pomocą metody `test()`:

javascript

```javascript
const ipv4Regex = /^(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}$/;

const addresses = [
    "192.168.1.1",
    "127.0.0.1",
    "255.255.255.255",
    "192.168.1.256",
    "192.168.1",
    "300.168.1.1"
];

addresses.forEach(address => {
    console.log(address, ipv4Regex.test(address));
});
```

Wynik:

text

```text
192.168.1.1 true
127.0.0.1 true
255.255.255.255 true
192.168.1.256 false
192.168.1 false
300.168.1.1 false
```

## 5. Ważna uwaga

Powyższy regex nie akceptuje zer wiodących, np. `192.168.001.1`.

Jest to celowe, ponieważ taki zapis nie jest standardową, kanoniczną reprezentacją adresu IPv4.

Podsumowanie: Regex sprawdza składnię adresu IPv4, liczbę oktetów oraz zakres wartości każdego oktetu (0–255). Nie sprawdza natomiast, czy adres jest faktycznie przypisany do urządzenia lub dostępny w sieci.