# First, and before importing any Enthought packages, set the ETS_TOOLKIT
# environment variable to qt4, to tell Traits that we will use Qt.

## --- mayavi imports
import os
os.environ['ETS_TOOLKIT'] = 'qt4'
# By default, the PySide binding will be used. If you want the PyQt bindings
# to be used, you need to set the QT_API environment variable to 'pyqt'
os.environ['QT_API'] = 'pyqt'

# To be able to use PySide or PyQt4 and not run in conflicts with traits,
# we need to import QtGui and QtCore from pyface.qt
from pyface.qt import QtGui, QtCore
# Alternatively, you can bypass this line, but you need to make sure that
# the following lines are executed before the import of PyQT:
#   import sip
#   sip.setapi('QString', 2)

from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor

from mayavi.sources.builtin_surface import BuiltinSurface
from mayavi.modules.surface import Surface
from mayavi.filters.transform_data import TransformData

## --- matplotlib imports
from PyQt5 import QtWidgets

import matplotlib
# Ensure using PyQt5 backend
matplotlib.use('QT5Agg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)



## --- other imports
import numpy as np
from pyGDM2 import tools




# =============================================================================
# mayavi
# =============================================================================
#==============================================================================
# Substrate
#==============================================================================
def _draw_rect(mlab, X0,X1, Y0,Y1, Z0,Z1, rotate_axis=(1,0,0), rotate_angle=(0),
                opacity=1, color=(.5,.5,.5), figure=None):
    engine = mlab.get_engine()
    def rotMat3D(axis, angle, tol=1e-12):
        """Return the rotation matrix for 3D rotation by angle `angle` degrees about an
        arbitrary axis `axis`.
        """
        t = np.radians(angle)
        x, y, z = axis
        R = (np.cos(t))*np.eye(3) +\
            (1-np.cos(t))*np.matrix(((x**2,x*y,x*z),(x*y,y**2,y*z),(z*x,z*y,z**2))) + \
            np.sin(t)*np.matrix(((0,-z,y),(z,0,-x),(-y,x,0)))
        R[np.abs(R)<tol]=0.0
        return R

    # Main code
    # Add a cubic builtin source
    rect_src = BuiltinSurface()
    engine.add_source(rect_src)
    rect_src.source = 'cube'
    rect_src.data_source.center = np.array([ (X1+X0)/2.,  (Y1+Y0)/2.,  (Z1+Z0)/2.])
    rect_src.data_source.x_length=X1-X0
    rect_src.data_source.y_length=Y1-Y0
    rect_src.data_source.z_length=Z1-Z0
    #~ rect_src.data_source.capping = False
    #~ rect_src.data_source.resolution = 250


    # Add transformation filter to rotate rect about an axis
    transform_data_filter = TransformData()
    engine.add_filter(transform_data_filter, rect_src)
    Rt = np.eye(4)
    Rt[0:3,0:3] = rotMat3D(rotate_axis, rotate_angle) # in homogeneous coordinates
    Rtl = list(Rt.flatten()) # transform the rotation matrix into a list
    transform_data_filter.transform.matrix.__setstate__({'elements': Rtl})
    transform_data_filter.widget.set_transform(transform_data_filter.transform)
    transform_data_filter.filter.update()
    transform_data_filter.widget.enabled = False   # disable the rotation control further.

    # Add surface module to the rect source
    rect_surface = Surface()
    engine.add_filter(rect_surface, transform_data_filter)
    # add color property
    rect_surface.actor.property.color = color
    rect_surface.actor.property.opacity = opacity
    
    return rect_surface

def _visu_struct(scene, struct, clearfig=True, reset_view=True, 
                 scale=0.85, abs_scale=False, material_labels=False, 
                 tit='', color='auto', mode='cube', 
                 draw_substrate=True, substrate_size=1.75, 
                 substrate_color=(0.7, 0.7, 0.9), substrate_opacity=0.5,
                 axis_labels=True, show=True, **kwargs):
        """plot structure in 3d
        
        plot the structure "struct" using 3d points. Either from list of 
        coordinates, or using a simulation definition dict as input.
        
        Parameters
        ----------
          - struct:    either simulation-dictionary or list of 3d coordinate tuples
          - clearfig:  if True, clf and init new figure on call
          - reset_view: if True, set isometric view
          - scale:     symbol scaling in units of stepsize (default 0.75)
          - abs_scale: enable absolute scaling, override internal scale calculation (default: False)
          - material_labels: add textlabels for different materials
          - color:     Color of scatterplot. Either "auto", or mayavi2-compatible color.
          - mode:      3d symbols for plotting meshpoints. see `mlab.points3d`. e.g. 'cube' or 'sphere' (default 'cube')
          - draw_substrate: Whether or not to draw a substrate (default: True)
          - substrate_size: size of substrate with respect to structure extensions (default: 2.0)
          - substrate_color: default (0.8, 0.8, 0.9)
          - substrate_opacity: default 0.5
          - axis_labels: whether to show the X/Y/Z dimensions of the nano-object (default: True)
          - show:      directly show plot (default True)
          - kwargs:    are passed to `mlab.points3d`
        
        """
        if not reset_view:
            ## save view to later restore it
            view = scene.mlab.view()
        if clearfig:
            scene.mlab.clf(figure=scene.mayavi_scene)
            scene.mlab.figure(bgcolor=(1.0, 1.0, 1.0), fgcolor=(0.,0.,0.),
                                   figure=scene.mayavi_scene)
        
        
        from pyGDM2 import structures
        X,Y,Z = tools.get_geometry(struct)
        step = tools.get_step_from_geometry(struct)
        
        ## -- set scatter-scaling depending on structure size
        maxdist = max([max(X)-min(X), max(Y)-min(Y)])
        if not abs_scale: scale = step*scale
        
        ## -- colors for subsets with different materials
        if color == 'auto':
            if hasattr(struct, "struct") or type(struct) == structures.struct:
                if hasattr(struct, "struct"):
                    struct = struct.struct
            
                if hasattr(struct.material, '__iter__'):
                    materials = [s.__name__ for s in struct.material]
                    if len(set(materials)) > 1:
                        material = np.array(materials)
                        different_materials = np.unique(materials)
                        indices_subsets = []
                        for struct_fraction in different_materials:
                            indices_subsets.append(np.arange(len(material))[material==struct_fraction])
                    else:
                        color = (0.3,0.3,0.3)
                else:
                    color = (0.3,0.3,0.3)
            else:
                color = (0.3,0.3,0.3)
                
        if draw_substrate:
            X0 = min(X) - (substrate_size/2. - 0.5) * maxdist
            Y0 = min(Y) - (substrate_size/2. - 0.5) * maxdist
            X1 = max(X) + (substrate_size/2. - 0.5) * maxdist
            Y1 = max(Y) + (substrate_size/2. - 0.5) * maxdist
            Z0 = - step
            Z1 = - step/10.
            _draw_rect(scene.mlab, X0,X1, Y0,Y1, Z0,Z1, 
                       opacity=substrate_opacity, color=substrate_color,
                       figure=scene.mayavi_scene)
        
        ## draw structure
        ## --- if multi-material: set marker colors
        if color != 'auto':
            im = scene.mlab.points3d(X,Y,Z, mode=mode, scale_factor=scale, 
                                          color=color, figure=scene.mayavi_scene, **kwargs)
            if axis_labels: 
                scene.mlab.axes(xlabel='X (nm)', ylabel='Y (nm)', zlabel='Z (nm)',
                                     figure=scene.mayavi_scene)
        else:
            import matplotlib.pyplot as plt
            colors = [plt.cm.colors.to_rgb('C{}'.format(i)) for i in range(1,10)] * int(2 + len(indices_subsets)/9.)
            im = []
            for i, idx in enumerate(indices_subsets):
                col = colors[i]
                im.append(scene.mlab.points3d(X[idx],Y[idx],Z[idx], mode=mode, 
                                                   scale_factor=scale, color=col, 
                                                   figure=scene.mayavi_scene, **kwargs))
                if axis_labels: 
                    scene.mlab.axes(xlabel='X (nm)', ylabel='Y (nm)', zlabel='Z (nm)',
                                         figure=scene.mayavi_scene)
                if material_labels:
                    ## add space for approximately same text length and size
                    N_max_char = max([len(l) for l in different_materials])
                    mat_label = different_materials[i] + " "*2*(N_max_char-len(different_materials[i]))
                    scene.mlab.text(0.02, 0.95-0.05*i, mat_label,
                                    color=col, opacity=0.8,
                                    figure=scene.mayavi_scene)
                    
        
        scene.mlab.title(tit, figure=scene.mayavi_scene)
        
        scene.mlab.orientation_axes(figure=scene.mayavi_scene)
        if reset_view:
            scene.mlab.view(45, 45, figure=scene.mayavi_scene)
        else:
            scene.mlab.view(*view, figure=scene.mayavi_scene)
        
        return im


def _visu_vectorfield(scene, NF, struct=None, clearfig=True, reset_view=True, 
                      scale=1.5, abs_scale=False, 
                     tit='', complex_part='real', clim=[0.0, 1.0],
                     axis_labels=True, show=True, **kwargs):
    """3d quiverplot of nearfield
    
    Parameters
    ----------
     - NF:       Nearfield definition. `np.array`, containing 6-tuples:
                   (X,Y,Z, Ex,Ey,Ez), the field components being complex.
     - struct:   optional structure definition (if field is supplied in 3-tuple 
                 form without coordinates). Either `simulation` object, or list
                 of coordinate (x,y,z) tuples 
     - clearfig:  if True, clf and init new figure on call
     - reset_view: if True, set isometric view
     - scale:     symbol scaling in units of stepsize (default 0.75)
     - abs_scale: enable absolute scaling, override internal scale calculation (default: False)
     - complex_part: Which part of complex field to plot. 
                     Either 'real' or 'imag'. (default: 'real')
     - axis_labels: whether to show the X/Y/Z dimensions of the nano-object (default: True)
     - show:     whether to directly show the figure (default: True)
    
    All other keyword arguments are passed to mlab's `quiver3d`.
    """
    if not reset_view:
        ## save view to later restore it
        view = scene.mlab.view()
    if clearfig:
        scene.mlab.clf(figure=scene.mayavi_scene)
        scene.mlab.figure(bgcolor=(1.0, 1.0, 1.0), fgcolor=(0.,0.,0.),
                               figure=scene.mayavi_scene)
            
    ## case: provided structure+NF separately: NF may contain field_config dict as first element
    if len(NF) == 2:
        NF = NF[1]
    
    if len(NF.T) == 6:
        X,Y,Z, UXcplx,UYcplx,UZcplx = np.transpose(NF).real
    elif len(NF.T) == 3 and struct is not None:
        UXcplx,UYcplx,UZcplx = np.transpose(NF)
        X,Y,Z = tools.get_geometry(struct).real
    else:
        raise ValueError("Error: Wrong number of columns in vector field. Expected (Ex,Ey,Ez)-tuples + `simulation` object or (x,y,z, Ex,Ey,Ez)-tuples.")
    
    if complex_part.lower() == "real":
        Ex,Ey,Ez = UXcplx.real, UYcplx.real, UZcplx.real
    elif complex_part.lower() == "imag":
        Ex,Ey,Ez = UXcplx.imag, UYcplx.imag, UZcplx.imag
    else:
        raise ValueError("Error: Unknown `complex_part` argument value. Must be either 'real' or 'imag'.")
    S = np.sqrt(Ex**2 + Ey**2 + Ez**2)
    
    step = tools.get_step_from_geometry(np.array([X,Y,Z]).T)
    if not abs_scale:
        scale = step*scale
    else:
        scale = scale
    
    im = scene.mlab.quiver3d(X,Y,Z, Ex,Ey,Ez, scalars=S, scale_factor=scale, 
                      vmin=clim[0], vmax=clim[1], figure=scene.mayavi_scene, **kwargs)
    
    if axis_labels: 
        scene.mlab.axes(xlabel='X (nm)', ylabel='Y (nm)', zlabel='Z (nm)', figure=scene.mayavi_scene)
    scene.mlab.title(tit)
    if reset_view:
        scene.mlab.view(45, 45, figure=scene.mayavi_scene)
    else:
        scene.mlab.view(*view, figure=scene.mayavi_scene)
        
    return im




#The actual visualization
class structure_visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())
    
    @on_trait_change('scene.activated')
    def update_plot(self):
        ## initiate empty scene
        self.scene.mlab.clf(figure=self.scene.mayavi_scene)
        self.scene.mlab.figure(bgcolor=(1.0, 1.0, 1.0), fgcolor=(0.,0.,0.),
                               figure=self.scene.mayavi_scene)
