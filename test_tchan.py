import datetime

from lxml.html import document_fromstring

from tchan import (
    ChannelInfo,
    ChannelMessage,
    normalize_url,
    parse_info,
    parse_messages,
)

original_url = "https://t.me/s/tchantest"


def test_normalize_url():
    assert normalize_url("https://t.me/fulano") == "https://t.me/s/fulano"
    assert normalize_url("https://t.me/s/fulano") == "https://t.me/s/fulano"
    assert normalize_url("https://t.me/fulano/12345") == "https://t.me/s/fulano"
    assert (
        normalize_url("https://t.me/s/fulano/12345") == "https://t.me/s/fulano"
    )
    assert normalize_url("t.me/fulano") == "https://t.me/s/fulano"
    assert normalize_url("t.me/s/fulano") == "https://t.me/s/fulano"
    assert normalize_url("t.me/s/fulano/12345") == "https://t.me/s/fulano"
    assert normalize_url("fulano") == "https://t.me/s/fulano"
    assert normalize_url("@fulano") == "https://t.me/s/fulano"


def test_channel_info():
    html = """
        [...]
        <meta property="og:title" content="tchan&#39;s test channel 👍">
        <meta property="og:image" content="https://cdn1.telegram-cdn.org/file/pEJs58u1vQ4-YvOJ-6t1MAIcTPNIusLkfFzACh2CHzG-IOGGZVSKNsNIJhO-bkTdyAIabgzH7RqJBEjPLDWkJT7IYoQeCiDehrk1-KNRuXEgbCHMWDSxMuc9mOp-w3TJkfzLserjAsgwqVKE4fb0NouctjkVJHMcPkwxUVdoiEwEc6cUPP16fYQJfxKELtbBrfPpEha6Bdvfrhy2-6Sn3PPUx_krgiNduHJXXhc8zRcJt-YoOmX_McGV7EqZhEtDZHhRB2r441l4OJQzHjP7L-cA_y6g8cI1_hU7E8oLJJCoEdzHDrR2_z23MzjbHQ4F538BnqPEINvYBGJZP3h6Hg.jpg">
        <meta property="og:site_name" content="Telegram">
        <meta property="og:description" content="Test channel for tchan Python library/CLI">
        [...]
        <div class="tgme_channel_info_header_username"><a href="https://t.me/tchantest">@tchantest</a></div>
        [...]
        <div class="tgme_channel_info_counters"><div class="tgme_channel_info_counter"><span class="counter_value">1</span> <span class="counter_type">subscriber</span></div><div class="tgme_channel_info_counter"><span class="counter_value">3</span> <span class="counter_type">photos</span></div><div class="tgme_channel_info_counter"><span class="counter_value">2</span> <span class="counter_type">videos</span></div><div class="tgme_channel_info_counter"><span class="counter_value">4</span> <span class="counter_type">links</span></div></div>
        [...]
    """
    tree = document_fromstring(html)
    result = parse_info(tree)
    expected = ChannelInfo(
        username="tchantest",
        title="tchan's test channel 👍",
        image_url="https://cdn1.telegram-cdn.org/file/pEJs58u1vQ4-YvOJ-6t1MAIcTPNIusLkfFzACh2CHzG-IOGGZVSKNsNIJhO-bkTdyAIabgzH7RqJBEjPLDWkJT7IYoQeCiDehrk1-KNRuXEgbCHMWDSxMuc9mOp-w3TJkfzLserjAsgwqVKE4fb0NouctjkVJHMcPkwxUVdoiEwEc6cUPP16fYQJfxKELtbBrfPpEha6Bdvfrhy2-6Sn3PPUx_krgiNduHJXXhc8zRcJt-YoOmX_McGV7EqZhEtDZHhRB2r441l4OJQzHjP7L-cA_y6g8cI1_hU7E8oLJJCoEdzHDrR2_z23MzjbHQ4F538BnqPEINvYBGJZP3h6Hg.jpg",
        description="Test channel for tchan Python library/CLI",
        subscribers=1,
        photos=3,
        videos=2,
        links=4,
    )
    assert result == expected


def test_parse_service_message_channel_created():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap service_message js-widget_message" data-post="tchantest/1" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6MSwidCI6MTY3NzIyODczMywiaCI6ImYwZGZmMWI4YTI4ZmMwOTk4ZiJ9">
            <div class="tgme_widget_message_user">
              <a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <div class="tgme_widget_message_text js-message_text" dir="auto">Channel created
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/1"><time datetime="2023-02-24T07:26:49+00:00" class="time">07:26</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=1,
        created_at=datetime.datetime(
            2023, 2, 24, 7, 26, 49, tzinfo=datetime.timezone.utc
        ),
        type="service",
        channel="tchantest",
        urls=[],
        author=None,
        edited=False,
        text="Channel created",
        views=None,
    )
    assert result[0] == expected


def test_parse_service_message_pinned():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap service_message js-widget_message" data-post="tchantest/92" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6OTIsInQiOjE2NzcyNDEzNDMsImgiOiI4ZjQ2ZDQ2MTcyMGIzOWVmOTYifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <div class="tgme_widget_message_text js-message_text" dir="auto"><a class="tgme_widget_message_author_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a> pinned «<span class="tgme_widget_service_strong_text" dir="auto">Going to pin this message</span>»
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/92"><time datetime="2023-02-24T12:20:19+00:00" class="time">12:20</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=92,
        created_at=datetime.datetime(
            2023, 2, 24, 12, 20, 19, tzinfo=datetime.timezone.utc
        ),
        type="service",
        channel="tchantest",
        urls=[],
        author=None,
        edited=False,
        text="tchan's test channel👍pinned «Going to pin this message»",
        views=None,
    )
    assert result[0] == expected


