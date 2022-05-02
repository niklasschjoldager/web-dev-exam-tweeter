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
    "Tweeter for Business",
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
]

mobile_navigation = [
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
]

navigation_dropdown = [
    {
        "icon": '<svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><title>Chatbox Ellipses</title><path d="M408 64H104a56.16 56.16 0 00-56 56v192a56.16 56.16 0 0056 56h40v80l93.72-78.14a8 8 0 015.13-1.86H408a56.16 56.16 0 0056-56V120a56.16 56.16 0 00-56-56z" fill="none" stroke="currentColor" stroke-linejoin="round" stroke-width="32"/><circle fill="currentColor" cx="160" cy="216" r="32"/><circle fill="currentColor" cx="256" cy="216" r="32"/><circle fill="currentColor" cx="352" cy="216" r="32"/></svg>',
        "text": "Topics",
    },
    {
        "icon": '<svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><title>Flash</title><path d="M315.27 33L96 304h128l-31.51 173.23a2.36 2.36 0 002.33 2.77h0a2.36 2.36 0 001.89-.95L416 208H288l31.66-173.25a2.45 2.45 0 00-2.44-2.75h0a2.42 2.42 0 00-1.95 1z" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32"/></svg>',
        "text": "Moments",
    },
    {
        "icon": '<svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><title>Newspaper</title><path d="M368 415.86V72a24.07 24.07 0 00-24-24H72a24.07 24.07 0 00-24 24v352a40.12 40.12 0 0040 40h328" fill="none" stroke="currentColor" stroke-linejoin="round" stroke-width="32"/><path d="M416 464h0a48 48 0 01-48-48V128h72a24 24 0 0124 24v264a48 48 0 01-48 48z" fill="none" stroke="currentColor" stroke-linejoin="round" stroke-width="32"/><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32" d="M240 128h64M240 192h64M112 256h192M112 320h192M112 384h192"/><path fill="currentColor" d="M176 208h-64a16 16 0 01-16-16v-64a16 16 0 0116-16h64a16 16 0 0116 16v64a16 16 0 01-16 16z"/></svg>',
        "text": "Newsletters",
    },
    {
        "icon": '<svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><title>Rocket</title><path d="M461.81 53.81a4.4 4.4 0 00-3.3-3.39c-54.38-13.3-180 34.09-248.13 102.17a294.9 294.9 0 00-33.09 39.08c-21-1.9-42-.3-59.88 7.5-50.49 22.2-65.18 80.18-69.28 105.07a9 9 0 009.8 10.4l81.07-8.9a180.29 180.29 0 001.1 18.3 18.15 18.15 0 005.3 11.09l31.39 31.39a18.15 18.15 0 0011.1 5.3 179.91 179.91 0 0018.19 1.1l-8.89 81a9 9 0 0010.39 9.79c24.9-4 83-18.69 105.07-69.17 7.8-17.9 9.4-38.79 7.6-59.69a293.91 293.91 0 0039.19-33.09c68.38-68 115.47-190.86 102.37-247.95zM298.66 213.67a42.7 42.7 0 1160.38 0 42.65 42.65 0 01-60.38 0z" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32"/><path d="M109.64 352a45.06 45.06 0 00-26.35 12.84C65.67 382.52 64 448 64 448s65.52-1.67 83.15-19.31A44.73 44.73 0 00160 402.32" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32"/></svg>',
        "text": "Tweeter for Professionals",
    },
    {
        "icon": '<svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><title>Open</title><path d="M384 224v184a40 40 0 01-40 40H104a40 40 0 01-40-40V168a40 40 0 0140-40h167.48M336 64h112v112M224 288L440 72" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32"/></svg>',
        "text": "Tweeter Ads",
    },
    {
        "icon": '<svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><title>Bar Chart</title><path d="M32 32v432a16 16 0 0016 16h432" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32"/><rect x="96" y="224" width="80" height="192" rx="20" ry="20" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32"/><rect x="240" y="176" width="80" height="240" rx="20" ry="20" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32"/><rect x="383.64" y="112" width="80" height="304" rx="20" ry="20" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32"/></svg>',
        "text": "Analytics",
    },
    {
        "icon": '<svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><title>Settings</title><path d="M262.29 192.31a64 64 0 1057.4 57.4 64.13 64.13 0 00-57.4-57.4zM416.39 256a154.34 154.34 0 01-1.53 20.79l45.21 35.46a10.81 10.81 0 012.45 13.75l-42.77 74a10.81 10.81 0 01-13.14 4.59l-44.9-18.08a16.11 16.11 0 00-15.17 1.75A164.48 164.48 0 01325 400.8a15.94 15.94 0 00-8.82 12.14l-6.73 47.89a11.08 11.08 0 01-10.68 9.17h-85.54a11.11 11.11 0 01-10.69-8.87l-6.72-47.82a16.07 16.07 0 00-9-12.22 155.3 155.3 0 01-21.46-12.57 16 16 0 00-15.11-1.71l-44.89 18.07a10.81 10.81 0 01-13.14-4.58l-42.77-74a10.8 10.8 0 012.45-13.75l38.21-30a16.05 16.05 0 006-14.08c-.36-4.17-.58-8.33-.58-12.5s.21-8.27.58-12.35a16 16 0 00-6.07-13.94l-38.19-30A10.81 10.81 0 0149.48 186l42.77-74a10.81 10.81 0 0113.14-4.59l44.9 18.08a16.11 16.11 0 0015.17-1.75A164.48 164.48 0 01187 111.2a15.94 15.94 0 008.82-12.14l6.73-47.89A11.08 11.08 0 01213.23 42h85.54a11.11 11.11 0 0110.69 8.87l6.72 47.82a16.07 16.07 0 009 12.22 155.3 155.3 0 0121.46 12.57 16 16 0 0015.11 1.71l44.89-18.07a10.81 10.81 0 0113.14 4.58l42.77 74a10.8 10.8 0 01-2.45 13.75l-38.21 30a16.05 16.05 0 00-6.05 14.08c.33 4.14.55 8.3.55 12.47z" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32"/></svg>',
        "text": "Settings and privacy",
    },
    {
        "icon": '<svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><title>Help Circle</title><path d="M256 80a176 176 0 10176 176A176 176 0 00256 80z" fill="none" stroke="currentColor" stroke-miterlimit="10" stroke-width="32"/><path d="M200 202.29s.84-17.5 19.57-32.57C230.68 160.77 244 158.18 256 158c10.93-.14 20.69 1.67 26.53 4.45 10 4.76 29.47 16.38 29.47 41.09 0 26-17 37.81-36.37 50.8S251 281.43 251 296" fill="none" stroke="currentColor" stroke-linecap="round" stroke-miterlimit="10" stroke-width="28"/><circle cx="250" cy="348" r="20"/></svg>',
        "text": "Help Center",
    },
    {
        "icon": '<svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><title>Create</title><path d="M384 224v184a40 40 0 01-40 40H104a40 40 0 01-40-40V168a40 40 0 0140-40h167.48" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32"/><path fill="currentColor" d="M459.94 53.25a16.06 16.06 0 00-23.22-.56L424.35 65a8 8 0 000 11.31l11.34 11.32a8 8 0 0011.34 0l12.06-12c6.1-6.09 6.67-16.01.85-22.38zM399.34 90L218.82 270.2a9 9 0 00-2.31 3.93L208.16 299a3.91 3.91 0 004.86 4.86l24.85-8.35a9 9 0 003.93-2.31L422 112.66a9 9 0 000-12.66l-9.95-10a9 9 0 00-12.71 0z"/></svg>',
        "text": "Display",
    },
    {
        "icon": '<svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><title>Accessibility</title><circle fill="none" stroke="currentColor" stroke-linejoin="round" stroke-width="32" cx="256" cy="56" r="40"/><path fill="none" stroke="currentColor" stroke-linejoin="round" stroke-width="32" d="M204.23 274.44c2.9-18.06 4.2-35.52-.5-47.59-4-10.38-12.7-16.19-23.2-20.15L88 176.76c-12-4-23.21-10.7-24-23.94-1-17 14-28 29-24 0 0 88 31.14 163 31.14s162-31 162-31c18-5 30 9 30 23.79 0 14.21-11 19.21-24 23.94l-88 31.91c-8 3-21 9-26 18.18-6 10.75-5 29.53-2.1 47.59l5.9 29.63 37.41 163.9c2.8 13.15-6.3 25.44-19.4 27.74S308 489 304.12 476.28l-37.56-115.93q-2.71-8.34-4.8-16.87L256 320l-5.3 21.65q-2.52 10.35-5.8 20.48L208 476.18c-4 12.85-14.5 21.75-27.6 19.46s-22.4-15.59-19.46-27.74l37.39-163.83z"/></svg>',
        "text": "Keyboard shortcuts",
    },
]

