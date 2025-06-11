# Askos Tours - Sistema Informativo per Tour Operator

**Askos Tours** è un sistema informativo realizzato con Django per la gestione completa dei tour, guide, clienti e prenotazioni. Il progetto supporta registrazione differenziata per clienti e staff, gestione dei tour, filtri per lingua, recensioni e dashboard personalizzate.

---

## 📌 Funzionalità Implementate

### 👤 Clienti
- Registrazione con codice fiscale, email, lingua preferita, telefono.
- Login tramite codice fiscale e password.
- Visualizzazione tour disponibili.
- Filtro tour per lingua preferita.
- Prenotazione tour (solo se la data è futura).
- Annullamento prenotazione (solo prima della data).
- Recensione tour già svolti (una sola per tour).
- Visualizzazione dei tour prenotati.

### 🧭 Staff (Guide / Driver)
- Registrazione con selezione multipla delle lingue parlate.
- Login tramite codice fiscale e password.
- Visualizzazione dei tour assegnati futuri (guida o driver).

### 🗺️ Tour
- Ogni tour è associato a:
  - una lingua
  - una o più guide
  - uno o più driver
- Visualizzazione dei partecipanti prenotati.
- Visibilità solo se la data è ancora futura.

### ⭐ Recensioni
- I clienti possono recensire solo i tour passati a cui hanno partecipato.
- Tutte le recensioni sono visibili pubblicamente in una pagina dedicata.

### 🔐 Amministratore (Admin)
- Gestione completa da pannello Django:
  - Tour
  - Clienti
  - Staff
  - Lingue
  - Prenotazioni
  - Recensioni

---

## ▶️ Come Avviare il Progetto

1. Esegui le migrazioni per creare le tabelle:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
2. **Crea un superuser** per accedere al pannello admin:
   ```bash
   python manage.py createsuperuser
   ```
3. **Avvia il server Django:**
   ```bash
   python manage.py runserver
   ```
4. Accedi all'app da `http://127.0.0.1:8000/`.

---

## 👨‍🏫 Accessi Utente

- **Clienti**:
  - Registrazione autonoma tramite app.
  - Login con codice fiscale.

- **Staff** (Guida / Driver):
  - Registrazione autonoma con selezione lingue.
  - Accesso personalizzato per visualizzare i tour futuri.

- **Admin**:
  - Accesso da `http://127.0.0.1:8000/admin`
  - Gestione completa dei dati.

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Autore**:
  Paolo Desiderio 
  **Corso**:
  Basi di Dati(6 cfu)
**Università degli Studi di Napoli Parthenope**
