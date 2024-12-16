# Personenstrom-Simulation mit Pygame und JSON-Konfiguration

Dieses Projekt simuliert das Verhalten von Menschenströmen in einer Umgebung mithilfe von `pygame` und einer JSON-basierten Konfiguration. Die Simulation ermöglicht es, Grid-Layouts, Hindernisse, Zielpunkte (Targets) und Spawner dynamisch zu definieren und visuell darzustellen.

## Voraussetzungen

### Systemanforderungen
- Python 3.13
- Betriebssystem: Windows, macOS oder Linux

### Installation der Abhängigkeiten

1. Stelle sicher, dass Python 3.13 oder neuer installiert ist.
2. Installiere die erforderlichen Bibliotheken mit folgendem Befehl:
   ```bash
   pip install -r requirements.txt

## Verwendung

### Simulation starten
1. Stelle sicher, dass die JSON-Konfigurationsdatei `simulationConfig/simulation_config.json` korrekt definiert ist.
2. Starte die Simulation mit folgendem Befehl:
   ```bash
   python run.py

### Unit-Tests ausführen
1. Starte die Unit-Tests mit folgendem Befehl:
   ```bash
   python -m unittest discover -s tests -p "test_*.py"