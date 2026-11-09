# Instalacja i uruchomienie Jenkins z konfiguracją JCasC

Jenkins Configuration as Code (JCasC) pozwala zarządzać konfiguracją Jenkinsa za pomocą plików YAML zamiast ręcznego ustawiania opcji w interfejsie WWW.

W praktyce oznacza to, że możesz:

- automatycznie skonfigurować nową instancję Jenkins;
- zainstalować wymagane pluginy;
- skonfigurować Maven, Node.js i Docker;
- automatycznie utworzyć zadania Pipeline;
- przechowywać konfigurację w Git i odtwarzać środowisko na innych serwerach.

Poniżej przedstawiam przykładowe wdrożenie z wykorzystaniem Dockera i Docker Compose.

## 1. Wymagania wstępne

Przygotuj:

- Docker Engine;
- Docker Compose v2;
- dostęp do internetu podczas pobierania obrazu i pluginów;
- katalog na konfigurację JCasC.

Sprawdź, czy Docker działa:

bash

```bash
docker --version
docker compose version
```

## 2. Przygotowanie struktury projektu

Utwórz katalog projektu:

bash

```bash
mkdir -p jenkins-config/casc
mkdir -p jenkins-config/plugins
cd jenkins-config
```

Struktura katalogów:

text

```text
jenkins-config/
├── casc/
│   └── jenkins.yaml
├── plugins/
│   └── plugins.txt
├── Dockerfile
├── docker-compose.yml
└── .env
```

Poszczególne pliki pełnią następujące funkcje:

| Plik | Przeznaczenie |
| --- | --- |
| `jenkins.yaml` | Konfiguracja JCasC |
| `plugins.txt` | Lista pluginów Jenkins |
| `Dockerfile` | Budowanie obrazu Jenkins |
| `docker-compose.yml` | Uruchamianie kontenera |
| `.env` | Zmienne środowiskowe i hasła |

## 3. Przygotowanie listy pluginów

W pliku `plugins/plugins.txt` umieść:

text

```text
configuration-as-code
workflow-aggregator
job-dsl
git
credentials
ssh-credentials
matrix-auth
timestamper
ws-cleanup
pipeline-stage-view
maven-plugin
nodejs
docker-workflow
```

Ważne: JCasC nie instaluje pluginów. Muszą one być dostępne przed załadowaniem konfiguracji YAML. W naszym przykładzie zostaną zainstalowane podczas budowania obrazu Dockera.

Jenkins plugin

+2

## 4. Przygotowanie Dockerfile

Utwórz plik `Dockerfile`:

dockerfile

```dockerfile

FROM jenkins/jenkins:lts-jdk21

USER root

# Instalacja narzędzi systemowych
RUN apt-get update && \
    apt-get install -y docker.io maven && \
    rm -rf /var/lib/apt/lists/*

USER jenkins

# Instalacja pluginów Jenkins
COPY plugins/plugins.txt /usr/share/jenkins/ref/plugins.txt

RUN jenkins-plugin-cli \
    --plugin-file /usr/share/jenkins/ref/plugins.txt

# Lokalizacja konfiguracji JCasC
ENV CASC_JENKINS_CONFIG=/var/jenkins_home/casc/jenkins.yaml
```

Co robi ten plik?

1. Pobiera oficjalny obraz Jenkins LTS.
2. Instaluje Maven i Docker CLI.
3. Kopiuje listę wymaganych pluginów.
4. Instaluje pluginy i ich zależności.
5. Ustawia zmienną środowiskową wskazującą lokalizację konfiguracji JCasC.

## 5. Przygotowanie pliku docker-compose.yml

Utwórz plik `docker-compose.yml`:

yaml

```yaml

services:
  jenkins:
    build:
      context: .

    container_name: jenkins

    restart: unless-stopped

    ports:
      - "8080:8080"
      - "50000:50000"

    environment:
      CASC_JENKINS_CONFIG: /var/jenkins_home/casc/jenkins.yaml
      JENKINS_ADMIN_USER: ${JENKINS_ADMIN_USER}
      JENKINS_ADMIN_PASSWORD: ${JENKINS_ADMIN_PASSWORD}

    volumes:
      # Trwałe dane Jenkins
      - jenkins_home:/var/jenkins_home

      # Konfiguracja JCasC
      - ./casc:/var/jenkins_home/casc:ro

volumes:
  jenkins_home:
```

Wyjaśnienie:

- `8080` – interfejs WWW Jenkins.
- `50000` – komunikacja z agentami przez inbound TCP.
- `jenkins_home` – trwałe przechowywanie danych Jenkins.
- `./casc` – katalog z plikiem YAML.
- `restart: unless-stopped` – automatyczne uruchamianie kontenera po restarcie hosta.

Port 50000 możesz pominąć, jeśli nie korzystasz z agentów komunikujących się przez inbound TCP.

## 6. Przygotowanie zmiennych środowiskowych

Utwórz plik `.env`:

bash

```bash
JENKINS_ADMIN_USER=admin
JENKINS_ADMIN_PASSWORD=ChangeThisPassword123!
```

Nie umieszczaj tego pliku w publicznym repozytorium Git. Dodaj go do `.gitignore`:

text

```text
.env
```

Jenkins wykorzysta te zmienne do utworzenia konta administratora podczas inicjalizacji.

## 7. Uruchomienie Jenkinsa

W katalogu głównym projektu wykonaj:

Krok 1. Zbudowanie obrazu:

bash

```bash
docker compose build
```

Krok 2. Uruchomienie kontenera:

bash

