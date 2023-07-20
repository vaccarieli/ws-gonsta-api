from bs4 import BeautifulSoup


def generate_message(yt_url):
    return f"""🎮 ¡Disponible Hoy! ¡Escribeme Ya!🕹
👉 Mira El Video Aquí: {yt_url} 👈
📲 #Nintendo #Switch #Videojuegos """

def extract_url(url) -> str:
    import re

    # Define the regular expression pattern to match the URL inside the parentheses
    pattern = r"url\((.*?)\)"

    # Use the findall() method to find all occurrences of the pattern in the string
    try:
        return re.findall(pattern, url)[0]
    except Exception:
        pass


def extract_main_data(html, filter="Today") -> dict:
    new_calendar = {}
    base_url = "https://www.releases.com"

    soup = BeautifulSoup(html, "html.parser")

    images = [
        extract_url(i.find("div", class_="calendar-item-head").get("style"))
        for i in soup.find_all("a", class_="calendar-item-href subpage-trigg")
    ]

    calendar = [
        {
            i.a.text.strip(): {
                "link": base_url + i.a.get("href").strip(),
                "Image": images[index],
            }
        }
        for index, i in enumerate(soup.find_all("div", class_="calendar-item-detail"))
    ]
    calendar_2 = [
        i.find("span", class_="test-time").text.strip()
        for i in soup.find_all(
            "div", class_="calendar-item-footer platform-selector-wrap"
        )
    ]

    for index, date in enumerate(calendar_2):
        for key, value in calendar[index].items():
            if date == filter:
                new_calendar[key] = value

    return new_calendar


def convert_embed_to_watch_link(embed_link):
    watch_link = embed_link.replace(
        "youtube.com/embed/", "www.youtube.com/watch?v="
    ).replace("?autoplay=1", "")
    return watch_link


def add_yt_url_to_data(webdriver, data):
    from tqdm import tqdm

    for game in tqdm(data, desc="Downloading YT Urls: "):
        webdriver.get(data[game]["link"])

        html = BeautifulSoup(webdriver.page_source, "html.parser")

        def youtube_url_attribute_value(value):
            return value and value.startswith("https://youtube.com")

        yt_url = html.find("section", attrs={"video-url": youtube_url_attribute_value})

        if yt_url:
            data[game].update(
                {
                    "yt_link": convert_embed_to_watch_link(
                        yt_url.get("video-url").strip()
                    )
                }
            )
    return data
