from conf import settings
USERS_SERVICE_URL  = settings.USERS_SERVICE_URL
EVENTS_SERVICE_URL = settings.EVENTS_SERVICE_URL


ROUTES = {
	######################## USERS_SERVICE_URL ########################
    "api/auth/token/": USERS_SERVICE_URL + '/api/auth/token/',
    "api/accounts/users/": USERS_SERVICE_URL + '/api/accounts/users/',


    ######################## EVENTS_SERVICE_URL ########################
    "api/events/": EVENTS_SERVICE_URL + '/api/events/'


}