CUSTOMED_APPS = [
    "users.apps.UsersConfig",
    "rooms.apps.RoomsConfig",
    "reviews.apps.ReviewsConfig",
    "medias.apps.MediasConfig",
    "wishlists.apps.WishlistsConfig",
    "bookings.apps.BookingsConfig",
    "direct_messages.apps.DirectMessagesConfig",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
]

DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS = DEFAULT_APPS + CUSTOMED_APPS + THIRD_PARTY_APPS
