import numpy as np
from microAO.aoAlg import AdaptiveOpticsFunctions
import matplotlib.pyplot as plt
from scipy.signal import tukey
from microAO.aoMetrics import make_ring_mask

# Should fix this with multiple inheritance for this class!
aoAlg = AdaptiveOpticsFunctions()

def measure_fourier_metric(image, wavelength=500 * 10 ** -9, NA=1.1,
                            pixel_size=0.1193 * 10 ** -6, **kwargs):
    ray_crit_dist = (1.22 * wavelength) / (2 * NA)
    ray_crit_freq = 1 / ray_crit_dist
    max_freq = 1 / (2 * pixel_size)
    freq_ratio = ray_crit_freq / max_freq
    OTF_outer_rad = (freq_ratio) * (np.shape(image)[0] / 2)

    im_shift = np.fft.fftshift(image)
    tukey_window = tukey(im_shift.shape[0], .10, True)
    tukey_window = np.fft.fftshift(tukey_window.reshape(1, -1) * tukey_window.reshape(-1, 1))
    im_tukey = im_shift * tukey_window
    fftarray = np.fft.fftshift(np.fft.fft2(im_tukey))

    fftarray_sq_log = np.log(np.real(fftarray * np.conj(fftarray)))

    cent2corner = np.sqrt(2 * ((image.shape[0] / 2) ** 2))
    rad_to_corner = cent2corner - OTF_outer_rad
    noise_corner_size = int(np.round(np.sqrt((rad_to_corner ** 2) / 2) * 0.9))
    noise = (fftarray_sq_log[0:noise_corner_size, 0:noise_corner_size] +
            fftarray_sq_log[0:noise_corner_size, -noise_corner_size:] +
            fftarray_sq_log[-noise_corner_size:, 0:noise_corner_size] +
            fftarray_sq_log[-noise_corner_size:, -noise_corner_size:]) / 4
    threshold = np.mean(noise) * 1.125

    ring_mask = make_ring_mask(np.shape(image),0.1 * OTF_outer_rad, OTF_outer_rad)
    freq_above_noise = (fftarray_sq_log > threshold) * ring_mask
    return freq_above_noise

def set_phase(applied_z_modes, offset=None):
    try:
        actuator_pos = aoAlg.ac_pos_from_zernike(applied_z_modes, 52)
    except Exception as err:
        print(err)
        raise err
    if np.any(offset) is None:
        actuator_pos += 0.5
    else:
        actuator_pos += offset
    return actuator_pos

sensorless_AO_correction_stack = np.load("C:\\Users\\nicho\\Documents\\DPhil work\\Asad sensorless full stack data\\sensorless_AO_correction_stack_15102019_1324.npy")
sensorless_AO_nollZernike = np.load("C:\\Users\\nicho\\Documents\\DPhil work\\Asad sensorless full stack data\\sensorless_AO_nollZernike_15102019_1324.npy")
sensorless_AO_zernike_applied = np.load("C:\\Users\\nicho\\Documents\\DPhil work\\Asad sensorless full stack data\\sensorless_AO_zernike_applied_15102019_1324.npy")

control_matrix = np.loadtxt("C:\\Users\\nicho\\Documents\\DPhil work\\Asad sensorless full stack data\\Control.txt")
aoAlg.set_controlMatrix(control_matrix)

aoAlg.set_metric("gradient")

#metrics = []
#for ii in range(5):
    #plt.figure(ii)
    #plt.imshow(sensorless_AO_correction_stack[ii,:,:])
    #image_metric = measure_fourier_metric(sensorless_AO_correction_stack[ii,:,:])
    #plt.figure(5+ii)
    #plt.imshow(image_metric)

    #metric = aoAlg.measure_metric(sensorless_AO_correction_stack[ii,:,:])
    #metrics.append(metric)

#plt.plot(metrics)

#plt.show()

numMes = 9
num_it = 2
z_steps = np.linspace(-0.3, 0.3, numMes)
no_actuators = 52
nollZernike=np.array([13, 24, 3, 5, 7, 8, 6, 9])

for ii in range(num_it):
    it_zernike_applied = np.zeros((numMes * nollZernike.shape[0], no_actuators))
    for noll_ind in nollZernike:
        ind = np.where(nollZernike == noll_ind)[0][0]
        it_zernike_applied[ind * numMes:(ind + 1) * numMes,
        noll_ind - 1] = z_steps
    if ii == 0:
        zernike_applied = it_zernike_applied
    else:
        zernike_applied = np.concatenate((zernike_applied, it_zernike_applied))

correction_stack = []
actuator_offset = None

print(zernike_applied[len(correction_stack), :])
actuator_positions = set_phase(zernike_applied[len(correction_stack), :], offset=actuator_offset)
print(actuator_positions)