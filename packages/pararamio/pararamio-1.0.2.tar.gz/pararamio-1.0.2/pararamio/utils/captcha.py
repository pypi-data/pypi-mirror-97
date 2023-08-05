import base64
import tkinter as tk
from urllib.error import HTTPError
from urllib.parse import urlencode

from pararamio._types import CookieJarT
from pararamio.constants import REQUEST_TIMEOUT as TIMEOUT
from pararamio.utils.requests import _base_request, api_request


def get_captcha_img(id_: str, headers: dict = None, cookie_jar: CookieJarT = None, timeout: int = TIMEOUT) -> 'tk.PhotoImage':
    args = urlencode({'id': id_})
    url = f'/auth/captcha?{args}'
    tc = 3
    data = None
    while True:
        try:
            data = _base_request(url, headers=headers, cookie_jar=cookie_jar, timeout=timeout).read()
            break
        except HTTPError:
            if not tc:
                raise
            tc -= 1
            continue
    return tk.PhotoImage(data=base64.b64encode(data))


def verify_captcha(code: str, headers: dict = None, cookie_jar: CookieJarT = None, timeout: int = TIMEOUT) -> bool:
    url = '/auth/captcha'
    resp = api_request(url, 'POST', data={'code': code}, headers=headers, cookie_jar=cookie_jar, timeout=timeout)
    return str.lower(resp.get('status', '')) == 'OK'


def show_captcha(login: str, headers: dict = None, cookie_jar: CookieJarT = None, timeout: int = TIMEOUT) -> bool:
    root = tk.Tk()
    root.title('Pararamio captcha')
    root.resizable(False, False)
    photo = get_captcha_img(login, headers=headers, cookie_jar=cookie_jar, timeout=timeout)
    h = photo.height() + 138
    w = photo.width() + 75
    root.geometry(f'{w:d}x{h:d}')
    panel = tk.Label(root, image=photo)
    br = tk.Button(text='R', width=7, height=4, cursor='hand2')
    bs = tk.Button(text='Send', width=15, height=4, cursor='hand2')
    label = tk.Label(root, text='Code: ', width=20)
    code = tk.StringVar()
    entry = tk.Entry(root, textvariable=code, justify='center')
    cookie_entered = False

    def refresh_photo():
        # noinspection PyBroadException
        try:
            img = get_captcha_img(login, headers=headers, cookie_jar=cookie_jar, timeout=timeout)
            panel.config(image=img)
            panel.image = img
        except Exception:
            pass

    def send_code():
        nonlocal cookie_entered
        try:
            verify_captcha(str.strip(entry.get()), headers=headers, cookie_jar=cookie_jar, timeout=timeout)
            cookie_entered = True
            root.destroy()
        except HTTPError:
            code.set('')
            refresh_photo()

    br.config(command=refresh_photo)
    bs.config(command=send_code)
    panel.grid(row=0, column=0, pady=0, padx=0, sticky=tk.N + tk.S + tk.W + tk.E)
    br.grid(row=0, column=1, pady=0, padx=0, sticky=tk.N + tk.S + tk.W + tk.E)
    label.grid(row=1, pady=0, padx=0, columnspan=2, sticky=tk.N + tk.S + tk.W + tk.E)
    entry.grid(row=2, pady=0, padx=0, columnspan=2, sticky=tk.N + tk.S + tk.W + tk.E)
    bs.grid(row=3, columnspan=2)
    root.mainloop()
    return cookie_entered
