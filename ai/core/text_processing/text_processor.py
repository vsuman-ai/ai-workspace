from typing import Any, Callable, Dict, List, Set

import neattext as nt
from cleantext import clean
from cleantext.clean import replace_urls
from ai.core.enums.source_type import SourceType
from pydantic import BaseModel


class ProcessingResult(BaseModel):
    original: str
    processed: str
    steps_applied: List[str]
    metadata: Dict[str, Any]


class TextProcessor:
    def __init__(self, text: str):
        self.original_text = text
        self.current_text = text
        self.steps_applied = []
        self.preserve_tokens = set()
        self.source_type = None

    def remove_urls(self) -> "TextProcessor":
        """Remove URLs from text."""
        try:
            self.current_text = replace_urls(self.current_text, "")
            self.steps_applied.append("remove_urls")
        except Exception as e:
            print(f"remove_urls error: {e}")
        return self

    def remove_html(self) -> "TextProcessor":
        """Remove HTML tags."""
        try:
            doc = nt.TextFrame(self.current_text)
            doc.remove_html_tags()
            self.current_text = doc.text
            self.steps_applied.append("remove_html")
        except Exception as e:
            print(f"remove_html error: {e}")
        return self

    def fix_contractions(self) -> "TextProcessor":
        """Fix contractions (don't -> do not)"""
        try:
            doc = nt.TextFrame(self.current_text)
            doc.fix_contractions()
            self.current_text = doc.text
            self.steps_applied.append("fix_contractions")
        except Exception as e:
            print(f"fix_contractions error: {e}")
        return self

    def remove_emojis(self) -> "TextProcessor":
        """Remove emojis."""
        try:
            doc = nt.TextFrame(self.current_text)
            doc.remove_emojis()
            self.current_text = doc.text
            self.steps_applied.append("remove_emojis")
        except Exception as e:
            print(f"remove_emojis error: {e}")
        return self

    def remove_punctuation(self, preserve: Set[str] = None) -> "TextProcessor":
        """Remove punctuation, optionally preserving some."""
        try:
            preserve = preserve or set()
            all_preserve = preserve | self.preserve_tokens

            if all_preserve:
                self.current_text = self._clean_with_preservation(
                    self.current_text, all_preserve, no_punct=True, replace_with_punct="", lang="en"
                )
            else:
                self.current_text = clean(
                    self.current_text, no_punct=True, replace_with_punct="", lang="en"
                )

            self.steps_applied.append("remove_punctuation")
        except Exception as e:
            print(f"remove_punctuation error: {e}")
        return self

    def remove_numbers(self) -> "TextProcessor":
        """Remove numbers."""
        try:
            self.current_text = clean(
                self.current_text,
                no_numbers=True,
                no_digits=True,
                no_currency_symbols=True,
                replace_with_digit="",
                replace_with_number="",
                replace_with_currency_symbol="",
                lang="en",
            )
            self.steps_applied.append("remove_numbers")
        except Exception as e:
            print(f"remove_numbers error: {e}")
        return self

    def normalize_whitespace(self) -> "TextProcessor":
        """Normalize whitespace and remove line breaks."""
        try:
            self.current_text = clean(
                self.current_text,
                normalize_whitespace=True,
                no_line_breaks=True,
                fix_unicode=True,
                to_ascii=True,
                lang="en",
            )
            self.steps_applied.append("normalize_whitespace")
        except Exception as e:
            print(f"normalize_whitespace error: {e}")
        return self

    def remove_contact_info(self) -> "TextProcessor":
        """Remove emails."""
        try:
            self.current_text = clean(
                self.current_text,
                no_emails=True,
                no_phone_numbers=True,
                replace_with_email="",
                replace_with_phone_number="",
            )
            self.steps_applied.append("remove_contact_info")
        except Exception as e:
            print(f"remove_contact_info error: {e}")
        return self

    def to_lowercase(self) -> "TextProcessor":
        """Convert to lowercase."""
        self.current_text = self.current_text.lower()
        self.steps_applied.append("to_lowercase")
        return self

    def remove_extra_spaces(self) -> "TextProcessor":
        """Remove extra spaces."""
        try:
            import re

            self.current_text = re.sub(r"\s+", " ", self.current_text).strip()
            self.steps_applied.append("remove_extra_spaces")
        except Exception as e:
            print(f"remove_extra_spaces error: {e}")
        return self

    def remove_digits(self) -> "TextProcessor":
        try:
            import re

            self.current_text = re.sub(r"\d", "", self.current_text).strip()
            self.steps_applied.append("remove_digits")
        except Exception as e:
            print(f"remove_digits error: {e}")
        return self

    # Configuration methods
    def preserve(self, *tokens: str) -> "TextProcessor":
        """Add tokens to preserve during cleaning."""
        self.preserve_tokens.update(tokens)
        return self

    def for_source(self, source: SourceType) -> "TextProcessor":
        """Configure for specific source type."""
        self.source_type = source
        if source == SourceType.TWITTER:
            self.preserve("@", "#")
        return self

    def apply_custom(self, func: Callable[[str], str], step_name: str) -> "TextProcessor":
        """Apply custom processing function."""
        try:
            self.current_text = func(self.current_text)
            self.steps_applied.append(f"custom_{step_name}")
        except Exception as e:
            print(f"apply_custom({step_name}) error: {e}")
        return self

    # Result methods
    def build(self) -> ProcessingResult:
        """Build and return processing result."""
        return ProcessingResult(
            original=self.original_text,
            processed=self.current_text,
            steps_applied=self.steps_applied.copy(),
            metadata={
                "source_type": self.source_type,
                "preserved_tokens": list(self.preserve_tokens),
            },
        )

    def text(self) -> str:
        """Get processed text."""
        return self.current_text

    def result(self) -> Dict[str, Any]:
        """Get result as dictionary."""
        result = self.build()
        return {
            "original": result.original,
            "processed": result.processed,
            "steps_applied": result.steps_applied,
            "metadata": result.metadata,
        }

    # Helper methods
    def basic_text_cleaning(self) -> "TextProcessor":
        """Apply aggressive cleaning for analysis."""
        return (
            self.normalize_whitespace()
            .remove_urls()
            .remove_emojis()
            .remove_html()
            .fix_contractions()
            .remove_punctuation()
            .remove_contact_info()
        )

    def _clean_with_preservation(self, text: str, preserve: Set[str], **clean_kwargs) -> str:
        """Clean text while preserving specific tokens."""
        placeholder_map = {token: f"__preserve_{i}__" for i, token in enumerate(preserve, 1)}
        # Protect tokens
        for token, placeholder in placeholder_map.items():
            text = text.replace(token, placeholder)
        # Clean
        cleaned = clean(text, **clean_kwargs)
        # Restore tokens
        for token, placeholder in placeholder_map.items():
            cleaned = cleaned.replace(placeholder, token)

        return cleaned
