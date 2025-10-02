import tkinter as tk
from tkinter import ttk, messagebox

class WizardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Development Setup Wizard")
        self.root.geometry("700x650")
        self.root.resizable(False, False)
        
        # Configure colors
        self.bg_color = "#f5f5f5"
        self.accent_color = "#4a90e2"
        self.selected_color = "#e3f2fd"
        self.hover_color = "#f0f8ff"
        self.root.configure(bg=self.bg_color)
        
        # Store selections
        self.selections = {
            'language': tk.StringVar(),
            'ide': tk.StringVar(),
            'tools': []
        }
        
        # Track selection frames for visual feedback
        self.language_frames = {}
        self.ide_frames = {}
        
        self.current_page = 0
        self.pages = []
        
        # Create main container
        self.main_frame = tk.Frame(root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Create header
        self.create_header()
        
        # Create progress indicator
        self.create_progress()
        
        # Create content area with fixed height
        self.content_frame = tk.Frame(self.main_frame, bg="white", relief=tk.SOLID, borderwidth=1, height=400)
        self.content_frame.pack(fill=tk.BOTH, expand=False, pady=(15, 0))
        self.content_frame.pack_propagate(False)
        
        # Create navigation buttons BEFORE pages so they're always visible
        self.create_navigation()
        
        # Create pages
        self.create_pages()
        
        # Show first page
        self.show_page(0)
    
    def create_header(self):
        header = tk.Frame(self.main_frame, bg=self.accent_color, height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="🚀 Development Setup Wizard", 
                        font=("Arial", 20, "bold"), 
                        bg=self.accent_color, fg="white")
        title.pack(pady=20)
    
    def create_progress(self):
        progress_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        progress_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.progress_labels = []
        steps = ["Language", "IDE", "Tools", "Summary"]
        
        for i, step in enumerate(steps):
            frame = tk.Frame(progress_frame, bg=self.bg_color)
            frame.pack(side=tk.LEFT, expand=True)
            
            # Circle
            circle = tk.Label(frame, text=str(i+1), font=("Arial", 12, "bold"),
                            bg="white", fg="gray", width=3, height=1,
                            relief=tk.SOLID, borderwidth=2)
            circle.pack()
            
            # Label
            label = tk.Label(frame, text=step, font=("Arial", 9),
                           bg=self.bg_color, fg="gray")
            label.pack()
            
            self.progress_labels.append((circle, label))
    
    def update_progress(self, current_step):
        for i, (circle, label) in enumerate(self.progress_labels):
            if i == current_step:
                circle.config(bg=self.accent_color, fg="white", borderwidth=3)
                label.config(fg="black", font=("Arial", 9, "bold"))
            elif i < current_step:
                circle.config(bg="#90CAF9", fg="white", borderwidth=2)
                label.config(fg="black")
            else:
                circle.config(bg="white", fg="gray", borderwidth=2)
                label.config(fg="gray")
    
    def create_pages(self):
        # Page 1: Language Selection
        page1 = tk.Frame(self.content_frame, bg="white")
        self.create_language_page(page1)
        self.pages.append(page1)
        
        # Page 2: IDE Selection
        page2 = tk.Frame(self.content_frame, bg="white")
        self.create_ide_page(page2)
        self.pages.append(page2)
        
        # Page 3: Tools Selection
        page3 = tk.Frame(self.content_frame, bg="white")
        self.create_tools_page(page3)
        self.pages.append(page3)
        
        # Page 4: Summary
        page4 = tk.Frame(self.content_frame, bg="white")
        self.create_summary_page(page4)
        self.pages.append(page4)
    
    def create_language_page(self, parent):
        # Create a canvas with scrollbar for content
        canvas_frame = tk.Frame(parent, bg="white")
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add content directly without scrollbar since we have enough space
        content = tk.Frame(canvas_frame, bg="white")
        content.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(content, text="Choose Your Programming Language", 
                font=("Arial", 16, "bold"), bg="white", fg="#333").pack(pady=(20, 10))
        
        tk.Label(content, text="Select the language you want to work with", 
                font=("Arial", 10), bg="white", fg="gray").pack(pady=(0, 15))
        
        languages = [
            ("Java", "☕ A versatile, object-oriented language for enterprise applications"),
            ("JavaScript", "⚡ The dynamic language of the web and modern applications"),
            ("COBOL", "💼 Business-oriented language for financial and legacy systems")
        ]
        
        for lang, desc in languages:
            frame = tk.Frame(content, bg="white", relief=tk.SOLID, borderwidth=2, cursor="hand2")
            frame.pack(pady=8, padx=50, fill=tk.X, ipady=5)
            self.language_frames[lang] = frame
            
            # Make entire frame clickable
            frame.bind("<Button-1>", lambda e, l=lang: self.select_language(l))
            frame.bind("<Enter>", lambda e, f=frame: self.on_hover(f))
            frame.bind("<Leave>", lambda e, f=frame: self.on_leave(f))
            
            inner_frame = tk.Frame(frame, bg="white")
            inner_frame.pack(fill=tk.BOTH, padx=20, pady=12)
            inner_frame.bind("<Button-1>", lambda e, l=lang: self.select_language(l))
            
            title_label = tk.Label(inner_frame, text=lang, font=("Arial", 13, "bold"), 
                                  bg="white", fg="#333", anchor="w")
            title_label.pack(anchor=tk.W)
            title_label.bind("<Button-1>", lambda e, l=lang: self.select_language(l))
            
            desc_label = tk.Label(inner_frame, text=desc, font=("Arial", 10), 
                                 bg="white", fg="gray", anchor="w", wraplength=500)
            desc_label.pack(anchor=tk.W, pady=(5, 0))
            desc_label.bind("<Button-1>", lambda e, l=lang: self.select_language(l))
    
    def select_language(self, language):
        self.selections['language'].set(language)
        self.update_language_selection()
    
    def update_language_selection(self):
        selected = self.selections['language'].get()
        for lang, frame in self.language_frames.items():
            if lang == selected:
                frame.config(bg=self.selected_color, borderwidth=3, relief=tk.SOLID)
                for child in frame.winfo_children():
                    self.update_widget_bg(child, self.selected_color)
            else:
                frame.config(bg="white", borderwidth=2, relief=tk.SOLID)
                for child in frame.winfo_children():
                    self.update_widget_bg(child, "white")
    
    def update_widget_bg(self, widget, color):
        try:
            widget.config(bg=color)
            for child in widget.winfo_children():
                self.update_widget_bg(child, color)
        except:
            pass
    
    def on_hover(self, frame):
        if frame.cget('bg') != self.selected_color:
            frame.config(bg=self.hover_color)
            for child in frame.winfo_children():
                self.update_widget_bg(child, self.hover_color)
    
    def on_leave(self, frame):
        if frame.cget('bg') != self.selected_color:
            frame.config(bg="white")
            for child in frame.winfo_children():
                self.update_widget_bg(child, "white")
    
    def create_ide_page(self, parent):
        content = tk.Frame(parent, bg="white")
        content.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(content, text="Choose Your IDE", 
                font=("Arial", 16, "bold"), bg="white", fg="#333").pack(pady=(20, 10))
        
        tk.Label(content, text="Select your preferred development environment", 
                font=("Arial", 10), bg="white", fg="gray").pack(pady=(0, 15))
        
        ides = [
            ("IntelliJ IDEA", "🎯 Powerful IDE with intelligent code assistance"),
            ("Visual Studio Code", "💻 Lightweight, fast, and highly customizable"),
            ("Eclipse", "🌐 Popular open-source IDE with extensive plugins"),
            ("NetBeans", "🔧 Free, open-source, and easy to use")
        ]
        
        for ide, desc in ides:
            frame = tk.Frame(content, bg="white", relief=tk.SOLID, borderwidth=2, cursor="hand2")
            frame.pack(pady=6, padx=50, fill=tk.X, ipady=5)
            self.ide_frames[ide] = frame
            
            # Make entire frame clickable
            frame.bind("<Button-1>", lambda e, i=ide: self.select_ide(i))
            frame.bind("<Enter>", lambda e, f=frame: self.on_hover(f))
            frame.bind("<Leave>", lambda e, f=frame: self.on_leave(f))
            
            inner_frame = tk.Frame(frame, bg="white")
            inner_frame.pack(fill=tk.BOTH, padx=20, pady=10)
            inner_frame.bind("<Button-1>", lambda e, i=ide: self.select_ide(i))
            
            title_label = tk.Label(inner_frame, text=ide, font=("Arial", 12, "bold"), 
                                  bg="white", fg="#333", anchor="w")
            title_label.pack(anchor=tk.W)
            title_label.bind("<Button-1>", lambda e, i=ide: self.select_ide(i))
            
            desc_label = tk.Label(inner_frame, text=desc, font=("Arial", 10), 
                                 bg="white", fg="gray", anchor="w")
            desc_label.pack(anchor=tk.W, pady=(3, 0))
            desc_label.bind("<Button-1>", lambda e, i=ide: self.select_ide(i))
    
    def select_ide(self, ide):
        self.selections['ide'].set(ide)
        self.update_ide_selection()
    
    def update_ide_selection(self):
        selected = self.selections['ide'].get()
        for ide, frame in self.ide_frames.items():
            if ide == selected:
                frame.config(bg=self.selected_color, borderwidth=3, relief=tk.SOLID)
                for child in frame.winfo_children():
                    self.update_widget_bg(child, self.selected_color)
            else:
                frame.config(bg="white", borderwidth=2, relief=tk.SOLID)
                for child in frame.winfo_children():
                    self.update_widget_bg(child, "white")
    
    def create_tools_page(self, parent):
        tk.Label(parent, text="Select Development Tools", 
                font=("Arial", 16, "bold"), bg="white", fg="#333").pack(pady=(30, 10))
        
        tk.Label(parent, text="Choose the tools you want to use (select all that apply)", 
                font=("Arial", 10), bg="white", fg="gray").pack(pady=(0, 25))
        
        tools = [
            ("Git", "📦 Version control system"),
            ("Docker", "🐳 Container platform"),
            ("Maven", "🔨 Build automation for Java"),
            ("Gradle", "⚙️ Modern build tool"),
            ("npm", "📚 Node package manager"),
            ("JUnit", "✅ Testing framework"),
            ("Postman", "🚀 API testing tool")
        ]
        
        self.tool_vars = {}
        
        tools_container = tk.Frame(parent, bg="white")
        tools_container.pack(pady=10, padx=50)
        
        for i, (tool, desc) in enumerate(tools):
            var = tk.BooleanVar()
            self.tool_vars[tool] = var
            
            frame = tk.Frame(tools_container, bg="white")
            frame.grid(row=i, column=0, sticky=tk.W, pady=8, padx=10)
            
            cb = tk.Checkbutton(frame, text=tool, variable=var,
                               font=("Arial", 12, "bold"), bg="white",
                               activebackground="white", selectcolor=self.accent_color,
                               cursor="hand2")
            cb.pack(side=tk.LEFT)
            
            desc_label = tk.Label(frame, text=desc, font=("Arial", 9), 
                                 bg="white", fg="gray")
            desc_label.pack(side=tk.LEFT, padx=(10, 0))
    
    def create_summary_page(self, parent):
        tk.Label(parent, text="✨ Setup Summary", 
                font=("Arial", 16, "bold"), bg="white", fg="#333").pack(pady=(30, 10))
        
        tk.Label(parent, text="Review your selections before finishing", 
                font=("Arial", 10), bg="white", fg="gray").pack(pady=(0, 20))
        
        self.summary_text = tk.Text(parent, height=14, width=55, 
                                   font=("Arial", 11), bg="#f9f9f9",
                                   relief=tk.SOLID, borderwidth=1, padx=25, pady=20,
                                   wrap=tk.WORD)
        self.summary_text.pack(pady=10, padx=40)
        self.summary_text.config(state=tk.DISABLED)
    
    def create_navigation(self):
        nav_frame = tk.Frame(self.main_frame, bg=self.bg_color, height=60)
        nav_frame.pack(fill=tk.X, pady=(15, 0))
        nav_frame.pack_propagate(False)
        
        self.back_btn = tk.Button(nav_frame, text="← Back", command=self.prev_page,
                                  font=("Arial", 11, "bold"), bg="white", fg="#333",
                                  relief=tk.SOLID, borderwidth=1, padx=25, pady=10,
                                  cursor="hand2")
        self.back_btn.pack(side=tk.LEFT, pady=10)
        
        self.next_btn = tk.Button(nav_frame, text="Next →", command=self.next_page,
                                  font=("Arial", 11, "bold"), bg=self.accent_color, fg="white",
                                  relief=tk.SOLID, borderwidth=0, padx=25, pady=10,
                                  cursor="hand2")
        self.next_btn.pack(side=tk.RIGHT, pady=10)
    
    def show_page(self, page_num):
        for page in self.pages:
            page.pack_forget()
        
        self.pages[page_num].pack(fill=tk.BOTH, expand=True)
        self.current_page = page_num
        
        # Update progress indicator
        self.update_progress(page_num)
        
        # Update buttons
        self.back_btn.config(state=tk.NORMAL if page_num > 0 else tk.DISABLED)
        
        if page_num == len(self.pages) - 1:
            self.next_btn.config(text="✓ Finish", command=self.finish)
        else:
            self.next_btn.config(text="Next →", command=self.next_page)
        
        # Update summary if on last page
        if page_num == len(self.pages) - 1:
            self.update_summary()
    
    def next_page(self):
        # Validate current page
        if self.current_page == 0 and not self.selections['language'].get():
            messagebox.showwarning("Selection Required", "Please select a programming language.")
            return
        if self.current_page == 1 and not self.selections['ide'].get():
            messagebox.showwarning("Selection Required", "Please select an IDE.")
            return
        
        if self.current_page < len(self.pages) - 1:
            self.show_page(self.current_page + 1)
    
    def prev_page(self):
        if self.current_page > 0:
            self.show_page(self.current_page - 1)
    
    def update_summary(self):
        selected_tools = [tool for tool, var in self.tool_vars.items() if var.get()]
        
        summary = "═" * 50 + "\n\n"
        summary += "📋 YOUR DEVELOPMENT SETUP\n\n"
        summary += "═" * 50 + "\n\n"
        
        summary += f"Programming Language:\n"
        summary += f"  ▸ {self.selections['language'].get() or 'Not selected'}\n\n"
        
        summary += f"IDE:\n"
        summary += f"  ▸ {self.selections['ide'].get() or 'Not selected'}\n\n"
        
        summary += f"Development Tools:\n"
        if selected_tools:
            for tool in selected_tools:
                summary += f"  ▸ {tool}\n"
        else:
            summary += "  ▸ None selected\n"
        
        summary += "\n" + "═" * 50
        
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(1.0, summary)
        self.summary_text.config(state=tk.DISABLED)
    
    def finish(self):
        selected_tools = [tool for tool, var in self.tool_vars.items() if var.get()]
        tools_str = ", ".join(selected_tools) if selected_tools else "None"
        
        messagebox.showinfo("🎉 Setup Complete!", 
                          "Your development environment has been configured!\n\n" +
                          f"Language: {self.selections['language'].get()}\n" +
                          f"IDE: {self.selections['ide'].get()}\n" +
                          f"Tools: {tools_str}")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = WizardApp(root)
    root.mainloop()
