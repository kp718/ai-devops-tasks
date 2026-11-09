Opis poszczególnych etapów
Etap

Opis

Przykładowe narzędzia

Checkout

Pobranie kodu z repozytorium

Git

Build

Kompilacja i budowanie aplikacji

Maven, Gradle, npm

Testy

Testy jednostkowe

JUnit, Jest

Analiza statyczna

Wykrywanie błędów i problemów jakościowych

SonarQube

Bezpieczeństwo

Analiza podatności i zależności

Snyk, OWASP Dependency-Check

Docker Build

Budowanie obrazu kontenera

Docker

Testy integracyjne

Weryfikacja współpracy komponentów

Postman, Testcontainers

Staging

Wdrożenie na środowisko testowe

Kubernetes, Docker

Production

Wdrożenie wersji produkcyjnej

Kubernetes, Helm

Przykładowy przebieg pipeline
Jenkins wykrywa zmianę w repozytorium Git.

Pobiera kod i buduje aplikację.

Uruchamia testy jednostkowe.

Analizuje jakość kodu i bezpieczeństwo.

Buduje obraz Docker.

Wykonuje testy integracyjne.

Wdraża aplikację na staging.

Przeprowadza testy akceptacyjne.

Po uzyskaniu akceptacji wdraża aplikację na produkcję.

Wykonuje Health Check i informuje zespół o wyniku.

Dobra praktyka: wdrożenie na produkcję warto zabezpieczyć ręczną akceptacją (Manual Approval), a ten sam obraz Docker promować ze staging na produkcję, zamiast budować go ponownie. Dzięki temu masz pewność, że na produkcję trafia dokładnie ten sam artefakt, który został wcześniej przetestowany.