def test_parse_multimedia_message():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/84" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6Ijg0ZyIsInQiOjE2NzcyNDEzNDMsImgiOiJkN2I0ZGFkYWUyYjRmY2ZlZjgifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <div class="tgme_widget_message_grouped_wrap js-message_grouped_wrap" data-margin-w="2" data-margin-h="2" style="width:453px;">
                <div class="tgme_widget_message_grouped js-message_grouped" style="padding-top:93.819%">
                  <div class="tgme_widget_message_grouped_layer js-message_grouped_layer" style="width:453px;height:425px">
                    <a class="tgme_widget_message_video_player grouped_media_wrap blured js-message_video_player" style="left:0px;top:0px;width:453px;height:254px;margin-right:0px;margin-bottom:2px;" data-ratio="1.7777777777778" href="https://t.me/tchantest/84?single">
                      <i class="tgme_widget_message_video_thumb" style="background-image:url('https://cdn1.telegram-cdn.org/file/nWyXAzTHX19MAA8oKaS4tcW-afBU7oOvCpQfVX-Z8l5dVuBeBUDZ5wVn0LRN5OIkwxbDAoSVuJiVm8BPt__9PML4K9rBmVcinjrLUtbNcqhx1WF-JpR_jd5FGQXQStSPYwgYyf460aoQsrVu48r-h4UGyuRLcnNoXytG-siQ_kOxpMArdeZXIQRzNW9eWHfO-IaIx78jqLdhcUaueZjkix91Ak35tPDdloQ7vhzDGqtpJQ1bI6YWVVP0gAm7AQdqcmkoNfFwXjh4uvxEAvsJxdSfMNJ3A1uKhqkm-_fVcbUBgBcJoPIjBBpJx5A3yorSMoMFCvne1QIvFdfjNbGZbg')"></i>
                      <div class="tgme_widget_message_video_wrap grouped_media js-message_video_wrap" style="left:0;right:0;top:-1px;bottom:0px;">
                        <video src="https://cdn1.telegram-cdn.org/file/bd7ceb0b41.mp4?token=FqRn4LGTlVsYQNCiPqd19TF0Z-EK6gWw__1F7os3qthEAdi8kkkrrWeUqJYCrNsv7OF80hlKUHUfKi_9PMsFbg28A8zONLdULTjmt256uaIBQqc3ieY_Js1kg8ezAIi5Y2tab_Z9dycZBrPQjARRoTVwLd9v_QrIQ7il3W1iXipnClgLZK4PxFjFOIhdYmEM_gAhxylo30BdpQFekkk5xCwNNTKmFjeaZTUQ_NNM1k3NGuKQo3SmrHUj4hK1xoKayOZxvB0oJIffTpMkHEBjs_j-tyi72uKmRz7my8ogBY0pHO-2Em5lDh-Li0rDGfHJ_NUssmwGqoToH-el_FZfZWA7juyZs_QNSkWABs0ijiVXDKZPKZKiOVQ0Uh8RtNs4UrNKp91GAVLLCb-C9TpW9SRlgMECG4yKWnXZ7nIsh_nhRNMk-aL0_Lehl0D4bRi1xMkXqtCu5B9pMS7MhIoNbg1sK7_4SJi3YRLugH_jiOGx3HhOP9HtBQZZTBZffb_d3vQQHNfXWEYUwP3t8iBwDrFL0qPwlT_1xMM57S6JlS3ApAEqqYFRxD6YBBFcJr3HMb2rinmL77iwCPtOirSeXFNaG0daSIaUn2jOMoDVH-MwVMBr6Oz_ESOWlqiGtHngUxKxgsbC9UxgvzcXXzHNelvl0z8isMf6oz0QqAntnWA" class="tgme_widget_message_video js-message_video" width="100%" height="100%"></video>
                      </div>
                      <div class="message_video_play js-message_video_play">
                      </div>
                      <time class="message_video_duration js-message_video_duration">0:27</time>
                      <div class="message_media_not_supported_wrap">
                        <div class="message_media_not_supported">
                          <div class="message_media_not_supported_label">This media is not supported in your browser
                          </div>
                          <span class="message_media_view_in_telegram">VIEW IN TELEGRAM</span>
                        </div>
                      </div>
                      </a><a class="tgme_widget_message_photo_wrap grouped_media_wrap blured js-message_photo" style="left:0px;top:256px;width:127px;height:169px;margin-right:2px;margin-bottom:0px;background-image:url('https://cdn1.telegram-cdn.org/file/CrsaR3dLCwSaTunI7l4nSUu5G7du7049yHXuZwbiOjAfSDEMrJaKiJ9-ly6RJOJf7wSYPGjpUppSBuqLkTbMIl_CMEpS_9nVLvNusCJTRXbhJbU4UFsTxiM89YyDE_9bapVEjoS9vhRS7qw1zSCbV2K42W3TZvvQ8scfiI2xiMIsRkw-YzpIVxbkzpeWz3-US6fi7DswlIobEgCG0uxmHdr6q2FEFOn9BCpfQHlrDqq8rCA9kBteMinAEkALObzktjJ76PMFWQZbQCcKIofW9oOThEJRAdFrRaho9PwBOQIcrSf_2MQmyqg8zA79k04ME76FsNNw3xr7xA160MHckA.jpg')" data-ratio="0.75" href="https://t.me/tchantest/85?single">
                      <div class="grouped_media_helper" style="top:0;bottom:0;left:67px;right:67px;">
                        <div class="tgme_widget_message_photo grouped_media" style="left:0;right:0;top:-1px;bottom:0px;">
                        </div>
                      </div>
                      </a><a class="tgme_widget_message_video_player grouped_media_wrap blured js-message_video_player" style="left:129px;top:256px;width:174px;height:169px;margin-right:2px;margin-bottom:0px;" data-ratio="0.5625" href="https://t.me/tchantest/86?single">
                      <i class="tgme_widget_message_video_thumb" style="background-image:url('https://cdn1.telegram-cdn.org/file/jFd1zyUf89Ze7MO2jtuFOuJXVJrYf9-QNmuE_f0x07Nwkx6KgVXhq71eAMiuTYhg1T9lmLA74NfOWgLwLaNk5H4OZYUtQBGrRrGeFaOcnRDcv9jOb23ZAjj6BHMDJ3bfFh_lmsAKQzQIuhJesbi3kBeioa4BeVYW4qjRYUmoKuRYpH6kr2eAalOQ_IYV8p0RxqGbhrJO3vKSYhwodxb3lYI-RKLDUrhSGQUy43hKEt1Epb0rwnpXnXsHcTrbo96O-bqfZ20A_wPqgzMyA13Xa7guojvXlRD2bpd-ezUYdwh9yBb636oqfkvTkaEI8rH4azIJxSB5eVlug5cN2wk97g')"></i>
                      <div class="tgme_widget_message_video_wrap grouped_media js-message_video_wrap" style="left:0;right:0;top:-71px;bottom:-70px;">
                        <video src="https://cdn1.telegram-cdn.org/file/e996ca12fa.mp4?token=KO0u7GXRUAGbO8QgNdwm-ZedWF5dNzcqm4VeQk_2XikjDahyMnyWKup0S9kyPO4piQqxDlK0yDsFa-myEr1LQPNnJdd1KqYUTiUGWgwI9d-9cA9d-J1U8mtiWDDiaLctgP73nFHrVNbpBopQELyGobP5ha5ofRzEC494a6QHkcKAakFRWlkMu2u2n_HAQZQhurOVvmJBW0pA_yMIv_lrVsHfmvjw-jGwd_dnou5l-158l_0i21I8jzjBMJ4bam9ayHgn3iEjw0uDcmmb-I9-i7Nz1vPQjRJs34_Qjyp6vDrawOGsOY0sAWT7r4lSpefK1Rdc0XQPwQgMY_izO_QfWw" class="tgme_widget_message_video js-message_video" width="100%" height="100%"></video>
                      </div>
                      <div class="message_video_play js-message_video_play">
                      </div>
                      <time class="message_video_duration js-message_video_duration">0:08</time>
                      <div class="message_media_not_supported_wrap">
                        <div class="message_media_not_supported">
                          <div class="message_media_not_supported_label">This media is not supported in your browser
                          </div>
                          <span class="message_media_view_in_telegram">VIEW IN TELEGRAM</span>
                        </div>
                      </div>
                      </a><a class="tgme_widget_message_photo_wrap grouped_media_wrap blured js-message_photo" style="left:305px;top:256px;width:148px;height:169px;margin-right:0px;margin-bottom:0px;background-image:url('https://cdn1.telegram-cdn.org/file/QMvda1Z9IET0DA4-jsfevuguTxnTpn6omRRA7gfRfYs6VCmxjsZdeX4R6k4n7rYe7skLclk-A1G7Dw4UuYzV5Ogj9KkYlLSsJD2x_WQDRqmUDauUWEAGa-JNACCFBH2zRJeFwb6OvAD6itpb05MbvyMVvsR18sw8Qe4VcPvODZmfKGxQ7ioslSsxTKoLz8KEAIcvPqVLkJKjkPVERS6u8QBSS-ZPOWu6RvJsS0_fS7oCTSfLjTmn3EfGlU3BvRAmNcVCQv7Jz-CPNBgXHUk5Bru05WNpsdaoCVfX9PzeDycLIoHm5S55H_TV9zocKvg_ZX0NVyLE_Em_wO7nbDwDRQ.jpg')" data-ratio="1.3333333333333" href="https://t.me/tchantest/87?single">
                      <div class="grouped_media_helper" style="left:0;right:0;top:43px;bottom:43px;">
                        <div class="tgme_widget_message_photo grouped_media" style="top:0;bottom:0;left:-39px;right:-39px;">
                        </div>
                      </div>
                    </a>
                  </div>
                </div>
              </div>
              <div class="tgme_widget_message_text js-message_text" dir="auto">
                <div class="tgme_widget_message_text js-message_text" dir="auto">Multiple videos and pictures
                </div>
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">436.6K</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/84"><time datetime="2023-02-24T11:01:46+00:00" class="time">11:01</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=84,
        created_at=datetime.datetime(
            2023, 2, 24, 11, 1, 46, tzinfo=datetime.timezone.utc
        ),
        type="multimedia",
        channel="tchantest",
        author=None,
        urls=[
            (
                "photo",
                "https://cdn1.telegram-cdn.org/file/CrsaR3dLCwSaTunI7l4nSUu5G7du7049yHXuZwbiOjAfSDEMrJaKiJ9-ly6RJOJf7wSYPGjpUppSBuqLkTbMIl_CMEpS_9nVLvNusCJTRXbhJbU4UFsTxiM89YyDE_9bapVEjoS9vhRS7qw1zSCbV2K42W3TZvvQ8scfiI2xiMIsRkw-YzpIVxbkzpeWz3-US6fi7DswlIobEgCG0uxmHdr6q2FEFOn9BCpfQHlrDqq8rCA9kBteMinAEkALObzktjJ76PMFWQZbQCcKIofW9oOThEJRAdFrRaho9PwBOQIcrSf_2MQmyqg8zA79k04ME76FsNNw3xr7xA160MHckA.jpg",
            ),
            (
                "photo",
                "https://cdn1.telegram-cdn.org/file/QMvda1Z9IET0DA4-jsfevuguTxnTpn6omRRA7gfRfYs6VCmxjsZdeX4R6k4n7rYe7skLclk-A1G7Dw4UuYzV5Ogj9KkYlLSsJD2x_WQDRqmUDauUWEAGa-JNACCFBH2zRJeFwb6OvAD6itpb05MbvyMVvsR18sw8Qe4VcPvODZmfKGxQ7ioslSsxTKoLz8KEAIcvPqVLkJKjkPVERS6u8QBSS-ZPOWu6RvJsS0_fS7oCTSfLjTmn3EfGlU3BvRAmNcVCQv7Jz-CPNBgXHUk5Bru05WNpsdaoCVfX9PzeDycLIoHm5S55H_TV9zocKvg_ZX0NVyLE_Em_wO7nbDwDRQ.jpg",
            ),
            (
                "video",
                "https://cdn1.telegram-cdn.org/file/bd7ceb0b41.mp4?token=FqRn4LGTlVsYQNCiPqd19TF0Z-EK6gWw__1F7os3qthEAdi8kkkrrWeUqJYCrNsv7OF80hlKUHUfKi_9PMsFbg28A8zONLdULTjmt256uaIBQqc3ieY_Js1kg8ezAIi5Y2tab_Z9dycZBrPQjARRoTVwLd9v_QrIQ7il3W1iXipnClgLZK4PxFjFOIhdYmEM_gAhxylo30BdpQFekkk5xCwNNTKmFjeaZTUQ_NNM1k3NGuKQo3SmrHUj4hK1xoKayOZxvB0oJIffTpMkHEBjs_j-tyi72uKmRz7my8ogBY0pHO-2Em5lDh-Li0rDGfHJ_NUssmwGqoToH-el_FZfZWA7juyZs_QNSkWABs0ijiVXDKZPKZKiOVQ0Uh8RtNs4UrNKp91GAVLLCb-C9TpW9SRlgMECG4yKWnXZ7nIsh_nhRNMk-aL0_Lehl0D4bRi1xMkXqtCu5B9pMS7MhIoNbg1sK7_4SJi3YRLugH_jiOGx3HhOP9HtBQZZTBZffb_d3vQQHNfXWEYUwP3t8iBwDrFL0qPwlT_1xMM57S6JlS3ApAEqqYFRxD6YBBFcJr3HMb2rinmL77iwCPtOirSeXFNaG0daSIaUn2jOMoDVH-MwVMBr6Oz_ESOWlqiGtHngUxKxgsbC9UxgvzcXXzHNelvl0z8isMf6oz0QqAntnWA",
            ),
            (
                "video",
                "https://cdn1.telegram-cdn.org/file/e996ca12fa.mp4?token=KO0u7GXRUAGbO8QgNdwm-ZedWF5dNzcqm4VeQk_2XikjDahyMnyWKup0S9kyPO4piQqxDlK0yDsFa-myEr1LQPNnJdd1KqYUTiUGWgwI9d-9cA9d-J1U8mtiWDDiaLctgP73nFHrVNbpBopQELyGobP5ha5ofRzEC494a6QHkcKAakFRWlkMu2u2n_HAQZQhurOVvmJBW0pA_yMIv_lrVsHfmvjw-jGwd_dnou5l-158l_0i21I8jzjBMJ4bam9ayHgn3iEjw0uDcmmb-I9-i7Nz1vPQjRJs34_Qjyp6vDrawOGsOY0sAWT7r4lSpefK1Rdc0XQPwQgMY_izO_QfWw",
            ),
            (
                "thumbnail-video",
                "https://cdn1.telegram-cdn.org/file/nWyXAzTHX19MAA8oKaS4tcW-afBU7oOvCpQfVX-Z8l5dVuBeBUDZ5wVn0LRN5OIkwxbDAoSVuJiVm8BPt__9PML4K9rBmVcinjrLUtbNcqhx1WF-JpR_jd5FGQXQStSPYwgYyf460aoQsrVu48r-h4UGyuRLcnNoXytG-siQ_kOxpMArdeZXIQRzNW9eWHfO-IaIx78jqLdhcUaueZjkix91Ak35tPDdloQ7vhzDGqtpJQ1bI6YWVVP0gAm7AQdqcmkoNfFwXjh4uvxEAvsJxdSfMNJ3A1uKhqkm-_fVcbUBgBcJoPIjBBpJx5A3yorSMoMFCvne1QIvFdfjNbGZbg",
            ),
            (
                "thumbnail-video",
                "https://cdn1.telegram-cdn.org/file/jFd1zyUf89Ze7MO2jtuFOuJXVJrYf9-QNmuE_f0x07Nwkx6KgVXhq71eAMiuTYhg1T9lmLA74NfOWgLwLaNk5H4OZYUtQBGrRrGeFaOcnRDcv9jOb23ZAjj6BHMDJ3bfFh_lmsAKQzQIuhJesbi3kBeioa4BeVYW4qjRYUmoKuRYpH6kr2eAalOQ_IYV8p0RxqGbhrJO3vKSYhwodxb3lYI-RKLDUrhSGQUy43hKEt1Epb0rwnpXnXsHcTrbo96O-bqfZ20A_wPqgzMyA13Xa7guojvXlRD2bpd-ezUYdwh9yBb636oqfkvTkaEI8rH4azIJxSB5eVlug5cN2wk97g",
            ),
        ],
        edited=False,
        text="Multiple videos and pictures",
        views=436_600,
    )
    assert result[0] == expected


def test_parse_service_message_channel_video_changed():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/82" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6ODIsInQiOjE2NzcyNDEzNDMsImgiOiJjZjI1MmYwNTRhODc2NjJkZTQifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <div class="tgme_widget_message_text js-message_text" dir="auto">+ &quot;Channel video changed&quot;
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">3.1M</span><span class="copyonly"> view</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/82"><time datetime="2023-02-24T10:15:33+00:00" class="time">10:15</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=82,
        created_at=datetime.datetime(
            2023, 2, 24, 10, 15, 33, tzinfo=datetime.timezone.utc
        ),
        type="text",
        channel="tchantest",
        author=None,
        urls=[],
        edited=False,
        text='+ "Channel video changed"',
        views=3_100_000,
    )
    assert result[0] == expected


def test_parse_service_message_channel_name_changed():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap service_message js-widget_message" data-post="tchantest/2" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6MiwidCI6MTY3NzIyODczMywiaCI6IjY3NzgxNzRhYTVkMDE4ZDM1YyJ9">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <div class="tgme_widget_message_text js-message_text" dir="auto">Channel name was changed to «<span class="tgme_widget_service_strong_text" dir="auto">tchan&#39;s test channel</span>»
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/2"><time datetime="2023-02-24T07:28:01+00:00" class="time">07:28</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=2,
        created_at=datetime.datetime(
            2023, 2, 24, 7, 28, 1, tzinfo=datetime.timezone.utc
        ),
        type="service",
        channel="tchantest",
        author=None,
        urls=[],
        edited=False,
        text="Channel name was changed to «tchan's test channel»",
        views=None,
    )
    assert result[0] == expected


