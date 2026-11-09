W przedstawionych logach Dockera widać problem z komunikacją kontenera z usługą działającą pod adresem `172.17.0.3` na porcie `5432`. Najprawdopodobniej chodzi o bazę danych PostgreSQL.

Przeanalizujmy poszczególne wpisy.

## 1. Analiza logów krok po kroku

### Pierwszy wpis – kontener uzyskał status healthy

text

```text
May 19 10:15:32
level=info
msg="Container 78a2b3c4 health status changed from starting to healthy"
```

- Kontener `78a2b3c4` zakończył fazę uruchamiania.
- Test kontrolny Docker Healthcheck zakończył się powodzeniem.
- Kontener został oznaczony jako `healthy`.

Wniosek: W tym momencie Docker uznał kontener za działający prawidłowo.

### Drugi wpis – problem z połączeniem

text

```text
May 19 10:16:45
level=info
msg="Container 78a2b3c4 failed to connect to 172.17.0.3:5432: connection refused"
```

To najważniejszy wpis w przedstawionych logach.

Oznacza on, że kontener próbował nawiązać połączenie z adresem:

- IP: `172.17.0.3`
- Port: `5432`
- Błąd: `connection refused`

Port `5432` jest domyślnym portem PostgreSQL.

Błąd `connection refused` oznacza, że próba połączenia została odrzucona. Najczęściej oznacza to, że pod wskazanym adresem nie działa proces nasłuchujący na tym porcie.

Możliwe przyczyny:

- Baza PostgreSQL nie została uruchomiona.
- Usługa PostgreSQL uległa awarii.
- PostgreSQL nasłuchuje na innym porcie.
- PostgreSQL jest skonfigurowany do nasłuchiwania wyłącznie na `localhost`.
- Kontener bazy danych został zrestartowany.
- Adres IP kontenera bazy danych uległ zmianie.

### Trzeci wpis – kontener zmienił status na unhealthy

text

```text
May 19 10:16:47
level=warning
msg="Container 78a2b3c4 health status changed from healthy to unhealthy"
```

- Docker wykrył niepowodzenie kontroli zdrowia.
- Kontener zmienił status z `healthy` na `unhealthy`.
- Oznacza to, że skonfigurowany Healthcheck nie przechodzi poprawnie.

Wniosek: Kontener działał wcześniej poprawnie, ale utracił możliwość komunikacji z usługą, od której zależy jego działanie.

## 2. Jakie problemy można zidentyfikować?

| Problem | Możliwa przyczyna | Potencjalny skutek |
| --- | --- | --- |
| Brak połączenia z PostgreSQL | Baza nie działa | Aplikacja nie może pobierać danych |
| Nieprawidłowa konfiguracja portu | Inny port niż 5432 | Brak komunikacji |
| Nieprawidłowy adres IP | Zmiana IP kontenera | Aplikacja łączy się z niewłaściwym hostem |
| Awaria PostgreSQL | Proces bazy zakończył działanie | Niedostępność danych |
| Nieprawidłowa konfiguracja sieci | Problem z komunikacją między kontenerami | Błędy połączeń |
| Nieudany Healthcheck | Brak odpowiedzi usługi zależnej | Status `unhealthy` |

## 3. Jak zdiagnozować problem?

Warto wykonać kilka poleceń na serwerze.

Krok 1. Sprawdzenie statusu kontenerów

bash

```bash
docker ps -a
```

Sprawdź, czy kontener aplikacji i kontener PostgreSQL są uruchomione.

Krok 2. Sprawdzenie logów PostgreSQL

bash

```bash
docker logs <postgres_container>
```

Szukaj błędów związanych z uruchamianiem bazy, awariami lub nasłuchiwaniem na porcie.

Krok 3. Sprawdzenie adresu IP kontenera PostgreSQL

bash

```bash
docker inspect <postgres_container>
```

Sprawdź sekcję `NetworkSettings`, aby ustalić aktualny adres IP.

Krok 4. Sprawdzenie dostępności portu 5432

Z poziomu kontenera aplikacji:

bash

```bash
nc -zv 172.17.0.3 5432
```

Jeżeli połączenie zostanie odrzucone, problem nadal występuje.

Krok 5. Sprawdzenie konfiguracji Healthcheck

bash

```bash
docker inspect 78a2b3c4
```

Zwróć uwagę na sekcję `Health`, szczególnie:

- `Status`
- `FailingStreak`
- `Log`

Pozwoli to ustalić, dlaczego Docker oznaczył kontener jako `unhealthy`.

## 4. Jakie rozwiązanie rekomenduję?

W pierwszej kolejności sprawdziłbym trzy rzeczy:

1. Czy PostgreSQL działa? – sprawdzenie statusu i logów kontenera bazy danych.
2. Czy PostgreSQL nasłuchuje na porcie 5432? – weryfikacja konfiguracji i dostępności portu.
3. Czy aplikacja korzysta z prawidłowego adresu bazy? – najlepiej używać nazwy usługi lub kontenera w sieci Docker zamiast sztywno wpisanego adresu IP.

Przykładowa konfiguracja `docker-compose.yml`:

yaml

```yaml
services:
  app:
    image: my-app
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: appdb
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5
```

W konfiguracji aplikacji należy wtedy używać:

text

```text
DB_HOST=db
DB_PORT=5432
```

## 5. Podsumowanie

Wykryty problemNajważniejszy problem to utrata połączenia z usługą dostępną pod adresem `172.17.0.3:5432`.

Przebieg zdarzeń wygląda następująco:

1. 10:15:32 – Kontener healthy
   Kontener działa prawidłowo, Healthcheck przechodzi.
2. 10:16:45 – Connection refused
   Próba połączenia z PostgreSQL kończy się niepowodzeniem.
3. 10:16:47 – Kontener unhealthy
   Kontrola zdrowia wykrywa problem i Docker zmienia status kontenera.

Moja główna hipoteza: PostgreSQL przestał nasłuchiwać na porcie `5432` albo jego kontener uległ awarii lub restartowi.

Warto jednak pamiętać, że sam status `unhealthy` nie oznacza automatycznie, że kontener został zatrzymany. Docker może nadal utrzymywać go w stanie `running`, mimo że Healthcheck zgłasza problemy.