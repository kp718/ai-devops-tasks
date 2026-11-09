Jenkins Pipeline to mechanizm automatyzacji procesów CI/CD (Continuous Integration / Continuous Delivery), który pozwala automatycznie pobierać kod źródłowy, instalować zależności, uruchamiać testy, budować aplikację i publikować jej artefakty, np. obrazy Docker.

W naszym przykładzie wykorzystujemy Declarative Pipeline, czyli deklaratywną składnię Jenkinsa, która pozwala w przejrzysty sposób definiować etapy procesu CI/CD.

Przeanalizujmy cały Jenkinsfile krok po kroku.

# 1. Struktura główna Jenkinsfile

groovy

```groovy
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'moj-rejestr/node-app'
        DOCKER_TAG = 'latest'
        DOCKER_CREDENTIALS = 'docker-hub-credentials'
    }

    stages {
        // Etapy pipeline
    }

    post {
        // Akcje wykonywane po zakończeniu pipeline
    }
}
```

### `pipeline`

Jest głównym blokiem deklaratywnego pipeline. Wszystkie etapy, zmienne środowiskowe i akcje końcowe definiujemy wewnątrz tego bloku.

### `agent any`

Określa, na jakim agencie Jenkins ma wykonywać zadania.

- `any` – Jenkins wybiera dowolnego dostępnego agenta.
- `none` – pipeline nie przypisuje agenta globalnie; można przypisywać go poszczególnym etapom.
- `label 'docker'` – wybiera agenta posiadającego etykietę `docker`.

W naszym przypadku Jenkins może wykorzystać dowolnego dostępnego agenta.

Dobra praktyka: W większych środowiskach warto stosować etykiety agentów, aby mieć kontrolę nad tym, gdzie wykonywane są zadania, np. `nodejs`, `docker` czy `linux`.

### `environment`

Definiuje zmienne środowiskowe dostępne podczas wykonywania pipeline.

| Zmienna | Znaczenie |
| --- | --- |
| `DOCKER_IMAGE` | Nazwa obrazu Docker |
| `DOCKER_TAG` | Tag obrazu |
| `DOCKER_CREDENTIALS` | Identyfikator poświadczeń w Jenkinsie |

Dzięki temu nie musimy wielokrotnie wpisywać tych samych wartości w różnych etapach.

Dobra praktyka: Dane wrażliwe, takie jak hasła, tokeny i klucze API, powinny być przechowywane w Jenkins Credentials, a nie bezpośrednio w Jenkinsfile.

# 2. Etap Checkout – pobieranie kodu

groovy

```groovy
stage('Checkout') {
    steps {
        echo 'Pobieranie kodu z repozytorium...'
        checkout scm
    }
}
```

Celem tego etapu jest pobranie kodu źródłowego aplikacji z repozytorium Git.

### Co dokładnie się dzieje?

1. Jenkins rozpoczyna etap `Checkout`.
2. Odczytuje konfigurację repozytorium z joba Jenkins.
3. Pobiera odpowiednią gałąź lub commit.
4. Umieszcza kod w katalogu roboczym agenta.

Instrukcja:

groovy

```groovy
checkout scm
```

oznacza, że Jenkins korzysta z konfiguracji SCM przypisanej do bieżącego joba, np. repozytorium GitHub lub GitLab.

Dobra praktyka:

- Korzystaj z webhooków GitHub/GitLab, aby uruchamiać pipeline po zmianach w repozytorium.
- Buduj konkretny commit, aby móc odtworzyć proces.
- Nie przechowuj haseł do repozytorium bezpośrednio w kodzie.
- W przypadku wielu repozytoriów używaj jawnej konfiguracji `git` lub `checkout`.

# 3. Etap Install Dependencies – instalacja zależności

groovy

```groovy
stage('Install Dependencies') {
    steps {
        echo 'Instalowanie zależności...'
        sh 'npm install'
    }
}
```

Na tym etapie instalowane są biblioteki wymagane przez aplikację Node.js.

### Co robi `npm install`?

Polecenie:

bash

```bash
npm install
```

- Odczytuje plik `package.json`.
- Pobiera wymagane pakiety z rejestru npm.
- Instaluje zależności w katalogu `node_modules`.
- Aktualizuje lub tworzy plik `package-lock.json`, jeśli jest to potrzebne.

Przykładowy `package.json`:

json

```json
{
  "name": "node-app",
  "version": "1.0.0",
  "scripts": {
    "test": "jest",
    "build": "webpack"
  },
  "dependencies": {
    "express": "^4.21.0"
  },
  "devDependencies": {
    "jest": "^29.7.0",
    "webpack": "^5.0.0"
  }
}
```

