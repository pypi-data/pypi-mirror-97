import os
import copy
import numpy as np

from pyGDM2 import tools
from pyGDM2 import linear
# from pyGDM2 import linear_py as linear    # use pure python API
from pyGDM2 import nonlinear



#%% spectra
# =============================================================================
# spectra
# =============================================================================
## dimensions: N_data, N_wl, DATA
def spec_add_single_axis(spec):
    spec = spec[None,:]    # add first axis: different results (here one)
    return spec
def spec_second_axis_first(spec):
    spec = np.moveaxis(spec, 1, 0)  # move different fields as first axis
    return spec
def spec_multipolemoment_norm(spec):
    # spec = np.moveaxis(spec, 1, 0)  # move different fields as first axis
    ## take norm of every element:
    new_spec = np.zeros((len(spec[0]), len(spec)))
    for i, wl in enumerate(spec):
        for j, datset_elem in enumerate(wl):
            new_spec[j,i] = np.linalg.norm(datset_elem)
    return new_spec
def spec_process_nf_intensity(spec):
    spec = np.squeeze(spec)         # remove empty axis
    spec = np.moveaxis(spec, 1, 0)  # move different fields as first axis
    spec = np.sum(np.abs(spec[:,:,3:])**2, axis=-1)   # last column: field intensity
    return spec



spectra_func = [
    dict(name='extinction', 
         func=linear.extinct, 
         config=dict(),
         fix_kwargs=dict(),
         postprocess=spec_second_axis_first,
         plot_layout=[3,1],
         results_titles=['extinction', 'scattering', 'absorption'],
         results_yaxis=['ext. cross section (nm^2)', 'scat. cross section (nm^2)', 'abs. cross section (nm^2)']),
    
    dict(name='farfield scattering', 
         func=linear.farfield, 
         config=dict(r=10000, tetamin=0, tetamax=np.pi/2,
                     Nteta=10, Nphi=36,
                     polarizerangle='none',
                     return_value='int_es'),
         fix_kwargs=dict(),
         postprocess=spec_add_single_axis,
         plot_layout=[1,1],
         results_titles=['farfield scattering'],
         results_yaxis=['scat. cross section (nm^2)']),
    
    dict(name='multipoles - extinction', 
         func=linear.multipole_decomp_extinct, 
         config=dict(),
         fix_kwargs=dict(quadrupoles=True),
         postprocess=spec_second_axis_first,
         plot_layout=[2,2],
         results_titles=['electric dipole', 'magnetic dipole', 'electric quadrupole', 'magnetic quadrupole'],
         results_yaxis=['ext. cross section (nm^2)']*4),
    
    dict(name='multipoles - moment magnitude', 
         func=linear.multipole_decomp,  #(Frobenius-norm for 3x3 qudrupole moments)
         config=dict(),
         fix_kwargs=dict(quadrupoles=True),
         postprocess=spec_multipolemoment_norm,
         plot_layout=[2,2],
         results_titles=['electric dipole', 'magnetic dipole', 'electric quadrupole', 'magnetic quadrupole'],
         results_yaxis=['norm of local multipole moment']*4),
    
    dict(name='nearfield intensity', 
         func=linear.nearfield, 
         config=dict(x=0, y=0, z=-50),
         fix_kwargs=dict(),
         postprocess=spec_process_nf_intensity,
         plot_layout=[2,2],
         results_titles=['scattered E', 'total E', 'scattered B', 'total B'],
         results_yaxis=['|E_s|^2 / |E0|^2', '|E_t|^2 / |E0|^2', '|B_s|^2 / |B0|^2', '|B_t|^2 / |B0|^2']),
    
    dict(name='nearfield optical chirality', 
         func=linear.optical_chirality, 
         config=dict(x=0, y=0, z=-50),
         fix_kwargs=dict(),
         postprocess=spec_add_single_axis,
         plot_layout=[1,1],
         results_titles=['nearfield optical chirality'],
         results_yaxis=['C / C_LCP']),
    
    dict(name='heat generation', 
          func=linear.heat, 
          config=dict(),
          fix_kwargs=dict(),
          postprocess=spec_add_single_axis,
          plot_layout=[1,1],
          results_titles=['heat generation'],
          results_yaxis=['deposited heat (nano Watt)']),
    
    dict(name='optical force', 
          func=linear.optical_force, 
          config=dict(),
          fix_kwargs=dict(),
          postprocess=spec_second_axis_first,
          plot_layout=[3,1],
          results_titles=['force along x', 'force along y', 'force along z'],
          results_yaxis=['F_x (a.u.)', 'F_z (a.u.)', 'F_z (a.u.)']),
    
    dict(name='local temperature increase', 
          func=linear.temperature, 
          config=dict(x=0, y=0, z=-50,
                      kappa_env=0.6,
                      kappa_subst=0.6),
          fix_kwargs=dict(),
          postprocess=spec_add_single_axis,
          plot_layout=[1,1],
          results_titles=['local temperature increase'],
          results_yaxis=['delta T (Kelvin)']),
    
    dict(name='TPL', 
          func=nonlinear.tpl_ldos, 
          config=dict(nonlin_order=2),
          fix_kwargs=dict(),
          postprocess=spec_add_single_axis,
          plot_layout=[1,1],
          results_titles=['two-photon photoluminescnec'],
          results_yaxis=['TPL (a.u.)']),
    ]




