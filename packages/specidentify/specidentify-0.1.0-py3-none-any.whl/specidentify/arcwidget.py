
import numpy as np
import copy
from matplotlib import pyplot as plt
from astropy import units as u
from astropy import modeling as mod

import ipywidgets as widgets

from .wavelengthsolution import WavelengthSolution
from .spectools import (flatspectrum,
                        make_artificial_spectra,
                        crosslinematch,
                        findzeropoint,
                        mcentroid
                        )


__all__ = ['ArcIdentify', 'CurveFit']

class ArcIdentify:
    def __init__(self, arc, ws, line_list=None, wavelength_range=None, flatten_order=None):
        """Preform identification of a spectrum of an arc lamp and return the wavelength solution for that spectrum.

        Parameters
        ----------
        arc: Spectrum1D
            An uncalibrated Spectrum1D of an observation of an arc lamp


        ws: WavelengthSolution
            An initial wavelength solution for the arc

        line_list: Astropy.Table
            A list of lines in the observed arc

        wavelength_range: list
            An initial guess for the wavelength range of the observed arc to be used in creating
            the artificial spectrum of the arc.

        flatten_order: int, None
            If not none, the continuum of the arc observations will be removed.  A polynomial of
            this order will be fit to the continuum and subtracted.

        Returns
        -------
        ws: WavelengthSolution
            A calibrated wavelength solution for the observed arc
        """
        #super().__init__()
        #output = widgets.Output()

        self.arc = arc
        self.xarr = self.arc.spectral_axis.value
        if flatten_order:
           self.farr = flatspectrum(self.arc.spectral_axis.value, self.arc.flux, order=flatten_order)
        else:
            self.farr = self.arc.spectral_axis.value
        self.ws = ws
        self.orig_ws = copy.deepcopy(ws)
        self.arc_color = '#2d34ff'
        self.line_list = line_list
        self.xp = []
        self.wp = []
        self.xpd = [] # saved deleted points
        self.wpd = []
        # TODO: Need to add these values into the options
        self.textcolor = 'black'
        self.cdiff = 20
        self.sections = 6
        self.mdiff = 20
        self.wdiff = 20
        self.sigma = 5
        self.res = 2
        self.niter = 5
        self.ndstep = 20

        # make an artificial version of the line list for plotting
        self.line_spec = make_artificial_spectra(self.line_list, wavelength_range,
                                                 wavelength_unit=u.angstrom,
                                                 flux_unit=u.electron, sigma=self.sigma)

        # set up the information and control panel
        color_picker = widgets.ColorPicker(
            value=self.arc_color,
            description='Color for Arc'
        )
        color_picker.observe(self.line_color, 'value')

        self.pixel_value = widgets.BoundedFloatText(
                min=0,
                max=len(self.arc.data),
                description='pixel',
                disable=True
            )
        self.wavelength_value = widgets.FloatText(
                description='wavelength',
                disable=True
            )

        self.add_point_button = widgets.Button(
            description='Add point',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click button to add a point at this x value and wavelength value',
        )
        self.add_point_button.on_click(self.add_point)

        self.dispersion_unit = widgets.RadioButtons(
                options=['pixel', 'wavelength'],
                value = 'pixel',
                description='Dispersion:',
                disabled=False
            )
        self.dispersion_unit.observe(self.set_dispersion, 'value')

        self.display_artificial = widgets.Checkbox(
            value=True,
            description='Display line list',
            disabled=False,
            indent=False
        )
        self.display_artificial.observe(self.set_display_artifical, 'value')

        self.display_features = widgets.Checkbox(
            value=True,
            description='Display features',
            disabled=False,
            indent=False
        )
        self.display_features.observe(self.set_display_features, 'value')

        controls = widgets.VBox([color_picker,
                                 self.pixel_value,
                                 self.wavelength_value,
                                 self.add_point_button, 
                                 self.dispersion_unit,
                                 self.display_artificial,
                                 self.display_features
                                ])

        # Set up the initial plot
        self.fig, self.ax = plt.subplots(constrained_layout=True, figsize=(8, 5))
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

        self.draw_plot()


        display(controls)

    def draw_plot(self):

        self.ax.cla()
        if self.dispersion_unit.value == 'pixel':
            x = self.xarr
        elif self.dispersion_unit.value == 'wavelength':
            x = self.ws(self.xarr)
        y = self.farr
        self.line, = self.ax.plot(x, y, self.arc_color)
        self.ax.set_xlabel(f'Dispersion({self.dispersion_unit.value})')
        self.ax.set_ylabel("Flux")
        if self.display_artificial.value:
            self.draw_artificial()
        if self.display_features.value:
            self.draw_features()

    def draw_artificial(self):

        w = self.ws(self.xarr)
        x = self.line_spec.spectral_axis.value
        y = self.line_spec.flux
        mask = (x > w.min()) * (x < w.max())
        x = x[mask]
        y = y[mask]
        y = y * self.farr.max() / y.max()

        if self.dispersion_unit.value == 'pixel':
            xarr = self.arc.spectral_axis.value
            farr = np.interp(w, x, y, left=0, right=0)
        elif self.dispersion_unit.value == 'wavelength':
            xarr = x
            farr = y

        self.line_art, = self.ax.plot(xarr, farr, 'grey')

    def draw_features(self):
        """Plot features identified in the line list"""

        if self.dispersion_unit.value == 'pixel':
            x = np.array(self.xp)
        elif self.dispersion_unit.value ==  'wavelength':
            x = np.array(self.wp)

        fl = x * 0.0 + 0.25 * self.arc.flux.max()
        self.splines = self.ax.plot(
            x, fl,
            ls='',
            marker='|',
            ms=20,
            color=self.textcolor)
        # set up the text position
        tsize = 8
        self.ymin, self.ymax = self.ax.get_ylim()
        ppp = (self.ymax - self.ymin) / (self.fig.get_figheight()
                                         * self.fig.get_dpi())
        f = self.ymax - 10 * tsize * ppp
        for x, w in zip(self.xp, self.wp):
            w_text = '%6.2f' % float(w)
            if self.dispersion_unit.value == 'pixel':
                x = x
            elif self.dispersion_unit.value ==  'wavelength':
                x = w
            self.ax.text(
                x,
                f,
                w_text,
                size=tsize,
                rotation='vertical',
                color=self.textcolor)


    def on_click(self, event):
        """These are the actions taken for mouse click press events on the plot

        """
        self.pixel_value.value = f'{event.xdata:5.2f}'
        self.wavelength_value.value = f'{self.ws(event.xdata):5.2f}' 


    def show_commands(self):
        cmd = """
 x - centroid on line    a - Display spectrum
 b - identify features   f - fit solution
 r - redraw spectrum     e - add closest line
 d - delete feature
       """
 #u - undelete feature
 #p - print features      P - print solution
 #z - zeropoint fit       Z - find zeropoint and dispersion
 #X - fit full X-cor      l - switch yscale to log
 #K - show detected peaks R - reset fit
        print(cmd)


    def on_key_press(self, event):
        """These are actions taken for key press events on the plot
        """
        if event.key == 'r':
            # redraw graph
            self.draw_plot()
        elif event.key == 'a':
            # draw artificial spectrum
            self.display_artificial.value = not self.display_artificial.value
            self.draw_plot()
        elif event.key == 'R':
            # reset the fit
            pass #TODO: check to make sure this works
            #self.ws = copy.deepcopy(self.orig_ws)
            #self.draw_plot()
        elif event.key == 'f':
            # find the fit
            self.find_fit()
        elif event.key == 'x':
            # return the centroid
            self.find_centroid(event.xdata)
        elif event.key == 'e':
            #  find closest feature from existing fit and line list
            # and match it
            self.addclosestline(event.xdata)
        elif event.key == 'd':
            # Delete feature
            save = False
            y = None
            self.deletepoints(event.xdata, y=y, save=save)
            self.draw_plot()
        elif event.key == 'b':
            # auto-idenitfy features
            self.findfeatures()
        elif event.key == 'z':
            # Assume the solution is correct and find the zeropoint
            # that best matches it from cross correllation
            self.findzp()

    def line_color(self, change):
        self.arc_color=change.new
        self.line.set_color(change.new)

    def set_dispersion(self, change):
        self.dispersion_unit.value = change.new
        self.draw_plot()


    def set_display_artifical(self, change):
        self.display_artificial.value=change.new
        if self.display_artificial.value:
            self.draw_artificial()
        else:
            self.draw_plot()

    def set_display_features(self, change):
        self.display_features.value=change.new
        if self.display_features.value:
            self.draw_features()
        else:
            self.draw_plot()

    def add_point(self, change):
        self.xp.append(self.pixel_value.value)
        self.wp.append(self.wavelength_value.value)
        self.draw_plot()

    def find_fit(self):
        self.ws.x = self.xp
        self.ws.wavelength = self.wp
        self.ws.fit()
        self.draw_plot()

    def find_centroid(self, x):
        cx = mcentroid(self.xarr,
                       self.farr,
                       xc=x,
                       xdiff=self.cdiff)

        self.pixel_value.value = f'{cx:5.2f}'


    def addclosestline(self, x):
        """Find the closes line to the centroided position and
           add it
        """
        cx = mcentroid(self.xarr,
                       self.farr,
                       xc=x,
                       xdiff=self.cdiff)
        w = self.ws(cx)
        d = abs(self.line_list['wavelength'] - w)
        w = self.line_list['wavelength'][d.argmin()]

        self.xp.append(cx)
        self.wp.append(w)
        self.draw_plot()

    def deletepoints(self, x, y=None, w=None, save=False):
        """ Delete points from the line list
        """
        dist = (np.array(self.xp) - x) ** 2
        in_minw = dist.argmin()

        if save:
            self.xpd.append(self.xp[in_minw])
            self.wpd.append(self.wp[in_minw])

        self.xp.__delitem__(in_minw)
        self.wp.__delitem__(in_minw)


    def findfeatures(self):
        """Given a set of features, find other features that might
           correspond to those features
        """
        xp, wp = crosslinematch(self.xarr, self.farr, self.line_list, self.ws,
                                res=self.sigma*self.res, mdiff=self.mdiff, wdiff=self.wdiff,
                                sections=self.sections, sigma=self.sigma, niter=self.niter)
        for x, w in zip(xp, wp):
            if w not in self.wp and w > -1:
                self.xp.append(x)
                self.wp.append(w)
        self.draw_plot()


    def findzp(self):
        """Find the zeropoint for the source and plot of the new value
        """
        dc = 0.5 * self.res * self.ndstep
        self.ws = findzeropoint(self.xarr, self.farr,
                                   self.line_spec.spectral_axis.value, self.line_spec.flux.value,
                                   self.ws, dc=dc, ndstep=self.ndstep, inttype='interp')
        self.draw_plot()


    def draw_error(self, error_color='blue'):
        self.ec = CurveFit(self.xp, self.wp, self.ws.model)


