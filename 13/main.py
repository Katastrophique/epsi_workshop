#!/usr/bin/env python3
"""
login_wigor.py
Script Selenium pour se connecter à :
https://ws-edt-cd.wigorservices.net/WebPsDyn.aspx?Action=posEDTLMS

Usage:
    python login_wigor.py
"""

import sys
import time
from getpass import getpass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# webdriver-manager pour récupérer automatiquement chromedriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options


TARGET_URL = "https://ws-edt-cd.wigorservices.net/WebPsDyn.aspx?Action=posEDTLMS"

def create_driver(headless=False):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")  # mode headless
        chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # optionnel : désactiver notifications
    chrome_options.add_argument("--disable-notifications")
    # Lance le driver (webdriver-manager télécharge et gère chromedriver)
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login(driver, username, password, timeout=15):
    driver.get(TARGET_URL)
    wait = WebDriverWait(driver, timeout)

    # attendre que le champ username soit présent
    try:
        username_el = wait.until(EC.presence_of_element_located((By.ID, "username")))
    except TimeoutException:
        raise RuntimeError("Le champ 'username' n'a pas été trouvé sur la page dans le délai imparti.")

    # récupérer aussi le champ password (peut être de type text d'après votre extrait)
    try:
        password_el = driver.find_element(By.ID, "password")
    except NoSuchElementException:
        # essayer par name
        try:
            password_el = driver.find_element(By.NAME, "password")
        except NoSuchElementException:
            raise RuntimeError("Le champ 'password' n'a pas été trouvé sur la page.")

    # remplir
    username_el.clear()
    username_el.send_keys(username)
    password_el.clear()
    password_el.send_keys(password)

    # tentative de soumission :
    # 1) appuyer sur Entrée dans le champ password
    password_el.send_keys(Keys.ENTER)

    # 2) si le site utilise un bouton, on peut essayer de cliquer dessus si présent
    #    (recherche d'un bouton de type submit)
    try:
        btn = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' or contains(@class,'login') or contains(@id,'login')]"))
        )
        try:
            btn.click()
        except Exception:
            pass
    except TimeoutException:
        # pas grave, l'envoi par ENTER suffit souvent
        pass

    # Attendre soit un changement d'URL soit la présence d'un élément indiquant que l'on est connecté.
    # Ici nous attendons que l'URL change (si le site redirige après connexion).
    try:
        current_url = driver.current_url
        wait.until(EC.url_changes(current_url))
        return True
    except TimeoutException:
        # si l'URL n'a pas changé, on peut vérifier l'apparition d'un élément suggérant l'authentification (à adapter)
        # Ex : présence d'un bouton "Déconnexion" ou d'un élément avec id 'logout' ou 'menu-user'
        possible_selectors = [
            (By.ID, "logout"),
            (By.XPATH, "//*[contains(text(),'Déconnexion') or contains(text(),'Logout') or contains(text(),'Se déconnecter')]"),
            (By.CSS_SELECTOR, ".user-menu, .logged-in, #menu-user"),
        ]
        for sel in possible_selectors:
            try:
                WebDriverWait(driver, 2).until(EC.presence_of_element_located(sel))
                return True
            except TimeoutException:
                continue
        # échec de détection d'une connexion fiable
        return False

def main():
    print("Connexion automatique vers :", TARGET_URL)
    username = input("Nom d'utilisateur : ").strip()
    if not username:
        print("Nom d'utilisateur vide, exit.")
        sys.exit(1)
    password = getpass("Mot de passe (entrée masquée) : ")

    # Choix : headless? (utile si vous voulez voir le navigateur)
    headless_answer = input("Mode headless ? (y/N) : ").strip().lower()
    headless = headless_answer == "y"

    try:
        driver = create_driver(headless=headless)
    except WebDriverException as e:
        print("Erreur lors du démarrage du navigateur :", e)
        sys.exit(1)

    try:
        ok = login(driver, username, password)
        if ok:
            print("Connexion : succès (détection d'un changement d'état après authentification).")
            print("URL actuelle :", driver.current_url)
        else:
            print("Connexion : impossible de confirmer le succès. Vérifiez manuellement la page ouverte.")
            print("URL actuelle :", driver.current_url)
        # garder le navigateur ouvert un peu en mode non-headless pour inspection, sinon on ferme
        if headless:
            # attendre brièvement pour que tout se stabilise (optionnel)
            time.sleep(2)
            driver.quit()
        else:
            print("Le navigateur est laissé ouvert pour inspection. Fermez-le manuellement quand vous avez fini.")
    except Exception as e:
        print("Erreur pendant la tentative de connexion :", repr(e))
        try:
            driver.quit()
        except Exception:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()