def test_parse_service_message_channel_photo_updated():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap service_message service_message_photo js-widget_message" data-post="tchantest/3" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6MywidCI6MTY3NzIyODczMywiaCI6IjAwMmZiNGZkYjhjMTEzMjE2ZCJ9">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <a class="tgme_widget_message_service_photo" href="https://t.me/tchantest/3"><img src="https://cdn1.telegram-cdn.org/file/DL-kcK51w4o7tyr5QWQWK7YexgMdwiKIVYbDNbzB2qUtyk9uYfrKo0t19LY08bW4WTdmGpI9t0YQ2aU3RpsaWVk_4Q9QfjBIjaM894tj1r96LzJ8PGXOLkHd3w_KDciIw-AFmZBAKs5UIK6WU6PW1Nx1uh9e084u9rKJQtVu7EZLx1YCgxtx5R69qSKCamUbie0yqbaocYeevtymiMw6C_BeYwLZux6iMhoejvs6jyaQXiQLtm53xvAcqPKefzM0frCmDU1t5sllrHJD7L2iv52m9j27Kcyi-cu6detpDOwxdC2Be9CvsN4UXDOwvxiEl3TQSkrFKb06csVd85lEaQ.jpg"></a>
              <div class="tgme_widget_message_text js-message_text" dir="auto">Channel photo updated
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/3"><time datetime="2023-02-24T07:29:23+00:00" class="time">07:29</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=3,
        created_at=datetime.datetime(
            2023, 2, 24, 7, 29, 23, tzinfo=datetime.timezone.utc
        ),
        type="service",
        channel="tchantest",
        author=None,
        edited=False,
        text="Channel photo updated",
        views=None,
        urls=[
            (
                "photo",
                "https://cdn1.telegram-cdn.org/file/DL-kcK51w4o7tyr5QWQWK7YexgMdwiKIVYbDNbzB2qUtyk9uYfrKo0t19LY08bW4WTdmGpI9t0YQ2aU3RpsaWVk_4Q9QfjBIjaM894tj1r96LzJ8PGXOLkHd3w_KDciIw-AFmZBAKs5UIK6WU6PW1Nx1uh9e084u9rKJQtVu7EZLx1YCgxtx5R69qSKCamUbie0yqbaocYeevtymiMw6C_BeYwLZux6iMhoejvs6jyaQXiQLtm53xvAcqPKefzM0frCmDU1t5sllrHJD7L2iv52m9j27Kcyi-cu6detpDOwxdC2Be9CvsN4UXDOwvxiEl3TQSkrFKb06csVd85lEaQ.jpg",
            ),
        ],
    )
    assert result[0] == expected


def test_parse_text_message_multiline():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/62" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6NjIsInQiOjE2NzcyMjcwNjYsImgiOiIxNjZmNTNhM2Y2ZTkyMTJiZjUifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <div class="tgme_widget_message_text js-message_text" dir="auto">Bigger<br/>text<br/>message<br/>number<br/>34
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/62"><time datetime="2023-02-24T08:01:26+00:00" class="time">08:01</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=62,
        created_at=datetime.datetime(
            2023, 2, 24, 8, 1, 26, tzinfo=datetime.timezone.utc
        ),
        type="text",
        channel="tchantest",
        urls=[],
        author=None,
        edited=False,
        text="Bigger\ntext\nmessage\nnumber\n34",
        views=2,
    )
    assert result[0] == expected


def test_parse_forwarded_text_message():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/89" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6ODksInQiOjE2NzcyNDEzNDMsImgiOiJiYmQ1NDIwODhmMDBmNGNlNGYifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <div class="tgme_widget_message_forwarded_from accent_color">Forwarded from&nbsp;<a class="tgme_widget_message_forwarded_from_name" href="https://t.me/some_user"><span dir="auto">Some user</span></a>
              </div>
              <div class="tgme_widget_message_text js-message_text" dir="auto">;)
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/89"><time datetime="2023-02-24T12:13:31+00:00" class="time">12:13</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=89,
        created_at=datetime.datetime(
            2023, 2, 24, 12, 13, 31, tzinfo=datetime.timezone.utc
        ),
        type="text",
        channel="tchantest",
        urls=[],
        author=None,
        edited=False,
        text=";)",
        views=2,
        forwarded_author="Some user",
        forwarded_author_url="https://t.me/some_user",
    )
    assert result[0] == expected


def test_parse_text_message_signed_not_edited():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/79" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6NzksInQiOjE2NzcyMjcwNjYsImgiOiJjZDMwYjM2NzQ4ZmZjNGVkOTMifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <div class="tgme_widget_message_text js-message_text" dir="auto">Signed and not edited
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><span class="tgme_widget_message_from_author" dir="auto">Álvaro Justen</span>,&nbsp;<a class="tgme_widget_message_date" href="https://t.me/tchantest/79"><time datetime="2023-02-24T08:07:51+00:00" class="time">08:07</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=79,
        created_at=datetime.datetime(
            2023, 2, 24, 8, 7, 51, tzinfo=datetime.timezone.utc
        ),
        type="text",
        channel="tchantest",
        urls=[],
        author="Álvaro Justen",
        edited=False,
        text="Signed and not edited",
        views=2,
    )
    assert result[0] == expected


def test_parse_text_message_link_no_preview():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/24" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6MjQsInQiOjE2NzcyMjU1MzQsImgiOiIxZWVmYmU3NDM1MDE5ZDM0YWUifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <div class="tgme_widget_message_text js-message_text" dir="auto">This is a message with a link<br/><br/><a href="https://brasil.io/" target="_blank" rel="noopener">https://brasil.io/</a>
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta">edited &nbsp;<a class="tgme_widget_message_date" href="https://t.me/tchantest/24"><time datetime="2023-02-24T07:48:02+00:00" class="time">07:48</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=24,
        created_at=datetime.datetime(
            2023, 2, 24, 7, 48, 2, tzinfo=datetime.timezone.utc
        ),
        type="text",
        channel="tchantest",
        urls=[("link", "https://brasil.io/")],
        author=None,
        edited=True,
        text="This is a message with a link\nhttps://brasil.io/",
        views=2,
    )
    assert result[0] == expected


def test_parse_text_message_link_with_regular_preview():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/94" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6OTQsInQiOjE2NzcyNDY0NzYsImgiOiI4YWQ5M2ZjZTcwOGU1ODc1MjMifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <div class="tgme_widget_message_text js-message_text" dir="auto"><a href="https://agenciabrasil.ebc.com.br/justica/noticia/2022-08/operacao-guardioes-do-bioma-apreende-239-toneladas-de-minerio" target="_blank" rel="noopener">https://agenciabrasil.ebc.com.br/justica/noticia/2022-08/operacao-guardioes-do-bioma-apreende-239-toneladas-de-minerio</a>
              </div>
              <a class="tgme_widget_message_link_preview" href="https://agenciabrasil.ebc.com.br/justica/noticia/2022-08/operacao-guardioes-do-bioma-apreende-239-toneladas-de-minerio">
                <div class="link_preview_site_name accent_color" dir="auto">Agência Brasil
                </div>
                <i class="link_preview_image" style="background-image:url('https://cdn4.telegram-cdn.org/file/C2HB_eIeUYDV3yo1xut1cz6d06v6ITJW1fnuT7uihR5nIzUG9unDbq_cCbJag2TFdg7C_uJReq5lTcu9HZHI88el4u17YROLNW-rm4nLJCGc9d7L8Pfvkf4wLEx7pfY32k68VOXqg3XQ3Y0M1HgiEZyz9IIY9WvqImvvgwWG5f_czeIe8cC8h_X7JAkwUnoNsPlPf6qzqfV5QBswqQQF0PoRzYxd3L-uLAAreSvahHIFTnhLWQZCNQXxucYd9-Ct-w6voFkGtBkpF68Tx5i6QdTFbWp6WqR4LR7BeNTdTgeMGoZN1x46I_maRaeeHyqDRqD9cJLl08hMH6NLtMKbkw.jpg');padding-top:53.571428571429%"></i>
                <div class="link_preview_title" dir="auto">Operação Guardiões do Bioma apreende 23,9 toneladas de minério
                </div>
                <div class="link_preview_description" dir="auto">Ação contra o garimpo ilegal em Terra Indígena Yanomami durou um mês e resultou na prisão de 25 pessoas, apreensão de aeronaves e munições e em 115 autos de infração.
                </div>
              </a>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">1</span><span class="copyonly"> view</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/94"><time datetime="2023-02-24T13:47:38+00:00" class="time">13:47</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=94,
        created_at=datetime.datetime(
            2023, 2, 24, 13, 47, 38, tzinfo=datetime.timezone.utc
        ),
        type="text",
        channel="tchantest",
        urls=[
            (
                "link",
                "https://agenciabrasil.ebc.com.br/justica/noticia/2022-08/operacao-guardioes-do-bioma-apreende-239-toneladas-de-minerio",
            )
        ],
        author=None,
        edited=False,
        text="https://agenciabrasil.ebc.com.br/justica/noticia/2022-08/operacao-guardioes-do-bioma-apreende-239-toneladas-de-minerio",
        views=1,
        preview_url="https://agenciabrasil.ebc.com.br/justica/noticia/2022-08/operacao-guardioes-do-bioma-apreende-239-toneladas-de-minerio",
        preview_image_url="https://cdn4.telegram-cdn.org/file/C2HB_eIeUYDV3yo1xut1cz6d06v6ITJW1fnuT7uihR5nIzUG9unDbq_cCbJag2TFdg7C_uJReq5lTcu9HZHI88el4u17YROLNW-rm4nLJCGc9d7L8Pfvkf4wLEx7pfY32k68VOXqg3XQ3Y0M1HgiEZyz9IIY9WvqImvvgwWG5f_czeIe8cC8h_X7JAkwUnoNsPlPf6qzqfV5QBswqQQF0PoRzYxd3L-uLAAreSvahHIFTnhLWQZCNQXxucYd9-Ct-w6voFkGtBkpF68Tx5i6QdTFbWp6WqR4LR7BeNTdTgeMGoZN1x46I_maRaeeHyqDRqD9cJLl08hMH6NLtMKbkw.jpg",
        preview_site_name="Agência Brasil",
        preview_title="Operação Guardiões do Bioma apreende 23,9 toneladas de minério",
        preview_description="Ação contra o garimpo ilegal em Terra Indígena Yanomami durou um mês e resultou na prisão de 25 pessoas, apreensão de aeronaves e munições e em 115 autos de infração.",
    )
    assert result[0] == expected


def test_parse_text_message_link_with_right_preview():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/81" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6ODEsInQiOjE2NzcyMjcwNjYsImgiOiJlYTljMmVmOWY2ZTk1ZDdjOWQifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <div class="tgme_widget_message_text js-message_text" dir="auto">link with preview <a href="https://python.org/" target="_blank" rel="noopener">https://python.org/</a>
              </div>
              <a class="tgme_widget_message_link_preview" href="https://www.python.org/">
                <i class="link_preview_right_image" style="background-image:url('https://cdn4.telegram-cdn.org/file/mcgzW-avL5x2aBHAMw_8xb-MEiP5rCavDScU8vCkIIiYDgc202XMtQ4daRGRZVGU8uIHWwOyWa-Io-NeHkdrbj87eaHQCMgH6t6T4cVrW5GUwQDuFgQpE7-7XFXWc2I_ffYrhqgZUqHfdJNIMovjz7H1i-Gk45e-rlFKlpb1bUOaOd07ISTdr1OCUSAbs7z6oofThWpyE_2AxA5upuupuiocaeMINNxnwnJ_ate8S3gvnGMq81trLqLtcrUI9Dlo1Na4QemQPH7IOz-ra6DhlyiHm6fb_Q0pDOpLvmpI73jODW3H7QfBjp5htgN7dNMtxkGxw11-tCmVU6gRTIU-5w.jpg')"></i>
                <div class="link_preview_site_name accent_color" dir="auto">Python.org
                </div>
                <div class="link_preview_title" dir="auto">Welcome to Python.org
                </div>
                <div class="link_preview_description" dir="auto">The official home of the Python Programming Language
                </div>
              </a>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/81"><time datetime="2023-02-24T08:16:18+00:00" class="time">08:16</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=81,
        created_at=datetime.datetime(
            2023, 2, 24, 8, 16, 18, tzinfo=datetime.timezone.utc
        ),
        type="text",
        channel="tchantest",
        urls=[("link", "https://python.org/")],
        author=None,
        edited=False,
        text="link with preview\nhttps://python.org/",
        views=2,
        preview_url="https://www.python.org/",
        preview_image_url="https://cdn4.telegram-cdn.org/file/mcgzW-avL5x2aBHAMw_8xb-MEiP5rCavDScU8vCkIIiYDgc202XMtQ4daRGRZVGU8uIHWwOyWa-Io-NeHkdrbj87eaHQCMgH6t6T4cVrW5GUwQDuFgQpE7-7XFXWc2I_ffYrhqgZUqHfdJNIMovjz7H1i-Gk45e-rlFKlpb1bUOaOd07ISTdr1OCUSAbs7z6oofThWpyE_2AxA5upuupuiocaeMINNxnwnJ_ate8S3gvnGMq81trLqLtcrUI9Dlo1Na4QemQPH7IOz-ra6DhlyiHm6fb_Q0pDOpLvmpI73jODW3H7QfBjp5htgN7dNMtxkGxw11-tCmVU6gRTIU-5w.jpg",
        preview_site_name="Python.org",
        preview_title="Welcome to Python.org",
        preview_description="The official home of the Python Programming Language",
    )
    assert result[0] == expected


