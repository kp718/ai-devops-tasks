text

```text
       +------------------+
       |      KLIENT      |
       | (przeglądarka /   |
       |    aplikacja)     |
       +------------------+
                |
                | Żądanie HTTP
                v
       +------------------+
       | SERWER APLIKACJI |
       |                  |
       | Logika biznesowa |
       | Przetwarzanie    |
       | żądań             |
       +------------------+
                |
                | Zapytanie SQL
                v
       +------------------+
       |  BAZA DANYCH     |
       |                  |
       | Przechowywanie   |
       | danych           |
       +------------------+
                |
                | Wyniki zapytania
                v
       +------------------+
       | SERWER APLIKACJI |
       +------------------+
                |
                | Odpowiedź HTTP
                v
       +------------------+
       |      KLIENT      |
       +------------------+
```

Przepływ komunikacji:

1. Klient wysyła żądanie do serwera aplikacji.
2. Serwer przetwarza żądanie i komunikuje się z bazą danych.
3. Baza danych zwraca wyniki.
4. Serwer odsyła odpowiedź do klienta.


-----------------------------------------------------------------------------------------------------------------------------------------------

Poniżej znajduje się rozszerzony diagram ASCII Art z opisami poszczególnych elementów oraz kierunkami przepływu danych.

## Diagram architektury systemu

text

```text
     UŻYTKOWNIK
          |
          | Interakcja z systemem
          v
+---------------------------+
|          KLIENT           |
|---------------------------|
| - Interfejs użytkownika   |
| - Przeglądarka / aplikacja|
| - Wyświetlanie danych     |
| - Wysyłanie żądań         |
+---------------------------+
          |
          | 1. Żądanie HTTP/HTTPS
          |    (np. GET, POST)
          v
+---------------------------+
|     SERWER APLIKACJI      |
|---------------------------|
| - Obsługa żądań klienta   |
| - Logika biznesowa        |
| - Walidacja danych        |
| - Autoryzacja             |
| - Przetwarzanie danych    |
+---------------------------+
          |
          | 2. Zapytanie SQL
          |    (SELECT, INSERT,
          |     UPDATE, DELETE)
          v
+---------------------------+
|        BAZA DANYCH        |
|---------------------------|
| - Przechowywanie danych   |
| - Wyszukiwanie rekordów   |
| - Aktualizacja danych     |
| - Zarządzanie danymi      |
+---------------------------+
          |
          | 3. Wyniki zapytania
          |    (rekordy / status)
          v
+---------------------------+
|     SERWER APLIKACJI      |
|---------------------------|
| - Odbiór wyników          |
| - Przetwarzanie wyników   |
| - Przygotowanie odpowiedzi|
+---------------------------+
          |
          | 4. Odpowiedź HTTP/HTTPS
          |    (JSON / HTML)
          v
+---------------------------+
|          KLIENT           |
|---------------------------|
| - Odbiór odpowiedzi       |
| - Aktualizacja interfejsu |
| - Wyświetlenie wyników    |
+---------------------------+
          |
          v
     UŻYTKOWNIK
```

## Opis przepływu danych

| Nr | Kierunek | Opis |
| --- | --- | --- |
| 1 | Klient → Serwer | Wysłanie żądania HTTP/HTTPS |
| 2 | Serwer → Baza | Wysłanie zapytania SQL |
| 3 | Baza → Serwer | Zwrócenie wyników zapytania |
| 4 | Serwer → Klient | Przesłanie odpowiedzi HTTP/HTTPS |

## Znaczenie poszczególnych warstw

- Klient (Frontend) – odpowiada za komunikację z użytkownikiem i prezentację danych.
- Serwer aplikacji (Backend) – realizuje logikę biznesową, przetwarza żądania i zarządza komunikacją z bazą.
- Baza danych (Database) – przechowuje dane i obsługuje operacje na nich.

Ważne: Klient nie komunikuje się bezpośrednio z bazą danych. Wszystkie operacje przechodzą przez serwer aplikacji, który kontroluje dostęp i przetwarzanie danych.
