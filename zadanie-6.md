Oto prosty diagram Mermaid przedstawiający proces CI/CD:

mermaid

```mermaid

flowchart LR
    A["📝 Commit"] --> B["🔨 Build"]
    B --> C["🧪 Test"]
    C --> D["🚀 Deploy"]

    style A fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    style B fill:#fef3c7,stroke:#d97706,color:#78350f
    style C fill:#dcfce7,stroke:#16a34a,color:#14532d
    style D fill:#f3e8ff,stroke:#9333ea,color:#581c87
```

Opis etapów:

1. Commit – programista zapisuje zmiany w repozytorium Git.
2. Build – system buduje aplikację.
3. Test – automatyczne testy sprawdzają poprawność kodu.
4. Deploy – aplikacja zostaje wdrożona na serwerze lub środowisku produkcyjnym.

