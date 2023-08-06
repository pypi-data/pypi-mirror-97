from wrap_py import settings as st
import gettext
import os
import wrap_engine

#global translation function
_translate_func = None

def set_lang(lang=""):
    global _translate_func
    os.environ['LANG'] = lang
    _tr = gettext.translation(domain=st.TRANSL_DOMAIN, localedir=st.TRANSLATIONS_FOLDER, fallback=True)
    _translate_func = _tr.gettext

    wrap_engine.transl.set_lang(lang)

def translator(text):
    return _translate_func(text)

set_lang()
wrap_engine.transl.set_translation_directory(st.TRANSLATIONS_FOLDER)