### Dobra praktyka: npm ci zamiast npm install

W pipeline CI/CD zazwyczaj lepiej zastosować:

bash

```bash
npm ci
```

Dlaczego?

- Instaluje dokładnie wersje zapisane w `package-lock.json`.
- Zapewnia bardziej powtarzalne środowisko.
- Nie modyfikuje pliku `package-lock.json`.
- Jest zoptymalizowane pod kątem automatycznych instalacji.

Dlatego w produkcyjnym Jenkinsfile warto zastąpić:

groovy

```groovy
sh 'npm install'
```

przez:

groovy

```groovy
sh 'npm ci'
```

# 4. Etap Run Tests – uruchamianie testów

groovy

```groovy
stage('Run Tests') {
    steps {
        echo 'Uruchamianie testów...'
        sh 'npm test'
    }
}
```

Ten etap odpowiada za automatyczne sprawdzenie poprawności działania aplikacji.

### Co dokładnie się dzieje?

Jenkins wykonuje:

bash

```bash
npm test
```

NPM odczytuje sekcję `scripts` z pliku `package.json` i uruchamia zdefiniowane tam polecenie.

Przykładowo:

json

```json
{
  "scripts": {
    "test": "jest"
  }
}
```

W takim przypadku zostanie uruchomiony framework Jest.

Przykładowy wynik:

Testy jednostkowe

SUCCESS

text

```text
PASS test/app.test.js
  ✓ should return HTTP 200
  ✓ should return application data
  ✓ should handle invalid requests

Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
```

### Co jeśli testy zakończą się błędem?

Jeśli polecenie `npm test` zwróci kod wyjścia różny od zera, Jenkins oznaczy etap jako nieudany.

W standardowej konfiguracji deklaratywnego pipeline kolejne etapy nie zostaną wykonane.

To bardzo ważne: nie publikujemy obrazu Docker aplikacji, która nie przeszła testów.

### Dobra praktyka

Warto rozszerzyć testowanie o:

- testy jednostkowe (Unit Tests),
- testy integracyjne (Integration Tests),
- testy API,
- analizę jakości kodu,
- skanowanie podatności zależności.

Można również publikować raporty JUnit, aby wyniki testów były widoczne bezpośrednio w Jenkinsie.

# 5. Etap Build Application – budowanie aplikacji

groovy

```groovy
stage('Build Application') {
    steps {
        echo 'Budowanie aplikacji...'
        sh 'npm run build'
    }
}
```

Na tym etapie Jenkins wykonuje proces budowania aplikacji.

### Co robi `npm run build`?

Polecenie uruchamia skrypt `build` zdefiniowany w `package.json`.

Przykład:

json

```json
{
  "scripts": {
    "build": "webpack --mode production"
  }
}
```

W tym przypadku Webpack:

- analizuje kod źródłowy,
- przetwarza moduły JavaScript,
- optymalizuje kod,
- generuje pliki wynikowe.

Przykładowa struktura po zbudowaniu:

text

```text
node-app/
├── src/
├── test/
├── dist/
│   ├── main.js
│   └── main.js.map
├── package.json
└── Jenkinsfile
```

Katalog `dist` zawiera gotową wersję aplikacji.

Ważne: Nie każda aplikacja Node.js wymaga osobnego etapu build. W przypadku prostego serwera Express może wystarczyć uruchomienie aplikacji bez kompilacji.

### Dobra praktyka

- Buduj aplikację w trybie produkcyjnym.
- Przechowuj wyniki budowania jako artefakty Jenkinsa.
- Nie buduj aplikacji ponownie podczas wdrożenia, jeśli masz już sprawdzony artefakt.
- Rozdzielaj konfigurację środowiskową od kodu aplikacji.

# 6. Etap Build Docker Image – budowanie obrazu Docker

groovy

```groovy
stage('Build Docker Image') {
    steps {
        echo 'Budowanie obrazu Docker...'
        sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
    }
}
```

Tutaj Jenkins buduje obraz Docker zawierający aplikację.

### Co robi polecenie?

bash

```bash
docker build -t moj-rejestr/node-app:latest .
```

Poszczególne elementy:

- `docker build` – rozpoczyna budowanie obrazu.
- `-t` – nadaje obrazowi nazwę i tag.
- `moj-rejestr/node-app` – nazwa obrazu.
- `latest` – tag wersji.
- `.` – wskazuje bieżący katalog jako kontekst budowania.

