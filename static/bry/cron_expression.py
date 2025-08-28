from browser import window

CRON_EXPRESSION_TRANSLATIONS = {
    "schedule_minutes": {
        "*": "every minute",
        "0": "the top of the hour",
        "1": "minute past the hour",
        "2": "minutes past the hour",
        "3": "minutes past the hour",
        "4": "minutes past the hour",
        "5": "minutes past the hour",
        "6": "minutes past the hour",
        "7": "minutes past the hour",
        "8": "minutes past the hour",
        "9": "minutes past the hour",
        "10": "minutes past the hour",
        "11": "minutes past the hour",
        "12": "minutes past the hour",
        "13": "minutes past the hour",
        "14": "minutes past the hour",
        "15": "quarter past the hour",
        "16": "minutes past the hour",
        "17": "minutes past the hour",
        "18": "minutes past the hour",
        "19": "minutes past the hour",
        "20": "minutes past the hour",
        "21": "minutes past the hour",
        "22": "minutes past the hour",
        "23": "minutes past the hour",
        "24": "minutes past the hour",
        "25": "minutes past the hour",
        "26": "minutes past the hour",
        "27": "minutes past the hour",
        "28": "minutes past the hour",
        "29": "minutes past the hour",
        "30": "half past the hour",
        "31": "minutes to the hour",
        "32": "minutes to the hour",
        "33": "minutes to the hour",
        "34": "minutes to the hour",
        "35": "minutes to the hour",
        "36": "minutes to the hour",
        "37": "minutes to the hour",
        "38": "minutes to the hour",
        "39": "minutes to the hour",
        "40": "minutes to the hour",
        "41": "minutes to the hour",
        "42": "minutes to the hour",
        "43": "minutes to the hour",
        "44": "minutes to the hour",
        "45": "a quarter to the hour",
        "46": "minutes to the hour",
        "47": "minutes to the hour",
        "48": "minutes to the hour",
        "49": "minutes to the hour",
        "50": "minutes to the hour",
        "51": "minutes to the hour",
        "52": "minutes to the hour",
        "53": "minutes to the hour",
        "54": "minutes to the hour",
        "55": "minutes to the hour",
        "56": "minutes to the hour",
        "57": "minutes to the hour",
        "58": "minutes to the hour",
        "59": "minutes to the hour",
    },
    "schedule_hours": {
        "*": "every hour",
        "0": "the midnight hour",
        "1": "am",
        "2": "am",
        "3": "am",
        "4": "am",
        "5": "am",
        "6": "am",
        "7": "am",
        "8": "am",
        "9": "am",
        "10": "am",
        "11": "am",
        "12": "the midday hour",
        "13": "pm",
        "14": "pm",
        "15": "pm",
        "16": "pm",
        "17": "pm",
        "18": "pm",
        "19": "pm",
        "20": "pm",
        "21": "pm",
        "22": "pm",
        "23": "pm",
    },
    "schedule_days_of_month": {
        "*": "every day of the month",
        "1": "st of the month",
        "2": "nd of the month",
        "3": "rd of the month",
        "4": "th of the month",
        "5": "th of the month",
        "6": "th of the month",
        "7": "th of the month",
        "8": "th of the month",
        "9": "th of the month",
        "10": "th of the month",
        "11": "th of the month",
        "12": "th of the month",
        "13": "th of the month",
        "14": "th of the month",
        "15": "th of the month",
        "16": "th of the month",
        "17": "th of the month",
        "18": "th of the month",
        "19": "th of the month",
        "20": "th of the month",
        "21": "st of the month",
        "22": "nd of the month",
        "23": "rd of the month",
        "24": "th of the month",
        "25": "th of the month",
        "26": "th of the month",
        "27": "th of the month",
        "28": "th of the month",
        "29": "th of the month",
        "30": "th of the month",
        "31": "st of the month",
    },
    "schedule_months": {
        "*": "every month",
        "1": "January",
        "2": "February",
        "3": "March",
        "4": "April",
        "5": "May",
        "6": "June",
        "7": "July",
        "8": "August",
        "9": "September",
        "10": "October",
        "11": "November",
        "12": "December",
    },
    "schedule_days_of_week": {
        "*": "any day of the week",
        "0": "Sunday",
        "1": "Monday",
        "2": "Tuesday",
        "3": "Wednesday",
        "4": "Thursday",
        "5": "Friday",
        "6": "Saturday",
    },
}


def cron_expression_to_string(selector_name, selector_option_values):
    if len(selector_option_values) > 0:
        if selector_name is "schedule_minutes":
            cron_expression_as_string = "At "
        elif selector_name is "schedule_hours":
            cron_expression_as_string = "during "
        elif selector_name is "schedule_days_of_month":
            cron_expression_as_string = "on the "
        elif selector_name is "schedule_months":
            cron_expression_as_string = "in "
        elif selector_name is "schedule_days_of_week":
            cron_expression_as_string = "and on "

        translator_dictionary = CRON_EXPRESSION_TRANSLATIONS[selector_name]
        for option_value in selector_option_values:
            option_value_key = str(option_value)
            if option_value_key is not "*":
                if selector_name is "schedule_minutes":
                    if int(option_value_key) > 30 and option_value_key not in ["45"]:
                        minutes_to_the_hour = str(60 - int(option_value_key))
                        cron_expression_as_string = (
                            cron_expression_as_string + minutes_to_the_hour + " "
                        )
                    elif option_value_key not in ["*", "0", "15", "30", "45"]:
                        cron_expression_as_string = (
                            cron_expression_as_string + option_value_key + " "
                        )
                elif selector_name is "schedule_hours":
                    if int(option_value_key) > 12:
                        minutes_to_the_hour = str(int(option_value_key) - 12)
                        cron_expression_as_string = cron_expression_as_string + minutes_to_the_hour
                    elif option_value_key not in ["*", "0", "12"]:
                        cron_expression_as_string = cron_expression_as_string + option_value_key
                elif selector_name is "schedule_days_of_month":
                    cron_expression_as_string = cron_expression_as_string + option_value_key

            elif selector_name is "schedule_days_of_month":
                cron_expression_as_string = "on "

            cron_expression_as_string = (
                cron_expression_as_string + translator_dictionary[option_value_key] + ", "
            )

        if selector_name is "schedule_days_of_week":
            cron_expression_as_string = cron_expression_as_string[:-2] + "."
        else:
            cron_expression_as_string = cron_expression_as_string[:-2] + ";"
        return cron_expression_as_string
    else:
        return ""


window.cron_expression_to_string = cron_expression_to_string