# Omschrijving
De eindopdracht is geinspireerd op de simulator gemaakt door Huib. De structuur aangehouden in zijn simulators worden ook aangehouden in mijn eindopdracht.

Het regelsysteem is een adaptive cruise controlsysteem voor een auto. Met twee sensoren wordt de snelheid en de afstand tot de auto voor bepaald. Door het regelen van het gas en de remmen kan de auto worden bestuurd.

# Klaarmaken van de installatie
1. Clone de repo
2. Open het project in VS Code
3. Creëer een venv met python 3.7 en run pip install -r requirements.txt
4. Install g++ compiler: https://code.visualstudio.com/docs/cpp/config-mingw
5. Als de c++ files nog niet zijn gebuild run dan python setup.py build_ext --inplace

# Starten en runnen van simulator
Om de simulator te starten kan je de file main.py runnen. De simulator gaat naar een volgende stap door op een toets te drukken. De distance tot de voorganger veranderd random en zal eerder veranderen naarmate de snelheid van de auto hoger is. De distance zal ook afnemen als de auto aan het remmen is. 

De afstand die de auto probeert aan te houden en de snelheid kan worden ingesteld in de Constants.py file. In deze file kunnen ook allerlei andere dingen rondom de simulatie of de Controller worden aangepast.

Ook worden de I2C writing en read operations en de get_distance_cm van de Lidar sensor executions gelogt in log.txt. Dit wordt gedaan via een wrapper.

# Tests
De tests kunnen worden uitgevoerd door het runnen van de files in de tests folder. Voor de tests wordt het unittest framework gebruikt.

## Unittests
De unittest die wordt uitgevoerd testen de diff_distance function in de Controller klasse. Het doel van de tests is te controleren of de functie de in het testplan beschreven gedrag vertoond. 
1. Positief getal ALS gegeven dist groter is dan de desired. 
2. Negatief getal ALS gegegven dist kleiner is dan de desired.
3. -10 teruggeven ALS gegeven dist negatief is.

Na het uitvoeren van de test kunnen we concluderen dat deze functie voldoet aan de eisen.

## Integratietest
In de integratietest testen we de integratie tussen de Lidar sensor en de brake actuator. We willen de de brake actuator aan gaat als de lidar sensor een afstand meet minder dan 200 cm.

Na het uitvoeren van de test kunnen we concluderen dat deze functie voldoet aan de eisen.

## Systemtest
In de systeemtest testen we de volledige controller. Deze valt het best te testen door de simulator daadwerkelijk te runnen, en omdat dit deels random gaat is hier automatisch tests voor schrijven best lastig. In de unittest testen we of de auto in het begin alleen gas geeft en NIET remt. Dit moet na de 1ste stap de juiste actie zijn omdat de snelheid 0 is en de afstand tot de voorganger is nog groot genoeg.

Bij het runnen van de simulatie zien we ook dat die het juiste gedrag vertoond, dus ook deze test mogen we als geslaagd zien.





