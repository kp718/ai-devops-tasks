Przykład użycia

javascript
const tasks = [
    { id: 3, title: "Testowanie", status: "completed" },
    { id: 1, title: "Projektowanie", status: "completed" },
    { id: 2, title: "Programowanie", status: "in progress" },
    { id: 4, title: "Dokumentacja", status: "completed" }
];

const result = getCompletedTaskTitles(tasks);

console.log(result);
Wynik:


javascript
[
    "Projektowanie",
    "Testowanie",
    "Dokumentacja"
]
Wyjaśnienie działania
.filter() – wybiera zadania ze statusem "completed".

.sort() – sortuje zadania rosnąco według id.

.map() – zwraca wyłącznie tytuły zadań.

Uwaga: sort() modyfikuje oryginalną tablicę. Jeśli chcesz zachować jej pierwotną kolejność, zastosuj:


javascript
function getCompletedTaskTitles(tasks) {
    return tasks
        .filter(task => task.status === "completed")
        .toSorted((a, b) => a.id - b.id)
        .map(task => task.title);
}