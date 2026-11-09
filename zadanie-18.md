Oto 5 kluczowych praktyk bezpieczeństwa dla aplikacji Dockerowych w środowisku produkcyjnym, które pomagają ograniczyć ryzyko włamania, eskalacji uprawnień, wycieku danych i podatności w kontenerach.

## 1. Stosuj minimalne obrazy bazowe i regularnie je aktualizuj

Priorytet: wysoki- Korzystaj z minimalnych obrazów, np. `alpine`, `debian-slim` lub obrazów distroless.
- Unikaj instalowania zbędnych pakietów i narzędzi systemowych.
- Regularnie aktualizuj obrazy bazowe.
- Skanuj obrazy pod kątem podatności CVE za pomocą:
  - Trivy,
  - Docker Scout,
  - Grype.

Przykład:

dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

Warto również przypinać obrazy do konkretnych wersji lub digestów, zamiast używać `latest`.

## 2. Nigdy nie uruchamiaj kontenerów jako root

Priorytet: wysokiUruchamianie aplikacji z uprawnieniami administratora zwiększa skutki potencjalnego przejęcia kontenera.

Utwórz dedykowanego użytkownika:

dockerfile

```dockerfile
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

USER appuser
```

Dodatkowo:

- Unikaj `--privileged`.
- Ograniczaj capabilities Linuksa.
- Stosuj `no-new-privileges`.
- Rozważ uruchamianie kontenerów z systemem plików tylko do odczytu.

Przykład:

bash

```bash
docker run \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges:true \
  my-app:1.0
```

## 3. Zarządzaj sekretami w bezpieczny sposób

Nigdy nie umieszczaj haseł, tokenów API ani kluczy prywatnych bezpośrednio w:

- Dockerfile,
- obrazie kontenera,
- repozytorium Git,
- plikach konfiguracyjnych przechowywanych w repozytorium.

Zamiast tego wykorzystuj:

- Docker Secrets,
- HashiCorp Vault,
- AWS Secrets Manager,
- Azure Key Vault,
- Kubernetes Secrets (z odpowiednim szyfrowaniem).

Przykład w Docker Compose:

yaml

```yaml
services:
  app:
    image: my-app:1.0
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

Pamiętaj, że zmienne środowiskowe również mogą zostać ujawnione przez diagnostykę lub błędną konfigurację.

## 4. Ogranicz komunikację sieciową i dostęp do kontenerów

Nie każdy kontener powinien mieć dostęp do wszystkich usług i portów.

Dobre praktyki:

- Udostępniaj na zewnątrz tylko niezbędne porty.
- Oddzielaj sieci frontendowe i backendowe.
- Ograniczaj komunikację między kontenerami.
- Nie wystawiaj publicznie portu Docker API (`2375`).
- Nie montuj bez potrzeby `/var/run/docker.sock`.

Przykład:

yaml

```yaml
services:
  frontend:
    image: frontend:1.0
    ports:
      - "443:443"
    networks:
      - frontend

  backend:
    image: backend:1.0
    networks:
      - frontend
      - backend

  database:
    image: postgres:17
    networks:
      - backend

networks:
  frontend:
  backend:
    internal: true
```

W ten sposób baza danych nie jest bezpośrednio dostępna z zewnętrznej sieci.

## 5. Wdrażaj monitoring, logowanie i ciągłe skanowanie bezpieczeństwa

Bezpieczeństwo nie kończy się na uruchomieniu kontenera.

Warto wdrożyć:

- Monitoring podejrzanych procesów i aktywności.
- Centralizację logów.
- Skanowanie obrazów w CI/CD.
- Monitorowanie zmian w systemie plików.
- Alerty dotyczące nietypowego ruchu sieciowego.

Przydatne narzędzia:

| Narzędzie | Zastosowanie |
| --- | --- |
| Trivy | Skanowanie podatności obrazów |
| Falco | Wykrywanie podejrzanej aktywności runtime |
| Prometheus | Monitoring metryk |
| Grafana | Wizualizacja i alerty |
| Wazuh | Monitoring bezpieczeństwa i hostów |

## Podsumowanie – lista kontrolna produkcyjnego Dockera

| Praktyka | Co należy zapewnić? |
| --- | --- |
| 1. Bezpieczne obrazy | Minimalne obrazy, aktualizacje, skanowanie CVE |
| 2. Least Privilege | Użytkownik non-root, brak zbędnych uprawnień |
| 3. Secrets Management | Brak haseł i tokenów w obrazach |
| 4. Network Security | Segmentacja sieci, minimalna liczba otwartych portów |
| 5. Monitoring | Logi, alerty, skanowanie CI/CD i runtime |

Moja rekomendacja: zacznij od zasady Least Privilege, skanowania obrazów w pipeline CI/CD oraz bezpiecznego zarządzania sekretami. Te trzy obszary znacząco ograniczają ryzyko typowych incydentów związanych z kontenerami.

Warto też pamiętać, że bezpieczeństwo Dockera obejmuje nie tylko same kontenery, ale również hosta, Docker Engine, rejestr obrazów oraz pipeline CI/CD.



Pierwszą praktykę, czyli stosowanie minimalnych obrazów bazowych i ich regularne aktualizowanie, możesz wdrożyć bezpośrednio w `Dockerfile` oraz `docker-compose.yml`.

Pokażę Ci przykład dla aplikacji Python, ale podobne zasady można zastosować do Node.js, Java czy PHP.

## 1. Dockerfile – minimalny i bezpieczny obraz

Zamiast używać pełnego obrazu, np. `python:3.12`, zastosuj wariant `slim`.

Przykładowy Dockerfile:

dockerfile

```dockerfile