class CurveFit:
    def __init__(self, xp, yp, function):
        """Interface for iterativelive fitting a curve

        Parameters
        ----------
        xp: np.array
            An array of x-values


        yp: WavelengthSolution
            An array of y-values

        function:  ~astropy.modeling.models
            A 1D model describing the transformation between x and y

        Returns
        -------
        ws: WavelengthSolution
            A calibrated wavelength solution for the observed arc
        """

        self.xp = xp
        self.yp = yp
        self.function = function
        self.xpd = [] # saved deleted points
        self.ypd = []
        self.color='#FF0011'


        # set up the information and control panel
        color_picker = widgets.ColorPicker(
            value=self.color, 
            description='Color for Arc'
        )
        color_picker.observe(self.set_line_color, 'value')

        self.check_residual = widgets.Checkbox(
            value=True,
            description='Display residual',
            disabled=False,
            indent=False
        )
        self.check_residual.observe(self.set_residual, 'value')

        self.w = widgets.HTML()
        self.w.value = 'Starting'


        controls = widgets.VBox([color_picker, self.check_residual, self.w])


        # Set up the initial plot
        self.fig, self.ax = plt.subplots(constrained_layout=True, figsize=(5, 3.5))
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

        self.draw_plot()


        display(controls)

    def draw_plot(self):
        self.ax.cla()
        if self.check_residual.value:
            self.ax.set_ylabel("$\Delta x - y$")
            self.points, = self.ax.plot(self.xp, self.yp - self.function(self.xp), ls='', marker='o', color=self.color)
            self.dpoints, = self.ax.plot(self.xpd, self.ypd - self.function(self.xpd), ls='', marker='x', color=self.color)
        else:
            self.ax.set_ylabel("y")
            self.points, = self.ax.plot(self.xp, self.yp, ls='', marker='o', color=self.color)
            x = np.array(self.xp)
            xarr = np.arange(x.min(), x.max(), (x.max()-x.min())/100.0)
            self.line, = self.ax.plot(xarr, self.function(xarr), color='black')



        self.ax.set_xlabel('x')


    def on_key_press(self, event):
        """These are actions taken for key press events on the plot
        """
        self.w.value = event.key
        if event.key == 'r':
            # redraw graph
            self.draw_plot()
        elif event.key == 'f':
            # find the fit
            self.find_fit()

        elif event.key == 'd':
            # Delete feature
            save = True
            self.delete_points(event.xdata, y=event.ydata, save=save)
            self.draw_plot()


        elif event.key == 'u':
            # undelete
            self.undeletepoints(event.xdata, y=event.ydata)
            self.draw_plot()


    def set_line_color(self, change):
        self.arc_color=change.new
        self.points.set_color(change.new)

    def set_residual(self, change):
        self.check_residual.value = change.new
        self.draw_plot()


    def find_fit(self):
        self.w.value = 'fitting'
        fitter = mod.fitting.LinearLSQFitter()
        weights = np.ones_like(self.xp)
        self.function = fitter(self.function, self.xp, self.yp, weights=weights)
        self.draw_plot()



    def delete_points(self, x, y=None, w=None, save=False):
        """ Delete points from the line list
        """
        dist = (np.array(self.xp) - x) ** 2


        if y is not None:
            x = np.array(self.xp)
            w = self.function(np.array(self.xp))
            norm = x.max() / abs(self.yp - w).max()
            dist += norm * (self.yp - w - y) ** 2
            # print y, norm, dist.min()
            # print y, dist.min()
        elif w is not None:
            norm = self.xarr.max() / abs(self.wp - w).max()
            dist += norm * (self.wp - w)**2
        in_minw = dist.argmin()

        if save:
            self.xpd.append(self.xp[in_minw])
            self.ypd.append(self.yp[in_minw])


        self.xp.__delitem__(in_minw)
        self.yp.__delitem__(in_minw)

        self.draw_plot()

    def undeletepoints(self, x, y=None):
        """ Delete points from the line list
        """
        if len(self.xpd) < 1:
            return
        if len(self.xpd) == 1:
            self.xp.append(self.xpd[0])
            self.yp.append(self.ypd[0])
            self.xpd.__delitem__(0)
            self.ypd.__delitem__(0)


            return

        dist = (np.array(self.xpd) - x) ** 2
        if y is not None:
            x = np.array(self.xpd)
            w = self.function(np.array(self.xpd))
            norm = x.max() / abs(self.ypd - w).max()
            dist += norm * (self.ypd - w - y) ** 2
        in_minw = dist.argmin()
        self.w.value = f'{in_minw}'

        self.xp.append(self.xpd[in_minw])
        self.yp.append(self.ypd[in_minw])
        self.w.value = '{in_minw}'
        self.xpd.__delitem__(in_minw)
        self.ypd.__delitem__(in_minw)
        self.w.value = 'here'

        return

