import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.video.io.VideoFileClip import VideoFileClip

def parse_time(time_str):
    """Convert time in min:sec format to total seconds."""
    try:
        minutes, seconds = map(float, time_str.split(':'))
        return minutes * 60 + seconds
    except ValueError:
        raise ValueError("Time format should be min:sec.")

# Function to browse for video file
def browse_video():
    filename = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
    if filename:
        entry_video_path.delete(0, tk.END)
        entry_video_path.insert(0, filename)

# Function to browse for output file
def browse_output():
    filename = filedialog.asksaveasfilename(defaultextension=".mp4",
                                           filetypes=[("MP4 Files", "*.mp4"), ("All Files", "*.*")])
    if filename:
        entry_output_path.delete(0, tk.END)
        entry_output_path.insert(0, filename)

# Function to trim video
def trim_video():
    input_video_path = entry_video_path.get()
    output_video_path = entry_output_path.get()
    start_time_str = entry_start_time.get()
    end_time_str = entry_end_time.get()

    try:
        start_time = parse_time(start_time_str)
        end_time = parse_time(end_time_str)

        if start_time < 0 or end_time < 0:
            raise ValueError("Start and end times must be non-negative.")
        
        # Load the video
        video = VideoFileClip(input_video_path)
        
        # Check if the times are within the video's duration
        duration = video.duration
        if start_time >= duration or end_time > duration:
            raise ValueError("Start and end times must be within the video duration.")

        if start_time >= end_time:
            raise ValueError("Start time must be less than end time.")
        
        # Trim the video
        trimmed_video = video.subclip(start_time, end_time)
        trimmed_video.write_videofile(output_video_path, codec='libx264')

        messagebox.showinfo("Success", f"Video trimmed and saved as {output_video_path}")

    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Set up the main window
root = tk.Tk()
root.title("Video Trimmer Software")

# Create and place widgets
tk.Label(root, text="Video File:").grid(row=0, column=0, padx=10, pady=5)
entry_video_path = tk.Entry(root, width=40)
entry_video_path.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_video).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Start Time (min:sec):").grid(row=1, column=0, padx=10, pady=5)
entry_start_time = tk.Entry(root, width=20)
entry_start_time.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="End Time (min:sec):").grid(row=2, column=0, padx=10, pady=5)
entry_end_time = tk.Entry(root, width=20)
entry_end_time.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Output File:").grid(row=3, column=0, padx=10, pady=5)
entry_output_path = tk.Entry(root, width=40)
entry_output_path.grid(row=3, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_output).grid(row=3, column=2, padx=10, pady=5)

tk.Button(root, text="Trim Video", command=trim_video).grid(row=4, column=1, padx=10, pady=20)
tk.Button(root, text="Exit", command=exit).grid(row=4, column=2, padx=10, pady=20)
# Start the GUI event loop
root.mainloop()
