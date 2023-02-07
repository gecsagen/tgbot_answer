"""Реализация сравнение двух текстовых сообщений"""
import asyncio
from difflib import SequenceMatcher


def string_comparison(
    string_to_compare: str, sample_for_comparison: str
) -> float:
    """Сравнивает строки и возвращает процент похожести в float формате"""
    CHARACTERS_TO_BE_REMOVED = '!?.,-+-*/"()%#№:;='
    clean_line_compare = string_to_compare
    clean_line_comparison = sample_for_comparison
    for x in CHARACTERS_TO_BE_REMOVED:
        clean_line_compare = clean_line_compare.replace(x, "")
        clean_line_comparison = clean_line_comparison.replace(x, "")

    string_to_compare, sample_for_comparison = (
        clean_line_compare.lower().strip(),
        clean_line_comparison.lower().strip(),
    )
    result = SequenceMatcher(None, string_to_compare, sample_for_comparison).ratio()
    return result
