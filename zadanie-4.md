Duże zużycie pamięci RAM przez kontener Docker może wynikać z kilku przyczyn: wycieku pamięci w aplikacji, nieprawidłowej konfiguracji kontenera, zbyt dużej liczby procesów, cache'u lub braku limitów pamięci.

Najlepiej podejść do problemu etapami: najpierw zidentyfikować źródło zużycia RAM, a następnie ograniczyć lub zoptymalizować jego wykorzystanie.

## 1. Sprawdź, ile pamięci zużywa kontener

Podstawowa komenda:

bash

```bash
docker stats
```

Wyświetla na żywo:

- `MEM USAGE` – aktualne zużycie pamięci.
- `MEM LIMIT` – limit pamięci kontenera.
- `MEM %` – procent wykorzystanej pamięci.
- `CPU %` – wykorzystanie procesora.

Dla konkretnego kontenera:

bash

```bash
docker stats nazwa_kontenera
```

Możesz też sprawdzić konfigurację:

bash

```bash
docker inspect nazwa_kontenera
```

## 2. Sprawdź, który proces zużywa pamięć

Wejdź do kontenera:

bash

```bash
docker exec -it nazwa_kontenera sh
```

Jeśli dostępny jest `top`:

bash

```bash
top
```

Lub:

bash

```bash
ps aux --sort=-%mem | head
```

Pozwoli to ustalić, czy problem powoduje:

- proces aplikacji,
- serwer WWW,
- baza danych,
- worker lub proces działający w tle.

## 3. Ustaw limit pamięci RAM

Jeśli kontener zużywa zbyt dużo pamięci, możesz ograniczyć jego maksymalne wykorzystanie.

Przykład:

bash

```bash
docker run -d \
  --name moja-aplikacja \
  --memory="512m" \
  --memory-swap="512m" \
  moja-aplikacja:latest
```

W tym przypadku kontener otrzymuje maksymalnie 512 MB pamięci.

Jeżeli używasz Docker Compose:

yaml

```yaml
services:
  app:
    image: moja-aplikacja:latest
    mem_limit: 512m
```

Uwaga: Limit pamięci nie rozwiązuje wycieku pamięci. Jeśli aplikacja potrzebuje więcej RAM, może zostać zakończona przez mechanizm OOM Kill.

## 4. Sprawdź, czy nie występuje memory leak

Typowy objaw wycieku pamięci:

Przykładowy wzrost zużycia RAM

Wykres

Przykładowy, hipotetyczny przebieg zużycia pamięci.

Rozwiń wykres

|  | RAM |
| --- | --- |
| 10:00 | 180 MB |
| 10:15 | 250 MB |
| 10:30 | 370 MB |
| 10:45 | 490 MB |
| 11:00 | 650 MB |
| 11:15 | 790 MB |

Jeśli zużycie stale rośnie i nie spada po zakończeniu operacji, może to wskazywać na memory leak.

Warto sprawdzić:

- Czy aplikacja zwalnia nieużywane obiekty?
- Czy połączenia z bazą danych są zamykane?
- Czy cache ma ograniczony rozmiar?
- Czy kolejki zadań nie gromadzą danych?
- Czy logi nie są niepotrzebnie przechowywane w pamięci?

## 5. Sprawdź logi kontenera

bash

```bash
docker logs --tail 200 nazwa_kontenera
```

Sprawdź również, czy kontener nie był restartowany z powodu braku pamięci:

bash

```bash
docker inspect nazwa_kontenera \
  --format='OOMKilled={{.State.OOMKilled}}'
```

## 6. Zoptymalizuj konfigurację aplikacji

W zależności od technologii:

| Technologia | Co sprawdzić |
| --- | --- |
| Node.js | `--max-old-space-size`, cache, heap |
| Java | `-Xms`, `-Xmx`, GC |
| Python | wycieki referencji, multiprocessing |
| PHP | `memory_limit`, PHP-FPM workers |
| MySQL | buffer pool, cache, liczba połączeń |
| PostgreSQL | shared\_buffers, work\_mem, liczba połączeń |
| Redis | maxmemory, polityka eviction |

## 7. Sprawdź wykorzystanie pamięci przez Dockera

