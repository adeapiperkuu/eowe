**PROJEKTKONZEPT • EOWE KI-WORKSPACE** 

Vertraulich | 13 Juli 2026 

# **PROJEKTKONZEPT** 

KI-basierter All-in-One Workspace für EOWE – European Open Water Events 

Update: 13.07.2026 Version 2 

Projektverantwortlich: Borek Solutions Group Auftraggeber: EOWE – European Open Water Events 

_VERTRAULICH_ 

© 2026 Borek Solutions Group – Vertrauliches Dokument 

Seite 1 von 19 

**PROJEKTKONZEPT • EOWE KI-WORKSPACE** 

Vertraulich | 13 Juli 2026 

## **1. Projektsteckbrief** 

Der folgende Steckbrief gibt einen kompakten Überblick über alle wesentlichen Eckdaten des Projekts. Er dient als schnelle Referenz für alle Projektbeteiligten und bildet die verbindliche Grundlage für Scope, Termine und Verantwortlichkeiten. 

|**Projektname**|EOWE Workspace – KI-basiertes All-in-One ERP-System|
|---|---|
|**Auftraggeber**|EOWE – European Open Water Events|
|**Projektverantwortlich**|Borek Solutions Group|
|**Projektstatus**|Initialisierungsphase – Genehmigung ausstehend|
|**Geplanter Projektstart**|01. Juli 2026 (vorbehaltlich finaler Freigabe)|
|**Projektlaufzeit**|4 Monate – Juli bis ~02 November 2026|
|**Geplanter Go-Live**|02. November 2026 (Module 1–5 vollständig produktiv)|
|**Interim-Meilenstein**|ca. 07. September 2026 (Modul 1 + Modul 2 produktiv)|
|**Modul 6**|Optionale Erweiterung C – separate Beauftragung nach Go-Live|
|**Projekttyp**|Neuentwicklung (Greenfield) – Maßgeschneidertes System|
|**Vorgehensmodell**|Agile Softwareentwicklung (Scrum) – 2-Wochen-Sprints|
|**Klassifizierung**|Strategisches IT-Projekt|
|**Sprache / Markt**|Deutsch (DE) / DACH-Region|
|**Technologie-Plattform**|Cloud-native (SaaS) – React.js, Node.js/Python, PostgreSQL|



© 2026 Borek Solutions Group – Vertrauliches Dokument 

Seite 2 von 19 

**PROJEKTKONZEPT • EOWE KI-WORKSPACE** 

Vertraulich | 13 Juli 2026 

## **2. Ausgangssituation und Problemanalyse** 

### **2.1 IST-Zustand: Aktuelle Infrastruktur der EOWE** 

Die EOWE verwaltet eine wachsende Anzahl von Open-Water-Schwimmveranstaltungen – darunter den renommierten Alpen Open Water Cup und den Full-Moon-Cup – sowie ein breites Netzwerk aus Teilnehmern, Sponsoren und Dienstleistern. Trotz des gestiegenen Umfangs und der zunehmenden Komplexität basiert die operative Abwicklung bisher nahezu vollständig auf manuellen Prozessen und isolierten Werkzeugen. Konkret sieht der aktuelle Betrieb so aus: 

|**Bereich**|**Aktueller Zustand**|**Konsequenz / Risiko**|
|---|---|---|
|Datenhaltung|Verteilte Excel-Listen, SharePoint-<br>Ablagen ohne einheitliche Struktur|Dateninkonsistenzen,<br>Versionskonflikte, hoher<br>Suchaufwand|
|Teilnehmerkommunikation|Manuelle E-Mail-Beantwortung<br>durch Geschäftsführung (z.B.<br>Wetsuit-Anfragen)|Hohe Zeitbelastung für GF,<br>inkonsistente Antwortqualität|
|Zahlungsabgleich|Manuelle Prüfung von<br>Kontoauszügen gegen Excel-<br>Meldung|Fehleranfälligkeit, zeitverzögerte<br>Buchungen|
|Event-Fotoverwaltung|Händisches Sortieren und<br>Benennen von Fotografen-Bildern<br>durch GF|Enormer Zeitaufwand, kein<br>systematischer Archivzugang|
|Inventar & Materialien|Keine systematische Verfolgung<br>von Bojen, Wetsuits, Merchandise|Überbestellungen, Engpässe vor<br>Events|
|Vertrags- &<br>Sponsorenverwaltung|Ablage in SharePoint ohne<br>automatisches Fristenmanagement|Verpasste Verlängerungsfristen,<br>fehlende Zahlungsübersicht|
|Systemintegration|Tiger Timing und RaceResult<br>werden manuell bedient, keine<br>Datensynchronisation|Medienbrüche, doppelte<br>Datenpflege, Fehlerrisiko|



### **2.2 Wachstumstreiber und Handlungsdruck** 

Die EOWE befindet sich in einer Phase des aktiven Wachstums: Neue Event-Serien, steigende Teilnehmerzahlen und das geplante Angebot an Fremd-Events sowie Schwimmcamps erhöhen die operative Komplexität exponentiell. Die bestehende Infrastruktur stößt dabei an ihre strukturellen Grenzen. Ohne eine konsequente Digitalisierung und Automatisierung drohen folgende Risiken: 

- Skalierungsbarriere: Die Geschäftsführung verbringt einen überproportional hohen Anteil der Arbeitszeit mit administrativen Routineaufgaben, die das Wachstum faktisch deckeln. 

- Qualitätsverlust: Mit steigender Teilnehmerzahl sinkt bei manueller Abwicklung zwangsläufig die Reaktionsgeschwindigkeit und Konsistenz in der Kommunikation. 

- Datenverlust-Risiko: Unstrukturierte Dateiablagen ohne Versions- und Zugriffsmanagement sind ein Sicherheitsrisiko und erschweren die Nachvollziehbarkeit. 

- Wettbewerbsnachteil: Professionell agierende Mitbewerber mit digitaler Infrastruktur können schneller, günstiger und teilnehmerfreundlicher operieren. 

© 2026 Borek Solutions Group – Vertrauliches Dokument 

Seite 3 von 19 

**PROJEKTKONZEPT • EOWE KI-WORKSPACE** 

Vertraulich | 13 Juli 2026 

### **2.3 Strategische Lösungsrichtung** 

Die Lösung liegt nicht in der Einführung weiterer isolierter Einzelsoftware ("Insellösungen"), sondern im Aufbau eines integrierten, maßgeschneiderten All-in-One-Systems, das alle betrieblichen Prozesse in einer einzigen, zentralen Plattform vereint. Bewährte externe Speziallösungen wie Tiger Timing oder RaceResult werden dabei nicht ersetzt, sondern über APIs bidirektional angebunden und in die zentrale Datenwelt integriert. Dieses Vorgehen folgt vier strategischen Leitprinzipien: Single Source of Truth (eine einzige, stets aktuelle Datenbasis), API-First-Architektur (Integrierbarkeit als Designprinzip), KI-gestützte Automatisierung (Entlastung der GF durch intelligente Prozesse) sowie modulare Skalierbarkeit (schrittweise Erweiterung ohne Systemumbrüche). 

