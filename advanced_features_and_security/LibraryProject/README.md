# Security Measures Implemented

## Cross-Site Scripting (XSS) Protection
- Automatic escaping in templates
- Content Security Policy (CSP) headers
- `SECURE_BROWSER_XSS_FILTER` enabled
- Manual escaping of user inputs in views

## Cross-Site Request Forgery (CSRF) Protection
- CSRF middleware enabled
- CSRF tokens in all forms
- Secure and HttpOnly flags on CSRF cookie

## SQL Injection Protection
- Exclusive use of Django ORM
- Parameterized queries
- Input validation in views

## Clickjacking Protection
- `X_FRAME_OPTIONS = 'DENY'`
- Frame-breaking JavaScript in templates

## Secure Headers
- HSTS enabled with 1-year duration
- Secure and HttpOnly cookies
- X-Content-Type-Options: nosniff

## Password Security
- Strong password validators
- Modern password hashing (Argon2)