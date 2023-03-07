import datetime
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List
from urllib.parse import urljoin, urlparse

import requests
from lxml.html import document_fromstring


__version__ = "0.1.4"
REGEXP_BACKGROUND_IMAGE_URL = re.compile(r"background-image:url\('(.*)'\)")


def extract_bg_img(style):
    url = REGEXP_BACKGROUND_IMAGE_URL.findall(style)[0]
    if url.startswith("//"):
        url = f"https:{url}"
    return url

def convert_int(value):
    if value.endswith("M"):
        return int(float(value[:-1]) * 1_000_000)
    elif value.endswith("K"):
        return int(float(value[:-1]) * 1_000)
    else:
        return int(value)


@dataclass
class ChannelMessage:
    id: int
    created_at: datetime.datetime
    type: str
    channel: str
    edited: bool
    urls: List[str]
    author: str = None
    text: str = None
    views: int = None
    reply_to_id: int = None
    preview_url: str = None
    preview_image_url: str = None
    preview_site_name: str = None
    preview_title: str = None
    preview_description: str = None
    forwarded_author: str = None
    forwarded_author_url: str = None


@dataclass
class ChannelInfo:
    username: str
    title: str
    image_url: str
    description: str = None
    subscribers: int = None
    photos: int = None
    videos: int = None
    links: int = None


def normalize_url(username_or_url):
    """Normalize username or URL to a channel canonical URL"""
    path = urlparse(username_or_url).path
    if path.startswith("t.me/"):
        path = path[4:]
    if path.startswith("/s/"):
        path = path[2:]
    if path.startswith("/"):
        path = path[1:]
    if path.startswith("@"):
        path = path[1:]
    return urljoin("https://t.me/s/", path.split("/")[0])


def extract_text(parts, delimiter="\n"):
    return delimiter.join(
        item.strip() for item in parts if item.strip()
    ).strip()


def parse_info(tree):
    username = extract_text(
        tree.xpath(
            "//div[@class = 'tgme_channel_info_header_username']//text()"
        ),
        delimiter="",
    )
    if username[0] == "@":
        username = username[1:]
    title_text = tree.xpath("//meta[@property = 'og:title']/@content")
    title = title_text[0] if title_text else None
    image_url_text = tree.xpath("//meta[@property = 'og:image']/@content")
    image_url = image_url_text[0] if image_url_text else None
    description_text = tree.xpath(
        "//meta[@property = 'og:description']/@content"
    )
    description = description_text[0] if description_text else None
    counters = {}
    counters_div = tree.xpath("//div[@class = 'tgme_channel_info_counters']")[0]
    for counter_div in counters_div.xpath(
        ".//div[@class = 'tgme_channel_info_counter']"
    ):
        key = counter_div.xpath(".//span[@class = 'counter_type']/text()")[0]
        value = convert_int(
            counter_div.xpath(".//span[@class = 'counter_value']/text()")[0]
        )
        counters[key] = value

    return ChannelInfo(
        username=username,
        title=title,
        image_url=image_url,
        description=description,
        subscribers=counters.get("subscriber"),
        photos=counters.get("photos"),
        videos=counters.get("videos"),
        links=counters.get("links"),
    )


