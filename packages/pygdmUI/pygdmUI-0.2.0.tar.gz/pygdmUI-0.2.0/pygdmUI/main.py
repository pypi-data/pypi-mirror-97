from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal)
from pygdmUI.custom_qt_objects import MayaviQWidget_NF, MayaviQWidget_geo, MplWidget

# import pyqtgraph as pg
# import pyqtgraph.opengl as gl

import numpy as np

from pyGDM2 import tools
from pyGDM2 import structures
from pyGDM2 import materials
from pyGDM2 import fields
from pyGDM2 import propagators
from pyGDM2 import propagators_2D
from pyGDM2 import core
from pyGDM2 import visu

import warnings
import os
import pickle
import copy
import sys
import time
import inspect
from inspect import signature

from pygdmUI import __version__ as _pygdmui_version
from pygdmUI.qt_ui_base import Ui_MainWindow
from pygdmUI.pygdm_function_configs import (spectra_func, derived_maps_func, rasterscan_func,
                                    gen_linescan_mapping1d)

import matplotlib.pyplot as plt




# =============================================================================
# other
# =============================================================================
class dummystruct():
    ## dummy class for unknown geometric model
    __name__ = "userdefined object"


# =============================================================================
# simulation running thread
# =============================================================================
class QThreadRunSim(QtCore.QThread):

    sigStatusSimRun = pyqtSignal(dict)
    sigFinishSimRun = pyqtSignal(core.simulation)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.sim = None
        self.method = 'lu'
        self.setupmethod = 'fortran'
        
    def set_sim(self, sim):
        self.sim = sim
        
    def set_method(self, method, calcH):
        self.method = method
        self.calcH = calcH

    def cancel(self):
        self.cont = False

    def emit_status(self, status_dict):
        self.sigStatusSimRun.emit(status_dict)
        return self.cont
    
    def run(self):
        self.cont = True
        self.running = True
        core.scatter(self.sim, 
                     method=self.method, 
                     calc_H=self.calcH, 
                     callback=self.emit_status, 
                     verbose=False)
        self.sigFinishSimRun.emit(self.sim)

        




# =============================================================================
# main GUI class 
# =============================================================================
class MyApplication(QtWidgets.QMainWindow):
    
    sigCancelSim = pyqtSignal()
    
    
    def __init__(self, parent=None):
        print("Init pyGDM-UI... ", end='')
        super(MyApplication, self).__init__(parent)
        self.ui =  Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.subgeotypelist = []
        self.geolist = []
        self.materialslist = []
        
        self.select_geo_mayaviobj = None
        self.sim_finished = False
        
        self.i_spec_plot_color = 0
        self.i_mapping_plot_color = 0
        self.i_rasterscan_plot_color = 0
        
        self.window_title = "pyGDM-UI - v{}".format(_pygdmui_version)
        self.setWindowTitle(self.window_title)
# =============================================================================
#         signals / slots
# =============================================================================
        ## --- general
        self.ui.actionsave_sim.triggered.connect(self.on_click_save_sim)
        self.ui.actionload_sim.triggered.connect(self.on_click_load_sim)
        self.ui.actionsave_structure.triggered.connect(self.on_click_save_struct)
        self.ui.actionsave_structure_as_txt.triggered.connect(self.on_click_save_struct_as_txt)
        self.ui.actionload_structure.triggered.connect(self.on_click_load_struct)
        
        
        ## --- geometry tab
        self.ui.comboBoxMesh.currentTextChanged.connect(self.on_select_mesh_n1_n2_n3_spacing)
        self.ui.lineEditStep.textChanged.connect(self.on_select_mesh_n1_n2_n3_spacing)
        self.ui.comboBoxMesh.currentTextChanged.connect(self.on_change_mesh_step)
        self.ui.lineEditStep.textChanged.connect(self.on_change_mesh_step)
        
        self.ui.lineEditN1.textChanged.connect(self.on_select_mesh_n1_n2_n3_spacing)
        self.ui.lineEditN2.textChanged.connect(self.on_select_mesh_n1_n2_n3_spacing)
        self.ui.lineEditN3.textChanged.connect(self.on_select_mesh_n1_n2_n3_spacing)
        self.ui.lineEditSpacing.textChanged.connect(self.on_select_mesh_n1_n2_n3_spacing)
        
        self.ui.comboBoxMaterial.currentIndexChanged.connect(self.on_select_material)
        self.ui.comboBoxGeo.currentIndexChanged.connect(self.on_select_geo)
        
        self.ui.pushButtonAddGeo.clicked.connect(self.on_click_gen_geo)
        self.ui.pushButtonApplyOffsetGeo.clicked.connect(self.on_click_offset_geo)
        self.ui.pushButtonApplyRotationGeo.clicked.connect(self.on_click_rotate_geo)
        self.ui.pushButtonOffsetXpOne.clicked.connect(lambda: self.geo_apply_offset([1,0,0]))
        self.ui.pushButtonOffsetXmOne.clicked.connect(lambda: self.geo_apply_offset([-1,0,0]))
        self.ui.pushButtonOffsetYpOne.clicked.connect(lambda: self.geo_apply_offset([0,1,0]))
        self.ui.pushButtonOffsetYmOne.clicked.connect(lambda: self.geo_apply_offset([0,-1,0]))
        self.ui.pushButtonOffsetZpOne.clicked.connect(lambda: self.geo_apply_offset([0,0,1]))
        self.ui.pushButtonOffsetZmOne.clicked.connect(lambda: self.geo_apply_offset([0,0,-1]))
        self.ui.pushButtonDelGeo.clicked.connect(self.on_click_del_geo)
        self.ui.pushButtonClearGeo.clicked.connect(lambda: self.on_click_clear_geo(True))
        self.ui.listWidgetStructures.itemSelectionChanged.connect(self.on_select_struct_constituent)
        self.ui.checkBoxGeoMaterialLabels.stateChanged.connect(self.on_click_geo_mat_lables)
        
        
        ## --- simulation tab
        self.AnimateIntFieldTimer = QtCore.QTimer(self)
        self.AnimateIntFieldTimer.timeout.connect(self.update_animation_intfield)
        self.ui.comboBoxFieldGen.currentIndexChanged.connect(self.on_select_field)
        self.ui.pushButtonStartSim.clicked.connect(self.on_click_run_sim)
        self.ui.pushButtonToggleAnimateIntField.clicked.connect(self.on_click_toggle_animation)
        self.ui.pushButtonCancelSim.clicked.connect(self.on_click_cancel_sim)
        self.ui.pushButtonQuicksaveSim.clicked.connect(lambda: self.save_sim("__quicksave.pygdmsim"))
        self.ui.pushButtonQuickloadSim.clicked.connect(self.on_click_quickload_sim)
        self.ui.listWidgetAvailableWavelengths.itemSelectionChanged.connect(self.on_click_select_sim_config)
        self.ui.listWidgetAvailableFieldConfigs.itemSelectionChanged.connect(self.on_click_select_sim_config)
        self.ui.lineEditAnimateIntFieldScale.textChanged.connect(self.on_click_select_sim_config)
        self.ui.horizontalSliderPlotMomentOpticalCycleIntField.sliderReleased.connect(self.on_click_select_sim_config)
        self.ui.radioButtonE.toggled.connect(self.on_click_select_sim_config)
        self.ui.radioButtonH.toggled.connect(self.on_click_select_sim_config)
        
        self.simRunThread = QThreadRunSim()
        self.sigCancelSim.connect(self.simRunThread.cancel)
        self.simRunThread.sigStatusSimRun.connect(self.on_simulation_status)
        self.simRunThread.sigFinishSimRun.connect(self.on_simulation_finished)
        
        
        ## --- spectra tab
        self.ui.listWidgetAvailableSpectraFuncs.itemSelectionChanged.connect(self.on_click_select_spectra_func)
        self.ui.pushButtonCalcSpectrum1.clicked.connect(self.on_click_calc_spectrum)
        self.ui.pushButtonCalcSpectrum2.clicked.connect(self.on_click_calc_spectrum)
        
        self.ui.pushButtonSaveSpec.clicked.connect(self.on_click_save_spectrum)
        self.ui.actionsave_last_calculated_spectra.triggered.connect(self.on_click_save_spectrum)
        

        ## --- mapping tab
        self.ui.listWidgetAvailableMappingFuncs.itemSelectionChanged.connect(self.on_click_select_mapping_func)
        self.ui.pushButtonCalcMapping1.clicked.connect(self.on_click_calc_mapping)
        self.ui.pushButtonCalcMapping2.clicked.connect(self.on_click_calc_mapping)
        
        self.ui.pushButtonSaveMapping.clicked.connect(self.on_click_save_mapping)
        self.ui.actionsave_last_calculated_mapping.triggered.connect(self.on_click_save_mapping)
        
        
        ## --- rasterscan tab
        self.ui.listWidgetAvailableRasterscanFuncs.itemSelectionChanged.connect(self.on_click_select_rasterscan_func)
        self.ui.pushButtonCalcRasterscan1.clicked.connect(self.on_click_calc_rasterscan)
        self.ui.pushButtonCalcRasterscan2.clicked.connect(self.on_click_calc_rasterscan)
        
        self.ui.pushButtonSaveRasterscan.clicked.connect(self.on_click_save_rasterscan)
        self.ui.actionsave_last_calculated_rasterscan.triggered.connect(self.on_click_save_rasterscan)
        
        
