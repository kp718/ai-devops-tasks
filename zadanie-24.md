Na podstawie przedstawionych metryk można stwierdzić, że serwer API działa stosunkowo dobrze pod względem średniego czasu odpowiedzi i wykorzystania CPU, ale widzę trzy potencjalne obszary problemowe: błędy 5xx, wysokie opóźnienia dla najwolniejszych zapytań oraz niewielki zapas pamięci RAM.

Poniżej szczegółowa analiza.

## 1. Analiza poszczególnych metryk

### Czas odpowiedzi API

| Metryka | Wynik | Ocena |
| --- | --- | --- |
| Średni czas odpowiedzi | 230 ms | Dobry |
| P95 | 450 ms | Dobry |
| P99 | 1200 ms | Do analizy |

Interpretacja:

- Średnia 230 ms jest dobrym wynikiem dla większości typowych API.
- P95 = 450 ms oznacza, że 95% zapytań kończy się w czasie nieprzekraczającym 450 ms.
- P99 = 1200 ms oznacza, że 1% zapytań trwa co najmniej około 1,2 sekundy.

Potencjalny problem: różnica między P95 i P99 jest dość duża. Sugeruje to, że niewielka część zapytań doświadcza znacznie większych opóźnień.

Możliwe przyczyny:

- Wolne zapytania SQL.
- Brak odpowiednich indeksów w bazie danych.
- Problemy z zewnętrznymi API.
- Zbyt długie operacje wykonywane synchronicznie.
- Okresowe przeciążenie serwera.

Moja sugestia: przeanalizować najwolniejsze 1% zapytań i zidentyfikować konkretne endpointy odpowiedzialne za opóźnienia.

### Liczba zapytań i błędy 5xx

# 15 000

Zapytań w ciągu 24h

# 120

Błędów 5xx

Wskaźnik błędów:

$$
\frac{120}{15000}\times100 = 0{,}8\%
$$

Wymaga uwagiOznacza to, że około 8 na 1000 zapytań kończy się błędem serwera.

To istotny problem, szczególnie jeśli API obsługuje krytyczne funkcje biznesowe.

Warto sprawdzić:

- HTTP 500 – błędy aplikacji, nieobsłużone wyjątki.
- HTTP 502 – problemy z komunikacją z usługami nadrzędnymi.
- HTTP 503 – niedostępność lub przeciążenie usług.
- HTTP 504 – przekroczenie limitu czasu oczekiwania.

Zalecam również sprawdzić, czy błędy występują równomiernie, czy pojawiają się w określonych godzinach.

### Wykorzystanie CPU

Średnie wykorzystanie CPU

# 45%

Maksymalne wykorzystanie CPU

# 80%

Interpretacja:

- Średnie 45% oznacza, że serwer ma jeszcze spory zapas mocy obliczeniowej.
- Maksymalne 80% wskazuje na okresowe wzrosty obciążenia.

Na ten moment CPU nie wygląda na główne ograniczenie wydajności.

Warto jednak sprawdzić:

- Czy CPU osiąga 80% regularnie?
- Jak długo utrzymują się takie wartości?
- Czy wzrost CPU koreluje ze wzrostem P95/P99 i błędów 5xx?

### Wykorzystanie pamięci RAM

Średnie wykorzystanie

# 2,1 GB

Maksymalne wykorzystanie

# 3,5 GB

Dostępna pamięć: 4 GB

87,5% wykorzystania

Najważniejszy obszar ryzykaMaksymalne wykorzystanie pamięci wynosi 87,5%.

Pozostaje jedynie 0,5 GB wolnej pamięci.

To może prowadzić do:

- Wydłużenia czasu odpowiedzi przez garbage collection.
- OOM Killera (systemowego zakończenia procesu z powodu braku pamięci).
- Restartów aplikacji.
- Problemów z obsługą nagłych wzrostów ruchu.
- Pogorszenia stabilności serwera.

Warto sprawdzić, czy pamięć stopniowo rośnie w czasie. Może to wskazywać na memory leak.

## 2. Najważniejsze zidentyfikowane problemy

Moja ocena priorytetów:

| Problem | Priorytet | Uzasadnienie |
| --- | --- | --- |
| Wykorzystanie RAM do 87,5% | Wysoki | Mały zapas pamięci |
| Błędy 5xx – 0,8% | Wysoki | Problemy z niezawodnością |
| P99 = 1200 ms | Średni | Wolne pojedyncze zapytania |
| CPU max 80% | Średni | Okresowe skoki obciążenia |
| Średni czas 230 ms | Dobry | Brak istotnych zastrzeżeń |

## 3. Co sugeruję poprawić?

Podzieliłbym działania na cztery obszary.

### A. Optymalizacja pamięci RAM

Najważniejsze działania:

1. Wykonać profilowanie pamięci aplikacji.
2. Sprawdzić, czy nie występują memory leaks.
3. Zoptymalizować cache – szczególnie jego maksymalny rozmiar i politykę wygaszania.
4. Sprawdzić wielkość connection pool do bazy danych.
5. Ograniczyć przechowywanie dużych obiektów w pamięci.
6. Rozważyć zwiększenie RAM z 4 GB do 6–8 GB, jeśli profilowanie wykaże, że obecne zasoby są niewystarczające.