def test_parse_unsigned_text_message():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/6" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6NiwidCI6MTY3NzIyODczMywiaCI6IjEwNTM1NzcxNDVhZGQ2MzkwNiJ9">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">

              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <div class="tgme_widget_message_text js-message_text" dir="auto">Unsigned message
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/6"><time datetime="2023-02-24T07:30:39+00:00" class="time">07:30</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=6,
        created_at=datetime.datetime(
            2023, 2, 24, 7, 30, 39, tzinfo=datetime.timezone.utc
        ),
        type="text",
        channel="tchantest",
        urls=[],
        author=None,
        edited=False,
        text="Unsigned message",
        views=2,
    )
    assert result[0] == expected


def test_parse_emoji_message():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/7" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6NywidCI6MTY3NzIyODczMywiaCI6IjhiNTM4MDhjZDM4ZjA0NmU4YiJ9">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <div class="tgme_widget_message_text js-message_text" dir="auto"><i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i>
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/7"><time datetime="2023-02-24T07:30:53+00:00" class="time">07:30</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=7,
        created_at=datetime.datetime(
            2023, 2, 24, 7, 30, 53, tzinfo=datetime.timezone.utc
        ),
        type="text",
        channel="tchantest",
        author=None,
        edited=False,
        urls=[("photo", "https://telegram.org/img/emoji/40/F09F918D.png")],
        text="👍",
        views=2,
    )
    assert result[0] == expected


def test_parse_sticker_message():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap sticker_media no_bubble js-widget_message" data-post="tchantest/9" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6OSwidCI6MTY3NzIyODczMywiaCI6IjNiMjFiZDhmYjY1OWIwNGM3OSJ9">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <div class="message_media_not_supported_wrap media_not_supported_cont">
                <div class="message_media_not_supported">
                  <div class="message_media_not_supported_label">This media is not supported in your browser
                  </div>
                  <a href="https://t.me/tchantest/9" class="message_media_view_in_telegram">VIEW IN TELEGRAM</a>
                </div>
              </div>
              <div class="tgme_widget_message_sticker_wrap media_supported_cont"><i class="tgme_widget_message_sticker js-sticker_image" style="background-image:url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB2aWV3Qm94PSIwIDAgNTEyIDUxMiI+PGRlZnM+PGxpbmVhckdyYWRpZW50IGlkPSJnIiB4MT0iLTMwMCUiIHgyPSItMjAwJSIgeTE9IjAiIHkyPSIwIj48c3RvcCBvZmZzZXQ9Ii0xMCUiIHN0b3Atb3BhY2l0eT0iLjEiLz48c3RvcCBvZmZzZXQ9IjMwJSIgc3RvcC1vcGFjaXR5PSIuMDciLz48c3RvcCBvZmZzZXQ9IjcwJSIgc3RvcC1vcGFjaXR5PSIuMDciLz48c3RvcCBvZmZzZXQ9IjExMCUiIHN0b3Atb3BhY2l0eT0iLjEiLz48YW5pbWF0ZSBhdHRyaWJ1dGVOYW1lPSJ4MSIgZnJvbT0iLTMwMCUiIHRvPSIxMjAwJSIgZHVyPSIzcyIgcmVwZWF0Q291bnQ9ImluZGVmaW5pdGUiLz48YW5pbWF0ZSBhdHRyaWJ1dGVOYW1lPSJ4MiIgZnJvbT0iLTIwMCUiIHRvPSIxMzAwJSIgZHVyPSIzcyIgcmVwZWF0Q291bnQ9ImluZGVmaW5pdGUiLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cGF0aCBmaWxsPSJ1cmwoI2cpIiBkPSJNMzIzLDMyNGMtNDksMC05OSwwLTE0OSwwLTYsMC0zNSw0LTM5LDAtMy0yLDYtMjYsMC0yNiwwLDAtNiw0LTksMi03LTQsNywwLTcsMC03LDAtNy0zOC01LTQwLDEwLTksMTcsOSwxNyw5LDMsMC0yLTcsMC05LDQtMiw5LDIsMTMsMCwxMC01LTgtODYsNDgtOTMsMTAtMS0xMi0yOS0xMS0zMCwyLTEyLDI0LTIyLDIxLTM0LDEtMi00LTItNS00LDEtMSwzLDEsNCwwLDItMi02LTEzLTUtMTYsMS01LDktMTIsNy0xOC0yLTUtMTAsNS0xMCwxLDEtOCwzLTI3LDgtMzIsNC0zLDYsMSw5LDEsNSwwLDEyLTEzLDE1LTE2LDUtNCwwLDgsMSw4LDUsMCw3LTYsMTEtOSw0LTIsMTQtNywxMS00LDEsMS0xNSw4LTExLDgsNiwxLDctNywxMS03LDE4LTIsMzItNCw1NS0yLDksMCwxNCw1LDIwLDEwLDUsNCwxMyw1LDE4LDgsMjIsMTMsMjgsNTUsMjMsNzgtMiwxMi05LDI4LTE0LDM5LTIsNS0xNCwxNi0xMywxNiw3OSwxMSw5MiwxNSwxNDUsOTAsMTYsMjIsMjItOCwyMiwxNywwLDExLDUsMTAsOCwxOSwxLDMsMiwzMywwLDM1LTUsNS0xNjgsMC0xODgsMHoiLz48L3N2Zz4=');width:256px;" data-webp="https://cdn1.telegram-cdn.org/file/5b5c6e1325.webp?token=chQuhI8SVanorZnNJ_PTvHtJR1UOPC_cIjPNCVXhhG40BqJ9cpBCgrQy0NazQTCWO7bG_6JyNI4mFboxXSTcZJvATVgKwRTEkzFzeVen9a5AaZV36NUk9AWXUWFOaAX6jY4fKMQ3Sq6hicdTU4OjX4SvrwX501-pRHzw7b-dXMPwymHqMNwE-eVpiFu827y32eSOulEDWMvg2LMpmsIpks0b7fXcO-V-JvGwDvMsjVRy82406A5zElMjdD6lgBXZy5Hg79AyyVMJOprENkM0DY0evphw3gmq5G7YreJ9EcWIPX7K9skVfukCFxCxqjlHxV6T4aFGwxlZEJywBw_7pg">
                  <div style="padding-top:63.28125%">
                </div></i>
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/9"><time datetime="2023-02-24T07:31:06+00:00" class="time">07:31</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=9,
        created_at=datetime.datetime(
            2023, 2, 24, 7, 31, 6, tzinfo=datetime.timezone.utc
        ),
        type="sticker",
        channel="tchantest",
        author=None,
        edited=False,
        urls=[
            (
                "photo",
                "https://cdn1.telegram-cdn.org/file/5b5c6e1325.webp?token=chQuhI8SVanorZnNJ_PTvHtJR1UOPC_cIjPNCVXhhG40BqJ9cpBCgrQy0NazQTCWO7bG_6JyNI4mFboxXSTcZJvATVgKwRTEkzFzeVen9a5AaZV36NUk9AWXUWFOaAX6jY4fKMQ3Sq6hicdTU4OjX4SvrwX501-pRHzw7b-dXMPwymHqMNwE-eVpiFu827y32eSOulEDWMvg2LMpmsIpks0b7fXcO-V-JvGwDvMsjVRy82406A5zElMjdD6lgBXZy5Hg79AyyVMJOprENkM0DY0evphw3gmq5G7YreJ9EcWIPX7K9skVfukCFxCxqjlHxV6T4aFGwxlZEJywBw_7pg",
            ),
        ],
        text=None,
        views=2,
    )
    assert result[0] == expected


def test_parse_audio_document():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/12" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6MTIsInQiOjE2NzcyMjg3MzMsImgiOiI1MzYyYzQxMjExN2ZmZjJlYjEifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <a class="tgme_widget_message_document_wrap" href="https://t.me/tchantest/12">
                <div class="tgme_widget_message_document_icon accent_bg audio">
                </div>
                <div class="tgme_widget_message_document">
                  <div class="tgme_widget_message_document_title accent_color" dir="auto">AUD-20130329-WA0000
                  </div>
                  <div class="tgme_widget_message_document_extra" dir="auto">portadosfundos
                  </div>
                </div>
              </a>
              <div class="tgme_widget_message_text js-message_text" dir="auto">Povo hebreu
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/12"><time datetime="2023-02-24T07:33:58+00:00" class="time">07:33</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=12,
        created_at=datetime.datetime(
            2023, 2, 24, 7, 33, 58, tzinfo=datetime.timezone.utc
        ),
        type="document",
        channel="tchantest",
        author=None,
        edited=False,
        urls=[],
        text="Povo hebreu",
        views=2,
    )
    assert result[0] == expected


