Poniżej znajduje się funkcja uzupełniona o komentarze dokumentacyjne w formacie JSDoc:

javascript

```javascript

/**
 * Pobiera dane użytkownika z zewnętrznego API.
 *
 * W przypadku powodzenia zwraca obiekt zawierający imię,
 * adres e-mail oraz datę ostatniego logowania użytkownika.
 * W przypadku błędu wyświetla komunikat w konsoli i zwraca null.
 *
 * @async
 * @function fetchUserData
 * @param {string|number} userId - Unikalny identyfikator użytkownika.
 * @returns {Promise<{name: string, email: string, lastLogin: Date}|null>}
 * Promise zwracający obiekt z danymi użytkownika lub null w przypadku błędu.
 *
 * @throws {Error} Błąd HTTP w przypadku nieudanego żądania.
 *
 * @example
 * fetchUserData(123)
 *   .then(user => {
 *     if (user) {
 *       console.log(user.name);
 *       console.log(user.email);
 *       console.log(user.lastLogin);
 *     }
 *   });
 */
function fetchUserData(userId) {
  return fetch(`https://api.example.com/users/${userId}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      return {
        name: data.name,
        email: data.email,
        lastLogin: new Date(data.lastLoginTimestamp)
      };
    })
    .catch(error => {
      console.error('Fetch error:', error);
      return null;
    });
}
```

Zastosowane znaczniki JSDoc:

- `@async` – oznacza funkcję asynchroniczną.
- `@function` – określa nazwę dokumentowanej funkcji.
- `@param` – opisuje parametr wejściowy.
- `@returns` – określa typ i opis zwracanej wartości.
- `@throws` – dokumentuje możliwy wyjątek.
- `@example` – przedstawia przykład użycia funkcji.

Uwaga: `@throws` dokumentuje błąd HTTP rzucany wewnątrz funkcji, ale ponieważ jest on przechwytywany przez `.catch()`, funkcja ostatecznie zwraca `null`, a nie odrzuca Promise tym błędem.