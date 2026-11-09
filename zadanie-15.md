Co zostało poprawione?
Usunięto wielokrotne warunki – zamiast if...else if wykorzystujemy jeden obiekt konfiguracyjny.

Wprowadzono DEFAULT_CONFIG – domyślna konfiguracja jest zdefiniowana tylko w jednym miejscu.

Zastosowano operator ?? – jeśli środowisko nie istnieje w konfiguracji, zwracana jest konfiguracja domyślna.

Ułatwiono rozszerzanie – dodanie nowego środowiska wymaga jedynie dodania kolejnego wpisu w ENV_CONFIGS.

Przykładowe użycie

javascript
console.log(getEnvironmentConfig('production'));
// {
//   apiUrl: 'https://api.example.com',
//   debug: false,
//   timeout: 15000
// }

console.log(getEnvironmentConfig('unknown'));
// {
//   apiUrl: 'http://localhost:3000/api',
//   debug: true,
//   timeout: 5000
// }
Dodatkowa uwaga: W tej wersji development wskazuje na ten sam obiekt co DEFAULT_CONFIG. Jeśli konfiguracje będą modyfikowane w trakcie działania aplikacji, warto zwracać kopię:


javascript
function getEnvironmentConfig(env) {
  return { ...(ENV_CONFIGS[env] ?? DEFAULT_CONFIG) };
}
Rekomendacja: Pierwsza wersja jest wystarczająca, jeśli konfiguracja jest tylko odczytywana. Druga jest bezpieczniejsza, jeśli istnieje możliwość jej modyfikowania.