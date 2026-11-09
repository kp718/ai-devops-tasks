Skrypt `jenkins_manager.py` jest prostym narzędziem do zarządzania zadaniami Jenkins z poziomu Pythona. Komunikuje się z serwerem Jenkins za pomocą jego REST API, dzięki czemu można pobierać informacje o zadaniach, sprawdzać statusy buildów i uruchamiać nowe buildy bez konieczności korzystania z interfejsu WWW.

Poniżej wyjaśniam poszczególne elementy skryptu.

## 1. Jakich bibliotek używa skrypt?

Skrypt korzysta głównie ze standardowych bibliotek Pythona oraz jednej zewnętrznej biblioteki.

| Biblioteka | Typ | Zastosowanie |
| --- | --- | --- |
| `requests` | Zewnętrzna | Wysyłanie żądań HTTP do Jenkins REST API |
| `requests.auth.HTTPBasicAuth` | Requests | Obsługa uwierzytelniania loginem i API Tokenem |
| `requests.exceptions` | Requests | Obsługa błędów komunikacji HTTP |
| `os` | Standardowa | Odczytywanie zmiennych środowiskowych |
| `sys` | Standardowa | Zakończenie programu z kodem błędu |

Instalacja wymaganej biblioteki:

bash

```bash
pip install requests
```

Nie potrzebujesz dodatkowych bibliotek Jenkins SDK. Komunikacja odbywa się bezpośrednio przez REST API.

## 2. Jak działa komunikacja z Jenkins API?

Schemat działania wygląda następująco:

Skrypt Python

jenkins\_manager.py

requests + HTTP Basic Auth

Jenkins Server

REST API / HTTP(S)

Odpowiedź HTTP / JSON

Wynik w Pythonie

Lista jobs, status buildów lub potwierdzenie uruchomienia

### Krok 1. Inicjalizacja klienta Jenkins

Klasa `JenkinsClient` odpowiada za komunikację z serwerem.

python

```python
class JenkinsClient:
    def __init__(self, url, username, token):
        self.url = url.rstrip("/")
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username, token)
        self.session.headers.update({
            "Accept": "application/json"
        })
        self.timeout = 15
```

Co się tutaj dzieje?

- `url` – adres serwera Jenkins.
- `username` – nazwa użytkownika Jenkins.
- `token` – API Token użytkownika.
- `requests.Session()` – tworzy sesję HTTP, którą można wykorzystywać wielokrotnie.
- `HTTPBasicAuth()` – konfiguruje uwierzytelnianie.
- `Accept: application/json` – informuje Jenkins, że oczekujemy odpowiedzi JSON.
- `timeout = 15` – maksymalny czas oczekiwania na odpowiedź.

### Krok 2. Wysyłanie żądań HTTP

Za komunikację odpowiada metoda `_request()`.

python

```python
response = self.session.request(
    method,
    url,
    timeout=self.timeout,
    **kwargs
)

response.raise_for_status()
```

Metoda obsługuje różne rodzaje błędów:

- `Timeout` – Jenkins nie odpowiedział w wyznaczonym czasie.
- `ConnectionError` – nie można połączyć się z serwerem.
- `HTTPError` – serwer zwrócił błąd HTTP, np. 401 lub 403.
- `RequestException` – inny problem związany z komunikacją.

Dzięki temu błędy nie muszą powodować niekontrolowanego zakończenia programu.

## 3. Jak działają poszczególne funkcje?

### A. Listowanie wszystkich zadań

Funkcja:

python

```python
def list_jobs(self):
```

Wysyła żądanie:

http

```http
GET /api/json?tree=jobs[name,url,color]
```

Jenkins zwraca listę zadań w formacie JSON.

Przykładowa odpowiedź:

json

```json
{
    "jobs": [
        {
            "name": "backend-build",
            "url": "https://jenkins.example.com/job/backend-build/",
            "color": "blue"
        },
        {
            "name": "frontend-build",
            "url": "https://jenkins.example.com/job/frontend-build/",
            "color": "red"
        }
    ]
}
```

Znaczenie pola `color`:

- `blue` – ostatni build zakończył się sukcesem.
- `red` – ostatni build zakończył się błędem.
- `blue_anime` lub `red_anime` – build jest wykonywany.
- `disabled` – zadanie jest wyłączone.

Funkcja wyświetla nazwy, statusy i adresy zadań.

### B. Sprawdzanie statusu ostatniego buildu

Funkcja:

python

```python
def get_last_build_status(self, job_name):
```

Wysyła żądanie:

http

```http
GET /job/backend-build/lastBuild/api/json
```

Pobiera informacje o ostatnim buildzie:

- numer buildu,
- wynik,
- informację, czy build nadal trwa,
- datę rozpoczęcia,
- adres buildu.

Przykładowa odpowiedź:

json