© 2026 Borek Solutions Group – Vertrauliches Dokument 

Seite 4 von 19 

**PROJEKTKONZEPT • EOWE KI-WORKSPACE** 

Vertraulich | 13 Juli 2026 

## **3. Projektziele und Erfolgskriterien (KPIs)** 

### **3.1 Strategische Projektziele** 

Das Projekt verfolgt drei übergeordnete strategische Ziele, die gleichrangig zu behandeln sind: 

|**#**|**Strategisches Ziel**|**Messkriterium (KPI)**|**Zielwert**|
|---|---|---|---|
|1|Operative Entlastung der<br>Geschäftsführung|Reduktion manueller<br>Aufgabenzeit (GF)|≥ 60% Zeitersparnis bei<br>Routineaufgaben|
|2|Datentransparenz &<br>Datenqualität|Single Source of Truth<br>etabliert|100% der operativen Daten im<br>zentralen System|
|3|Skalierbarkeit für Wachstum|Neue Events ohne Admin-<br>Mehraufwand|Onboarding neuer Event-Serie <<br>1 Arbeitstag|



### **3.2 Abgrenzung: Was dieser Scope NICHT umfasst (Out-of-Scope)** 

Zur Vermeidung von Scope-Creep sind folgende Bereiche explizit aus dem 4-Monats-Scope ausgeschlossen. Sie können als optionale Erweiterungen separat beauftragt werden: 

- Modul 6 – Abo-Modell & Zukunftsplattform (optionale Erweiterung C, Scope und Zeitplan nach Go-Live gemeinsam definieren) 

- Entwicklung einer öffentlichen Teilnehmer-App (Consumer-facing Mobile App für iOS/Android) 

- Vollständiges Buchhaltungssystem (DATEV-Schnittstelle ist im Scope enthalten; kein Ersatz des Steuerberaters oder der vollständigen Buchführungssoftware) 

- Echtzeit-Geodaten-Streckensimulation (geplante Ausbaustufe in Modul 6) 

- Mandantenfähigkeit / SaaS-Lizenzierung der Plattform an Dritte (Ausbaustufe Modul 6) 

© 2026 Borek Solutions Group – Vertrauliches Dokument 

Seite 5 von 19 

**PROJEKTKONZEPT • EOWE KI-WORKSPACE** 

Vertraulich | 13 Juli 2026 

## **4. Agile Vorgehensweise & Methodik** 

### **4.1 Warum Agile/Scrum für dieses Projekt?** 

Dieses Projekt weist mehrere Charakteristika auf, die einen klassischen "Wasserfall"-Ansatz mit starren Meilensteinplänen zu einem Risiko machen würden: Die konkreten Anforderungen werden sich in den ersten Wochen schärfen, Prioritäten können sich durch neue Erkenntnisse verschieben, und die GF soll frühzeitig echten Mehrwert erleben nicht erst am Ende der 4 Monate. Daher wählen wir die agile ScrumMethodik mit folgenden Kernelementen: 

### **4.2 Scrum-Zeremonien und Rhythmus** 

|(vorgeschlagen, m<br>|it dem Auftragge<br>|ber final ab<br>|zustimmen)<br>||
|---|---|---|---|---|
|**Zeremonie**|**Frequenz**|**Dauer**|**Teilnehmer**|**Zweck**|
|Sprint Planning|Alle 2 Wochen<br>(Montag)|2<br>Stunden|Entwicklungsteam|Aufgaben für nächsten<br>Sprint planen und<br>schätzen|
|Daily Standup|Täglich<br>(Werktage)|15<br>Minuten|Entwicklungsteam|Status, Blocker,<br>Synchronisation|
|Sprint Review|Alle 2 Wochen<br>(Freitag)|1–2<br>Stunden|Entwicklungsteam +<br>Auftraggeber|Demo fertiger Features,<br>Feedback einholen und<br>Zwischenstand absegnen|
|Steering<br>Committee|1x monatlich|1<br>Stunde|Projektleitung<br>(Auftraggeber + Borek<br>Solutions Group)|Budget, Strategie,<br>Meilenstein-Review,<br>Risiko-Update|



### **4.3 Change-Request-Prozess** 

In einem agilen Projekt ist Veränderung keine Ausnahme, sondern ein normaler Bestandteil. Dennoch braucht es einen klaren Prozess, um unkontrolliertes Wachstum des Scope (Scope Creep) zu verhindern. Change Requests werden wie folgt behandelt: 

- Jede Anforderungsänderung oder -erweiterung wird als neues "Issue" im Backlog erfasst (mit Beschreibung, Priorität und Aufwandsschätzung in Story Points). 

- Änderungen mit geringem Aufwand (< 4 Story Points) werden im nächsten regulären Sprint Planning priorisiert und können direkt in den nächsten Sprint einfließen. 

- Änderungen mit größerem Aufwand (≥ 4 Story Points oder Scope-Erweiterungen) werden im monatlichen Steering Committee besprochen und genehmigt, bevor sie geplant werden. 

- Für jede Änderung, die den vereinbarten 4-Monats-Scope oder das Budget beeinflusst, ist eine schriftliche Freigabe durch den Auftraggeber erforderlich. 

- Alle genehmigten Change Requests werden im "Änderungsprotokoll" dokumentiert, das monatlich allen Stakeholdern kommuniziert wird. 

© 2026 Borek Solutions Group – Vertrauliches Dokument 

Seite 6 von 19 

**PROJEKTKONZEPT • EOWE KI-WORKSPACE** 

Vertraulich | 13 Juli 2026 

## **5. Projektphasen und Meilensteinplan (4-Monats-Scope)** 

Das Projekt ist in drei Phasen unterteilt, die vollständig innerhalb der 4-monatigen Vertragslaufzeit (Juli – Oktober 2026) abgeschlossen werden. Phase 1 umfasst das Kern-MVP mit Modul 1 und 2 (Interim-GoLive ca. 07. September 2026). Phase 2 bringt Modul 3, 4 und 5 in den produktiven Betrieb (Full-Go-Live 02 November 2026). Beide Entwicklungsteams (2x KI-Builder) arbeiten in Phase 2 teilweise parallel an unterschiedlichen Modulen. 

**Priorisierung innerhalb der Phasen (Kundenfeedback EOWE, Juli 2026):** In Phase 1 hat die Eventfunktionalität inkl. Ausschreibungsmanagement Vorrang; die Financial-Funktionen (Modul 2) werden bei Ressourcenengpässen zeitlich nachrangig behandelt. In Phase 2 hat die ShopFunktionalität (Modul 3) Vorrang für das Weihnachtsgeschäft; die Funktionen 