def parse_messages(original_url, tree):
    "Retrieve messages from HTML tree"
    messages = tree.xpath("//div[contains(@class, 'tgme_widget_message_wrap')]")
    for message in reversed(messages):
        if message.xpath(".//div[contains(@class, 'tme_no_messages_found')]"):
            # XXX: this case may happen because a great number of requests was
            # made and Telegram sent this response as if there were no new
            # posts when actually there are.
            return
        channel, id_ = message.xpath(".//div/@data-post")[0].split("/")
        created_at = datetime.datetime.fromisoformat(
            message.xpath(".//time/@datetime")[0]
        )
        edited_text = message.xpath(
            ".//span[@class = 'tgme_widget_message_meta']/text()"
        )
        edited = "edited" in edited_text[0].strip() if edited_text else False
        author_text = message.xpath(
            ".//span[@class = 'tgme_widget_message_from_author']/text()"
        )
        author = author_text[0] if author_text else None
        text, views, type_, reply_to_id, urls = None, None, None, None, []
        forwarded_author, forwarded_author_url = None, None
        (
            preview_url,
            preview_image_url,
            preview_site_name,
            preview_title,
            preview_description,
        ) = (None, None, None, None, None)
        text_div_list = message.xpath(
            ".//div[contains(@class, 'tgme_widget_message_text')]"
        )
        text_div = text_div_list[0] if text_div_list else None
        if message.xpath(".//div[contains(@class, 'service_message')]"):
            text = extract_text(text_div.xpath(".//text()"), delimiter="")
            type_ = "service"
            image_url_text = message.xpath(
                ".//a[@class = 'tgme_widget_message_service_photo']/img/@src"
            )
            if image_url_text:
                urls.append(("photo", urljoin(original_url, image_url_text[0])))

        else:
            views_text = extract_text(
                message.xpath(
                    ".//span[contains(@class, 'tgme_widget_message_views')]//text()"
                ),
                delimiter="",
            )
            if views_text:
                views = convert_int(views_text)
            if text_div is not None:
                text = extract_text(text_div.xpath(".//text()"), delimiter="\n")
                emoji_style_text = text_div.xpath(
                    ".//i[@class = 'emoji']/@style"
                )
                if emoji_style_text:
                    urls.append(
                        (
                            "photo",
                            urljoin(
                                original_url,
                                extract_bg_img(emoji_style_text[0]),
                            ),
                        )
                    )
            else:
                sticker_div_list = message.xpath(
                    ".//div[contains(@class, 'tgme_widget_message_sticker_wrap')]//i[contains(@class, 'tgme_widget_message_sticker')]/@data-webp"
                )
                if sticker_div_list:
                    # TODO: add option to get sticker data from:
                    # message.xpath(".//i[contains(@class, 'tgme_widget_message_sticker')]/@style")[0]
                    type_ = "sticker"
                    urls.append(
                        ("photo", urljoin(original_url, sticker_div_list[0]))
                    )

                location_a_list = message.xpath(
                    ".//a[@class = 'tgme_widget_message_location_wrap']/@href"
                )
                if location_a_list:
                    type_ = "location"
                    urls.append(
                        ("link", urljoin(original_url, location_a_list[0]))
                    )

                audio_src_list = message.xpath(".//audio/@src")
                if audio_src_list:
                    # TODO: add duration to dataclass?
                    # duration = extract_text(
                    #     message.xpath(
                    #         ".//time[contains(@class, 'tgme_widget_message_voice_duration')]/text()"
                    #     )[0],
                    #     delimiter="",
                    # )
                    type_ = "audio"
                    urls.append(
                        ("audio", urljoin(original_url, audio_src_list[0]))
                    )

            document_class_list = message.xpath(
                ".//div[contains(@class, 'tgme_widget_message_document')]/@class"
            )
            if document_class_list:
                # TODO: get title, document type and other info
                type_ = "document"

            poll_div_list = message.xpath(
                ".//div[contains(@class, 'tgme_widget_message_poll')]"
            )
            if poll_div_list:
                # TODO: get other info
                type_ = "poll"

            photos_div_list = message.xpath(
                ".//a[contains(@class, 'tgme_widget_message_photo_wrap')]/@style"
            )
            if photos_div_list:
                urls.extend(
                    [
                        ("photo", urljoin(original_url, extract_bg_img(style)))
                        for style in photos_div_list
                    ]
                )
                type_ = "photo" if type_ is None else "multimedia"

            roundvideos_div_list = message.xpath(
                ".//video[contains(@class, 'tgme_widget_message_roundvideo')]/@src"
            )
            if roundvideos_div_list:
                # TODO: get video duration?
                urls.extend(
                    [
                        ("round-video", urljoin(original_url, url))
                        for url in roundvideos_div_list
                    ]
                )
                type_ = "round-video" if type_ is None else "multimedia"

            video_link_list = message.xpath(
                "//a[contains(@class, 'tgme_widget_message_video_player')]"
            )
            if video_link_list:
                type_ = "video" if type_ is None else "multimedia"
                videos_div_list = message.xpath(
                    ".//div[contains(@class, 'tgme_widget_message_video_wrap')]//video[contains(@class, 'tgme_widget_message_video')]/@src"
                )
                if videos_div_list:
                    # TODO: get video duration?
                    urls.extend(
                        [
                            ("video", urljoin(original_url, url))
                            for url in videos_div_list
                        ]
                    )

            reply_list = message.xpath(
                ".//a[contains(@class, 'tgme_widget_message_reply')]/@href"
            )
            if reply_list:
                reply_to_id = int(reply_list[0].split("/")[-1])

            a_preview_list = message.xpath(
                ".//a[contains(@class, 'tgme_widget_message_link_preview')]"
            )
            if a_preview_list:
                a_tag = a_preview_list[0]
                url_preview = a_tag.xpath("./@href")
                preview_url = url_preview[0] if url_preview else None
                image_preview = a_tag.xpath(
                    ".//i[contains(@class, 'link_preview_')]/@style"
                )
                preview_image_url = (
                    extract_bg_img(image_preview[0]) if image_preview else None
                )
                preview_site_name = (
                    extract_text(
                        a_tag.xpath(
                            ".//div[contains(@class, 'link_preview_site_name')]//text()"
                        )
                    )
                    or None
                )
                preview_title = (
                    extract_text(
                        a_tag.xpath(
                            ".//div[contains(@class, 'link_preview_title')]//text()"
                        )
                    )
                    or None
                )
                preview_description = (
                    extract_text(
                        a_tag.xpath(
                            ".//div[contains(@class, 'link_preview_description')]//text()"
                        )
                    )
                    or None
                )

            if text_div is not None:
                # TODO: parse spoilers?
                # TODO: how to know for which text the link is?
                if link_list := text_div.xpath(".//a/@href"):
                    urls.extend(
                        [
                            ("link", urljoin(original_url, url))
                            for url in link_list
                        ]
                    )

            a_fwd_list = message.xpath(
                ".//a[contains(@class, 'tgme_widget_message_forwarded_from_name')]"
            )
            if a_fwd_list:
                forwarded_author = extract_text(
                    a_fwd_list[0].xpath(".//text()")
                )
                forwarded_author_url = a_fwd_list[0].xpath("./@href")[0]

            if type_ is None:
                type_ = "text"

            for thumb_type in ("reply", "video", "roundvideo"):
                query = f".//i[contains(@class, 'tgme_widget_message_{thumb_type}_thumb')]/@style"
                urls.extend(
                    [
                        (
                            f"thumbnail-{thumb_type}",
                            urljoin(original_url, extract_bg_img(style)),
                        )
                        for style in message.xpath(query)
                    ]
                )

            # TODO: parse live location
            # TODO: parse poll
            # TODO: parse document/audio
            # TODO: parse document/other
        yield ChannelMessage(
            id=int(id_),
            created_at=created_at,
            type=type_,
            channel=channel,
            author=author,
            edited=edited,
            text=text,
            views=views,
            urls=urls,
            reply_to_id=reply_to_id,
            preview_url=preview_url,
            preview_image_url=preview_image_url,
            preview_site_name=preview_site_name,
            preview_title=preview_title,
            preview_description=preview_description,
            forwarded_author=forwarded_author,
            forwarded_author_url=forwarded_author_url,
        )


