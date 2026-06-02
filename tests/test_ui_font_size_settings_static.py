from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relpath: str) -> str:
    return (ROOT / relpath).read_text(encoding="utf-8")


def test_appearance_settings_expose_font_size_controls():
    html = read("static/index.html")

    assert 'id="set-chat-font-size"' in html
    assert 'id="set-sidebar-font-size"' in html
    assert 'id="set-chat-font-size" class="theme-fd-range font-size-range" min="8" max="48"' in html
    assert 'id="set-sidebar-font-size" class="theme-fd-range font-size-range" min="7" max="32"' in html
    assert 'id="set-chat-font-size-value" class="font-size-value" for="set-chat-font-size" role="button"' in html
    assert 'id="set-sidebar-font-size-value" class="font-size-value" for="set-sidebar-font-size" role="button"' in html
    assert 'id="set-chat-font-size-reset"' in html
    assert 'id="set-sidebar-font-size-reset"' in html
    assert "chat-font-custom" in html
    assert "sidebar-font-custom" in html


def test_theme_module_persists_and_applies_ui_font_sizes():
    theme_js = read("static/js/theme.js")

    for token in [
        "CHAT_FONT_SIZE_MIN = 8",
        "CHAT_FONT_SIZE_MAX = 48",
        "SIDEBAR_FONT_SIZE_MIN = 7",
        "SIDEBAR_FONT_SIZE_MAX = 32",
        "CHAT_FONT_SIZE_DEFAULT",
        "SIDEBAR_FONT_SIZE_DEFAULT",
        "applyUIFontSizes",
        "getUIFontSizes",
        "updateSavedOptions",
        "chatFontSize",
        "sidebarFontSize",
        "--chat-font-size",
        "--sidebar-font-size",
    ]:
        assert token in theme_js


def test_settings_module_wires_font_size_controls_to_theme_preferences():
    settings_js = read("static/js/settings.js")

    assert "import themeModule from './theme.js';" in settings_js
    assert "function initAppearanceFontSizes()" in settings_js
    assert "function editValue(" in settings_js
    assert "font-size-value-input" in settings_js
    assert "themeModule.applyUIFontSizes" in settings_js
    assert "themeModule.updateSavedOptions" in settings_js


def test_css_font_size_overrides_are_scoped_to_custom_classes():
    css = read("static/style.css")

    assert ":root.chat-font-custom #chat-history .msg" in css
    assert ":root.chat-font-custom .chat-input-bar textarea#message" in css
    assert ":root.sidebar-font-custom #sidebar .section-header-flex h4" in css
    assert ":root.sidebar-font-custom #sidebar .list-item .grow" in css
    assert ".font-size-value-input" in css
