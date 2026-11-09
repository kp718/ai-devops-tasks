1. Znalezione błędy
1. Literówka stesp zamiast steps

W etapie Build użyto:


groovy
stesp {
Powinno być:


groovy
steps {
Jest to błąd składniowy w deklaratywnym pipeline Jenkins. Jenkins nie rozpozna niepoprawnego bloku.

2. Niepoprawna komenda npm build

W kodzie znajduje się:


groovy
sh 'npm build'
Prawidłowa komenda to:


groovy
sh 'npm run build'
Komenda npm run build uruchamia skrypt build zdefiniowany w pliku package.json.

3. Niepoprawna kolejność i sposób budowania obrazu Docker

W etapie Deploy znajduje się:


groovy
sh 'docker build -t myapp .'
sh 'docker push myapp:latest'
Pierwsza komenda jest poprawna, ale warto jawnie określić tag obrazu:


groovy
sh 'docker build -t myapp:latest .'
Druga komenda jest poprawna pod warunkiem, że obraz został wcześniej oznaczony tagiem latest.

4. Brak konfiguracji połączenia z rejestrem Docker

Komenda:


groovy
sh 'docker push myapp:latest'
wymaga zalogowania do rejestru Docker oraz odpowiedniego oznaczenia obrazu. Bez tego publikacja może zakończyć się błędem autoryzacji lub nieprawidłowej nazwy repozytorium.

5. Warunek when

W kodzie użyto:


groovy
when {
    branch 'master'
}
Składnia jest poprawna. Jednak współcześnie często stosuje się gałąź main zamiast master. Należy dostosować warunek do rzeczywistej nazwy gałęzi w repozytorium.

3. Wyjaśnienie wprowadzonych poprawek
Element

Przed poprawką

Po poprawce

Blok Build

stesp

steps

Budowanie aplikacji

npm build

npm run build

Tagowanie obrazu

myapp

myapp:latest

Logowanie Docker

Brak

docker login

Publikacja obrazu

myapp:latest

DOCKER_USER/myapp:latest

Warunek wdrożenia

master

main

4. Jak działa poprawiony pipeline?
Pipeline wykonuje trzy etapy w określonej kolejności:

Build – budowanie aplikacji

Instalacja zależności (npm install).

Budowanie aplikacji (npm run build).

Test – testowanie aplikacji

Uruchomienie testów (npm test).

Jeśli testy zakończą się błędem, pipeline zatrzyma się i nie przejdzie do wdrożenia.

Deploy – wdrażanie aplikacji

Etap wykonuje się tylko dla gałęzi main.

Budowany jest obraz Docker.

Jenkins loguje się do Docker Hub.

Obraz jest publikowany w rejestrze.

5. Dodatkowe zalecenia
Warto rozważyć jeszcze kilka usprawnień:

Zastosowanie npm ci zamiast npm install w pipeline CI/CD, jeśli projekt posiada plik package-lock.json. Zapewnia to bardziej powtarzalną instalację zależności.

Dodanie obsługi tagów wersji obrazów Docker zamiast używania wyłącznie latest.

Dodanie etapu czyszczenia po zakończeniu pipeline'u.

Wykorzystanie Jenkins Credentials do bezpiecznego przechowywania haseł i tokenów.

Podsumowanie: Najważniejsze błędy to literówka stesp oraz niepoprawna komenda npm build. Dodatkowo poprawiono proces budowania i publikowania obrazu Docker oraz zabezpieczono logowanie do rejestru za pomocą Jenkins Credentials. Dzięki temu pipeline jest bardziej poprawny, bezpieczny i gotowy do wykorzystania w procesie CI/CD.