Inventar-/Materialverwaltung (Events) und Fuhrpark-Management können bei Bedarf nach hinten gestellt werden. 

|**Phase**|**Bezeichnung**|**Module**|**Zeitraum**|**Zentraler Meilenstein**|
|---|---|---|---|---|
|0|Projekt-Setup &<br>Architektur|–|~01.–10. Juli 2026|Dev-Umgebung aufgesetzt,<br>DB-Schema finalisiert,<br>Backlog befüllt|
|1|MVP: Kern-<br>Operations|M1 + M2|~13. Juli – 07. Sept.<br>2026|Interim-Go-Live ca. 07.<br>Sept. 2026: Event- &<br>Finanzmodul vollständig<br>produktiv|
|2|Erweiterung:<br>Commerce,<br>Marketing & CRM|M3 + M4<br>+ M5|~ 07. Sept. – 02. Nov<br>2026|Full-Go-Live 2 Nov. 2026:<br>Alle 5 Module vollständig<br>produktiv|



### **Phase 0: Projekt-Setup und Systemarchitektur (2 Wochen)** 

Die Initialisierungsphase legt das Fundament für alle folgenden Entwicklungsarbeiten. In dieser Phase werden keine Features entwickelt – stattdessen werden alle technischen und organisatorischen Voraussetzungen für einen reibungslosen Entwicklungsstart geschaffen. 

|**Sprint**|**Aufgaben**|**Deliverable**|
|---|---|---|
|Sprint 0 (01.–<br>10. Juli)|Cloud-Infrastruktur aufsetzen (PostgreSQL, Server,<br>CI/CD-Pipeline) | Datenbank-Schema für alle Module<br>entwerfen (ER-Diagramm) |<br>Entwicklungsumgebungen (Dev / Staging / Prod)<br>konfigurieren | API-Verträge mit Tiger Timing und<br>RaceResult klären | Grundgerüst Frontend (React.js)<br>und Backend (Node.js / Python) aufsetzen |<br>Projektmanagement-Tool (Jira/Linear) einrichten |<br>Initiales Product Backlog befüllen und priorisieren|Lauffähige<br>Entwicklungsumgebung |<br>Finalisiertes ER-Diagramm |<br>Initiales Product Backlog |<br>Klärung Tiger Timing API-<br>Zugang|



**Meilenstein M0:** Systemarchitektur finalisiert und vom Auftraggeber abgenommen. Alle Entwickler haben Zugang zu allen notwendigen Systemen. Sprint 1 kann am 13. Juli 2026 ohne Hindernisse starten. 

© 2026 Borek Solutions Group – Vertrauliches Dokument 

Seite 7 von 19 

**PROJEKTKONZEPT • EOWE KI-WORKSPACE** 

Vertraulich | 13 Juli 2026 

### **Phase 1: MVP – Modul 1 + Modul 2 (8 Wochen | | Interim-Go-Live 07. Sept. 2026)** 

Phase 1 ist die erste Kernphase des Projekts. Mit Fertigstellung von Modul 1 (Event-Management) und Modul 2 (Finanzen) geht das System erstmals in den produktiven Einsatz. Der Auftraggeber erlebt unmittelbar den ersten spürbaren Nutzen – von der automatisierten Teilnehmerverwaltung bis zum KIgestützten Zahlungsabgleich. Die 4 Sprints à 2 Wochen sind wie folgt strukturiert: 

**Priorisierung Phase 1 (Kundenfeedback EOWE):** Schwerpunkt ist die Eventfunktionalität inkl. Ausschreibungsmanagement. Hintergrund: EOWE plant, 2027 voraussichtlich drei neue Großstadtevents zu launchen, und will diese Mitte September – kurz nach dem letzten 2026er Event am Chiemsee – freischalten. Die Sprintfolge stellt daher das Eventmodul (M1) konsequent vor das Finanzmodul (M2); bei Ressourcenengpässen werden die Financial-Funktionen (M2) zeitlich nach hinten gestellt. Der zeitliche Bedarf der Geschäftsführung für Phase 1 ist frühzeitig zu klären und einzuplanen, da diese durch die operativen Events bis September stark eingebunden ist. 

|**Sprint**|**Schwerpunkt-Themen**|**User Stories (Auswahl)**|
|---|---|---|
|Sprint 1 (13.–<br>24. Juli)|M1: Datenbankmodell Events,<br>bidirektionale API-Anbindung Tiger<br>Timing, Grundstruktur Event-Anlage,<br>RaceResult-Import|"Als Nutzer kann ich eine neue<br>Veranstaltung mit allen Kerndaten (Ort,<br>Datum, Distanzen, Kapazität) in unter 5<br>Minuten anlegen." | "Als GF werden<br>Meldedaten aus Tiger Timing<br>automatisch ins System synchronisiert."|
|Sprint 2 (27.<br>Juli–07. Aug.)|M1: Dashboard Event-Übersicht<br>(Anmeldezahlen in Echtzeit),<br>automatischer Teilnehmer-Import,<br>Wetsuit-Verwaltung mit KI-<br>Größenempfehlung, KI-E-Mail-Assistent<br>(Prototyp)|"Als GF sehe ich auf dem Dashboard alle<br>aktiven Events mit aktuellen<br>Anmeldezahlen." | "Als GF erhalte ich für<br>eine Wetsuit-Anfrage automatisch einen<br>Antwort-Entwurf, den ich mit einem Klick<br>versenden kann."|
|Sprint 3 (10.–<br>21. Aug.)|M2: Digitale Vertragsgenerierung<br>(PDF), All-Event-Ticket mit Rabatt-<br>Engine, Rechnungsstellung &<br>automatisches Mahnwesen, Qonto-API-<br>Anbindung|"Als GF kann ich einen Teilnahmevertrag<br>mit einem Klick als PDF erzeugen und<br>direkt per E-Mail versenden." | "Als GF<br>sehe ich täglich alle neuen<br>Zahlungseingänge in Echtzeit."|
||M2: KI-Zahlungsabgleich MVP mit|"Als GF sehe ich alle Zahlungseingänge|
|Sprint 4 (24.<br>Aug.–04.<br>Sept.)|Konfidenz-Score, DATEV-Export-<br>Generator, OCR für<br>Eingangsrechnungen, Finanz-<br>Dashboard, User Acceptance Testing<br>(UAT), Interim-Go-Live-Vorbereitung|automatisch zugeordnet (grün) oder zur<br>Prüfung markiert (gelb)." | "Als<br>Steuerberater erhalte ich am<br>Monatsersten automatisch eine DATEV-<br>Exportdatei per E-Mail."|