# =============================================================================
#         populate items
# =============================================================================
        ## --- geometry tab
        self.ui.comboBoxDyads.clear()
        self.ui.comboBoxDyads.addItems(['3D', '2D'])
        
        self.ui.comboBoxMesh.clear()
        self.ui.comboBoxMesh.addItems(['cube', 'hex'])
        
        listMaterial = [i.__name__ for i in materials.MAT_LIST]
        self.ui.comboBoxMaterial.clear()
        self.ui.comboBoxMaterial.addItems(listMaterial)
        
        listGeos = [i.__name__ for i in structures.STRUCT_LIST]
        self.ui.comboBoxGeo.clear()
        self.ui.comboBoxGeo.addItems(listGeos)
        
        ## --- simulation tab
        listFields = [i.__name__ for i in fields.FIELDS_LIST]
        self.ui.comboBoxFieldGen.clear()
        self.ui.comboBoxFieldGen.addItems(listFields)
        
        ## --- spectrum tab
        for conf in spectra_func:
            item = QtWidgets.QListWidgetItem(conf["name"])
            self.ui.listWidgetAvailableSpectraFuncs.addItem(item)
        
        ## --- derived mappings tab
        for conf in derived_maps_func:
            item = QtWidgets.QListWidgetItem(conf["name"])
            self.ui.listWidgetAvailableMappingFuncs.addItem(item)
        
        ## --- rasterscan tab
        for conf in rasterscan_func:
            item = QtWidgets.QListWidgetItem(conf["name"])
            self.ui.listWidgetAvailableRasterscanFuncs.addItem(item)
        
        
        print("Done.")
        
        
        
# =============================================================================
#         reload last structure
# =============================================================================
        try:
            self.load_struct("__autosave_struct_tmp.pkl.pygdmstruct")
            # self.load_sim("__quicksave.pygdmsim")
        except (FileNotFoundError, EOFError):
            pass
        except Exception as e:
            warnings.warn("Failed loading former structure: " + str(e))
    
        
#%% common functions
# =============================================================================
# save / load 
# =============================================================================
    def save_sim(self, filename):
        if self.sim_finished:
            tools.save_simulation(self.sim, filename)
                   
    def load_sim(self, filename):
        self.sim = tools.load_simulation(filename)
        
        ## populate "field configs" and wavelenght lists
        self.load_field_config_and_wl_lists()
        
        
        self.ui.textEditSimStatus.clear()
        msg = tools.print_sim_info(self.sim, prnt=False)
        self.ui.textEditSimStatus.append("Loaded simulation\n" + msg + '\n\n\n')
        self.sim_finished = True
        
        self.ui.lineEditWl0.setText(str(np.min(self.sim.efield.wavelengths)))
        self.ui.lineEditWl1.setText(str(np.max(self.sim.efield.wavelengths)))
        self.ui.lineEditNwl.setText(str(len(self.sim.efield.wavelengths)))
        
        ## reset structure
        try:
            self.load_struct(filename + ".pkl.pygdmstruct")
        except:
            warnings.warn("No saved structure found with the simulation. Loading geometry from sim as generic model.")
            self.load_struct(self.sim)
            

    def save_struct(self, filename):
        pickle.dump(dict(geolist=self.geolist, 
                             materialslist=self.materialslist,
                             subgeotypelist=self.subgeotypelist, 
                             struct_full=self.struct_full,
                             dyads=self.dyads
                             ),
                        open(filename, "wb"))
    
    def load_struct(self, filename):
        if type(filename) == core.simulation:
            sim = filename
            struct = sim.struct
            self.on_click_clear_geo(show_dialog=False)
            self.geolist = [struct.geometry]
            self.materialslist = [struct.material]
            self.subgeotypelist = [dummystruct()]
            self.dyads = sim.dyads
        else:   # no simulation --> got filename to load list of geometries
            struct_dict = pickle.load(open(filename, "rb"))
            self.on_click_clear_geo(show_dialog=False)
            struct = struct_dict['struct_full']
            self.materialslist = struct_dict['materialslist']
            self.subgeotypelist = struct_dict['subgeotypelist']
            self.geolist = struct_dict['geolist']
            self.dyads = struct_dict['dyads']
        
        ## check mesh type
        mesh = tools.get_mesh_from_geometry(self.geolist[0])
        if mesh.lower() == 'cube':
            self.ui.comboBoxMesh.setCurrentIndex(0)
        else:
            self.ui.comboBoxMesh.setCurrentIndex(1)
        
        self.dyads.getEnvironmentIndices(500, self.geolist[0])
        self.ui.lineEditN1.setText(str(self.dyads.n1))
        self.dyads.getEnvironmentIndices(500, self.geolist[0])
        self.ui.lineEditN2.setText(str(self.dyads.n2))
        self.dyads.getEnvironmentIndices(500, self.geolist[0])
        self.ui.lineEditN3.setText(str(self.dyads.n3))
        
        self.ui.lineEditSpacing.setText(str(float(self.dyads.spacing)))
        self.ui.lineEditStep.setText(str(float(struct.step)))
        
        ## list of constituents
        for i in range(len(self.subgeotypelist)):
            item = QtWidgets.QListWidgetItem("{} (Ndp={}, mat={})".format(
                                            self.subgeotypelist[i].__name__, 
                                            len(self.geolist[i]), 
                                            self.materialslist[i][0].__name__))
            self.ui.listWidgetStructures.addItem(item)
        
        self.gen_full_structure(savestruct=False)
        self.reset_3D_views()


    def on_click_save_sim(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save pyGDM simulation", "",
                                                  "pyGDM simulations Files (*.pygdmsim *.pygdm *.sim);;All Files (*)", options=options)
        if filename:
            if '.' not in os.path.basename(filename):
                filename += ".pygdmsim"
            self.save_sim(filename)
            self.save_struct(filename + ".pkl.pygdmstruct")
            
    
    def on_click_load_sim(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"Load pyGDM simulation", "", 
                                                          "pyGDM simulations Files (*.pygdmsim *.pygdm *.sim);;All Files (*)", options=options)
        if files:
            self.load_sim(files[0])
            self.setWindowTitle(self.window_title + " - {}".format(os.path.basename(files[0])))


    def on_click_save_struct(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save pyGDM-UI geometry", "",
                                                  "pyGDM-UI structure Files (*.pygdmstruct);;All Files (*)", options=options)
        if filename:
            if '.' not in os.path.basename(filename):
                filename += ".pkl.pygdmstruct"
            self.save_struct(filename)


    def on_click_save_struct_as_txt(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save geometry coordinates as txt", "",
                                                  "text files (*.txt);;All Files (*)", options=options)
        if filename:
            if '.' not in os.path.basename(filename):
                filename += ".pygdmstruct.txt"
            np.savetxt(filename, self.struct_full.geometry, 
                       fmt='%.5g', header='X, Y, Z (nm)')
            
    
    def on_click_load_struct(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"Load pyGDM-UI geometry", "", 
                                                          "pyGDM-UI structure Files (*.pygdmstruct);;All Files (*)", options=options)
        if files:
            self.load_struct(files[0])

        