```bash
docker compose up -d
```

Krok 3. Sprawdzenie statusu:

bash

```bash
docker compose ps
```

Krok 4. Sprawdzenie logów:

bash

```bash
docker compose logs -f jenkins
```

W logach powinny pojawić się informacje o:

- uruchamianiu Jenkins;
- ładowaniu pluginów;
- inicjalizacji Configuration as Code;
- ładowaniu konfiguracji YAML;
- tworzeniu zadania Pipeline.

Krok 5. Otwarcie interfejsu Jenkins:

Otwórz w przeglądarce:

[http://localhost:8080](<http://localhost:8080?utm_source=chatgpt.com>)

Zaloguj się danymi z pliku `.env`.

## 8. Ważna korekta konfiguracji JCasC

Warto poprawić jedną rzecz w poprzednim szablonie: konfiguracja globalnych narzędzi powinna znajdować się w głównej sekcji `tool:`, a nie wewnątrz `jenkins:`.

Prawidłowy układ wygląda następująco:

yaml

```yaml

jenkins:
  systemMessage: "Jenkins configured using JCasC"
  numExecutors: 2
  mode: NORMAL
  quietPeriod: 5

tool:
  maven:
    installations:
      - name: "Maven-3.9"
        home: "/opt/maven"

  nodejs:
    installations:
      - name: "NodeJS-20"
        home: "/opt/nodejs"

unclassified:
  location:
    url: "http://localhost:8080/"
    adminAddress: "admin@example.com"
```

To istotne, ponieważ JCasC rozróżnia sekcje `jenkins`, `tool`, `unclassified` i `credentials`.

Jenkins

+1

Pamiętaj też o dwóch dodatkowych kwestiach:

- Ścieżki `/opt/maven` i `/opt/nodejs` muszą istnieć w środowisku wykonawczym. Samo zdefiniowanie instalacji nie pobiera tych narzędzi. Możesz wykorzystać instalatory zarządzane przez odpowiednie pluginy.
- Docker CLI zainstalowany w kontenerze nie oznacza jeszcze dostępu do demona Docker. Jeśli chcesz wykonywać `docker build`, musisz zapewnić agentowi dostęp do demona, np. przez odpowiednio zabezpieczony zdalny Docker Engine.

## 9. Weryfikacja konfiguracji JCasC

Po uruchomieniu Jenkins przejdź do:

1. `Manage Jenkins`.
2. `Configuration as Code`.
3. Wybierz `View Configuration`.

Możesz tam sprawdzić aktualnie załadowaną konfigurację YAML.

Następnie zweryfikuj:

| Element | Gdzie sprawdzić |
| --- | --- |
| Liczba executorów | Manage Jenkins → Nodes |
| Maven | Manage Jenkins → Tools |
| Node.js | Manage Jenkins → Tools |
| Pluginy | Manage Jenkins → Plugins |
| Zadanie Pipeline | Dashboard |
| Timeout | Konfiguracja Pipeline |

Jeśli zmienisz plik `jenkins.yaml`, możesz przeładować konfigurację przez:

`Manage Jenkins → Configuration as Code → Reload existing configuration`

Nie trzeba restartować Jenkinsa po każdej zmianie JCasC.

Jenkins

## 10. Uruchomienie przykładowego Pipeline

Po poprawnym załadowaniu konfiguracji na dashboardzie powinno pojawić się zadanie:

example-pipeline

Job DSL

Kliknij zadanie, a następnie `Build Now`.

Przykładowy przebieg:

## example-pipeline

1. Checkout
   Pobranie kodu z repozytorium Git.
2. Build
   Budowanie aplikacji przez Maven.
3. Test
   Uruchomienie testów jednostkowych.
4. Node.js Build
   Instalacja zależności i budowanie frontendu.
5. Docker Build
   Budowanie obrazu kontenera (wymaga dostępu do demona Docker).

Timeout 30 minut jest ustawiany w sekcji `options` przykładowego Pipeline i dotyczy pojedynczego wykonania zadania.

## 11. Przydatne komendy administracyjne

| Operacja | Komenda |
| --- | --- |
| Uruchomienie | `docker compose up -d` |
| Zatrzymanie | `docker compose stop` |
| Restart | `docker compose restart` |
| Logi | `docker compose logs -f jenkins` |
| Status | `docker compose ps` |
| Zatrzymanie i usunięcie kontenera | `docker compose down` |
| Ponowne budowanie obrazu | `docker compose build --no-cache` |

Uwaga: `docker compose down -v` usuwa również wolumen z danymi Jenkins, dlatego nie używaj tej komendy, jeśli chcesz zachować konfigurację, historię zadań i dane użytkowników.

## 12. Dokumentacja

Przydatne oficjalne materiały:

- [Jenkins – Configuration as Code](<https://www.jenkins.io/doc/book/managing/casc/?utm_source=chatgpt.com>).
- [JCasC Plugin](<https://plugins.jenkins.io/configuration-as-code/?utm_source=chatgpt.com>).
- [Jenkins Docker – oficjalne repozytorium](<https://github.com/jenkinsci/docker?utm_source=chatgpt.com>).
- [Job DSL Plugin](<https://plugins.jenkins.io/job-dsl/?utm_source=chatgpt.com>).

Moja rekomendacja: traktuj plik `jenkins.yaml` jako główne źródło konfiguracji instancji Jenkins, przechowuj go w Git i testuj każdą zmianę na osobnej instancji przed wdrożeniem produkcyjnym. Pamiętaj również, że dostęp do plików JCasC powinien być ograniczony do zaufanych administratorów.