from tkinter import filedialog
from tkinter import *
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
from astropy.io import fits
import matplotlib.colors
import cv2
from astropy.visualization.mpl_normalize import simple_norm
import math
from skimage import exposure
from astropy.wcs import WCS
import os
import warnings
from tkinter import messagebox as MessageBox
from astropy.stats import sigma_clip
from scipy import interpolate
from astropy.coordinates import SkyCoord
from PIL import Image
from PIL import ImageTk
import matplotlib.patches as patches
from tkinter import scrolledtext
import platform  

warnings.filterwarnings("ignore")

class prueba_ifsUW():
    
    
    file_dir = ''
    band = 0
    name = ''
    hi_data = ''
    data = ''
    header_file = ''
    wcs_header = ''
    size_x  = 0
    size_y  = 0
    pixels = 1
    x_ticks = []
    y_ticks = []
    x_ticks_l = []
    y_ticks_l = []
    Integrated_spectrum =[]
    integrated_x = []
    integrated_y = []
    
    wcs = 0 
    arrlambda = np.zeros(pixels) 
    array_data = 0
    dband=0
    res = []
    cir_x = 0
    cir_y = 0
    name_f = "" 
    
    spectrum= 0    
    min_value_da= 0
    max_value_da= 0
    ####Flags
    flag_explorer = 0
    flag_flux=0
    flag_wave=0
    flag_band=0
    flag_file=0
    flag_integrate_region = 0
    flag_integrate_region2 = 0
    flag_create_fits = 0
    flag_system = 0 
    red_marks = []
    maps_array = []
    maps_array_inv = []
    ax1 = 0
    ax0 = 0
    saved_image = 0
    imagen_final = 0
    color = "#E6E6FA"

    ##variables for the graphic part
    window = Tk()
    window.title("IFS Explorer")
    window.geometry("1350x730")
    window.resizable(0, 0)
    radius_ = IntVar()
    band_sticks = IntVar()
    min_value_la = 0
    max_value_la = 0
    varla1 = StringVar()
    varlaflux = StringVar() 
    varla3 = DoubleVar()
    varla4 = DoubleVar()
    varlawave = StringVar()
    varla5 = IntVar()
    varla6 = IntVar()
    varla7 = StringVar()
    varla8 = StringVar()
    varla9 = StringVar()
    varla10 = StringVar()
    varla11 = DoubleVar()
    var = IntVar() 
    var.set(1)
    var3 = StringVar()
    var3 = StringVar()
    sp1 = IntVar()
    
    ##graphic elements
    box_entry = 0
    entry_Radius = 0
    entry_wvlenMin = 0
    entry_wvlenMax = 0
    entry_MWave = 0
    entry_shFiltmin = 0
    entry_shFiltmax = 0
    entry_shFilt = 0
    bar_ = 0
    canvas = 0
    f2 = ''
    canvas2 = 0
    f = 0
    combo1 = 0
    combo2 = 0
    
    
    def __init__(self): 
        '''
        function that define the type of Operative System, necesarry to know how access to the files 
        like image or filters
        '''
        def operative_system():
            sistema = platform.system()
            if sistema == "Windows":
                (self.flag_system) = 0
            else:
                (self.flag_system) = 1
        '''
        function that defines the maps_array and maps_array_inv, necessary to 
        Function set_color_map()
        '''
        def get_cmaps():
            #parte para crear los mapas solo una vez:
            prism = matplotlib.colors.LinearSegmentedColormap.from_list('custom prism', [(0,    "white"),(0.2, '#000000'),(0.4, '#8b0000'),(0.6, '#f63f2b'),(0.8, '#15E818'),(1, '#1139d9'  )], N=256)
            stern = matplotlib.colors.LinearSegmentedColormap.from_list('custom stern',[(0,    "white"),(0.2, '#8b0000'),(0.3, '#e42121'),(0.4, '#252850'),(0.6, '#0588EF'), (0.8, '#3b83bd'),(1, '#c6ce00'  )], N=256)
            std = matplotlib.colors.LinearSegmentedColormap.from_list('custom Std-Gamma', [(0,    "white"),(0.2, '#0000ff'),(0.4, '#2178E4'),(0.6, '#ff0000'),(0.8, '#ff8000'),(1, '#ffff00'  )], N=256)
            BGRY = matplotlib.colors.LinearSegmentedColormap.from_list('custom BGRY', [(0,    "white"),(0.2, '#ff8000'),(0.4, '#EFEE05'),(0.6, '#EF5A05'),(0.8, '#51EF05'),(1, '#0000ff'  )], N=256)
            califa = matplotlib.colors.LinearSegmentedColormap.from_list('custom CALIFA special', [(0,    "white"),(0.25, '#00008B'),(0.5, '#B2FFFF'),(0.62, '#B2FFFF'),(0.75, '#ff4000'),(1, '#008f39'  )], N=256)
            ping = matplotlib.colors.LinearSegmentedColormap.from_list('custom Pingsoft-special', [(0,    "white"),(0.25, '#00008B'),(0.5, '#3b83bd'),(0.75, '#ff8000'),(1, '#ffff00'  )], N=256)
            
            
            prism_r= matplotlib.colors.LinearSegmentedColormap.from_list('custom prism inv', [(0,    '#1139d9'),(0.2, '#15E818'),(0.4, '#f63f2b'),(0.6, '#8b0000'),(0.8, '#000000'),(1, "white"  )], N=256)
            stern_r= matplotlib.colors.LinearSegmentedColormap.from_list('custom strn inv', [(0,    '#c6ce00'),(0.2, '#3b83bd'),(0.3, '#0588EF'),(0.4, '#252850'),(0.6, '#e42121'),(0.8, '#8b0000'),(1, "white"  )], N=256)
            std_r= matplotlib.colors.LinearSegmentedColormap.from_list('custom std inv', [(0,    '#ffff00'),(0.2, '#ff8000'),(0.4, '#ff0000'),(0.6, '#2178E4'),(0.8, '#0000ff'),(1, "white"  )], N=256)
            BGRY_r= matplotlib.colors.LinearSegmentedColormap.from_list('custom BGRY inv', [(0,    '#0000ff'),(0.2, '#51EF05'),(0.4, '#EF5A05'),(0.6, '#EFEE05'),(0.8, '#ff8000'),(1, "white"  )], N=256)
            califa_r= matplotlib.colors.LinearSegmentedColormap.from_list('custom CALIFA inv', [(0,    '#008f39'),(0.25, '#ff4000'),(0.5, '#B2FFFF'),(0.62, '#B2FFFF'),(0.75, '#00008B'),(1, "white"  )], N=256)
            ping_r= matplotlib.colors.LinearSegmentedColormap.from_list('custom Pingsoft inv', [(0,    '#ffff00'),(0.25, '#ff8000'),(0.5, '#3b83bd'),(0.75, '#00008B'), (1, "white"  )], N=256)
            
            (self.maps_array).append('Blues')
            (self.maps_array).append('Reds')
            (self.maps_array).append('Greens')
            (self.maps_array).append('Greys')
            (self.maps_array).append(ping)
            (self.maps_array).append(califa)
            (self.maps_array).append('rainbow')
            (self.maps_array).append(BGRY)
            (self.maps_array).append(prism)
            (self.maps_array).append(stern)
            (self.maps_array).append(std)
            (self.maps_array_inv).append('Blues_r')
            (self.maps_array_inv).append('Reds_r')
            (self.maps_array_inv).append('Greens_r')
            (self.maps_array_inv).append('Greys_r')
            (self.maps_array_inv).append(ping_r)
            (self.maps_array_inv).append(califa_r)
            (self.maps_array_inv).append('rainbow_r')
            (self.maps_array_inv).append(BGRY_r)
            (self.maps_array_inv).append(prism_r)
            (self.maps_array_inv).append(stern_r)
            (self.maps_array_inv).append(std_r)
        '''
        Function to control the click inside the canvas that  display the FITS image
        and controls the function to select the spaxel for integrate_region()
        '''
        def onclick_(event):
            if (self.flag_file)==1:
                if (self.flag_integrate_region) == 0:
                    if (self.flag_explorer) == 1:
                        (self.flag_explorer) = 0
                        (self.varla10).set("Explorer OFF")
                    else:
                        (self.flag_explorer) = 1
                        (self.varla10).set("Explorer ON")
                else:
                    if (self.flag_integrate_region2) == 0:
                        try:
                            cord_x = int(round(event.xdata))
                            cord_y = int(round(event.ydata))
                            draw_circle(int(round(event.xdata)), int(round(event.ydata)))
                            
                        except Exception as e:
                            print(e)
        '''
        Function to register the mouse movement within the canvas that shows the image fits,
        when the explorer is active and the mousse is adove a spaxel, call the function
        coordinates()
        '''
        def move_mouse(event):
            if (self.flag_explorer) == 1:
                try:
                    cord_x = int(round(event.xdata))
                    cord_y = int(round(event.ydata))
                    coordinates_(int(round(event.xdata)), int(round(event.ydata)))
                except Exception as e:
                    var = "not spaxel in graph"
        '''
        Function to set wavelength range, with varla5 and varla6 for the minimum and maximum
        values, is only for varla5 < varla6, with 
        minimum value of array lambda <=  varla5 < varla6 <= maximum value of array lambda
        Negative values are not accepted
        '''
        def set_wavelength_range():
            if (self.flag_file)==1:
                try:
                    if (self.varla5).get() >= (self.varla6).get() or ((self.varla6).get() >=  (self.max_value_la) and (self.varla5).get() >=  (self.max_value_la)) or ((self.varla6).get() <=  (self.min_value_la) and (self.varla5).get() <=  (self.min_value_la)) :
                        MessageBox.showerror("Error!","The minimum and the maximum value should be differents and the first value minimum that the second")
                        (self.varla5).set(int(self.min_value_la))
                        (self.varla6).set(int(self.max_value_la))
                        (self.ax0).set_xlim(xmin=(self.min_value_la),xmax=(self.max_value_la))
                        (self.canvas).draw()
                    else:
                        if (self.varla5).get() >= (self.min_value_la) and (self.varla6).get() <= (self.max_value_la):
                            (self.ax0).set_xlim(xmin=(self.varla5).get(),xmax=(self.varla6).get())
                            (self.flag_wave) = 1
                            (self.canvas).draw()
                        else:
                            if (self.varla5).get() >= (self.min_value_la) and (self.varla6).get() > (self.max_value_la):
                                MessageBox.showwarning("Warning!","The maximum value is %d"%(np.amax((self.arrlambda))))     
                                (self.ax0).set_xlim(xmin=(self.varla5).get(),xmax=(self.max_value_la))
                                (self.varla6).set(int(((self.ax0).get_xlim())[1]))
                                (self.flag_wave) = 1
                                (self.canvas).draw()
                            else:
                                if (self.varla5).get() < (self.min_value_la) and (self.varla6).get() <= (self.max_value_la):
                                    MessageBox.showwarning("Warning!","The minimum value is %d"%((self.min_value_la)))
                                    (self.ax0).set_xlim(xmin=(self.min_value_la),xmax=(self.varla6).get())
                                    (self.varla5).set(int(((self.ax0).get_xlim())[0]))
                                    (self.flag_wave) = 1
                                    (self.canvas).draw()
                                else:
                                    MessageBox.showwarning("Warning!","The minimum value is %d and the maximum value is %d"%((self.min_value_la),(self.max_value_la)))
                                    (self.varla5).set(int(self.min_value_la))
                                    (self.varla6).set(int(self.max_value_la))
                                    (self.ax0).set_xlim(xmin=(self.min_value_la),xmax=(self.max_value_la))
                                    (self.canvas).draw()
                except Exception as e:    
                       MessageBox.showerror("Error!","Please, enter numbers")
                       (self.varla5).set(int(self.min_value_la))
                       (self.varla6).set(int(self.max_value_la))
                       (self.ax0).set_xlim(xmin=(self.min_value_la),xmax=(self.max_value_la))
                       (self.canvas).draw()
                
            else:
                MessageBox.showerror("Error!","Please, select a file")
        '''
        function to reset wavelength range to the origins values that are show in the variables of:
            varla5 = minimum value of the array lambda
            varla6 = maximum value of the array lambda
        '''
        def reset_wavelength_range():
            print("reset wave")
            if (self.flag_file)==1:
                if (self.flag_wave) == 1:
                    (self.flag_wave) = 0
                    (self.varla5).set(int(self.min_value_la)) 
                    (self.varla6).set(int(self.max_value_la))
                    (self.ax0).set_xlim(xmin=(self.min_value_la),xmax=(self.max_value_la))
                    (self.canvas).draw()
            else:
                MessageBox.showerror("Error!","Please, select a file") 
        
        '''
        function to set the flux range with varla3 and varla4 for the minimum and maximum
        values, is only for varla3 < varla4, negative values are accepted
        '''
        def set_flux_range():
            if (self.flag_file)==1:
                try:
                    if (self.varla3).get() < (self.varla4).get():
                        (self.ax0).set_ylim(ymin=(self.varla3).get(),ymax=(self.varla4).get())
                     #   (self.canvas).draw()
                        (self.flag_flux)=1
                        for i in (self.red_marks):
                            (self.ax0).axvline(int(i),(self.varla3).get(),(self.varla4).get(),color='red')
                        (self.canvas).draw()
                            
                    else:
                        MessageBox.showerror("Error!","The minimum value should be minimum that the maximum value")
                        reset_flux_range()
                except Exception as e:   
                       print(e)
                       MessageBox.showerror("Error!","Please, enter numbers")
                       reset_flux_range()
               
               
            else:
                MessageBox.showerror("Error!","Please, select a file") 
        '''
        function to reset flux range
        varla3 = minimum value of the actual spectrum
        varla4 = maximum value of the actual spectrum
        '''
        def reset_flux_range():
            if (self.flag_file)==1:
                (self.flag_flux)=0
                (self.varla3).set(0)
                (self.varla4).set(0)
                if (self.flag_integrate_region)==1 and (self.flag_integrate_region2)==1:
                    (self.ax0).set_ylim(ymin=np.amin((self.Integrated_spectrum)),ymax=np.amax((self.Integrated_spectrum))*1.2)
                else:
                    (self.ax0).set_ylim(ymin=np.amin((self.spectrum)),ymax=np.amax((self.spectrum))*1.2)
                for i in (self.red_marks):
                    (self.ax0).axvline(int(i),(self.min_value_da),(self.max_value_da),color='red')
                (self.canvas).draw()
            else:
                MessageBox.showerror("Error!","Please, select a file") 
        '''function to set the label that show the value of the band.
        changes when user move the scale bar
        '''
        def set_bar(bar_1):
            (self.varla11).set(bar_1)
        '''function to set the value of the band,is defined by the variable varla11
        when the user enters the number of the band directly, it affects changing
        the value of the scale bar
        '''
        def set_band():
            if (self.flag_file)==1:
                try:
                    (self.band) = (self.varla11).get()
                    (self.bar_).set((self.varla11).get())
               #     (self.varla11).set((self.varla11).get())
                    (self.flag_band)=1
                    filters_(self.name_f)
                    set_scaling() 
                except Exception as e: 
                       (self.varla11).set((self.band))
                       (self.bar_).set((self.varla11).get())
                       MessageBox.showerror("Error!","Please, enter numbers") 
            else:
                MessageBox.showerror("Error!","Please, select a file")
        
        '''function to set scale, affect only to the image of the FITS file
        the image should be clear to apply a scale
        Depends of the display axis, the color map and the filter applied
        '''    
        def set_scaling():
            if (self.flag_file)==1:
                scaling = (self.var).get()
                if (self.sp1).get()==1:
                    cmap_1=(self.maps_array_inv)[(self.combo1).current()]
                else:
                    cmap_1=(self.maps_array)[(self.combo1).current()]
                if (self.band_sticks).get() == 0:
                    (self.f2).clf()
                    (self.ax1) = (self.f2).add_subplot(projection=(self.wcs_header), slices=('x', 'y', 2))
                else:
                    (self.ax1).cla()
                    (self.ax1).set_xlabel( 'RA (arcsec)' )
                    (self.ax1).set_ylabel( 'DEC (arcsec)' )
                    (self.ax1).set_xticks((self.x_ticks))
                    (self.ax1).set_yticks((self.y_ticks))
                    (self.ax1).set_xticklabels((self.x_ticks_l))
                    (self.ax1).set_yticklabels((self.y_ticks_l))      
                if scaling == 1:
                    (self.saved_image)=(self.ax1).imshow((self.image_final),cmap=cmap_1,interpolation='nearest',origin='lower' )
                    lineal = simple_norm((self.image_final), stretch='linear')
                    (self.saved_image).set_norm(lineal)
                else:
                    if scaling == 2:
                        total = sigma_clip((self.image_final), sigma=2)
                        (self.saved_image)=(self.ax1).imshow(total,cmap=cmap_1,interpolation='nearest',origin='lower' )
                    else:
                        if scaling == 3:
                            (self.saved_image)=(self.ax1).imshow((self.image_final),cmap=cmap_1,interpolation='nearest',origin='lower' )
                            asin_h = simple_norm((self.image_final), stretch='asinh')
                            (self.saved_image).set_norm(asin_h)
                        else:
                            if scaling == 4:
                                (self.saved_image)=(self.ax1).imshow((self.image_final),cmap=cmap_1,interpolation='nearest',origin='lower' )
                                power = 2.0
                                power_l = simple_norm((self.image_final), stretch='power', power=power)
                                (self.saved_image).set_norm(power_l)
                            else:
                                if scaling == 5:
                                    (self.saved_image)=(self.ax1).imshow((self.image_final),cmap=cmap_1,interpolation='nearest',origin='lower')
                                    raiz_c = simple_norm((self.image_final), stretch='sqrt')
                                    (self.saved_image).set_norm(raiz_c)
                                else:
                                    if scaling == 6:
                                        (self.saved_image)=(self.ax1).imshow((self.image_final),cmap=cmap_1,interpolation='nearest',origin='lower' )
                                        img_cdf, bin_centers = exposure.cumulative_distribution((self.image_final))
                                        final = np.interp((self.image_final),bin_centers,img_cdf)
                                #        (self.ax1).cla()
                                        (self.saved_image)=(self.ax1).imshow(final,cmap=cmap_1,interpolation='nearest',origin='lower' )
                                    else:
                                        if scaling == 7:
                                            (self.saved_image)=(self.ax1).imshow((self.image_final),cmap=cmap_1,interpolation='nearest',origin='lower' )
                                            sigma=1
                                            norm_img = np.zeros((self.size_x,self.size_y))
                                            imagen_pi = cv2.normalize((self.image_final),norm_img, -math.pi, math.pi, cv2.NORM_MINMAX)
                                            una=1/(sigma*math.sqrt(2*math.pi))
                                            cuadrado=np.power(imagen_pi,2)
                                            division= cuadrado/(2*(sigma**2))
                                            dos = np.exp(-division)
                                            total=una*dos
                                 #           (self.ax1).cla()
                                            (self.saved_image)=(self.ax1).imshow(total,cmap=cmap_1,interpolation='nearest',origin='lower' )
                                        else:
                                            (self.saved_image)=(self.ax1).imshow((self.image_final),cmap=cmap_1,interpolation='nearest',origin='lower' )
                                            log_a = 100
                                            loga = simple_norm((self.image_final), stretch='log', log_a=log_a)
                                            (self.saved_image).set_norm(loga)
                                            
                if (self.flag_integrate_region) == 1 and (self.flag_integrate_region2) == 1:
                        cd = (self.header_file)['CDELT1']
                        if cd > 1:
                            new_r = (self.radius_).get()/cd
                        else:
                            new_r = int(round((self.radius_).get()/cd))
                            
                        
                        cir = patches.Circle(((self.cir_x),(self.cir_y)),int(new_r),edgecolor='red',fill = False)
                        (self.ax1).add_patch(cir)
                        
                (self.canvas2).draw()
            else:
                MessageBox.showerror("Error!","Please, select a file") 
                (self.var).set(1)
        '''
        Fuction that is called when the user change the filter for the combobox
        Their main function is calls the function Filers_
        
        '''
        def set_filter(event):
            if (self.flag_file)==1:
                combo_2 = event.widget.get()
                (self.name_f) = combo_2 + '.txt'
                (self.flag_band)=0
                filters_((self.name_f))
            else:
                MessageBox.showerror("Error!","Please, select a file")
                (self.combo2).current(0)
        '''
        Fuction that is called when the user change the color map for the combobox
        or apply the invert color map, depends of the variable maps_array and maps_array_inv
        
        '''
        def set_color_map(event=''):
            if (self.flag_file)==1:
                if (self.sp1).get()==1:
                    (self.saved_image).set_cmap((self.maps_array_inv)[(self.combo1).current()])
                else:
                    (self.saved_image).set_cmap((self.maps_array)[(self.combo1).current()])
                (self.canvas2).draw()
            else:
                (self.sp1).set(0)
                (self.combo1).current(0)
                MessageBox.showerror("Error!","Please, select a file") 
        '''
        function to clear the marks on the wavelength
        '''
        def reset_mark_wavelength():
            if (self.flag_file)==1:
                (self.red_marks) = []
                (self.var3).set("")
                (self.ax0).cla()
                (self.ax0).set_xlabel( 'Wavelength' )
                (self.ax0).set_ylabel( 'Flux' )
                
                if (self.flag_integrate_region) == 1 and (self.flag_integrate_region2) == 1:
                    if (self.flag_flux)==1:
                        (self.ax0).set_ylim(ymin=(self.varla3).get(),ymax=(self.varla4).get())
                        (self.ax0).plot((self.arrlambda),(self.res)*(self.varla4).get(),'--',color = 'orange')
                    else:
                     #   (self.ax0).plot((self.arrlambda),(self.res)*np.amax((self.Integrated_spectrum))*1.2,'--',color = 'orange')
                        (self.ax0).set_ylim(ymin=np.amin((self.Integrated_spectrum)),ymax=np.amax((self.Integrated_spectrum))*1.2)
                        
                    (self.ax0).plot((self.arrlambda),(self.Integrated_spectrum),color='red')
                    if (self.flag_wave) == 1:
                            (self.ax0).set_xlim(xmin=(self.varla5).get(),xmax=(self.varla6).get())
                    else:
                            (self.ax0).set_xlim(xmin=(self.min_value_la),xmax=(self.max_value_la))
                        
                else:
                    (self.ax0).plot((self.arrlambda),(self.spectrum),color='blue')
                    if (self.flag_flux)==1:
                        (self.ax0).set_ylim(ymin=(self.varla3).get(),ymax=(self.varla4).get())
                        (self.ax0).plot((self.arrlambda),(self.res)*(self.varla4).get(),'--',color = 'orange')
                    else:
                        (self.ax0).plot((self.arrlambda),(self.res)*np.amax((self.spectrum))*1.2,'--',color = 'orange')
                        (self.ax0).set_ylim(ymin=np.amin((self.spectrum)),ymax=np.amax((self.spectrum))*1.2)
                    if (self.flag_wave) == 1:
                        (self.ax0).set_xlim(xmin=(self.varla5).get(),xmax=(self.varla6).get())
                    else:
                        (self.ax0).set_xlim(xmin=(self.min_value_la),xmax=(self.max_value_la))
                (self.canvas).draw()
            else:
                MessageBox.showerror("Error!","Please,select a file")
                
        '''
        function to draw one or many lines in the graph, for mark a value on the wavelength
        the sintax is: number separaters by a coma
        example: 400,500
        the values should be:
        minimum value of the array lambda <= x <= maximum value of the array lambda
        '''
        
        def mark_wavelength():
            if (self.flag_file)==1:
                mark = (self.var3).get()
                (self.red_marks) = mark.split(',')
                b = 0
                try:
                    for i in (self.red_marks):
                        if int(i) < (self.min_value_la) or int(i) > (self.max_value_la):
                            b = 1
                        else:
                            (self.ax0).axvline(int(i),(self.min_value_da),(self.max_value_da),color='red')
                    if b == 1:
                        MessageBox.showwarning("Warning!","The minimum value is %d and the maximum value is %d"%((self.min_value_la),(self.max_value_la)))
                        (self.red_marks) = []
                        (self.var3).set("")
                    else:            
                      (self.canvas).draw()
                except Exception as e: 
                       MessageBox.showerror("Error!","Please, enter numbers") 
                       (self.red_marks) = []
                       (self.var3).set("")
            else:
                MessageBox.showerror("Error!","Please, select a file")
        '''
        function to create the labels for show the values of the image FITS in arcsec 
        this depends of the values CDELT1 and CDELT2 (0<CDELT1>0.01 and 0<CDELT2>0.01)
        and the center of the values CRPIX1 and CRPIX2 (that should be 0<CRPIX1<NAXIS1
                                                        0<CRPIX2<NAXIS2)
        '''
        def create_label_offset():
            try:
                (self.x_ticks)=[]
                (self.y_ticks)=[]
                (self.x_ticks_l)=[]
                (self.y_ticks_l)=[]
                cdelt_1 = (self.header_file)['CDELT1']
                cdelt_2 = (self.header_file)['CDELT2']
                
                    
                    
                if cdelt_1 <= 0: 
                    cdelt_1 = cdelt_1*-1
                if cdelt_2 <= 0: 
                    cdelt_1 = cdelt_2*-1
                    
                if cdelt_1 <= 0.01: 
                    cdelt_1 = cdelt_1*100
                    
                if cdelt_2 <= 0.01: 
                    cdelt_2 = cdelt_2*100
                    
                text_1 = (u"CDELT1 = %f  \nCDELT2 = %f \n"%(cdelt_1,cdelt_2) )
                (self.box_entry).configure(state='normal')
                (self.box_entry).insert(INSERT, text_1)
                (self.box_entry).see(END)
                (self.box_entry).configure(state='disabled')
                crpix_1 = (self.header_file)['CRPIX1']
                crpix_2 = (self.header_file)['CRPIX2']
                if crpix_1 <= 0 or crpix_1 > (self.size_x):
                    crpix_1 = int((self.size_x)/2)
                    text_1 = (u"CRPIX1 entry was negative or greater than NAXIS1, using CRPIX1= NAXIS1/2 \n" )
                    (self.box_entry).configure(state='normal')
                    (self.box_entry).insert(INSERT, text_1)
                    (self.box_entry).see(END)
                    (self.box_entry).configure(state='disabled')
                else:
                    text_1 = (u"CRPIX1 = %f\n"%(crpix_1) )
                    (self.box_entry).configure(state='normal')
                    (self.box_entry).insert(INSERT, text_1)
                    (self.box_entry).see(END)
                    (self.box_entry).configure(state='disabled')
                    
                if crpix_2 <= 0 or crpix_2 > (self.size_y):
                    crpix_2 = int((self.size_y)/2)
                    text_1 = (u"CRPIX2 entry was negative or greater than NAXIS2, using CRPIX2= NAXIS2/2 \n" )
                    (self.box_entry).configure(state='normal')
                    (self.box_entry).insert(INSERT, text_1)
                    (self.box_entry).see(END)
                    (self.box_entry).configure(state='disabled')
                else:
                    text_1 = (u"CRPIX2 = %f\n"%(crpix_2) )
                    (self.box_entry).configure(state='normal')
                    (self.box_entry).insert(INSERT, text_1)
                    (self.box_entry).see(END)
                    (self.box_entry).configure(state='disabled')
                    
                (self.x_ticks)= np.linspace(0,(self.size_x)-1,(self.size_x))
                (self.y_ticks)= np.linspace(0,(self.size_y)-1,(self.size_y))
                for s in range((self.size_x)):
                    (self.x_ticks_l).append("")
                for s in range((self.size_y)):
                    (self.y_ticks_l).append("")
                        
                (self.x_ticks_l)[int(round(crpix_1))] = 0    
                (self.y_ticks_l)[int(round(crpix_2))] = 0
        
                
                
                num_a=((self.size_x) * cdelt_1)/(self.size_x)
                num_b=((self.size_y) * cdelt_2)/(self.size_y)
                    
                s_1 = int(round(crpix_1+1))
                inter_1=int(round((self.size_x)/10))
                cont_1=0
                while s_1 < (self.size_x):
                    if cont_1%inter_1 == 0 and cont_1 != 0:
                        (self.x_ticks_l)[s_1]=int(round(cont_1*-1*num_a))
                    cont_1=cont_1+1
                    s_1 = s_1+1
                s_1 = int(crpix_1-1)
                cont_1=0;
                while s_1 > 0:
                    if cont_1%inter_1 == 0 and cont_1 != 0:
                        (self.x_ticks_l)[s_1]=int(round(cont_1*num_a))
                    cont_1=cont_1+1
                    s_1 = s_1-1    
                s_1 = int(round(crpix_2+1))
                inter_1=int(round((self.size_y)/10))
                cont_1=0
                while s_1 < (self.size_y):
                    if cont_1%inter_1 == 0 and cont_1 != 0 :
                        (self.y_ticks_l)[s_1]=int(round(cont_1*num_b))
                    cont_1=cont_1+1
                    s_1 = s_1+1
                s_1 = int(crpix_2-1)
                cont_1=0
                while s_1 > 0:
                    if cont_1%inter_1 == 0 and cont_1 != 0:
                        (self.y_ticks_l)[s_1]=int(round(cont_1*-1*num_b))
                    cont_1=cont_1+1
                    s_1 = s_1-1
        
            except Exception as e:    
                print(e)
                
        '''
        Verify that exists a circle drew in the image
        create three files in the functions create_txt, create_spectrum_fits, create_circle_fits
        '''
        def create_files():
            if (self.flag_file)==1:
                if (self.flag_integrate_region) == 1 and (self.flag_integrate_region2)==1:
                    if (self.flag_create_fits) == 0:
                        create_txt()
                        create_spectrum_fits()
                        create_circle_fits()
                        (self.flag_create_fits) = 1
                    else:
                        MessageBox.showerror("Error!","Please, select other region to create files")
                    
                    
                else:
                    MessageBox.showerror("Error!","Please, first integrate a region")#revisar
            else:
                MessageBox.showerror("Error!","Please, select a file")
        '''
        Function that create the file of the integrated spectrum in the format:
            number of the line     value of the array lambda   value of the integrated spectrum
        The extention of the file is .txt
            
        '''
        def create_txt():
            try:
                name_text = (self.varla1).get()
                name_text = name_text.split('.')
                name_text = name_text[0]+'.spectrum_'+str((self.cir_x))+'_'+str((self.cir_y))+'.text'
                final_dir = (self.file_dir).replace((self.varla1).get(),name_text)
                
                file = open(final_dir, "w")
                for i in range(len((self.arrlambda))):
                    line = "   %d     %f     %f  \n"%(i+1,(self.arrlambda)[i],(self.Integrated_spectrum)[i])
                    file.write(line)
                file.close()
                text_1 = (u"File created: %s\n"%(name_text))
                (self.box_entry).configure(state='normal')
                (self.box_entry).insert(INSERT, text_1)
                (self.box_entry).see(END)
                (self.box_entry).configure(state='disabled')
            except Exception as e:
                print(e)        
        '''Function that create the file of the integrated spectrum in the format FITS
        without the information of array lambda.
            
        '''
        def create_spectrum_fits():
            try:
                name_spectrum = (self.varla1).get()
                name_spectrum = name_spectrum.split('.')
                name_spectrum = name_spectrum[0]+'.spectrum_'+str((self.cir_x))+'_'+str((self.cir_y))+'.fits'
                fits_s = fits.PrimaryHDU((self.Integrated_spectrum))
                final_dir = (self.file_dir).replace((self.varla1).get(),name_spectrum)
                fits_s.writeto(final_dir)  
                text_1 = (u"File created: %s\n"%(name_spectrum))
                (self.box_entry).configure(state='normal')
                (self.box_entry).insert(INSERT, text_1)
                (self.box_entry).see(END)
                (self.box_entry).configure(state='disabled')
            except Exception as e:
                print(e)
        '''The function extracts the information from the spaxels within the drawn circle 
        with center on cir_x and cir_y, return the new cube for the new file fits

        '''
        def circle_fits():
            v = np.amax((self.integrated_x))-np.amin((self.integrated_x))
            v = v+1
            v2 = np.amax((self.integrated_y))-np.amin((self.integrated_y))
            v2 = v2+1
            new_data = np.zeros([(self.pixels),v2,v])
            k = 0
            cd  = (self.header_file)['CDELT1']
            radius = (self.radius_).get()/cd
            if (self.cir_x) <= int (v/2):
                new_center_x = (self.cir_x)
            else:
                if (self.cir_x) >= (self.size_x)-radius:
                    new_center_x = (v-1) - ((self.size_x)-1-(self.cir_x))
                else:
                    new_center_x = int (v/2)
                    
            if (self.cir_y) <= int (v2/2):
                new_center_y = (self.cir_y)
            else:
                if (self.cir_y) >= (self.size_y) - radius:
                    new_center_y = (v2-1) - ((self.size_y)-1-(self.cir_y))
                else:
                    new_center_y = int (v2/2)
            for i in range(v):
                for j in range(v2):
                    d = get_distance(new_center_x,new_center_y,i,j)
                    if d <= radius:
                        new_data[:,j,i] = (self.data)[:,(self.integrated_y)[k],(self.integrated_x)[k]]
                        k = k+1
            return new_data     
        '''Create the  fits file fits with the spaxels definite on the function 
        circle_fits(), change the header of the original fits in the next fields:
        NAXSIS1,NAXIS2,CRPIX1 y CRPIX2
        '''
        def create_circle_fits():
            try:
                new_data = circle_fits()
                name_circle = (self.varla1).get()
                name_circle = name_circle.split('.')
                name_circle = name_circle[0]+'.cirle.rscube_'+str((self.cir_x))+'_'+str((self.cir_y))+'.fits'
                final_dir = (self.file_dir).replace((self.varla1).get(),name_circle) 
                v = np.amax((self.integrated_x))-np.amin((self.integrated_x))
                v = v+1
                v2 = np.amax((self.integrated_y))-np.amin((self.integrated_y))
                v2 = v2+1
                (self.header_file)['NAXIS1'] = v2
                (self.header_file)['NAXIS2'] = v
                (self.header_file)['CRPIX1'] = int(v2/2)
                (self.header_file)['CRPIX2'] = int(v/2)
                fits.writeto(final_dir,data=new_data,header=(self.header_file))
                text_1 = (u"File created: %s\n"%(name_circle))
                (self.box_entry).configure(state='normal')
                (self.box_entry).insert(INSERT, text_1)
                (self.box_entry).see(END)
                (self.box_entry).configure(state='disabled')
            except Exception as e:
                print(e)
        '''
        function to reset integrated region, clean the circle drew and the information
        of the integrated spectrum, for draw a new circle
        '''
        def reset_integrated_region():
            if (self.flag_file) == 1:
                if (self.flag_integrate_region2) == 1 and (self.flag_integrate_region) == 1:
                    (self.flag_integrate_region2) = 0
                    (self.flag_integrate_region) = 0
                    text_1 = (u"\nCircle erased\n")
                    (self.box_entry).configure(state='normal')
                    (self.box_entry).insert(INSERT, text_1)
                    (self.box_entry).see(END)
                    (self.box_entry).configure(state='disabled')   
                    (self.varla10).set("Explorer OFF")
                    (self.integrated_x) = []
                    (self.integrated_y) = []
                    filters_((self.name_f))
                    (self.radius_).set(0)
                    (self.entry_Radius).config(state=NORMAL)
                    (self.flag_create_fits) = 0
            else:
                MessageBox.showerror("Error!","Please, select a file") 
       
            
            
        '''
        function to exit of the graphic interface
        '''
        def button_quit_destroy():
            (self.window).destroy()
        
        '''
        function that is called when the user press the button of "browse",
        display a window that permit select a file to open with the program 
        the program determinate if the file is valid, able all buttons, entrys,
        and show the information about the FITS file
        '''
        def new_file():
            try:
                if (self.flag_file) == 1:
                    (self.hi_data).close()
                
                py_exts = r"*.fits  *.fits.gz *.fits.rar" 
                folder_selected = filedialog.askopenfile(mode="r")#, filetypes = ("all files","*.*"))#,("fits files",".fits .fits.gz")))
                (self.file_dir) = os.path.abspath(folder_selected.name)
                name=folder_selected.name
                nombre2=name.split('/')
                n=nombre2[len(nombre2)-1]
                (self.hi_data) = fits.open((self.file_dir))
                (self.varla1).set(n)
                (self.name) = n
                (self.data) = (self.hi_data)[0].data
                
                (self.min_value_da)=np.amin((self.data))
                (self.max_value_da)=np.amax((self.data))
                (self.hi_data).info()
                (self.header_file) = (self.hi_data)[0].header
                
                (self.band_sticks).set(0)
                (self.integrated_x) = []
                (self.integrated_y) = []
                if (self.flag_file) == 1:
                    (self.box_entry).configure(state='normal')
                    (self.box_entry).delete("1.0","end")
                    (self.box_entry).configure(state='disabled')  
                    
                text_1 = (u" \nIFS Explorer 3D cube spectra viewer\n" 
                              u"Move mouse over the mosaic to plot the spectra \n"
                              u"Click for ON/OFF the explorer  \n")
                (self.box_entry).configure(state='normal')
                (self.box_entry).insert(INSERT, text_1)
                (self.box_entry).see(END)
                (self.box_entry).configure(state='disabled')
                (self.flag_file)=1
                if (self.flag_file) == 1:
                    try:
                        crval  = (self.header_file)['CRVAL3']
                        cdelt  = (self.header_file)['CDELT3']
                        crpix  = (self.header_file)['CRPIX3']
                        (self.size_x)  = (self.header_file)['NAXIS1']
                        (self.size_y)  = (self.header_file)['NAXIS2']
                        (self.pixels) = (self.header_file)['NAXIS3']
                        text_1 = (u"The dimensions of the cube are: %d x %d x %d \n"%((self.size_x),(self.size_y),(self.pixels)) )
                        (self.box_entry).configure(state='normal')
                        (self.box_entry).insert(INSERT, text_1)
                        (self.box_entry).see(END)
                        (self.box_entry).configure(state='disabled')
                            
                            
                        create_label_offset()        
                        (self.wcs_header) = WCS((self.header_file))
                        Dec = 0
                        RA = 0
                        try:
                            Dec = (self.header_file)['CRVAL2']
                            RA = (self.header_file)['CRVAL1']
                        except KeyError as e:
                            (self.box_entry).configure(state='normal')
                            text_1 = (u"Warning: No WCS founder in header. \n")
                            (self.box_entry).insert(INSERT, text_1)
                            (self.box_entry).see(END)
                            (self.box_entry).configure(state='disabled')
                            
                        if RA <= 0: 
                            (self.wcs) = 0 
                            (self.varla7).set("     Spaxel        ID           ")
                        else: 
                            (self.wcs) = 1
                            (self.varla7).set("      Spaxel             ID                        RA                                    DEC                      RA-deg                DEC-deg")
                        try:
                            (self.varla9).set("Object: %s"%((self.header_file)['OBJECT']))
                        except Exception as e:  
                            try:
                                (self.varla9).set("Object: %s"%((self.header_file)['OBJNAME']))
                            except Exception as e: 
                                (self.varla9).set("Object:  %s "%((self.name)))  
                        (self.arrlambda) = np.zeros((self.pixels)) 
                        if cdelt == 0:
                            cdelt = 1
                            text_1 = (u"CDELT entry not found, using CDELT=1 \n" )
                            (self.box_entry).configure(state='normal')
                            (self.box_entry).insert(INSERT, text_1)
                            (self.box_entry).see(END)
                            (self.box_entry).configure(state='disabled')
                        for x in range((self.pixels)):
                            (self.arrlambda)[x] = (crval + x*cdelt)-(crpix-1)*cdelt
                        promedio = np.mean((self.arrlambda))
                        if promedio < 100:
                            (self.arrlambda) = (self.arrlambda)*10000
                        
                   #     if flag_file==1:
                    #        (self.ax1).cla()  
                        (self.Integrated_spectrum) = np.zeros((self.pixels))       
                   #     flag_file=1
                        (self.f2).clf()
                        (self.ax1) = (self.f2).add_subplot(projection=(self.wcs_header), slices=('x', 'y', 2))
                        (self.dband)=np.zeros((self.size_x)*(self.size_y))
                        (self.image_final) = np.zeros(((self.size_y),(self.size_x)))
                        (self.array_data)=np.reshape((self.data),((self.pixels),(self.size_x)*(self.size_y)))
                        (self.min_value_la)=np.amin((self.arrlambda))
                        (self.max_value_la)=np.amax((self.arrlambda))
                        (self.bar_) = Scale(lblframe_info, orient = HORIZONTAL, showvalue= 0, from_=(self.min_value_la)+1, to=(self.max_value_la)-1, sliderlength = 30,command = set_bar )
                        (self.bar_).pack()
                        (self.bar_).place_configure(x=150, y=60, width= 560)
                        (self.bar_).config(bg=color)
                   #     bar_ = Scale(frame3, orient = HORIZONTAL, showvalue= 0, from_=(self.min_value_la)+1, to=(self.max_value_la)-1, sliderlength = 30, length=480, command = set_bar)
                    #    bar_.grid(row=2,column=2,sticky="nsew",pady=3,padx=5)
                        (self.flag_wave) = 0
                        (self.flag_flux) = 0
                        (self.flag_band) = 0
                        (self.flag_explorer)=0
                        (self.flag_integrate_region)=0
                        (self.flag_integrate_region2)=0
                        (self.flag_create_fits) = 0
                        (self.radius_).set(0)
                        (self.varla10).set("Explorer OFF")
                        (self.sp1).set(0)
                        (self.red_marks) = []
                        (self.band) = 0
                        (self.combo1).current(0)
                        (self.combo2).current(0)
                        update_graph()     
                        (self.var).set(1)
                        (self.var3).set("")   
                        (self.varla5).set(int(self.min_value_la))
                        (self.varla6).set(int(self.max_value_la))
                        (self.varla3).set(0)
                        (self.varla4).set(0)
                        (self.name_f) = "Halpha-KPN0 6547-80A.txt"
                        filters_(self.name_f)
                        (self.ax0).set_xlim(xmin=(self.min_value_la),xmax=(self.max_value_la))
                        coordinates_(int((self.size_x)/2),int((self.size_y)/2))
                        (self.entry_Radius).config(state=NORMAL)
                        (self.entry_shFilt).config(state=NORMAL)
                        (self.entry_MWave).config(state=NORMAL)
                        (self.entry_shFiltmin).config(state=NORMAL)
                        (self.entry_shFiltmax).config(state=NORMAL)
                        (self.entry_wvlenMin).config(state=NORMAL)
                        (self.entry_wvlenMax).config(state=NORMAL)
                        
                        
                    except Exception as e:
                           print(e)
                           MessageBox.showerror("Error!","The selected object is not a cube FITS") 
                           button_quit()
                else:
                    print(e)
                    MessageBox.showerror("Error!","Please, select a file")
            except Exception as e:  
                print(e)
                MessageBox.showerror("Error!","Please, select a file valid")
                if self.flag_file == 0:
                    (self.varla1).set("")
                #aqui borrar nombre
            
        '''Function of transition necesarry to initialize the graph of the spectrum, that 
        after is updated
        '''
        def update_graph():
            (self.ax0).cla()
            (self.ax0).set_xlabel( 'Wavelength' )
            (self.ax0).set_ylabel( 'Flux' )
            (self.spectrum)=(self.data)[:,int((self.size_x)/2),int((self.size_y)/2)]
            (self.spectrum)=np.nan_to_num((self.spectrum))   
            for i in range(0,(self.pixels)):
                if (abs((self.spectrum)[i])>1e30):
                    (self.spectrum)[i]=0
            (self.ax0).plot((self.arrlambda),(self.spectrum),color='blue')
            (self.canvas).draw()
        '''
        Function that control the image show of the fits file, 
        apply a filter to the image to do better the visualization, 
        and plot graph of the data of the filter.
        When a filter is not available fot the actual fits file, set to the 
        V-Johnson filter
        '''
        def filters_(name_1):
            lineas = []
            cwl = 0
            filePath = __file__
            if self.flag_system == 0:
                filter_dir=filePath.replace('prueba_ifsUW.py', 'Filters\\')
            else:
                filter_dir=filePath.replace('prueba_ifsUW.py', 'Filters/')
            nuev_=filter_dir+name_1
            if os.path.isfile(nuev_):
                archivo = open(nuev_, 'r')
                for linea in archivo.readlines():
                    if linea.startswith("# CWL:")==True:
                        cwl = float(linea[7:len(linea)-1])
                    if linea.startswith("#")==False and linea.isalnum()==False and linea!= '':
                        linea = linea.rstrip('\r\n')
                        lineas.append(linea)
                lineas = list(filter(bool,lineas))
                arr_w = np.zeros(len(lineas))
                arr_f =  np.zeros(len(lineas))
                j= 0
                for i in lineas:
                    primeralinea=i.split()
                    arr_w[j] = primeralinea[0]
                    arr_f[j] = primeralinea[1]
                    j = j+1
                if (arr_w[0] < (self.min_value_la) and arr_w[j-1] < (self.min_value_la)) or ((self.max_value_la) < arr_w[0] and (self.max_value_la) < arr_w[j-1]):
                    text_1 = (u"WARNING: Using a V-band filter within the data wavelength \n limits: %d - %d \n "%((self.min_value_la),(self.max_value_la)))
                    (self.box_entry).configure(state='normal')
                    (self.box_entry).insert(INSERT, text_1)
                    (self.box_entry).see(END)
                    (self.box_entry).configure(state='disabled')
                    archivo.close()
                    lineas = []
                    (self.name_f) = "V-Johnson.txt"
                    nuev_=filter_dir+"V-Johnson.txt"
                    (self.combo2).current(3)
                    archivo = open(nuev_, 'r')
                    for linea in archivo.readlines():
                        if linea.startswith("# CWL:")==True:
                            cwl = float(linea[7:len(linea)-1])
                        if linea.startswith("#")==False and linea.isalnum()==False and linea!= '':
                            linea = linea.rstrip('\r\n')
                            lineas.append(linea)
                    
                    lineas = list(filter(bool,lineas))
                    arr_w = np.zeros(len(lineas))
                    arr_f =  np.zeros(len(lineas))
                    j= 0
                    for i in lineas:
                        primeralinea=i.split()
                        arr_w[j] = primeralinea[0]
                        arr_f[j] = primeralinea[1]
                        j = j+1
                    ##-hasta aqui
                    if (self.flag_band) == 0:
                        (self.band)= np.mean((self.arrlambda))  
                        (self.varla11).set((self.band))
                        (self.bar_).set((self.band))
                   
                
                else:
                   if (self.flag_band)==0:
                       (self.band)=cwl
                       (self.varla11).set((self.band))
                       (self.bar_).set((self.band))
                       
                shift = cwl/(self.band)
                new1 = (arr_w)/shift
                (self.res)=interpolate.InterpolatedUnivariateSpline(new1,arr_f)(self.arrlambda)
                posiciones = []
                posiciones2 = []
                for i in range(len((self.arrlambda))):
                    if (self.arrlambda)[i] <= np.amin(new1) or (self.arrlambda)[i] >= np.amax(new1):
                        posiciones2.append(i)
                    if (self.arrlambda)[i] >= np.amin(new1) and (self.arrlambda)[i] <= np.amax(new1):
                        posiciones.append(i)
                (self.res)[posiciones2]=0
                convolve = (self.res)[posiciones]
                for i in range(len((self.dband))):
                    (self.dband)[i] = sum(convolve*(self.array_data)[posiciones,i])
                (self.image_final)=np.reshape((self.dband),((self.size_y),(self.size_x)))
                (self.ax0).clear()
                if (self.flag_integrate_region) == 1 and (self.flag_integrate_region2) == 1:
                    if (self.flag_flux)==1:
                        (self.ax0).set_ylim(ymin=(self.varla3).get(),ymax=(self.varla4).get())
                        (self.ax0).plot((self.arrlambda),(self.res)*(self.varla4).get(),'--',color = 'orange')
                        for i in (self.red_marks):
                                (self.ax0).axvline(int(i),(self.varla3).get(),(self.varla4).get(),color='red')
                    else:
                     #   (self.ax0).plot((self.arrlambda),(self.res)*np.amax((self.Integrated_spectrum))*1.2,'--',color = 'orange')
                        (self.ax0).set_ylim(ymin=np.amin((self.Integrated_spectrum)),ymax=np.amax((self.Integrated_spectrum))*1.2)
                        for i in (self.red_marks):
                                (self.ax0).axvline(int(i),(self.min_value_da),(self.max_value_da),color='red')
                    
                    (self.ax0).plot((self.arrlambda),(self.Integrated_spectrum),color='red')
                    if (self.flag_wave) == 1:
                            (self.ax0).set_xlim(xmin=(self.varla5).get(),xmax=(self.varla6).get())
                    else:
                            (self.ax0).set_xlim(xmin=(self.min_value_la),xmax=(self.max_value_la))
                   
                else:
                    if (self.flag_flux)==1:
                        (self.ax0).set_ylim(ymin=(self.varla3).get(),ymax=(self.varla4).get())
                        (self.ax0).plot((self.arrlambda),(self.res)*(self.varla4).get(),'--',color = 'orange')
                        for i in (self.red_marks):
                                (self.ax0).axvline(int(i),(self.varla3).get(),(self.varla4).get(),color='red')
                    else:
                        (self.ax0).plot((self.arrlambda),(self.res)*np.amax((self.spectrum))*1.2,'--',color = 'orange')
                        (self.ax0).set_ylim(ymin=np.amin((self.spectrum)),ymax=np.amax((self.spectrum))*1.2)
                        for i in (self.red_marks):
                                (self.ax0).axvline(int(i),(self.min_value_da),(self.max_value_da),color='red')
                    
                    (self.ax0).plot((self.arrlambda),(self.spectrum),color='blue')
                    if (self.flag_wave) == 1:
                            (self.ax0).set_xlim(xmin=(self.varla5).get(),xmax=(self.varla6).get())
                    else:
                            (self.ax0).set_xlim(xmin=(self.min_value_la),xmax=(self.max_value_la))
                            
                nomb_a = (self.name_f).split(".")
                text_1 = (u"\nFilter used %s with band %d \n"%(nomb_a[0],(self.band)))
                (self.box_entry).configure(state='normal')
                (self.box_entry).insert(INSERT, text_1)
                (self.box_entry).see(END)
                (self.box_entry).configure(state='disabled')    
                (self.canvas).draw()
                archivo.close()
                set_scaling()
        
                
            else:
                MessageBox.showerror("Error!","Not exists the folder of filters") 
        
        
        '''
        function to show the information about a spaxel, coordinate in the x and y axis,
        the coordinates in RA and DEC and in degrees.
        Is called when the user moves the mousse in the area of the image 
        
        '''
        def coordinates_(cord_x,cord_y):
            ID = (cord_y*(self.size_x))+cord_x
            (self.ax0).cla()
            (self.ax0).set_xlabel( 'Wavelength' )
            (self.ax0).set_ylabel( 'Flux' )
            (self.spectrum)=(self.data)[:,cord_y,cord_x]
            (self.spectrum)=np.nan_to_num((self.spectrum)) 
            for i in range(0,(self.pixels)):
               if (abs((self.spectrum)[i])>1e30):
                   (self.spectrum)[i]=0
            (self.ax0).plot((self.arrlambda),(self.spectrum),color='blue')
            if (self.flag_wave) == 1:
               (self.ax0).set_xlim(xmin=(self.varla5).get(),xmax=(self.varla6).get())
            else:
               (self.ax0).set_xlim(xmin=(self.min_value_la),xmax=(self.max_value_la))
            if (self.flag_flux)==1:
               (self.ax0).set_ylim(ymin=(self.varla3).get(),ymax=(self.varla4).get())
               (self.ax0).plot((self.arrlambda),(self.res)*(self.varla4).get(),'--',color = 'orange')
               for i in (self.red_marks):
                   (self.ax0).axvline(int(i),(self.varla3).get(),(self.varla4).get(),color='red')
               
            else:
               (self.ax0).plot((self.arrlambda),(self.res)*np.amax((self.spectrum))*1.2,'--',color = 'orange')
               (self.ax0).set_ylim(ymin=np.amin((self.spectrum)),ymax=np.amax((self.spectrum))*1.2)
               for i in (self.red_marks):
                   (self.ax0).axvline(int(i),(self.min_value_da),(self.max_value_da),color='red')
            (self.canvas).draw()
            if (self.wcs) == 0:
               (self.varla8).set("   [ %d , %d ]       %d        "%(cord_x,cord_y,ID))
            else:
               try: 
                   celestial, spectral = (self.wcs_header).pixel_to_world([cord_x], [cord_y], [1])  
                   ra_1=celestial.ra.hms
                   c = str(celestial.dec)
                   c=c.replace("d"," d ")
                   c=c.replace("m"," m ")
                   c=c.replace("s"," s ")
                   c=c.replace("["," ")
                   c=c.replace("]"," ")
                   degr = str(celestial.to_string('decimal'))
                   degr = degr.replace(" ","              ")
                   degr = degr.replace("["," ")
                   degr = degr.replace("]"," ")
                   degr = degr.replace("'"," ")
                   (self.varla8).set("   [ %d , %d ]       %d        %d h  %d m  %f s     %s     %s "%(cord_x,cord_y,ID,ra_1[0],ra_1[1],ra_1[2],c,degr))
                 #  print("   [ %d , %d ]       %d        %d h  %d m  %f s     %s     %s "%(cord_x,cord_y,ID,ra_1[0],ra_1[1],ra_1[2],c,degr))
               except Exception as e:
                   celestial = (self.wcs_header).pixel_to_world([cord_x], [cord_y], [1])    
                   coo = SkyCoord(ra=celestial[0], dec=celestial[1],unit="deg")
                   ra_1=coo.ra.hms
                   c = str(coo.dec)
                   c=c.replace("d"," d ")
                   c=c.replace("m"," m ")
                   c=c.replace("s"," s ")
                   c=c.replace("["," ")
                   c=c.replace("]"," ")
                   completa= "   [ %d , %d ]       %d        %d h  %d m  %f s   %s  "%(cord_x,cord_y,ID,ra_1[0],ra_1[1],ra_1[2],c)
                   completa_1 = completa+str(celestial[0])+str(celestial[1])
                   completa_1 = completa_1.replace("deg"," ")
                   completa_1 = completa_1.replace("["," ")
                   completa_1 = completa_1.replace("]"," ")
                   (self.varla8).set(completa_1)
                   
        '''function to set the axis in the image to display coordinates (wcs) or 
        offset
        '''
            
        def set_offsets():
            if (self.flag_file)==1:
                if (self.band_sticks).get() == 1:
                 #   (self.band_sticks) = 1
                    (self.f2).clf()
                    (self.ax1) = (self.f2).add_axes( (0.05, .15, .90, .80), frameon=False)
                    filters_((self.name_f))
                else:
                    (self.f2).clf()
                    (self.ax1) = (self.f2).add_subplot(projection=(self.wcs_header), slices=('x', 'y', 2))
                    filters_((self.name_f))
            else:
                MessageBox.showerror("Error!","Please, select a file")
                (self.band_sticks).set(0)
        
        '''function that allows the user to select a spaxel that will be taken as the center 
        of the circle to integrate the spectrum
        '''
        def integrated_region():
            if (self.flag_file) == 1:
                if (self.flag_integrate_region) == 1 or (self.flag_integrate_region2) ==1:
                    MessageBox.showerror("Error!","Please, first reset integrate region") 
                else:
                    (self.flag_integrate_region) = 1
                    (self.entry_Radius).config(state=DISABLED)
                    if (self.flag_explorer) == 0:
                        (self.flag_explorer) = 1
                    (self.varla10).set("Select a spaxel")
            else:
                MessageBox.showerror("Error!","Please, select a file") 
        '''function that is called when the user select the spaxel to take like the center of the cirle
        Draw the circle in the image, calls to the function for get the
        spaxels inside the circle and show the spectrum integrated in the graph
        '''
        def draw_circle(cord_x,cord_y):
            try:
                if int((self.radius_).get()) <= 0 or int((self.radius_).get()) >=(self.size_x)/2:
                    MessageBox.showwarning("Warning!","Please, enter a radius positive and logic")
                    (self.flag_integrate_region) = 0
                    (self.flag_integrate_region2) = 0
                    (self.integrated_x) = []
                    (self.integrated_y) = []
                    (self.radius_).set(0)
                    (self.flag_explorer) = 0
                    (self.varla10).set("Explorer OFF")
                    (self.entry_Radius).config(state=NORMAL)
                    
                else:
                     cd = (self.header_file)['CDELT1']
                     if cd > 1:
                         new_r = (self.radius_).get()/cd
                     else:
                         new_r = int(round((self.radius_).get()/cd))
                     cir = patches.Circle((cord_x,cord_y),
                              int(new_r),
                              edgecolor='red',
                              fill = False)
                     (self.ax1).add_patch(cir)
                     (self.canvas2).draw()
                     
                     (self.cir_x)=cord_x
                     (self.cir_y)=cord_y
                     (self.flag_explorer) = 0
                     arr_x,arr_y=get_coor(cord_x,cord_y,(self.radius_).get()/cd)
                     get_integrated_spectrum(arr_x,arr_y)
                     (self.varla10).set("Show integrated flux")
                     text_1 = (u"\nDrawing circle with center %d,%d \nAnd radius of %d\n"%(cord_x,cord_y,(self.radius_).get()))
                     (self.integrated_x) = arr_x
                     (self.integrated_y) = arr_y
                     (self.box_entry).configure(state='normal')
                     (self.box_entry).insert(INSERT, text_1)
                     (self.box_entry).see(END)
                     (self.box_entry).configure(state='disabled')     
                     (self.flag_integrate_region2) = 1       
                     (self.flag_flux) = 0
                     (self.flag_wave) = 0
                     (self.varla5).set(int(self.min_value_la))
                     (self.varla6).set(int(self.max_value_la))
                     filters_((self.name_f))
            except Exception as e: 
                   print(e)
                   MessageBox.showerror("Error!","Please, enter numbers")  
                   (self.flag_integrate_region) = 0
                   (self.flag_integrate_region2) = 0
                   (self.radius_).set(0)
       
        '''function to determine  the spaxels that are inside the circle drew and return 
        the spaxels in two array, x and y 
       '''
        def get_coor(x,y,radius):
            pix_x = []
            pix_y = []   
            for i in range((self.size_x)):
                for j in range((self.size_y)):
                    d = get_distance(x,y,i,j)
                    if d <= radius:
                        pix_x.append(i)
                        pix_y.append(j)   
            return pix_x,pix_y
        '''function to sum the spectrum of every spaxel inside the circle
        and return the integrates spectrum
        '''
        def get_integrated_spectrum(pix_x,pix_y):
            (self.Integrated_spectrum) = np.zeros((self.pixels))   
            for j in range(len(pix_x)):
                if 0<=pix_y[j]<(self.size_y) and 0<=pix_x[j]<(self.size_x):
                    esp=(self.data)[:,pix_y[j],pix_x[j]]
                    esp=np.nan_to_num(esp)   
                    for i in range(0,(self.pixels)):
                        if (abs(esp[i])>1e30):
                            esp[i]=0
                    (self.Integrated_spectrum) = (self.Integrated_spectrum) + esp
        '''function to determine  the distance between to points
        '''
        def get_distance(x1,y1,x2,y2):
            d = ((x2-x1)**2)+((y2-y1)**2)
            d = np.sqrt(d)
            return d
        '''function to clear the graph and image fits, disabled entrys and buttons,
        is used when a error ocurred in selecction of the file
        '''
        
        def button_quit():
            if (self.flag_file) == 1:
                (self.hi_data).close()
                (self.flag_file)=0
                (self.ax0).cla()
                (self.f2).clf()
                (self.canvas).draw()
                (self.canvas2).draw()
                (self.var).set(1)
                (self.varla8).set("")
                (self.varla10).set("")
                (self.varla9).set("")
                (self.varla7).set("")
                (self.varla5).set(0)
                (self.varla6).set(0)
                (self.varlaflux).set("")
                (self.varlawave).set("")
                (self.radius_).set(0)
                (self.combo2).current(0)
                (self.combo1).current(0)
                (self.var3).set("")
                (self.varla11).set(0)
                (self.varla1).set("")
                (self.box_entry).configure(state='normal')
                (self.box_entry).delete("1.0","end")
                (self.box_entry).configure(state='disabled')
                (self.entry_Radius).config(state=DISABLED)
                (self.entry_shFilt).config(state=DISABLED)
                (self.entry_MWave).config(state=DISABLED)
                (self.entry_shFiltmin).config(state=NORMAL)
                (self.entry_shFiltmax).config(state=NORMAL)
                (self.entry_wvlenMin).config(state=NORMAL)
                (self.entry_wvlenMax).config(state=NORMAL)
        
        
            else:
                MessageBox.showerror("Error!","Please, select a file") 
            
        
        get_cmaps()
        color = "#E6E6FA"
        filePath = __file__
        operative_system()
        if self.flag_system == 0:
            filePath=filePath.replace('prueba_ifsUW.py', 'Img\\logoIFSexplorer.ico')
            (self.window).iconbitmap(filePath)
        (self.window).config(bg=color) 
        if self.flag_system == 0:
            filePath=filePath.replace('.ico', '.png')
        else:
            filePath = __file__
            filePath=filePath.replace('prueba_ifsUW.py', 'Img/logoIFSexplorer.png')
        image=Image.open(filePath)
        img = image.resize((150,150))
        photo = ImageTk.PhotoImage(img) 
        label = Label((self.window), image = photo) 
        label.pack()
        label.place_configure(x=15,y=30,width=150,height=150) 
    
        #----  Widget Abrir Fits -----------------------------
        lblframe_widget = LabelFrame((self.window), text = "")
        lblframe_widget.pack ()
        lblframe_widget.place_configure(x=170, y=5, height= 205, width=510)
        lblframe_widget.config(bg=color)
        
        #---------- Label Fits --------------
        lbl_Fits = Label (lblframe_widget, text = "FITS")
        lbl_Fits.pack ()
        lbl_Fits.place_configure(x=4, y= 5)
        lbl_Fits.config(bg=color)
        
        #----------- Objecto Fits  -----------------
        entry_fits =Entry (lblframe_widget,state=DISABLED,textvariable=(self.varla1))
        entry_fits.insert (0, "")
        entry_fits.pack ()
        entry_fits.place_configure(x=40, y=5, height= 25, width=295)
        
        #------- Boton Browse  ---------------
        button_browse = Button (lblframe_widget,text = "Browse", command= new_file)
        button_browse.pack ()
        button_browse.place_configure(x=350, y=5, height= 25, width=65)
            
        #------- Boton Quit  ---------------
        button_quit_i = Button (lblframe_widget,text = "Quit", command= button_quit_destroy)
        button_quit_i.pack ()
        button_quit_i.place_configure(x=430, y=5, height= 25, width=60)
        
        #------- Frame descripcion del Objeto ---------------

        #----------- Entry Objecto Fits  -----------------
        entry_obj =Entry (lblframe_widget,state=DISABLED, textvariable=(self.varla9))
        entry_obj.insert (0, "")
        entry_obj.pack ()
        entry_obj.place_configure(x=5, y=35, height= 24, width=490)
        
        #----------- Entry Objecto Fits  -----------------
        entry_intFlux =Entry (lblframe_widget,state=DISABLED, textvariable=(self.varla10))
        entry_intFlux.insert (0, "")
        entry_intFlux.pack ()
        entry_intFlux.place_configure(x=5, y=60, height= 24, width=490)
        
        
        
        #------- Entrada de Descripcion del Objeto ----------
        (self.box_entry) = scrolledtext.ScrolledText(lblframe_widget)
        (self.box_entry).configure(state='disabled',yscrollcommand=TRUE)
        (self.box_entry).pack ()
        (self.box_entry).place_configure(x=5, y=90, width=490,height=100)
        
        
            #--------  Integrate Region ----------------------------------------------------
        lblfr_WIntg= LabelFrame((self.window), text = "")
        lblfr_WIntg.pack ()
        lblfr_WIntg.place_configure(x=690, y=5, height= 230, width=140)
        lblfr_WIntg.config(bg=color)
        
        #-------- Boton Radius ----------------
        btn_Radius = Button(lblfr_WIntg, text="Integrated Region",command=integrated_region)
        btn_Radius.pack()
        btn_Radius.place_configure(x=8, y=5, height= 25, width=120)
        
        #-------- Label Radius ----------------
        lbl_Radius = Label (lblfr_WIntg, text = "Radius")
        lbl_Radius.pack ()
        lbl_Radius.place_configure(x=25, y= 32)
        lbl_Radius.config(bg=color)
        
        #-------- Entry Radius ----------------
        (self.entry_Radius) = Entry(lblfr_WIntg,textvariable=(self.radius_))
        (self.entry_Radius).pack()
        (self.entry_Radius).place_configure(x=10, y=54, height= 20, width=50)
        (self.entry_Radius).config(state=DISABLED)
        
        
         #-------- Boton Radius ----------------
        btn_Radius = Button(lblfr_WIntg, text="Reset",command=reset_integrated_region)
        btn_Radius.pack()
        btn_Radius.place_configure(x=70, y=54, height= 20, width=50)
        #-------- Created Files ----------------
        btn_Radius = Button(lblfr_WIntg, text="Create Files",command=create_files)
        btn_Radius.pack()
        btn_Radius.place_configure(x=30, y=85, height= 20, width=80)
        
        #-------- Display Axes ---------------
        lblfr_DisAx= LabelFrame((self.window), text = "Display axis")
        lblfr_DisAx.pack()
        lblfr_DisAx.place_configure(x=690, y=120, height= 110, width=140)
        lblfr_DisAx.config(bg=color)
        
        rb1= Radiobutton(lblfr_DisAx, text="RA-Dec", variable=(self.band_sticks), value=0, command=set_offsets)
        rb2= Radiobutton(lblfr_DisAx, text="Offset", variable=(self.band_sticks), value=1, command=set_offsets)
        
        rb1.pack()
        rb2.pack()
        
        rb1.place_configure(x=30, y=4)
        rb2.place_configure(x=30, y=24)
        
        rb1.config(bg=color)
        rb2.config(bg=color)
        
        
        #-------- Mark Wavelenght ---------------
        lblfr_MWave= LabelFrame((self.window), text = "Mark Wavelenght")
        lblfr_MWave.pack()
        lblfr_MWave.place_configure(x=690, y=185, height= 80, width=140)
        lblfr_MWave.config(bg=color)
        
        #-------- Entry Mark Wavelenght  ----------------- 
        (self.entry_MWave) = Entry (lblfr_MWave,textvariable=(self.var3))
        (self.entry_MWave).insert (0, "")
        (self.entry_MWave).pack ()
        (self.entry_MWave).place_configure(x=15, y=8, height= 20, width=100)
        (self.entry_MWave).config(state=DISABLED)
        
        btn_set = Button (lblfr_MWave, text = "Set", command=mark_wavelength)
        btn_set.pack ()
        btn_set.place_configure(x=10, y=36, height= 20, width=50)
        
        btn_set = Button (lblfr_MWave, text = " Reset", command=reset_mark_wavelength)
        btn_set.pack ()
        btn_set.place_configure(x=80, y=36, height= 20, width=50)
        
        
         #--------- label frame Display --------
        lblfr_Display= LabelFrame((self.window), text = "Display")
        lblfr_Display.pack()
        lblfr_Display.place_configure(x=840, y=40, height= 160, width=210)
        lblfr_Display.config(bg=color)
        
        lbl_Clr = Label (lblfr_Display, text = "Color Map")
        lbl_Clr.pack ()
        lbl_Clr.place_configure(x=5, y =5)
        lbl_Clr.config(bg=color)
        
        (self.combo1) = ttk.Combobox(lblfr_Display,state="readonly",background=color) 
        (self.combo1)['values'] = ( 'Blue scaling', 
                                            'Red scaling',
                                            'Green scaling',
                                            'Grayscale',
                                            'PINGSoft special',
                                            'CALIFA-special',
                                            'Rainbow',
                                            'BGRY',
                                            'Prism',
                                            'Stern',
                                            'Std-Gamma')   
        (self.combo1).current(0)
        (self.combo1).bind("<<ComboboxSelected>>", set_color_map)
        (self.combo1).place_configure(x=5, y=30, width= 150, height=28)
     #   combo1.config(bg="#E6E6FA")
        
        
        lbl_filter = Label (lblfr_Display, text = "Filter")
        lbl_filter.pack ()
        lbl_filter.place_configure(x=5, y =60)
        lbl_filter.config(bg=color)
        (self.combo2) = ttk.Combobox(lblfr_Display,state="readonly",background="#E6E6FA") 
        (self.combo2)['values'] = ( 'Halpha-KPN0 6547-80A', 
                                            'HALPHA-CTI0 6586-20A',
                                            'B-Johnson (1965)',
                                            'V-Johnson',
                                            'u-SDSS-III',
                                            'g-SDSS-III',
                                            'r-SDSS-III',
                                            'i-SDSS-III',
                                            'B-Bessell (1990)',
                                            'V-Bessell',
                                            'R-Bessell',
                                            'B-KPN0-Harris',
                                            'V-KPN0-Harris',
                                            'R-KPN0-Harris')   
        (self.combo2).current(0)
        (self.combo2).bind("<<ComboboxSelected>>", set_filter)
        (self.combo2).place_configure(x=5, y=80, width= 195, height=28)
        
        checkbtn_InvColMap = Checkbutton(lblfr_Display, text="Invert color map",variable=(self.sp1), onvalue=1, offvalue=0, command=set_color_map)
        checkbtn_InvColMap.select()
        checkbtn_InvColMap.pack()
        checkbtn_InvColMap.place_configure(x=5,y=110)
        checkbtn_InvColMap.config(bg=color)
        
        #----------  label Frame Scalling  ----------------
        lblfr_Scal= LabelFrame((self.window), text = "Scaling")
        lblfr_Scal.pack()
        lblfr_Scal.place_configure(x=1065, y=40, height= 160, width=215)
        lblfr_Scal.config(bg=color)
        linear = Radiobutton(lblfr_Scal, text="Linear", variable=(self.var), value=1, command=set_scaling)
        clipping= Radiobutton(lblfr_Scal, text="2% Clipping", variable=(self.var), value=2, command=set_scaling)
        asinh= Radiobutton(lblfr_Scal, text="Asinh", variable=(self.var), value=3, command=set_scaling)
        powerl= Radiobutton(lblfr_Scal, text="Power-Law", variable=(self.var), value=4, command=set_scaling)
        sqRoot= Radiobutton(lblfr_Scal, text="Square Root", variable=(self.var), value=5, command=set_scaling)
        hEqual= Radiobutton(lblfr_Scal, text="Hist Equal", variable=(self.var), value=6, command=set_scaling)
        gaussian= Radiobutton(lblfr_Scal, text="Gaussian", variable=(self.var), value=7, command=set_scaling)
        logarithmic= Radiobutton(lblfr_Scal, text="Logarithmic", variable=(self.var), value=8, command=set_scaling)
        
        linear.pack()
        clipping.pack()
        asinh.pack()
        powerl.pack()
        sqRoot.pack()
        hEqual.pack()
        gaussian.pack()
        logarithmic.pack()
        
        linear.place_configure(x=5, y=20)
        clipping.place_configure(x=5, y=40)
        asinh.place_configure(x=5, y=60)
        powerl.place_configure(x=5, y=80)
        sqRoot.place_configure(x=100, y=20)
        hEqual.place_configure(x=100, y=40)
        gaussian.place_configure(x=100, y=60)
        logarithmic.place_configure(x=100, y=80)
        
        linear.config(bg=color)
        clipping.config(bg=color)
        asinh.config(bg=color)
        powerl.config(bg=color)
        sqRoot.config(bg=color)
        hEqual.config(bg=color)
        gaussian.config(bg=color)
        logarithmic.config(bg=color)
        
        opScal = Label(lblfr_Scal)
        opScal.pack()
        opScal.place_configure(x=5,  y= 100)
        opScal.config(bg=color)
        
        #--------- 
        lblframe_info = LabelFrame((self.window),text="")
        lblframe_info.pack()
        lblframe_info.place_configure(x=15, y=270, width=815, height=95)
        lblframe_info.config(bg=color)
        
        #--------------- Entry Informacion ------------------
        entry_wcs = Entry(lblframe_info, textvariable=(self.varla7),state=DISABLED)
        entry_wcs.insert(0, "")
        entry_wcs.pack()
        entry_wcs.place_configure(x=5, y= 5, width=795, height=20)
        
        entry_coord = Entry(lblframe_info,textvariable=(self.varla8),state=DISABLED)
        entry_coord.insert(0, "")
        entry_coord.pack()
        entry_coord.place_configure(x=5, y= 25, width=795, height=20)
        
        #-------------- Label Shift Filter ------------------
        lbl_shFilter = Label(lblframe_info, text="Shift Filter")
        lbl_shFilter.pack()
        lbl_shFilter.place_configure(x=5, y=60)
        lbl_shFilter.config(bg=color)
        
        #-------------- Entry Shift Filter ------------------
        (self.entry_shFilt) = Entry(lblframe_info,state=DISABLED, textvariable=(self.varla11))
        (self.entry_shFilt) .insert(0, "0.0")
        (self.entry_shFilt) .pack()
        (self.entry_shFilt) .place_configure(x=80, y=60, width=60, height=20)
        
        #-------------- Scale -----------------------
        (self.bar_) = Scale(lblframe_info, orient = HORIZONTAL, showvalue= 0, from_=(self.min_value_la)+1, to=(self.max_value_la)-1, sliderlength = 30,command = set_bar )
        (self.bar_).pack()
        (self.bar_).place_configure(x=150, y=60, width= 560)
        (self.bar_).config(bg=color)
        
        #------------ Boton Apply ----------------
        btn_apply = Button(lblframe_info, text="Apply", command=set_band)
        btn_apply.pack()
        btn_apply.place_configure(x=730, y=60, width=60, height=25)
        
        #------------ label frame Flux range ------------------------------------------
        lblframe_flR = LabelFrame((self.window),text="")
        lblframe_flR.pack()
        lblframe_flR.place_configure(x=15, y=215, width=322, height=50)
        lblframe_flR.config(bg=color)
        
        #------------ label Flux range -----------------
        lbl_fluxR = Label(lblframe_flR, text="Flux\n range")
        lbl_fluxR.pack()
        lbl_fluxR.place_configure(x=8, y=5)
        lbl_fluxR.config(bg=color)
        
        
         #------------ label espacio -----------------
        lbl_espaciofr = Label(lblframe_flR, text=" __ ")
        lbl_espaciofr.pack()
        lbl_espaciofr.place_configure(x=115, y=5)
        lbl_espaciofr.config(bg=color)
    
        #------------ Entry Flux Range Minimo -----------------
        (self.entry_shFiltmin) = Entry(lblframe_flR,textvariable=(self.varla3))
        (self.entry_shFiltmin) .config(state=DISABLED)
        (self.entry_shFiltmin) .pack()
        (self.entry_shFiltmin) .place_configure(x=60, y=10, width=50, height=20)
      
        #------------ Entry Flux Range Maximo  -----------------
        (self.entry_shFiltmax) = Entry(lblframe_flR,textvariable=(self.varla4))
        (self.entry_shFiltmax).config(state=DISABLED)
        (self.entry_shFiltmax) .pack()
        (self.entry_shFiltmax).place_configure(x=140, y=10, width=50, height=20)
        
        
        #------------ Boton set de Flux Range ------------ 
        btn_setFR = Button(lblframe_flR, text="Set",command=set_flux_range)
        btn_setFR.pack()
        btn_setFR.place_configure(x=200, y=10, width=50, height=25)
        
        #------------ Boton reset de Flux Range ------------ 
        btn_resetFR = Button(lblframe_flR, text="Reset",command=reset_flux_range)
        btn_resetFR.pack()
        btn_resetFR.place_configure(x=260, y=10, width=50, height=25)
        
        #--------------------------------------------------------------------------------
         #------------ label frame Wavelenght --------------------------------------------
        lblframe_wave = LabelFrame((self.window),text="")
        lblframe_wave.pack()
        lblframe_wave.place_configure(x=345, y=215, width=335, height=50)
        lblframe_wave.config(bg=color)
        
        #-------------- label Wavelenght range -------------
        lbl_wavelen = Label(lblframe_wave , text="Wavelenght\nrange")
        lbl_wavelen.pack()
        lbl_wavelen.place_configure(x=2, y=5)
        lbl_wavelen.config(bg=color)
        
        
         #------------ Entry Wavelenght range Minimo -----------------
        (self.entry_wvlenMin) = Entry(lblframe_wave, textvariable=(self.varla5))
        (self.entry_wvlenMin) .config(state=DISABLED)
        (self.entry_wvlenMin) .pack()
        (self.entry_wvlenMin) .place_configure(x=84, y=10, width=50, height=20)
    
        #-------------- label / -------------
        lbl_barra = Label(lblframe_wave , text="__")
        lbl_barra.pack()
        lbl_barra.place_configure(x=138, y=5)
        lbl_barra.config(bg=color)
        
        #------------ Entry Wavelenght range  -----------------
        (self.entry_wvlenMax) = Entry(lblframe_wave,textvariable=(self.varla6))
        (self.entry_wvlenMax) .pack()
        (self.entry_wvlenMax) .place_configure(x=160, y=10, width=50, height=20)
        (self.entry_wvlenMax).config(state=DISABLED)
        
        
        
        #------------ Boton set de Wavelenght range ------------ 
        btn_setWl = Button(lblframe_wave, text="Set",command=set_wavelength_range)
        btn_setWl.pack()
        btn_setWl.place_configure(x=224, y=10, width=40, height=25)
        
        #------------ Boton reset de Wavelenght range ------------ 
        btn_resetWl = Button(lblframe_wave, text="Reset",command= reset_wavelength_range)
        btn_resetWl.pack()
        btn_resetWl.place_configure(x=274, y=10, width=50, height=25)
        
        
        f = Figure( figsize=(10.3, 3.7), dpi=80 )
        (self.ax0) = f.add_axes( (0.088, .15, .90, .80), frameon=False)
        
        (self.canvas) = FigureCanvasTkAgg(f, master=(self.window))
        (self.canvas).get_tk_widget().pack()
        (self.canvas).get_tk_widget().place_configure(x=15, y=370, width=815, height=310)
        (self.canvas).draw()
        toolbar = NavigationToolbar2Tk((self.canvas),(self.window) )
        toolbar.pack()
        toolbar.place_configure(x=15, y=680)#, width=715, height=300)
        
        (self.f2) = Figure( figsize=(6.9, 4.8), dpi=80 )
        saved_image = 0 
        (self.canvas2) = FigureCanvasTkAgg((self.f2), master=(self.window))
        (self.canvas2).get_tk_widget().pack() #455
        (self.canvas2).get_tk_widget().place_configure(x=840, y=270, width=499, height=410)
        (self.canvas2).mpl_connect("motion_notify_event", move_mouse)
        (self.canvas2).mpl_connect("button_press_event", onclick_)
        (self.canvas2).draw()
        toolbar2 = NavigationToolbar2Tk((self.canvas2),(self.window))
        toolbar2.pack()
        toolbar2.place_configure(x=840, y=680)
        toolbar2.update() 
        
        (self.window).mainloop()