```json
{
    "number": 125,
    "result": "SUCCESS",
    "building": false,
    "timestamp": 1794230000000,
    "url": "https://jenkins.example.com/job/backend-build/125/"
}
```

Ważne: jeśli `building` ma wartość `true`, skrypt wyświetla `BUILDING`, niezależnie od pola `result`.

### C. Uruchamianie zadania

Funkcja:

python

```python
def trigger_job(self, job_name):
```

Wysyła żądanie:

http

```http
POST /job/backend-build/build
```

Jenkins otrzymuje polecenie uruchomienia nowego buildu.

Jeżeli operacja zostanie zaakceptowana, Jenkins zwykle zwraca HTTP `201 Created`.

Warto pamiętać, że odpowiedź potwierdza przyjęcie żądania, a nie zakończenie buildu.

## 4. Jak uruchomić skrypt?

Przyjmijmy następującą strukturę katalogu:

text

```text
jenkins-tool/
│
├── jenkins_manager.py
└── requirements.txt
```

Plik `requirements.txt`:

text

```text
requests>=2.31.0
```

### Krok 1. Instalacja zależności

bash

```bash
pip install -r requirements.txt
```

### Krok 2. Konfiguracja połączenia

Linux/macOS:

bash

```bash
export JENKINS_URL="https://jenkins.example.com"
export JENKINS_USER="admin"
export JENKINS_TOKEN="your-api-token"
```

Windows PowerShell:

powershell

```powershell
$env:JENKINS_URL="https://jenkins.example.com"
$env:JENKINS_USER="admin"
$env:JENKINS_TOKEN="your-api-token"
```

### Krok 3. Uruchomienie programu

bash

```bash
python jenkins_manager.py
```

Pojawi się menu:

text

```text
========== JENKINS MANAGER ==========
1. Lista wszystkich zadań
2. Status ostatniego buildu
3. Uruchom zadanie
4. Wyjście

Wybierz opcję:
```

## 5. Przykładowe użycie

Przykład 1. Pobieranie listy zadań

Wejście

text

```text
Wybierz opcję: 1
```

Wynik

text

```text
=== LISTA ZADAŃ ===

Nazwa: backend-build
Status: blue

Nazwa: frontend-build
Status: red
```

Przykład 2. Sprawdzanie statusu buildu

Wejście

text

```text
Wybierz opcję: 2
Podaj nazwę zadania: backend-build
```

Wynik

text

```text
=== OSTATNI BUILD: backend-build ===

Numer: 125
Status: SUCCESS
URL: https://jenkins.example.com/job/backend-build/125/
```

Przykład 3. Uruchomienie zadania

Wejście

text

```text
Wybierz opcję: 3
Podaj nazwę zadania: backend-build

Czy uruchomić 'backend-build'? (tak/nie): tak
```

Wynik

text

```text
[OK] Zadanie 'backend-build' zostało uruchomione.
HTTP Status: 201
```

## 6. Przykładowe błędy

| Kod HTTP | Znaczenie | Możliwa przyczyna |
| --- | --- | --- |
| 401 | Unauthorized | Nieprawidłowy login lub token |
| 403 | Forbidden | Brak wymaganych uprawnień |
| 404 | Not Found | Nie istnieje zadanie lub endpoint |
| 500 | Internal Server Error | Błąd po stronie Jenkins |
| Timeout | Przekroczony czas | Serwer nie odpowiada |

Użytkownik Jenkins powinien mieć odpowiednie uprawnienia, w szczególności:

- `Overall/Read` – dostęp do informacji o Jenkins.
- `Job/Read` – odczytywanie zadań.
- `Job/Build` – uruchamianie buildów.

## 7. Jak można rozbudować skrypt?

Jeśli chcesz wykorzystać go w środowisku DevOps, proponuję następujące rozszerzenia:

| Funkcjonalność | Opis | Przydatność |
| --- | --- | --- |
| Historia buildów | Pobieranie ostatnich 10 buildów | Wysoka |
| Parametry buildów | Uruchamianie `buildWithParameters` | Wysoka |
| Monitorowanie | Oczekiwanie na zakończenie buildu | Wysoka |
| Console Output | Pobieranie logów z wykonania | Wysoka |
| Foldery Jenkins | Obsługa zagnieżdżonych jobs | Średnia |
| Logging | Zapisywanie operacji do pliku | Wysoka |
| CLI | Obsługa poleceń przez argparse | Wysoka |

Podsumowując: najważniejszą biblioteką jest `requests`, która odpowiada za całą komunikację HTTP z Jenkins REST API. `HTTPBasicAuth` zapewnia uwierzytelnianie, a pozostałe biblioteki standardowe Pythona obsługują konfigurację i działanie programu. Dzięki takiemu podejściu możesz automatyzować podstawowe operacje Jenkins bez korzystania z interfejsu WWW.