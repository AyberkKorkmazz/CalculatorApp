import tkinter as tk
from tkinter import font
import math

class Calculator:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Calculator")
        self.window.geometry("320x480")
        self.window.resizable(False, False)
        self.window.configure(bg="#2C3E50")

        #variables
        self.current_input = "0"
        self.previous_input = ""
        self.operator = ""
        self.reset_display = False  # Bu değişken eksikti

        #fonts
        self.display_font = font.Font(family="Arial", size=24, weight="bold")
        self.button_font = font.Font(family="Arial", size=14, weight="bold")

        self.setup_ui()

    def setup_ui(self):
        # main frame
        main_frame = tk.Frame(self.window, bg="#2C3E50", padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        #display
        self.display = tk.Label(
            main_frame,
            text=self.current_input,
            font=self.display_font,
            bg="#34495E",
            fg="White",
            anchor='e',
            padx=15,
            pady=15,
            relief='flat',
            bd=0
        )
        self.display.pack(fill='x', pady=(0, 10))

        # button frame
        button_frame = tk.Frame(main_frame, bg="#2C3E50")
        button_frame.pack(fill="both", expand=True)

        #button configuration
        buttons = [
            ('C', 0, 0, 'special', 1), ('±', 0, 1, 'special', 1), ('%', 0, 2, 'special', 1), ('÷', 0, 3, 'operator', 1),
            ('7', 1, 0, 'number', 1), ('8', 1, 1, 'number', 1), ('9', 1, 2, 'number', 1), ('×', 1, 3, 'operator', 1),
            ('4', 2, 0, 'number', 1), ('5', 2, 1, 'number', 1), ('6', 2, 2, 'number', 1), ('-', 2, 3, 'operator', 1),
            ('1', 3, 0, 'number', 1), ('2', 3, 1, 'number', 1), ('3', 3, 2, 'number', 1), ('+', 3, 3, 'operator', 1),
            ('0', 4, 0, 'number', 2), ('.', 4, 2, 'number', 1), ('=', 4, 3, 'equals', 1)  # 0 butonunu 2 kolon yap
        ]

        # color theme
        colors = {
            'number': {'bg': '#95A5A6', 'fg': 'white', 'active_bg': '#BDC3C7'},
            'operator': {'bg': '#E74C3C', 'fg': 'white', 'active_bg': '#C0392B'},
            'special': {'bg': '#34495E', 'fg': 'white', 'active_bg': '#2C3E50'},
            'equals': {'bg': '#27AE60', 'fg': 'white', 'active_bg': '#229954'},
            'empty': {'bg': '#2C3E50', 'fg': 'white', 'active_bg': '#2C3E50'}
        }

        # configure grid weights
        for i in range(5):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):    
            button_frame.grid_columnconfigure(i, weight=1)

        # create buttons
        for text, row, col, color_type, columnspan in buttons:
            color_config = colors[color_type]

            btn = tk.Button(
                button_frame,
                text=text,
                font=self.button_font,
                bg=color_config['bg'],
                fg=color_config['fg'],
                activebackground=color_config['active_bg'],
                activeforeground="white",
                relief='flat',
                bd=0,
                command=lambda t=text: self.button_click(t)
            )

            btn.grid(
                row=row,
                column=col,
                columnspan=columnspan,
                sticky='nsew',
                padx=2,
                pady=2,
                ipady=20,
            )

    def button_click(self, text):
        if text.isdigit():
            self.handle_number(text)
        elif text == ".":
            self.handle_decimal()
        elif text in ['+', '-', '×', '÷']:
            self.handle_operator(text)
        elif text == '=':
            self.handle_equals()
        elif text == 'C':
            self.handle_clear()
        elif text == '±':
            self.handle_sign_change()
        elif text == '%':
            self.handle_percentage()
        
    def handle_number(self, num):
        if self.reset_display or self.current_input == "0":
            self.current_input = num
            self.reset_display = False
        else:
            self.current_input += num
        self.update_display()

    def handle_decimal(self):
        if self.reset_display:
            self.current_input = "0."
            self.reset_display = False
        elif '.' not in self.current_input:
            self.current_input += '.'
        self.update_display()

    def handle_operator(self, op):
        if self.operator and not self.reset_display:
            self.handle_equals()

        self.previous_input = self.current_input
        self.operator = op
        self.reset_display = True

    def handle_equals(self):
        if self.operator and self.previous_input:
            try:
                #operator conversion
                op_map = {"×": "*", "÷": "/"}  # × sembolünü düzelttim
                calc_operator = op_map.get(self.operator, self.operator)

                #calculate
                result = eval(f"{self.previous_input}{calc_operator}{self.current_input}")

                #format result
                if result == int(result):
                    self.current_input = str(int(result))
                else:
                    self.current_input = f"{result:.8g}"

                self.update_display()
                self.operator = ""
                self.previous_input = ""
                self.reset_display = True

            except ZeroDivisionError:
                self.current_input = "Error"  # Yazım hatasını düzelttim
                self.update_display()
                self.reset_calculator()
            except:
                self.current_input = "Error"
                self.update_display()
                self.reset_calculator()

    def handle_clear(self):
        self.current_input = "0"
        self.previous_input = ""
        self.operator = ""
        self.reset_display = False
        self.update_display()
    
    def handle_sign_change(self):
        if self.current_input != "0":
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
        self.update_display()

    def handle_percentage(self):
        try:
            result = float(self.current_input) / 100
            if result == int(result):
                self.current_input = str(int(result))
            else:
                self.current_input = f"{result:.8g}"
            self.update_display()
        except:
            self.current_input = "Error"
            self.update_display()
            self.reset_calculator()

    def reset_calculator(self):
        self.previous_input = ""
        self.operator = ""
        self.reset_display = True
    
    def update_display(self):
        # truncate long numbers
        display_text = self.current_input
        if len(display_text) > 12:
            try:
                num = float(display_text)
                display_text = f"{num:.6e}"
            except:
                display_text = display_text[:12] + "..."

        self.display.config(text=display_text)

    def run(self):
        self.window.mainloop()

# run the application
if __name__ == "__main__":
    calc = Calculator()
    calc.run()