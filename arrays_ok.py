#!/usr/bin/env python
__author__ = 'Hiep Nguyen'
import os
import sys
try:               # Python 2.7x
    import Tkinter as tk
    import ttk
    import tkFont
    import tkMessageBox
    import tkFileDialog
    import tkSimpleDialog
    from ScrolledText import ScrolledText as tkScrolledText
except Exception:  # Python 3.x
    import tkinter as tk
    from tkinter import ttk
    import tkinter.font as tkFont
    import tkinter.messagebox as tkMessageBox
    import tkinter.filedialog as tkFileDialog
    import tkinter.simpledialog as tkSimpleDialog
    from tkinter.scrolledtext import ScrolledText as tkScrolledText

import numpy             as np
import matplotlib        as mpl
import matplotlib.pyplot as plt
mpl.use("TkAgg")
from matplotlib.figure                 import Figure
from matplotlib.ticker                 import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from PIL                               import Image

# Webcam library
try:
    import cv2
    hasCV2 = True
except ImportError:
    hasCV2 = False

# Disable cv2 use on Mac OS because of buggy implementation
if sys.platform=="darwin":
    hasCV2 = False

# Modules
import md_calc as cal




# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(tk.Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        
        # parameters that you want to send through the Frame class. 
        tk.Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master         = master
        
        self.bg_colour      = '#ececec'
        self.txtfont        = 'TkFixedFont'
        self.array          = ''
        self.C              = 2.99792458e8 # m/s - speed of light
        self.uv_status      = False
        self.src_status     = False
        self.griduv_status  = False
        self.beam_status    = False
        self.src_fft_status = False

        # changing the title of our master widget      
        self.master.title('Radio Arrays')
        
        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    





    #Creation of init_window
    def init_window(self):

        # Add a grid
        self.mainframe = ttk.Frame(self.master)
        self.mainframe.grid(row=0, column=0, sticky='NWES' )
        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.rowconfigure(0, weight = 1)
        self.mainframe.pack(side='left', fill='both', expand=True, pady = 10, padx = 10)

        # creating a menu instance
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)


        # create the file object)
        file = tk.Menu(menu, tearoff=True)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label='Exit', command=self.client_exit)

        #added "file" to our menu
        menu.add_cascade(label='File', menu=file)

        



        # create the file object)
        edit = tk.Menu(menu, tearoff=True)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        edit.add_command(label='Undo')

        #added "file" to our menu
        menu.add_cascade(label='Edit', menu=edit)




        # create the file object)
        help = tk.Menu(menu, tearoff=True)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        help.add_command(label='Guide',
            command=lambda filename='docs/HELP.txt',
            title='Radio Array Instructions': self.show_textfile(filename, title) )

        #added "file" to our menu
        menu.add_cascade(label='Help', menu=help)




        # Set the grid expansion properties
        self.mainframe.columnconfigure(0, weight=2)
        self.mainframe.columnconfigure(1, weight=2)
        self.mainframe.columnconfigure(2, weight=0)
        self.mainframe.columnconfigure(3, weight=0)
        self.mainframe.columnconfigure(4, weight=0)
        self.mainframe.columnconfigure(5, weight=0)
        self.mainframe.columnconfigure(6, weight=1)
        self.mainframe.columnconfigure(7, weight=1)
        self.mainframe.columnconfigure(8, weight=1)
        self.mainframe.columnconfigure(9, weight=1)
        # self.mainframe.rowconfigure(0, weight=1)



        # For array configurations
        self.array = tk.StringVar(self.master)

        choices    = cal.get_items('configs/', ext='config')
        self.array.set(choices[0]) # set the default option

        arr_menu   = tk.OptionMenu(self.mainframe, self.array, *choices, command=self.change_dropdown)
        tk.Label(self.mainframe, text='Select array').grid(row=0, column=0, padx=5, pady=2, sticky='EW')
        arr_menu.grid(row=0, column=1, padx=5, pady=2, sticky='EW')

        self.infor = cal.load_config('configs/' + choices[0] + '.config')
        self.plot_ant_config()






        # For source models
        self.src = tk.StringVar(self.master)

        photos   = cal.get_items('sources/', ext='png')
        self.src.set('galaxy_lobes') # set the default option

        arr_menu = tk.OptionMenu(self.mainframe, self.src, *photos, command=self.show_src)
        tk.Label(self.mainframe, text='Select source').grid(row=2, column=0, padx=5, pady=2, sticky='EW')
        arr_menu.grid(row=2, column=1, padx=5, pady=2, sticky='EW')

        self.show_src()






        ## Hour Angle
        self.ha_start = tk.StringVar(self.master)
        self.ha_start.set(-12.0)

        tk.Label(self.mainframe, text='Hour angles [-12, 12] (h)').grid(row=0, column=2, padx=15, pady=2, sticky='W')
        tk.Entry(self.mainframe,textvariable = self.ha_start).grid(row=0, column=3, padx=5, pady=2, sticky='E')

        self.ha_end = tk.StringVar(self.master)
        self.ha_end.set(12.0)
        tk.Entry(self.mainframe, textvariable=self.ha_end).grid(row=0, column=4, padx=5, pady=2, sticky='E')





        # Sampling cadence (s)
        self.cad = tk.StringVar(self.master)
        cads     = [10.0, 30.0, 60.0, 100.0, 300.0, 600.0, 1200.0, 1800.0, 3600.0]
        cads.sort()
        self.cad.set(300.0) # set the default option

        cad_menu = tk.OptionMenu(self.mainframe, self.cad, *cads)
        tk.Label(self.mainframe, text='Sampling cadence (s)').grid(row=1, column=2, padx=15, pady=2, sticky='W')
        cad_menu.grid(row=1, column=4, padx=5, pady=2, sticky='E')


        ## Declination of the source
        self.decl = tk.StringVar(self.master)
        tk.Label(self.mainframe, text='Source declination [-90, 90] (deg)').grid(row=2, column=2, padx=15, pady=2, sticky='W')
        tk.Entry(self.mainframe, textvariable = self.decl).grid(row=2, column=4, padx=5, pady=2, sticky='E')
        self.decl.set(20.0)




        ## Pixel scale in arsec of the source image
        self.pix_scale_img_asec = tk.StringVar(self.master)
        tk.Label(self.mainframe, text='Pixel scale (arcsec)').grid(row=3, column=2, padx=15, pady=2, sticky='W')
        tk.Entry(self.mainframe, textvariable=self.pix_scale_img_asec).grid(row=3, column=4, padx=5, pady=2, sticky='E')
        self.pix_scale_img_asec.set(1.0)
        self.pix_scale_img_asec.trace('w', self.update_pixscale)
        self.update_pixscale()








        # Frequency [MHz]
        self.freq = tk.StringVar(self.master)
        freqs     = ['HI 1420.406', 'OH 1612.231', 'OH 1665.402', 'OH 1667.359', 'OH 1720.53', 'HCO+ 89.189',
                 'CO 115.271', 'C17O 112.359', '13CO 110.201', 'C18O 109.782', 'CI 492.162']
        freqs.sort()
        self.freq.set('HI 1420.406') # set the default option

        freq_menu = tk.OptionMenu(self.mainframe, self.freq, *freqs)
        tk.Label(self.mainframe, text='Frequency [MHz]').grid(row=4, column=2, padx=15, pady=2, sticky='W')
        freq_menu.grid(row=4, column=4, padx=5, pady=2, sticky='E')

        



        ## Plot elevation curve
        tk.Button(self.mainframe, text='1. Elevation curve', bg='orange', fg='black',
            command = self.plot_elevation).grid(row=5, column=0, padx=5, pady=2, sticky='EW')

        ## UV-coverage
        self.white_fig(row=1, col=5, padx=5, pady=2)
        tk.Button(self.mainframe, text='2. UV Coverage', bg='orange', fg='black',
            command = self.uv_coverage).grid(row=5, column=1, padx=5, pady=2, sticky='EW')

        ## FFT of the source
        tk.Button(self.mainframe, text='3. Source FFT', bg='orange', fg='black',
            command = self.src_fft).grid(row=5, column=2, padx=5, pady=2, sticky='EW')

        ## Observed FFT
        self.white_fig(row=3, col=5, padx=5, pady=2)
        tk.Button(self.mainframe, text='4. Observed FFT', bg='orange', fg='black',
            command = self.obs_fft).grid(row=5, column=3, padx=5, pady=2, sticky='EW')


        ## Observed FFT
        self.white_fig(row=1, col=6, padx=5, pady=2)
        tk.Button(self.mainframe, text='5. Beam', bg='orange', fg='black',
            command = self.synth_beam).grid(row=5, column=4, padx=5, pady=2, sticky='EW')


        ## Observed image
        self.white_fig(row=3, col=6, padx=5, pady=2)
        tk.Button(self.mainframe, text='Go!', bg='orange', fg='black',
            command = self.observing).grid(row=5, column=5, columnspan=2, padx=5, pady=2, sticky='EW')


        ## Exit
        tk.Button(self.mainframe, text='Exit', bg='red', fg='black',
            command=self.client_exit).grid(row=0, column=5, columnspan=2, padx=5, pady=2, sticky='EW')


    
    




    def client_exit(self):
        exit()





    def white_fig(self, row=0, col=0, padx=0, pady=0):
        fig    = Figure(figsize=(3.5, 3.5))        
        canvas = FigureCanvasTkAgg(fig, master=self.mainframe)
        # canvas.get_tk_widget().pack()
        canvas.get_tk_widget().grid(row=row, column=col, padx=padx, pady=pady, sticky="EW")
        canvas.draw()
        plt.close()


    



    def show_textfile(self, filename, title=''):
        """Show a text file in a new window."""

        win = tk.Toplevel(background=self.bg_colour)
        win.title(title)
        txt = tkScrolledText(win, width=80, font=self.txtfont)
        txt.config(state="normal")
        with open(filename,'r') as f:
            text = f.read()
        txt.insert('1.0', text)
        txt.config(state="disabled")
        txt.grid(column=0, row=0, padx=5, pady=2, sticky="NSEW")
        xbtn = ttk.Button(win, text='Close',
                                   command=win.destroy)
        xbtn.grid(column=0, row=1, padx=5, pady=2, sticky="E")
        win.rowconfigure(0, weight=1)
        win.columnconfigure(0, weight=1)


    # on change dropdown value
    def change_dropdown(self,value):
        self.infor = cal.load_config('configs/' + self.array.get() + '.config')
        self.plot_ant_config()


    def plot_ant_config(self):
        x    = self.infor['east_coord_m']/1000.
        y    = self.infor['north_coord_m']/1000.
        dx   = np.max(x) - np.min(x)
        maxx = np.max(x) + 0.05*dx
        minx = np.min(x) - 0.05*dx
        if(minx == maxx):
            minx = minx - 0.1
            maxx = maxx + 0.1

        dy   = np.max(y) - np.min(y)
        maxy = np.max(y) + 0.05*dy
        miny = np.min(y) - 0.05*dy
        if(miny == maxy):
            miny = miny - 0.1
            maxy = maxy  + 0.1

        fig = Figure(figsize=(3.5, 3.5))
        a   = fig.add_subplot(111)
        a.scatter(x, y, color='red', marker='x')
        a.plot([0., 0.], [miny, maxy], 'k:', label='No. antennas: ' + str(self.infor['n_ant']))
        a.plot([minx, maxx], [0., 0.], 'k:', label='No. baselines: ' + str(self.infor['n_base']))
        a.plot([0., 0.], [0., 0.], 'k:', label='Diameter: ' + str(self.infor['diameter_m']) + ' m')
        a.plot([0., 0.], [0., 0.], 'k:', label='Min baseline: ' + str( round(self.infor['base_min'],1) ) + ' m')
        a.plot([0., 0.], [0., 0.], 'k:', label='Max baseline: ' + str( round(self.infor['base_max'],1) ) + ' m')
        # a.invert_yaxis()

        a.set_title (self.infor['telescope'] + ', ' + self.infor['config'] + ', Latitude: ' + str( round(self.infor['latitude_deg'],1) ) + '(deg)',
                     fontsize=10)
        a.set_ylabel('North-South [km]', fontsize=8)
        a.set_xlabel('East-West [km]', fontsize=8)
        a.tick_params(axis='x', direction='in', labelsize=7, pad=5)
        a.tick_params(axis='y', direction='in', labelsize=7)
        a.set_xlim(minx, maxx)
        a.set_ylim(miny, maxy)
        a.legend(loc='upper left', fontsize=8, handletextpad=0.0, handlelength=0)

        canvas = FigureCanvasTkAgg(fig, master=self.mainframe)
        # canvas.get_tk_widget().pack()
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=5, pady=2, sticky="EW")
        canvas.draw()
        plt.close()




    def plot_elevation(self):
        dec       = float(self.decl.get())
        samp_rate = float(self.cad.get())
        ha_end    = float(self.ha_end.get())
        ha_start  = float(self.ha_start.get())

        if( ha_end < ha_start ):
            print('HourAngle_end should be greater than HourAngle_start')
            sys.exit()

        ha_hr                 = np.array( [ha_start, ha_end] )
        ha_arr_hr, el_arr_deg = cal.get_elevation_curve(self.infor['latitude_rad'], ha_hr, dec, samp_rate)
        
        topwin = tk.Toplevel(background=self.bg_colour)
        topwin.title('Elevation')
        f      = Figure(figsize=(3.5,3.5), dpi=100)
        ax     = f.add_subplot(111)

        ax.plot(ha_arr_hr, el_arr_deg, 'b.', label=self.infor['telescope'])
        ax.plot(ha_arr_hr, el_arr_deg, 'k-', label='')

        # Format labels and legend
        ax.set_title('Elevation plot - ' + self.infor['telescope'] + ' - ' + self.infor['config'])
        ax.set_xlim(-12., 12.)
        ax.set_ylim(0.0, np.max(el_arr_deg) + 2.)
        ax.set_xlabel('Hour Angle [hours]')
        ax.set_ylabel('Elevation [degrees]')
        ax.margins(0.02)
        leg = ax.legend(shadow=False)
        for t in leg.get_texts():
            t.set_fontsize('small')

        canv = FigureCanvasTkAgg(f, topwin)
        canv.draw()
        canv.get_tk_widget().pack(side="top",fill='both',expand=True)
        # canv.pack(side="top",fill='both',expand=True)


    



    def src_fft(self):
        """Show the FFT of the src image."""

        # Plot the src FFT
        lim_kl =  self.fft_scale_lam/1.e3
        extent = [-lim_kl, lim_kl, -lim_kl, lim_kl]

        topwin = tk.Toplevel(background=self.bg_colour)
        topwin.title('FFT of src image')

        f  = Figure(figsize=(8,8), dpi=100)
        ax = f.add_subplot(111)


        ax.imshow(np.abs(self.src_fft_arr), norm=mpl.colors.LogNorm(), cmap=plt.cm.cubehelix,
                  interpolation='nearest', origin='lower', extent=extent)

        # Format labels and legend
        ax.set_title('FFT of source')
        ax.set_xlabel(u'u (k$\lambda$)')
        ax.set_ylabel(u'v (k$\lambda$)')
        ax.set_aspect('equal', 'datalim')
        ax.tick_params(axis='x', direction='in', labelsize=7, pad=2)
        ax.tick_params(axis='y', direction='in', labelsize=7)
        ax.margins(0.02)
        plt.setp(ax.get_yticklabels(), visible=True)
        plt.setp(ax.get_xticklabels(), visible=True)

        canv = FigureCanvasTkAgg(f, topwin)
        canv.draw()
        canv.get_tk_widget().pack(side='top',fill='both',expand=True)
        # canv.pack(side="top",fill='both',expand=True)




    def obs_fft(self):
        """Show the observed FFT of the src image."""
            
        if(not self.uv_status):
            print('')
            print('UV-coverage has not been calculated!')
            return
            # sys.exit()
        
        # Plot the observed FFT
        lim_kl =  self.fft_scale_lam/1.e3
        extent=[-lim_kl, lim_kl, -lim_kl, lim_kl]

        fig = Figure(figsize=(3.5, 3.5))
        ax  = fig.add_subplot(111)

        ax.imshow(np.abs(self.obs_fft_arr), norm=mpl.colors.LogNorm(), cmap=plt.cm.cubehelix,
                  interpolation="nearest", origin="lower", extent=extent)

        # Format labels and legend
        ax.set_title('Observed FFT of source')
        ax.set_xlabel(u'u (k$\lambda$)', fontsize=8)
        ax.set_ylabel(u'v (k$\lambda$)', fontsize=8)
        ax.set_aspect('equal', 'datalim')
        ax.tick_params(axis='x', direction='in', labelsize=4, pad=3)
        ax.tick_params(axis='y', direction='in', labelsize=4)
        ax.margins(0.02)
        plt.setp(ax.get_yticklabels(), visible=True)
        plt.setp(ax.get_xticklabels(), visible=True)

        canv = FigureCanvasTkAgg(fig, master=self.mainframe)
        canv.draw()
        canv.get_tk_widget().grid(row=3, column=5, padx=5, pady=2, sticky="EW")
        canv.draw()
        plt.close()





    def synth_beam(self, pRNG=(-0.1, 0.5)):
        """Show the Synthesised Beam."""
        # First check uv-coverage and model are available
        if(not self.griduv_status):
            print('')
            print('The uv-coverage has not been gridded!')
            return
        
        # Calc. the Synthesised Beam
        self.beam_arr = cal.get_synth_beam(self.griduv_status, self.uv_mask_arr)
        self.beam_arr = np.abs(self.beam_arr)

        # Catch blank arrays
        if self.beam_arr is None:
            return
        if self.beam_arr.max()==self.beam_arr.min():
            return


        # Set the colour clip to fractions of range, if requested
        zmin = None
        zmax = None
        if pRNG is not None:
            zmin = np.nanmin(self.beam_arr)
            zmax = np.nanmax(self.beam_arr)
            zRNG = zmin - zmax
            zmin -= zRNG * pRNG[0]
            zmax += zRNG * pRNG[1]
        if zmax==zmin:
            zmin = None
            zmax = None

        fig = Figure(figsize=(3.5, 3.5))
        ax  = fig.add_subplot(111)

        # Show the image array
        ax.imshow(self.beam_arr, cmap=plt.cm.cubehelix, interpolation='nearest',
                  origin='lower', vmin=zmin, vmax=zmax)

        # Format labels and legend
        ax.set_title('Synthesised Beam')
        # ax.set_xlabel(u'u (k$\lambda$)')
        # ax.set_ylabel(u'v (k$\lambda$)')
        ax.set_aspect('equal', 'datalim')
        ax.tick_params(axis='x', direction='in', labelsize=7, pad=2)
        ax.tick_params(axis='y', direction='in', labelsize=7)
        ax.margins(0.02)
        plt.setp(ax.get_yticklabels(), visible=True)
        plt.setp(ax.get_xticklabels(), visible=True)

        ax.set_axis_off()
        fig.set_tight_layout(True)

        canv = FigureCanvasTkAgg(fig, master=self.mainframe)
        canv.draw()
        canv.get_tk_widget().grid(row=1, column=6, padx=5, pady=2, sticky="EW")
        canv.draw()
        plt.close()

        self.beam_status = True
        
        


    

    def observing(self):
        # Check
        if(not self.griduv_status):
            print('')
            print('The uv-coverage has not been gridded!')
            return

        if(not self.beam_status):
            print('')
            print('The Synthesised Beam has not been established!')
            return

        self.obs_img_arr = cal.invert_obs(self.griduv_status, self.beam_status, self.obs_fft_arr)
        self.obs_img_arr = np.abs(self.obs_img_arr)

        
        fig = Figure(figsize=(3.5, 3.5))
        ax  = fig.add_subplot(111)

        # Show the image array
        ax.imshow(self.obs_img_arr, cmap=plt.cm.cubehelix, interpolation='nearest',
                  origin='lower', vmin=None, vmax=None)

        # Format labels and legend
        ax.set_title('Observed image')
        # ax.set_xlabel(u'u (k$\lambda$)')
        # ax.set_ylabel(u'v (k$\lambda$)')
        ax.set_aspect('equal', 'datalim')
        ax.tick_params(axis='x', direction='in', labelsize=7, pad=2)
        ax.tick_params(axis='y', direction='in', labelsize=7)
        ax.margins(0.02)
        plt.setp(ax.get_yticklabels(), visible=True)
        plt.setp(ax.get_xticklabels(), visible=True)

        ax.set_axis_off()
        fig.set_tight_layout(True)

        canv = FigureCanvasTkAgg(fig, master=self.mainframe)
        canv.draw()
        canv.get_tk_widget().grid(row=3, column=6, padx=5, pady=2, sticky='EW')
        canv.draw()
        plt.close()

        self.done = True

        print()
        print('Done!!')
        


    def uv_coverage(self):
        freq          = self.freq.get()
        line, freq    = freq.split(' ')
        self.freq_Hz  = float(freq) * 1e6
        self.line     = line
        self.lambda_m = self.C/self.freq_Hz
        
        dec           = float(self.decl.get())
        samp_rate     = float(self.cad.get())
        ha_end        = float(self.ha_end.get())
        ha_start      = float(self.ha_start.get())

        if( ha_end < ha_start ):
            print('HourAngle_end should be greater than HourAngle_start')
            sys.exit()
        
        ha_hr                          = np.array( [ha_start, ha_end] )
        ha_arr_hr, el_arr_deg          = cal.get_elevation_curve(self.infor['latitude_rad'], ha_hr, dec, samp_rate)
        
        self.u_arr_lda, self.v_arr_lda = cal.get_uv_coverage(self.infor, dec, ha_arr_hr, el_arr_deg, self.lambda_m)
        self.uv_status                 = True



        fig = Figure(figsize=(3.5, 3.5))
        ax  = fig.add_subplot(111)

        ax.scatter(x=self.u_arr_lda/1000., y=self.v_arr_lda/1000., marker='.', edgecolor='none',
                   s=2.5, color='r', zorder=0)
        ax.scatter(x=-self.u_arr_lda/1000., y=-self.v_arr_lda/1000., marker='.', edgecolor='none',
                   s=2.5, color='r', zorder=0)

        # Format labels and legend
        ax.set_title('UV Coverage')
        ax.set_xlabel(u'u (k$\lambda$)', fontsize=8)
        ax.set_ylabel(u'v (k$\lambda$)', fontsize=8)
        ax.set_aspect('equal', 'datalim')
        ax.tick_params(axis='x', direction='in', labelsize=4, pad=3)
        ax.tick_params(axis='y', direction='in', labelsize=4)
        ax.margins(0.02)
        plt.setp(ax.get_yticklabels(), visible=True)
        plt.setp(ax.get_xticklabels(), visible=True)

        canv = FigureCanvasTkAgg(fig, master=self.mainframe)
        canv.draw()
        canv.get_tk_widget().grid(row=1, column=5, padx=15, pady=2, sticky="EW")
        canv.draw()
        plt.close()


        self.uv_mask_arr, self.uv_cnt_arr, self.obs_fft_arr = cal.grid_uvcoverage(self.src_fft_status, self.uv_status, self.src_fft_arr,\
                                                                                  self.fft_scale_lam, self.pix_scale_fftX_lam, self.pix_scale_fftY_lam,\
                                                                                  self.u_arr_lda, self.v_arr_lda)
        self.griduv_status = True







    def show_src(self, *args):
        # reading png image
        src_file         = 'sources/' + self.src.get() + '.png'
        # ximg           = mpl.image.imread(src_file)

        print(src_file)
        
        ximg             = Image.open(src_file).convert("L")
        self.src_img_arr = np.flipud(np.asarray(ximg))
        self.ny, self.nx = self.src_img_arr.shape

        self.src_status  = True

        fig = Figure(figsize=(4, 4))
        a   = fig.add_subplot(111)

        a.imshow(ximg, cmap=plt.cm.cubehelix, interpolation='nearest')
        a.set_axis_off()

        # a.set_aspect('equal')
        # fig.tight_layout()
        fig.set_tight_layout(True)

        canvas = FigureCanvasTkAgg(fig, master=self.mainframe)
        # canvas.get_tk_widget().pack()
        canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, padx=5, pady=2, sticky="EW")
        canvas.draw()
        plt.close()


        if(self.src_fft_status):
            self.src_fft_arr, self.pix_scale_img_lam, self.fft_scale_lam,\
            self.pix_scale_fftX_lam, self.pix_scale_fftY_lam = cal.invert_src_img(self.src_status, self.src_img_arr, self.pix_scale_img_asec, self.nx, self.ny)





    def update_pixscale(self, *args):
        pix_scale_img_asec = self.pix_scale_img_asec.get()
        if(self.src_status and (pix_scale_img_asec != '') ):
            self.pix_scale_img_asec = float( pix_scale_img_asec )
            self.pix_scale_img_deg  = self.pix_scale_img_asec / 3600.0
            text = ' %d x %d pix  /  %s x %s' % (self.nx, self.ny,
                cal.ang2str(self.nx * self.pix_scale_img_deg),
                cal.ang2str(self.ny * self.pix_scale_img_deg))
            tk.Label(self.mainframe, text=text).grid(row=4, column=0, padx=5, pady=2, sticky='EW')

            self.src_fft_arr, self.pix_scale_img_lam, self.fft_scale_lam,\
            self.pix_scale_fftX_lam, self.pix_scale_fftY_lam = cal.invert_src_img(self.src_status, self.src_img_arr, self.pix_scale_img_asec, self.nx, self.ny)

            self.src_fft_status = True








# root window created. Here, that would be the haveonly window, but
# you can later have windows within windows.
root = tk.Tk()

# root.minsize(640, 100)
root.geometry('1800x900')
root.resizable(0, 0)

#creation of an instance
app = Window(root)

#mainloop 
root.mainloop()  