GET /api/users
Opis

Endpoint GET /api/users zwraca listę użytkowników systemu. Umożliwia pobieranie wyników z podziałem na strony (paginacja) oraz filtrowanie użytkowników według przypisanej roli.

Parametry zapytania (Query Parameters)
Parametr	Typ	Wymagany	Domyślna wartość	Opis
page	integer	Nie	1	Numer strony wyników.
limit	integer	Nie	10	Liczba użytkowników na stronie. Maksymalna wartość: 100.
role	string	Nie	Brak	Filtruje użytkowników według przypisanej roli.
Przykładowe żądanie

Pobranie pierwszej strony z listą 10 użytkowników:

http
GET /api/users?page=1&limit=10


Pobranie drugiej strony z listą użytkowników posiadających rolę admin:

http
GET /api/users?page=2&limit=10&role=admin

Przykładowa odpowiedź

Status HTTP: 200 OK

json
{
  "data": [
    {
      "id": 1,
      "name": "Jan Kowalski",
      "email": "jan.kowalski@example.com",
      "role": "admin"
    },
    {
      "id": 2,
      "name": "Anna Nowak",
      "email": "anna.nowak@example.com",
      "role": "user"
    },
    {
      "id": 3,
      "name": "Piotr Wiśniewski",
      "email": "piotr.wisniewski@example.com",
      "role": "user"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 3,
    "totalPages": 1
  }
}


Uwaga: Powyższy format odpowiedzi jest przykładowy i zakłada strukturę z polami data oraz pagination.

Uwagi
Jeśli parametr page nie zostanie podany, przyjmowana jest wartość 1.
Jeśli parametr limit nie zostanie podany, przyjmowana jest wartość 10.
Maksymalna liczba użytkowników zwracanych w jednym żądaniu wynosi 100.
Parametr role jest opcjonalny. Jeśli zostanie podany, zwracani są wyłącznie użytkownicy posiadający wskazaną rolę.
Paginacja umożliwia pobieranie dużych zbiorów danych w mniejszych partiach.