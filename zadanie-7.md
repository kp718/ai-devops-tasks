Przejdźmy przez skrypt krok po kroku, zakładając, że dopiero zaczynasz naukę Bash i Linuksa.

## 1. Cały skrypt

Na początek przypomnijmy sobie jego treść:

bash

```bash
#!/bin/bash

SERVICE="docker"

echo "Sprawdzam status usługi Docker..."

if systemctl is-active --quiet "$SERVICE"; then
    echo "Docker działa poprawnie."
else
    echo "Docker nie działa. Próbuję uruchomić usługę..."

    if sudo systemctl start "$SERVICE"; then
        echo "Docker został pomyślnie uruchomiony."
    else
        echo "BŁĄD: Nie udało się uruchomić Dockera."
        exit 1
    fi
fi
```

## 2. Wyjaśnienie linia po linii

### Linia 1

bash

```bash
#!/bin/bash
```

To tak zwany shebang.

Informuje system operacyjny, że skrypt powinien zostać wykonany przy użyciu interpretera Bash.

Można to rozumieć następująco:

„Hej, systemie\! Ten plik zawiera polecenia napisane w języku Bash. Użyj Basha, żeby je wykonać”.

### Linia 2

bash

```bash
SERVICE="docker"
```

Tutaj tworzymy zmienną o nazwie `SERVICE`.

Zmienna to miejsce, w którym przechowujemy jakąś wartość.

W naszym przypadku:

- `SERVICE` – nazwa zmiennej.
- `docker` – wartość zmiennej.

Dzięki temu nie musimy za każdym razem wpisywać nazwy usługi ręcznie.

Gdybyśmy chcieli sprawdzać inną usługę, np. SSH, moglibyśmy zmienić tę linię na:

bash

```bash
SERVICE="ssh"
```

### Linia 3

bash

```bash
echo "Sprawdzam status usługi Docker..."
```

Polecenie `echo` wyświetla tekst w terminalu.

W tym przypadku użytkownik zobaczy:

text

```text
Sprawdzam status usługi Docker...
```

Jest to tylko komunikat informacyjny. Nie sprawdza jeszcze stanu Dockera.

### Linia 4

bash

```bash
if systemctl is-active --quiet "$SERVICE"; then
```

To jedna z najważniejszych linii skryptu.

Rozłóżmy ją na części:

- `if` – oznacza warunek, czyli „jeżeli”.
- `systemctl` – narzędzie służące do zarządzania usługami systemowymi w Linuksie.
- `is-active` – sprawdza, czy dana usługa jest aktywna.
- `--quiet` – wyłącza wyświetlanie standardowego komunikatu o wyniku sprawdzania.
- `"$SERVICE"` – oznacza wartość naszej zmiennej, czyli `docker`.
- `then` – oznacza „wtedy wykonaj poniższe polecenia”.

W praktyce wykonywane jest polecenie:

bash

```bash
systemctl is-active --quiet docker
```

Co ono robi?

Sprawdza, czy usługa Docker działa.

Ważna rzecz: polecenie `systemctl` zwraca tzw. kod wyjścia:

- `0` – operacja zakończyła się sukcesem, czyli Docker działa.
- wartość różna od `0` – warunek nie został spełniony, czyli Docker nie jest aktywny.

Bash wykorzystuje te informacje do podjęcia decyzji.

### Linia 5

bash

```bash
echo "Docker działa poprawnie."
```

Ta linia wykona się tylko wtedy, gdy Docker jest aktywny.

Czyli jeśli warunek z poprzedniej linii jest prawdziwy, zobaczymy:

text

```text
Docker działa poprawnie.
```

### Linia 6

bash

```bash
else
```

Słowo `else` oznacza „w przeciwnym przypadku”.

Czyli:

- Jeśli Docker działa – wykonaj polecenia po `then`.
- Jeśli Docker nie działa – wykonaj polecenia po `else`.

To odpowiednik instrukcji warunkowej znanej z innych języków programowania, np. Pythona czy JavaScriptu.

### Linia 7

bash

```bash
echo "Docker nie działa. Próbuję uruchomić usługę..."
```

Wyświetlamy komunikat informujący użytkownika, że Docker nie działa i skrypt podejmie próbę jego uruchomienia.

### Linia 8

bash

```bash
if sudo systemctl start "$SERVICE"; then
```

Tutaj pojawia się drugi warunek `if`.

Rozłóżmy go na części:

- `sudo` – uruchamia polecenie z uprawnieniami administratora (root).
- `systemctl` – narzędzie do zarządzania usługami.
- `start` – próbuje uruchomić wskazaną usługę.
- `"$SERVICE"` – wskazuje usługę Docker.
- `then` – oznacza, że jeśli uruchomienie się powiedzie, wykonujemy kolejne polecenia.