# =============================================================================
# functions shared by several tabs
# =============================================================================
    def load_field_config_and_wl_lists(self, wavelengths=True, auto_select_first=True):
        ## clear lists
        self.ui.listWidgetAvailableFieldConfigs.clear()
        self.ui.listWidgetRasterscanFieldconfig.clear()
        self.ui.listWidgetAvailableWavelengths.clear()
        
        ## populate "field configs" list
        field_configs = self.sim.efield.kwargs_permutations
        for i, conf in enumerate(field_configs):
            item = QtWidgets.QListWidgetItem("{}: ({})".format(i, str(conf)))
            self.ui.listWidgetAvailableFieldConfigs.addItem(item)
        if auto_select_first:
            self.ui.listWidgetAvailableFieldConfigs.setCurrentRow(0)  # select first
        
        ## populate "wavelengths" list
        if wavelengths:
            for i, wl in enumerate(self.sim.efield.wavelengths):
                item = QtWidgets.QListWidgetItem("{}nm".format(str(round(wl, 2))))
                self.ui.listWidgetAvailableWavelengths.addItem(item)
            if auto_select_first:
                self.ui.listWidgetAvailableWavelengths.setCurrentRow(0)  # select first
        
        ## populate "rasterscan field configs" list
        xkey_list = self.ui.lineEditResterscanXkey.text().split(',')
        ykey_list = self.ui.lineEditResterscanYkey.text().split(',')
        self.rasterscan_possibleX = False
        self.rasterscan_possibleY = False
        
        for xkey in xkey_list:
            if xkey in self.sim.efield.kwargs_permutations[0]:
                self.rasterscan_possibleX = True
                self.scanparam1_text = xkey
                break
        for ykey in ykey_list:
            if ykey in self.sim.efield.kwargs_permutations[0]:
                self.rasterscan_possibleY = True
                self.scanparam2_text = ykey                
                break
            
        if self.rasterscan_possibleX and self.rasterscan_possibleY:
            rasterscan_conf = tools.get_possible_field_params_rasterscan(self.sim, xkey, ykey)
            for i, conf in enumerate(rasterscan_conf):
                item = QtWidgets.QListWidgetItem("{}: ({})".format(i, str(conf)))
                self.ui.listWidgetRasterscanFieldconfig.addItem(item)
            if auto_select_first:
                self.ui.listWidgetRasterscanFieldconfig.setCurrentRow(0)  # select first
                
            self.ui.pushButtonCalcRasterscan1.setDisabled(False)
            self.ui.pushButtonCalcRasterscan2.setDisabled(False)

        else:
            item = QtWidgets.QListWidgetItem("incident field config contains no raster-scan")
            self.ui.listWidgetRasterscanFieldconfig.addItem(item)
            
            self.ui.pushButtonCalcRasterscan1.setEnabled(False)
            self.ui.pushButtonCalcRasterscan2.setEnabled(False)
    
    
    def reset_3D_views(self):
        self.ui.mayaviWidgetGeo.visualization.scene.mlab.view(45, 45, 
                  figure=self.ui.mayaviWidgetGeo.visualization.scene.mayavi_scene)
        self.ui.mayaviWidgetNF.visualization.scene.mlab.view(45, 45, 
                  figure=self.ui.mayaviWidgetNF.visualization.scene.mayavi_scene)
        
        
    
    
    
    
