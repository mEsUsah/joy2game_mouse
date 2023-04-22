import tkinter as tk
import tkinter.ttk as ttk
import gui

class Tab():
    def __init__(self, tab):
        '''Config tab in app window'''
        self.tab = tab
        self.showing_center_option = False
        self.translation_method = tk.IntVar(value=1)
        self.joystick_resolution = tk.IntVar(value=16)
        self.autocenter = tk.BooleanVar(value=False)

        self.joysticks = {}
        self.joystick_selected = tk.StringVar(value="None")
        self.joystick_x_selected = tk.StringVar(value="None")
        self.joystick_y_selected = tk.StringVar(value="None")
        

        self.row_1 = ttk.Frame(self.tab)
        self.row_1.pack(side="top", expand=1, fill="both")

        # Translation method selection
        self.transation_label = ttk.Label(
            self.row_1,
            text="Translation method:",
            font="TkDefaultFont 10 bold"
        )
        self.transation_label.pack(side="top", fill="x", padx=10, pady=6)

        self.transation_methods = {
            1: "Absolute - From last mouse position before activation",
            2: "Absolute - From center of screen",
            3: "Relative - Based on absolute joystick position",
        }

        for key, value in self.transation_methods.items():
            ttk.Radiobutton(
                self.row_1,
                text=value,
                variable=self.translation_method,
                value=key,
                command=self.update_options
            ).pack(side="top", fill="x", padx=10)
        
        self.row_2 = ttk.Frame(self.tab)
        self.row_2.pack(side="top", expand=1, fill="both")

        # Joystick resolution options
        self.transation_label = ttk.Label(
            self.row_1,
            text="Joystick resolution:",
            font="TkDefaultFont 10 bold"
        )
        self.transation_label.pack(side="top", fill="x", padx=10, pady=6)

        self.row_3 = ttk.Frame(self.tab)
        self.row_3.pack(side="top", expand=1, fill="both")

        self.joystick_resolution_options = {
            8: "8-bit",
            12: "12-bit",
            16: "16-bit",
        }

        for key, value in self.joystick_resolution_options.items():
            ttk.Radiobutton(
                self.row_1,
                text=value,
                variable=self.joystick_resolution,
                value=key
            ).pack(side="top", fill="x", padx=10)

        self.row_4 = ttk.Frame(self.tab)
        self.row_4.pack(side="top", expand=1, fill="both")

        self.joystick_select_label = ttk.Label(
            self.row_4,
            text="Joystick for mouse control:",
            font="TkDefaultFont 10 bold"
        )
        self.joystick_select_label.pack(side="top", fill="x", padx=10, pady=6)
        
        # X axis selection
        self.row_5 = ttk.Frame(self.tab)
        self.row_5.pack(side="top", expand=1, fill="both", pady=6)
        
        # X axis selection
        self.row_6 = ttk.Frame(self.tab)
        self.row_6.pack(side="top", expand=1, fill="both", pady=6)


    def update_device_list(self, joysticks):
        self.joysticks = joysticks
        self.update_joystick_combobox()
        self.update_axis_selection()


    def update_joystick_combobox(self):
        # Destroy combobox if it exists
        try:
            self.joystick_list.destroy()
        except:
            pass

        # Create new selection combobox
        joystick_list_values = ['None']
        for device in self.joysticks.values():
            joystick_list_values.append(device.get_name())

        self.joystick_list = ttk.Combobox(
            self.row_4,
            values=joystick_list_values,
            textvariable=self.joystick_selected,
            state="readonly",
        )
        self.joystick_list.bind('<<ComboboxSelected>>', self.update_axis_selection)    
        self.joystick_list.pack(side="top", fill="x", padx=10)


    def update_axis_selection(self,event=None):
        # Destroy axis selection if it exists and deselect axis
        try:
            self.x_axis_label.destroy()
            self.x_axis_list.destroy()
            self.y_axis_label.destroy()
            self.y_axis_list.destroy()
            self.joystick_x_selected.set("None")
            self.joystick_y_selected.set("None")
        except:
            pass

        if self.joystick_selected.get() != "None":
            for device in self.joysticks.values():
                if device.get_name() == self.joystick_selected.get():
                    axis_list = [x+1 for x in range(device.get_numaxes())]

                    # X axis selection
                    self.x_axis_label = ttk.Label(
                        self.row_5,
                        text="X axis:",
                    )
                    self.x_axis_label.pack(side="left", padx=10)
                    self.x_axis_list = ttk.Combobox(
                        self.row_5,
                        values=axis_list,
                        state="readonly",
                        textvariable=self.joystick_x_selected,
                    )
                    self.x_axis_list.bind('<<ComboboxSelected>>', self.update_joystick_x_axis)    
                    self.x_axis_list.pack(side="left", padx=10)
                    
                    # Y axis selection
                    self.y_axis_label = ttk.Label(
                        self.row_6,
                        text="Y axis:",
                    )
                    self.y_axis_label.pack(side="left", padx=10)
                    self.y_axis_list = ttk.Combobox(
                        self.row_6,
                        values=axis_list,
                        state="readonly",
                        textvariable=self.joystick_y_selected,
                    )
                    self.y_axis_list.bind('<<ComboboxSelected>>', self.update_joystick_y_axis)  
                    self.y_axis_list.pack(side="left", padx=10)
                    
                    
    def update_joystick_x_axis(self, event=None):
        print(self.joystick_x_selected.get())


    def update_joystick_y_axis(self, event=None):
        print(self.joystick_y_selected.get())


    def get_translation_method(self):
        return self.translation_method.get()


    def get_autocenter(self):
        return self.autocenter.get()


    def get_joystick_resolution(self):
        return self.joystick_resolution.get()


    def update_options(self):
        if self.translation_method.get() != 1:
            if not self.showing_center_option:
                self.showing_center_option = True
                self.center_option = ttk.Checkbutton(
                    self.row_2,
                    text="Autocenter mouse",
                    variable=self.autocenter
                )
                self.center_option.pack(side="top", fill="x", padx=10, pady=6)
        else:
            self.center_option.destroy()
            self.showing_center_option = False
            self.autocenter.set(False)