Docker odczytuje plik `Dockerfile` i wykonuje zdefiniowane w nim instrukcje.

Przykładowy Dockerfile:

dockerfile

```dockerfile
FROM node:22-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci --omit=dev

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

Po zakończeniu budowania obraz będzie dostępny lokalnie na agencie Jenkins.

### Dobra praktyka

- Używaj lekkich obrazów bazowych, np. Alpine, jeśli są kompatybilne z aplikacją.
- Nie umieszczaj sekretów w obrazie Docker.
- Dodaj `.dockerignore`, aby nie kopiować zbędnych plików.

Przykładowy `.dockerignore`:

text

```text
node_modules
.git
.env
npm-debug.log
coverage
```

- Stosuj wersjonowanie obrazów zamiast polegania wyłącznie na tagu `latest`.
- Rozważ wykorzystanie wieloetapowego budowania (Multi-stage Build).

# 7. Etap Push Docker Image – publikowanie obrazu

groovy

```groovy
stage('Push Docker Image') {
    steps {
        echo 'Publikowanie obrazu Docker...'

        script {
            docker.withRegistry(
                'https://index.docker.io/v1/',
                DOCKER_CREDENTIALS
            ) {
                docker.image(
                    "${DOCKER_IMAGE}:${DOCKER_TAG}"
                ).push()
            }
        }
    }
}
```

Ostatni etap publikuje wcześniej zbudowany obraz w rejestrze Docker, np. Docker Hub.

### Co dokładnie się dzieje?

1. Jenkins odczytuje dane logowania z Jenkins Credentials.
2. Łączy się z Docker Hub.
3. Uwierzytelnia użytkownika.
4. Wskazuje obraz Docker do opublikowania.
5. Wysyła obraz do rejestru.

Najważniejszy fragment:

groovy

```groovy
docker.withRegistry(
    'https://index.docker.io/v1/',
    DOCKER_CREDENTIALS
)
```

Odpowiada za uwierzytelnienie w rejestrze.

Natomiast:

groovy

```groovy
docker.image(
    "${DOCKER_IMAGE}:${DOCKER_TAG}"
).push()
```

publikuje obraz o wskazanej nazwie i tagu.

### Dlaczego używamy `script`?

Deklaratywna składnia Jenkinsa pozwala używać bloków `script`, w których można wykonywać instrukcje napisane w bardziej elastycznej składni Groovy.

Jest to potrzebne w tym przykładzie do wykorzystania metod Docker Pipeline.

### Dobra praktyka

Zamiast publikować wyłącznie obraz:

text

```text
moj-rejestr/node-app:latest
```

lepiej stosować tagi powiązane z konkretnym buildem, np.:

text

```text
moj-rejestr/node-app:125
moj-rejestr/node-app:latest
```

Dzięki temu można łatwo zidentyfikować wersję obrazu i wrócić do wcześniejszego wydania.

# 8. Sekcja post – obsługa zakończenia pipeline

groovy

```groovy
post {
    success {
        echo 'Pipeline zakończony sukcesem!'
    }

    failure {
        echo 'Pipeline zakończony błędem!'
    }

    always {
        echo 'Zakończono wykonywanie pipeline.'
    }
}
```

Sekcja `post` definiuje akcje wykonywane po zakończeniu pipeline.

| Blok | Kiedy jest wykonywany? |
| --- | --- |
| `success` | Gdy pipeline zakończy się sukcesem |
| `failure` | Gdy pipeline zakończy się błędem |
| `always` | Zawsze, niezależnie od wyniku |

Można tutaj również:

- wysyłać powiadomienia e-mail,
- wysyłać komunikaty na Slack,
- publikować raporty testów,
- usuwać pliki tymczasowe,
- archiwizować artefakty.

Przykładowo:

groovy

```groovy
post {
    always {
        junit 'reports/**/*.xml'
        cleanWs()
    }
}
```

Wymaga to odpowiednich pluginów Jenkinsa i generowania raportów JUnit przez aplikację.

# 9. Najlepsze praktyki przy tworzeniu Jenkins Pipeline

Poniżej najważniejsze zasady, które warto stosować w rzeczywistych projektach CI/CD.

## 1. Używaj powtarzalnych instalacji zależności

Zamiast:

bash

```bash
npm install
```

preferuj:

bash

```bash
npm ci
```

Dzięki temu kolejne buildy korzystają z wersji zależności zapisanych w `package-lock.json`.

## 2. Nie przechowuj haseł w Jenkinsfile

Niepoprawne rozwiązanie:

groovy

```groovy
environment {
    DOCKER_PASSWORD = 'mojehaslo123'
}
```

Poprawne rozwiązanie:

groovy

```groovy
environment {
    DOCKER_CREDENTIALS = 'docker-hub-credentials'
}
```

Sekrety przechowuj w Jenkins Credentials.

## 3. Stosuj wersjonowanie obrazów Docker

Unikaj polegania wyłącznie na tagu `latest`.

Lepsze rozwiązanie:

groovy

```groovy
environment {
    DOCKER_IMAGE = 'moj-rejestr/node-app'
    DOCKER_TAG = "${BUILD_NUMBER}"
}
```

Każdy build otrzyma wtedy unikalny numer wersji obrazu.

## 4. Wykorzystuj cache

Budowanie aplikacji może być czasochłonne, szczególnie przy dużej liczbie zależności.

Warto wykorzystać:

- cache npm,
- cache warstw Docker,
- współdzielone cache na agentach Jenkins.

## 5. Oddzielaj etapy pipeline

Każdy etap powinien odpowiadać za konkretną czynność.

Przykładowo:

- Checkout – pobieranie kodu.
- Install – instalacja zależności.
- Test – weryfikacja poprawności.
- Build – budowanie aplikacji.
- Docker Build – tworzenie obrazu.
- Docker Push – publikowanie obrazu.
- Deploy – wdrażanie aplikacji.

Dzięki temu łatwiej diagnozować błędy.

## 6. Korzystaj z agentów Jenkins

W większych środowiskach warto oddzielać środowiska wykonywania zadań.

Przykładowo:

groovy

```groovy
pipeline {
    agent none

    stages {
        stage('Build') {
            agent {
                label 'nodejs'
            }
            steps {
                sh 'npm ci'
                sh 'npm run build'
            }
        }

        stage('Docker') {
            agent {
                label 'docker'
            }
            steps {
                sh 'docker build -t node-app:latest .'
            }
        }
    }
}
```

Pozwala to wykonywać zadania na różnych agentach, zależnie od wymaganych narzędzi.

Uwaga: jeżeli agenci są różni, trzeba dodatkowo zadbać o przekazywanie artefaktów pomiędzy nimi.

## 7. Dodaj skanowanie bezpieczeństwa

W profesjonalnym pipeline warto uwzględnić:

- `npm audit` – analizę podatności zależności.
- Skanowanie obrazu Docker, np. Trivy.
- Analizę jakości kodu, np. SonarQube.
- Kontrolę sekretów w repozytorium.

## 8. Nie wdrażaj aplikacji bez weryfikacji

Publikowanie obrazu powinno następować dopiero po pomyślnym zakończeniu testów i budowania.

W środowisku produkcyjnym warto dodatkowo zastosować ręczną akceptację wdrożenia.

# 10. Jak wygląda cały proces CI/CD?

Poniższy schemat przedstawia przepływ wykonywania naszego pipeline.

1. Checkout

Pobranie kodu z Git

2. Install Dependencies

npm ci

3. Run Tests

npm test

4. Build Application

npm run build

5. Build Docker Image

docker build

6. Push Docker Image

Publikowanie do Docker Hub

Pipeline SUCCESS

Jeżeli którykolwiek z etapów zakończy się błędem, standardowo Jenkins przerwie wykonywanie kolejnych etapów i oznaczy pipeline jako `FAILURE`.

# 11. Moje rekomendacje – co poprawiłbym w pierwotnym Jenkinsfile?

W projekcie produkcyjnym wprowadziłbym przede wszystkim następujące zmiany:

| Obszar | Obecne rozwiązanie | Zalecane rozwiązanie |
| --- | --- | --- |
| Instalacja npm | `npm install` | `npm ci` |
| Wersjonowanie Docker | `latest` | `${BUILD_NUMBER}` |
| Bezpieczeństwo | Podstawowe Credentials | Credentials + skanowanie |
| Testy | `npm test` | Testy + raporty JUnit |
| Docker | Jeden etap build | Build + skanowanie obrazu |
| Sprzątanie | Brak | `cleanWs()` |

Najważniejsza zasada: dobry Jenkins Pipeline powinien być powtarzalny, bezpieczny, łatwy do diagnozowania i niezależny od konkretnego agenta Jenkins, o ile architektura projektu na to pozwala.

Warto też pamiętać, że Jenkinsfile powinien być przechowywany razem z kodem aplikacji w repozytorium Git. Dzięki temu historia zmian pipeline jest wersjonowana tak samo jak historia zmian aplikacji.