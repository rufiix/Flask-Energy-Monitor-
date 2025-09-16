# Energy Monitor - System Monitorowania Zużycia Energii

## Opis projektu
Energy Monitor to aplikacja webowa do monitorowania zużycia energii elektrycznej przez różne urządzenia. System pozwala na śledzenie zużycia energii w czasie rzeczywistym, generowanie raportów dziennych oraz eksport danych do formatu CSV.

## Struktura projektu
```
energy-monitor/
├── app.py              # Główna aplikacja Flask
├── init_db.py         # Skrypt inicjalizujący bazę danych
├── init_db.sql        # Schemat bazy danych SQL
├── check_db.py        # Narzędzie do sprawdzania stanu bazy
├── populate_db.py     # Skrypt generujący dane testowe
├── requirements.txt    # Zależności Pythona
├── energy.db          # Baza danych SQLite
└── static/
    └── index.html     # Frontend aplikacji
```

## Technologie
- Backend: Python + Flask
- Baza danych: SQLite
- Frontend: HTML + JavaScript
- Wizualizacja: Chart.js

## Struktura bazy danych

### Tabela `devices`
```sql
CREATE TABLE devices (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  location TEXT,
  serial TEXT UNIQUE,
  installed_at DATETIME DEFAULT (datetime('now'))
);
```

### Tabela `readings`
```sql
CREATE TABLE readings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_id INTEGER NOT NULL,
  timestamp DATETIME NOT NULL,
  value_wh REAL NOT NULL,
  FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
);
```

## API Endpoints

### GET /api/devices
Lista wszystkich urządzeń w systemie.

**Odpowiedź:**
```json
[
  {
    "id": 1,
    "name": "Licznik 1",
    "location": "Biuro",
    "serial": "SN001"
  }
]
```

### POST /api/devices
Dodawanie nowego urządzenia.

**Przykładowe dane:**
```json
{
  "name": "Licznik 2",
  "location": "Sala konferencyjna",
  "serial": "SN002"
}
```

### POST /api/readings
Dodawanie nowego odczytu energii.

**Przykładowe dane:**
```json
{
  "device_id": 1,
  "value_wh": 450.5,
  "timestamp": "2025-09-14T12:00:00"
}
```

### GET /api/reports/daily
Raport dzienny zużycia energii w formacie JSON.

**Parametry:**
- `date`: Data w formacie YYYY-MM-DD (domyślnie: dzisiaj)

**Przykładowa odpowiedź:**
```json
{
  "date": "2025-09-14",
  "data": [
    {
      "device_id": 1,
      "name": "Licznik 1",
      "kwh": 10.5
    }
  ]
}
```

### GET /api/reports/daily.csv
Raport dzienny w formacie CSV do pobrania.

## Instalacja i uruchomienie

1. Klonowanie repozytorium:
```bash
git clone <repository-url>
cd energy-monitor
```

2. Tworzenie wirtualnego środowiska Python:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # Linux/macOS
```

3. Instalacja zależności:
```bash
pip install -r requirements.txt
```

4. Inicjalizacja bazy danych:
```bash
python init_db.py
```

5. (Opcjonalnie) Generowanie danych testowych:
```bash
python populate_db.py
```

6. Uruchomienie aplikacji:
```bash
python app.py
```

Aplikacja będzie dostępna pod adresem: http://127.0.0.1:5000

## Funkcje frontendowe

### Wyświetlanie danych
- Interaktywny wykres słupkowy pokazujący zużycie energii dla każdego urządzenia
- Liczniki pokazujące aktualne zużycie dla każdego urządzenia
- Możliwość wyboru daty do analizy
- Eksport danych do CSV

### Elementy interfejsu
- Pole wyboru daty
- Przycisk "Pokaż" do aktualizacji danych
- Przycisk "Pobierz CSV" do eksportu danych
- Wykres Chart.js z responsywnym layoutem
- Sekcja liczników z wartościami dla każdego urządzenia

## Narzędzia deweloperskie

### check_db.py
Narzędzie do weryfikacji stanu bazy danych i debugowania.

### populate_db.py
Skrypt generujący przykładowe dane do testów:
- Tworzy 10 urządzeń testowych
- Generuje odczyty za ostatnie 30 dni
- 24 odczyty dziennie per urządzenie
- Losowe wartości między 100 a 500 Wh

## Bezpieczeństwo
- Walidacja danych wejściowych
- Parametryzowane zapytania SQL
- Zabezpieczenie przed SQL injection
- Obsługa błędów i walidacja typów danych

## Dalszy rozwój
Możliwe rozszerzenia systemu:
- Autentykacja użytkowników
- Panel administracyjny
- Raporty tygodniowe/miesięczne
- Powiadomienia o anomaliach
- Prognozowanie zużycia
- API do integracji z innymi systemami

## Znane problemy
- Brak obsługi stref czasowych
- Brak paginacji dla dużych zbiorów danych
- Brak cachowania wyników zapytań

## Licencja
Ten projekt jest dostępny na licencji MIT.