# Minimalny obraz bazowy
FROM python:3.12-slim

# Katalog roboczy
WORKDIR /app

# Instalacja zależności
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie kodu aplikacji
COPY . .

# Uruchomienie aplikacji
CMD ["python", "app.py"]
```

Dlaczego to lepsze?

- `slim` zawiera mniej zbędnych pakietów.
- `--no-cache-dir` ogranicza niepotrzebne dane w obrazie.
- Kopiowanie `requirements.txt` przed kodem aplikacji poprawia wykorzystanie cache Dockera.

## 2. Dodaj .dockerignore

To bardzo ważny element. Zapobiega kopiowaniu niepotrzebnych i potencjalnie wrażliwych plików do obrazu.

Utwórz plik `.dockerignore`:

text

```text

.git
.gitignore
.env
.env.*
*.pem
*.key
__pycache__
*.pyc
.pytest_cache
.venv
venv
node_modules
tests/
Dockerfile
docker-compose.yml
README.md
```

Dzięki temu:

- Nie kopiujesz lokalnego środowiska programistycznego.
- Nie umieszczasz przypadkowo sekretów w obrazie.
- Zmniejszasz rozmiar kontekstu budowania.

## 3. docker-compose.yml – wykorzystanie zoptymalizowanego obrazu

Przykładowa konfiguracja:

yaml

```yaml

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile

    image: my-app:1.0

    restart: unless-stopped

    ports:
      - "8000:8000"

    environment:
      PYTHONUNBUFFERED: "1"

    security_opt:
      - no-new-privileges:true
```

W tym przypadku Compose buduje obraz na podstawie Twojego Dockerfile.

## 4. Dodaj automatyczne skanowanie podatności

Polecam wykorzystać Trivy.

Po zbudowaniu obrazu uruchom:

bash

```bash
docker compose build

trivy image my-app:1.0
```

Możesz też sprawdzić podatności w konfiguracji:

bash

```bash
trivy config .
```

Trivy wykrywa m.in.:

- Znane podatności CVE.
- Podatne pakiety systemowe.
- Podatne zależności aplikacji.
- Problemy z konfiguracją Dockera.

## 5. Przypinaj wersje obrazów bazowych

Unikaj:

dockerfile

```dockerfile
FROM python:latest
```

Lepiej:

dockerfile

```dockerfile
FROM python:3.12-slim
```

Jeszcze bardziej powtarzalnym rozwiązaniem jest przypięcie obrazu do konkretnego digestu:

dockerfile

```dockerfile
FROM python:3.12-slim@sha256:TWOJ_RZECZYWISTY_DIGEST
```

Digest musi pochodzić z zaufanego rejestru. Aktualizuj go świadomie, po sprawdzeniu nowej wersji obrazu.

## 6. Docelowa procedura wdrażania

## Bezpieczny pipeline budowania obrazu

1. Build
   Budowanie obrazu Docker.
   `docker compose build`
2. Scan
   Sprawdzanie podatności obrazu.
   `trivy image my-app:1.0`
3. Test
   Testy aplikacji i obrazu.
4. Deploy
   Wdrożenie zatwierdzonego obrazu.
   `docker compose up -d`

## Co jeszcze warto zrobić?

Moja sugestia: wprowadź trzy dodatkowe zasady:

1. Ustaw przypięte wersje wszystkich obrazów w Compose, np. PostgreSQL zamiast `postgres:latest`.
2. Aktualizuj obrazy bazowe regularnie i ponownie skanuj je po aktualizacji.
3. Ustaw w CI/CD blokowanie wdrożenia, jeśli skanowanie wykryje podatności krytyczne lub wysokie, zgodnie z przyjętą polityką ryzyka.

Mogę też przygotować kompletny, produkcyjny przykład `Dockerfile` + `docker-compose.yml` + `.dockerignore` + pipeline GitHub Actions z automatycznym skanowaniem Trivy.