def test_parse_text_reply_to_video():
    html = """

        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/20" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6MjAsInQiOjE2NzcyMjU1MzQsImgiOiJjOWI2MGJhOWUyODY0YmMyZjMifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <a class="tgme_widget_message_reply" href="https://t.me/tchantest/19" ><i class="tgme_widget_message_reply_thumb" style="background-image:url('https://cdn1.telegram-cdn.org/file/nWyXAzTHX19MAA8oKaS4tcW-afBU7oOvCpQfVX-Z8l5dVuBeBUDZ5wVn0LRN5OIkwxbDAoSVuJiVm8BPt__9PML4K9rBmVcinjrLUtbNcqhx1WF-JpR_jd5FGQXQStSPYwgYyf460aoQsrVu48r-h4UGyuRLcnNoXytG-siQ_kOxpMArdeZXIQRzNW9eWHfO-IaIx78jqLdhcUaueZjkix91Ak35tPDdloQ7vhzDGqtpJQ1bI6YWVVP0gAm7AQdqcmkoNfFwXjh4uvxEAvsJxdSfMNJ3A1uKhqkm-_fVcbUBgBcJoPIjBBpJx5A3yorSMoMFCvne1QIvFdfjNbGZbg')"></i>
                <div class="tgme_widget_message_author accent_color">
                  <span class="tgme_widget_message_author_name" dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span>
                </div>
                <div class="tgme_widget_message_metatext js-message_reply_text" dir="auto">Video
                </div>
              </a>
              <div class="tgme_widget_message_text js-message_text" dir="auto">Reply to a video (not recorded in telegram)
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/20"><time datetime="2023-02-24T07:38:31+00:00" class="time">07:38</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=20,
        created_at=datetime.datetime(
            2023, 2, 24, 7, 38, 31, tzinfo=datetime.timezone.utc
        ),
        type="text",
        channel="tchantest",
        author=None,
        edited=False,
        urls=[
            (
                "thumbnail-reply",
                "https://cdn1.telegram-cdn.org/file/nWyXAzTHX19MAA8oKaS4tcW-afBU7oOvCpQfVX-Z8l5dVuBeBUDZ5wVn0LRN5OIkwxbDAoSVuJiVm8BPt__9PML4K9rBmVcinjrLUtbNcqhx1WF-JpR_jd5FGQXQStSPYwgYyf460aoQsrVu48r-h4UGyuRLcnNoXytG-siQ_kOxpMArdeZXIQRzNW9eWHfO-IaIx78jqLdhcUaueZjkix91Ak35tPDdloQ7vhzDGqtpJQ1bI6YWVVP0gAm7AQdqcmkoNfFwXjh4uvxEAvsJxdSfMNJ3A1uKhqkm-_fVcbUBgBcJoPIjBBpJx5A3yorSMoMFCvne1QIvFdfjNbGZbg",
            ),
        ],
        text="Reply to a video (not recorded in telegram)",
        views=2,
        reply_to_id=19,
    )
    assert result[0] == expected


def test_parse_poll():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/11" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6MTEsInQiOjE2NzcyMjg3MzMsImgiOiJhNjFlZGVlYmVjZDE0MjNhOWEifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <div class="tgme_widget_message_poll js-poll">
                <div class="tgme_widget_message_poll_question">Let&#39;s do a quick poll quizz mode
                </div>
                <div class="tgme_widget_message_poll_type">Anonymous Quiz
                </div>
                <a class="tgme_widget_message_poll_options" href="https://t.me/tchantest/11">  <div class="tgme_widget_message_poll_option">
                    <div class="tgme_widget_message_poll_option_percent">0%
                    </div>
                    <div class="tgme_widget_message_poll_option_value">
                      <div class="tgme_widget_message_poll_option_text">Opt1
                      </div>
                      <div class="tgme_widget_message_poll_option_bar accent_bg" style="width:0%">
                      </div>
                    </div>
                    </div>  <div class="tgme_widget_message_poll_option">
                    <div class="tgme_widget_message_poll_option_percent">0%
                    </div>
                    <div class="tgme_widget_message_poll_option_value">
                      <div class="tgme_widget_message_poll_option_text">Opt2
                      </div>
                      <div class="tgme_widget_message_poll_option_bar accent_bg" style="width:0%">
                      </div>
                    </div>
                    </div>  <div class="tgme_widget_message_poll_option">
                    <div class="tgme_widget_message_poll_option_percent">0%
                    </div>
                    <div class="tgme_widget_message_poll_option_value">
                      <div class="tgme_widget_message_poll_option_text">Opt3
                      </div>
                      <div class="tgme_widget_message_poll_option_bar accent_bg" style="width:0%">
                      </div>
                    </div>
                </div></a>
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_voters">0</span><span class="copyonly"> voter</span><span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/11"><time datetime="2023-02-24T07:32:23+00:00" class="time">07:32</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=11,
        created_at=datetime.datetime(
            2023, 2, 24, 7, 32, 23, tzinfo=datetime.timezone.utc
        ),
        type="poll",
        channel="tchantest",
        author=None,
        edited=False,
        urls=[],
        text=None,
        views=2,
    )
    assert result[0] == expected


def test_parse_photo_single():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/16" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6MTYsInQiOjE2NzcyMjg3MzMsImgiOiJlNmFhYmVmNTZiYzcyZGNmNDEifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <a class="tgme_widget_message_photo_wrap blured 5172795381250108682 1204385278_456240394" href="https://t.me/tchantest/16" style="width:450px;background-image:url('https://cdn1.telegram-cdn.org/file/AqX5QJmpXiolNyLq3Aq8-4eqTHJtpueMZqcszNrmWGgUt4I4iaH-CPxmqR-QPdgdzVtE_rX8cpCOgeAOsN9Ais72d79W-56VIEOdCenSvm5YuK9nHh-faVhkQAnTnw3DtOobB6G3jbZRDvHdjhlxyojAwvNXWGSyfIzmaEPq9C_ut2VXo5gJk8ZOAUi5OfxIRf7UVSyNyXbfKXZPwDdok7uTLp1gTaLacKNdcHN0Wdo0NCj2phCO_Hhv5zOqvJkC_Ct-3d3vv_aa03gOWTXzGtq1sbrlynldi9zVtWn6TOsNBGzDGSWqcm7WUe1QbddpBeS7VQWqyih2fKmhKLr5wA.jpg')">
                <div class="tgme_widget_message_photo" style="width:75%;padding-top:133.33333333333%">
                </div>
              </a>
              <div class="tgme_widget_message_text js-message_text" dir="auto">Picture by telegram camera
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/16"><time datetime="2023-02-24T07:35:28+00:00" class="time">07:35</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=16,
        created_at=datetime.datetime(
            2023, 2, 24, 7, 35, 28, tzinfo=datetime.timezone.utc
        ),
        type="photo",
        channel="tchantest",
        author=None,
        edited=False,
        urls=[
            (
                "photo",
                "https://cdn1.telegram-cdn.org/file/AqX5QJmpXiolNyLq3Aq8-4eqTHJtpueMZqcszNrmWGgUt4I4iaH-CPxmqR-QPdgdzVtE_rX8cpCOgeAOsN9Ais72d79W-56VIEOdCenSvm5YuK9nHh-faVhkQAnTnw3DtOobB6G3jbZRDvHdjhlxyojAwvNXWGSyfIzmaEPq9C_ut2VXo5gJk8ZOAUi5OfxIRf7UVSyNyXbfKXZPwDdok7uTLp1gTaLacKNdcHN0Wdo0NCj2phCO_Hhv5zOqvJkC_Ct-3d3vv_aa03gOWTXzGtq1sbrlynldi9zVtWn6TOsNBGzDGSWqcm7WUe1QbddpBeS7VQWqyih2fKmhKLr5wA.jpg",
            ),
        ],
        text="Picture by telegram camera",
        views=2,
    )
    assert result[0] == expected


def test_parse_message_weird_preview():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="CamaradosDeputados/7334" data-view="eyJjIjotMTEzMzE1MDExMiwicCI6NzMzNCwidCI6MTY3NzI0ODE4NywiaCI6IjVmMTA0ZDZhODcwOGM4MWUzNyJ9">
            <div class="tgme_widget_message_user"><a href="https://t.me/CamaradosDeputados"><i class="tgme_widget_message_user_photo bgcolor3" data-content="C"><img src="https://cdn1.telegram-cdn.org/file/ZTzJAvUdTMa373EIK-DI2yu4HrknmAMK2n2HQhXLLc2USZDisX08CsefGXbecXuVSQINOWDMY6E2GK1OOLz6PT34Fli2D7NXvmu2uFjfDaHxoKCjl997lvdxg74pAxbjSoTykmkVj2HG7y30I1WVPeZpUq9iuYAkLahGQZiV8gig6Miy4CBnOijhNbgVQCLspDgnX6mZx0Ao26ZclmoTLgrxRXjWHCkuNbXpwZE3XCx6SF0kcMOAq9d_4CcdzCtkEOvt1HlXjvUR8iMc4m86mwdIDPXw4tYPNDcKY6foYmQQLSBRol9vET2X8FBEWh2vFeQ4aW0hozWceLQudH3KQw.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/CamaradosDeputados"><span dir="auto">Câmara dos Deputados</span></a>
              </div>
              <div class="tgme_widget_message_text js-message_text" dir="auto">_<br/><br/><b><i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/E29C8D.png')"><b>✍️</b></i> CÂMARA APROVA<br/>_<br/><br/><br/></b><i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F94B8.png')"><b>🔸</b></i> <a href="http://bit.ly/3Tq1C4G" target="_blank" rel="noopener" onclick="return confirm('Open this link?\n\n'+this.href);">Projeto que aumenta penas para crimes sexuais contra crianças<br/></a><a href="?q=%23Puni%C3%A7%C3%A3o_ampliada">#Punição_ampliada</a><br/><i><i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F97B3.png')"><b>🗳</b></i></i> Opine sobre esta proposta <a href="http://bit.ly/3PCX1vn" target="_blank" rel="noopener" onclick="return confirm('Open this link?\n\n'+this.href);">clicando aqui&#33;<br/></a>____<br/><br/><i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F94B8.png')"><b>🔸</b></i><a href="http://bit.ly/3tkdScB" target="_blank" rel="noopener" onclick="return confirm('Open this link?\n\n'+this.href);">Projeto que facilita corte ou poda de árvore quando houver risco de acidente.<br/></a><a href="?q=%23Poda_de_%C3%A1rvores">#Poda_de_árvores</a><br/><i><i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F97B3.png')"><b>🗳</b></i></i> Opine sobre esta proposta <a href="http://bit.ly/3A1c4c4" target="_blank" rel="noopener" onclick="return confirm('Open this link?\n\n'+this.href);">clicando aqui&#33;<br/></a>____<br/><br/><i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F94B8.png')"><b>🔸</b></i><a href="http://bit.ly/3A3EoKS" target="_blank" rel="noopener" onclick="return confirm('Open this link?\n\n'+this.href);">Proposta que susta resoluções da Aneel sobre tarifas de transmissão</a>.<br/><a href="?q=%23Tarifas_de_transmiss%C3%A3o">#Tarifas_de_transmissão</a><br/><i><i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F97B3.png')"><b>🗳</b></i></i> Opine sobre esta proposta <a href="http://bit.ly/3zWxOpw" target="_blank" rel="noopener" onclick="return confirm('Open this link?\n\n'+this.href);">clicando aqui&#33;<br/><br/><br/></a>____<br/><br/><i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F93AC.png')"><b>📬</b></i> Convide seus contatos do WhatsApp a conhecerem nosso canal <a href="https://bit.ly/2UBmLNC" target="_blank" rel="noopener" onclick="return confirm('Open this link?\n\n'+this.href);">clicando aqui&#33; <br/></a>____
              </div>
              <a class="tgme_widget_message_link_preview" href="http://bit.ly/3Tq1C4G">
                <div class="link_preview_site_name accent_color" dir="auto">Portal da Câmara dos Deputados
                </div>
                <div class="link_preview_title" dir="auto">Câmara aprova projeto que aumenta penas para crimes sexuais contra crianças; acompanhe - Notícias
                </div>
              </a>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">1.2K</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta">edited &nbsp;<a class="tgme_widget_message_date" href="https://t.me/CamaradosDeputados/7334"><time datetime="2022-11-09T22:43:54+00:00" class="time">22:43</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages("https://t.me/s/CamaradosDeputados", tree))
    expected = ChannelMessage(
        id=7334,
        created_at=datetime.datetime(
            2022, 11, 9, 22, 43, 54, tzinfo=datetime.timezone.utc
        ),
        type="text",
        channel="CamaradosDeputados",
        author=None,
        edited=True,
        urls=[
            ("photo", "https://telegram.org/img/emoji/40/E29C8D.png"),
            ("link", "http://bit.ly/3Tq1C4G"),
            (
                "link",
                "https://t.me/s/CamaradosDeputados?q=%23Puni%C3%A7%C3%A3o_ampliada",
            ),
            ("link", "http://bit.ly/3PCX1vn"),
            ("link", "http://bit.ly/3tkdScB"),
            (
                "link",
                "https://t.me/s/CamaradosDeputados?q=%23Poda_de_%C3%A1rvores",
            ),
            ("link", "http://bit.ly/3A1c4c4"),
            ("link", "http://bit.ly/3A3EoKS"),
            (
                "link",
                "https://t.me/s/CamaradosDeputados?q=%23Tarifas_de_transmiss%C3%A3o",
            ),
            ("link", "http://bit.ly/3zWxOpw"),
            ("link", "https://bit.ly/2UBmLNC"),
        ],
        text="_\n✍️\nCÂMARA APROVA\n_\n🔸\nProjeto que aumenta penas para crimes sexuais contra crianças\n#Punição_ampliada\n🗳\nOpine sobre esta proposta\nclicando aqui!\n____\n🔸\nProjeto que facilita corte ou poda de árvore quando houver risco de acidente.\n#Poda_de_árvores\n🗳\nOpine sobre esta proposta\nclicando aqui!\n____\n🔸\nProposta que susta resoluções da Aneel sobre tarifas de transmissão\n.\n#Tarifas_de_transmissão\n🗳\nOpine sobre esta proposta\nclicando aqui!\n____\n📬\nConvide seus contatos do WhatsApp a conhecerem nosso canal\nclicando aqui!\n____",
        views=1200,
        preview_url="http://bit.ly/3Tq1C4G",
        preview_image_url=None,
        preview_site_name="Portal da Câmara dos Deputados",
        preview_title="Câmara aprova projeto que aumenta penas para crimes sexuais contra crianças; acompanhe - Notícias",
        preview_description=None,
    )
    assert result[0] == expected


def test_parse_video_big():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="some_random_user/5343" data-view="eyJjIjotMTI3MzQ2NTU4OSwicCI6NTM0MywidCI6MTY3NzI0NjkxNSwiaCI6Ijg3Yjc5NTg4YWNiMDI0ODY5OCJ9">
            <div class="tgme_widget_message_user"><a href="https://t.me/some_random_user"><i class="tgme_widget_message_user_photo bgcolor4" data-content="J"><img src="https://cdn1.telegram-cdn.org/file/fbv-0M0ELNAnq0eo-yMCMCqT3GkbDs76Zi7N9ZN3_LJR-tvBSc6NDfl9mqBaqEAvAwGAYRgtRhiLuUitz8ZUWCRilfZGRUQH3T5zVUrb2c2wz--E0OwMZm9cY77RCJnFQys0Egu1rkneAaCjYiH9DkmLLaFuwE2za4uT4jK3BKx-hVyQr44RCSb097nTnpz2ErVjr7clxeaxPl4X_1lV-ycYn3bkQ_TpXz_2wY-iN-HwWm_hdCbu2SMrcNID6y7C0XXN5QmMOYTRfcjBsKmMXZ6drsCAKbxcELy9kt5tXqoUzpgPcraYflvG_54PRebr_6ApoGkDI68uzGnRWD4Wqg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/some_random_user"><span dir="auto">Blah</span></a>
              </div>
              <a class="tgme_widget_message_video_player not_supported js-message_video_player" href="https://t.me/some_random_user/5343"><i class="tgme_widget_message_video_thumb" style="background-image:url('https://cdn1.telegram-cdn.org/file/HyfobRUDoAxInyfbDVXk1q13pW97NtZN0TYuraxfsJLPps5R14DRXfT1DN2qZkAg4UIpu4RE0frU5LJLK3Y9oWyDgw3Y-Jg92EghLSe0Wmb6dMqCFwoz2CISl_hAeNgDksSQ5i_feURS-NzwXJRHeHwqz1funqsyNkdC5irHPSglylhsf3ZdEZMA4b1XqYrU3Zz4IgT3pLz0HcPSHcxHSyRAGjmb6vFbUYr-qThcvTD7HGXdb6gVRhV3bQyzo8xS9d2Vxho2j735Rxnr5qaprcef883AEuYuDSD31Anok_s6cvOz0jurCG8jbtonkSN9omsub5oyLrvT0H2ZQ4Gx3g')"></i>
                <div class="tgme_widget_message_video_wrap" style="width:704px;padding-top:133.33333333333%">
                </div>
                <div class="message_video_play js-message_video_play">
                </div>
                <time class="message_video_duration js-message_video_duration">0:52</time>
                <div class="message_media_not_supported_wrap">
                  <div class="message_media_not_supported">
                    <div class="message_media_not_supported_label">Media is too big
                    </div>
                    <span class="message_media_view_in_telegram">VIEW IN TELEGRAM</span>
                  </div>
              </div></a>
              <div class="tgme_widget_message_text js-message_text" dir="auto">some text</div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">436.6K</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/some_random_user/5343"><time datetime="2023-01-30T23:30:40+00:00" class="time">23:30</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=5343,
        created_at=datetime.datetime(
            2023, 1, 30, 23, 30, 40, tzinfo=datetime.timezone.utc
        ),
        type="video",
        channel="some_random_user",
        author=None,
        edited=False,
        urls=[
            (
                "thumbnail-video",
                "https://cdn1.telegram-cdn.org/file/HyfobRUDoAxInyfbDVXk1q13pW97NtZN0TYuraxfsJLPps5R14DRXfT1DN2qZkAg4UIpu4RE0frU5LJLK3Y9oWyDgw3Y-Jg92EghLSe0Wmb6dMqCFwoz2CISl_hAeNgDksSQ5i_feURS-NzwXJRHeHwqz1funqsyNkdC5irHPSglylhsf3ZdEZMA4b1XqYrU3Zz4IgT3pLz0HcPSHcxHSyRAGjmb6vFbUYr-qThcvTD7HGXdb6gVRhV3bQyzo8xS9d2Vxho2j735Rxnr5qaprcef883AEuYuDSD31Anok_s6cvOz0jurCG8jbtonkSN9omsub5oyLrvT0H2ZQ4Gx3g",
            ),
        ],
        text="some text",
        views=436600,
    )
    assert result[0] == expected


def test_parse_video_single():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/18" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6MTgsInQiOjE2NzcyMjg3MzMsImgiOiJhZGU3MTk4NDBjMDIyMjAxM2IifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <a class="tgme_widget_message_video_player blured js-message_video_player" href="https://t.me/tchantest/18"><i class="tgme_widget_message_video_thumb" style="background-image:url('https://cdn1.telegram-cdn.org/file/WiZBMqAIrM0sjmV7tKxjJQ3BcyP04k0bU3i1_kCI_cipeYNV2EgXyUIZ8Jii-7BMgdpGH9HKFCY8NuzsnvpYToh3PJdSdd4aOwSrYvu8uGQgogharMY-8IjAdcFNQh0stJ7r1-3mjJCT-1SojXo1LOBCt-sX7PI9woHjvqPFDDJyv9-xNbEgwWYMuKUyCA6Z1aKsEAz0wIDzLil4IXze3_neSQRkSlqWUnCGV_JoPy-qQuJd_6do_AnJMaLwlDcFBYAzZ-sX1kJC03qWhtjHUy9uaG9j8z23C_RcSlhWPTYPQi5t0x1HQXRWm-kaASMrghIIg9HFSu4MdCLOb8IgIA')"></i>
                <video src="https://cdn1.telegram-cdn.org/file/61dc623809.mp4?token=K5rf-tYZuK-hwjpm2Aa8NLNZI54LnZSlUftpmFaAjXdqeUtO0xfykZx8zfupPs7TYNYHMTDKJcmfoDs66q2bTsAk0d1kwrwZrArAGYOWBnJmTDualrn2gIQ8_VPKEQccf_k_sGyzGcbsCs9rkdlOTWMUQXOxoKDQ12X2hdnPONoehz0KAR_nH-W0lGKGUuxbUhu8yFVZGuu9JLFSp5dLprKNy9HYAJeh8D7yM3lZ7GmIG3ck5GLdjeYzRFx96sn0NviOl8H7kHcoDOCv_CkppMpXWninC8yboJUsmPISjfwQOiDD9ZOE2wZb7TN0zYSAHDFEy0Ga1msxs6f1j7Wjyw" class="tgme_widget_message_video blured js-message_video_blured" width="100%" height="100%" muted></video>
                <div class="tgme_widget_message_video_wrap" style="width:720px;padding-top:133.33333333333%">
                  <video src="https://cdn1.telegram-cdn.org/file/61dc623809.mp4?token=K5rf-tYZuK-hwjpm2Aa8NLNZI54LnZSlUftpmFaAjXdqeUtO0xfykZx8zfupPs7TYNYHMTDKJcmfoDs66q2bTsAk0d1kwrwZrArAGYOWBnJmTDualrn2gIQ8_VPKEQccf_k_sGyzGcbsCs9rkdlOTWMUQXOxoKDQ12X2hdnPONoehz0KAR_nH-W0lGKGUuxbUhu8yFVZGuu9JLFSp5dLprKNy9HYAJeh8D7yM3lZ7GmIG3ck5GLdjeYzRFx96sn0NviOl8H7kHcoDOCv_CkppMpXWninC8yboJUsmPISjfwQOiDD9ZOE2wZb7TN0zYSAHDFEy0Ga1msxs6f1j7Wjyw" class="tgme_widget_message_video js-message_video" width="100%" height="100%"></video>
                </div>
                <div class="message_video_play js-message_video_play">
                </div>
                <time class="message_video_duration js-message_video_duration">0:06</time>
                <div class="message_media_not_supported_wrap">
                  <div class="message_media_not_supported">
                    <div class="message_media_not_supported_label">This media is not supported in your browser
                    </div>
                    <span class="message_media_view_in_telegram">VIEW IN TELEGRAM</span>
                  </div>
              </div></a>
              <div class="tgme_widget_message_text js-message_text" dir="auto">Video by telegram camera
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/18"><time datetime="2023-02-24T07:36:49+00:00" class="time">07:36</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=18,
        created_at=datetime.datetime(
            2023, 2, 24, 7, 36, 49, tzinfo=datetime.timezone.utc
        ),
        type="video",
        channel="tchantest",
        author=None,
        edited=False,
        urls=[
            (
                "video",
                "https://cdn1.telegram-cdn.org/file/61dc623809.mp4?token=K5rf-tYZuK-hwjpm2Aa8NLNZI54LnZSlUftpmFaAjXdqeUtO0xfykZx8zfupPs7TYNYHMTDKJcmfoDs66q2bTsAk0d1kwrwZrArAGYOWBnJmTDualrn2gIQ8_VPKEQccf_k_sGyzGcbsCs9rkdlOTWMUQXOxoKDQ12X2hdnPONoehz0KAR_nH-W0lGKGUuxbUhu8yFVZGuu9JLFSp5dLprKNy9HYAJeh8D7yM3lZ7GmIG3ck5GLdjeYzRFx96sn0NviOl8H7kHcoDOCv_CkppMpXWninC8yboJUsmPISjfwQOiDD9ZOE2wZb7TN0zYSAHDFEy0Ga1msxs6f1j7Wjyw",
            ),
            (
                "thumbnail-video",
                "https://cdn1.telegram-cdn.org/file/WiZBMqAIrM0sjmV7tKxjJQ3BcyP04k0bU3i1_kCI_cipeYNV2EgXyUIZ8Jii-7BMgdpGH9HKFCY8NuzsnvpYToh3PJdSdd4aOwSrYvu8uGQgogharMY-8IjAdcFNQh0stJ7r1-3mjJCT-1SojXo1LOBCt-sX7PI9woHjvqPFDDJyv9-xNbEgwWYMuKUyCA6Z1aKsEAz0wIDzLil4IXze3_neSQRkSlqWUnCGV_JoPy-qQuJd_6do_AnJMaLwlDcFBYAzZ-sX1kJC03qWhtjHUy9uaG9j8z23C_RcSlhWPTYPQi5t0x1HQXRWm-kaASMrghIIg9HFSu4MdCLOb8IgIA",
            ),
        ],
        text="Video by telegram camera",
        views=2,
    )
    assert result[0] == expected


def test_parse_video_single_2():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/19" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6MTksInQiOjE2NzcyMjg3MzMsImgiOiI2MTkzM2QxY2Y3OWJkY2UzMDYifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <a class="tgme_widget_message_video_player js-message_video_player" href="https://t.me/tchantest/19"><i class="tgme_widget_message_video_thumb" style="background-image:url('https://cdn1.telegram-cdn.org/file/nWyXAzTHX19MAA8oKaS4tcW-afBU7oOvCpQfVX-Z8l5dVuBeBUDZ5wVn0LRN5OIkwxbDAoSVuJiVm8BPt__9PML4K9rBmVcinjrLUtbNcqhx1WF-JpR_jd5FGQXQStSPYwgYyf460aoQsrVu48r-h4UGyuRLcnNoXytG-siQ_kOxpMArdeZXIQRzNW9eWHfO-IaIx78jqLdhcUaueZjkix91Ak35tPDdloQ7vhzDGqtpJQ1bI6YWVVP0gAm7AQdqcmkoNfFwXjh4uvxEAvsJxdSfMNJ3A1uKhqkm-_fVcbUBgBcJoPIjBBpJx5A3yorSMoMFCvne1QIvFdfjNbGZbg')"></i>
                <div class="tgme_widget_message_video_wrap" style="width:1280px;padding-top:56.25%">
                  <video src="https://cdn1.telegram-cdn.org/file/bd7ceb0b41.mp4?token=FqRn4LGTlVsYQNCiPqd19TF0Z-EK6gWw__1F7os3qthEAdi8kkkrrWeUqJYCrNsv7OF80hlKUHUfKi_9PMsFbg28A8zONLdULTjmt256uaIBQqc3ieY_Js1kg8ezAIi5Y2tab_Z9dycZBrPQjARRoTVwLd9v_QrIQ7il3W1iXipnClgLZK4PxFjFOIhdYmEM_gAhxylo30BdpQFekkk5xCwNNTKmFjeaZTUQ_NNM1k3NGuKQo3SmrHUj4hK1xoKayOZxvB0oJIffTpMkHEBjs_j-tyi72uKmRz7my8ogBY0pHO-2Em5lDh-Li0rDGfHJ_NUssmwGqoToH-el_FZfZWA7juyZs_QNSkWABs0ijiVXDKZPKZKiOVQ0Uh8RtNs4UrNKp91GAVLLCb-C9TpW9SRlgMECG4yKWnXZ7nIsh_nhRNMk-aL0_Lehl0D4bRi1xMkXqtCu5B9pMS7MhIoNbg1sK7_4SJi3YRLugH_jiOGx3HhOP9HtBQZZTBZffb_d3vQQHNfXWEYUwP3t8iBwDrFL0qPwlT_1xMM57S6JlS3ApAEqqYFRxD6YBBFcJr3HMb2rinmL77iwCPtOirSeXFNaG0daSIaUn2jOMoDVH-MwVMBr6Oz_ESOWlqiGtHngUxKxgsbC9UxgvzcXXzHNelvl0z8isMf6oz0QqAntnWA" class="tgme_widget_message_video js-message_video" width="100%" height="100%"></video>
                </div>
                <div class="message_video_play js-message_video_play">
                </div>
                <time class="message_video_duration js-message_video_duration">0:27</time>
                <div class="message_media_not_supported_wrap">
                  <div class="message_media_not_supported">
                    <div class="message_media_not_supported_label">This media is not supported in your browser
                    </div>
                    <span class="message_media_view_in_telegram">VIEW IN TELEGRAM</span>
                  </div>
              </div></a>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/19"><time datetime="2023-02-24T07:38:13+00:00" class="time">07:38</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=19,
        created_at=datetime.datetime(
            2023, 2, 24, 7, 38, 13, tzinfo=datetime.timezone.utc
        ),
        type="video",
        channel="tchantest",
        author=None,
        edited=False,
        urls=[
            (
                "video",
                "https://cdn1.telegram-cdn.org/file/bd7ceb0b41.mp4?token=FqRn4LGTlVsYQNCiPqd19TF0Z-EK6gWw__1F7os3qthEAdi8kkkrrWeUqJYCrNsv7OF80hlKUHUfKi_9PMsFbg28A8zONLdULTjmt256uaIBQqc3ieY_Js1kg8ezAIi5Y2tab_Z9dycZBrPQjARRoTVwLd9v_QrIQ7il3W1iXipnClgLZK4PxFjFOIhdYmEM_gAhxylo30BdpQFekkk5xCwNNTKmFjeaZTUQ_NNM1k3NGuKQo3SmrHUj4hK1xoKayOZxvB0oJIffTpMkHEBjs_j-tyi72uKmRz7my8ogBY0pHO-2Em5lDh-Li0rDGfHJ_NUssmwGqoToH-el_FZfZWA7juyZs_QNSkWABs0ijiVXDKZPKZKiOVQ0Uh8RtNs4UrNKp91GAVLLCb-C9TpW9SRlgMECG4yKWnXZ7nIsh_nhRNMk-aL0_Lehl0D4bRi1xMkXqtCu5B9pMS7MhIoNbg1sK7_4SJi3YRLugH_jiOGx3HhOP9HtBQZZTBZffb_d3vQQHNfXWEYUwP3t8iBwDrFL0qPwlT_1xMM57S6JlS3ApAEqqYFRxD6YBBFcJr3HMb2rinmL77iwCPtOirSeXFNaG0daSIaUn2jOMoDVH-MwVMBr6Oz_ESOWlqiGtHngUxKxgsbC9UxgvzcXXzHNelvl0z8isMf6oz0QqAntnWA",
            ),
            (
                "thumbnail-video",
                "https://cdn1.telegram-cdn.org/file/nWyXAzTHX19MAA8oKaS4tcW-afBU7oOvCpQfVX-Z8l5dVuBeBUDZ5wVn0LRN5OIkwxbDAoSVuJiVm8BPt__9PML4K9rBmVcinjrLUtbNcqhx1WF-JpR_jd5FGQXQStSPYwgYyf460aoQsrVu48r-h4UGyuRLcnNoXytG-siQ_kOxpMArdeZXIQRzNW9eWHfO-IaIx78jqLdhcUaueZjkix91Ak35tPDdloQ7vhzDGqtpJQ1bI6YWVVP0gAm7AQdqcmkoNfFwXjh4uvxEAvsJxdSfMNJ3A1uKhqkm-_fVcbUBgBcJoPIjBBpJx5A3yorSMoMFCvne1QIvFdfjNbGZbg",
            ),
        ],
        text=None,
        views=2,
    )
    assert result[0] == expected


def test_parse_round_video_single():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap roundvideo_media no_bubble js-widget_message" data-post="tchantest/17" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6MTcsInQiOjE2NzcyMjg3MzMsImgiOiJlNTVlYTY4ZGEyNzY5MzlhODIifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <div class="tgme_widget_message_roundvideo_player js-message_roundvideo_player">
                <div class="tgme_widget_message_roundvideo_wrap">
                  <i class="tgme_widget_message_roundvideo_thumb" style="background-image:url('https://cdn1.telegram-cdn.org/file/U9Z-cXN1H4Y4JdCGNLPCaw8Y_4idAGdFDGqOMSS20fsGBN0OWrzYo-rtvGIgex8IkoAGGjqz2DduF369l5kY_jGB1zd7NpE9rqgSnB1hhUVFmxWqhP3bzsyTjJRABWJns176vCa_Jn8CEjHFddu39ONkG4Hyqc7wGDA6eOOMFF2pATNxePd-Jg056jTn79In9byN7cKk5Rlkt2hkY02vlaee_eokRInwNRQShvJ59Xdv0gEQV27DpSbjFvc4Ci_66unLiu3aWWA50etg5CbB2nmtSfLSs7ujGBteh5Aw9z0HjB4BVw3eNbZVrDKBUTe_5eFw6XE4RKwRnJ8LL4TPuA')"></i>
                  <video class="tgme_widget_message_roundvideo js-message_roundvideo" src="https://cdn1.telegram-cdn.org/file/68145c80a1.mp4?token=Asgm3ihYDp5WkmfxRXtMximu8cGDQy4Y2UIeZ3JmSNpRz-oDSsXbORc8H4V4oaR4LkaIEFfPz82hrRD1Fvu2wNDljkcCVbxwa0D5iD_sfhWKTDK3Hfy1Fu1hQPZG0b4-1rEkNIfRJp8T_H0nW6Rej80Nl8I8xZAINfHAe0ibS6Qs5R4IudWG4ULL3NRmJLzGDM92YlqVlkEzwvLB9au1G0jczynEbJ7qn5npIxQYPPIBzZehLtZHAXqp_cnq6moGUL6mAfK1tOPqN13wVfizhtv2XHy8WqvaEVxZMTWFyMu64nPc1aB1EGsfvdgSdpV-pENMcsH5ihLEbwfCTbQPFw" width="100%" height="100%" preload muted autoplay loop playsinline></video>
                  <div class="tgme_widget_message_roundvideo_muted">
                  </div>
                  <div class="tgme_widget_message_roundvideo_border">
                  </div>
                </div>
                <div class="message_media_not_supported_wrap js-message_roundvideo_not_supported">
                  <div class="message_media_not_supported">
                    <div class="message_media_not_supported_label">This media is not supported in your browser
                    </div>
                    <a href="https://t.me/tchantest/17" class="message_media_view_in_telegram">VIEW IN TELEGRAM</a>
                  </div>
                </div>
                <svg class="tgme_widget_message_roundvideo_progress_wrap" viewPort="0 0 256 256">
                <circle class="tgme_widget_message_roundvideo_progress js-message_roundvideo_progress" r="126.5" cx="50%" cy="50%" fill="transparent" stroke-dasharray="794.82294135822" stroke-dashoffset="0" data-rd="3"></circle>
                </svg>
                <div class="tgme_widget_message_roundvideo_play js-message_roundvideo_play">
                </div>
                <time class="tgme_widget_message_roundvideo_duration js-message_roundvideo_duration">0:05</time>
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/17"><time datetime="2023-02-24T07:35:45+00:00" class="time">07:35</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=17,
        created_at=datetime.datetime(
            2023, 2, 24, 7, 35, 45, tzinfo=datetime.timezone.utc
        ),
        type="round-video",
        channel="tchantest",
        author=None,
        edited=False,
        urls=[
            (
                "round-video",
                "https://cdn1.telegram-cdn.org/file/68145c80a1.mp4?token=Asgm3ihYDp5WkmfxRXtMximu8cGDQy4Y2UIeZ3JmSNpRz-oDSsXbORc8H4V4oaR4LkaIEFfPz82hrRD1Fvu2wNDljkcCVbxwa0D5iD_sfhWKTDK3Hfy1Fu1hQPZG0b4-1rEkNIfRJp8T_H0nW6Rej80Nl8I8xZAINfHAe0ibS6Qs5R4IudWG4ULL3NRmJLzGDM92YlqVlkEzwvLB9au1G0jczynEbJ7qn5npIxQYPPIBzZehLtZHAXqp_cnq6moGUL6mAfK1tOPqN13wVfizhtv2XHy8WqvaEVxZMTWFyMu64nPc1aB1EGsfvdgSdpV-pENMcsH5ihLEbwfCTbQPFw",
            ),
            (
                "thumbnail-roundvideo",
                "https://cdn1.telegram-cdn.org/file/U9Z-cXN1H4Y4JdCGNLPCaw8Y_4idAGdFDGqOMSS20fsGBN0OWrzYo-rtvGIgex8IkoAGGjqz2DduF369l5kY_jGB1zd7NpE9rqgSnB1hhUVFmxWqhP3bzsyTjJRABWJns176vCa_Jn8CEjHFddu39ONkG4Hyqc7wGDA6eOOMFF2pATNxePd-Jg056jTn79In9byN7cKk5Rlkt2hkY02vlaee_eokRInwNRQShvJ59Xdv0gEQV27DpSbjFvc4Ci_66unLiu3aWWA50etg5CbB2nmtSfLSs7ujGBteh5Aw9z0HjB4BVw3eNbZVrDKBUTe_5eFw6XE4RKwRnJ8LL4TPuA",
            ),
        ],
        text=None,
        views=2,
    )
    assert result[0] == expected


def test_parse_photo_multiple():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/14" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6IjE0ZyIsInQiOjE2NzcyMjg3MzMsImgiOiI0ZGVkZTQyN2M3ZGVmNGIzODYifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <div class="tgme_widget_message_grouped_wrap js-message_grouped_wrap" data-margin-w="2" data-margin-h="2" style="width:453px;">
                <div class="tgme_widget_message_grouped js-message_grouped" style="padding-top:47.682%">
                  <div class="tgme_widget_message_grouped_layer js-message_grouped_layer" style="width:453px;height:216px">
                    <a class="tgme_widget_message_photo_wrap grouped_media_wrap blured js-message_photo" style="left:0px;top:0px;width:288px;height:216px;margin-right:2px;margin-bottom:0px;background-image:url('https://cdn1.telegram-cdn.org/file/QMvda1Z9IET0DA4-jsfevuguTxnTpn6omRRA7gfRfYs6VCmxjsZdeX4R6k4n7rYe7skLclk-A1G7Dw4UuYzV5Ogj9KkYlLSsJD2x_WQDRqmUDauUWEAGa-JNACCFBH2zRJeFwb6OvAD6itpb05MbvyMVvsR18sw8Qe4VcPvODZmfKGxQ7ioslSsxTKoLz8KEAIcvPqVLkJKjkPVERS6u8QBSS-ZPOWu6RvJsS0_fS7oCTSfLjTmn3EfGlU3BvRAmNcVCQv7Jz-CPNBgXHUk5Bru05WNpsdaoCVfX9PzeDycLIoHm5S55H_TV9zocKvg_ZX0NVyLE_Em_wO7nbDwDRQ.jpg')" data-ratio="1.3333333333333" href="https://t.me/tchantest/14?single">
                      <div class="grouped_media_helper" style="top:0;bottom:0;left:82px;right:83px;">
                        <div class="tgme_widget_message_photo grouped_media" style="top:0;bottom:0;left:0px;right:0px;">
                        </div>
                      </div>
                      </a><a class="tgme_widget_message_photo_wrap grouped_media_wrap blured js-message_photo" style="left:290px;top:0px;width:163px;height:216px;margin-right:0px;margin-bottom:0px;background-image:url('https://cdn1.telegram-cdn.org/file/CrsaR3dLCwSaTunI7l4nSUu5G7du7049yHXuZwbiOjAfSDEMrJaKiJ9-ly6RJOJf7wSYPGjpUppSBuqLkTbMIl_CMEpS_9nVLvNusCJTRXbhJbU4UFsTxiM89YyDE_9bapVEjoS9vhRS7qw1zSCbV2K42W3TZvvQ8scfiI2xiMIsRkw-YzpIVxbkzpeWz3-US6fi7DswlIobEgCG0uxmHdr6q2FEFOn9BCpfQHlrDqq8rCA9kBteMinAEkALObzktjJ76PMFWQZbQCcKIofW9oOThEJRAdFrRaho9PwBOQIcrSf_2MQmyqg8zA79k04ME76FsNNw3xr7xA160MHckA.jpg')" data-ratio="0.75" href="https://t.me/tchantest/15?single">
                      <div class="grouped_media_helper" style="top:0;bottom:0;left:145px;right:146px;">
                        <div class="tgme_widget_message_photo grouped_media" style="left:0;right:0;top:-1px;bottom:-1px;">
                        </div>
                      </div>
                    </a>
                  </div>
                </div>
              </div>
              <div class="tgme_widget_message_text js-message_text" dir="auto">
                <div class="tgme_widget_message_text js-message_text" dir="auto">Multiple pics
                </div>
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/14"><time datetime="2023-02-24T07:34:20+00:00" class="time">07:34</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=14,
        created_at=datetime.datetime(
            2023, 2, 24, 7, 34, 20, tzinfo=datetime.timezone.utc
        ),
        type="photo",
        channel="tchantest",
        author=None,
        edited=False,
        urls=[
            (
                "photo",
                "https://cdn1.telegram-cdn.org/file/QMvda1Z9IET0DA4-jsfevuguTxnTpn6omRRA7gfRfYs6VCmxjsZdeX4R6k4n7rYe7skLclk-A1G7Dw4UuYzV5Ogj9KkYlLSsJD2x_WQDRqmUDauUWEAGa-JNACCFBH2zRJeFwb6OvAD6itpb05MbvyMVvsR18sw8Qe4VcPvODZmfKGxQ7ioslSsxTKoLz8KEAIcvPqVLkJKjkPVERS6u8QBSS-ZPOWu6RvJsS0_fS7oCTSfLjTmn3EfGlU3BvRAmNcVCQv7Jz-CPNBgXHUk5Bru05WNpsdaoCVfX9PzeDycLIoHm5S55H_TV9zocKvg_ZX0NVyLE_Em_wO7nbDwDRQ.jpg",
            ),
            (
                "photo",
                "https://cdn1.telegram-cdn.org/file/CrsaR3dLCwSaTunI7l4nSUu5G7du7049yHXuZwbiOjAfSDEMrJaKiJ9-ly6RJOJf7wSYPGjpUppSBuqLkTbMIl_CMEpS_9nVLvNusCJTRXbhJbU4UFsTxiM89YyDE_9bapVEjoS9vhRS7qw1zSCbV2K42W3TZvvQ8scfiI2xiMIsRkw-YzpIVxbkzpeWz3-US6fi7DswlIobEgCG0uxmHdr6q2FEFOn9BCpfQHlrDqq8rCA9kBteMinAEkALObzktjJ76PMFWQZbQCcKIofW9oOThEJRAdFrRaho9PwBOQIcrSf_2MQmyqg8zA79k04ME76FsNNw3xr7xA160MHckA.jpg",
            ),
        ],
        text="Multiple pics",
        views=2,
    )
    assert result[0] == expected


def test_parse_location_message():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/10" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6MTAsInQiOjE2NzcyMjg3MzMsImgiOiI2NDNjNTQ5Zjk1NGM4MzY4ZDgifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">

              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <a class="tgme_widget_message_location_wrap" href="https://maps.google.com/maps?q=-23.930587176407,-44.086305367818&ll=-23.930587176407,-44.086305367818&z=16">
                <div class="tgme_widget_message_location" style="background-image:url('https://static-maps.yandex.ru/1.x/?l=map&ll=-44.086305367818,-23.930587176407&z=15&size=600,300&scale=1.5&pt=-44.086305367818,-23.930587176407,comma&lang=en_US')">
                </div>
              </a>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/10"><time datetime="2023-02-24T07:31:38+00:00" class="time">07:31</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=10,
        created_at=datetime.datetime(
            2023, 2, 24, 7, 31, 38, tzinfo=datetime.timezone.utc
        ),
        type="location",
        channel="tchantest",
        author=None,
        edited=False,
        urls=[
            (
                "link",
                "https://maps.google.com/maps?q=-23.930587176407,-44.086305367818&ll=-23.930587176407,-44.086305367818&z=16",
            ),
        ],
        text=None,
        views=2,
    )
    assert result[0] == expected


def test_parse_location_message_2():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/83" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6ODMsInQiOjE2NzcyNDEzNDMsImgiOiI4MjZkZjFhYmM2NDc5NzgzZWQifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <a class="tgme_widget_message_location_wrap" href="https://maps.google.com/maps?q=-23.532363086523,-46.689620092745&ll=-23.532363086523,-46.689620092745&z=16">
                <div class="tgme_widget_message_location" style="background-image:url('https://static-maps.yandex.ru/1.x/?l=map&ll=-46.689620092745,-23.532363086523&z=15&size=600,300&scale=1.5&pt=-46.689620092745,-23.532363086523,comma&lang=en_US')">
                </div>
              </a>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">1</span><span class="copyonly"> view</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/83"><time datetime="2023-02-24T11:01:22+00:00" class="time">11:01</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=83,
        created_at=datetime.datetime(
            2023, 2, 24, 11, 1, 22, tzinfo=datetime.timezone.utc
        ),
        type="location",
        channel="tchantest",
        author=None,
        edited=False,
        urls=[
            (
                "link",
                "https://maps.google.com/maps?q=-23.532363086523,-46.689620092745&ll=-23.532363086523,-46.689620092745&z=16",
            ),
        ],
        text=None,
        views=1,
    )
    assert result[0] == expected


def test_parse_location_message_3():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/88" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6ODgsInQiOjE2NzcyNDEzNDMsImgiOiIxZTIwZmFmMzY2ZDM1NmFhNDUifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <a class="tgme_widget_message_location_wrap" href="https://maps.google.com/maps?q=-23.531972140424,-46.689076113848&ll=-23.531972140424,-46.689076113848&z=16">
                <div class="tgme_widget_message_location" style="background-image:url('https://static-maps.yandex.ru/1.x/?l=map&ll=-46.689076113848,-23.531972140424&z=15&size=600,300&scale=1.5&pt=-46.689076113848,-23.531972140424,comma&lang=en_US')">
                </div>
              </a>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/88"><time datetime="2023-02-24T11:23:40+00:00" class="time">11:23</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=88,
        created_at=datetime.datetime(
            2023, 2, 24, 11, 23, 40, tzinfo=datetime.timezone.utc
        ),
        type="location",
        channel="tchantest",
        author=None,
        edited=False,
        urls=[
            (
                "link",
                "https://maps.google.com/maps?q=-23.531972140424,-46.689076113848&ll=-23.531972140424,-46.689076113848&z=16",
            ),
        ],
        text=None,
        views=2,
    )
    assert result[0] == expected


def test_parse_audio_message():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/13" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6MTMsInQiOjE2NzcyMjg3MzMsImgiOiI4YTgyMWYwY2NiZTkxODFmNzcifQ">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <a class="tgme_widget_message_voice_player js-message_voice_player" href="https://t.me/tchantest/13">
                <audio class="tgme_widget_message_voice js-message_voice" src="https://cdn1.telegram-cdn.org/file/29881a3f30.ogg?token=RPh7-yUn9te932hRlzltMAmWTgmmAzD_PswWMJnmCZSfQQ63SfT5jfT_IpSq71gXP0d5F_G3fZLc1mxLuPR_NFSBVncAk7hvT5086hIQJfHX8qoE8VW-714sWoGTqVv6l35yS7V8_hCkt4KD2kW3F_5K2MPJ6yKPHBB4VzvlLmrwUoVVTPPOl2NJypUtDdN2fwFj7TkeZYHu0jrtKGrynmmBOp36SHpks7c9bkkL8HcaHhlzZXCBzibbWh0IM895baESbOimQrxnUwuTE9gv_VHGa_EMiwBD71p_NyHYPfpgNxGi1TPCVzJSO5QVPXDBZ3MSHoYI4COLZMt_4wwx1A" data-ogg width="100%" data-waveform="0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,15,19,31,31,31,31,31,31,31,31,31,31,31,31,28,17,15,18,21,0,17,4,10,2,0,0,0,0,0,0,0,0,0"></audio>
                <div class="tgme_widget_message_voice_play accent_bghover">
                </div>
                <div class="tgme_widget_message_voice_wrap">
                  <div class="tgme_widget_message_voice_progress_wrap js-message_voice_progress_wrap">
                    <div class="tgme_widget_message_voice_progress_bg">
                      <div class="bar"><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:4.516%;"></s><s style="height:42.581%;"></s><s style="height:84.516%;"></s><s style="height:100%;"></s><s style="height:100%;"></s><s style="height:100%;"></s><s style="height:100%;"></s><s style="height:100%;"></s><s style="height:100%;"></s><s style="height:96.129%;"></s><s style="height:60.645%;"></s><s style="height:54.194%;"></s><s style="height:40.645%;"></s><s style="height:35.484%;"></s><s style="height:24.516%;"></s><s style="height:3.871%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s>
                      </div>
                    </div>
                    <div class="tgme_widget_message_voice_progress js-message_voice_progress">
                      <div class="bar"><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:4.516%;"></s><s style="height:42.581%;"></s><s style="height:84.516%;"></s><s style="height:100%;"></s><s style="height:100%;"></s><s style="height:100%;"></s><s style="height:100%;"></s><s style="height:100%;"></s><s style="height:100%;"></s><s style="height:96.129%;"></s><s style="height:60.645%;"></s><s style="height:54.194%;"></s><s style="height:40.645%;"></s><s style="height:35.484%;"></s><s style="height:24.516%;"></s><s style="height:3.871%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s><s style="height:0%;"></s>
                      </div>
                    </div>
                  </div>
                  <time class="tgme_widget_message_voice_duration js-message_voice_duration">0:01</time>
                </div>
              </a>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><a class="tgme_widget_message_date" href="https://t.me/tchantest/13"><time datetime="2023-02-24T07:34:05+00:00" class="time">07:34</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=13,
        created_at=datetime.datetime(
            2023, 2, 24, 7, 34, 5, tzinfo=datetime.timezone.utc
        ),
        type="audio",
        channel="tchantest",
        author=None,
        edited=False,
        urls=[
            (
                "audio",
                "https://cdn1.telegram-cdn.org/file/29881a3f30.ogg?token=RPh7-yUn9te932hRlzltMAmWTgmmAzD_PswWMJnmCZSfQQ63SfT5jfT_IpSq71gXP0d5F_G3fZLc1mxLuPR_NFSBVncAk7hvT5086hIQJfHX8qoE8VW-714sWoGTqVv6l35yS7V8_hCkt4KD2kW3F_5K2MPJ6yKPHBB4VzvlLmrwUoVVTPPOl2NJypUtDdN2fwFj7TkeZYHu0jrtKGrynmmBOp36SHpks7c9bkkL8HcaHhlzZXCBzibbWh0IM895baESbOimQrxnUwuTE9gv_VHGa_EMiwBD71p_NyHYPfpgNxGi1TPCVzJSO5QVPXDBZ3MSHoYI4COLZMt_4wwx1A",
            ),
        ],
        text=None,
        views=2,
    )
    assert result[0] == expected


def test_parse_signed_edited_text_message():
    html = """
        <div class="tgme_widget_message_wrap js-widget_message_wrap">
          <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="tchantest/5" data-view="eyJjIjotMTU5MTUzNzY3NCwicCI6NSwidCI6MTY3NzIyODczMywiaCI6ImUwMWY5ZDU2YjkyZWNiODIyOSJ9">
            <div class="tgme_widget_message_user"><a href="https://t.me/tchantest"><i class="tgme_widget_message_user_photo bgcolor6" data-content="t"><img src="https://cdn1.telegram-cdn.org/file/dWVU3pm8LUqzTdgkSFjWttTn3owWaD3gkmwu463Q3ZlBMTAv9glTIDa8bm-MvvjRbkf32cEp91B81vhC-GMcU7kCNimccSBj3pw2RvhfvlKqbeUicH9tiKAtcKDsT12fJbto9h65ErIi5B3NxkKxmjrZ12YppA7FZc7D6e6nYbSlUClZxYXtpesZktIxNJeWuvoyKMOTsDUkSDJ4gZ__Rio3M9HUEjFGga56F3o8RLZae8ouJmtoCIiFEoDwb41SNqijR0a4K3yZb4p1ZMJAEF-sD9mw38usMhHze95WXUqZ2DzK9-u4Mftzd9GEr_Hrbpw_-aaN4DKEc5-OxoyLNg.jpg"></i></a>
            </div>
            <div class="tgme_widget_message_bubble">
              <i class="tgme_widget_message_bubble_tail">
                <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
                <g fill="none">
                <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
                <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
                <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
                <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
                </g>
                </svg>
              </i>
              <div class="tgme_widget_message_author accent_color"><a class="tgme_widget_message_owner_name" href="https://t.me/tchantest"><span dir="auto">tchan&#39;s test channel <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F918D.png')"><b>👍</b></i></span></a>
              </div>
              <div class="tgme_widget_message_text js-message_text" dir="auto">Hello&#33; Signed and edited message
              </div>
              <div class="tgme_widget_message_footer compact js-message_footer">
                <div class="tgme_widget_message_info short js-message_info">
                  <span class="tgme_widget_message_views">2</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"><span class="tgme_widget_message_from_author" dir="auto">Álvaro Justen</span>,&nbsp;edited &nbsp;<a class="tgme_widget_message_date" href="https://t.me/tchantest/5"><time datetime="2023-02-24T07:29:57+00:00" class="time">07:29</time></a></span>
                </div>
              </div>
            </div>
          </div>
        </div>
    """
    tree = document_fromstring(html)
    result = list(parse_messages(original_url, tree))
    expected = ChannelMessage(
        id=5,
        created_at=datetime.datetime(
            2023, 2, 24, 7, 29, 57, tzinfo=datetime.timezone.utc
        ),
        type="text",
        channel="tchantest",
        urls=[],
        author="Álvaro Justen",
        edited=True,
        text="Hello! Signed and edited message",
        views=2,
    )
    assert result[0] == expected