#%% geometry tab
# =============================================================================
#     geometry / material 
# =============================================================================
    def on_select_mesh_n1_n2_n3_spacing(self):
        self.mesh = self.ui.comboBoxMesh.currentText()
        self.step = float(self.ui.lineEditStep.text())
        self.n1 = complex(self.ui.lineEditN1.text())
        self.n2 = complex(self.ui.lineEditN2.text())
        self.n3 = complex(self.ui.lineEditN3.text())
        self.spacing = float(self.ui.lineEditSpacing.text())
        
        if self.ui.comboBoxDyads.currentText().lower() == '3d':
            self.dyads = propagators.DyadsQuasistatic123(self.n1, self.n2, self.n2, self.spacing)
        else:   # 2D
            self.dyads = propagators_2D.DyadsQuasistatic2D123(self.n1, self.n2, self.n2, self.spacing)
        
    def on_change_mesh_step(self):
        if self.ui.listWidgetStructures.count() >= 1:
            QtWidgets.QMessageBox.question(self, 'warning', 
                     "A structure already exists. Chaning step or mesh of sub-structures will break the model consitency!", 
                     QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
    
    def on_select_material(self):
        i_mat = self.ui.comboBoxMaterial.currentIndex()
        self.geo_material = materials.MAT_LIST[i_mat]
        kwarg_str_list = str(signature(self.geo_material))[1:-1].split(', ')
        self.ui.tableWidgetMaterialParams.clear()
        self.ui.tableWidgetMaterialParams.setColumnCount(2)
        self.ui.tableWidgetMaterialParams.setHorizontalHeaderLabels(['parameter', 'value'])
        self.ui.tableWidgetMaterialParams.setRowCount(len(kwarg_str_list))
        self.ui.tableWidgetMaterialParams.setToolTip(inspect.getdoc(self.geo_material))
        for i, kwstr in enumerate(kwarg_str_list):
            kwstr = kwstr.split('=')[0]
            item = QtWidgets.QTableWidgetItem()
            item.setText(kwstr)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidgetMaterialParams.setItem(i, 0, item)
            default = signature(self.geo_material).parameters[kwstr].default
            if default != inspect._empty:
                ## default value
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(default))
                self.ui.tableWidgetMaterialParams.setItem(i, 1, item)
    
    
    def on_select_geo(self):
        i_geo = self.ui.comboBoxGeo.currentIndex()
        self.geo_type = structures.STRUCT_LIST[i_geo]
        kwarg_str_list = str(signature(self.geo_type))[1:-1].split(', ')
        self.ui.tableWidgetGeoParams.clear()
        self.ui.tableWidgetGeoParams.setColumnCount(2)
        self.ui.tableWidgetGeoParams.setHorizontalHeaderLabels(['parameter', 'value'])
        self.ui.tableWidgetGeoParams.setRowCount(len(kwarg_str_list)-2)
        self.ui.tableWidgetGeoParams.setToolTip(inspect.getdoc(self.geo_type))
        i_row = 0
        for i, kwstr in enumerate(kwarg_str_list):
            kwstr = kwstr.split('=')[0]
            if kwstr not in ['step', 'mesh']:
                item = QtWidgets.QTableWidgetItem()
                item.setText(kwstr)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidgetGeoParams.setItem(i_row, 0, item)
                default = signature(self.geo_type).parameters[kwstr].default
                if default != inspect._empty:
                    ## default value
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(str(default))
                    self.ui.tableWidgetGeoParams.setItem(i_row, 1, item)
                i_row += 1
    
    
    def on_click_gen_geo(self):
        ## --- material instance
        kwargs = dict()
        for row in range(self.ui.tableWidgetMaterialParams.rowCount()):
            key = self.ui.tableWidgetMaterialParams.item(row, 0).text()
            val = self.ui.tableWidgetMaterialParams.item(row, 1).text()
            
            default = signature(self.geo_material).parameters[key].default
            if default != inspect._empty:
                val = type(default)(val)
            else:
                try:
                    val = float(val)
                except ValueError:
                    val = str(val)
                    
            kwargs[key] = val
        # print (kwargs)
        material = self.geo_material(**kwargs)
        
        
        ## --- generate geometry
        kwargs = dict()
        for row in range(self.ui.tableWidgetGeoParams.rowCount()):
            key = self.ui.tableWidgetGeoParams.item(row, 0).text()
            val = self.ui.tableWidgetGeoParams.item(row, 1).text()
            
            default = signature(self.geo_type).parameters[key].default
            if default != inspect._empty:
                val = type(default)(val)
            else:
                try:
                    val = float(val)
                except ValueError:
                    val = str(val)
                    
            kwargs[key] = val
        
        
        kwargs['step'] = float(self.ui.lineEditStep.text())
        kwargs['mesh'] = self.ui.comboBoxMesh.currentText()
        self.step = kwargs['step']
        self.mesh = kwargs['mesh']
        self.n1 = complex(self.ui.lineEditN1.text())
        self.n2 = complex(self.ui.lineEditN2.text())
        self.n3 = complex(self.ui.lineEditN3.text())
        self.spacing = float(self.ui.lineEditSpacing.text())
        # print (kwargs)
        
        self.geo = self.geo_type(**kwargs)
        self.geo.T[2] += self.step/2.
        
        self.geolist.append(self.geo)
        self.subgeotypelist.append(self.geo_type)
        self.materialslist.append([material]*len(self.geo))
        
        item = QtWidgets.QListWidgetItem("{} (Ndp={}, mat={})".format(
                                        self.geo_type.__name__, len(self.geo), 
                                        self.geo_material.__name__))
        self.ui.listWidgetStructures.addItem(item)
        
        ## --- instantiate `struct` class
        self.gen_full_structure()
        
        
        
    def gen_full_structure(self, reset_view=True, savestruct=True):
        if self.geolist:
            geo_all = np.concatenate(self.geolist)
            mat_all = np.concatenate(self.materialslist)
        
            self.struct_full = structures.struct(self.step, geo_all, mat_all, 
                                                 auto_shift_structure=False)
            
            ## --- visu
            mat_labels = self.ui.checkBoxGeoMaterialLabels.checkState()
            self.ui.mayaviWidgetGeo.visualization.plot_struct(self.struct_full, 
                                      axis_labels=True, material_labels=mat_labels, 
                                      reset_view=reset_view)
            self.on_select_struct_constituent()
            
            ## --- autosave
            if savestruct:
                self.save_struct("__autosave_struct_tmp.pkl.pygdmstruct")
            
            ## --- statusbar message
            if len(self.struct_full.geometry) <= 500:
                sim_speed = 'Very fast simulation speed expected.'
            elif 500 < len(self.struct_full.geometry) <= 1500:
                sim_speed = 'Fast simulation speed expected.'
            elif 1500 < len(self.struct_full.geometry) <= 3000:
                sim_speed = 'Moderate simulation speed expected.'
            elif 3000 < len(self.struct_full.geometry) <= 6000:
                sim_speed = 'Slow simulation speed expected.'
            elif 6000 < len(self.struct_full.geometry) <= 10000:
                sim_speed = 'Very slow simulation speed expected.'
            elif 10000 < len(self.struct_full.geometry) <= 15000:
                sim_speed = 'Insanely slow simulation speed expected.'
            else:
                sim_speed = 'Too many meshcells! Run at own risk!'
            self.statusBar().showMessage('Model: {} meshpoints. {}'.format(len(self.struct_full.geometry), sim_speed))
        else:
            self.struct_full = None
            ## --- clear mayavi visu
            self.ui.mayaviWidgetGeo.visualization.update_plot()
    
    
    def geo_apply_offset(self, offset):
        i_geo = int(self.ui.listWidgetStructures.currentRow())
        if i_geo >= 0:
            DX = offset[0]
            DY = offset[1]
            DZ = offset[2]
            self.geolist[i_geo].T[0] += self.step * DX
            self.geolist[i_geo].T[1] += self.step * DY
            self.geolist[i_geo].T[2] += self.step * DZ
            
            self.gen_full_structure(reset_view=False)
    
    def on_click_offset_geo(self):
        DX = float(self.ui.lineEditOffsetX.text())
        DY = float(self.ui.lineEditOffsetY.text())
        DZ = float(self.ui.lineEditOffsetZ.text())
        
        self.geo_apply_offset([DX, DY, DZ])
    
    
    def geo_apply_rotation(self, offset):
        i_geo = int(self.ui.listWidgetStructures.currentRow())
        if i_geo >= 0:
            rotX = offset[0]
            rotY = offset[1]
            rotZ = offset[2]
            if rotX != 0:
                self.geolist[i_geo] = structures.rotate(
                                self.geolist[i_geo], alpha=rotX, axis='x')
            if rotY != 0:
                self.geolist[i_geo] = structures.rotate(
                                self.geolist[i_geo], alpha=rotY, axis='y')
            if rotZ != 0:
                self.geolist[i_geo] = structures.rotate(
                                self.geolist[i_geo], alpha=rotZ, axis='z')
            
            self.gen_full_structure(reset_view=False)
    
    def on_click_rotate_geo(self):
        DX = float(self.ui.lineEditOffsetX.text())
        DY = float(self.ui.lineEditOffsetY.text())
        DZ = float(self.ui.lineEditOffsetZ.text())
        
        self.geo_apply_rotation([DX, DY, DZ])
            
    
    
    def on_click_del_geo(self):
        i_geo = int(self.ui.listWidgetStructures.currentRow())
        
        ## remove from list widget
        listItems = self.ui.listWidgetStructures.selectedItems()
        for item in listItems:
           self.ui.listWidgetStructures.takeItem(self.ui.listWidgetStructures.row(item))
        
        ## remove from geometries
        del self.subgeotypelist[i_geo]
        del self.geolist[i_geo]
        del self.materialslist[i_geo]
        
        if self.select_geo_mayaviobj is not None:
                self.select_geo_mayaviobj.remove()
        self.select_geo_mayaviobj = None
        self.gen_full_structure()
        
    
    
    def on_click_clear_geo(self, show_dialog=True):
        if show_dialog:
            reply = QtWidgets.QMessageBox.question(self, 'Confirm', 
                             "Sure?", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        else:
            reply = QtWidgets.QMessageBox.Yes
        
        if reply == QtWidgets.QMessageBox.Yes:
            ## unselect structure-list items before clear
            self.ui.listWidgetStructures.clearSelection()
            
            self.subgeotypelist = []
            self.geolist = []
            self.materialslist = []
            if self.select_geo_mayaviobj is not None:
                self.select_geo_mayaviobj.remove()
            self.select_geo_mayaviobj = None
            self.ui.listWidgetStructures.clear()
            self.gen_full_structure(savestruct=False)
        else:
            pass
    
    def on_select_struct_constituent(self):
        mat_labels = self.ui.checkBoxGeoMaterialLabels.checkState()
        self.ui.mayaviWidgetGeo.visualization.plot_struct(self.struct_full, 
                                  axis_labels=False, material_labels=mat_labels,
                                  clearfig=True, reset_view=False)
        
        i_geo = int(self.ui.listWidgetStructures.currentRow())
        if i_geo >= 0 and i_geo < self.ui.listWidgetStructures.count():
            substruct = self.geolist[i_geo]
            if self.select_geo_mayaviobj is not None:
                self.select_geo_mayaviobj.remove()
            
            self.select_geo_mayaviobj = self.ui.mayaviWidgetGeo.visualization.plot_struct(
                            substruct, scale=1.15, draw_substrate=False,
                            color=(0,0,1), opacity=0.10,
                            axis_labels=True, clearfig=False, reset_view=False)

    def on_click_geo_mat_lables(self):
        self.on_select_struct_constituent()





#%% simulation tab
# =============================================================================
#     simulation / internal fields
# =============================================================================
    def on_select_field(self):
        i_field = self.ui.comboBoxFieldGen.currentIndex()
        self.field_gen = fields.FIELDS_LIST[i_field]
        kwarg_str_list = str(signature(self.field_gen))[1:-1].split(', ')
        self.ui.tableWidgetFieldParams.clear()
        self.ui.tableWidgetFieldParams.setColumnCount(4)
        self.ui.tableWidgetFieldParams.setHorizontalHeaderLabels(['param.', 'min', 'max', 'N'])
        self.ui.tableWidgetFieldParams.setRowCount(len(kwarg_str_list)-3)
        self.ui.tableWidgetFieldParams.setToolTip(inspect.getdoc(self.field_gen))
        i_row = 0
        for i, kwstr in enumerate(kwarg_str_list):
            kwstr = kwstr.split('=')[0]
            if kwstr not in ['wavelength', 'pos', 'env_dict', 'returnField', '**kwargs', '']:
                item = QtWidgets.QTableWidgetItem()
                item.setText(kwstr)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidgetFieldParams.setItem(i_row, 0, item)
                default = signature(self.field_gen).parameters[kwstr].default
                if default != inspect._empty:
                    ## default value
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(str(default))
                    self.ui.tableWidgetFieldParams.setItem(i_row, 1, item)
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(str(default))
                    self.ui.tableWidgetFieldParams.setItem(i_row, 2, item)
                    ## by default: N = 1
                    item = QtWidgets.QTableWidgetItem()
                    item.setText("1")
                    self.ui.tableWidgetFieldParams.setItem(i_row, 3, item)
                i_row += 1
        header = self.ui.tableWidgetFieldParams.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        for i in range(1, 4):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)


    def gen_sim_instance(self):
        ## --- setup field generator config
        kwargs = dict()
        for row in range(self.ui.tableWidgetFieldParams.rowCount()):
            if self.ui.tableWidgetFieldParams.item(row, 0) is not None:
                key = self.ui.tableWidgetFieldParams.item(row, 0).text()
                val1 = self.ui.tableWidgetFieldParams.item(row, 1).text()
                val2 = self.ui.tableWidgetFieldParams.item(row, 2).text()
                N = int(self.ui.tableWidgetFieldParams.item(row, 3).text())
                
                
                default = signature(self.field_gen).parameters[key].default
                # print(row, self.ui.tableWidgetFieldParams.rowCount(), type(default))
                if type(default) == bool:
                    val = False if (val1.lower()=="false" or val1==0) else True
                elif type(default) == str:
                    val = str(val1)
                elif default != inspect._empty and default is not None:
                    val1 = type(default)(val1)
                    val2 = type(default)(val2)
                    val = np.linspace(val1, val2, N)
                elif default is None and val1.lower()=='none':
                    val = None
                else:
                    try:
                        val1 = float(val1)
                        if N>1:
                            val2 = float(val2)
                            val = np.linspace(val1, val2, N)
                        else:
                            val = val1
                    except ValueError:
                        val = str(val1)  # ignore second value if not a number
                # print(val, default, val is not default, val != default)
                if val is not default:
                    kwargs[key] = val
        # print (kwargs)
        wl0 = float(self.ui.lineEditWl0.text())
        wl1 = float(self.ui.lineEditWl1.text())
        Nwl = int(self.ui.lineEditNwl.text())
        self.wavelengths = np.linspace(wl0, wl1, Nwl)
        self.efield = fields.efield(self.field_gen, self.wavelengths, kwargs)
        
        self.sim = core.simulation(self.struct_full, self.efield, self.dyads)
        
        
    def clear_simulation(self):
        self.sim = None
        self.ui.listWidgetAvailableWavelengths.clear()
        self.ui.listWidgetAvailableFieldConfigs.clear()
        self.ui.plainTextEditSelectedConfig.clear()
        self.ui.textEditSimStatus.clear()
        

    def on_click_run_sim(self):
        reply = QtWidgets.QMessageBox.question(self, 'Confirm', 
                         "Sure? This will delete any unsaved simulation results.", 
                         QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No, 
                         QtWidgets.QMessageBox.Yes)
        # else:
        #     reply = QtWidgets.QMessageBox.Yes
        
        if reply == QtWidgets.QMessageBox.Yes:
            self.sim_finished = False
            self.clear_simulation()
            self.gen_sim_instance()
            
            self.simRunThread.set_sim(self.sim)
            method = self.ui.comboBoxInversionMethod.currentText()
            calcH = self.ui.checkBoxCalcH.checkState()
            self.simRunThread.set_method(method=method, calcH=calcH)
            self.simRunThread.start()
            
            msg = tools.print_sim_info(self.sim, prnt=False)
            self.ui.textEditSimStatus.append("Starting simulation\n" + msg + '\n\n\n')
            self.ui.pushButtonCancelSim.setDisabled(False)
            
            self.load_field_config_and_wl_lists(wavelengths=False)
    
    

                
    
    
    def on_click_cancel_sim(self):
        self.sigCancelSim.emit()
        self.sim_finished = False
        
        
    def on_simulation_status(self, status_dict):
        percent_done = int(100*((status_dict['i_wl']+1) / len(self.sim.efield.wavelengths)))
        msg = "{}%: {:.1f}nm ({}ms)".format(percent_done, status_dict['wavelength'], 
                            int(status_dict['t_inverse']+status_dict['t_repropa']))
        self.ui.textEditSimStatus.append(msg)
        
        item = QtWidgets.QListWidgetItem("{:.2f}nm".format(status_dict['wavelength']))
        self.ui.listWidgetAvailableWavelengths.addItem(item)
        
        self.sim = status_dict['sim']
        
        if status_dict['i_wl']==0:
            ## init structure plot
            self.ui.mayaviWidgetNF.visualization.plot_struct(self.struct_full, 
                                                 clearfig=True, reset_view=True)
            self.ui.listWidgetAvailableFieldConfigs.setCurrentRow(0)
            self.ui.listWidgetAvailableWavelengths.setCurrentRow(0)
        if self.ui.checkBoxUpdateLatest.checkState():
            self.ui.listWidgetAvailableWavelengths.setCurrentRow(status_dict['i_wl'])
            
        self.ui.progressBarSim.setValue(percent_done)
        
    
    def on_simulation_finished(self, sim):
        self.sim = sim
        self.sim_finished = True
        self.ui.pushButtonCancelSim.setEnabled(False)
        
        
    def on_click_select_sim_config(self):
        i_wl = int(self.ui.listWidgetAvailableWavelengths.currentRow())
        i_conf = int(self.ui.listWidgetAvailableFieldConfigs.currentRow())
        if i_conf >= 0 and i_wl >= 0 and self.sim is not None:
            ## --- show selected config parameters
            msg = 'wavelength: {:.2f}nm\n'.format(self.sim.efield.wavelengths[i_wl])
            
            for param in self.sim.efield.kwargs_permutations[i_conf]:
                msg += "'{}': {}\n".format(
                    param, str(self.sim.efield.kwargs_permutations[i_conf][param]))
            
            self.ui.plainTextEditSelectedConfig.clear()
            self.ui.plainTextEditSelectedConfig.insertPlainText(msg)
            if self.ui.radioButtonE.isChecked():
                plot_field = 'E'
            else:
                plot_field = 'H'

            ## --- load internal fields into visualization
            search_kwargs = copy.deepcopy(self.sim.efield.kwargs_permutations[i_conf])
            search_kwargs['wavelength'] = self.sim.efield.wavelengths[i_wl]
            f_idx = tools.get_closest_field_index(self.sim, search_kwargs)
            self.selected_fieldidx = f_idx
            
            ## update 2D visu
            self.ui.widgetMPL_2dNF_XY.canvas.fig.clear()
            ax = self.ui.widgetMPL_2dNF_XY.canvas.ax = self.ui.widgetMPL_2dNF_XY.canvas.fig.add_subplot(111)
            visu.vectorfield_by_fieldindex(self.sim, f_idx, ax=ax, tit='XY',
                                           projection='XY', which_field=plot_field, show=False)
            self.ui.widgetMPL_2dNF_XY.canvas.draw()
            
            self.ui.widgetMPL_2dNF_XZ.canvas.fig.clear()
            ax = self.ui.widgetMPL_2dNF_XZ.canvas.ax = self.ui.widgetMPL_2dNF_XZ.canvas.fig.add_subplot(111)
            visu.vectorfield_by_fieldindex(self.sim, f_idx, ax=ax, tit='XZ', 
                                           projection='XZ', which_field=plot_field, show=False)
            self.ui.widgetMPL_2dNF_XZ.canvas.draw()
            
            self.ui.widgetMPL_2dNF_YZ.canvas.fig.clear()
            ax = self.ui.widgetMPL_2dNF_YZ.canvas.ax = self.ui.widgetMPL_2dNF_YZ.canvas.fig.add_subplot(111)
            visu.vectorfield_by_fieldindex(self.sim, f_idx, ax=ax, tit='YZ',
                                           projection='YZ', which_field=plot_field, show=False)
            self.ui.widgetMPL_2dNF_YZ.canvas.draw()
            
            
            ## update 3D visu
            scale = float(self.ui.lineEditAnimateIntFieldScale.text())
            cycle_moment = float(self.ui.horizontalSliderPlotMomentOpticalCycleIntField.value())
            self.ui.mayaviWidgetNF.visualization.plot_struct(self.sim.struct, 
                                      axis_labels=False, scale=0.5, opacity=0.075,
                                      clearfig=True, reset_view=False)
            # self.ui.mayaviWidgetNF.visualization.plot_field(self.sim, field_index=f_idx, 
            #                              clearfig=False, reset_view=False)
            self.ui.mayaviWidgetNF.visualization.init_field_dat(self.sim, field_index=f_idx, 
                                        scale=3.5*scale, cycle_moment=cycle_moment, 
                                        clim=[-0.2, 0.9], mode='arrow', which_field=plot_field,
                                        clearfig=False, reset_view=False)
            
            
        
    def on_click_quickload_sim(self):
        reply = QtWidgets.QMessageBox.question(self, 'Confirm', 
                         "Sure? This will delete any unsaved simulation results.", 
                         QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No, 
                         QtWidgets.QMessageBox.Yes)
        
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                self.load_sim("__quicksave.pygdmsim")
            except:
                pass
        
    
    def on_click_toggle_animation(self):
        if self.AnimateIntFieldTimer.isActive():
            self.AnimateIntFieldTimer.stop()
            self.ui.horizontalSliderPlotMomentOpticalCycleIntField.sliderReleased.connect(self.on_click_select_sim_config)
        else:
            self.ui.horizontalSliderPlotMomentOpticalCycleIntField.sliderReleased.disconnect()
            fps = float(self.ui.lineEditAnimateIntFieldfps.text())
            self.AnimateIntFieldTimer.start(1000 / fps)
        
    def update_animation_intfield(self):
        self.ui.mayaviWidgetNF.visualization.animate_field_next_step()
        slider_pos = int(100 * self.ui.mayaviWidgetNF.visualization.i_cur_frame / 
                         self.ui.mayaviWidgetNF.visualization.Nframes)
        self.ui.horizontalSliderPlotMomentOpticalCycleIntField.setValue(slider_pos)
        
        
    



