# -*- coding: utf-8 -*-

import os
import re
import io

from lib.mybibtex.database import EntryKey, EntryKeyParsingError
from lib.mybibtex import generator

from lib.web2py_ctrl_default import *

import module_db.config
import lib.header

generator.config = module_db.config

@cache.action(cache_model=cache.ram)
def index():
    confs = db(db.conf.type=="conf").select(db.conf.ALL, orderby=db.conf.name)
    journals = db(db.conf.type=="journal").select(db.conf.ALL, orderby=db.conf.name)
    misc = db(db.conf.type=="misc").select(db.conf.ALL, orderby=db.conf.name)
    changes = db().select(db.change.ALL, orderby=~db.change.date)

    return dict(confs=confs, journals=journals, misc=misc, changes=changes)

@cache.action(cache_model=cache.ram)
def manual():
    def get_list_keys(conf_type):
        d = db(db.conf.type==conf_type).select(db.conf.key, db.conf.name, orderby=db.conf.name)
        return [(c["name"],c["key"]) for c in d]

    confs = get_list_keys("conf")
    journals = get_list_keys("journal")
    misc = get_list_keys("misc")

    return dict(confs=confs, journals=journals, misc=misc)

@cache.action(cache_model=cache.ram)
def about():
    return dict()

def custom():
    confs = db(db.conf.type=="conf").select(db.conf.key, db.conf.name, db.conf.start_year, db.conf.end_year, orderby=db.conf.name)
    journals = db(db.conf.type=="journal").select(db.conf.key, db.conf.name, db.conf.start_year, db.conf.end_year, orderby=db.conf.name)

    download_file = None
    errors = {}
    years = {}
    nb = 0

    if request.vars.download != None or request.vars.check != None:
        (errors_confs, years_confs, nb_confs) = get_years(confs, request.vars)
        (errors_journals, years_journals, nb_journals) = get_years(journals, request.vars)
        errors = dict(list(errors_confs.items()) + list(errors_journals.items()))
        years = dict(list(years_confs.items()) + list(years_journals.items()))
        nb = nb_confs + nb_journals

        if len(errors) > 0:
            errors[""] = "Year ranges for conferences/journals in red are not valid."
        elif nb == 0:
            errors[""] = "Year ranges have to be non-empty for at least one conference/journal."
                    
    if request.vars.download != None and len(errors) == 0:
        download_file = URL("crypto_custom.bib", vars=request.vars)

    return dict(confs = confs, journals = journals, errors = errors, download_file = download_file)

def crypto_custom():
    response.headers["Content-Disposition"] = "attachment; filename=crypto_custom.bib"

    confs = db(db.conf.type=="conf").select(db.conf.key, db.conf.name, db.conf.start_year, db.conf.end_year, orderby=db.conf.name)
    journals = db(db.conf.type=="journal").select(db.conf.key, db.conf.name, db.conf.start_year, db.conf.end_year, orderby=db.conf.name)

    expand_crossrefs = request.vars.crossrefs != "true"

    (errors_confs, years_confs, nb_confs) = get_years(confs, request.vars)
    (errors_journals, years_journals, nb_journals) = get_years(journals, request.vars)
    nb = nb_confs + nb_journals
    years = dict(list(years_confs.items()) + list(years_journals.items()))
    
    if nb == 0 or len(errors_confs) > 0 or len(errors_journals) > 0:
        raise HTTP(400, "bad query")

    def gen_bib(out, years):
        q = None
        for (confkey, (start_year, end_year)) in years.items():
            q2 = db.entry.key_conf==confkey
            q2 = q2 & (db.entry.key_year >= start_year)
            q2 = q2 & (db.entry.key_year <= end_year)

            if q == None:
                q = q2
            else:
                q = q | q2

        entries = db(q).select(db.entry.ALL, orderby=db.entry.id)

        if expand_crossrefs:
            crossrefs = {}
            for entry in entries.find(lambda x: x.key_auth == None):
                crossref = entry.as_dict()
                crossref["key"] = None # A bit of a hack... TODO...
                crossrefs[str(EntryKey(confkey=entry.key_conf, year=entry.key_year, dis=entry.key_dis))] = crossref

        for entry in entries:
            if expand_crossrefs and entry.key_auth == None:
                continue
            if expand_crossrefs and entry.crossref != None:
                generator.sql_write_entry(out, entry, crossrefs[entry.crossref_expanded])
            else:
                generator.sql_write_entry(out, entry)
            out.write("\n\n")

    out = io.StringIO()
    out.write(lib.header.get_header(module_db.config, "http://cryptobib.di.ens.fr/init/default/custom", years))
    gen_bib(out, years)

    return dict(result = out.getvalue())

def entry():
    key_str = ":".join(request.args)
    if key_str == "":
        raise HTTP(404, "empty key")
    else:
        try:
            key = EntryKey.from_string(key_str)
        except EntryKeyParsingError as e:
            raise HTTP(404, 'bad format for key (not "CONF/AuthYY")')
        else:
            if key in bibdb.entry:
                entry = bibdb.entry[key]
            else:
                raise HTTP(404, 'no key "{}" found'.format(key_str))

    return dict(bibdb = bibdb, key = key, entry = entry)


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

