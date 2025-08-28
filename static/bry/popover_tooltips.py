from browser import window, document, console


def main(*args, **kwargs):
    elements_with_tooltips = document.select("[data-bs-toggle]")
    for element in elements_with_tooltips:
        if element.attrs["data-bs-toggle"] == "tooltip":
            S(element).tooltip()


S = window.jQuery
S(document).ready(main)