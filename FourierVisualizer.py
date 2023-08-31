import fourier as fourierObj
import tkinter as tk
from tkinter import font, ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# Confirm that the text entered is numerical
def isEntryNumerical(event):
    inputStr = event.widget.get()

    try:
        if(event.widget.name == "harmonics"):
            int(inputStr)
        else:
            float(inputStr)

    except ValueError:
        
        if(event.widget.name == "offset"):
            event.widget.delete(0,tk.END)
            event.widget.insert(0, "0.0")
        elif(event.widget.name == "amplitude"):
            event.widget.delete(0,tk.END)
            event.widget.insert(0, "1.0")
        elif(event.widget.name == "noise"):
            event.widget.delete(0,tk.END)
            event.widget.insert(0, "0.001")
        elif(event.widget.name == "frequency"):
            event.widget.delete(0,tk.END)
            event.widget.insert(0, "20")
        elif(event.widget.name == "harmonics"):
            event.widget.delete(0,tk.END)
            event.widget.insert(0, "1")
            messagebox.showerror(title = "Input Error", message = "Harmonic Value provided must be an Integer")
            return
            
        messagebox.showerror(title = "Input Error", message = "Only Float/Integer Values Accepted")

def generate_data():
    signalType = sigTypesCombo.current()

    numHarmonics = int(harmonicsEntry.get())

    if noiseTypesCombo.get() == "None":
        thisFourier.disable_noise()
    else:
        thisFourier.enable_noise()
        noiseVal = float(noiseEntry.get())
        thisFourier.generate_noise_data(noiseTypesCombo.get().lower(), noiseVal)


    thisFourier.set_amplitude(float(amplitudeEntry.get()))
    thisFourier.set_offset(float(offsetEntry.get()))
    thisFourier.set_frequency((float(frequencyEntry.get()) * 1e3))

    if signalType >= 0 and signalType < 4:
        thisFourier.generate_time_domain_data(sigTypesCombo.get())
    elif signalType == 4:
        thisFourier.construct_square_wave_from_sines(numHarmonics)
    elif signalType == 5:
        thisFourier.construct_triangle_wave_from_sines(numHarmonics)

    thisFourier.generate_freq_domain_data()

def plot_data():
    generate_data()
    [time_axis, signal_data] = thisFourier.get_time_domain_data()
    [fft_bins, fft_magnitude] = thisFourier.get_fft_domain_data()

    frequency = thisFourier.get_freq()
    fs = thisFourier.get_fs()
    amplitude = thisFourier.get_amplitude()
    window_name  = thisFourier.get_window_type().capitalize()
    ax[0].clear()
    ax[1].clear()

    ax[0].plot(time_axis, signal_data)
    ax[0].set_title(f"Time Domain Data: Frequency: {frequency}kHz, Sampling Frequency: {fs}kHz, Amplitude: {amplitude}")
    ax[0].set_xlim(min(time_axis), max(time_axis))
    ax[0].set_ylabel('Units')
    ax[0].set_xlabel('Seconds')
    ax[0].grid(True, 'both')

    ax[1].semilogx(fft_bins, fft_magnitude)
    if thisFourier.get_window_state():
        ax[1].set_title(f"FFT Plot: Frequency: {frequency}kHz, Sampling Frequency: {fs}KHz, FFT Window: {window_name}")
    else:
        ax[1].set_title(f"FFT Plot: Frequency: {frequency}kHz, Sampling Frequency: {fs}KHz, FFT Window: No Window")
    ax[1].set_xlim(min(fft_bins), max(fft_bins))
    ax[1].set_ylabel('Magnitude [dBFS]')
    ax[1].set_xlabel('Frequency [Hz]')
    ax[1].grid(True, 'both')

    dataCanvas.draw()

    


#Initialize the FourierObject
thisFourier = fourierObj.FourierDataObject()
# Create the tkinter Window
window = tk.Tk()
# window.geometry("1200x1000")
window.title("Fourier Visualizer Tool")
window.grid_columnconfigure(0, weight = 1)
window.grid_rowconfigure(0, weight = 0)

#Create the OptionsFrame
optionsFrame = ttk.Frame(window, height = window.winfo_height() - 20, width = window.winfo_width() - 20)
optionsFrame['borderwidth'] = 5
optionsFrame['relief'] = 'groove'

optionsFrameLabel = ttk.Label(optionsFrame, text = "Signal Options", font = 'Arial 24')
optionsFrameLabel.grid(row = 0, columnspan =2 , padx = 10, pady = 10)

#Create the Signal Types Drop Down 
sigTypeLabel = ttk.Label(optionsFrame, text = "Signal Type: ")
sigTypeLabel.grid(row = 1, column = 0, padx = 10, pady = 10)

sigTypesCombo = ttk.Combobox(optionsFrame)
sigTypesCombo['values'] = ["Sine", "Square", "Sawtooth", "Triangle", "Sine-Constructed Square Wave", "Sine-Constructed Triangle Wave"]
sigTypesCombo.current(0)
sigTypesCombo.grid(row = 1, column= 1, padx = 10, pady = 10)

#Create the FFT Windows Drop Down 
fftTypeLabel = ttk.Label(optionsFrame, text = "FFT Window: ")
fftTypeLabel.grid(row = 2, column = 0, padx = 10, pady = 5)

