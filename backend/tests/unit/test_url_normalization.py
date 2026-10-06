from app.tools.scraper import normalize_url, sanitize_text


def test_normalize_url_removes_utm_parameters():
    raw = "https://example.com/article?utm_source=twitter&utm_medium=social&utm_campaign=launch&id=123"
    expected = "https://example.com/article?id=123"
    assert normalize_url(raw) == expected


def test_normalize_url_removes_trailing_slash_and_fragment():
    raw = "https://example.com/docs/api/#authentication"
    expected = "https://example.com/docs/api"
    assert normalize_url(raw) == expected


def test_normalize_url_lowercases_domain_and_scheme():
    raw = "HTTPS://WWW.Example.COM/Path"
    expected = "https://www.example.com/Path"
    assert normalize_url(raw) == expected


def test_normalize_url_empty_or_none():
    assert normalize_url("") == ""
    assert normalize_url("   ") == ""


def test_sanitize_text_strips_html_and_excessive_whitespace():
    raw_html = "<p>This is a <b>bold</b> statement.</p>\n\n<script>alert('xss')</script>  More text."
    cleaned = sanitize_text(raw_html)
    assert "<p>" not in cleaned
    assert "<b>" not in cleaned
    assert "This is a bold statement. alert('xss') More text." == cleaned


def test_sanitize_text_truncation():
    long_text = "word " * 500
    cleaned = sanitize_text(long_text, max_chars=50)
    assert len(cleaned) <= 53  # 50 chars + "..."
    assert cleaned.endswith("...")
