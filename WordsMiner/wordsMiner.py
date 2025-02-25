'''Before use it,check that you have installed the following packages:
   pip install requests jieba matplotlib beautifulsoup4 wordcloud pillow'''

#GUI package
import tkinter as tk
from tkinter import ttk,filedialog,messagebox
from PIL import Image,ImageTk

#Data processing package
import os
import requests
import jieba
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from wordcloud import WordCloud

class WordsMinerGUI:
    '''GUI for WordsMiner'''

    def __init__(self,master):
    #master is the main window
        self.master = master
        master.title("WordsMiner")
        master.configure(bg="#f0f9f5")
        master.geometry("980x500")
        master.resizable(width=False,height=False)
        master.configure(bg="#f0f9f5")

        #set icon
        try:
            icon_img = Image.open("WordsMiner/assets/fatGoose.ico")
            icon_photo = ImageTk.PhotoImage(icon_img)
            master.iconphoto(True, icon_photo)
            self.icon_photo = icon_photo
        except Exception as e:
            print(f"图标加载失败: {e}")

        #config ttk style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.init_theme("#f0f9f5", "#2c615c", "#a8dacc", "#6ab8af")

        #set default font_path and wordcloud
        self.font_path = "simhei.ttf"
        self.current_wordcloud = None

        #create tk window widgets
        self.create_widgets()

    def init_theme(self, bg, fg, btn_bg, btn_active):
    #initialize style
        self.style.configure("TFrame", background=bg)
        self.style.configure("TLabel", background=bg, foreground=fg)
        self.style.configure("TButton", background=btn_bg, foreground=fg)
        self.style.map("TButton",
                      foreground=[('active', '#ffffff'), ('!active', fg)],
                      background=[('active', btn_active), ('!active', btn_bg)])

    def create_widgets(self):
    # create left and right frame
        self.left_frame = ttk.Frame(self.master, width=320, padding=15)
        self.left_frame.pack(side="left", fill="y", padx=5, pady=5)
        
        #separate line in the middle
        separator = ttk.Separator(self.master, orient="vertical")
        separator.pack(side="left", fill="y", padx=5)
        
        self.right_frame = ttk.Frame(self.master, padding=15)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        #left frame content
        header_label = ttk.Label(self.left_frame, 
                               text="📰 WordsMiner", 
                               font=("Microsoft YaHei", 12, "bold"))
        header_label.pack(pady=(0, 15))

        # url input
        ttk.Label(self.left_frame, text="新闻URL：").pack(anchor="w")
        self.url_entry = ttk.Entry(self.left_frame, width=30)
        self.url_entry.pack(fill="x", pady=5, ipady=3)

        # stop words file selection
        ttk.Label(self.left_frame, text="停用词文件：").pack(anchor="w", pady=(10,0))
        self.stopwords_frame = ttk.Frame(self.left_frame)
        self.stopwords_frame.pack(fill="x")
        self.stopwords_entry = ttk.Entry(self.stopwords_frame, width=28)
        self.stopwords_entry.pack(side="left", fill="x", expand=True, ipady=3)
        ttk.Button(self.stopwords_frame, text="浏览", width=6, 
                  command=self.select_stopwords).pack(side="right", padx=5)

        # font file selection
        ttk.Label(self.left_frame, text="字体文件：").pack(anchor="w", pady=(10,0))
        self.font_frame = ttk.Frame(self.left_frame)
        self.font_frame.pack(fill="x")
        self.font_entry = ttk.Entry(self.font_frame, width=28)
        self.font_entry.pack(side="left", fill="x", expand=True, ipady=3)
        ttk.Button(self.font_frame, text="浏览", width=6, 
                  command=self.select_fontfile).pack(side="right",padx=5)

        # analysis mode selection
        ttk.Label(self.left_frame, text="解析模式：").pack(anchor="w", pady=(15,0))
        self.mode_combobox = ttk.Combobox(self.left_frame, 
                                        values=["模式1(越牛新闻)", "模式2(政府新闻)"], 
                                        state="readonly")
        self.mode_combobox.current(0)
        self.mode_combobox.pack(fill="x", pady=5, ipady=2)
        
        # theme color selection
        ttk.Label(self.left_frame, text="主题色选择：").pack(anchor="w", pady=(15,0))
        self.color_combobox = ttk.Combobox(self.left_frame, 
                                        values=["抹茶绿", "标准白"], 
                                        state="readonly")
        self.color_combobox.current(0)
        self.color_combobox.bind("<<ComboboxSelected>>", self.change_theme)
        self.color_combobox.pack(fill="x", pady=5, ipady=2)

        # action buttons
        action_frame = ttk.Frame(self.left_frame)
        action_frame.pack(pady=20)
        ttk.Button(action_frame, text="✨ 生成词云", width=12,
                  command=self.generate_wordcloud).pack(side="left", padx=5)
        ttk.Button(action_frame, text="💾 保存词云", width=12,
                  command=self.save_wordcloud).pack(side="right", padx=5)

        # right frame content
        self.image_label = ttk.Label(self.right_frame)
        self.image_label.pack(fill="both", expand=True)

    def change_theme(self, event=None):
    #change theme
        theme = self.color_combobox.get()
        if theme == "抹茶绿":
            self.master.configure(bg="#f0f9f5")
            self.init_theme("#f0f9f5", "#2c615c", "#a8dacc", "#6ab8af")
        elif theme == "标准白":
            self.master.configure(bg="#ffffff")
            self.init_theme("#ffffff", "#333333", "#e0e0e0", "#666666")
            
        # refresh frame background
        self.left_frame.configure(style="TFrame")
        self.right_frame.configure(style="TFrame")

    def select_stopwords(self):
    #select stop words file
        path = filedialog.askopenfilename(filetypes=[("文本文件", "*.txt")])
        if path:
            self.stopwords_entry.delete(0, tk.END)
            self.stopwords_entry.insert(0, path)

    def select_fontfile(self):
    #select font file
        path = filedialog.askopenfilename(filetypes=[("字体文件", "*.ttf;*.ttc")])
        if path:
            self.font_entry.delete(0, tk.END)
            self.font_entry.insert(0, path)

    def generate_wordcloud(self):
    #generate wordcloud
        url = self.url_entry.get()
        stopwords_path = self.stopwords_entry.get()
        font_path = self.font_entry.get()
        mode = self.mode_combobox.current() + 1

        if not url:
            messagebox.showerror("错误", "请输入正确的新闻URL")
            return

        try:
            miner = WordsMiner(
                url=url,
                font_path=font_path or self.font_path,
                stop_words=stopwords_path or "WordsMiner/assets/stopwords.txt",
                crawl_mode=mode
            )
            
            miner.get_content()
            miner.cut_words()
            
            #generate wordcloud
            temp_dir = "WordsMiner/temp"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            temp_file = os.path.join(temp_dir, "temp_wc.png")
            miner.generate_wordcloud(temp_file)
            
            img = Image.open(temp_file)
            img = img.resize((600, 400), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            self.image_label.configure(image=photo)
            self.image_label.image = photo
            self.current_wordcloud = temp_file
            
        except Exception as e:
            messagebox.showerror("生成错误", "生成失败: 请尝试不同的解析模式")

    def save_wordcloud(self):
    #save wordcloud
        if not self.current_wordcloud:
            messagebox.showinfo("提示", "请先生成词云")
            return
            
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG图片", "*.png"), ("所有文件", "*.*")]
        )
        
        if save_path:
            try:
                Image.open(self.current_wordcloud).save(save_path)
                messagebox.showinfo("成功", "词云保存成功！")
            except Exception as e:
                messagebox.showerror("保存错误", f"保存失败：{str(e)}")