#%% spectra tab
# =============================================================================
#     spectra
# =============================================================================
    def on_click_select_spectra_func(self):
        i_func = int(self.ui.listWidgetAvailableSpectraFuncs.currentRow())
        if i_func >= 0:
            self.spectra_func = spectra_func[i_func]
            ## populate config table
            self.ui.tableWidgetSpectraFuncConfig.clear()
            self.ui.tableWidgetSpectraFuncConfig.setColumnCount(2)
            self.ui.tableWidgetSpectraFuncConfig.setHorizontalHeaderLabels(['parameter', 'value'])
            self.ui.tableWidgetSpectraFuncConfig.setRowCount(len(self.spectra_func['config']))
            self.ui.tableWidgetSpectraFuncConfig.setToolTip(inspect.getdoc(self.spectra_func['func']))
            for i, kwstr in enumerate(self.spectra_func['config']):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(kwstr))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidgetSpectraFuncConfig.setItem(i, 0, item)
                
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(self.spectra_func['config'][kwstr]))
                self.ui.tableWidgetSpectraFuncConfig.setItem(i, 1, item)
            header = self.ui.tableWidgetSpectraFuncConfig.horizontalHeader()
            for i in range(2):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
            ## -- no config:
            if len(self.spectra_func['config']) == 0:
                self.ui.tableWidgetSpectraFuncConfig.setRowCount(1)
                self.ui.tableWidgetSpectraFuncConfig.setColumnCount(1)
                item = QtWidgets.QTableWidgetItem()
                item.setText("no config")
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidgetSpectraFuncConfig.setItem(0, 0, item)
                
                
    
    def on_click_calc_spectrum(self):
        i_conf = int(self.ui.listWidgetAvailableFieldConfigs.currentRow())
        i_func = int(self.ui.listWidgetAvailableSpectraFuncs.currentRow())
        if i_conf >= 0 and i_func >= 0 and self.sim_finished:
            ## assemble kwargs for function
            kwargs = copy.deepcopy(self.spectra_func["fix_kwargs"])
            for row in range(self.ui.tableWidgetSpectraFuncConfig.rowCount()):
                key = self.ui.tableWidgetSpectraFuncConfig.item(row, 0).text()
                if str(key) != 'no config':
                    val = self.ui.tableWidgetSpectraFuncConfig.item(row, 1).text()
                    try:
                        val = float(val)
                    except ValueError:
                        val = str(val)
                    kwargs[key] = val
            # print (kwargs)
            if 'x' in kwargs.keys() and 'y' in kwargs.keys() and 'z' in kwargs.keys():
                kwargs["r_probe"] = np.array([kwargs['x'], kwargs['y'], kwargs['z']])
                del kwargs['x']
                del kwargs['y']
                del kwargs['z']
            wl, spec = tools.calculate_spectrum(self.sim, i_conf, 
                                                self.spectra_func["func"], 
                                                callback=self.on_spectrum_status,
                                                **kwargs)
            
            if self.spectra_func['postprocess'] is not None:
                spec = self.spectra_func['postprocess'](spec)
            
            self.do_plot_spectrum(wl, spec, self.spectra_func)
            self.spec = spec
    
    
    def on_spectrum_status(self, status_dict):
        # dict-keys: 'spectrum' (values), 'wavelengths'
        percent_done = int(100*len(status_dict['wavelengths']) / len(self.sim.efield.wavelengths))
        self.ui.progressBarRasterscan.setValue(percent_done)
        return(True)   # continue: True
    
    
    def do_plot_spectrum(self, wl, spec, f_dict):
        canvas = self.ui.widgetMPLspectrum.canvas
        
        if (self.ui.checkBoxSepPlotsSpectra.checkState() or len(canvas.fig.get_axes())>1 or 
                    self.ui.checkBoxClearPlotsSpectra.checkState()):
            canvas.fig.clear()
            self.i_spec_plot_color = 0
            
        colors = ["C{}".format(i) for i in range(10)]
        
        if not self.ui.checkBoxSepPlotsSpectra.checkState() and len(canvas.fig.get_axes())==0:
            ax = canvas.ax = canvas.fig.add_subplot(1,1,1)
        elif len(canvas.fig.get_axes())==1:
            ax = canvas.ax
        
        for i in range(len(spec)):
            if self.ui.checkBoxSepPlotsSpectra.checkState():
                ax = canvas.ax = canvas.fig.add_subplot(f_dict['plot_layout'][0], 
                                                        f_dict['plot_layout'][1], 
                                                        i+1)
                label = ''
                ax.set_title(f_dict['results_titles'][i])
            else:
                label = f_dict['results_titles'][i]
                
            ax.plot(wl, spec[i], color=colors[self.i_spec_plot_color], label=label)
            ax.set_xlabel("wavelength (nm)")
            ax.set_ylabel(f_dict['results_yaxis'][i])
            self.i_spec_plot_color += 1
            if self.i_spec_plot_color> 9: 
                self.i_spec_plot_color=0
        
        if not self.ui.checkBoxSepPlotsSpectra.checkState():
            ax.legend()
        canvas.fig.tight_layout()
        canvas.draw()
            

    def on_click_save_spectrum(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save '{}' spectrum as txt".format(self.spectra_func['name']), "",
                                                  "text files (*.txt);;All Files (*)", options=options)
        if filename:
            if '.' not in os.path.basename(filename):
                filename += ".spectrum.txt"
            spec_save_dat = np.concatenate([self.sim.efield.wavelengths[None, :], self.spec])
            header = "wavelength (nm)" + ''.join([s+', ' for s in self.spectra_func['results_yaxis']])
            np.savetxt(filename, spec_save_dat.T, fmt='%.5g', header=header)



