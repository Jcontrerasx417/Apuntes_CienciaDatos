import numpy as np
import matplotlib.pyplot as plt

# cargar CSV
image = np.loadtxt("numero8a255.csv", delimiter=";", skiprows=1)
 
 
# mostrar imagen
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.axis('off')
plt.show()