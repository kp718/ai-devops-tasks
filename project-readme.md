Simple Task API

REST API do zarządzania zadaniami, stworzone przy użyciu Node.js, Express.js oraz MongoDB.

Opis

Simple Task API to prosta aplikacja backendowa umożliwiająca zarządzanie zadaniami (CRUD).

Główne funkcjonalności:

Tworzenie nowych zadań.
Pobieranie listy zadań oraz pojedynczego zadania.
Aktualizowanie istniejących zadań.
Usuwanie zadań.
Filtrowanie zadań według statusu i priorytetu.
Prosta autoryzacja użytkowników.
Technologie
Node.js
Express.js
MongoDB
Mongoose
JWT (autoryzacja)
Instalacja
1. Klonowanie repozytorium
bash
git clone https://github.com/username/simple-task-api.git
cd simple-task-api

2. Instalacja zależności
bash
npm install

3. Konfiguracja zmiennych środowiskowych

Utwórz plik .env w głównym katalogu projektu:

env
PORT=3000
MONGODB_URI=mongodb://localhost:27017/simple-task-api
JWT_SECRET=your_secret_key

4. Uruchomienie aplikacji

Tryb produkcyjny:

bash
npm start


Tryb developerski:

bash
npm run dev


API będzie dostępne pod adresem:

http://localhost:3000

Użycie

Do komunikacji z API można wykorzystać narzędzia takie jak Postman, Insomnia lub curl.

Przykładowe żądanie utworzenia zadania:

http
POST /api/tasks
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN


Przykładowe dane JSON:

json
{
  "title": "Przygotować dokumentację",
  "description": "Utworzyć plik README.md",
  "status": "pending",
  "priority": "high"
}


Przykładowe filtrowanie zadań:

http
GET /api/tasks?status=pending&priority=high

Endpointy API
Autoryzacja
Metoda	Endpoint	Opis
POST	/api/auth/register	Rejestracja użytkownika
POST	/api/auth/login	Logowanie użytkownika
Zadania
Metoda	Endpoint	Opis
GET	/api/tasks	Pobieranie wszystkich zadań
GET	/api/tasks/:id	Pobieranie zadania według ID
POST	/api/tasks	Tworzenie nowego zadania
PUT	/api/tasks/:id	Aktualizacja zadania
DELETE	/api/tasks/:id	Usuwanie zadania
Parametry filtrowania

Endpoint GET /api/tasks obsługuje następujące parametry:

Parametr	Opis	Przykładowa wartość
status	Status zadania	pending, in-progress, completed
priority	Priorytet zadania	low, medium, high

Przykład:

http
GET /api/tasks?status=in-progress&priority=high

Przykładowe statusy zadań
pending – oczekujące
in-progress – w trakcie realizacji
completed – zakończone
Przykładowe priorytety
low – niski
medium – średni
high – wysoki
Licencja

Projekt udostępniony na licencji MIT.