**Meilenstein M1 – Interim-Go-Live:** ca. 07. September 2026. Modul 1 und 2 sind vollständig produktiv. Das EOWE-Team arbeitet aktiv mit dem System. KI-Zahlungszuordnungen und E-Mail-Antworten laufen automatisch durch. 

### **Phase 2: Erweiterung – Modul 3 + Modul 4 + Modul 5 (8 Wochen | Full-Go-Live 02. Nov. 2026)** 

Phase 2 baut auf dem produktiven M1/M2-Fundament auf und erweitert den Workspace um E- Commerce, Marketing, Foto-KI und das Sponsoring-CRM. Beide KI-Builder arbeiten in dieser Phase 

© 2026 Borek Solutions Group – Vertrauliches Dokument 

Seite 8 von 19 

**PROJEKTKONZEPT • EOWE KI-WORKSPACE** 

Vertraulich | 13 Juli 2026 

weitgehend parallel an unterschiedlichen Modulen, um alle drei Erweiterungsmodule innerhalb von 8 Wochen fertigzustellen. 

**Priorisierung Phase 2 (Kundenfeedback EOWE):** Schwerpunkt ist die Shop-Funktionalität (Modul 3), da sie für das Weihnachtsgeschäft benötigt wird und rechtzeitig produktiv sein muss. Die Funktionen Inventar-/Materialverwaltung (Events) und Fuhrpark-Management können innerhalb von Modul 3 bei Bedarf zeitlich nach hinten gestellt werden. 

|**Sprint**|**Schwerpunkt-Themen**|**User Stories (Auswahl)**|
|---|---|---|
|Sprint 5 (07.–<br>18. Sept.)|M4 (Builder A): Foto-Webportal für<br>Fotografen, Computer-Vision-Integration<br>(Google Vision API), automatische<br>Bildkategorisierung | M5 (Builder B):<br>Sponsoren-CRM Datenmodell,<br>Vertragserfassung, Fristentracking|"Als GF lade ich Fotos ins Portal, die KI<br>kategorisiert sie automatisch in<br>Startfotos, Streckenfotos und Zielfotos."<br>| "Als GF sehe ich alle Sponsoren-<br>Verträge mit ihren Laufzeiten und<br>ausstehenden Zahlungen auf einen<br>Blick."|
|Sprint 6 (21.<br>Sept.–02. Okt.)|M3 (Builder A): Online-Shop<br>(Produktverwaltung, Warenkorb,<br>Lagerbestand), Finisher-Shirt-Aggregation<br>in Echtzeit | M5 (Builder B): Alert-System<br>(Fristenbenachrichtigungen, Mahnungen),<br>Sponsoren-Report-Generator,<br>Dienstleister-Koordination|"Als GF sehe ich in Echtzeit, wie viele<br>Finisher-Shirts in welcher Größe pro<br>Event benötigt werden." | "Als GF<br>erhalte ich automatisch eine E-Mail,<br>wenn ein Sponsor-Vertrag in 90 Tagen<br>ausläuft."|
|Sprint 7 (05.–<br>16. Okt.)|**M3 (Builder A):**Retourenmanagement,<br>Shop-Integration, Echtzeit-<br>Lagerbestandsabgleich |**M4 (Builder A):**<br>Athleten-Erkennung (Startnummer-OCR),<br>Asset-Portal für Grid Sports |**M3 (Builder**<br>**B):**Inventar- & Materialverwaltung (Bojen,<br>Restubes), Fuhrpark-Management |**M5**<br>**(Builder B):**Kampagnen- &<br>Budgetplanung Sponsorenaktivierungen|"Als GF kann ich am Event-Tag direkt<br>am Tablet kassieren, der Lagerbestand<br>wird automatisch reduziert." | "Als Grid<br>Sports Agentur erhalte ich direkten<br>Zugang zu freigegebenen Fotos und<br>Assets für Social Media."|
|Sprint 8 (19.–<br>30. Okt.)|Gesamtintegration aller Module (M1–M5):<br>Modul-übergreifende Datenflüsse testen<br>und optimieren | Abschließendes User<br>Acceptance Testing (UAT) mit GF |<br>Performance-Tests und Security-Check |<br>Go-Live-Vorbereitung und Deployment<br>Produktion|"Als GF kann ich im System nahtlos<br>von einem Event zu den zugehörigen<br>Fotos, Verträgen und Zahlungen<br>navigieren." | Vollständiger UAT-<br>Abnahmebericht unterzeichnet vom<br>Auftraggeber|



**Meilenstein M2 – Full-Go-Live:** 02. November 2026. Alle fünf Module sind vollständig produktiv und integriert. Das EOWE-Team arbeitet mit einem einzigen, zentralen System für Event-Management, Finanzen, E-Commerce, Marketing und Sponsoring. 

© 2026 Borek Solutions Group – Vertrauliches Dokument 

Seite 9 von 19 

**PROJEKTKONZEPT • EOWE KI-WORKSPACE** 

Vertraulich | 13 Juli 2026 

## **6. Detaillierte Modulbeschreibungen** 

Im Folgenden werden alle sechs Module des EOWE Workspaces beschrieben. Module 1 bis 5 sind vollständiger Bestandteil des 4-Monats-Scopes. Modul 6 ist eine optionale Erweiterung, die nach dem Go-Live separat beauftragt werden kann. Die Modulbeschreibungen dienen als inhaltliche Grundlage für die Backlog-Erstellung und Sprint-Planung. 

### **Modul 1: Event- und Teilnehmermanagement  |  Scope: Phase 1 (M1+M2 Interim-Go-Live 07. Sept. 2026)** 

##### **Kernziel dieses Moduls** 

Das operative Herzstück des Gesamtsystems. Alle Prozesse rund um Planung, Durchführung und Nachbereitung der Open-Water-Events laufen hier zusammen. 

Zentrale Herausforderung: Die nahtlose bidirektionale Integration mit Tiger Timing (Meldewesen) und RaceResult (Ranglisten/Abrechnung) via API. 

**Ergänzung Kundenfeedback EOWE (Phase-1-Priorität):** Das Ausschreibungsmanagement (Erstellung, Verwaltung und Nachverfolgung von Ausschreibungen/Bewerbungen für neue Großstadtevents) ist als neue, vorrangige Funktion in Modul 1 aufzunehmen und im Rahmen der Phase-1-Backlog-Priorisierung zu detaillieren. Treiber: geplanter Launch von drei neuen Großstadtevents 2027 mit Freischaltung Mitte September 2026. 

#### **6.1.1 Funktionsübersicht** 