fftWindowsCombo = ttk.Combobox(optionsFrame)
fftWindowsCombo['values'] = [windowName.capitalize() for windowName in thisFourier.get_window_types()]
fftWindowsCombo.current(5)
fftWindowsCombo.grid(row = 2, column = 1, padx = 10, pady = 5)

#Create the Noise Types Drop Down

noiseTypesLabel = ttk.Label(optionsFrame, text = "Noise Type: ")
noiseTypesLabel.grid(row = 3, column = 0, padx = 10, pady = 5)

noiseTypesCombo = ttk.Combobox(optionsFrame)
noiseTypesCombo['value'] = ("None",) + thisFourier.get_noise_types()
noiseTypesCombo.current(0)
noiseTypesCombo.grid(row = 3, column = 1, padx = 10, pady = 10)

# Set up the Amplitude Text Entry Box
offsetLabel = ttk.Label(optionsFrame, text = "Offset Value: ")
offsetLabel.grid(row = 4, column = 0, padx = 10, pady= 10)

offsetText = tk.StringVar()
offsetText.set("0.0")

offsetEntry = ttk.Entry(optionsFrame, textvariable = offsetText)
offsetEntry.bind('<Return>', isEntryNumerical)
offsetEntry.bind('<FocusOut>', isEntryNumerical)
offsetEntry.name = "offset"
offsetEntry.grid(row = 4, column = 1, padx = 10, pady= 10)

# Set up the Amplitude Text Entry Box
amplitudeLabel = ttk.Label(optionsFrame, text = "Amplitude Value: ")
amplitudeLabel.grid(row = 5, column = 0, padx = 10, pady= 10)

amplitudeText = tk.StringVar()
amplitudeText.set("1.0")

amplitudeEntry = ttk.Entry(optionsFrame, textvariable = amplitudeText)
amplitudeEntry.bind('<Return>', isEntryNumerical)
amplitudeEntry.bind('<FocusOut>', isEntryNumerical)
amplitudeEntry.name = "amplitude"
amplitudeEntry.grid(row = 5, column = 1, padx = 10, pady= 10)

# Set up the Noise Magnitude Text Entry Box
noiseLabel = ttk.Label(optionsFrame, text = "Noise Magnitude: ")
noiseLabel.grid(row = 6, column = 0, padx = 10, pady= 10)

noiseText = tk.StringVar()
noiseText.set("0.01")

noiseEntry = ttk.Entry(optionsFrame, textvariable = noiseText)
noiseEntry.bind('<Return>', isEntryNumerical)
noiseEntry.bind('<FocusOut>', isEntryNumerical)
noiseEntry.name = "noise"
noiseEntry.grid(row = 6, column = 1, padx = 10, pady= 10)

# Set up the Frequency Text Entry Box
frequencyLabel = ttk.Label(optionsFrame, text = "Frequency [kHz]: ")
frequencyLabel.grid(row = 7, column = 0, padx = 10, pady= 10)

frequencyText = tk.StringVar()
frequencyText.set("0.01")

frequencyEntry = ttk.Entry(optionsFrame, textvariable = frequencyText)
frequencyEntry.bind('<Return>', isEntryNumerical)
frequencyEntry.bind('<FocusOut>', isEntryNumerical)
frequencyEntry.name = "frequency"
frequencyEntry.grid(row = 7, column = 1, padx = 10, pady= 10)

# Set up the Harmonics Text Entry Box
harmonicsLabel = ttk.Label(optionsFrame, text = "Harmonics: ")
harmonicsLabel.grid(row = 8, column = 0, padx = 10, pady= 10)

harmonicsText = tk.StringVar()
harmonicsText.set("1")

harmonicsEntry = ttk.Entry(optionsFrame, textvariable = harmonicsText)
harmonicsEntry.bind('<Return>', isEntryNumerical)
harmonicsEntry.bind('<FocusOut>', isEntryNumerical)
harmonicsEntry.name = "harmonics"
harmonicsEntry.grid(row = 8, column = 1, padx = 10, pady= 10)

optionsFrame.pack(side = 'left', padx = 10, pady = 10, expand = True, fill = "both")

#Setup the display frame
displayFrame = ttk.Frame(window, height =  window.winfo_height() - 20, width = window.winfo_width() - 20)
displayFrame['borderwidth'] = 5
displayFrame['relief'] = 'groove'

displayFrameLabel = ttk.Label(displayFrame, text = "Signal Data", font = "Helvetica 24")
displayFrameLabel.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'n')

fig, ax = plt.subplots(2, 1)
dataCanvas = FigureCanvasTkAgg(fig, master = displayFrame)
dataCanvas.get_tk_widget().grid(row = 1, padx = 10, pady = 10, stick = 'nsew')

displayFrame.grid_columnconfigure(0, weight = 1)
displayFrame.grid_rowconfigure(1 , weight = 1)
displayFrame.pack(side = 'right', padx = 10, pady = 10, expand = True, fill = "both")

plotButton = ttk.Button(optionsFrame, text = "Generate Plot", command = plot_data)
plotButton.grid(row = 9, columnspan = 2, padx = 10, pady = 10)
window.mainloop()