#%% mappings (for fixed illumination)
# =============================================================================
# mappings
# =============================================================================
def maps_add_single_axis(map_dat):
    map_dat = map_dat[None,:]    # add first axis: different results (here one)
    return map_dat
def maps_convert_theta_lowerBFP(map_dat):
    map_dat = list(map_dat)
    map_dat[0] = np.pi - map_dat[0]    # add first axis: different results (here one)
    return map_dat
def maps_NF_intensity(map_dat):
    map_dat = np.array(map_dat)         # remove empty axis
    map_dat_i = np.sum(np.abs(map_dat[:,:,3:])**2, axis=-1)   # last column: field intensity
    return np.concatenate([map_dat[:,:,:3], map_dat_i[...,None]], axis=-1)


def gen_linescan_mapping1d(x_range, y_range, z_range, lineaxis):
    N = int(max([x_range[2], y_range[2], z_range[2]]))
    xpos = np.ones(N) * x_range[0]
    ypos = np.ones(N) * y_range[0]
    zpos = np.ones(N) * z_range[0]
    
    if lineaxis.lower() == "x":
        line_pos = np.linspace(x_range[0], x_range[1], N)
        r_probe = np.transpose([line_pos, ypos, zpos])
    elif lineaxis.lower() == "y":
        line_pos = np.linspace(y_range[0], y_range[1], N)
        r_probe = np.transpose([xpos, line_pos, zpos])
    elif lineaxis.lower() == "z":
        line_pos = np.linspace(z_range[0], z_range[1], N)
        r_probe = np.transpose([xpos, ypos, line_pos])
    else:
        raise ValueError("Invalid lineaxis parameter!")
    return r_probe

default_NFmap_kwargs = dict(x0=-500, x1=500, NX=30,
                          y0=-500, y1=500, NY=30,
                          z0=-50, z1=0, NZ=0)
default_OCmap_kwargs = copy.deepcopy(default_NFmap_kwargs)
default_OCmap_kwargs["which_field"] = 't'

default_Tmap_kwargs = copy.deepcopy(default_NFmap_kwargs)
default_Tmap_kwargs["kappa_env"] = 0.6
default_Tmap_kwargs["kappa_subst"] = 0.6


derived_maps_func = [
    dict(name='nearfield intensity', 
         internal_name='nfi',
         input_type='r_probe',
         func=linear.nearfield, 
         config=default_NFmap_kwargs,
         fix_kwargs=dict(),
         postprocess=maps_NF_intensity,
         plot_layout=[2,2],
         results_titles=['scattered E', 'total E', 'scattered B', 'total B'],
         results_yaxis=['|E_s|^2 / |E0|^2', '|E_t|^2 / |E0|^2', '|B_s|^2 / |B0|^2', '|B_t|^2 / |B0|^2']),
    
    dict(name='nearfield optical chirality', 
         internal_name='oc',
         input_type='r_probe',
         func=linear.optical_chirality, 
         config=default_OCmap_kwargs,
         fix_kwargs=dict(),
         postprocess=maps_add_single_axis,
         plot_layout=[1,1],
         results_titles=['optical chiraliy C'],
         results_yaxis=['C / C_LCP']),
    
    dict(name='local temperature increase', 
         internal_name='DT',
         input_type='r_probe',
         func=linear.temperature, 
         config=default_Tmap_kwargs,
         fix_kwargs=dict(),
         postprocess=maps_add_single_axis,
         plot_layout=[1,1],
         results_titles=['local temperature increase'],
         results_yaxis=['Delta T (Kelvin)']),
    
    dict(name='farfield BFP - above', 
         internal_name='ff-BFP-up',
         input_type='polar-2D',
         func=linear.farfield, 
         config=dict(r=10000, Nteta=36, Nphi=36, polarizerangle='none'),
         fix_kwargs=dict(tetamin=0, tetamax=np.pi/2.),
         postprocess=None,
         plot_layout=[1,1],
         results_titles=['scattering'],
         results_yaxis=['|E_s|^2 / |E0|^2']),
    
    dict(name='farfield BFP - below', 
         internal_name='ff-BFP-down',
         input_type='polar-2D',
         func=linear.farfield, 
         config=dict(r=10000, Nteta=36, Nphi=36, polarizerangle='none'),
         fix_kwargs=dict(tetamin=np.pi/2., tetamax=np.pi),
         postprocess=maps_convert_theta_lowerBFP,
         plot_layout=[1,1],
         results_titles=['scattering'],
         results_yaxis=['|E_s|^2 / |E0|^2']),
    ]



#%% rasterscan (moving illumination)
# =============================================================================
# rasterscan
# =============================================================================
def rasterscan_add_single_axis(spec):
    spec = spec[None,:]    # add first axis: different results (here one)
    return spec
