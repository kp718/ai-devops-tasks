Ten błąd oznacza, że port 3000 jest już zajęty przez inny proces lub kontener, a Docker próbuje uruchomić Twoją aplikację (`app`), która również chce korzystać z tego portu.

Najważniejszy fragment komunikatu to:

text

```text
listen tcp4 0.0.0.0:3000: bind: address already in use
```

Oznacza to, że Docker nie może przypisać portu 3000 do nowego kontenera, ponieważ jest on już używany.

## 1. Sprawdź, co zajmuje port 3000

W zależności od systemu operacyjnego użyj odpowiedniej komendy.

Linux:

bash

```bash
sudo lsof -i :3000
```

Alternatywnie:

bash

```bash
sudo ss -lptn 'sport = :3000'
```

macOS:

bash

```bash
lsof -i :3000
```

Windows (PowerShell):

powershell

```powershell
netstat -ano | findstr :3000
```

Zobaczysz identyfikator procesu (PID), który korzysta z portu.

## 2. Zatrzymaj proces zajmujący port

Jeśli korzystasz z Linuxa lub macOS:

bash

```bash
sudo kill -9 PID
```

Zamiast `PID` wpisz numer procesu znaleziony w poprzednim kroku.

Na Windows:

powershell

```powershell
taskkill /PID NUMER_PID /F
```

Uwaga: upewnij się, że zatrzymujesz właściwy proces. Może to być np. inna aplikacja Node.js, serwer developerski lub kontener Docker.

## 3. Sprawdź uruchomione kontenery Docker

Możliwe, że port 3000 jest zajęty przez inny kontener.

Sprawdź działające kontenery:

bash

```bash
docker ps
```

Jeżeli znajdziesz kontener korzystający z portu 3000, możesz go zatrzymać:

bash

```bash
docker stop NAZWA_LUB_ID_KONTENERA
```

Następnie spróbuj ponownie uruchomić aplikację:

bash

```bash
docker compose up -d
```

## 4. Alternatywnie zmień port aplikacji

Jeśli chcesz, aby obie aplikacje działały jednocześnie, możesz zmienić port zewnętrzny w pliku `docker-compose.yml`.

Przykładowo, jeśli masz:

yaml

```yaml
services:
  app:
    ports:
      - "3000:3000"
```

Zmień na:

yaml

```yaml
services:
  app:
    ports:
      - "3001:3000"
```

Oznacza to:

- `3001` – port dostępny na Twoim komputerze.
- `3000` – port wewnątrz kontenera.

Po zmianie uruchom:

bash

```bash
docker compose up -d
```

Aplikacja będzie dostępna pod adresem:

text

```text
http://localhost:3001
```

## Co polecam?

Najpierw wykonaj:

bash

```bash
docker ps
```

Jeśli nie znajdziesz tam kontenera zajmującego port 3000, sprawdź:

bash

```bash
sudo lsof -i :3000
```

Jeśli chcesz, pomogę Ci znaleźć dokładną przyczynę.

Napisz tylko:

- Czy korzystasz z Linuxa, Windowsa czy macOS?
- Czy uruchamiasz aplikację przez Docker Compose?
- Możesz też wkleić zawartość swojego `docker-compose.yml`.

Na tej podstawie wskażę Ci dokładnie, co zmienić, żeby aplikacja uruchomiła się poprawnie.