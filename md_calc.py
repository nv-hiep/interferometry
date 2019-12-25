#!/usr/bin/env python
__author__ = 'Hiep Nguyen'
import os
import sys
import re
import glob
import numpy as np

## Get list of files #
 #
 # params str   dirpath   Path to directory
 #
 # return list files
 # 
 # Version 11/2019
 # Author Hiep Nguyen
 ##
def get_items(dirpath, ext='config'):
	files = glob.glob(dirpath + '*.' + ext)
	for i,x in enumerate(files):
		x = x.replace(dirpath, '')
		x = x.replace('.' + ext, '')
		files[i] = x

	files.sort()
	return files





## Read a config file #
 #
 # params str file   path to file
 #
 # return float rms
 #        1-D array v_fltr filtered vlsr 
 #        1-D array T_fltr filtered Tb 
 # 
 # Version 11/2019
 # Author Hiep Nguyen
 ##
def load_config(file):
	key_val_dict = {}
	east_coord   = []
	north_coord  = []
	
    # Compile necessary regular expressions
	spaces         = re.compile('\s+')
	comma_n_spaces = re.compile(',\s+')
	comment        = re.compile('#.*')
	quotes         = re.compile('\'[^\']*\'')
	key_val        = re.compile('^.+=.+')
	cols           = re.compile('^.+,.+')

	# Open the file and scan, line by line
	try:
		dat = open(file, "r")
	except Exception:
		print("Failed to open file '%s'." % file)
		return False
	for line in dat:
		line = line.rstrip("\n\r")
		if not comment.match(line):
			line = comment.sub('', line)           # internal comments 
			line = line.replace("'", '')           # remove quotes
			line = comma_n_spaces.sub(',', line)   # kill ambiguous spaces

			# Capture key=value pairs
			if key_val.match(line):
				keyword, value = line.split('=',1)
				value          = value.strip()              # kill ext whitespace 
				keyword        = keyword.strip()       
				value          = spaces.sub('', value)      # shrink int whitespace
				keyword        = spaces.sub('', keyword)    
				if value       :
					key_val_dict[keyword] = value

			# Capture antenna coordinate entries
			if cols.match(line):
				east, north = line.split(',')
				east_coord.append(east)
				north_coord.append(north)
	dat.close()

	# Number of antennas should be > 2
	if (len(east_coord) < 2) :
		print('Number of antennas should be > 2')
		sys.exit()
		return None


	# From Cormac -> Calculate the antenna coordinates in Earth-centred coordinate frame
	# Technically, we should have terms for the distance from the
	# centre of the Earth, but if the elevation is the same for all
	# antennas, these cancel out when calculating the baseline vectors.
	east_coord   = np.array(east_coord, dtype='f4')
	north_coord  = np.array(north_coord, dtype='f4')
	latitude_deg = float(key_val_dict.get('latitude_deg', 20.0))
	latitude_rad = np.radians(latitude_deg)
	x_m          = -north_coord*np.sin(latitude_rad)
	y_m          = east_coord
	z_m          = north_coord*np.cos(latitude_rad)

	ret = {}
	ret['telescope']     = key_val_dict.get('telescope', 'UNKNOWN')
	ret['config']        = key_val_dict.get('config', 'UNKNOWN')
	ret['latitude_deg']  = latitude_deg
	ret['latitude_rad']  = latitude_rad
	ret['diameter_m']    = float(key_val_dict.get('diameter_m', 22.0))
	ret['east_coord_m']  = east_coord
	ret['north_coord_m'] = north_coord
	ret['n_ant']         = int(len(ret['east_coord_m']))
	ret['n_base']        = int(ret['n_ant']*(ret['n_ant']-1)/2)
	ret['x_m']           = x_m
	ret['y_m']           = y_m
	ret['z_m']           = z_m
	
	Lx, Ly, Lz, base     = get_baselines(ret)
	
	ret['Lx_m']          = Lx
	ret['Ly_m']          = Ly
	ret['Lz_m']          = Lz
	ret['base']          = base
	
	ret['base_min']      = np.nanmin(base)
	ret['base_max']      = np.nanmax(base)

	return ret



## Calculate the baselines in metres from the antenna
 # coordinates in the Earth-centred system.
 #
 # params dict data   infor of the array
 #
 # return ???
 # 
 # Version 11/2019
 # Author Hiep Nguyen
 ##
def get_baselines(dat):
    Lx = np.zeros( (dat['n_base']) )
    Ly = np.zeros( (dat['n_base']) )
    Lz = np.zeros( (dat['n_base']) )

    # Loop through the unique antenna pairs
    n = 0
    for i in range(dat['n_ant']-1):
        for j in range(i+1, dat['n_ant']):
            Lx[n] = dat['x_m'][j] - dat['x_m'][i]
            Ly[n] = dat['y_m'][j] - dat['y_m'][i]
            Lz[n] = dat['z_m'][j] - dat['z_m'][i]
            n += 1

    # Calculate vector of baseline lengths
    base = np.sqrt(Lx**2.0 + Ly**2.0 + Lz**2.0)

    return Lx, Ly, Lz, base ## in meters





