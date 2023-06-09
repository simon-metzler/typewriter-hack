from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import keyboard
import time
import sys
import random


def main():

    LINK = "https://bgdo.typewriter.at/index.php?r=site/index"

    # initialize browser options
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("--log-level=3")


    # get input from user
    print("[T Y P E W R I T E R   H A C K]")
    letters_per_10_minuts = int(input("Gewünschte 'Anschläge in 10 Minuten' eingeben (2000-3000 sind menschlich):  "))

    #calculating letters per second
    letter_delay = 1/(letters_per_10_minuts/600)

    # getting the number of mistakes
    mistakes = int(input("Gewünschte Anzahl von automatisch generierten Fehlern eingeben (kann je nach Lektion um 1 abweichen):  "))

    #roughly calculate the distribution of the mistakes
    if mistakes != 0:
        mistake_sequence = int(500/mistakes)
        mistake_counter = random.randint(0, mistake_sequence)

    # creating a list of all possible characters to generate mistakes
    characters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                  "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]


    # initialize and open browser
    print("Browser startet...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(LINK)
    print("Browser erfolgreich gestartet!")

    # wait for user to select exercise, waiting 1 hour to find start button element with xpath "/html/body/div[6]/div[3]/div/button", if found find next letter with xpath
    print("Anmelden und Lektion im Browser auswählen (Programm erkennt ausgewählte Lektion automatisch und löst diese dann sofort)...")
    start_button = WebDriverWait(driver, 3600).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/div[3]/div/button")))
    next_letter = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[3]/div[2]/div[2]/span[1]")

    print("Lektion erkannt!")
    print("Warten bis Lektion agbeschlossen wird (bitte aktuelles Fenster ausgewählt lassen)...")

    #short delay to wait for the page to load, if not loaded yet
    time.sleep(1)
    # start exercise by clicking the start button
    start_button.click()


    while True:
        try:

            # define next letter
            output_text = next_letter.text

            # if mistakes not 0, and mistake counter counted down (random delay, so all mistakes aren't done side by side) then do following:
            if mistakes != 0:
                if mistake_counter == 0:
                    # generate a random letter
                    random_character = random.choice(characters)
                    while random_character == output_text:
                        random_character = random.choice(characters)
                    # write it to the keyboard, before right letter is written
                    keyboard.write(random_character)
                    mistake_counter = random.randint(0, mistake_sequence)
                    mistakes -= 1

                else:
                    mistake_counter -= 1

            # write letter and wait calculated delay
            keyboard.write(output_text)
            time.sleep(letter_delay)

        except:
            # if done, it cant find the html elements and it will fail to read the next letter
            print("Lektion abgeschlossen!")
            input("Enter to exit...")
            driver.quit()
            sys.exit()



#calling the main function
if __name__ == "__main__":
    main()