Nie zwiększałbym jednak pamięci bez wcześniejszego sprawdzenia jej rzeczywistego wykorzystania.

### B. Optymalizacja zapytań API

Skupiłbym się na najwolniejszych endpointach.

Proponowane działania:

- Analiza zapytań SQL za pomocą `EXPLAIN ANALYZE`.
- Dodanie brakujących indeksów.
- Wykorzystanie cache dla często odczytywanych danych.
- Wprowadzenie paginacji dla dużych wyników.
- Ograniczenie liczby zapytań do bazy danych (np. problem N+1).
- Przeniesienie długotrwałych operacji do kolejek asynchronicznych.

Szczególnie ważne jest zmniejszenie P99 z 1200 ms.

### C. Redukcja błędów 5xx

Zalecam:

- Wdrożenie centralnego logowania błędów.
- Grupowanie błędów według endpointu i kodu HTTP.
- Dodanie monitorowania wyjątków aplikacji.
- Wprowadzenie timeoutów dla zewnętrznych usług.
- Stosowanie retry z exponential backoff dla operacji, które można bezpiecznie ponawiać.
- Zastosowanie circuit breaker dla zawodnych usług zewnętrznych.

Ważne: retry powinno być ograniczone i stosowane ostrożnie, aby nie zwiększać przeciążenia.

### D. Monitoring i skalowanie

Warto wdrożyć monitoring w czasie rzeczywistym, np. za pomocą:

- Prometheus – zbieranie metryk.
- Grafana – dashboardy.
- OpenTelemetry – distributed tracing.
- Sentry – monitorowanie wyjątków.

Szczególnie polecam dashboard pokazujący korelację między:

- Czasem odpowiedzi P95/P99.
- Wykorzystaniem CPU.
- Wykorzystaniem RAM.
- Liczbą błędów 5xx.
- Liczbą aktywnych połączeń do bazy danych.

## 4. Proponowane cele optymalizacyjne

Jako wstępne cele przyjąłbym:

| Metryka | Obecnie | Proponowany cel |
| --- | --- | --- |
| Średni czas odpowiedzi | 230 ms | poniżej 200 ms |
| P95 | 450 ms | poniżej 350 ms |
| P99 | 1200 ms | poniżej 700 ms |
| Błędy 5xx | 0,8% | poniżej 0,1% |
| Średnie CPU | 45% | poniżej 60% |
| Maksymalne RAM | 87,5% | poniżej 75% |

Są to orientacyjne cele optymalizacyjne, a nie uniwersalne standardy. Powinny zostać dostosowane do wymagań biznesowych i SLA.

## 5. Plan działania – kolejność wdrożenia

1. Etap 1 – Diagnostyka (najpierw)
   - Przeanalizować błędy 5xx.
   - Sprawdzić logi aplikacji.
   - Zidentyfikować najwolniejsze endpointy.
   - Sprawdzić historię wykorzystania RAM.
2. Etap 2 – Optymalizacja
   - Poprawić zapytania SQL.
   - Zoptymalizować cache.
   - Usunąć potencjalne memory leaks.
   - Zoptymalizować obsługę wyjątków i timeoutów.
3. Etap 3 – Testy wydajnościowe
   - Wykonać testy obciążeniowe.
   - Sprawdzić zachowanie przy 2–3-krotnym wzroście ruchu.
   - Zweryfikować P95 i P99.
   - Sprawdzić stabilność pamięci.
4. Etap 4 – Skalowanie i monitoring
   - Rozważyć zwiększenie RAM.
   - Wdrożyć alerty.
   - Ustawić automatyczne skalowanie, jeśli infrastruktura na to pozwala.
   - Monitorować trendy i regresje wydajności.

## 6. Moja końcowa ocena

Ogólny stan serwera

Wymaga optymalizacji

Serwer nie wygląda na przeciążony pod względem średniego wykorzystania CPU, ale ma pewne problemy ze stabilnością i wydajnością skrajnych przypadków.

Trzy rzeczy, którymi zająłbym się w pierwszej kolejności:

1. Zredukowanie błędów 5xx z 0,8%.
2. Znalezienie przyczyny wysokiego P99.
3. Zwiększenie bezpieczeństwa pamięciowego – obecny szczyt 3,5 GB przy dostępnych 4 GB daje niewielki margines.

## 7. Dodatkowe informacje, które pomogłyby w dokładniejszej diagnozie

Chciałbym ustalić jeszcze jedną ważną rzecz: na jakiej technologii działa Twoje API?

Czy jest to:

- Node.js / Express / NestJS
- Python / FastAPI / Django
- Java / Spring Boot
- PHP / Laravel
- .NET / ASP.NET Core
- Inna technologia?

Na tej podstawie mogę zaproponować konkretne techniki profilowania, optymalizacji pamięci, konfigurację connection pool oraz ustawienia serwera, które pomogą rozwiązać zidentyfikowane problemy.