|**Funktion**|**Beschreibung**|**KI / Automatisierung**|
|---|---|---|
|Event- & Serien-<br>Verwaltung|Anlage von Einzelrennen, Distanzen (1,5km,<br>3km, 5km) und übergeordneten Serien<br>(Alpen Open Water Cup, Full-Moon-Cup).<br>Vollständige Metadaten: Ort, Datum,<br>Kapazität, Streckeninfos, Kategorien,<br>Zeitpläne.|–|
|Tiger Timing<br>Integration|Bidirektionale API-Anbindung: Meldedaten<br>werden automatisch aus Tiger Timing<br>importiert. Statusänderungen<br>(Nachmeldungen, Abmeldungen) werden in<br>Echtzeit synchronisiert. Keine manuelle<br>Übertragung mehr.|Automatische<br>Datensynchronisation|
|RaceResult<br>Integration|Ergebnislisten werden nach dem Event<br>automatisch aus RaceResult abgerufen und<br>im System gespeichert. Basis für Finisher-<br>Zertifikate und Abrechnung.|Auto-Import Ergebnisse|
|Kapazitäts-<br>Dashboard|Echtzeit-Aggregation der Anmeldezahlen<br>über alle Events. Wie viele freie Plätze gibt<br>es pro Event und Distanz? Welche Events<br>drohen auszubuchen?|Echtzeit-Dashboard|
|KI-E-Mail-Assistent|Eingehende E-Mails werden via NLP<br>analysiert. Bei erkannten Standardanfragen<br>(Wetsuit, Eventinfos, Finisher-Shirt-Größen)<br>erstellt die KI einen vollständigen Antwort-<br>Entwurf. Geschäftsführung gibt mit einem<br>Klick frei (Human-in-the-Loop).|NLP + LLM-API (Azure<br>OpenAI / Open AI GPT-4o)|
|Wetsuit-Verwaltung|Zentrales Inventar aller Leih-Wetsuits mit<br>Größen, Zustand und Verfügbarkeit. KI<br>gleicht Anfragenden mit Anmeldedaten|KI-Größenempfehlung +<br>Bestandsprüfung|



© 2026 Borek Solutions Group – Vertrauliches Dokument 

Seite 10 von 19 

**PROJEKTKONZEPT • EOWE KI-WORKSPACE** 

Vertraulich | 13 Juli 2026 

|**Funktion**|**Beschreibung**|**KI / Automatisierung**|
|---|---|---|
||(Alter, Größe, Gewicht) ab und schlägt<br>passende Größe automatisch vor.||
|Strecken- & Medien-<br>Ablage|Strukturierte Ablage aller technischen<br>Zeichnungen, Bojensetz-Pläne und<br>Streckenfotos, kategorisiert nach Event und<br>Jahr. Anbindung an bestehende SharePoint-<br>Ablage möglich.|– (KI-Simulation in Modul 6)|
|Schwimmcamps &<br>Fremd-Events|Separate Verwaltungsbereiche für<br>Schwimmcamps (Hotel- und<br>Trainingsplanung) und Fremd-Events.<br>Gleiche Datenstruktur, separate Instanz.|–|



#### **6.1.2 Zentrale User Stories** 

- "Als GF möchte ich eine neue Veranstaltung (z.B. Bodensee Open 2027) in unter 5 Minuten vollständig anlegen können, sodass alle relevanten Metadaten sofort im System verfügbar sind." 

- "Als GF erhalte ich täglich um 08:00 Uhr eine E-Mail-Zusammenfassung der neu eingegangenen Teilnehmeranmeldungen und offenen Anfragen – ohne manuellen Aufwand." 

- "Als GF bekomme ich für eine eingehende Wetsuit-Anfrage von Teilnehmer Herbert G. automatisch einen Antwort-Entwurf mit passender Größenempfehlung und Verfügbarkeitsstatus, den ich mit einem Klick versenden kann." 

- "Als GF kann ich jederzeit auf dem Dashboard sehen, wie viele Finisher-Shirts in welchen Größen pro Event benötigt werden – automatisch berechnet auf Basis der aktuellen Anmeldedaten." 

### **Modul 2: Vertrags- und Finanzwesen  |  Scope: Phase 1 (Interim-Go-Live 07. Sept. 2026)** 

##### **Kernziel dieses Moduls** 

Zentralisierung und Automatisierung aller kaufmännischen Prozesse. Das Herzstück ist das KIgestützte Zahlungsabgleich-System (Qonto-API), 

das manuellen Aufwand bei der Buchhaltung drastisch reduziert. Alle Dokumente sind revisionssicher im System archiviert. 

#### **6.2.1 Funktionsübersicht** 

|**Funktion**|**Beschreibung**|**KI / Automatisierung**|
|---|---|---|
|Digitale<br>Vertragsverwaltung|Automatisierte Generierung von<br>Teilnehmerverträgen auf Basis von<br>Templates (Haftungsausschluss,<br>Ausfallklauseln, Datenschutz). Versionierte,<br>rechtssichere Ablage pro Teilnehmer und<br>Event.|Automatische PDF-<br>Generierung|
|All-Event-Ticket &<br>Rabatt-Logik|Verwaltung von All-Event-Jahrestickets mit<br>komplexer Rabatt- und Anrechnungslogik.<br>Automatische Berechnung von Rabatten bei<br>Kombinationsbuchungen.|Regelbasierte Rabatt-Engine|
||Automatischer Versand von||
|Rechnungsstellung &<br>Mahnwesen|Zahlungsaufforderungen nach der<br>Anmeldung. Eskalationsstufen: Erinnerung,<br>Mahnung 1, Mahnung 2, Übergabe an GF|Automatisiertes Mahnwesen|



© 2026 Borek Solutions Group – Vertrauliches Dokument 

Seite 11 von 19 

**PROJEKTKONZEPT • EOWE KI-WORKSPACE** 

Vertraulich | 13 Juli 2026 

|**Funktion**|**Beschreibung**|**KI / Automatisierung**|
|---|---|---|
||zur Entscheidung.||
|Qonto-API:<br>Zahlungseingang-<br>Tracking|Alle Kontobewegungen auf dem EOWE-<br>Qonto-Konto werden via API in Echtzeit ins<br>System gespiegelt. Vollständige<br>Transparenz über eingehende Zahlungen.|Echtzeit-API-Sync|
|KI-Zahlungsabgleich|Machine-Learning-Algorithmus gleicht<br>Zahlungseingänge mit offenen<br>Teilnehmergebühren ab. Basis: Betrag,<br>Verwendungszweck, Name, IBAN.<br>Konfidenz-Score entscheidet über Auto-<br>Buchung oder manuelle Prüfung.|ML-Matching-Algorithmus<br>(Ziel: ≥85% Auto-Rate)|
|OCR:<br>Eingangsrechnungen|Hochgeladene Eingangsrechnungen<br>(Wasserwacht, Lieferanten) werden per<br>OCR ausgelesen und automatisch<br>vorkontiert. GF gibt mit einem Klick frei.|OCR + LLM-Extraktion|
|DATEV-Export|Monatliche Exportdateien im DATEV-<br>kompatiblen Format für den Steuerberater.<br>Enthält alle gebuchten Ein- und Ausgänge,<br>kategorisiert nach SKR-Kontenplan.|Automatischer Export-<br>Generator|
|Finanz-Dashboard|Echtzeit-Übersicht über: offene<br>Forderungen, Zahlungseingänge,<br>Liquiditätsstatus, Event-Profitabilität<br>(Einnahmen vs. geplante Ausgaben).|Echtzeit-Aggregation|



