# Web API Considerations

You can use `django-aai-eduhr` when building both traditional and API-based web architectures, the core functionality 
remains the same in both scenarios. Still, there are a few best practices and recommendations that can help you 
maximize its effectiveness, especially when integrating with web APIs.

## Authentication method

`djangosaml2`, and by extension `django-aai-eduhr`, manages user authentication sessions via the `saml_session` and
`sessionid` cookies. These cookies are set when a user successfully authenticates through the AAI@EduHr service, and 
they must be included in all subsequent requests, regardless of whether the client is a web browser or a different 
type of client.

While web applications can easily work with cookies, APIs often prefer alternative authentication mechanisms, such as 
API keys sent through HTTP headers. As such, API clients integrating with `django-aai-eduhr` have two main options:

1. **Include the `sessionid` and `saml_session` cookies with each request.**  
This is the simplest approach and works well when cookie handling is feasible for the client.

2. **Use the session cookies to authenticate once, then exchange it for a secondary credential (e.g., an access token 
or an API key) that can be used for subsequent requests.**  
This strategy decouples long-term authentication from the SAML session and may be more suitable for stateless or 
mobile clients.

Both approaches are valid and supported. The best choice depends on your application's architecture, security 
requirements, and client capabilities.

### JSON Web Tokens

It's worth noting that strategy #2 aligns closely with the JSON Web Token (JWT) authentication model. In this 
scenario, the `sessionid` and `saml_session` cookies can be used to refresh an access token, which then serves as the 
credential for subsequent requests.

The authentication flow may go something like this:

1. **Initial Authentication:**
The user authenticates via the AAI@EduHr, which sets the `sessionid` and `saml_session` cookies. These acts as 
temporary credentials that prove the user has successfully logged in.

2. **Access Token Retrieval**:
Next, a client sends out both cookies to the backend which validates the session, and the application issues 
JWT access token.

3. **Subsequent Requests:**
For subsequent API calls, the client uses the access token (instead of `sessionid` and `saml_session` cookies) to 
authenticate.

4. **Token Expiration and Refresh:**
When an access token expires, the client can use the cookies together with a refresh token to request a 
new access token. In this scenario, the cookies can be used to validate the AAI@EduHr session, ensuring the token is 
refreshed only if the refresh token and the SSO session remain valid.

## Separate API and frontend domains

When your frontend is hosted on a different domain from the backend (e.g., `api.example.org` and `example.org`), you 
will need to adjust your cookie settings to ensure proper cross-domain functionality.

Requests originating from a different host, e.g. `example.org` to `api.example.org` need to satisfy CORS criteria. At 
the very least, the origin should be allowed by the server through `access-control-allow-origin` header. For requests 
carrying credentials such as authentication cookies, server needs to send `access-control-allow-credentials: true` 
header as well. Note that in that case `access-control-allow-origin` can not have wildcard value, it needs an explicit 
origin.

You can use `django-cors-headers` package to set these headers:

```py
# Assuming example.org as the frontend, and api.example.org as the backend.
CORS_ALLOWED_ORIGINS = ['https://example.org']
CORS_ALLOW_CREDENTIALS = True
```

You can configure CORS headers on the server yourself if you do not want to use `django-cors-headers` package.

If you need to send cookies to your frontend for any reason, you must explicitly define the domains where 
the browser is allowed to set or transmit cookies by modifying the `Domain` attribute. By default, browsers only send 
cookies to the exact domain from which they were set, excluding subdomains. **However, explicitly setting the Domain 
attribute allows the browser to share cookies across subdomains.**

```py
SESSION_COOKIE_DOMAIN = 'example.org'  # Scope session cookie to example.org and its subdomains.
```

```{important}
Note that [RFC 2109](https://www.rfc-editor.org/rfc/rfc2109) and the newer 
[RFC 6265](https://www.rfc-editor.org/rfc/rfc6265) differ somewhat in how they handle `Domain` attribute. In the RFC 
6265, setting a domain automatically includes its subdomains. In contrast, RFC 2109 requires leading dot, e.g. 
`.example.org`, to include subdomains.

Different browsers implement these standards to varying degrees, and may follow either of these standards or both.
```