W praktyce wykonujemy:

bash

```bash
sudo systemctl start docker
```

Dlaczego używamy `sudo`?

Ponieważ uruchamianie usług systemowych zazwyczaj wymaga uprawnień administratora.

System może poprosić o podanie hasła użytkownika.

### Linia 9

bash

```bash
echo "Docker został pomyślnie uruchomiony."
```

Jeśli polecenie uruchomienia zakończy się sukcesem, zobaczymy:

text

```text
Docker został pomyślnie uruchomiony.
```

Uwaga: ten komunikat oznacza, że polecenie `systemctl start` zakończyło się sukcesem. Nie wykonujemy tutaj dodatkowej kontroli, czy Docker rzeczywiście zaczął już poprawnie obsługiwać kontenery.

### Linia 10

bash

```bash
else
```

To drugi blok `else`.

Oznacza, że jeśli próba uruchomienia Dockera zakończyła się niepowodzeniem, wykonujemy instrukcje znajdujące się poniżej.

### Linia 11

bash

```bash
echo "BŁĄD: Nie udało się uruchomić Dockera."
```

Wyświetlamy komunikat o błędzie:

text

```text
BŁĄD: Nie udało się uruchomić Dockera.
```

### Linia 12

bash

```bash
exit 1
```

To bardzo ważne polecenie.

`exit` kończy działanie skryptu.

Liczba `1` oznacza, że skrypt zakończył się błędem.

Warto zapamiętać:

- `exit 0` – skrypt zakończył się poprawnie.
- `exit 1` – skrypt zakończył się błędem.

Dzięki temu inne skrypty lub narzędzia mogą rozpoznać, czy wykonanie zakończyło się sukcesem.

### Linie 13–15

bash

```bash
fi
fi
```

Słowo `fi` kończy instrukcję `if`.

W Bashu każda instrukcja `if` musi zostać zamknięta przez `fi`.

Ponieważ w naszym skrypcie mamy dwa warunki `if`, potrzebujemy dwóch instrukcji `fi`.

## 3. Jak działa cały skrypt? Schemat logiczny

Poniżej przedstawiam uproszczony schemat działania:

START

Uruchomienie skryptu

Sprawdź status Dockera

systemctl is-active docker

TAKDocker działa

Wyświetl komunikat o poprawnym działaniu.

NIEDocker nie działa

Spróbuj uruchomić usługę.

Czy uruchomienie się powiodło?

TAKWyświetl sukces

Zakończ działanie.

NIEWyświetl błąd

exit 1

## 4. Przykładowe działanie w terminalu

Przypadek A – Docker już działa:

text

```text
Sprawdzam status usługi Docker...
Docker działa poprawnie.
```

Przypadek B – Docker nie działa, ale udało się go uruchomić:

text

```text
Sprawdzam status usługi Docker...
Docker nie działa. Próbuję uruchomić usługę...
Docker został pomyślnie uruchomiony.
```

Przypadek C – nie udało się uruchomić Dockera:

text

```text
Sprawdzam status usługi Docker...
Docker nie działa. Próbuję uruchomić usługę...
BŁĄD: Nie udało się uruchomić Dockera.
```

## 5. Co warto zapamiętać z tego przykładu?

Poznałeś kilka podstawowych elementów programowania w Bashu:

| Element | Znaczenie |
| --- | --- |
| `#!/bin/bash` | Wskazuje interpreter Bash |
| `SERVICE="docker"` | Tworzy zmienną |
| `echo` | Wyświetla tekst |
| `if` | Sprawdza warunek |
| `then` | Wykonuje kod, gdy warunek jest spełniony |
| `else` | Wykonuje kod w przeciwnym przypadku |
| `fi` | Kończy instrukcję warunkową |
| `sudo` | Uruchamia polecenie z uprawnieniami administratora |
| `exit 1` | Kończy skrypt z kodem błędu |

## 6. Małe ćwiczenie dla Ciebie

Spróbuj samodzielnie odpowiedzieć na trzy pytania:

1. Co oznacza polecenie echo?

Uruchamia usługę

Wyświetla tekst w terminalu

Kończy działanie skryptu

2. Co zrobi skrypt, jeśli Docker już działa?

Spróbuje go uruchomić ponownie

Wyświetli komunikat o poprawnym działaniu

Zakończy się błędem

3. Do czego służy exit 1?

Do uruchomienia Dockera

Do utworzenia zmiennej

Do zakończenia skryptu z kodem błędu

 Sprawdź odpowiedzi

Moja rada: najlepiej ucz się Basha właśnie w ten sposób – poznawaj jedną instrukcję, sprawdzaj, co robi, a następnie próbuj samodzielnie ją modyfikować. Dzięki temu szybko zrozumiesz, jak budować własne skrypty administracyjne.