#### **6.2.2 Zentrale User Stories** 

- "Als GF möchte ich täglich eine Übersicht aller neuen Zahlungseingänge sehen, wobei jeder Eingang entweder bereits automatisch einem Teilnehmer zugeordnet wurde (grün) oder zur manuellen Prüfung markiert ist (gelb), sodass ich nie mehr Kontoauszüge manuell durchforsten muss." 

- "Als GF kann ich eine eingescannte Rechnung der Wasserwacht hochladen und erhalte innerhalb von Sekunden einen automatischen Buchungsvorschlag mit Kostenstelle und Zahlungsziel, den ich mit einem Klick bestätigen kann." 

- "Als Steuerberater erhalte ich am Ersten jedes Monats automatisch eine DATEV-kompatible Exportdatei per E-Mail." 

### **Modul 3: E-Commerce, Inventar & Administration  |  Scope: Phase 2 (Full-GoLive 02. Nov. 2026)** 

##### **Kernziel dieses Moduls** 

Verwaltung des gesamten physischen Warenbestands: Merchandising, Swim-Gear, EventMaterialien (Bojen, Restubes) und Fuhrpark. 

Das Highlight: Automatische Aggregation der benötigten Finisher-Shirt-Größen in Echtzeit auf Basis der aktuellen Teilnehmeranmeldungen. 

**Ergänzung Kundenfeedback EOWE (Phase-2-Priorität):** Innerhalb von Modul 3 hat die ShopFunktionalität (Online-Shop, Retouren) Vorrang, da sie für das Weihnachtsgeschäft benötigt wird. Die Funktionen Inventar-/Materialverwaltung und Fuhrpark-Management können bei Ressourcenengpässen zeitlich nach hinten gestellt werden. 

© 2026 Borek Solutions Group – Vertrauliches Dokument 

Seite 12 von 19 

**PROJEKTKONZEPT • EOWE KI-WORKSPACE** 

Vertraulich | 13 Juli 2026 

|**Funktion**|**Beschreibung**|**KI / Automatisierung**|
|---|---|---|
|Online-Shop (50–100<br>Artikel)|Vollständige Shop-Integration für<br>Merchandising (T-Shirts, Caps,<br>Badeanzüge) und Swim-Gear (Brillen,<br>Schwimmbojen) mit Produktverwaltung,<br>Preisen, Varianten, Fotos und<br>Lagerbestand.|Automatische<br>Lagerbestandsführung|
|Retourenmanagement|Verwaltung von Rücksendungen und<br>Umtausch. Lagerbestand wird automatisch<br>korrigiert, Erstattung wird in Modul 2<br>ausgelöst.|Automatische<br>Bestandskorrektur|
|Inventar- &<br>Materialverwaltung|Tracking aller Event-Materialien: Bojen,<br>Restubes, Zeitnahmechips, Plakate, Pokale.<br>Bestandswarnung bei Unterschreitung von<br>Mindestmengen.|Automatische<br>Mindestmengen-Alerts|
|Fuhrpark-<br>Management|Verwaltung des Fahrzeugpools<br>(Transporter, Geschäftsführerwagen) mit<br>Verfügbarkeitskalender, Wartungsintervallen<br>und Kostenerfassung pro Event.|–|



**Modul 4: Marketing, Fotos & Social Media  |  Scope: Phase 2 (Full-Go-Live 02. Nov. 2026)** 

##### **Kernziel dieses Moduls** 

Vollautomatische Klassifizierung und Archivierung von Event-Fotos durch Computer Vision – eine der zeitintensivsten manuellen Tätigkeiten der GF. 

Zusätzlich: Professionalisierung der Zusammenarbeit mit Agentur Grid Sports über ein strukturiertes Asset-Portal. 

|**Funktion**|**Beschreibung**|**KI / Automatisierung**|
|---|---|---|
|KI-Foto-Sortierung<br>(Computer Vision)|Fotografen laden Rohdaten über ein<br>Webportal hoch. Eine Computer-Vision-KI<br>klassifiziert jedes Bild automatisch in: "Vor<br>dem Start", "Start", "Streckenfotos", "Ziel",<br>"Siegerehrung", "Einzel-Athlet",<br>"Team/Gruppe". Bilder mit Konfidenz < 80%<br>werden zur manuellen Prüfung markiert.|Computer Vision (Google<br>Vision API / Custom Model) –<br>Ziel: ≥90% Trefferquote|
|Athleten-Erkennung|Startnummer-Erkennung mit Zuordnung<br>zum Teilnehmer in der Anmeldedatenbank –<br>Bilder direkt dem jeweiligen Teilnehmer<br>zugeordnet und individuell abrufbar.|OCR + Datenbank-Matching|
|Foto-Archiv &<br>Freigabe-Workflow|Zentrales, durchsuchbares Fotoarchiv. GF<br>kann Fotos freigeben oder sperren.<br>Metadaten (Event, Kategorie, Datum,<br>Fotograf) werden automatisch hinterlegt.|– (Freigabe durch GF)|
|Asset-Portal für Grid<br>Sports|Agentur Grid Sports erhält einen<br>geschützten Bereich mit freigegebenen<br>Assets (Fotos, Logos, Texte) für Instagram<br>und andere Kanäle. Content-Freigaben<br>digital – keine WhatsApp-Kommunikation<br>mehr.|Rollenbasiertes Zugriffsystem|
|Kampagnen- &|Planung und Budgetierung von|–|



© 2026 Borek Solutions Group – Vertrauliches Dokument 

Seite 13 von 19 

**PROJEKTKONZEPT • EOWE KI-WORKSPACE** 

Vertraulich | 13 Juli 2026 

|**Funktion**|**Beschreibung**|**KI / Automatisierung**|
|---|---|---|
||Marketingkampagnen (Plakate, Events,||
|Budgetplanung|Parties, Meet&Greets). Verknüpfung mit<br>Modul 2 für Ausgaben-Tracking.||



### **Modul 5: Partner-, Sponsoring- und Dienstleisterverwaltung (CRM)  |  Scope: Phase 2 (Full-Go-Live 02. Nov. 2026)** 

##### **Kernziel dieses Moduls** 