#%% mapping tab
# =============================================================================
#     mapping
# =============================================================================
    def on_click_select_mapping_func(self):
        i_func = int(self.ui.listWidgetAvailableMappingFuncs.currentRow())
        if i_func >= 0:
            self.mapping_func = derived_maps_func[i_func]
            ## populate config table
            self.ui.tableWidgetMappingFuncConfig.clear()
            self.ui.tableWidgetMappingFuncConfig.setColumnCount(2)
            self.ui.tableWidgetMappingFuncConfig.setHorizontalHeaderLabels(['parameter', 'value'])
            self.ui.tableWidgetMappingFuncConfig.setRowCount(len(self.mapping_func['config']))
            self.ui.tableWidgetMappingFuncConfig.setToolTip(inspect.getdoc(self.mapping_func['func']))
            for i, kwstr in enumerate(self.mapping_func['config']):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(kwstr))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidgetMappingFuncConfig.setItem(i, 0, item)
                
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(self.mapping_func['config'][kwstr]))
                self.ui.tableWidgetMappingFuncConfig.setItem(i, 1, item)
            header = self.ui.tableWidgetMappingFuncConfig.horizontalHeader()
            for i in range(2):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
            ## -- no config:
            if len(self.mapping_func['config']) == 0:
                self.ui.tableWidgetMappingFuncConfig.setRowCount(1)
                self.ui.tableWidgetMappingFuncConfig.setColumnCount(1)
                item = QtWidgets.QTableWidgetItem()
                item.setText("no config")
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidgetMappingFuncConfig.setItem(0, 0, item)
    
    def on_click_calc_mapping(self):
        i_wl = int(self.ui.listWidgetAvailableWavelengths.currentRow())
        i_conf = int(self.ui.listWidgetAvailableFieldConfigs.currentRow())
        i_func = int(self.ui.listWidgetAvailableMappingFuncs.currentRow())
        if i_conf >= 0 and i_func >= 0 and i_wl >= 0 and self.sim_finished:
            ## assemble kwargs for function
            kwargs = copy.deepcopy(self.mapping_func["fix_kwargs"])
            x_range = []
            y_range = []
            z_range = []
            for row in range(self.ui.tableWidgetMappingFuncConfig.rowCount()):
                key = self.ui.tableWidgetMappingFuncConfig.item(row, 0).text()
                if str(key) != 'no config':
                    val = self.ui.tableWidgetMappingFuncConfig.item(row, 1).text()
                    try:
                        val = float(val)
                    except ValueError:
                        val = str(val)
                    if key in ["x0", "x1", "NX"]:
                        x_range.append(val)
                    elif key in ["y0", "y1", "NY"]:
                        y_range.append(val)
                    elif key in ["z0", "z1", "NZ"]:
                        z_range.append(val)
                    else:
                        kwargs[key] = val
            if self.mapping_func["input_type"] == 'r_probe':
                ## -- 1D cases
                if x_range[2] > 0 and y_range[2] == 0 and z_range[2] == 0:
                    r_probe = gen_linescan_mapping1d(x_range, y_range, z_range, lineaxis='x')
                    projection = 'x'
                elif x_range[2] == 0 and y_range[2] > 0 and z_range[2] == 0:
                    r_probe = gen_linescan_mapping1d(x_range, y_range, z_range, lineaxis='y')
                    projection = 'y'
                elif x_range[2] == 0 and y_range[2] == 0 and z_range[2] > 0:
                    r_probe = gen_linescan_mapping1d(x_range, y_range, z_range, lineaxis='z')
                    projection = 'z'
                ## -- 2D cases
                elif x_range[2] > 0 and y_range[2] > 0 and z_range[2] == 0:
                    r_probe = tools.generate_NF_map(*(x_range+y_range), Z0=z_range[0], projection='xy')
                    projection = 'xy'
                elif x_range[2] > 0 and y_range[2] == 0 and z_range[2] > 0:
                    r_probe = tools.generate_NF_map(*(x_range+z_range), Z0=y_range[0], projection='xz')
                    projection = 'xz'
                elif x_range[2] == 0 and y_range[2] > 0 and z_range[2] > 0:
                    r_probe = tools.generate_NF_map(*(y_range+z_range), Z0=x_range[0], projection='yz')
                    projection = 'yz'
                else:
                    raise ValueError("Invalid input. 1D or 2D mapping required, seem to got 3D range.")
                kwargs["r_probe"] = r_probe
                self.map_r_probe = r_probe
                self.map_projection = projection
            
            ## --- load internal fields into visualization
            map_dat = self.mapping_func["func"](self.sim, self.selected_fieldidx, **kwargs)
            
            if self.mapping_func['postprocess'] is not None:
                map_dat = self.mapping_func['postprocess'](map_dat)
            
            self.map_dat = map_dat
            
            
            if self.mapping_func["input_type"] == 'r_probe':
                self.do_plot_mapping(r_probe, map_dat, projection, self.mapping_func)
            elif self.mapping_func["input_type"] == 'polar-2D':
                self.do_plot_mapping_polar2D(map_dat, self.mapping_func)
                

    def do_plot_mapping(self, r_probe, map_dat, projection, f_dict):
        self.mapping_save_dat = []
        canvas = self.ui.widgetMPLmapping.canvas
        
        if (self.ui.checkBoxSepPlotsMapping.checkState() or len(canvas.fig.get_axes())>1 or 
                    self.ui.checkBoxClearPlotsMapping.checkState()):
            canvas.fig.clear()
            self.i_mapping_plot_color = 0
        
        if not self.ui.checkBoxSepPlotsMapping.checkState() and len(canvas.fig.get_axes())==0:
            ax = canvas.ax = canvas.fig.add_subplot(1,1,1)
        elif len(canvas.fig.get_axes())==1:
            ax = canvas.ax
        
        colors = ["C{}".format(i) for i in range(10)]
        idx_1D = dict(x=0, y=1, z=2)
        polar = False
        for i, mapping in enumerate(map_dat):
            if self.ui.checkBoxSepPlotsMapping.checkState():
                ax = canvas.ax = canvas.fig.add_subplot(f_dict['plot_layout'][0], 
                                                        f_dict['plot_layout'][1], 
                                                        i+1, polar=polar)
            title = ''
            self.mapping_scan_title = ''
            ## --- 1D data
            if len(projection) == 1:
                label = f_dict['results_titles'][i]
                self.map_positions = r_probe.T[idx_1D[projection]]
                if len(mapping) == len(r_probe):
                        mapping = mapping.T
                ax.plot(r_probe.T[idx_1D[projection]], mapping[3], 
                        color=colors[self.i_mapping_plot_color], label=label)
                for k in idx_1D:
                    if k != projection:
                        title += "{}={:.1f}nm ".format(k, float(mapping[0][idx_1D[k]]))
                
                self.mapping_scan_title = title
                if self.mapping_save_dat == []:
                    self.mapping_save_dat.append(r_probe.T[idx_1D[projection]].astype(float))
                self.mapping_save_dat.append(mapping[3].astype(float))
                
                ax.set_title(f_dict['results_titles'][i] + ' - ' + title)
                ax.set_xlabel(projection + " (nm)")
                ax.set_ylabel(f_dict['results_yaxis'][i] + " (nm)")
                if not self.ui.checkBoxSepPlotsMapping.checkState():
                    ax.legend()
                
                self.i_mapping_plot_color += 1
                if self.i_mapping_plot_color> 9:
                    self.i_mapping_plot_color = 0
                    
            ## --- 2D data
            if len(projection) == 2:
                self.map_positions = mapping[0]
                im = visu.scalarfield(mapping, ax=ax, cmap='jet', show=0)
                cbar = canvas.fig.colorbar(im, ax=ax)
                cbar.set_label(f_dict['results_yaxis'][i])
                
                ## draw structure contour
                if self.ui.checkBoxMappingGeoContour.checkState():
                    visu.structure_contour(self.sim, color='w', 
                               ax=ax, show=0, projection=projection)
                    visu.structure_contour(self.sim, color='k', dashes=[2,2],
                               ax=ax, show=0, projection=projection)
                
                for k in idx_1D:
                    if k not in projection:
                        title += "{}={:.1f}nm ".format(k, float(np.real(mapping[0][idx_1D[k]])))

                self.mapping_scan_title = title
                if self.mapping_save_dat == []:
                    self.mapping_save_dat.append(np.real(mapping.T[:3]).astype(float))
                self.mapping_save_dat.append(np.real(mapping.T[3]).astype(float)[None, :])
                
                ax.set_title(f_dict['results_titles'][i] + ' - ' + title)
                ax.set_xlabel("{} (nm)".format(projection[0]))
                ax.set_ylabel("{} (nm)".format(projection[1]))
                ax.set_aspect("equal")
                ax.autoscale(tight=True)
        canvas.fig.tight_layout()
        canvas.draw()
        if len(projection) == 2:
            self.mapping_save_dat = np.concatenate(self.mapping_save_dat)
    
    
    def do_plot_mapping_polar2D(self, map_dat, f_dict):
        theta, phi, Is, It, I0 = map_dat
        self.mapping_save_dat = np.array([theta.flatten(), phi.flatten(), 
                                          Is.flatten(), It.flatten()], dtype=float)
        
        canvas = self.ui.widgetMPLmapping.canvas
        canvas.fig.clear()
        for i, I in enumerate([Is]):
            ax = canvas.ax = canvas.fig.add_subplot(f_dict['plot_layout'][0], 
                                                    f_dict['plot_layout'][1],
                                                    i+1, polar=True)
            
            im = visu.farfield_pattern_2D(theta, phi, I, ax=ax, show=0)
            cbar = canvas.fig.colorbar(im, ax=ax, shrink=0.4)
            
            cbar.set_label(f_dict['results_yaxis'][i])
            ax.set_title(f_dict['results_titles'][i])
            
        canvas.fig.tight_layout()
        canvas.draw()
        
        
    def on_click_save_mapping(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save '{}' mapping as txt".format(self.mapping_func['name']), "",
                                                  "text files (*.txt);;All Files (*)", options=options)
        if filename:
            if '.' not in os.path.basename(filename):
                filename += ".mapping.txt"
            # self.map_r_probe = r_probe
            # self.map_projection = projection
            if self.mapping_func["input_type"] == 'r_probe':
                if len(self.map_projection)==1:
                    header = "{} position (nm), ".format(self.map_projection) + ''.join([s+', ' for s in self.mapping_func['results_yaxis']])
                else:
                    header = "x,y,z position (nm), " + ''.join([s+', ' for s in self.mapping_func['results_yaxis']])
                header += '\n' + self.mapping_scan_title
                
            elif self.mapping_func["input_type"] == 'polar-2D': 
                header = "theta (rad), phi (rad), I_scat, I_tot"
            
            np.savetxt(filename, np.transpose(self.mapping_save_dat), fmt='%.5g', header=header)
            
        
        