#        self.scene.renderer.set(use_depth_peeling=True)
        
    def plot_struct(self, struct, reset_view=True, material_labels=False, **kwargs):
        im = _visu_struct(self.scene, struct, reset_view=reset_view, material_labels=material_labels, **kwargs)
        return im
    
    
    # the layout of the dialog created
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=250, width=300, show_label=False),
                resizable=True # We need this to resize with the parent widget
                )


## Widget geometry visualization
class MayaviQWidget_geo(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)   # tight
        layout.setSpacing(0)
        self.visualization = structure_visualization()

        # The edit_traits call will generate the widget to embed.
        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)






#The actual visualization
class NF_visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())
    
    def __init__(self):
        self.ims = []
        self.Emax = []
        self.i_cur_frame = 0
        self.Nframes = 50
    
    @on_trait_change('scene.activated')
    def update_plot(self):
        ## initiate empty scene
        self.scene.mlab.clf(figure=self.scene.mayavi_scene)
        self.scene.mlab.figure(bgcolor=(1.0, 1.0, 1.0), fgcolor=(0.,0.,0.), 
                               figure=self.scene.mayavi_scene)
    
    def plot_struct(self, struct, **kwargs):
        im = _visu_struct(self.scene, struct, **kwargs)
        return im
    
    
    def init_field_dat(self, sim, field_index, 
                       Nframes=50, t_start=0, frame_list=None,
                       colormap='Blues', 
                       scale=2.5, clim=[0.2, 1.0], cycle_moment=0,
                       axis_labels=True, abs_scale=False,
                       reset_view=False, clearfig=True, which_field='E',
                       **kwargs):
        self.sim = sim
        self.field_index = field_index
        self.scale = scale
        self.Nframes = Nframes
        
        NF = tools.get_field_as_list_by_fieldindex(sim, field_index, which_field).T
        x,y,z = NF[0:3].real
        
        self. maxdist = max([max(x)-min(x), max(y)-min(y)])
        self.step = tools.get_step_from_geometry(NF[0:3].real.T)
        if not abs_scale:
            self.scale_quiver = self.step*scale
        else:
            self.scale_quiver = scale
            
        
        ## --- phase and length of complex field
        Exi = NF[3]
        Exr = np.absolute(Exi)
        Ax  = np.angle(Exi)
        
        Eyi = NF[4]
        Eyr = np.absolute(Eyi)
        Ay  = np.angle(Eyi)
        
        Ezi = NF[5]
        Ezr = np.absolute(Ezi)
        Az  = np.angle(Ezi)
        
        scaleF = float((Exr.max()+Eyr.max()+Ezr.max()))
        Exr /= scaleF
        Eyr /= scaleF
        Ezr /= scaleF
        
        ## --- create list of timesteps
        alambda = 100.
        omega = 2*np.pi/float(alambda)
        
        framnumbers = np.linspace(t_start, alambda+t_start, Nframes)
        if frame_list is not None:
            framnumbers = framnumbers[frame_list]
        
        self.ims = []
        self.Emax = []
        for t in framnumbers:    
            Ex = (Exr * np.cos((Ax - omega*t))).real
            Ey = (Eyr * np.cos((Ay - omega*t))).real
            Ez = (Ezr * np.cos((Az - omega*t))).real
            E = np.sqrt( Ex**2 +Ey**2 + Ez**2)            
            self.Emax.append(E.max())
            self.ims.append( [x,y,z, Ex,Ey,Ez, E] )
        for i, _tmp in enumerate(self.Emax):
            self.ims[i][-1] /= max(self.Emax)
        
        