Spezialisiertes CRM für das EOWE-Stakeholder-Ökosystem: Sponsoren (monetär und Sachleistungen), Dienstleister (Wasserwacht, Catering, Logistik) und Medienpartner. Kernfunktion: Proaktives Fristenmanagement durch automatische Benachrichtigungen. 

|**Funktion**|**Beschreibung**|**KI / Automatisierung**|
|---|---|---|
|Sponsoren-CRM|Vollständige Erfassung aller Sponsoren-<br>Beziehungen: Vertragsdetails, Leistungen (Geld,<br>Sachleistungen wie Hotel-Nächte oder Getränke),<br>Ansprechpartner, Vertragslaufzeiten und<br>geleistete/ausstehende Zahlungen.|Automatisches<br>Fristentracking|
|Dienstleister-<br>Koordination|Planung und Budgetüberwachung für alle Event-<br>Dienstleister (Wasserwacht, Sanitätsdienst,<br>Catering, Zeitnahme). Einsatzzeiten und Kosten<br>pro Event dokumentiert.|Kostenüberwachung-<br>Dashboard|
|Alert-System|Automatische E-Mail-Benachrichtigungen: 90 Tage<br>vor Vertragsablauf (Verlängerungshinweis), 30<br>Tage nach Fälligkeit offener Zahlungen (Mahnung),<br>sofort bei verpassten Lieferterminen<br>(Sachleistungen).|Regelbasiertes Alert-<br>System|
|Leistungsnachweis<br>für Sponsoren|Automatisierte Erstellung von Sponsoren-Reports<br>(Reichweite, Foto-Erwähnungen, Event-Statistiken)<br>als Grundlage für Gespräche über<br>Vertragsverlängerungen.|Report-Generator|



### **Modul 6: Zukünftige Ausbaustufe & Abo-Modell  |  Optionale Erweiterung C** 

Modul 6 beschreibt den langfristigen Wachstumsplan der Plattform. Durch die von Beginn an modular angelegte Architektur können diese Funktionen ohne strukturelle Umbrüche integriert werden. Scope und Zeitplan werden nach dem Full-Go-Live (02. Nov. 2026) gemeinsam mit dem Auftraggeber definiert. 

- **Subscription-Management:** Wiederkehrende Zahlungsabwicklung für Abo-Modelle (JahresMitgliedschaft mit All-Event-Ticket plus digitale Inhalte), kompatibel mit Stripe oder ähnlichen Payment Providern. 

- **Digitale Leistungspakete:** Verkauf von Trainingsvideos, personalisierten Auswertungen und exklusivem Content über die Plattform. 

- **KI-gestützte Streckensimulation:** Auf Basis von Geodaten können neue Streckenvarianten am Computer simuliert und visualisiert werden, bevor physische Bojensetzungen getestet werden. 

- **Mandantenfähigkeit:** Optionale Erweiterung der Plattform, um sie anderen Open-WaterVeranstaltern als lizenzierbare SaaS-Lösung anzubieten. 

© 2026 Borek Solutions Group – Vertrauliches Dokument 

Seite 14 von 19 

**PROJEKTKONZEPT • EOWE KI-WORKSPACE** 

Vertraulich | 13 Juli 2026 

© 2026 Borek Solutions Group – Vertrauliches Dokument 

Seite 15 von 19 

**PROJEKTKONZEPT • EOWE KI-WORKSPACE** 

Vertraulich | 13 Juli 2026 

## **7. Technische Systemarchitektur** 

### **7.1 Überblick: Cloud-native Drei-Schichten-Architektur** 

Das EOWE Workspace System wird als cloud-native Anwendung mit einer klaren Drei-SchichtenArchitektur (Frontend – Backend – Datenbank) entwickelt. Die cloud-native Architektur garantiert Verfügbarkeit, Skalierbarkeit und Datensicherheit, ohne dass EOWE eigene Server betreiben muss. Alle Daten werden verschlüsselt übertragen und in einer EU-basierten Cloud-Infrastruktur gespeichert (DSGVO-konform). 

|**Schicht**|**Technologie**|**Einsatzzweck & Begründung**|
|---|---|---|
|Frontend (UI)|React.js (TypeScript)|Reaktionsschnelle, app-ähnliche Bedienung (Single<br>Page Application). De-facto-Standard für komplexe,<br>datengetriebene Web-UIs. TypeScript erhöht Code-<br>Qualität und verringert Laufzeit-Fehler erheblich.|
|Backend (API &<br>Logik)|Node.js (Express) +<br>Python (FastAPI)|Node.js für schnelle, nicht-blockierende API-Endpunkte<br>(Echtzeit-Dashboards). Python für alle KI/ML-<br>intensiven Aufgaben (Zahlungsabgleich, NLP,<br>Computer Vision) – Python ist das führende<br>Ökosystem für Machine Learning.|
|Datenbank|PostgreSQL (Cloud<br>Hosted – AWS RDS /<br>Supabase)|Robuste, relationale Datenbank für komplexe<br>Beziehungen (Teilnehmer ↔ Events ↔ Zahlungen ↔<br>Verträge). Cloud-Hosting sichert Backup, Skalierung<br>und Hochverfügbarkeit.|
|KI &<br>Automatisierung|Azure OpenAI / OpenAI<br>API (GPT-4o) + Google<br>Vision API|LLM für E-Mail-Verständnis und -Generierung,<br>Dokument-OCR und Zahlungsabgleich. Computer<br>Vision für automatische Foto-Klassifizierung (Modul 4).|
|Authentifizierung|OAuth 2.0 + JWT|Sicheres, standardisiertes Anmeldesystem. Unterstützt<br>"Login mit Google/Microsoft" für einfachen Zugang<br>ohne Passwort-Management.|
|Schnittstellen<br>(APIs)|REST (extern) +<br>GraphQL (intern)|REST für Anbindung externer Systeme (Tiger Timing,<br>RaceResult, Qonto, DATEV). GraphQL intern für<br>flexible, effiziente Datenabfragen im Frontend.|
|Hosting &<br>Infrastruktur|AWS / Azure (EU-<br>Region) + Docker|Container-basierte Infrastruktur ermöglicht einfache<br>Deployments und Skalierung. DSGVO-konformes EU-<br>Hosting.|
|CI/CD & Code-<br>Qualität|GitHub Actions + Jest +<br>ESLint|Vollautomatisierte Test- und Deployment-Pipeline:<br>Jede Code-Änderung wird automatisch getestet, bevor<br>sie live geht (Zero-Downtime-Deployments).|



### **7.2 Externe System-Integrationen** 