class WordsMiner:
    '''wordsMiner can fetch content from url or raw_text, cut words and generate wordcloud.'''

    def __init__(self, url=None, raw_text=None, font_path=None, stop_words=None, crawl_mode=1):
        self.font_path = font_path
        self.stop_words = stop_words
        self.word_str = ""
        self.crawl_mode = crawl_mode 
        #crawl_mode 1 for yueniu news, 2 for gov news

        if url or raw_text:
            self.url = url
            self.raw_text = raw_text
        #url or raw_text must be provided one
        else:
            raise ValueError("url or raw_text must be provided")
    
    def get_content(self):
        # use url to get the raw_text
        raw_text = ""
        crawl_mode = self.crawl_mode
        if self.url:
            try:
                response = requests.get(self.url, timeout=20)
                response.encoding = response.apparent_encoding
                #insure the encoding is correct
                soup = BeautifulSoup(response.text, 'html.parser')
                
                if crawl_mode == 1:
                    # for yueniu news    
                    content_div = soup.find('div', class_='article pre')

                    if content_div:
                        content_p = content_div.find_all('p')
                        for p in content_p:
                            raw_text += p.get_text().strip() + "\n"
                        self.raw_text = raw_text
                    else:
                        print("mode error: cannot fetch content")

                elif crawl_mode == 2:
                    # for gov news
                    content_div = soup.find('div', class_='pages_content')

                    if content_div:
                        content_p = content_div.find_all('p')
                        for p in content_p:
                            raw_text += p.get_text().strip() + "\n"
                        self.raw_text = raw_text
                    else:
                        print("mode error: cannot fetch content")
            
            except Exception as e:
                print(f"request failed, error code: {response.status_code}")

        else:
            pass
            # for no url condition, raw_text is already provided.
    
    def cut_words(self):
        # cut raw_text to split word string(word_str) and filter stop words
        stop_words = self.stop_words or "stopwords.txt"
        if not self.stop_words:
            print("file error: stop_words file is not provided, use default stop_words.txt")
        with open(stop_words, 'r', encoding='utf-8') as f:
            raw_stop_words = f.read().splitlines()
            stop_words = set(raw_stop_words)
            word_list = jieba.lcut(self.raw_text)
            filtered_words = [word for word in word_list if word not in stop_words]
            word_str = " ".join(filtered_words)
            self.word_str = word_str

    def generate_wordcloud(self, output_file=None):
        # use word_str to make visible wordcloud
        wordcloud = WordCloud(
            font_path=self.font_path,
            width=1600,
            height=1200,
            background_color='#f8f9fa',
            colormap='viridis',
            max_words=300,
            contour_width=2,
            contour_color='steelblue',
            scale=3
        ).generate(self.word_str)
        
        if output_file:
            wordcloud.to_file(output_file)
        else:
            plt.figure(figsize=(10, 8))
            plt.imshow(wordcloud, interpolation='bilinear')
            #imshow for image processing and make it more delicate.
            plt.axis('off')

if __name__ == "__main__":
    root = tk.Tk()
    app = WordsMinerGUI(root)
    root.mainloop()