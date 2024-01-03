# import tkinter
# from modules.constants import GSD as original_GSD
# # window = tkinter.Tk()
#
# window.title("Aforo vehicular")
#
# # Principal nest frame
#
# # Tkinter steps
# # Define the widget that we want to add
# frame = tkinter.Frame(window)
# # Pack the created widget
# frame.pack()
#
# # Label frame
# # Input the GSD for the speeds in the raw_csv_file
# GSD_title_frame = tkinter.LabelFrame(frame, text="Insertar el GSD")  # The parent is frame, is nested inside
# GSD_title_frame.grid(row=0, column=0)
#
# GSD_label = tkinter.Label(GSD_title_frame, text="Escriba el GSD:")
# GSD_label.grid(row=0, column=0)
#
# # This is where the user actually inputs the GSD
# GSD_user_input = tkinter.Entry(GSD_title_frame)
# GSD_user_input.grid(row=0, column=1)
#
#
# # original_GSD = float(GSD_user_input)
#
# # print(original_GSD)
# get_GSD_button = tkinter.Button(GSD_title_frame, text="Get Original GSD", command=original_GSD)
# get_GSD_button.grid(row=1, column=0, columnspan=2)
#
#
# window.mainloop()