|**Externes**<br>**System**|**Integration**|**Richtung**|**Status**|
|---|---|---|---|
|Tiger Timing|REST API (Meldewesen,<br>Teilnehmerdaten)|Bidirektional|API-Vertrag zu klären (Phase<br>0)|
|RaceResult|REST API (Ergebnislisten,<br>Ranglisten)|Import (→<br>EOWE)|API-Dokumentation<br>vorhanden|
|Qonto (Banking)|Official Qonto API v2 (Echtzeit-<br>Transaktionen)|Import (→<br>EOWE)|OAuth 2.0 – bereit|



© 2026 Borek Solutions Group – Vertrauliches Dokument 

Seite 16 von 19 

**PROJEKTKONZEPT • EOWE KI-WORKSPACE** 

Vertraulich | 13 Juli 2026 

|**Externes**<br>**System**|**Integration**|**Richtung**|**Status**|
|---|---|---|---|
|DATEV|DATEV-Export-Format<br>(CSV/Lodas)|Export (EOWE<br>→)|Standard-Schnittstelle|
|Azure OpenAI /<br>OpenAI / LLM|Azure OpenAI / OpenAI API<br>(GPT-4o) für E-Mail-KI & OCR|API-Call (→<br>KI)|API-Key erforderlich|
|Google Vision<br>API|Computer Vision für Foto-<br>Klassifizierung (Modul 4)|API-Call (→<br>KI)|Phase 2, Sprint 5|
|Grid Sports<br>(Agentur)|Rollenbasierter Portal-Zugang|Direktzugang<br>im System|Phase 2, Sprint 7|
|E-Mail-System|SMTP / SendGrid für<br>automatisierte E-Mails|Export (EOWE<br>→ TN)|Standard-Integration|



### **7.3 Datensicherheit und DSGVO** 

Der Schutz personenbezogener Daten der Teilnehmer hat höchste Priorität. Das System wird von Beginn an nach dem Privacy-by-Design-Prinzip DSGVO-konform entwickelt. 

- Alle Daten werden ausschließlich auf EU-basierten Servern gespeichert (AWS Frankfurt / Azure Amsterdam). 

- Übertragung aller Daten ausschließlich verschlüsselt (TLS 1.3). 

- Personenbezogene Daten (Name, E-Mail, IBAN) werden verschlüsselt in der Datenbank gespeichert (at-rest encryption). 

- Rollenbasiertes Zugriffskonzept: Jeder Nutzer sieht nur die Daten, die für seine Rolle freigegeben sind. 

- Vollständiges Audit-Log: Jede Datenänderung wird protokolliert (Wer hat was wann geändert?). 

© 2026 Borek Solutions Group – Vertrauliches Dokument 

Seite 17 von 19 

**PROJEKTKONZEPT • EOWE KI-WORKSPACE** 

Vertraulich | 13 Juli 2026 

## **8. Ressourcen- und Teamplanung** 

### **8.1 Personalbedarf (Borek Solutions Group)** 

Für die erfolgreiche Umsetzung des Projekts sind folgende Rollen und Kapazitäten vorgesehen. In Phase 2 arbeiten die beiden KI-Builder weitgehend parallel an unterschiedlichen Modulen, um M3, M4 und M5 innerhalb von 8 Wochen fertigzustellen. 

|**Rolle**|**Einsatzbereich**|**Kapazität**|
|---|---|---|
|Project Lead|Projektsteuerung, Backlog-Management,<br>Stakeholder-Kommunikation, Sprint Reviews|20%|
|KI-Builder A|Phase 1: M1+M2 (Frontend React.js, Backend<br>Node.js, KI-Integrationen) | Phase 2: M4 (Computer<br>Vision, Foto-Portal) + M3 (Shop, POS)|100% (Vollzeit,<br>Monate 1–4)|
|KI-Builder B|Phase 1: M1+M2 (Backend Python/FastAPI,<br>Zahlungsabgleich, API-Anbindungen) | Phase 2: M5<br>(Sponsoring-CRM) + M3 (Inventar, Fuhrpark)|100% (Vollzeit,<br>Monate 1–4)|
|UI/UX Designer|Benutzeroberflächen-Design, Dashboard-<br>Konzeption, Usability (alle Module)|~20 Std. gesamt<br>(Phase 0–2,<br>Freelancer)|



© 2026 Borek Solutions Group – Vertrauliches Dokument 

Seite 18 von 19 

**PROJEKTKONZEPT • EOWE KI-WORKSPACE** 

Vertraulich | 13 Juli 2026 

## **9. Qualitätssicherung und Testing-Strategie** 

Qualität wird in diesem Projekt nicht als nachgelagerte Phase verstanden, sondern als integraler Bestandteil jedes Sprints. Die Testing-Pyramide definiert unsere Strategie: Viele automatisierte UnitTests an der Basis, ergänzt durch Integrations- und End-to-End-Tests sowie manuelle UAT (User Acceptance Testing) an der Spitze. Sprint 8 widmet sich der Gesamtintegration und dem abschließenden UAT über alle 5 Module. 

|**Test-Typ**|**Abdeckung**|**Tool**|**Wann / Verantwortlich**|
|---|---|---|---|
|Unit Tests|Einzelne Funktionen und<br>Komponenten (Ziel: ≥<br>80% Code-Coverage)|Jest (JavaScript) /<br>pytest (Python)|Kontinuierlich – jeder<br>Entwickler schreibt Tests zu<br>seinem Code|
|Integration<br>Tests|API-Endpunkte,<br>Datenbankoperationen,<br>externe Schnittstellen<br>(Tiger Timing, Qonto,<br>Google Vision)|Supertest / pytest|Jeder Sprint – CI/CD-<br>Pipeline blockiert bei Fehler|
|End-to-End<br>Tests|Kritische Nutzerpfade<br>(Anmeldung →<br>Zahlungsabgleich →<br>Bestätigung, Foto-Upload<br>→ KI-Klassifizierung)|Playwright|Vor jedem Sprint-Release|
|User<br>Acceptance<br>Testing|GF testet alle neuen<br>Features in der Staging-<br>Umgebung vor Go-Live|Manuell (Staging-<br>System)|Ende jedes Sprints mit<br>neuem Feature;<br>vollständiges UAT in Sprint 4<br>(M1/M2) und Sprint 8 (M1–<br>M5)|



- **Definition of Done (DoD) – Wann ist ein Feature "fertig"?** ✔  Code ist implementiert, reviewed (4-Augen-Prinzip) und in den main-Branch gemerged ✔  Unit Tests und Integration Tests für neue Logik sind geschrieben und grün ✔  Feature wurde in der Staging-Umgebung ohne Fehler demonstriert ✔  Akzeptanzkriterien der User Story sind vollständig erfüllt (per GF/PO bestätigt) ✔  Keine kritischen oder hohen offenen Bugs ✔  Technische Dokumentation (API-Endpunkte, Datenbankänderungen) ist aktualisiert 

© 2026 Borek Solutions Group – Vertrauliches Dokument 

Seite 19 von 19 

