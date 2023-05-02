from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import keyboard
import time
import sys
import random


LINK = "https://bgdo.typewriter.at/index.php?r=site/index"

# initialize browser options
options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--log-level=3")


# get input from user
letters_per_10_minuts = int(
    input("Gewünschte *Anschläge in 10 Minuten* eingeben:  "))


# ansatzweise die aufteilung der fehler berechnen
mistakes = int(input(
    "Gewünschte Anzahl von automatisch generierten Fehlern eingeben (kann je nach Lektion um 1 abweichen):  "))
if mistakes != 0:
    mistake_sequence = int(500/mistakes)
    mistake_counter = random.randint(0, mistake_sequence)
else:
    mistake_counter = 0


letter_delay = 1/(letters_per_10_minuts/600)

characters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y",
              "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]


# initialize, open browser and wait for user to select exercise
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
driver.get(LINK)
print("Anmelden und Lektion auswählen...")
start_button = WebDriverWait(driver, 3600).until(EC.presence_of_element_located((By.CLASS_NAME, "ui-dialog.ui-corner-all.ui-widget.ui-widget-content.ui-front.ui-dialog-buttons.ui-resizable")))
print("Lektion ausgewählt!")
print("Warten bis Lektion agbeschlossen wird (bitte aktuelles Fenster ausgewählt lassen)...")
next_letter = driver.find_element(By.ID, "text_todo").find_element(By.TAG_NAME, "span")


# start exercise
start_button.click()

while True:
    try:

        # nächster buchstabe definieren
        output_text = next_letter.text

        # alle fehler mit random intervallen über die lektion verteilt abarbeiten
        if mistakes != 0:
            if mistake_counter == 0:
                random_character = random.choice(characters)
                while random_character == output_text:
                    random_character = random.choice(characters)
                keyboard.write(random_character)
                mistake_counter = random.randint(0, mistake_sequence)
                mistakes -= 1

            else:
                mistake_counter -= 1

        # buchstabe schreiben und den berechneten delay warten
        keyboard.write(output_text)
        time.sleep(letter_delay)

    except:
        print("Lektion abgeschlossen!")
        input("Enter to exit...")
        driver.quit()
        sys.exit()