## Calc. the elevation curves for an array from source declination within a range of hour-angles
 #
 # params float   latitude_rad   Lattitude in radians
 # params list    ha_hr          starting and ending Hour-angles
 # params float   decl           Declination
 # params float   samp_rate      sampling rate in seconds
 #
 # return ???
 # 
 # Version 11/2019
 # Author Hiep Nguyen
 ##
def get_elevation_curve(latitude_rad, ha_hr, decl, samp_rate):
	samp_rate_hr                = samp_rate / 3600.0
	# samp_rate_deg              = samp_rate_hr * 15.0
	
	n_samp                      = int((ha_hr[1] - ha_hr[0])/samp_rate_hr + 1)
	
	ha_arr_hr                   = np.linspace(ha_hr[0], ha_hr[1], n_samp)
	ha_arr_rad                  = np.radians(ha_arr_hr * 15.0)
	
	dec_rad                     = np.radians(decl)
	
	el_arr_rad                  = (np.sin(latitude_rad) * np.sin(dec_rad) + np.cos(latitude_rad) * np.cos(dec_rad) * np.cos(ha_arr_rad))
	el_arr_deg                  = np.degrees(el_arr_rad)
	el_arr_deg[el_arr_deg < 0.] = 0.0
	
	return ha_arr_hr, el_arr_deg




## Calc. the elevation curves for an array from source declination within a range of hour-angles
 #
 # params dict data   infor of the array
 #
 # return ???
 # 
 # Version 11/2019
 # Author Hiep Nguyen
 ##
def get_uv_coverage(infor, decl, ha_arr_hr, el_arr_deg, lambda_m):
	dec_rad                      = np.radians( decl )
	latitude_rad                 = infor['latitude_rad']
	ha_arr_rad                   = np.radians(ha_arr_hr * 15.0)
	ha_arr_rad[el_arr_deg <= 0.] = np.nan
	nsamples                     = len(ha_arr_rad)

	u_m = np.zeros( (infor['n_base'], nsamples) )
	v_m = np.zeros( (infor['n_base'], nsamples) )
	for i in range(infor['n_base']):
	    u_m[i, :] = (infor['Lx_m'][i] * np.sin(ha_arr_rad) + 
	                 infor['Ly_m'][i] * np.cos(ha_arr_rad))
	    v_m[i, :] = (-infor['Lx_m'][i] * np.sin(dec_rad) *
	                 np.cos(ha_arr_rad) +
	                 infor['Ly_m'][i] * np.sin(dec_rad) *
	                 np.sin(ha_arr_rad) +
	                 infor['Lz_m'][i] * np.cos(dec_rad))
	u_arr_lda = u_m/lambda_m
	v_arr_lda = v_m/lambda_m

	# Calculate the max & min scales from the uv-coverage
	if np.all(ha_arr_rad != ha_arr_rad):
		scale_min_deg = np.nan
		scale_max_deg = np.nan
		pribeam_deg   = np.nan
	else:
	    xl_arr_lda = np.sqrt(u_arr_lda**2.0 + v_arr_lda**2.0)
	    scale_min_deg = np.degrees(1.0/np.nanmax(xl_arr_lda))
	    scale_max_deg = np.degrees(1.0/np.nanmin(xl_arr_lda))
	    pribeam_deg   = np.degrees(1.22*lambda_m/ infor['diameter_m'])

	return u_arr_lda, v_arr_lda






## Convert an angle in degrees to a unicode string with appropriate units.
 #
 # params float angle_deg   Angle in degree
 #
 # return ???
 # 
 # Version 11/2019
 # Author Cormac
 ##
def ang2str(angle_deg):
    """Convert an angle in degrees to a unicode string with appropriate units.
    """
    try:
        angle_deg = float(angle_deg)
        angle_arcsec = angle_deg*3600.0
        if angle_arcsec<60.0:
            text = u'{:.2f}"'.format(angle_arcsec)
        elif angle_arcsec>=60.0 and angle_arcsec<3600.0:
            text = u"{:.2f}'".format(angle_deg*60.0)
        else:
            text = u"{:.2f}\u00B0".format(angle_deg)
        return text
    except Exception:
        return ""







## Calculate the 2D Fast Fourier Transform of the model image.
 #
 # params dict data   infor of the array
 #
 # return ???
 # 
 # Version 11/2019
 # Author Hiep Nguyen
 ##