user_page_tabs = [
    {
        "id": "",
        "url": "",
        "text": "Tweets",
    },
    {
        "id": "with-replies",
        "url": "",
        "text": "Tweets & replies",
    },
    {
        "id": "media",
        "url": "/media",
        "text": "Media",
    },
    {
        "id": "likes",
        "url": "/likes",
        "text": "Likes",
    },
]

user_page_default_messages = {
    "": {
        "personal": {
            "title": "You haven't tweeted anything yet.",
            "description": "When you make your first tweet, it will show up here",
        },
        "user": {
            "title": "The user haven't tweeted anything yet.",
            "description": "When they make their first tweet, it will show up here",
        },
    },
    "with-replies": {
        "personal": {
            "title": "You haven't tweeted nor made any replies yet.",
            "description": "When you make a tweet or reply to a tweet, it will show up here",
        },
        "user": {
            "title": "The user haven't tweeted nor made any replies yet.",
            "description": "when they make their first tweet or reply to a tweet, it will show up here",
        },
    },
    "media": {
        "personal": {
            "title": "Lights, camera … attachments!",
            "description": "When you send Tweets with photos or videos in them, it will show up here",
        },
        "user": {
            "title": "Lights, camera … attachments!",
            "description": "When the user send Tweets with photos or videos in them, it will show up here",
        },
    },
    "likes": {
        "personal": {
            "title": "You don't have any likes yet",
            "description": "Tap the heart on any Tweet to show it some love. When you do, it'll show up here.",
        },
        "user": {
            "title": "The user don't have any likes yet",
            "description": "When they do, it'll show up here.",
        },
    },
}
