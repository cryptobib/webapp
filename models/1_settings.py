# -*- coding: utf-8 -*-

## Title, ...

response.title = "CryptoBib"
response.navbar_title = "CryptoBib"
response.logo = A("CryptoBib", _class = "navbar-brand", _href = URL('default', 'index'))

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Michel Abdalla and Fabrice Benhamouda'
response.meta.description = 'BibTeX database containing papers related to Cryptography'
response.meta.keywords = 'BibTeX, cryptography'
response.meta.generator = 'Web2py Web Framework'

## Menu

from gluon import current

def auto_active_menu_item(title, url):
    """ return a menu item (element of a list given to MENU) with the active bool set to true if and only if we are visiting the corresponding page """
    return (title, current.request.env.path_info.startswith(url), url)

response.menu = [
    auto_active_menu_item(T('Manual'), URL('default', 'manual')),
    auto_active_menu_item(T('Custom'), URL('default', 'custom')),
    (T('Crypto Team'), False, "https://crypto.di.ens.fr"),
    auto_active_menu_item(T('About'), URL('default', 'about'))
]