Przydatne polecenia:

bash

```bash
docker system df
```

Pokazuje wykorzystanie miejsca przez obrazy, kontenery i wolumeny.

bash

```bash
docker ps
```

Pokazuje uruchomione kontenery.

bash

```bash
docker inspect nazwa_kontenera
```

Pozwala sprawdzić szczegóły konfiguracji kontenera.

Pamiętaj, że usuwanie nieużywanych obrazów i cache Dockera zwalnia miejsce na dysku, a niekoniecznie pamięć RAM.

## Żeby znaleźć konkretną przyczynę

Chciałbym dopasować diagnostykę do Twojego środowiska.

1. Jaka aplikacja działa w kontenerze?

Node.js Node.js

Java / Spring Boot

Python

PHP

MySQL / PostgreSQL

Redis

Inna

2. Jak uruchamiasz kontener?

Docker Compose Docker Compose

docker run

Kubernetes

Inne

3. Jaki jest objaw?

RAM stale rośnie RAM stale rośnie

RAM jest wysoki od uruchomienia

Kontener kończy działanie (OOMKilled)

RAM nie spada po zakończeniu operacji

Nie wiem

4. Ile pamięci zużywa kontener?

Do 512 MB

512 MB – 1 GB

1–2 GB 1–2 GB

2–4 GB

Ponad 4 GB

 Prześlij odpowiedzi

Możesz też wkleić wynik `docker stats` oraz fragment `docker-compose.yml` (bez haseł i sekretów). Na tej podstawie pomogę ustalić, czy problem leży w Dockerze, konfiguracji czy samej aplikacji.


---------------------------------------------------------------------------------------------------------------------------------------------------------

Jako DevOps Engineer z 10-letnim doświadczeniem podszedłbym do problemu dużego zużycia pamięci przez kontener Docker metodycznie: najpierw identyfikacja źródła problemu, następnie analiza zachowania aplikacji, a na końcu optymalizacja i zabezpieczenie kontenera przed ponownym wystąpieniem problemu.

Nie zaczynałbym od zwiększania limitu pamięci. To często tylko maskuje rzeczywistą przyczynę.

Poniżej przedstawiam podejście, które zastosowałbym w środowisku produkcyjnym.

# 1. Zidentyfikuj kontener zużywający najwięcej pamięci

Zacznij od sprawdzenia wykorzystania zasobów przez wszystkie kontenery:

bash

```bash
docker stats
```

Przykładowy wynik:

text

```text
CONTAINER ID   NAME       CPU %   MEM USAGE / LIMIT
a12bc34        api        15%     1.8GiB / 2GiB
b23cd45        nginx      0.5%    25MiB / 2GiB
c34de56        worker     45%     950MiB / 2GiB
```

W tym przypadku kontener `api` zużywa 1.8 GiB z dostępnych 2 GiB.

Możesz również sprawdzić statystyki konkretnego kontenera:

bash

```bash
docker stats api
```

Albo jednorazowo:

bash

```bash
docker stats --no-stream
```

Na co zwrócić uwagę?

- MEM USAGE – aktualne zużycie pamięci.
- MEM LIMIT – limit pamięci kontenera.
- MEM % – procent wykorzystania dostępnej pamięci.
- Zachowanie w czasie – czy pamięć stale rośnie, czy utrzymuje się na wysokim poziomie?

Szczególnie niepokojący jest stale rosnący wykres pamięci bez późniejszego spadku.

# 2. Sprawdź, czy kontener nie jest zabijany przez OOM Killer

Docker może zakończyć proces, jeśli przekroczy on limit pamięci.

Sprawdź status kontenera:

bash

```bash
docker inspect api --format '{{.State.OOMKilled}}'
```

Jeśli otrzymasz:

text

```text
true
```

oznacza to, że kontener został zabity z powodu przekroczenia limitu pamięci.

Sprawdź również logi:

bash

```bash
docker logs --tail 200 api
```

Oraz zdarzenia Dockera:

bash

```bash
docker events --since 1h
```

Na poziomie hosta Linux możesz sprawdzić:

bash

```bash
dmesg -T | grep -i -E 'oom|killed process'
```

