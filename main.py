import random
import string
import tkinter as tk
from tkinter import messagebox
from typing import List

def create_crossword(words: List[str]) -> List[List[str]]:
    SIZE = 10
    grid = [['' for _ in range(SIZE)] for _ in range(SIZE)]
    directions = [
        (0, 1), (1, 0), (1, 1), (1, -1),
        (0, -1), (-1, 0), (-1, -1), (-1, 1)
    ]

    def can_place(word, row, col, dr, dc):
        for i in range(len(word)):
            r, c = row + dr * i, col + dc * i
            if not (0 <= r < SIZE and 0 <= c < SIZE):
                return False
            if grid[r][c] not in ('', word[i]):
                return False
        return True

    def place_word(word):
        tries = 0
        while tries < 100:
            dr, dc = random.choice(directions)
            row = random.randint(0, SIZE - 1)
            col = random.randint(0, SIZE - 1)
            if can_place(word, row, col, dr, dc):
                for i in range(len(word)):
                    r, c = row + dr * i, col + dc * i
                    grid[r][c] = word[i]
                return True
            tries += 1
        return False

    for word in words:
        word = word.upper()
        place_word(word)

    for r in range(SIZE):
        for c in range(SIZE):
            if grid[r][c] == '':
                grid[r][c] = random.choice(string.ascii_uppercase)
    return grid

