# AladdinConnect SDK

## Authentication

### OAuth Client
This SDK requires you to already have an OAuth client setup with us.
The initial OAuth2.0 flow must be implemented by the users of this
library as we provide no default implementation. More information
on how to set this up will be provided when the OAuth client is set up.

### Auth Class Implementation
The SDK provides an `Auth` class. It requires the following constructor parameters:

- `websession`: an `aiohttp.ClientSession` that will be used for requests
- `host`: the partner-specific base URL for the API
- `access_token`: an initial access token to use (either cached or retrieved via the login flow)
- `api_key`: a partner-specific API key provided during initial onboarding

This class also provides an abstract method `async_get_access_token`.
This method is meant to be overridden with logic to handle checking the
current token's validity and refreshing if needed. The refresh token will
need to be managed outside of this class. Once this is implemented, the
`request` method will automatically check the access token and set the
appropriate authentication headers.

## Model
Each garage door is modeled using the `GarageDoor` class that has the following
properties:

- `device_id`: a unique ID for the device (that could have multiple doors)
- `door_number`: the index of the door, can be 1, 2 or 3
- `unique_id`: a unique ID for the door of the format `{DEVICE_ID}-{DOOR_NUMBER}`
- `name`: a user defined name for the door
- `status`: the current state of the door, one of:
    - `open`: door is open
    - `closed`: door is closed
    - `opening`: door is in the process of being opened
    - `closing`: door is in the process of being closed
    - `unknown`: device has been recently setup or reset, requires a user
    to locally cycle the door open / closed to get the correct state
- `link_status`: whether or not the door sensor is properly paired. Can be one of:
    - `not_config`: not yet configured, must use the app to pair
    - `paired`: configured, but not yet connected
    - `connected`: fully functional
- `battery_level`: the current battery percentage (0 - 100) of the door sensor

## Client
The `AladdinConnectClient` class provides the actual functionality of the API. It
requires an `Auth` session to be configured (described above in the Authentication section).
This class provides the following methods:
- `get_doors`: Sync all the user's devices. This returns a list of `GarageDoor` instances as well
as updating its own internal state
- `update_door`: Sync a specific door and update the internal state
- `open_door`: Issue an open command
- `open_door`: Issue a close command
- `get_door_status`: Return the current state of a door (this uses the internal state, it does not make a call to the API. To sync the state of a door, use `update_door` and then call this to get its status).
- `get_battery_status`: Get the battery status of a door (this uses the internal state, it does not make a call to the API. To sync the state of a door, use `update_door` and then call this to get the battery status)
