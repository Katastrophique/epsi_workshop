#!/usr/bin/env python3
"""
login_wigor.py - Version avec debug amélioré
Script Selenium pour se connecter à Wigor
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
    StaleElementReferenceException
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options


TARGET_URL = "https://ws-edt-cd.wigorservices.net/WebPsDyn.aspx?Action=posEDTLMS"

def create_driver(headless=False):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-notifications")
    # Réduire les logs Chrome
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login(driver, username, password, timeout=20):
    """Tente de se connecter et détecte le succès"""
    driver.get(TARGET_URL)
    print(f"[DEBUG] Page chargée : {driver.current_url}")
    wait = WebDriverWait(driver, timeout)

    def retry_action(action, retries=3, delay=0.5):
        last_exc = None
        for i in range(retries):
            try:
                return action()
            except StaleElementReferenceException as e:
                last_exc = e
                time.sleep(delay)
        if last_exc:
            raise last_exc

    # Attendre le champ username
    try:
        username_el = wait.until(EC.presence_of_element_located((By.ID, "username")))
        print("[DEBUG] Champ 'username' trouvé")
    except TimeoutException:
        raise RuntimeError("Le champ 'username' n'a pas été trouvé")

    # Trouver le champ password
    try:
        password_el = driver.find_element(By.ID, "password")
        print("[DEBUG] Champ 'password' trouvé")
    except NoSuchElementException:
        try:
            password_el = driver.find_element(By.NAME, "password")
            print("[DEBUG] Champ 'password' trouvé par name")
        except NoSuchElementException:
            raise RuntimeError("Le champ 'password' n'a pas été trouvé")

    # Remplir les champs avec meilleure gestion des erreurs
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            # Re-trouver les éléments à chaque tentative
            username_el = driver.find_element(By.ID, "username")
            password_el = driver.find_element(By.ID, "password")
            
            username_el.clear()
            time.sleep(0.3)
            username_el.send_keys(username)
            time.sleep(0.3)
            
            password_el.clear()
            time.sleep(0.3)
            password_el.send_keys(password)
            time.sleep(0.3)
            
            print(f"[DEBUG] Identifiants remplis (tentative {attempt + 1})")
            break
            
        except StaleElementReferenceException:
            if attempt < max_attempts - 1:
                print(f"[DEBUG] Élément périmé, nouvelle tentative ({attempt + 2}/{max_attempts})...")
                time.sleep(1)
            else:
                raise RuntimeError("Impossible de remplir le formulaire après plusieurs tentatives")

    # Soumettre le formulaire
    initial_url = driver.current_url
    print(f"[DEBUG] URL avant soumission : {initial_url}")
    
    # Re-trouver le champ password juste avant de soumettre
    try:
        password_el = driver.find_element(By.ID, "password")
        password_el.send_keys(Keys.ENTER)
        print("[DEBUG] Formulaire soumis (ENTER)")
    except StaleElementReferenceException:
        print("[DEBUG] Élément périmé lors de la soumission, tentative via JavaScript...")
        # Fallback: soumettre via JavaScript
        driver.execute_script("document.querySelector('form').submit();")
        print("[DEBUG] Formulaire soumis (JavaScript)")
    
    # Tentative de clic sur bouton submit
    try:
        btn = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//button[@type='submit'] | //input[@type='submit'] | //*[contains(@class,'btn-login')]"))
        )
        btn.click()
        print("[DEBUG] Bouton submit cliqué")
    except TimeoutException:
        print("[DEBUG] Pas de bouton submit trouvé")

    # Attendre que la page charge (après soumission)
    time.sleep(2)
    
    print(f"[DEBUG] URL après soumission : {driver.current_url}")
    
    # Vérifier le titre de la page
    print(f"[DEBUG] Titre de la page : {driver.title}")
    
    # Chercher des messages d'erreur
    error_keywords = ['error', 'erreur', 'invalid', 'incorrect', 'échec', 'failed']
    page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    for keyword in error_keywords:
        if keyword in page_text:
            print(f"[WARNING] Possible erreur détectée : mot-clé '{keyword}' trouvé dans la page")
    
    # Stratégie 1 : Changement d'URL
    if driver.current_url != initial_url:
        print("[DEBUG] ✓ URL a changé (connexion probable)")
        return True
    
    # Stratégie 2 : Recherche d'éléments "connecté"
    print("[DEBUG] Recherche d'éléments indiquant une connexion réussie...")
    
    success_selectors = [
        (By.ID, "logout"),
        (By.ID, "deconnexion"),
        (By.CLASS_NAME, "user-menu"),
        (By.CLASS_NAME, "logged-in"),
        (By.XPATH, "//*[contains(text(),'Déconnexion')]"),
        (By.XPATH, "//*[contains(text(),'Logout')]"),
        (By.XPATH, "//*[contains(@class, 'emploi-du-temps')]"),
        (By.XPATH, "//*[contains(@class, 'calendar')]"),
        (By.XPATH, "//*[contains(@class, 'schedule')]"),
    ]
    
    for sel_type, sel_value in success_selectors:
        try:
            element = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((sel_type, sel_value))
            )
            print(f"[DEBUG] ✓ Élément trouvé : {sel_type}={sel_value}")
            return True
        except TimeoutException:
            continue
    
    # Stratégie 3 : Vérifier si le formulaire de login a disparu
    try:
        driver.find_element(By.ID, "username")
        print("[DEBUG] ✗ Le formulaire de login est toujours présent")
        return False
    except NoSuchElementException:
        print("[DEBUG] ✓ Le formulaire de login a disparu (connexion probable)")
        return True

def main():
    print("=" * 60)
    print("Connexion automatique Wigor - Version Debug")
    print("=" * 60)
    print(f"URL cible : {TARGET_URL}\n")
    
    username = input("Nom d'utilisateur : ").strip()
    if not username:
        print("Nom d'utilisateur vide, exit.")
        sys.exit(1)
    
    password = getpass("Mot de passe : ")
    
    headless_answer = input("Mode headless ? (y/N) : ").strip().lower()
    headless = headless_answer == "y"

    try:
        print("\n[INFO] Démarrage du navigateur...")
        driver = create_driver(headless=headless)
    except WebDriverException as e:
        print(f"[ERROR] Impossible de démarrer le navigateur : {e}")
        sys.exit(1)

    try:
        ok = login(driver, username, password)
        print("\n" + "=" * 60)
        if ok:
            print("✓ CONNEXION RÉUSSIE")
            print(f"URL actuelle : {driver.current_url}")
            
            # Attendre que la page se charge complètement
            print("\n[INFO] Attente du chargement complet de la page...")
            time.sleep(3)
            
            # Prendre une capture d'écran
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"wigor_screenshot_{timestamp}.png"
            driver.save_screenshot(screenshot_name)
            print(f"[INFO] ✓ Capture d'écran sauvegardée : {screenshot_name}")
            
        else:
            print("✗ CONNEXION INCERTAINE")
            print(f"URL actuelle : {driver.current_url}")
            print("\nVérifiez manuellement la page ouverte.")
            print("Si vous êtes connecté, adaptez la détection dans le script.")
        print("=" * 60)
        
        if headless:
            time.sleep(1)
            driver.quit()
        else:
            print("\n[INFO] Navigateur laissé ouvert pour inspection.")
            print("[INFO] Appuyez sur Entrée pour fermer...")
            input()
            driver.quit()
            
    except Exception as e:
        print(f"\n[ERROR] Erreur pendant la connexion : {repr(e)}")
        try:
            driver.quit()
        except Exception:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()