import re


class TextUtils:
    EMOJI_PATTERN = re.compile(
        "["
        "\U0001f600-\U0001f64f"  # Emoji for smileys
        "\U0001f300-\U0001f5ff"  # Symbols and pictographs
        "\U0001f680-\U0001f6ff"  # Transport and map symbols
        "\U0001f700-\U0001f77f"  # Alchemical symbols
        "\U0001f780-\U0001f7ff"  # Geometric shapes
        "\U0001f800-\U0001f8ff"  # Supplemental symbols
        "\U0001f900-\U0001f9ff"  # Additional supplemental symbols
        "\U0001fa00-\U0001fa6f"  # Chess symbols
        "\U0001fa70-\U0001faff"  # Symbols and pictograms
        "\U00002702-\U000027b0"  # Dingbats
        "\U000024c2-\U0001f251"  # Enclosed characters
        "]+",
        flags=re.UNICODE,
    )

    @staticmethod
    def get_post_link(owner_id, post_id):
        """Constructs a VK post URL using the owner's ID and the post ID."""
        return f"https://vk.com/wall{owner_id}_{post_id}"

    @staticmethod
    def remove_emoji(text: str, EMOJI_PATTERN=EMOJI_PATTERN):
        """Removes all emojis from the provided text using a predefined regex pattern."""

        return EMOJI_PATTERN.sub(r"", text)

    @staticmethod
    def extract_title(post_text: str):
        """Extracts the first line of the text, cleans it up, and removes emojis."""
        lines = post_text.split("\n")  # Split text by newlines

        if lines:
            title = lines[0].strip()  # Use the first non-empty line as the title
            return TextUtils.remove_emoji(title)  # Remove any emojis in the title

        return "Без названия"  # Default value for empty posts

    @staticmethod
    def count_chars_before_pattern(post_text: str):
        hash_index = post_text.find("#")  # Find first occurrence of '#'

        if hash_index == -1:  # If '#' is not found
            return len(post_text)  # Return the full length of the text

        return hash_index  # Return the index of the first '#'
