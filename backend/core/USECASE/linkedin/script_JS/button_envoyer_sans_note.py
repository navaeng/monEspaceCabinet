from datetime import time


def button_envoyer_sans_note(driver):

    try:
        time.sleep(5)
        script_find_button_envoyer_sans_note = """
                                                function findButton() {
                                                    // 1. Check standard
                                                    let btn = document.querySelector('button[aria-label="Envoyer sans note"]');
                                                    if (btn) return btn;
    
                                                    // 2. Check dans le Shadow DOM (interop-outlet)
                                                    let host = document.querySelector('#interop-outlet');
                                                    if (host && host.shadowRoot) {
                                                        return host.shadowRoot.querySelector('button[aria-label="Envoyer sans note"]');
                                                    }
    
                                                    // 3. Check par texte si aria-label a sauté
                                                    return Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('sans note'));
                                                }
    
                                                let target = findButton();
                                                if (target) {
                                                    target.click();
                                                    return true;
                                                }
                                                return false;
                                                """

        success = driver.execute_script(script_find_button_envoyer_sans_note)
        if success:
            yield "✅ Invitation envoyée !"
        else:
            yield " Bouton introuvable même en recherche profonde."

        yield " Invitation envoyée avec succès !"
    except Exception as e:
        error_type = type(e).__name__
        yield f"Erreur précise [{error_type}] : {str(e)[:100]}"