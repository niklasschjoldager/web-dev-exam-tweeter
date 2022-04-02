import datetime

############################################################

time = datetime.datetime.now()
current_year = time.year
months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

footer_links = [
    "About",
    "Helper Center",
    "Terms of Service",
    "Privacy Policy",
    "Cookie Policy",
    "Accessibility",
    "Ads info",
    "Blog",
    "Status",
    "Careers",
    "Brand Resources",
    "Advertising",
    "Marketing",
    "Twitter for Business",
    "Developers",
    "Directory",
    "Settings",
    f"© {current_year} Tweeter, inc",
]

navigation = [
    {
        "name": "Home",
        "url": "home",
        "icons": {
            "default": "twitter.svg",
            "active": "twitter.svg",
        },
    },
    {
        "name": "Home",
        "url": "home",
        "icons": {
            "default": "home-outline.svg",
            "active": "home.svg",
        },
    },
    {
        "name": "Search",
        "url": "search",
        "icons": {
            "default": "search-outline.svg",
            "active": "search.svg",
        },
    },
    {
        "name": "Notifications",
        "url": "notifications",
        "icons": {
            "default": "notifications-outline.svg",
            "active": "notifications.svg",
        },
    },
    {
        "name": "Messages",
        "url": "messages",
        "icons": {
            "default": "mail-outline.svg",
            "active": "mail.svg",
        },
    },
    {
        "name": "Bookmarks",
        "url": "bookmarks",
        "icons": {
            "default": "bookmark-outline.svg",
            "active": "bookmark.svg",
        },
    },
    {
        "name": "Lists",
        "url": "lists",
        "icons": {
            "default": "clipboard-outline.svg",
            "active": "clipboard.svg",
        },
    },
    {
        "name": "Profile",
        "url": "profile",
        "icons": {
            "default": "person-outline.svg",
            "active": "person.svg",
        },
    },
]