#%% rasterscan tab
# =============================================================================
#     rasterscan
# =============================================================================
    def on_click_select_rasterscan_func(self):
        i_func = int(self.ui.listWidgetAvailableRasterscanFuncs.currentRow())
        if i_func >= 0:
            self.rasterscan_func = rasterscan_func[i_func]
            ## populate config table
            self.ui.tableWidgetRasterscanFuncConfig.clear()
            self.ui.tableWidgetRasterscanFuncConfig.setColumnCount(2)
            self.ui.tableWidgetRasterscanFuncConfig.setHorizontalHeaderLabels(['parameter', 'value'])
            self.ui.tableWidgetRasterscanFuncConfig.setRowCount(len(self.rasterscan_func['config']))
            self.ui.tableWidgetRasterscanFuncConfig.setToolTip(inspect.getdoc(self.rasterscan_func['func']))
            for i, kwstr in enumerate(self.rasterscan_func['config']):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(kwstr))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidgetRasterscanFuncConfig.setItem(i, 0, item)
                
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(self.rasterscan_func['config'][kwstr]))
                self.ui.tableWidgetRasterscanFuncConfig.setItem(i, 1, item)
            header = self.ui.tableWidgetRasterscanFuncConfig.horizontalHeader()
            for i in range(2):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
            ## -- no config:
            if len(self.rasterscan_func['config']) == 0:
                self.ui.tableWidgetRasterscanFuncConfig.setRowCount(1)
                self.ui.tableWidgetRasterscanFuncConfig.setColumnCount(1)
                item = QtWidgets.QTableWidgetItem()
                item.setText("no config")
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidgetRasterscanFuncConfig.setItem(0, 0, item)


    def on_click_calc_rasterscan(self):
        i_conf = int(self.ui.listWidgetRasterscanFieldconfig.currentRow())
        i_func = int(self.ui.listWidgetAvailableRasterscanFuncs.currentRow())
        if i_conf >= 0 and i_func >= 0:
            ## assemble kwargs for function
            kwargs = copy.deepcopy(self.rasterscan_func["fix_kwargs"])
            for row in range(self.ui.tableWidgetRasterscanFuncConfig.rowCount()):
                key = self.ui.tableWidgetRasterscanFuncConfig.item(row, 0).text()
                if str(key) != 'no config':
                    val = self.ui.tableWidgetRasterscanFuncConfig.item(row, 1).text()
                    try:
                        val = float(val)
                    except ValueError:
                        val = str(val)
                    kwargs[key] = val
            # print (kwargs)
            if 'x' in kwargs.keys() and 'y' in kwargs.keys() and 'z' in kwargs.keys():
                kwargs["r_probe"] = np.array([kwargs['x'], kwargs['y'], kwargs['z']])
                del kwargs['x']
                del kwargs['y']
                del kwargs['z']
            coords, map_dat = tools.calculate_rasterscan(self.sim, i_conf, 
                                    self.rasterscan_func["func"], 
                                    callback=self.on_rasterscan_status, **kwargs)
            
            if self.rasterscan_func['postprocess'] is not None:
                map_dat = self.rasterscan_func['postprocess'](map_dat)
            
            self.do_plot_rasterscan(coords, map_dat, self.rasterscan_func)
            self.rasterscan_dat = [coords, map_dat]
            # visu.scalarfield(self.rasterscan_dat)
            

    def do_plot_rasterscan(self, coords, map_dat, f_dict):
        if len(np.unique(coords.T[0])) > 1 and len(np.unique(coords.T[1])) > 1: 
            projection = self.scanparam1_text[0] + self.scanparam2_text[0]
        elif len(np.unique(coords.T[0])) > 1:
            idx_1D = 0
            projection = self.scanparam1_text[0]
        elif len(np.unique(coords.T[1])) > 1:
            idx_1D = 1
            projection = self.scanparam2_text[0]
        else:
            raise ValueError("No rasterscan config found. The incident field " +
                             "must be configured for raster-scan at least " + 
                             "along one dimension!")
        self.rasterscan_projection = projection
        
        map_dat = np.nan_to_num(map_dat)
        
        canvas = self.ui.widgetMPLrasterscan.canvas
        if (self.ui.checkBoxSepPlotsRasterscan.checkState() or len(canvas.fig.get_axes())>1 or 
                    self.ui.checkBoxClearPlotsRasterscan.checkState()):
            canvas.fig.clear()
            self.i_rasterscan_plot_color = 0
            
        if not self.ui.checkBoxSepPlotsRasterscan.checkState() and len(canvas.fig.get_axes())==0:
            ax = canvas.ax = canvas.fig.add_subplot(1,1,1)
        elif len(canvas.fig.get_axes())==1:
            ax = canvas.ax
        
        colors = ["C{}".format(i) for i in range(10)]
        
        self.rasterscan_save_dat = []
        for i, mapping in enumerate(map_dat):
            if self.ui.checkBoxSepPlotsRasterscan.checkState():
                ax = canvas.ax = canvas.fig.add_subplot(f_dict['plot_layout'][0], 
                                                        f_dict['plot_layout'][1], 
                                                        i+1, polar=False)
            
            title = ' - {} {}D-scan'.format(projection.upper(), len(projection))
            ## --- 1D data
            if len(projection) == 1:
                label = f_dict['results_titles'][i]
                ax.plot(coords.T[idx_1D], mapping, color=colors[self.i_rasterscan_plot_color], label=label)
                
                ax.set_title(f_dict['results_titles'][i] + title)
                ax.set_xlabel(projection + " (nm)")
                ax.set_ylabel(f_dict['results_yaxis'][i] + " (nm)")
                self.i_rasterscan_plot_color += 1
                if self.i_rasterscan_plot_color> 9: 
                    self.i_rasterscan_plot_color=0
                    
                if not self.ui.checkBoxSepPlotsRasterscan.checkState():
                    ax.legend()
                    
                if self.rasterscan_save_dat == []:
                    self.rasterscan_save_dat.append(np.real(coords.T[idx_1D]).astype(float))
                self.rasterscan_save_dat.append(np.real(mapping).astype(float))
                
            ## --- 2D data
            if len(projection) == 2:
                im = visu.scalarfield([coords, mapping], ax=ax, cmap='jet', show=0)
                cbar = canvas.fig.colorbar(im, ax=ax)
                cbar.set_label(f_dict['results_yaxis'][i])
                
                ## draw structure contour
                if self.ui.checkBoxRasterscanGeoContour.checkState():
                    visu.structure_contour(self.sim, color='w', 
                               ax=ax, show=0)
                    visu.structure_contour(self.sim, color='k', dashes=[2,2],
                               ax=ax, show=0)
                
                ax.set_title(f_dict['results_titles'][i] + title)
                ax.set_xlabel("{} (nm)".format(projection[0]))
                ax.set_ylabel("{} (nm)".format(projection[1]))
                ax.set_aspect("equal")
                ax.autoscale(tight=True)
                
                if self.rasterscan_save_dat == []:
                    self.rasterscan_save_dat.append(np.real(coords.T).astype(float))
                self.rasterscan_save_dat.append(np.real(mapping).astype(float)[None, :])
                
        canvas.fig.tight_layout()
        canvas.draw()
        
        if len(projection) == 2:
            self.rasterscan_save_dat = np.concatenate(self.rasterscan_save_dat)


    def on_rasterscan_status(self, status_dict):
        percent_done = int(100*(status_dict['i_scan']+1) / status_dict['N_scan'])
        self.ui.progressBarRasterscan.setValue(percent_done)
        return(True)   # continue: True
    
    
    def on_click_save_rasterscan(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save '{}' rasterscan as txt".format(self.rasterscan_func['name']), "",
                                                  "text files (*.txt);;All Files (*)", options=options)
        if filename:
            if '.' not in os.path.basename(filename):
                filename += ".rasterscan.txt"
                header = "{} position (nm), ".format(self.rasterscan_projection) + ''.join(
                      [s+', ' for s in self.rasterscan_func['results_yaxis']])
            
            np.savetxt(filename, np.transpose(self.rasterscan_save_dat), fmt='%.5g', header=header)
        


# =============================================================================
# start GUI
# =============================================================================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApplication()
    window.resize(3000, 2000)
    # window.showMaximized()
    window.showNormal()
    sys.exit(app.exec_()) 
    
