
flowchart TD
    A([Start: Trigger Jenkins Pipeline]) --> B[Checkout kodu z Git]
    B --> C[Budowanie aplikacji]
    C --> D[Testy jednostkowe]
    D --> E[Analiza statyczna kodu<br/>SonarQube]
    E --> F[Skanowanie bezpieczeństwa<br/>SAST / Dependency Check]

    F --> G[Budowanie obrazu Docker]
    G --> H[Testy integracyjne]
    
    H --> I{Wszystkie testy<br/>zakończone sukcesem?}
    I -- Nie --> X[Pipeline FAILED]
    I -- Tak --> J[Wdrożenie na STAGING]

    J --> K[Testy akceptacyjne<br/>i smoke tests]
    K --> L{Akceptacja<br/>wdrożenia?}

    L -- Nie --> X
    L -- Tak --> M[Wdrożenie na PRODUCTION]

    M --> N[Weryfikacja wdrożenia<br/>Health Check]
    N --> O([Pipeline SUCCESS])

    X --> P[Powiadomienie zespołu<br/>Slack / Email]

    style A fill:#d1e7dd,stroke:#198754,color:#000
    style O fill:#d1e7dd,stroke:#198754,color:#000
    style X fill:#f8d7da,stroke:#dc3545,color:#000
    style J fill:#cfe2ff,stroke:#0d6efd,color:#000
    style M fill:#fff3cd,stroke:#ffc107,color:#000
