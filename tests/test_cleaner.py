from training_bot.processing.cleaner import TextCleaner

def test_text_cleaner():
    cleaner = TextCleaner()
    raw_text = "  Hello   World!  \n\n\nNew line  "
    cleaned = cleaner.clean(raw_text)
    assert cleaned == "Hello World!\n\nNew line"

def test_remove_short_lines():
    cleaner = TextCleaner()
    text = "Good long line here\nShort\nAnother long line here"
    cleaned = cleaner.remove_short_lines(text, min_length=10)
    assert "Short" not in cleaned
    assert "Good long line" in cleaned
