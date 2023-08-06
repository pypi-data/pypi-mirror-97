import panel as pn


def url_link_button(url, label="Authenticate", **kwargs):
    button = pn.widgets.Button(name=label, **kwargs)
    button.js_on_click(code=f"window.open('{url}')")
    return button
