import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.simpledialog
import json


class SimpleInkscapeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Draw")
        self.canvas = tk.Canvas(self.master, bg="white", width=800, height=600)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_toolbar()
        self.shapes = []  # Store ids of created shapes
        self.start_x = None
        self.start_y = None
        self.selected_shapes = []  # Store the ids of selected shapes
        self.selection_rect = None  # Rubber band selection rectangle
        self.move_mode = False
        self.copied_shape = None  # Store the id of the copied shape

        
        # Bind Ctrl+C to copy
        self.master.bind("<Control-c>", self.copy_selected_shape)
        # Bind Ctrl+V to paste
        self.master.bind("<Control-v>", self.paste_shape)

    def create_toolbar(self):
        self.toolbar = ttk.Frame(self.master)
        self.toolbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Draw Rectangle Button
        self.rect_btn = ttk.Button(self.toolbar, text="Rectangle", command=self.set_draw_rectangle_mode)
        self.rect_btn.pack(pady=2)

        # Draw Circle Button
        self.circle_btn = ttk.Button(self.toolbar, text="Circle", command=self.set_draw_circle_mode)
        self.circle_btn.pack(pady=2)

        # Draw Text Label Button
        self.text_btn = ttk.Button(self.toolbar, text="Text", command=self.set_draw_text_mode)
        self.text_btn.pack(pady=2)
        
        # Rename Button
        self.rename_btn = ttk.Button(self.toolbar, text="Rename", command=self.edit_text)
        self.rename_btn.pack(pady=2)

        # Draw Line Button
        self.line_btn = ttk.Button(self.toolbar, text="Line", command=self.set_draw_line_mode)
        self.line_btn.pack(pady=2)

        # Select Tool Button
        self.select_btn = ttk.Button(self.toolbar, text="Select", command=self.set_select_mode)
        self.select_btn.pack(pady=2)

        # Deselect All Button
        self.deselect_btn = ttk.Button(self.toolbar, text="Deselect All", command=self.deselect_all)
        self.deselect_btn.pack(pady=2)
        
        # Move Tool Button
        self.move_btn = ttk.Button(self.toolbar, text="Move", command=self.set_move_mode)
        self.move_btn.pack(pady=2)
        
        # Delete Tool Button
        self.delete_btn = ttk.Button(self.toolbar, text="Delete", command=self.delete_selected_shapes)
        self.delete_btn.pack(pady=2)

        # Export Button
        self.export_btn = ttk.Button(self.toolbar, text="Export", command=self.export_data)
        self.export_btn.pack(pady=2)
        
        # Import Button
        self.import_btn = ttk.Button(self.toolbar, text="Import", command=self.import_data)
        self.import_btn.pack(pady=2)

        # Reset Button
        self.reset_btn = ttk.Button(self.toolbar, text="Reset", command=self.reset_canvas)
        self.reset_btn.pack(pady=2)
        
        # Copy Button
        self.copy_btn = ttk.Button(self.toolbar, text="Copy", command=self.copy_selected_shape)
        self.copy_btn.pack(pady=2)
        
        # Paste Button
        self.paste_btn = ttk.Button(self.toolbar, text="Paste", command=self.paste_shape)
        self.paste_btn.pack(pady=2)
        
        # Future buttons for other shapes and functionalities

    def reset_canvas(self):
        # Clear all shapes, lines, and text labels from the canvas
        self.canvas.delete("all")
        # Clear the lists storing shape ids and selected shapes
        self.shapes = []
        self.selected_shapes = []
        
    def set_draw_line_mode(self):
        self.canvas.bind("<Button-1>", self.start_draw_line)
        self.canvas.bind("<B1-Motion>", self.drawing_line)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw_line)
        # Disable move mode
        self.move_mode = False

    def start_draw_line(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.line = self.canvas.create_line(self.start_x, self.start_y, self.start_x, self.start_y, width=5, fill="black", tags=("line",))
        self.shapes.append(self.line)  # Add the line's item ID to the list of shapes

    def drawing_line(self, event):
        self.canvas.coords(self.line, self.start_x, self.start_y, event.x, event.y)

    def stop_draw_line(self, event):
        # Reset start_x and start_y instead of unbinding the events
        self.start_x = None
        self.start_y = None

    def deselect_all(self):
        for shape_id in self.selected_shapes:
            if shape_id in self.shapes:
                if "line" in self.canvas.gettags(shape_id):
                    self.canvas.itemconfig(shape_id, fill="black")  
                else:
                    self.canvas.itemconfig(shape_id, outline="black", width=5)
            elif self.canvas.type(shape_id) == "text":
                self.canvas.itemconfig(shape_id, fill="black")
        self.selected_shapes = []
            
    def edit_text(self):
        for item in self.selected_shapes:
            if self.canvas.type(item) == "text":
                # Get the current text of the label
                current_text = self.canvas.itemcget(item, "text")
                # Prompt the user to edit the text using the current text as the default value
                new_text = tkinter.simpledialog.askstring("Edit Text", "Enter new text:", initialvalue=current_text)
                if new_text:
                    self.canvas.itemconfig(item, text=new_text)
            else:
                tkinter.messagebox.showinfo("Error", "Please select a text label to edit.")


            
    def set_draw_text_mode(self):
        self.canvas.bind("<Button-1>", self.place_text)
        # Disable move mode
        self.move_mode = False
    
    def place_text(self, event):
        text = tkinter.simpledialog.askstring("Text Input", "Enter text:")
        if text:
            text_id = self.canvas.create_text(event.x, event.y, text=text, fill="black", tags=("text_label",), font=("Helvetica", 16))  # Increase font size to 12

    def set_draw_circle_mode(self):
        # Unbind other drawing events
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<Button-1>", self.start_draw_circle)
        self.canvas.bind("<B1-Motion>", self.drawing_circle)
        #self.canvas.bind("<ButtonRelease-1>", self.stop_draw_circle)

        # Disable move mode
        self.move_mode = False

    def start_draw_circle(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.circle = self.canvas.create_oval(self.start_x, self.start_y, self.start_x, self.start_y, outline="black", width=5)
        self.shapes.append(self.circle)  # Add the circle's item ID to the list of shapes

    def drawing_circle(self, event):
        self.canvas.coords(self.circle, self.start_x, self.start_y, event.x, event.y)

    def stop_draw_circle(self, event):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        
    def set_draw_rectangle_mode(self):
        # Unbind other drawing events
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<Button-1>", self.start_draw_rectangle)
        self.canvas.bind("<B1-Motion>", self.drawing_rectangle)
        #self.canvas.bind("<ButtonRelease-1>", self.stop_draw_rectangle)

        # Disable move mode
        self.move_mode = False
    
    def set_select_mode(self):
        self.canvas.bind("<ButtonPress-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.draw_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)
        # Bind right mouse button for moving shapes
        self.canvas.bind("<ButtonPress-3>", self.start_move_with_right_click)
        self.canvas.bind("<B3-Motion>", self.move_shape_with_right_click)
        self.canvas.bind("<ButtonRelease-3>", self.end_move_with_right_click)
        self.move_mode = False

    def start_move_with_right_click(self, event):
        if self.selected_shapes:
            self.start_x = event.x
            self.start_y = event.y

    def move_shape_with_right_click(self, event):
        if self.selected_shapes:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            for shape_id in self.selected_shapes:
                self.canvas.move(shape_id, dx, dy)
            self.start_x = event.x
            self.start_y = event.y

    def end_move_with_right_click(self, event):
        self.start_x = None
        self.start_y = None
    
    def set_move_mode(self):
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.move_shape)
        self.canvas.bind("<ButtonRelease-1>", self.end_move)
        # Enable move mode
        self.move_mode = True

    def start_draw_rectangle(self, event):
        self.start_x = event.x
        self.start_y = event.y
        shape_id = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="black", width=5, fill="")
        self.shapes.append(shape_id)

    def drawing_rectangle(self, event):
        self.canvas.coords(self.shapes[-1], self.start_x, self.start_y, event.x, event.y)

    def stop_draw_rectangle(self, event):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
            
    def start_selection(self, event):

        self.deselect_all()

        self.start_x = event.x
        self.start_y = event.y
        # Create a rubber band rectangle
        self.selection_rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="blue", width=5)

    def draw_selection(self, event):
        # Update the rubber band rectangle as the mouse moves
        self.canvas.coords(self.selection_rect, self.start_x, self.start_y, event.x, event.y)

    def end_selection(self, event):
        # Get the area covered by the rubber band rectangle
        x0, y0, x1, y1 = self.canvas.coords(self.selection_rect)
        # Find all objects within the selection rectangle
        items = self.canvas.find_overlapping(x0, y0, x1, y1)
        # Determine if any shape or text label within the selection area is already selected
        already_selected = any(item in self.selected_shapes for item in items if item != self.selection_rect)
        
        if already_selected:
            # If the shape or text label is already selected, deselect only the rubber-banded shape
            for item in items:
                if item != self.selection_rect and item in self.selected_shapes:
                    if item in self.shapes:
                        if "line" in self.canvas.gettags(item):
                            self.canvas.itemconfig(item, fill="black")
                        else:
                            self.canvas.itemconfig(item, outline="black", width=5)
                    elif self.canvas.type(item) == "text":
                        self.canvas.itemconfig(item, fill="black")
                    self.selected_shapes.remove(item)
        else:
            # Otherwise, select all objects within the selection rectangle
            for item in items:
                if item != self.selection_rect:
                    if "line" in self.canvas.gettags(item):
                        self.canvas.itemconfig(item, fill="red")
                        self.selected_shapes.append(item)
                    else:
                        if item in self.shapes:
                            self.canvas.itemconfig(item, outline="red", width=5)
                        elif self.canvas.type(item) == "text":
                            self.canvas.itemconfig(item, fill="red")
                        self.selected_shapes.append(item)
                    
                    # Check if the line intersects with the selection rectangle
                    if self.canvas.type(item) == "line":
                        x0_line, y0_line, x1_line, y1_line = self.canvas.coords(item)
                        if (x0_line > x0 and x0_line < x1 and y0_line > y0 and y0_line < y1) or \
                        (x1_line > x0 and x1_line < x1 and y1_line > y0 and y1_line < y1):
                            self.selected_shapes.append(item)

        # Delete the rubber band rectangle
        self.canvas.delete(self.selection_rect)

        
    def start_move(self, event):
        if self.move_mode:
            self.start_x = event.x
            self.start_y = event.y

    def move_shape(self, event):
        if self.move_mode and self.selected_shapes:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            for shape_id in self.selected_shapes:
                self.canvas.move(shape_id, dx, dy)
                # Update the starting coordinates to the current position
                self.start_x = event.x
                self.start_y = event.y

    def end_move(self, event):
        self.start_x = None
        self.start_y = None

    def delete_selected_shapes(self):
        for shape_id in self.selected_shapes:
            self.canvas.delete(shape_id)
        self.shapes = [shape_id for shape_id in self.shapes if shape_id not in self.selected_shapes]
        self.selected_shapes = []


    def export_data(self):

        # Deselect all items before exporting
        self.deselect_all()
        
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            data = {
                "shapes": [],
                "lines": [],
                "text_labels": []
            }

            for shape_id in self.shapes:
                shape_type = self.canvas.type(shape_id)
                if shape_type == "rectangle":
                    x0, y0, x1, y1 = self.canvas.coords(shape_id)
                    data["shapes"].append({
                        "type": "rectangle",
                        "coords": [x0, y0, x1, y1],
                        "outline": self.canvas.itemcget(shape_id, "outline"),
                        "width": self.canvas.itemcget(shape_id, "width")
                    })
                elif shape_type == "oval":
                    x0, y0, x1, y1 = self.canvas.coords(shape_id)
                    data["shapes"].append({
                        "type": "circle",
                        "coords": [x0, y0, x1, y1],
                        "outline": self.canvas.itemcget(shape_id, "outline"),
                        "width": self.canvas.itemcget(shape_id, "width")
                    })

            for line_id in self.canvas.find_withtag("line"):
                x0, y0, x1, y1 = self.canvas.coords(line_id)
                data["lines"].append({
                    "coords": [x0, y0, x1, y1],
                    "fill": self.canvas.itemcget(line_id, "fill"),
                    "width": self.canvas.itemcget(line_id, "width")
                })

            for text_id in self.canvas.find_withtag("text_label"):
                x, y = self.canvas.coords(text_id)
                text = self.canvas.itemcget(text_id, "text")
                font = self.canvas.itemcget(text_id, "font")
                data["text_labels"].append({
                    "x": x,
                    "y": y,
                    "text": text,
                    "font": font
                })

            with open(filename, "w") as f:
                json.dump(data, f)


    def import_data(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, "r") as f:
                data = json.load(f)

            self.canvas.delete("all")  # Clear canvas before importing new data

            for shape_data in data["shapes"]:
                if shape_data["type"] == "rectangle":
                    x0, y0, x1, y1 = shape_data["coords"]
                    shape_id = self.canvas.create_rectangle(x0, y0, x1, y1, outline=shape_data["outline"], width=shape_data["width"], fill="")
                    self.shapes.append(shape_id)
                elif shape_data["type"] == "circle":
                    x0, y0, x1, y1 = shape_data["coords"]
                    shape_id = self.canvas.create_oval(x0, y0, x1, y1, outline=shape_data["outline"], width=shape_data["width"])
                    self.shapes.append(shape_id)

            for line_data in data["lines"]:
                x0, y0, x1, y1 = line_data["coords"]
                line_id = self.canvas.create_line(x0, y0, x1, y1, fill=line_data["fill"], width=line_data["width"], tags=("line",))
                self.shapes.append(line_id)

            for text_data in data["text_labels"]:
                text_id = self.canvas.create_text(text_data["x"], text_data["y"], text=text_data["text"], fill="black", font=text_data["font"], tags=("text_label",))

        self.set_select_mode()


    def copy_selected_shape(self, event):
        # Copy all selected shapes
        if self.selected_shapes:
            self.copied_shapes = self.selected_shapes.copy()  # Use copy() to avoid aliasing issues

    def paste_shape(self, event):
        if self.copied_shapes:
            dx, dy = 50, 50  # Offset for pasting
            new_copied_shapes = []  # To store newly created shapes for selection
            
            for copied_shape in self.copied_shapes:
                shape_type = self.canvas.type(copied_shape)
                new_shape_id = None

                if shape_type == 'line':
                    new_shape_id = self.canvas.create_line(0, 0, 0, 0, fill="black", width=5, tags=("line",))
                elif shape_type == 'rectangle':
                    new_shape_id = self.canvas.create_rectangle(0, 0, 0, 0, outline="black", width=5, fill="")
                elif shape_type == 'oval':
                    new_shape_id = self.canvas.create_oval(0, 0, 0, 0, outline="black", width=5)
                elif shape_type == 'text':  # Handling text labels
                    text_content = self.canvas.itemcget(copied_shape, "text")
                    font = self.canvas.itemcget(copied_shape, "font")
                    new_shape_id = self.canvas.create_text(0, 0, text=text_content, fill="black", font=font, tags=("text_label",))

                if new_shape_id is not None:
                    # For text, use the position directly instead of a bounding box
                    if shape_type == 'text':
                        x0, y0 = self.canvas.coords(copied_shape)  # Unpack 2 values for text
                        self.canvas.coords(new_shape_id, x0 + dx, y0 + dy)
                    else:
                        x0, y0, x1, y1 = self.canvas.coords(copied_shape)  # Unpack 4 values for other shapes
                        self.canvas.coords(new_shape_id, x0 + dx, y0 + dy, x1 + dx, y1 + dy)

                    # Add the new shape ID to the list for selection and highlighting
                    new_copied_shapes.append(new_shape_id)

                    # Add the new shape ID to the self.shapes list
                    if not shape_type  == 'text':
                        self.shapes.append(new_shape_id)


            # Deselect originally selected shapes and select newly pasted shapes
            self.deselect_all()

            self.selected_shapes = new_copied_shapes.copy()  # Select newly pasted shapes

            # Optionally, highlight the newly pasted shapes
            for shape_id in self.selected_shapes:
                shape_type = self.canvas.type(shape_id)

                if shape_type in ['rectangle', 'oval']:
                    self.canvas.itemconfig(shape_id, outline="red", width=5)
                elif shape_type == 'line':
                    self.canvas.itemconfig(shape_id, fill="red", width=5)
                elif shape_type == 'text':  # Highlighting text labels
                    self.canvas.itemconfig(shape_id, fill="red")



if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleInkscapeApp(root)
    root.mainloop()
