#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
hunspell_dump_forms_v12.py

v12:
- безопасно обрабатывает языки, для которых нет pyphen-словаря:
  pyphen_dic = None => в output пишутся исходные словоформы (без переносных меток)
  и в no-hyphen.log аппендится "<lang>\tMISSING" или "<lang>\tAVAILABLE"
- сохраняет логику PFX/SFX (.aff parsing), разбиение составных частей,
  украинские эвристики и пост-правки, и флаги управления (stream, dedupe, keep-invalid, removed-log)
- маркер переноса: U+2500 (BOX DRAWINGS LIGHT HORIZONTAL)
"""

from __future__ import annotations
import argparse
import re
import sys
from itertools import product
import pyphen
from pathlib import Path

# -----------------------
# Константы / настройки
# -----------------------
HY_MARK = "\u2500"  # U+2500 BOX DRAWINGS LIGHT HORIZONTAL '─'
COMPOUND_SEPARATORS = "-\u2010\u2011\u2012\u2013\u2014\u2015"
_COMPOUND_SPLIT_RE = re.compile(r"([" + re.escape(COMPOUND_SEPARATORS) + r"])")

UK_VOWELS = set("аеєиіїоуюяАЕЄИІЇОУЮЯ")
UK_CONSONANTS = set("бвгґджзйклмнпрстфхцчшщБВГҐДЖЗЙКЛМНПРСТФХЦЧШЩ")

# -----------------------
# AFF parsing (PFX/SFX)
# -----------------------
def load_affixes(path: str):
    pfx_rules = {}
    sfx_rules = {}
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                if parts[0] == "PFX":
                    flag = parts[1]
                    if parts[2] in ("Y", "N"):
                        pfx_rules.setdefault(flag, [])
                    else:
                        remove = parts[2]; add = parts[3]; cond = parts[4] if len(parts) > 4 else "."
                        pfx_rules.setdefault(flag, []).append((remove, add, cond))
                elif parts[0] == "SFX":
                    flag = parts[1]
                    if parts[2] in ("Y", "N"):
                        sfx_rules.setdefault(flag, [])
                    else:
                        remove = parts[2]; add = parts[3]; cond = parts[4] if len(parts) > 4 else "."
                        sfx_rules.setdefault(flag, []).append((remove, add, cond))
    except FileNotFoundError:
        # если .aff не найден — возвращаем пустые правила (скрипт всё равно сможет писать исходные слова)
        return {}, {}
    return pfx_rules, sfx_rules

# -----------------------
# Apply affix rules
# -----------------------
def apply_affixes(word: str, flags: list[str], pfx_rules: dict, sfx_rules: dict) -> set[str]:
    forms = set([word])

    # PFX
    for flag in flags:
        if flag in pfx_rules:
            for remove, add, cond in pfx_rules[flag]:
                try:
                    ok = re.match(cond + r"$", word) is not None
                except re.error:
                    ok = True
                if not ok:
                    continue
                if remove == "0":
                    base = word
                elif word.startswith(remove):
                    base = word[len(remove):]
                else:
                    continue
                forms.add(add + base)

    # SFX
    for flag in flags:
        if flag in sfx_rules:
            for remove, add, cond in sfx_rules[flag]:
                try:
                    ok = re.search(cond + r"$", word) is not None
                except re.error:
                    ok = True
                if not ok:
                    continue
                if remove == "0":
                    base = word
                elif word.endswith(remove):
                    base = word[:-len(remove)]
                else:
                    continue
                forms.add(base + add)

    return forms

# -----------------------
# split components (preserve separators)
# -----------------------
def split_components_preserve_separators(word: str) -> list[str]:
    parts = _COMPOUND_SPLIT_RE.split(word)
    return [p for p in parts if p != ""]

# -----------------------
# Ukrainian heuristics & post-fix rules
# -----------------------
def collapse_single_consonants_uk(parts: list[str]) -> list[str]:
    out = []
    i = 0
    n = len(parts)
    while i < n:
        p = parts[i]
        if len(p) == 1 and p in UK_CONSONANTS:
            if i + 1 < n:
                parts[i + 1] = p + parts[i + 1]
            elif out:
                out[-1] = out[-1] + p
            else:
                out.append(p)
            i += 1
        else:
            out.append(p)
            i += 1
    return out

_UK_SUFFIX_RULES = [
    (re.compile(r"([Нн]и[й])([аеєиіїоуюяАЕЄИІЇОУЮЯ])"), r"\1" + HY_MARK + r"\2"),
    (re.compile(r"([сС]ьк)([аеєиіїоуюяАЕЄИІЇОУЮЯ])"), r"\1" + HY_MARK + r"\2"),
    (re.compile(r"([Нн]и[й])([А-Яа-я]{2,})$"), r"\1" + HY_MARK + r"\2"),
]

def fix_uk_suffixes(s: str) -> str:
    out = s
    for pat, repl in _UK_SUFFIX_RULES:
        out = pat.sub(repl, out)
    return out

# -----------------------
# hyphenate single component (uses pyphen_dic if present)
# -----------------------
def hyphenate_component(comp: str, pyphen_dic, lang: str) -> str:
    """
    If pyphen_dic is None -> return comp unchanged.
    Otherwise use pyphen_dic.inserted(comp), apply uk heuristics, join with HY_MARK.
    """
    if pyphen_dic is None:
        return comp

    try:
        inserted = pyphen_dic.inserted(comp)
    except Exception:
        return comp

    if inserted == comp:
        return comp

    parts = inserted.split("-")
    if lang.startswith("uk"):
        parts = collapse_single_consonants_uk(parts)

    joined = HY_MARK.join(parts)

    if lang.startswith("uk"):
        joined = fix_uk_suffixes(joined)

    # defensive normalizations
    joined = re.sub(HY_MARK + r"{2,}", HY_MARK, joined).strip()
    joined = joined.strip(HY_MARK)
    return joined

# -----------------------
# final validation / filters
# -----------------------
def is_invalid_output(s: str) -> bool:
    if not s or s.strip() == "":
        return True
    if s.endswith("0"):
        return True
    return False

# -----------------------
# write no-hyphen log
# -----------------------
def append_no_hyphen_log(lang: str, status: str, logfile: str = "no-hyphen.log"):
    try:
        with open(logfile, "a", encoding="utf-8") as fh:
            fh.write(f"{lang}\t{status}\n")
    except Exception:
        # best-effort: don't fail the whole script for logging problems
        pass

# -----------------------
# CLI / main
# -----------------------
def main():
    p = argparse.ArgumentParser(description="Dump Hunspell forms with hyphen marker (U+2500) — v12")
    p.add_argument("--aff", required=True, help="Path to .aff file")
    p.add_argument("--dic", required=True, help="Path to .dic file")
    p.add_argument("--lang", required=True, help="Pyphen language code, e.g. uk_UA, ru_RU")
    p.add_argument("--output", required=True, help="Output file")
    p.add_argument("--limit", type=int, default=10**9, help="Limit number of entries to process")
    p.add_argument("--keep-invalid", action="store_true", help="Do not drop outputs that end with '0'")
    p.add_argument("--no-dedupe", action="store_true", help="Do not deduplicate outputs")
    p.add_argument("--stream", action="store_true", help="Write results to output as they are generated (no big in-memory set)")
    p.add_argument("--removed-log", default=None, help="If set, write removed/filtered lines to this file")
    args = p.parse_args()

    # try load aff rules
    pfx_rules, sfx_rules = load_affixes(args.aff)

    # try init pyphen, but handle missing dictionary gracefully
    pyphen_dic = None
    pyphen_status = "MISSING"
    try:
        # try to create pyphen dic; this may raise KeyError if language missing
        pyphen_dic = pyphen.Pyphen(lang=args.lang)
        pyphen_status = "AVAILABLE"
    except Exception:
        pyphen_dic = None
        pyphen_status = "MISSING"
    # append to no-hyphen.log (append mode)
    append_no_hyphen_log(args.lang, pyphen_status, logfile="no-hyphen.log")

    removed_fh = None
    if args.removed_log:
        removed_fh = open(args.removed_log, "w", encoding="utf-8")

    stream_mode = args.stream
    dedupe = not args.no_dedupe
    seen_stream = set() if (stream_mode and dedupe) else set()
    collected = set() if (not stream_mode and dedupe) else None

    written = 0
    processed = 0

    try:
        with open(args.dic, encoding="utf-8", errors="ignore") as df, \
             open(args.output, "w", encoding="utf-8") as out:
            header = df.readline()  # skip possible count
            for raw in df:
                line = raw.strip()
                if not line:
                    continue
                if "/" in line:
                    lemma, flag_str = line.split("/", 1)
                    flags = list(flag_str)
                else:
                    lemma = line
                    flags = []

                forms = apply_affixes(lemma, flags, pfx_rules, sfx_rules)
                for f in forms:
                    comps = split_components_preserve_separators(f)
                    out_parts = []
                    for comp in comps:
                        if len(comp) == 1 and comp in COMPOUND_SEPARATORS:
                            out_parts.append(comp)
                        else:
                            out_parts.append(hyphenate_component(comp, pyphen_dic, args.lang))
                    final = "".join(out_parts)

                    # normalization
                    final = re.sub(HY_MARK + r"{2,}", HY_MARK, final).strip()
                    final = final.strip(HY_MARK)

                    invalid = is_invalid_output(final)
                    if invalid and not args.keep_invalid:
                        if removed_fh:
                            removed_fh.write(final + "\n")
                        continue

                    if stream_mode:
                        if dedupe:
                            if final in seen_stream:
                                continue
                            seen_stream.add(final)
                        out.write(final + "\n")
                        written += 1
                    else:
                        if dedupe:
                            collected.add(final)
                        else:
                            out.write(final + "\n")
                            written += 1

                processed += 1
                if processed % 10000 == 0:
                    print(f"[+] processed {processed} lemmas...", file=sys.stderr)
                if processed >= args.limit:
                    break

            # flush collected
            if not stream_mode:
                if collected is not None:
                    for w in sorted(collected):
                        out.write(w + "\n")
                    written = len(collected)

    finally:
        if removed_fh:
            removed_fh.close()

    print(f"Done: processed {processed} lemmas, written {written} lines to {args.output}", file=sys.stderr)
    print(f"Pyphen status for {args.lang}: {pyphen_status} (logged to no-hyphen.log)", file=sys.stderr)


if __name__ == "__main__":
    main()
