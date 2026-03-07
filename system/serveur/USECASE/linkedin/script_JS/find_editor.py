def find_editor():
    js_find_editor = """
                                            function findDeep(sel, APIRouter = dossier) {
                                                let n = APIRouter.querySelector(sel);
                                                if (n) return n;
                                                let all = APIRouter.querySelectorAll('*');
                                                for (let e of all) {
                                                    if (e.shadowRoot) {
                                                        let res = findDeep(sel, e.shadowRoot);
                                                        if (res) return res;
                                                    }
                                                }
                                                return null;
                                            }
                                            return findDeep("div[contenteditable='true'], div[role='textbox'], .ql-editor");
                                            """

    return js_find_editor