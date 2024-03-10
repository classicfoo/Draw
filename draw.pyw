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
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    
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
        self.canvas.bind("<Button-1>", self.start_draw_circle)
        self.canvas.bind("<B1-Motion>", self.drawing_circle)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw_circle)
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
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.drawing)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)
        # Disable move mode
        self.move_mode = False
    
    def set_select_mode(self):
        self.canvas.bind("<ButtonPress-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.draw_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)
        # Disable move mode
        self.move_mode = False
    
    def set_move_mode(self):
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.move_shape)
        self.canvas.bind("<ButtonRelease-1>", self.end_move)
        # Enable move mode
        self.move_mode = True

    def start_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y
        shape_id = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="black", width=5, fill="")
        self.shapes.append(shape_id)

    def drawing(self, event):
        self.canvas.coords(self.shapes[-1], self.start_x, self.start_y, event.x, event.y)

    def stop_draw(self, event):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
            
    def start_selection(self, event):
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
            # Calculate the offset from the starting mouse position
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            # Move each selected shape by the calculated offset
            for shape_id in self.selected_shapes:
                shape_type = self.canvas.type(shape_id)
                # Determine if the shape is a line
                if shape_type == 'line':
                    # Get the current position of the line's start and end points
                    x0, y0, x1, y1 = self.canvas.coords(shape_id)
                    # Move the line by the calculated offset
                    self.canvas.coords(shape_id, x0 + dx, y0 + dy, x1 + dx, y1 + dy)
                else:
                    # For rectangles and ovals, use the move method
                    self.canvas.move(shape_id, dx, dy)
            # Update the starting coordinates for the next move operation
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





if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleInkscapeApp(root)
    root.mainloop()