Pozwoli to ustalić, czy problem dotyczy pojedynczego kontenera, czy całego hosta.

# 3. Zdiagnozuj zużycie pamięci wewnątrz kontenera

To jeden z najważniejszych etapów.

Wysokie zużycie pamięci przez kontener nie zawsze oznacza memory leak w aplikacji.

Możliwe przyczyny:

- Memory leak w kodzie aplikacji.
- Zbyt duży cache.
- Nieograniczona kolejka zadań.
- Zbyt duża liczba workerów lub procesów.
- Nieprawidłowa konfiguracja JVM.
- Nieograniczony connection pool.
- Buforowanie dużych plików.
- Cache systemu plików (page cache).

Sprawdź procesy:

bash

```bash
docker exec api ps aux --sort=-%mem | head -15
```

Jeśli kontener nie ma narzędzi diagnostycznych, możesz wykorzystać tymczasowy kontener diagnostyczny współdzielący jego przestrzeń procesów.

bash

```bash
docker top api
```

Dla aplikacji Linux warto również sprawdzić:

bash

```bash
docker exec api cat /proc/meminfo
```

Jeśli korzystasz z Docker na Linuxie, sprawdź także statystyki cgroup.

Dla cgroup v2:

bash

```bash
docker exec api cat /sys/fs/cgroup/memory.current
docker exec api cat /sys/fs/cgroup/memory.max
docker exec api cat /sys/fs/cgroup/memory.stat
```

`memory.stat` pozwala rozróżnić m.in. pamięć anonimową od pamięci plikowej.

To istotne, ponieważ `docker stats` może uwzględniać pamięć cache, która niekoniecznie oznacza problem z aplikacją.

# 4. Sprawdź, czy występuje Memory Leak

Jeśli pamięć systematycznie rośnie, warto przeprowadzić analizę aplikacji.

Metoda zależy od technologii.

Java / Spring Boot

Sprawdź wykorzystanie Heap:

bash

```bash
jcmd <PID> GC.heap_info
```

Wygeneruj heap dump:

bash

```bash
jcmd <PID> GC.heap_dump /tmp/heap.hprof
```

Przeanalizuj go w Eclipse MAT lub VisualVM.

Node.js

Uruchom aplikację z:

bash

```bash
node --inspect app.js
```

Wykorzystaj Chrome DevTools do analizy heap snapshots.

Możesz też monitorować pamięć:

javascript

```javascript
console.log(process.memoryUsage());
```

Python

Wykorzystaj `tracemalloc`:

python

```python
import tracemalloc

tracemalloc.start()

# kod aplikacji

snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics("lineno")[:10]:
    print(stat)
```

.NET

Wykorzystaj:

bash

```bash
dotnet-counters monitor
```

Do szczegółowej analizy możesz użyć `dotnet-dump`.

Ważne: Heap dump może zawierać dane wrażliwe i zajmować dużo miejsca. Nie wykonuj go bez kontroli dostępnej przestrzeni dyskowej.

# 5. Ustaw limity pamięci w Dockerze

Jeśli kontener nie ma limitów, może zużyć znaczną część pamięci hosta.

Przykład uruchomienia kontenera z ograniczeniem do 1 GB:

bash

```bash
docker run -d \
  --name api \
  --memory=1g \
  --memory-reservation=768m \
  --memory-swap=1g \
  my-api:latest
```

Znaczenie parametrów:

| Parametr | Znaczenie |
| --- | --- |
| `--memory=1g` | Maksymalna pamięć kontenera |
| `--memory-reservation=768m` | Miękka rezerwacja pamięci |
| `--memory-swap=1g` | Łączny limit RAM i swap |

Uwaga: `--memory-swap=1g` przy `--memory=1g` oznacza brak dodatkowej przestrzeni swap dla kontenera.

W przypadku Docker Compose:

yaml

```yaml
services:
  api:
    image: my-api:latest
    mem_limit: 1g
    mem_reservation: 768m
```

Nie ustawiaj limitu bez wcześniejszego sprawdzenia rzeczywistego zapotrzebowania aplikacji. Zbyt niski limit może doprowadzić do OOM Kill.

# 6. Zoptymalizuj aplikację

