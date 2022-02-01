#!/usr/bin/python3

"""
Generates `meetup.com` URLs for the upcoming TWiR
"""
import datetime

WEDNESDAY_DATETIME_DAY = 2
END_DATE_WEEKS = 4 # Number of weeks to skip

START_URL_ENCODING = "T03%3A00%3A00-05%3A00" #T03:00:00
END_URL_ENCODING = "T02%3A59%3A00-05%3A00" #T02:59:00
EVENT_TYPES = [
    "online",
    "inPerson"
]
KEYWORDS = [
    "Rust"
]
LOCATIONS = [
    "us--tx--Dallas",
    "us--ca--San%20Francisco",
    "us--ma--Boston",
    "gb--Greater%20London--London",
    "ru--Moscow",
    "ma--Casablanca",
    "de--Berlin"
]

def get_closest_wednesday():
    """
    Returns the closest Wednesday to the current day
    """
    day = datetime.datetime.today()

    while day.weekday() != WEDNESDAY_DATETIME_DAY:
        day += datetime.timedelta(days=1)
    
    return day

def get_desired_date_range():
    """
    Returns datetime.datetime for the next closest Wednesday, and the Wednesday that 
    is four weeks later.
    """
    closest_wednesday = get_closest_wednesday()

    # We add END_DATE_WEEKS, and 1 day because Meetup requires DAY+1 for proper querying
    end_date = closest_wednesday + datetime.timedelta(weeks=END_DATE_WEEKS, days=1) 

    return closest_wednesday, end_date

def get_formatted_dates():
    """
    Returns formatted date strings of format "YEAR-MONTH-DAY"

    e.g. March 11, 2022 would be 2022-03-01{START_URL_ENCODING}
    """

    start, end = get_desired_date_range()
    start_year, end_year = str(start.year), str(end.year)
    start_month, end_month = str(start.month).zfill(2), str(end.month).zfill(2) # left padding with 0s
    start_day, end_day = str(start.day).zfill(2), str(end.day).zfill(2) # left padding with 0s

    return f"{start_year}-{start_month}-{start_day}{START_URL_ENCODING}", f"{end_year}-{end_month}-{end_day}{END_URL_ENCODING}"

def get_urls():
    urls = []
    start_date, end_date = get_formatted_dates() 

    for event_type in EVENT_TYPES:
        for keyword in KEYWORDS:
            for loc in LOCATIONS:
                full_url = f"https://www.meetup.com/find/" \
                        f"?keywords={keyword}" \
                        f"&source=EVENTS&" \
                        f"customStartDate={start_date}" \
                        f"&customEndDate={end_date}" \
                        f"&location={loc}" \
                        f"&eventType={event_type}"
                urls.append(full_url)
    
    return urls


def main():
    urls = get_urls()

    # TODO: Auto parse results... For now, generates an HTML page of links to use
    date_title = str(datetime.datetime.today().strftime("%m_%d_%Y"))
    with open(f'{date_title}.html', 'w') as f:
        f.write(f'<p>{date_title}</p>\n<br>\n')
        for i, url in enumerate(urls):
            text_line = url[160:]
            f.write(f'<a href="{url}" target="_blank">{text_line}</a>\n<br>\n<br>\n')

if __name__ == '__main__':
    main()
