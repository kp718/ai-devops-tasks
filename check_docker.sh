
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