class ChannelScraper:
    def __init__(self, user_agent=f"tchan/{__version__}"):
        self.session = requests.Session()
        self.session.headers["User-Agent"] = user_agent

    def info(self, username_or_url):
        url = normalize_url(username_or_url)
        response = self.session.get(url)
        tree = document_fromstring(response.text)
        return parse_info(tree)

    def messages(self, username_or_url):
        "Get messages from a channel, paginating until it ends"
        url = normalize_url(username_or_url)

        last_captured_id = None
        while True:
            response = self.session.get(url)
            tree = document_fromstring(response.text)
            for message in parse_messages(url, tree):
                last_captured_id = message.id
                yield message
            next_page_url = tree.xpath("//link[@rel = 'prev']/@href")
            if not next_page_url:
                if last_captured_id is not None and message.id > 20:
                    # Telegram did not respond correctly, try again
                    url = (
                        normalize_url(username_or_url)
                        + f"?before={last_captured_id}"
                    )
                    continue
                break
            url = urljoin(url, next_page_url[0])

def main():
    import argparse
    import csv
    import json
    from pathlib import Path

    try:
        from loguru import logger
        from tqdm import tqdm
    except ImportError:
        print("Error - you muse install CLI dependencies with:")
        print("    pip install tchan[cli]")
        exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("csv_filename")
    parser.add_argument("username_or_url", nargs="+")
    args = parser.parse_args()
    # TODO: add option to limit messages (--max=N, --until=datetime, --after=datetime etc.)
    # TODO: implement `urls_format`: postgres_array, json, multiline
    usernames_or_urls = args.username_or_url
    filename = Path(args.csv_filename)
    if not filename.parent.exists():
        filename.parent.mkdir(parents=True)

    scraper = ChannelScraper()
    with filename.open(mode="w") as fobj:
        progress = tqdm(unit=" posts", unit_scale=True, dynamic_ncols=True)
        scrape_count, writer = 0, None
        for username_or_url in usernames_or_urls:
            username = normalize_url(username_or_url).replace(
                "https://t.me/s/", ""
            )
            progress.desc = f"Scraping {username}"
            try:
                for message in scraper.messages(username):
                    message = asdict(message)
                    message["urls"] = json.dumps(message["urls"])
                    if writer is None:
                        writer = csv.DictWriter(
                            fobj, fieldnames=list(message.keys())
                        )
                        writer.writeheader()
                    writer.writerow(message)
                    progress.update()

            except StopIteration:  # Group, bot or invalid username
                logger.error(
                    "Invalid username or not a public channel: {username}"
                )
                continue
            else:
                scrape_count += 1
            progress.desc = (
                f"Scraped {scrape_count} user{'s' if scrape_count > 1 else ''}"
            )
        progress.close()


if __name__ == "__main__":
    main()
