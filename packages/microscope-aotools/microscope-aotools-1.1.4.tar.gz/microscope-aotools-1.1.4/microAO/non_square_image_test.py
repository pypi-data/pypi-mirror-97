import numpy as np
from microAO import aoMetrics, aoAlg, aoDev
import matplotlib.pyplot as plt

np.random.seed(2321)
non_sq_image = np.random.random((2048,2048))

fourier_power_metric = aoMetrics.measure_fourier_power_metric(non_sq_image)
print(fourier_power_metric)

fourier_metric = aoMetrics.measure_fourier_metric(non_sq_image)
print(fourier_metric)

second_moment_metric = aoMetrics.measure_second_moment_metric(non_sq_image)
print(second_moment_metric)

contrast_metric = aoMetrics.measure_contrast_metric(non_sq_image)
print(contrast_metric)

gradient_metric = aoMetrics.measure_gradient_metric(non_sq_image)
print(gradient_metric)
