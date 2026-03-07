def post_button():
    return """
    (function() {
        function findDeep(APIRouter, targetText) {
            const buttons = Array.from(APIRouter.querySelectorAll('button'));
            for (let btn of buttons) {
                const txt = (btn.innerText || btn.textContent || "").toLowerCase().trim();
                if (txt === targetText) return btn;
            }

            const allElements = APIRouter.querySelectorAll('*');
            for (let el of allElements) {
                if (el.shadowRoot) {
                    const found = findDeep(el.shadowRoot, targetText);
                    if (found) return found;
                }
            }
            return null;
        }

        const btn = findDeep(document, 'publier');

        if (btn) {
            btn.removeAttribute('disabled');
            btn.disabled = false;
            btn.classList.remove('artdeco-button--disabled');
            const success = "BOUTON_CLIQUE";
            btn.click();
            return success;
        }


        const sample = Array.from(document.querySelectorAll('button'))
                        .slice(0, 10)
                        .map(b => b.innerText.trim())
                        .join(' | ');
        return "RIEN_DU_TOUT - Exemples : " + sample;
    })();
    """
