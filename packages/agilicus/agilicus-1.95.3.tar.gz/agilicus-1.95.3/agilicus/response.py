import os


def validate(resp, _continue_on_error=False):
    # 409 is a special case -- it means that the entry existed.
    # Our API handles that nicely.
    if resp.status_code == 409:
        return

    if resp.status_code >= 400:
        print(f"Error {resp.status_code}")
        print(resp.text)
        if not _continue_on_error:
            os._exit(1)
