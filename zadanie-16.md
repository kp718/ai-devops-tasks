Najważniejsze różnice między Bash a PowerShell
Bash

PowerShell

Opis

#!/bin/bash

Brak odpowiednika

PowerShell uruchamia plik .ps1

DB_NAME="..."

$DB_NAME = "..."

Deklaracja zmiennej

$(date +...)

Get-Date -Format

Generowanie daty

[ ! -d "$DIR" ]

-not (Test-Path ...)

Sprawdzanie katalogu

mkdir -p

New-Item -Force

Tworzenie katalogu

echo

Write-Host

Wyświetlanie komunikatów

$?

$LASTEXITCODE

Kod zakończenia programu zewnętrznego

gzip

gzip -c

Kompresowanie danych

Wymagania
Przed uruchomieniem skryptu upewnij się, że:

Masz zainstalowany MySQL Client (program mysqldump).

Masz dostępny program gzip w zmiennej środowiskowej PATH (np. z Git for Windows).

PowerShell ma uprawnienia do zapisu w C:\Backups\db.

Uruchomienie
Otwórz PowerShell i wykonaj:


powershell
.\backup.ps1
Uwaga: Warto pamiętać, że w PowerShell $LASTEXITCODE po potoku może nie odzwierciedlać poprawnie błędu mysqldump, ponieważ może zostać nadpisany przez gzip. W produkcyjnym skrypcie backupowym najlepiej dodatkowo sprawdzać kod wyjścia obu programów, aby nie uznać niekompletnej kopii za poprawną.