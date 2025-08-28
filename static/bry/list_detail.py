from browser import window, document, console


TRANSLATION_TARGET = document["schedule-translation"]
cron_translation = {
    "schedule_minutes": "",
    "schedule_hours": "",
    "schedule_days_of_month": "",
    "schedule_months": "",
    "schedule_days_of_week": "",
}


def main(*args, **kwargs):
    S("#edit-list").tooltip()
    S("#delete-list").tooltip()
    cron_expression_to_string = window.cron_expression_to_string

    text_for_translation = TRANSLATION_TARGET.html.lstrip().rstrip()
    if text_for_translation is not "There is no specific schedule for this procedure.":
        cron_elements = text_for_translation.split(" ")
        cron_values = [cron_element_values.split(",") for cron_element_values in cron_elements]

        for cron_element_values, selector_name in zip(cron_values, cron_translation.keys()):
            cron_translation[selector_name] = cron_expression_to_string(
                selector_name,
                cron_element_values,
            )

        TRANSLATION_TARGET.html = "<br>--".join(cron_translation.values())

    S(TRANSLATION_TARGET).removeClass("placeholder")


S = window.jQuery
S(document).ready(main)