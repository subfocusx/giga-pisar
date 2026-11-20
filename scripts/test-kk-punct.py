#!/usr/bin/env python
"""Фикстуры для server/kk_punct.py: вход → ожидаемый текст.

    python scripts/test-kk-punct.py

«|» в строке — пауза 0.8 с, остальные промежутки — 0.1 с. Времена
подбираются здесь же, чтобы фикстуры читались как обычная фраза.
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "server"))
from kk_punct import punctuate  # noqa: E402

CASES = [
    # знак в конце — вопрос, если последнее слово вопросительное
    ("сіз ертең келесіз бе", "Сіз ертең келесіз бе?"),
    ("сіз келесіз бе | құрметті", "Сіз келесіз бе? Құрметті."),
    # личные окончания -дым/-дім/... — сказуемое, пауза делит на предложения
    ("мен бардым | келдім", "Мен бардым. Келдім."),
    ("мен келдім | сен келдің", "Мен келдім. Сен келдің."),
    # ложные срабатывания: винительный падеж, «хабар», производное на -шы
    ("мен үйді | көрдім", "Мен үйді көрдім."),
    ("бұл хабар | айтты", "Бұл хабар айтты."),
    ("ол жұмысшы | келді", "Ол жұмысшы келді."),
    # точка после обычного сказуемого без вопроса
    ("мен ертең келемін", "Мен ертең келемін."),
]


def timed(phrase: str):
    words = []
    t = 0.0
    for token in phrase.split():
        if token == "|":
            t += 0.8
            continue
        words.append((token, t, t + 0.4))
        t += 0.5
    return words


def main() -> int:
    failed = 0
    for phrase, expected in CASES:
        got = punctuate(timed(phrase))
        ok = got == expected
        failed += not ok
        print(("✓" if ok else "✗"), phrase)
        print("   ждали:", expected)
        print("   вышло:", got)
    print(f"\n{len(CASES) - failed}/{len(CASES)} совпало")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
