from browser import window, document, console


TRANSLATION_TARGET = document["schedule_translation"]
cron_translation = {
    "schedule_minutes": "",
    "schedule_hours": "",
    "schedule_days_of_month": "",
    "schedule_months": "",
    "schedule_days_of_week": "",
}
cron_expression_to_string = window.cron_expression_to_string


def selector_changed(ev, *args, **kwargs):
    cron_translation[ev.target.name] = cron_expression_to_string(
        ev.target.name,
        [option.value for option in ev.target.selectedOptions],
    )
    TRANSLATION_TARGET.html = " <br>--".join(cron_translation.values())

    for cron_element in cron_translation.values():
        if cron_element is not "":
            return

    TRANSLATION_TARGET.html = "No Schedule Set. To set one click here"


def main_cronfield(*args, **kwargs):
    S("#schedule_tabs").tabs()

    schedule_selectors = document.select(".schedule-selector")
    for selector, selector_name in zip(schedule_selectors, cron_translation.keys()):
        document[selector.id].bind("change", selector_changed)
        select_element = document.get(name=selector_name)[0]
        cron_translation[selector_name] = cron_expression_to_string(
            selector_name,
            [option.value for option in select_element.selectedOptions],
        )

    if cron_translation["schedule_minutes"] is "":
        cron_translation["schedule_minutes"] = "No Schedule Set. To set one click here"
        TRANSLATION_TARGET.html = "".join(cron_translation.values())
    else:
        TRANSLATION_TARGET.html = "<br>--".join(cron_translation.values())


S = window.jQuery
S(document).ready(main_cronfield)