def invert_src_img(src_status, src_img_arr, pix_scale_img_asec, nx, ny):

	# First check that a model has been loaded
	if(not src_status):
	    print("A model image has not been loaded.")
	    sys.exit()

	# Calculate the 2D FFT and scaling factors.
	# The shape of FFT array is same as the model image.
	try:
		src_fft_arr        = np.fft.fft2(src_img_arr)
		src_fft_arr        = np.fft.fftshift(src_fft_arr)
		pix_scale_img_lam  = np.radians(pix_scale_img_asec/3600.0)
		fft_scale_lam      = 1.0/pix_scale_img_lam
		pix_scale_fftX_lam = 2.0*fft_scale_lam/nx
		pix_scale_fftY_lam = 2.0*fft_scale_lam/ny            
	except Exception:
		print("Failed to calculate the FFT of the model image.")
		sys.exit()

	# Print the model FFT parameters
	print ("\nModel FFT Parameters:")
	print(u"Pixel scale = %.3f x %.3f k\u03bb" % \
	      (pix_scale_fftX_lam/1000.0, pix_scale_fftY_lam/1000.0))
	print(u"Image limits = -%.3f to +%.3f k\u03bb" % \
	      (fft_scale_lam/1000.0, fft_scale_lam/1000.0))

	return src_fft_arr, pix_scale_img_lam, fft_scale_lam, pix_scale_fftX_lam, pix_scale_fftY_lam





## Grid the uv-coverage to use as a mask for the model FFT image
 #
 # params dict data   infor of the array
 #
 # return ???
 # 
 # Version 11/2019
 # Author Hiep Nguyen
 ##
def grid_uvcoverage(src_fft_status, uv_status, src_fft_arr,\
	fft_scale_lam, pix_scale_fftX_lam, pix_scale_fftY_lam,\
	u_arr_lda, v_arr_lda):

	# First check uv-coverage and model are available
	if(not src_fft_status or not uv_status):
		print('')
		print('Model FFT or uv-Coverage unavailable!')
		return

	# Grid the uv-coverage
	# src_fft_arr, pix_scale_img_lam, fft_scale_lam, pix_scale_fftX_lam, pix_scale_fftY_lam
	try:
	    uv_mask_arr = np.zeros(src_fft_arr.shape, dtype=np.int32)
	    uv_cnt_arr  = np.zeros(src_fft_arr.shape, dtype=np.int32)

	    u_lam = u_arr_lda.flatten()
	    v_lam = v_arr_lda.flatten()
	    u_pix = (u_lam+fft_scale_lam)/pix_scale_fftX_lam
	    v_pix = (v_lam+fft_scale_lam)/pix_scale_fftY_lam
	    u2_pix = (-u_lam+fft_scale_lam)/pix_scale_fftX_lam
	    v2_pix = (-v_lam+fft_scale_lam)/pix_scale_fftY_lam
	    for j in range(len(u_pix)):
	        try:
	            uv_mask_arr[int(v_pix[j]), int(u_pix[j])]   = 1
	            uv_mask_arr[int(v2_pix[j]), int(u2_pix[j])] = 1
	            uv_cnt_arr[int(v_pix[j]), int(u_pix[j])]    += 1
	            uv_cnt_arr[int(v2_pix[j]), int(u2_pix[j])]  += 1
	        except Exception:
	            # Ignore if visibility falls outside of the FFT image
	            pass
	except Exception:
	        print("Gridding failed!")
	        sys.exit()

	# Apply the gridded uv-coverage to the model FFT
	try:
	    obs_fft_arr = src_fft_arr.copy()*uv_mask_arr
	except Exception:
	    print("Masking failed!")
	    return
	            
	# Print the percentage coverage
	print('')
	npix = uv_mask_arr.shape[0] * uv_mask_arr.shape[1]
	n_used_pix = np.sum(uv_mask_arr)
	pc = n_used_pix*100.0/npix
	print("{:.2f} % of pixels used in observed FFT image.".format(pc))

	return uv_mask_arr, uv_cnt_arr, obs_fft_arr







## Calculate the beam image for the gridded uv-coverage
 #
 # params dict data   infor of the array
 #
 # return ???
 # 
 # Version 11/2019
 # Author Hiep Nguyen
 ##
def get_synth_beam(griduv_status, uv_mask_arr):

	# Calculate the beam image
	try:
		beam_arr = np.fft.ifft2(uv_mask_arr)
		beam_arr = np.fft.ifftshift(beam_arr)
	except Exception:
		print("Failed to calculate the beam image!")

	return beam_arr






## Apply the gridded uv-coverage to the model FFT image, and invert to produce the final observed image
 #
 # params dict data   infor of the array
 #
 # return ???
 # 
 # Version 11/2019
 # Author Hiep Nguyen
 ##
def invert_obs(griduv_status, beam_status, obs_fft_arr):
    
    try:
        # Invert to produce the final image
        obs_img_arr = np.fft.ifft2(np.fft.ifftshift(obs_fft_arr))
    except Exception:
        print('Failed produce the observed image!')
        return

    # if self.verbose:
    #     print("Observation complete!")

    return obs_img_arr