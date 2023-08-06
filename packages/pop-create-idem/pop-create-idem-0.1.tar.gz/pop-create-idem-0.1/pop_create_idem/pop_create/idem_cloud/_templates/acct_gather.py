import aiohttp


async def gather(hub):
    """
    Authenticate with a username and password to the given endpoint url.
    Any extra parameters will be saved as part of the profile.

    Example:

    .. code-block:: yaml

        R__CLOUD__.basic_auth:
          profile_name:
            username: my_user
            password: my_good_password
            endpoint_url: https://console.R__CLOUD__.com/api
    """
    sub_profiles = {}
    for profile, ctx in hub.acct.PROFILES.get("R__CLOUD__.basic_auth", {}).items():
        try:
            # Add an aiohttp session to the ctx
            # One profile we put in "ctx" right will show up in idem functions under ctx.acct
            ctx.connection = aiohttp.ClientSession(
                loop=hub.pop.Loop,
                auth=aiohttp.BasicAuth(ctx["username"], ctx["password"]),
            )
            sub_profiles[profile] = ctx
            hub.log.debug(f"connected to R__CLOUD__ with profile: {profile}")
        except Exception as e:
            # If a profile fails to load, it might not be the one the program is using
            # Log the error and move along
            hub.log.error(f"{e.__class__.__name__}: {e}")
            continue

    return sub_profiles


async def close(hub, profiles):
    # Clean up all profiles when the program is terminated
    for profile_name, ctx in profiles.items():
        await ctx.connection.close()