def show_puzzle_ui(grid, words, time_limit=None):
    SIZE = len(grid)
    root = tk.Tk()
    root.title("🔍 Word Search Puzzle")
    root.configure(bg='#2c3e50')  # Dark blue-gray background
    root.state('zoomed')  # Maximize window
    
    # Modern styling
    style_config = {
        'bg': '#2c3e50',
        'fg': '#ecf0f1',
        'font': ('Segoe UI', 12)
    }

    # Main container
    container = tk.Frame(root, bg='#2c3e50')
    container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Title and Timer
    header_frame = tk.Frame(container, bg='#2c3e50')
    header_frame.pack(pady=(0, 20), fill='x')
    
    title_label = tk.Label(header_frame, text="🎯 WORD SEARCH PUZZLE", 
                          font=('Segoe UI', 20, 'bold'), 
                          bg='#2c3e50', fg='#e74c3c')
    title_label.pack(side='left')
    
    # Right side frame for timer and end game button
    right_frame = tk.Frame(header_frame, bg='#2c3e50')
    right_frame.pack(side='right')
    
    # Custom confirmation dialog
    def show_custom_confirmation():
        """Show custom confirmation dialog instead of default messagebox"""
        # Create confirmation popup
        confirm_popup = tk.Toplevel(root)
        confirm_popup.title("⚠️ Confirm End Game")
        confirm_popup.configure(bg='#2c3e50')
        confirm_popup.geometry("450x200")
        confirm_popup.transient(root)
        confirm_popup.grab_set()
        confirm_popup.resizable(False, False)
        
        # Center the popup
        confirm_popup.update_idletasks()
        x = root.winfo_x() + (root.winfo_width() // 2) - (confirm_popup.winfo_width() // 2)
        y = root.winfo_y() + (root.winfo_height() // 2) - (confirm_popup.winfo_height() // 2)
        confirm_popup.geometry(f"+{x}+{y}")
        
        # Warning message
        tk.Label(confirm_popup, text="⚠️ End Current Game?", 
                font=('Segoe UI', 16, 'bold'), 
                bg='#2c3e50', fg='#f39c12').pack(pady=20)
        
        tk.Label(confirm_popup, text="This will end your current progress.", 
                font=('Segoe UI', 12), 
                bg='#2c3e50', fg='#ecf0f1').pack(pady=5)
        
        # Button frame
        button_frame = tk.Frame(confirm_popup, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        def confirm_yes():
            timer_running[0] = False
            confirm_popup.destroy()
            show_mid_game_end_message()
        
        def confirm_no():
            confirm_popup.destroy()
        
        # Yes button
        tk.Button(button_frame, text="✅ Yes, End Game", 
                 font=('Segoe UI', 11, 'bold'),
                 bg='#e74c3c', fg='white',
                 relief='flat', bd=0, padx=20, pady=8,
                 cursor='hand2',
                 command=confirm_yes).pack(side='left', padx=10)
        
        # No button
        tk.Button(button_frame, text="❌ No, Continue", 
                 font=('Segoe UI', 11, 'bold'),
                 bg='#27ae60', fg='white',
                 relief='flat', bd=0, padx=20, pady=8,
                 cursor='hand2',
                 command=confirm_no).pack(side='left', padx=10)
    
    # Try Again confirmation dialog
    def show_try_again_confirmation():
        """Show custom confirmation dialog for Try Again"""
        # Create confirmation popup
        confirm_popup = tk.Toplevel(root)
        confirm_popup.title("🔄 Confirm Try Again")
        confirm_popup.configure(bg='#2c3e50')
        confirm_popup.geometry("450x200")
        confirm_popup.transient(root)
        confirm_popup.grab_set()
        confirm_popup.resizable(False, False)
        
        # Center the popup
        confirm_popup.update_idletasks()
        x = root.winfo_x() + (root.winfo_width() // 2) - (confirm_popup.winfo_width() // 2)
        y = root.winfo_y() + (root.winfo_height() // 2) - (confirm_popup.winfo_height() // 2)
        confirm_popup.geometry(f"+{x}+{y}")
        
        # Warning message
        tk.Label(confirm_popup, text="🔄 Start New Game?", 
                font=('Segoe UI', 16, 'bold'), 
                bg='#2c3e50', fg='#f39c12').pack(pady=20)
        
        tk.Label(confirm_popup, text="This will restart the game with new settings.", 
                font=('Segoe UI', 12), 
                bg='#2c3e50', fg='#ecf0f1').pack(pady=5)
        
        # Button frame
        button_frame = tk.Frame(confirm_popup, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        def confirm_try_again():
            timer_running[0] = False
            confirm_popup.destroy()
            root.destroy()
            main()
        
        def cancel_try_again():
            confirm_popup.destroy()
        
        # Yes button
        tk.Button(button_frame, text="✅ Yes, Try Again", 
                 font=('Segoe UI', 11, 'bold'),
                 bg='#f39c12', fg='white',
                 relief='flat', bd=0, padx=20, pady=8,
                 cursor='hand2',
                 command=confirm_try_again).pack(side='left', padx=10)
        
        # No button
        tk.Button(button_frame, text="❌ No, Continue", 
                 font=('Segoe UI', 11, 'bold'),
                 bg='#27ae60', fg='white',
                 relief='flat', bd=0, padx=20, pady=8,
                 cursor='hand2',
                 command=cancel_try_again).pack(side='left', padx=10)
    
    # Try Again button
    try_again_btn = tk.Button(right_frame, text="🔄 Try Again", 
                             font=('Segoe UI', 10, 'bold'),
                             bg='#f39c12', fg='white',
                             relief='flat', bd=0, padx=15, pady=5,
                             cursor='hand2',
                             command=show_try_again_confirmation)
    try_again_btn.pack(side='right', padx=(0, 10))
    
    # End Game button
    end_game_btn = tk.Button(right_frame, text="🚪 End Game", 
                            font=('Segoe UI', 10, 'bold'),
                            bg='#e74c3c', fg='white',
                            relief='flat', bd=0, padx=15, pady=5,
                            cursor='hand2',
                            command=show_custom_confirmation)
    end_game_btn.pack(side='right', padx=(0, 10))
    
    # Timer display
    timer_label = tk.Label(right_frame, text="", 
                          font=('Segoe UI', 16, 'bold'), 
                          bg='#2c3e50', fg='#f39c12')
    timer_label.pack(side='right')
    
    # Timer variables
    start_time = [None]
    timer_running = [True]
    
    def update_timer():
        if not timer_running[0]:
            return
            
        if time_limit is None:
            # Unlimited time - show elapsed time
            if start_time[0] is None:
                start_time[0] = root.tk.call('clock', 'seconds')
            elapsed = root.tk.call('clock', 'seconds') - start_time[0]
            mins, secs = divmod(elapsed, 60)
            timer_label.config(text=f"⏱️ {mins:02d}:{secs:02d}")
        else:
            # Limited time - show countdown
            if start_time[0] is None:
                start_time[0] = root.tk.call('clock', 'seconds')
            elapsed = root.tk.call('clock', 'seconds') - start_time[0]
            remaining = max(0, time_limit - elapsed)
            
            if remaining <= 0:
                timer_label.config(text="⏰ TIME'S UP!", fg='#e74c3c')
                show_time_up_message()
                return
            
            mins, secs = divmod(remaining, 60)
            color = '#e74c3c' if remaining <= 30 else '#f39c12'
            timer_label.config(text=f"⏰ {mins:02d}:{secs:02d}", fg=color)
        
        root.after(1000, update_timer)
    
    # Start timer
    root.after(1000, update_timer)
    
    # Handle window close button (red X)
    def on_window_close():
        """Handle window close event - stop timer and close cleanly"""
        timer_running[0] = False
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_window_close)

    # Content frame
    content_frame = tk.Frame(container, bg='#2c3e50')
    content_frame.pack(fill=tk.BOTH, expand=True)

    # Puzzle frame with border
    puzzle_container = tk.Frame(content_frame, bg='#34495e', relief='raised', bd=2)
    puzzle_container.pack(side=tk.LEFT, padx=(0, 30), pady=10)
    
    puzzle_title = tk.Label(puzzle_container, text="📋 PUZZLE GRID", 
                           font=('Segoe UI', 14, 'bold'), 
                           bg='#34495e', fg='#ecf0f1')
    puzzle_title.pack(pady=10)

    main_frame = tk.Frame(puzzle_container, bg='#34495e')
    main_frame.pack(padx=20, pady=(0, 20))

    # Word list frame with modern styling
    word_container = tk.Frame(content_frame, bg='#34495e', relief='raised', bd=2, width=250)
    word_container.pack(side=tk.RIGHT, fill=tk.Y, padx=(30, 0), pady=10)
    word_container.pack_propagate(False)
    
    word_title = tk.Label(word_container, text="📝 WORDS TO FIND", 
                         font=('Segoe UI', 14, 'bold'), 
                         bg='#34495e', fg='#ecf0f1')
    word_title.pack(pady=15)

    word_frame = tk.Frame(word_container, bg='#34495e')
    word_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    word_vars = []
    word_labels = []
    for i, w in enumerate(words):
        var = tk.StringVar(value=f"• {w.upper()}")
        lbl = tk.Label(word_frame, textvariable=var, 
                      font=('Segoe UI', 11), 
                      bg='#34495e', fg='#bdc3c7',
                      anchor='w', justify='left')
        lbl.pack(anchor="w", pady=2, fill='x')
        word_vars.append(var)
        word_labels.append(lbl)

    # For selection and animation
    selected = []
    labels = [[None for _ in range(SIZE)] for _ in range(SIZE)]
    found_words = set()
    selection_start = [None]
    animation_colors = ['#f39c12', '#e67e22', '#d35400', '#e74c3c', '#c0392b']
    
    # Rainbow colors for different words
    word_colors = [
        '#e74c3c',  # Red
        '#3498db',  # Blue  
        '#2ecc71',  # Green
        '#f39c12',  # Orange
        '#9b59b6',  # Purple
        '#1abc9c',  # Turquoise
        '#e67e22',  # Dark Orange
        '#34495e',  # Dark Blue
        '#27ae60',  # Dark Green
        '#d35400',  # Dark Orange
        '#8e44ad',  # Dark Purple
        '#16a085',  # Dark Turquoise
        '#c0392b',  # Dark Red
        '#2980b9',  # Darker Blue
        '#f1c40f'   # Yellow
    ]
    
    # Track which color each found word uses
    word_color_map = {}
    
    def is_found_word_cell(r, c):
        """Check if a cell is part of any found word"""
        return any(word_color in labels[r][c]["fg"] for word_color in word_colors)
    
    def reset_selection():
        for r, c in selected:
            # Check if this cell is part of any found word
            if not is_found_word_cell(r, c):
                labels[r][c]["bg"] = "#ecf0f1"
                labels[r][c]["fg"] = "#2c3e50"
                labels[r][c]["borderwidth"] = 2
                labels[r][c]["highlightthickness"] = 0
        selected.clear()
        selection_start[0] = None

    def highlight_selection(color):
        for r, c in selected:
            # Only highlight if not already part of a found word
            if not is_found_word_cell(r, c):
                labels[r][c]["bg"] = color
    
    def highlight_found_word(cells, word_idx):
        """Instantly highlight found word with unique color"""
        # Get unique color for this word
        word_color = word_colors[len(found_words) % len(word_colors)]
        word_color_map[word_idx] = word_color
        
        # Create a lighter background color based on the word color
        def hex_to_light_bg(hex_color):
            # Convert hex to RGB, then create a very light version
            hex_color = hex_color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            # Make it very light (closer to white)
            light_r = min(255, r + 200)
            light_g = min(255, g + 200)
            light_b = min(255, b + 200)
            return f"#{light_r:02x}{light_g:02x}{light_b:02x}"
        
        light_bg = hex_to_light_bg(word_color)
        
        # Instantly apply the final styling
        for r, c in cells:
            labels[r][c]["bg"] = light_bg  # Light version of the word's color
            labels[r][c]["fg"] = word_color   # Word's unique color for text
            labels[r][c]["relief"] = "solid"
            labels[r][c]["borderwidth"] = 3
            labels[r][c]["highlightbackground"] = word_color
            labels[r][c]["highlightthickness"] = 2
            labels[r][c]["font"] = ('Segoe UI', 16, 'bold')
        
        # Update word list instantly
        animate_word_found(word_idx, word_color)
        
        # Check if all words are found
        if len(found_words) == len(words):
            timer_running[0] = False
            show_completion_message()
    
    def animate_word_found(word_idx, word_color):
        """Animate the word being crossed out with matching color"""
        # First, briefly highlight with the word's color
        word_labels[word_idx]["fg"] = word_color
        word_labels[word_idx]["font"] = ('Segoe UI', 11, 'bold')
        
        def strike_through():
            # Add checkmark with the same color as the circled word
            word_vars[word_idx].set(f"✓ {words[word_idx].upper()}")
            word_labels[word_idx]["fg"] = word_color  # Keep the same color as the circle
        
        root.after(400, strike_through)
    
    def show_completion_message():
        """Show immediate completion message when all words are found"""
        # Calculate time taken
        if start_time[0] is not None:
            elapsed = root.tk.call('clock', 'seconds') - start_time[0]
            mins, secs = divmod(elapsed, 60)
            time_text = f"⏰ Completed in {mins:02d}:{secs:02d}"
        else:
            time_text = "⏰ Puzzle Completed!"
        
        # Create completion popup
        popup = tk.Toplevel(root)
        popup.title("🎉 Congratulations!")
        popup.configure(bg='#2c3e50')
        popup.geometry("600x500")
        popup.transient(root)
        popup.grab_set()
        
        # Center the popup
        popup.update_idletasks()
        x = root.winfo_x() + (root.winfo_width() // 2) - (popup.winfo_width() // 2)
        y = root.winfo_y() + (root.winfo_height() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")
        
        # Main congratulations message
        tk.Label(popup, text="🎉 PUZZLE COMPLETED! 🎉", 
                font=('Segoe UI', 20, 'bold'), 
                bg='#2c3e50', fg='#27ae60').pack(pady=30)
        
        # Time display
        tk.Label(popup, text=time_text, 
                font=('Segoe UI', 16, 'bold'), 
                bg='#2c3e50', fg='#f39c12').pack(pady=10)
        
        # Performance message
        if start_time[0] is not None:
            elapsed = root.tk.call('clock', 'seconds') - start_time[0]
            if elapsed < 120:  # Less than 2 minutes
                perf_msg = "🚀 LIGHTNING FAST!"
                perf_color = '#e74c3c'
            elif elapsed < 300:  # Less than 5 minutes
                perf_msg = "⚡ EXCELLENT SPEED!"
                perf_color = '#f39c12'
            else:
                perf_msg = "🎯 GREAT JOB!"
                perf_color = '#27ae60'
            
            tk.Label(popup, text=perf_msg, 
                    font=('Segoe UI', 14, 'bold'), 
                    bg='#2c3e50', fg=perf_color).pack(pady=5)
        
        # Appreciation messages
        appreciation_frame = tk.Frame(popup, bg='#2c3e50')
        appreciation_frame.pack(pady=20)
        
        tk.Label(appreciation_frame, text="🌟 We appreciate your time and effort!", 
                font=('Segoe UI', 13, 'italic'), 
                bg='#2c3e50', fg='#e8b4f0').pack()
        
        tk.Label(appreciation_frame, text="✨ Every puzzle you play helps you grow!", 
                font=('Segoe UI', 13, 'italic'), 
                bg='#2c3e50', fg='#a8e6cf').pack()
        
        tk.Label(appreciation_frame, text="🎊 Thank you for being an awesome player!", 
                font=('Segoe UI', 13, 'italic'), 
                bg='#2c3e50', fg='#ffd3a5').pack()
        
        # Button frame for OK and Try Again buttons
        button_frame = tk.Frame(popup, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        # Try Again button
        tk.Button(button_frame, text="🔄 Try Again", 
                 font=('Segoe UI', 14, 'bold'),
                 bg='#f39c12', fg='white',
                 relief='flat', bd=0, padx=30, pady=12,
                 cursor='hand2',
                 command=lambda: (popup.destroy(), root.destroy(), main())).pack(side='left', padx=10)
        
        # OK button to close everything
        tk.Button(button_frame, text="✅ OK", 
                 font=('Segoe UI', 14, 'bold'),
                 bg='#27ae60', fg='white',
                 relief='flat', bd=0, padx=40, pady=12,
                 cursor='hand2',
                 command=lambda: (popup.destroy(), root.destroy())).pack(side='left', padx=10)
    
    def show_time_up_message():
        """Show time up message when timer expires"""
        timer_running[0] = False
        
        # Create time up popup
        popup = tk.Toplevel(root)
        popup.title("⏰ Time's Up!")
        popup.configure(bg='#2c3e50')
        popup.geometry("500x400")
        popup.transient(root)
        popup.grab_set()
        
        # Center the popup
        popup.update_idletasks()
        x = root.winfo_x() + (root.winfo_width() // 2) - (popup.winfo_width() // 2)
        y = root.winfo_y() + (root.winfo_height() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")
        
        tk.Label(popup, text="⏰ TIME'S UP! ⏰", 
                font=('Segoe UI', 18, 'bold'), 
                bg='#2c3e50', fg='#e74c3c').pack(pady=20)
        
        found_count = len(found_words)
        tk.Label(popup, text=f"You found {found_count} out of {len(words)} words", 
                font=('Segoe UI', 14), 
                bg='#2c3e50', fg='#ecf0f1').pack(pady=10)
        
        if found_count > 0:
            percentage = (found_count / len(words)) * 100
            tk.Label(popup, text=f"Score: {percentage:.1f}%", 
                    font=('Segoe UI', 14, 'bold'), 
                    bg='#2c3e50', fg='#f39c12').pack(pady=10)
        
        tk.Button(popup, text="🚀 Try Again", 
                 font=('Segoe UI', 12, 'bold'),
                 bg='#e74c3c', fg='white',
                 relief='flat', bd=0, padx=20, pady=10,
                 cursor='hand2',
                 command=lambda: (popup.destroy(), root.destroy(), main())).pack(pady=20)
    
    def show_mid_game_end_message():
        """Show immediate thank you message when game is ended mid-way"""
        # Create end game popup
        popup = tk.Toplevel(root)
        popup.title("👋 Game Ended")
        popup.configure(bg='#2c3e50')
        popup.geometry("550x450")
        popup.transient(root)
        popup.grab_set()
        
        # Center the popup
        popup.update_idletasks()
        x = root.winfo_x() + (root.winfo_width() // 2) - (popup.winfo_width() // 2)
        y = root.winfo_y() + (root.winfo_height() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")
        
        # Main thank you message
        tk.Label(popup, text="🙏 THANK YOU FOR PARTICIPATING! 🙏", 
                font=('Segoe UI', 18, 'bold'), 
                bg='#2c3e50', fg='#3498db').pack(pady=30)
        
        # Game stats
        found_count = len(found_words)
        tk.Label(popup, text=f"📊 Words Found: {found_count} out of {len(words)}", 
                font=('Segoe UI', 14), 
                bg='#2c3e50', fg='#ecf0f1').pack(pady=10)
        
        if found_count > 0:
            percentage = (found_count / len(words)) * 100
            tk.Label(popup, text=f"🎯 Progress: {percentage:.1f}%", 
                    font=('Segoe UI', 14, 'bold'), 
                    bg='#2c3e50', fg='#f39c12').pack(pady=5)
        
        # Encouraging message
        if found_count == 0:
            msg = "🌱 Every expert was once a beginner!"
        elif found_count > 0:
            percentage = (found_count / len(words)) * 100
            if percentage < 25:
                msg = "🚀 Great start! Practice makes perfect!"
            elif percentage < 50:
                msg = "⭐ Good progress! You're getting there!"
            elif percentage < 75:
                msg = "🔥 Excellent work! Almost there!"
            else:
                msg = "🏆 Outstanding! You were so close!"
        
        tk.Label(popup, text=msg, 
                font=('Segoe UI', 12, 'italic'), 
                bg='#2c3e50', fg='#bdc3c7').pack(pady=10)
        
        # Appreciation messages
        appreciation_frame = tk.Frame(popup, bg='#2c3e50')
        appreciation_frame.pack(pady=20)
        
        tk.Label(appreciation_frame, text="💝 We appreciate your time and effort!", 
                font=('Segoe UI', 13, 'italic'), 
                bg='#2c3e50', fg='#e8b4f0').pack()
        
        tk.Label(appreciation_frame, text="🌟 Every puzzle you play helps you grow!", 
                font=('Segoe UI', 13, 'italic'), 
                bg='#2c3e50', fg='#a8e6cf').pack()
        
        tk.Label(appreciation_frame, text="🚀 Thank you for being an awesome player!", 
                font=('Segoe UI', 13, 'italic'), 
                bg='#2c3e50', fg='#ffd3a5').pack()
        
        # Button frame for OK and Try Again buttons
        button_frame = tk.Frame(popup, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        # Try Again button
        tk.Button(button_frame, text="🔄 Try Again", 
                 font=('Segoe UI', 14, 'bold'),
                 bg='#f39c12', fg='white',
                 relief='flat', bd=0, padx=30, pady=12,
                 cursor='hand2',
                 command=lambda: (popup.destroy(), root.destroy(), main())).pack(side='left', padx=10)
        
        # OK button to close everything
        tk.Button(button_frame, text="✅ OK", 
                 font=('Segoe UI', 14, 'bold'),
                 bg='#3498db', fg='white',
                 relief='flat', bd=0, padx=40, pady=12,
                 cursor='hand2',
                 command=lambda: (popup.destroy(), root.destroy())).pack(side='left', padx=10)

    def on_cell_press(event, r, c):
        reset_selection()
        selection_start[0] = (r, c)
        selected.append((r, c))
        highlight_selection('#3498db')  # Blue highlight

    def on_cell_enter(event, r, c):
        if selection_start[0] is not None:
            start_r, start_c = selection_start[0]
            dr = r - start_r
            dc = c - start_c
            length = max(abs(dr), abs(dc))
            if length == 0:
                temp = [(start_r, start_c)]
            else:
                dr = (dr // length) if dr != 0 else 0
                dc = (dc // length) if dc != 0 else 0
                temp = []
                for i in range(length + 1):
                    nr = start_r + dr * i
                    nc = start_c + dc * i
                    if 0 <= nr < SIZE and 0 <= nc < SIZE:
                        temp.append((nr, nc))
            # Only update if the path is straight
            if (r == start_r or c == start_c or abs(r - start_r) == abs(c - start_c)):
                for rr, cc in selected:
                    # Don't reset found words (any color)
                    if not is_found_word_cell(rr, cc):
                        labels[rr][cc]["bg"] = "#ecf0f1"
                        labels[rr][cc]["fg"] = "#2c3e50"
                        labels[rr][cc]["borderwidth"] = 2
                        labels[rr][cc]["highlightthickness"] = 0
                selected.clear()
                for nr, nc in temp:
                    selected.append((nr, nc))
                highlight_selection('#3498db')

    def on_cell_release(event, r, c):
        if not selected:
            reset_selection()
            return
        word = ''.join([grid[r][c] for r, c in selected])
        rev_word = word[::-1]
        match_idx = -1
        for idx, w in enumerate(words):
            if w.upper() == word or w.upper() == rev_word:
                match_idx = idx
                break
        if match_idx != -1 and match_idx not in found_words:
            # Add the word to found_words first
            found_words.add(match_idx)
            # Then highlight the found word with unique color
            highlight_found_word(selected.copy(), match_idx)
        else:
            reset_selection()

    def get_cell_from_widget(widget):
        # Find which cell this widget corresponds to
        for r in range(SIZE):
            for c in range(SIZE):
                if labels[r][c] == widget:
                    return r, c
        return None, None

    def on_motion(event):
        # Get the widget under the mouse
        widget = event.widget.winfo_containing(event.x_root, event.y_root)
        if widget and hasattr(widget, 'grid_info'):
            r, c = get_cell_from_widget(widget)
            if r is not None and c is not None:
                on_cell_enter(event, r, c)

    for r in range(SIZE):
        for c in range(SIZE):
            label = tk.Label(
                main_frame, 
                text=grid[r][c], 
                width=3, 
                height=2, 
                font=('Segoe UI', 16, 'bold'), 
                bg='#ecf0f1',
                fg='#2c3e50',
                borderwidth=2, 
                relief="solid",
                cursor="hand2"
            )
            label.grid(row=r, column=c, padx=1, pady=1)
            
            # Smooth hover effect
            def on_enter_cell(event, lbl=label, r=r, c=c):
                # Don't hover over found words or currently selected cells
                if (not is_found_word_cell(r, c) and lbl["bg"] != "#3498db"):
                    lbl["bg"] = "#d5dbdb"
            
            def on_leave_cell(event, lbl=label, r=r, c=c):
                # Don't reset found words or currently selected cells
                if (not is_found_word_cell(r, c) and lbl["bg"] != "#3498db"):
                    lbl["bg"] = "#ecf0f1"
            
            label.bind('<Enter>', on_enter_cell)
            label.bind('<Leave>', on_leave_cell)
            label.bind('<Button-1>', lambda e, r=r, c=c: on_cell_press(e, r, c))
            label.bind('<B1-Motion>', on_motion)
            label.bind('<ButtonRelease-1>', lambda e, r=r, c=c: on_cell_release(e, r, c))
            
            labels[r][c] = label

    root.mainloop()



def get_game_settings():
    """Get game settings: number of words and timer"""
    settings = {'num_words': 15, 'time_limit': None}
    
    setup_window = tk.Tk()
    setup_window.title("🎮 Game Setup")
    setup_window.configure(bg='#2c3e50')
    setup_window.state('zoomed')  # Maximize window
    
    # Title
    title_label = tk.Label(setup_window, text="🎮 Word Search Setup", 
                          font=('Segoe UI', 20, 'bold'), 
                          bg='#2c3e50', fg='#e74c3c')
    title_label.pack(pady=20)
    
    # Number of words selection
    words_frame = tk.Frame(setup_window, bg='#2c3e50')
    words_frame.pack(pady=20)
    
    tk.Label(words_frame, text="📝 Number of Words:", 
            font=('Segoe UI', 14, 'bold'),
            bg='#2c3e50', fg='#ecf0f1').pack()
    
    word_options = [5, 8, 10, 12, 15, 18, 20]
    word_var = tk.IntVar(value=15)
    
    words_option_frame = tk.Frame(words_frame, bg='#2c3e50')
    words_option_frame.pack(pady=10)
    
    for i, option in enumerate(word_options):
        rb = tk.Radiobutton(words_option_frame, text=f"{option} words", 
                           variable=word_var, value=option,
                           font=('Segoe UI', 11),
                           bg='#2c3e50', fg='#bdc3c7',
                           selectcolor='#34495e',
                           activebackground='#2c3e50',
                           activeforeground='#ecf0f1')
        if i < 4:
            rb.grid(row=0, column=i, padx=10)
        else:
            rb.grid(row=1, column=i-4, padx=10)
    
    # Timer selection
    timer_frame = tk.Frame(setup_window, bg='#2c3e50')
    timer_frame.pack(pady=20)
    
    tk.Label(timer_frame, text="⏰ Timer:", 
            font=('Segoe UI', 14, 'bold'),
            bg='#2c3e50', fg='#ecf0f1').pack()
    
    timer_options = [
        ("Unlimited", None),
        ("2 minutes", 120),
        ("3 minutes", 180),
        ("5 minutes", 300),
        ("7 minutes", 420),
        ("10 minutes", 600)
    ]
    timer_var = tk.StringVar(value="Unlimited")
    
    timer_option_frame = tk.Frame(timer_frame, bg='#2c3e50')
    timer_option_frame.pack(pady=10)
    
    for i, (text, value) in enumerate(timer_options):
        rb = tk.Radiobutton(timer_option_frame, text=text, 
                           variable=timer_var, value=text,
                           font=('Segoe UI', 11),
                           bg='#2c3e50', fg='#bdc3c7',
                           selectcolor='#34495e',
                           activebackground='#2c3e50',
                           activeforeground='#ecf0f1')
        if i < 3:
            rb.grid(row=0, column=i, padx=15)
        else:
            rb.grid(row=1, column=i-3, padx=15)
    
    def start_game():
        settings['num_words'] = word_var.get()
        # Convert timer selection to seconds
        timer_map = dict(timer_options)
        settings['time_limit'] = timer_map[timer_var.get()]
        setup_window.destroy()
    
    tk.Button(setup_window, text="🚀 Start Game", 
             font=('Segoe UI', 14, 'bold'),
             bg='#27ae60', fg='white',
             relief='flat', bd=0, padx=30, pady=15,
             cursor='hand2',
             command=start_game).pack(pady=30)
    
    # Handle window close button (red X)
    def on_setup_window_close():
        """Handle setup window close event - exit application"""
        setup_window.destroy()
        exit()
    
    setup_window.protocol("WM_DELETE_WINDOW", on_setup_window_close)
    
    setup_window.mainloop()
    return settings

def get_words_from_user(num_words=15):
    def submit():
        user_words = [entry.get().strip() for entry in entries]
        if all(user_words) and len(user_words) == num_words:
            nonlocal words
            words = user_words
            input_window.destroy()

    def on_enter(event, current_index):
        # Move to next entry or submit if last one
        if current_index < num_words - 1:
            entries[current_index + 1].focus_set()
        else:
            submit()

    words = []
    input_window = tk.Tk()
    input_window.title("📝 Word Search Creator")
    input_window.configure(bg='#2c3e50')
    input_window.state('zoomed')  # Maximize window
    
    # Title
    title_label = tk.Label(input_window, text="🎯 Enter Your Words", 
                          font=('Segoe UI', 18, 'bold'), 
                          bg='#2c3e50', fg='#e74c3c')
    title_label.grid(row=0, column=0, columnspan=2, pady=20)
    
    subtitle_label = tk.Label(input_window, text=f"Enter {num_words} words for your puzzle", 
                             font=('Segoe UI', 11), 
                             bg='#2c3e50', fg='#bdc3c7')
    subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
    
    entries = []
    
    for i in range(num_words):
        label = tk.Label(input_window, text=f"Word {i+1}:", 
                        font=('Segoe UI', 11, 'bold'),
                        bg='#2c3e50', fg='#ecf0f1')
        label.grid(row=i+2, column=0, padx=15, pady=3, sticky='e')
        
        entry = tk.Entry(input_window, width=25, font=('Segoe UI', 11),
                        bg='#ecf0f1', fg='#2c3e50', 
                        relief='flat', bd=5)
        entry.grid(row=i+2, column=1, padx=15, pady=3, sticky='w')
        
        # Bind Enter key to move to next field
        entry.bind('<Return>', lambda e, idx=i: on_enter(e, idx))
        entries.append(entry)
    
    submit_btn = tk.Button(input_window, text="🚀 Create Puzzle", command=submit,
                          font=('Segoe UI', 12, 'bold'),
                          bg='#e74c3c', fg='white',
                          relief='flat', bd=0, padx=20, pady=10,
                          cursor='hand2')
    submit_btn.grid(row=num_words+2, column=0, columnspan=2, pady=20)
    
    # Focus on first entry
    entries[0].focus_set()
    
    # Handle window close button (red X)
    def on_input_window_close():
        """Handle input window close event - exit application"""
        input_window.destroy()
        exit()
    
    input_window.protocol("WM_DELETE_WINDOW", on_input_window_close)
    
    input_window.mainloop()
    return words

def main():
    """Main game function"""
    # Get game settings
    settings = get_game_settings()
    
    # Get words from user
    words = get_words_from_user(settings['num_words'])
    
    # Create puzzle
    puzzle = create_crossword(words)
    
    # Show puzzle UI with timer
    show_puzzle_ui(puzzle, words, settings['time_limit'])

if __name__ == "__main__":
    main()