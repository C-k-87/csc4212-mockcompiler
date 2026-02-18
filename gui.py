import tkinter as tk
import socket

def run_server(output_label:tk.Label, throttle=0, rpm=1700, load=0):
    input_str=f"throttle={throttle}; rpm={rpm}; load={load}; end;"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 8080))

    client.send(input_str.encode())
    response = client.recv(2048)
    print("Message from server:", response.decode())
    output_label.config(text=f"ECU Ouptut:{response.decode()}")

    client.close()

def run_gui():
    def update_output():
        throttle = throttle_slider.get()
        rpm = rpm_slider.get()
        load = load_slider.get()
        input_label.config(
            text=f"Throttle: {throttle}% | RPM: {rpm} | Load: {load}%"
        )

        run_server(output_label, throttle, rpm, load);

        root.after(1000, update_output)

    # Create main window
    root = tk.Tk()
    root.title("Engine Control GUI")

    slider_frame = tk.Frame(root)
    slider_frame.pack(padx=10, pady=10)

    # Throttle slider
    throttle_frame = tk.Frame(slider_frame)
    throttle_frame.pack(side="left", padx=10)
    throttle_slider = tk.Scale(throttle_frame, from_=100, to=0, orient="vertical")
    throttle_slider.pack()
    tk.Label(throttle_frame, text="Throttle (%)").pack()

    # RPM slider
    rpm_frame = tk.Frame(slider_frame)
    rpm_frame.pack(side="left", padx=10)
    rpm_slider = tk.Scale(rpm_frame, from_=4000, to=0, orient="vertical")
    rpm_slider.config(variable=tk.IntVar(value=1700))
    rpm_slider.pack()
    tk.Label(rpm_frame, text="RPM").pack()

    # Engine load slider
    load_frame = tk.Frame(slider_frame)
    load_frame.pack(side="left", padx=10)
    load_slider = tk.Scale(load_frame, from_=100, to=0, orient="vertical")
    load_slider.pack()
    tk.Label(load_frame, text="Engine Load (%)").pack()

    # Label for input sliders
    input_label = tk.Label(root, text="Adjust sliders")
    input_label.pack(padx=10, pady=10)

    # Label for output
    output_label = tk.Label(root, text="Waiting for output")
    output_label.pack(padx=10, pady=10)

    update_output()
    root.mainloop()

# run_server()
run_gui()