def post_button():

    return """
        let btn = document.querySelector('button.share-actions__primary-action') ||
                  document.querySelector('.share-box_actions button') ||
                  Array.from(document.querySelectorAll('button')).find(b => b.innerText.toLowerCase().includes('Publier'));

        if (btn) {
            btn.removeAttribute('disabled');
            btn.classList.remove('artdeco-button--disabled');
            btn.click();
            return "BOUTON_CLIQUE";
        }
        return "INTROUVABLE";
    """