def rasterscan_second_axis_first(spec):
    spec = np.moveaxis(spec, 1, 0)  # move different fields as first axis
    return spec
def rasterscan_multipolemoment_norm(spec):
    # spec = np.moveaxis(spec, 1, 0)  # move different fields as first axis
    ## take norm of every element:
    new_spec = np.zeros((len(spec[0]), len(spec)))
    for i, wl in enumerate(spec):
        for j, datset_elem in enumerate(wl):
            new_spec[j,i] = np.linalg.norm(datset_elem)
    return new_spec
def rasterscan_process_nf_intensity(spec):
    spec = np.squeeze(spec)         # remove empty axis
    spec = np.moveaxis(spec, 1, 0)  # move different fields as first axis
    spec = np.sum(np.abs(spec[:,:,3:])**2, axis=-1)   # last column: field intensity
    return spec

rasterscan_func = [
    dict(name='extinction', 
         func=linear.extinct, 
         config=dict(),
         fix_kwargs=dict(),
         postprocess=rasterscan_second_axis_first,
         plot_layout=[3,1],
         results_titles=['extinction', 'scattering', 'absorption'],
         results_yaxis=['ext. cross section (nm^2)', 'scat. cross section (nm^2)', 'abs. cross section (nm^2)']),
    
    dict(name='farfield scattering', 
         func=linear.farfield, 
         config=dict(r=10000, tetamin=0, tetamax=np.pi/2,
                     Nteta=10, Nphi=36,
                     polarizerangle='none',
                     return_value='int_es'),
         fix_kwargs=dict(),
         postprocess=rasterscan_add_single_axis,
         plot_layout=[1,1],
         results_titles=['farfield scattering'],
         results_yaxis=['scat. cross section (nm^2)']),
    
    dict(name='multipoles - extinction', 
         func=linear.multipole_decomp_extinct, 
         config=dict(),
         fix_kwargs=dict(quadrupoles=True),
         postprocess=rasterscan_second_axis_first,
         plot_layout=[2,2],
         results_titles=['electric dipole', 'magnetic dipole', 'electric quadrupole', 'magnetic quadrupole'],
         results_yaxis=['ext. cross section (nm^2)']*4),
    
    dict(name='multipoles - moment magnitude', 
         func=linear.multipole_decomp,  #(Frobeniusnorm for 3x3 qudrupole moments)
         config=dict(),
         fix_kwargs=dict(quadrupoles=True),
         postprocess=rasterscan_multipolemoment_norm,
         plot_layout=[2,2],
         results_titles=['electric dipole', 'magnetic dipole', 'electric quadrupole', 'magnetic quadrupole'],
         results_yaxis=['norm of local multipole moment']*4),
    
    dict(name='nearfield intensity', 
         func=linear.nearfield, 
         config=dict(x=0, y=0, z=-50),
         fix_kwargs=dict(),
         postprocess=rasterscan_process_nf_intensity,
         plot_layout=[2,2],
         results_titles=['scattered E', 'total E', 'scattered B', 'total B'],
         results_yaxis=['|E_s|^2 / |E0|^2', '|E_t|^2 / |E0|^2', '|B_s|^2 / |B0|^2', '|B_t|^2 / |B0|^2']),
    
    dict(name='nearfield optical chirality', 
         func=linear.optical_chirality, 
         config=dict(x=0, y=0, z=-50),
         fix_kwargs=dict(),
         postprocess=rasterscan_add_single_axis,
         plot_layout=[1,1],
         results_titles=['nearfield optical chirality'],
         results_yaxis=['C / C_LCP']),
    
    dict(name='optical force', 
          func=linear.optical_force, 
          config=dict(),
          fix_kwargs=dict(),
          postprocess=rasterscan_second_axis_first,
          plot_layout=[1,3],
          results_titles=['force along x', 'force along y', 'force along z'],
          results_yaxis=['F_x (a.u.)', 'F_z (a.u.)', 'F_z (a.u.)']),
    
    dict(name='heat generation', 
          func=linear.heat, 
          config=dict(),
          fix_kwargs=dict(),
          postprocess=rasterscan_add_single_axis,
          plot_layout=[1,1],
          results_titles=['heat generation'],
          results_yaxis=['deposited heat (nano Watt)']),
    
    dict(name='local temperature increase', 
          func=linear.temperature, 
          config=dict(x=0, y=0, z=-50,
                      kappa_env=0.6,
                      kappa_subst=0.6),
          fix_kwargs=dict(),
          postprocess=rasterscan_add_single_axis,
          plot_layout=[1,1],
          results_titles=['local temperature increase'],
          results_yaxis=['delta T (Kelvin)']),
    
    dict(name='TPL', 
          func=nonlinear.tpl_ldos, 
          config=dict(nonlin_order=2),
          fix_kwargs=dict(),
          postprocess=rasterscan_add_single_axis,
          plot_layout=[1,1],
          results_titles=['two-photon photoluminescnec'],
          results_yaxis=['TPL (a.u.)']),
    ]