# =============================================================================
#         do the actual field plot
# =============================================================================
        if not reset_view:
            ## save view to later restore it
            view = self.scene.mlab.view()
        if clearfig:
            self.scene.mlab.clf(figure=self.scene.mayavi_scene)
            self.scene.mlab.figure(bgcolor=(1.0, 1.0, 1.0), fgcolor=(0.,0.,0.),
                                   figure=self.scene.mayavi_scene)
        
        self.i_cur_frame = int(self.Nframes * cycle_moment/100) # cycle_moment: value between 0 and 100
        D = self.ims[self.i_cur_frame]
        self.im = self.scene.mlab.quiver3d(D[0],D[1],D[2], D[3],D[4],D[5], scalars=D[6], 
                            scale_factor=self.scale_quiver, vmin=clim[0], vmax=clim[1], 
                            colormap=colormap, figure=self.scene.mayavi_scene, **kwargs)
        
        if axis_labels: 
            self.scene.mlab.axes(xlabel='X (nm)', ylabel='Y (nm)', zlabel='Z (nm)', 
                                 figure=self.scene.mayavi_scene)
        
        self.im.glyph.color_mode = 'color_by_scalar'
        
        if reset_view:
            self.scene.mlab.view(45, 45, figure=self.scene.mayavi_scene)
        else:
            self.scene.mlab.view(*view, figure=self.scene.mayavi_scene)
        
        return self.im
    
    
    def animate_field_next_step(self):
        self.i_cur_frame += 1
        if self.i_cur_frame >= self.Nframes:
            self.i_cur_frame = 0
        D = self.ims[self.i_cur_frame]
        
        self.im.mlab_source.set(x=D[0],y=D[1],z=D[2], u=D[3],v=D[4],w=D[5])
        self.im.mlab_source.scalars = D[6]
        # self.im.glyph.color_mode = 'color_by_scalar'
                
        return self.im
        
    
    # the layout of the dialog created
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=250, width=300, show_label=False),
                resizable=True # We need this to resize with the parent widget
                )

## Widget nearfield visualization
class MayaviQWidget_NF(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)   # tight
        layout.setSpacing(0)
        self.visualization = NF_visualization()

        # The edit_traits call will generate the widget to embed.
        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)








# =============================================================================
# matplotlib
# =============================================================================
# Matplotlib canvas class to create figure
class MplCanvas(Canvas):
    def __init__(self):
        self.fig = Figure()
        # self.ax = self.fig.add_subplot(111)
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

# Matplotlib widget
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)   # Inherit from QWidget
        self.setLayout(QtWidgets.QVBoxLayout())
        self.canvas = MplCanvas()
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.canvas)
        self.layout().addWidget(self.toolbar)

