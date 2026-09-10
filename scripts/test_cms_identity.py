"""Browser regression checks using the real widget and a fake Identity service.

Requires Playwright, Chromium, and a production Hugo build in public/.
No requests reach Netlify and no real accounts or emails are used.
"""

import argparse
import mimetypes
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import expect, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://cms.example.test"
USER = {"id": "test-editor", "email": "editor@example.test", "user_metadata": {}}
TOKEN = {"access_token": "test-access", "refresh_token": "test-refresh",
         "token_type": "bearer", "expires_in": 3600}


def run(browser, widget, path, flow):
    context = browser.new_context()
    page = context.new_page()
    requests = []
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))

    def route(request_route):
        request = request_route.request
        url = urlparse(request.url)
        if request.url == "https://identity.netlify.com/v1/netlify-identity-widget.js":
            request_route.fulfill(path=str(widget), content_type="text/javascript")
        elif request.url.startswith(ORIGIN + "/.netlify/identity/"):
            endpoint = url.path.removeprefix("/.netlify/identity/")
            body = request.post_data_json if request.post_data else None
            requests.append((request.method, endpoint, body))
            status = 200
            if endpoint == "settings":
                response = {"external": {}, "disable_signup": True, "autoconfirm": False}
            elif endpoint == "verify":
                if flow == "expired":
                    status = 400
                    response = {"code": 400, "msg": "Recovery token has expired"}
                else:
                    response = TOKEN
            elif endpoint == "user":
                response = USER
            elif endpoint == "recover":
                response = {}
            else:
                raise AssertionError(f"Unexpected Identity endpoint: {endpoint}")
            request_route.fulfill(status=status, json=response)
        elif url.netloc == urlparse(ORIGIN).netloc and not url.path.startswith("/.netlify/"):
            file = ROOT / "public" / url.path.lstrip("/")
            if url.path.endswith("/"):
                file /= "index.html"
            if file.is_file():
                request_route.fulfill(path=str(file), content_type=mimetypes.guess_type(file)[0])
            else:
                request_route.fulfill(status=404, body="Not found")
        else:
            # CMS Git Gateway and third-party site assets are outside this test.
            request_route.fulfill(status=503, json={"message": "Mock: unavailable"})

    context.route("**/*", route)
    fragment = {"recovery": "recovery_token=valid-recovery",
                "expired": "recovery_token=expired-recovery",
                "invite": "invite_token=valid-invite"}.get(flow, "")
    page.goto(ORIGIN + path + ("#" + fragment if fragment else ""))
    frame = page.frame_locator("#netlify-identity-widget")

    if flow in ("recovery", "invite"):
        button = "Update password" if flow == "recovery" else "Sign up"
        expect(frame.locator('input[type="password"]')).to_be_visible()
        # Decap's fallback initialization timer must not reset the password form.
        page.wait_for_timeout(3000)
        expect(page.locator("#netlify-identity-widget")).to_have_count(1)
        assert urlparse(page.url).path == path
        assert not any(method == "PUT" for method, _, _ in requests)
        frame.locator('input[type="password"]').fill("Example-test-password-123!")
        frame.get_by_role("button", name=button, exact=True).click()
        if path == "/":
            page.wait_for_url(ORIGIN + "/admin/")
        else:
            page.wait_for_function("!!window.netlifyIdentity.currentUser()")
        if flow == "recovery":
            assert ("POST", "verify", {"type": "recovery", "token": "valid-recovery"}) in requests
            assert ("PUT", "user", {"password": "Example-test-password-123!"}) in requests
        else:
            assert ("POST", "verify", {"type": "signup", "token": "valid-invite",
                                      "password": "Example-test-password-123!"}) in requests
    elif flow == "expired":
        expect(frame.get_by_text("Recovery token has expired", exact=True)).to_be_visible()
        assert urlparse(page.url).path == path
        assert not any(method == "PUT" for method, _, _ in requests)
    elif flow == "request":
        page.evaluate("window.netlifyIdentity.open('login')")
        frame.get_by_text("Forgot password?", exact=True).click()
        frame.locator('input[type="email"]').fill(USER["email"])
        frame.get_by_role("button", name="Send recovery email", exact=True).click()
        expect(frame.get_by_text("We've sent a recovery email", exact=False)).to_be_visible()
        assert ("POST", "recover", {"email": USER["email"]}) in requests
    else:
        expect(page.locator("#netlify-identity-widget")).to_be_hidden()
        assert urlparse(page.url).path == path

    assert not errors, errors
    context.close()
    print(f"PASS {path} {flow}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--widget-script", required=True, type=Path)
    parser.add_argument("--browser", help="Optional Chrome/Chromium executable")
    args = parser.parse_args()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=args.browser)
        try:
            for path in ("/", "/admin/"):
                for flow in ("recovery", "invite", "expired", "request", "visitor"):
                    run(browser, args.widget_script.resolve(), path, flow)
        finally:
            browser.close()
