def to_lower_camel(name: str) -> str:
    """
    Converts a snake_case string to lowerCamelCase
    """
    upper = "".join(word.capitalize() for word in name.split("_"))
    return upper[:1].lower() + upper[1:]
