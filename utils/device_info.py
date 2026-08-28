from user_agents import parse

def get(request, user_agent: str):
    user_agent = request.META.get('HTTP_USER_AGENT')
    ua = parse(user_agent)
    browser = ua.browser
    platform = ua.os

    if ua.is_mobile:
        device_type = "mobile"
    elif ua.is_tablet:
        device_type = "tablet"
    elif ua.is_pc:
        device_type = "desktop"
    else:
        device_type = "other"

    return dict(
        user_agent=user_agent,
        browser=browser,
        platform=platform,
        device_type=device_type
    )