Samo ograniczenie pamięci nie rozwiązuje problemu, jeśli aplikacja ma nieprawidłową gospodarkę pamięcią.

Przykładowe działania:

| Problem | Rozwiązanie |
| --- | --- |
| Memory leak | Profilowanie i naprawa kodu |
| Zbyt duży cache | Wprowadzenie TTL i limitów cache |
| Zbyt dużo workerów | Ograniczenie liczby procesów |
| Duże kolejki | Backpressure i ograniczenie długości kolejki |
| Duże zapytania SQL | Paginacja i optymalizacja zapytań |
| Zbyt dużo połączeń | Ograniczenie connection pool |
| Duże pliki | Streaming zamiast ładowania całości do RAM |

Przykładowo w aplikacji Node.js możesz ustawić limit pamięci sterty:

bash

```bash
node --max-old-space-size=768 app.js
```

W przypadku Javy:

bash

```bash
java -Xms256m -Xmx768m -jar app.jar
```

Pamiętaj, że heap JVM to nie cała pamięć procesu. Dochodzą m.in. Metaspace, stosy wątków i pamięć natywna.

# 7. Wprowadź monitoring i alerty

W środowisku produkcyjnym nie polegałbym wyłącznie na ręcznym wykonywaniu `docker stats`.

Polecam następujący stack:

## Przykładowa architektura monitoringu

Docker Containers

API · Worker · Database · Cache

cAdvisor

Zbieranie metryk kontenerów

Prometheus

Przechowywanie i agregacja metryk

Grafana

Dashboardy

Alertmanager

Powiadomienia

Przykładowa reguła alertu Prometheus:

yaml

```yaml
groups:
  - name: docker-memory
    rules:
      - alert: ContainerHighMemoryUsage
        expr: |
          (
            container_memory_working_set_bytes
            /
            container_spec_memory_limit_bytes
          ) > 0.85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage in container"
          description: "Container memory usage is above 85%."
```

W praktyce należy dodatkowo wykluczyć kontenery bez określonego limitu pamięci i zweryfikować dostępność metryk dla używanej wersji cAdvisor.

# 8. Jak wyglądałaby moja procedura w produkcji?

Zastosowałbym następującą kolejność:

1. Identyfikacja problemu
   `docker stats`, identyfikacja kontenera i analiza trendu pamięci.
2. Analiza OOM
   `docker inspect`, `docker events`, logi aplikacji i logi kernela.
3. Analiza procesów
   `docker top`, `ps aux`, statystyki cgroup.
4. Profilowanie aplikacji
   Heap dump, memory profiling, analiza cache i liczby workerów.
5. Optymalizacja
   Naprawa memory leak, ograniczenie cache, workerów i kolejek.
6. Zabezpieczenie
   Limity pamięci, healthcheck, monitoring i alerty.
7. Weryfikacja
   Test obciążeniowy i sprawdzenie, czy pamięć stabilizuje się pod obciążeniem.

# 9. Podejdźmy do konkretnego przypadku

Żeby przejść z teorii do rzeczywistej diagnostyki, chciałbym poznać technologię działającą w problematycznym kontenerze.

1. Jaka technologia działa w kontenerze?

Java / Spring Boot Java / Spring Boot

Node.js

Python

PHP

Go

PostgreSQL / MySQL

Inna

2. Jak zarządzasz kontenerami?

Docker Compose Docker Compose

Docker Swarm

Kubernetes

Pojedynczy Docker

3. Jaki jest objaw problemu?

Pamięć stale rośnie z czasem Pamięć stale rośnie z czasem

Kontener nagle zużywa dużo RAM

Kontener jest restartowany (OOMKilled)

Wysokie zużycie pamięci od samego startu

Problem występuje tylko przy dużym ruchu

4. Jaki jest limit pamięci kontenera?

512 MB

1 GB

2 GB 2 GB

4 GB

8 GB lub więcej

Brak limitu / Nie wiem

 Przeanalizuj mój przypadek

Na podstawie odpowiedzi przygotuję konkretny plan diagnostyczny, zestaw komend i rekomendowane zmiany konfiguracyjne, które można zastosować w środowisku produkcyjnym.