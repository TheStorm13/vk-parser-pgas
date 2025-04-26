import re


class TextUtils:
    EMOJI_PATTERN = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # Emoji for smileys
        u"\U0001F300-\U0001F5FF"  # Symbols and pictographs
        u"\U0001F680-\U0001F6FF"  # Transport and map symbols
        u"\U0001F700-\U0001F77F"  # Alchemical symbols
        u"\U0001F780-\U0001F7FF"  # Geometric shapes
        u"\U0001F800-\U0001F8FF"  # Supplemental symbols
        u"\U0001F900-\U0001F9FF"  # Additional supplemental symbols
        u"\U0001FA00-\U0001FA6F"  # Chess symbols
        u"\U0001FA70-\U0001FAFF"  # Symbols and pictograms
        u"\U00002702-\U000027B0"  # Dingbats
        u"\U000024C2-\U0001F251"  # Enclosed characters
        "]+", flags=re.UNICODE)

    @staticmethod
    def get_post_link(owner_id, post_id):
        """Constructs a VK post URL using the owner's ID and the post ID."""
        return f"https://vk.com/wall{owner_id}_{post_id}"

    @staticmethod
    def remove_emoji(text: str, EMOJI_PATTERN=EMOJI_PATTERN):
        """Removes all emojis from the provided text using a predefined regex pattern."""

        return EMOJI_PATTERN.sub(r'', text)

    @staticmethod
    def extract_title(post_text: str):
        """Extracts the first line of the text, cleans it up, and removes emojis."""
        lines = post_text.split('\n')  # Split text by newlines

        if lines:
            title = lines[0].strip()  # Use the first non-empty line as the title
            return TextUtils.remove_emoji(title)  # Remove any emojis in the title

        return "Без названия"  # Default value for empty posts

    @staticmethod
    def count_chars_before_pattern(post_text: str):
        hash_index = post_text.find('#')  # Find first occurrence of '#'

        if hash_index == -1:  # If '#' is not found
            return len(post_text)  # Return the full length of the text

        return hash_index  # Return the index of the first '#'
