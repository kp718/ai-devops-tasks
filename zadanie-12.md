def find_duplicates(list_of_items):
    duplicates = []
    for i in range(len(list_of_items)):
        for j in range(i+1, len(list_of_items)):
            if list_of_items[i] == list_of_items[j] and list_of_items[i] not in duplicates:
                duplicates.append(list_of_items[i])
    return duplicates






Tak\! Twój kod można znacząco zoptymalizować. Obecna implementacja wykorzystuje dwie zagnieżdżone pętle, przez co ma złożoność czasową O(n²).

Można to poprawić, wykorzystując strukturę `set` (zbiór), która zapewnia średnio stały czas sprawdzania, czy element już występuje.

## 1. Zoptymalizowana wersja – rekomendowana

python

```python
def find_duplicates(list_of_items):
    seen = set()
    duplicates = set()

    for item in list_of_items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)

    return list(duplicates)
```

Złożoność obliczeniowa:

- Czasowa: O(n) – zamiast O(n²).
- Pamięciowa: O(n) – przechowujemy zbiory elementów.

## 2. Wersja zachowująca kolejność występowania duplikatów

Warto zauważyć, że poprzednia wersja nie gwarantuje kolejności duplikatów zgodnej z kolejnością ich pierwszego powtórzenia.

Jeżeli chcesz zachować zachowanie oryginalnego kodu, zastosuj:

python

```python
def find_duplicates(list_of_items):
    seen = set()
    duplicates = []

    for item in list_of_items:
        if item in seen:
            if item not in duplicates:
                duplicates.append(item)
        else:
            seen.add(item)

    return duplicates
```

Ta wersja również ma złożoność O(n) tylko wtedy, gdy sprawdzanie `duplicates` jest wydajne — tutaj jednak `item not in duplicates` ma złożoność O(n).

Dlatego lepszym rozwiązaniem jest:

python

```python
def find_duplicates(list_of_items):
    seen = set()
    duplicates = []
    duplicates_set = set()

    for item in list_of_items:
        if item in seen and item not in duplicates_set:
            duplicates.append(item)
            duplicates_set.add(item)
        else:
            seen.add(item)

    return duplicates
```

## 3. Przykład działania

python

```python
items = [1, 2, 3, 2, 4, 5, 1, 3, 3]

print(find_duplicates(items))
```

Wynik:

python

```python
[2, 1, 3]
```

## 4. Porównanie wydajności

| Właściwość | Oryginalny kod | Zoptymalizowany kod |
| --- | --- | --- |
| Złożoność czasowa | O(n²) | O(n) średnio |
| Złożoność pamięciowa | O(n) | O(n) |
| Zachowanie kolejności | Tak | Tak (wersja 2) |
| Obsługa elementów hashable | Nie wymaga hashowania | Wymaga hashability |

Moja rekomendacja: wybierz wersję 2 z dodatkowym zbiorem `duplicates_set`. Jest najbardziej uniwersalna spośród przedstawionych wersji, zachowuje kolejność wyników i zapewnia średnią złożoność czasową O(n).

Uwaga: implementacje wykorzystujące `set` wymagają, aby elementy listy były hashowalne (np. liczby, napisy czy krotki zawierające hashowalne elementy).