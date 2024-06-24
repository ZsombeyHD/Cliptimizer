import tkinter as tk
import tkinter.ttk as ttk
import webbrowser


class ContactPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg='white')

        # Az elérhetőségek kiírása
        contact_label = ttk.Label(self, text="KAPCSOLATTARTÓ INFORMÁCIÓK", font=('Helvetica', 20, 'bold'))
        contact_label.pack(pady=(100, 50))

        email_label = ttk.Label(self, text="Email", font=('Helvetica', 16, 'bold'))
        email_label.pack(pady=10)
        email_entry = ttk.Entry(self, font=('Helvetica', 14), justify='center', width=40)
        email_entry.pack(pady=5)
        email_entry.insert(0, "wennervarkonyizsombor@gmail.com")
        email_entry.config(state='readonly')

        phone_label = ttk.Label(self, text="Telefonszám", font=('Helvetica', 16, 'bold'))
        phone_label.pack(pady=10)
        phone_entry = ttk.Entry(self, font=('Helvetica', 14), justify='center', width=20)
        phone_entry.pack(pady=5)
        phone_entry.insert(0, "06705069814")
        phone_entry.config(state='readonly')

        social_label = ttk.Label(self, text="Social Media", font=('Helvetica', 16, 'bold'))
        social_label.pack(pady=10)

        facebook_link = tk.Label(self, text="Wenner-Várkonyi Zsombor [Facebook]", font=('Helvetica', 14, 'bold'),
                                 fg="blue",
                                 cursor="hand2")
        facebook_link.pack(pady=5)
        facebook_link.bind("<Button-1>",
                           lambda e: webbrowser.open_new("https://www.facebook.com/zsombor.wennervarkonyi"))

        youtube_link = tk.Label(self, text="ZsombeyHD [YouTube]", font=('Helvetica', 14, 'bold'), fg="red",
                                cursor="hand2")
        youtube_link.pack(pady=5)
        youtube_link.bind("<Button-1>",
                          lambda e: webbrowser.open_new("https://www.youtube.com/channel/UCQ_QAobbdVw6ntDMAloTKww"))

        twitch_link = tk.Label(self, text="ZsombeyHD [Twitch]", font=('Helvetica', 14, 'bold'), fg="purple",
                               cursor="hand2")
        twitch_link.pack(pady=5)
        twitch_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.twitch.tv/zsombeyhd"))

        twitter_link = tk.Label(self, text="ZsombeyHD [Twitter/X]", font=('Helvetica', 14, 'bold'), fg="black",
                                cursor="hand2")
        twitter_link.pack(pady=5)
        twitter_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://twitter.com/ZsombeyHD"))
