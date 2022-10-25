
import numpy as np
import matplotlib.pyplot as plt

sinus =[]
measurement_points = 200
cycle_length = 200
base_temperature = 30
cycle_width = 5

function = lambda x: cycle_width*np.sin((x/cycle_length)*2*np.pi)+base_temperature

for i in range(measurement_points):
   sinus.append(function(i))
print(sinus)
#Nur für Plot

plt.plot(sinus)
plt.ylabel('Temperratur [°C]')
plt.xlabel('10tel Sekunden')
plt.show()


# Das müsste man noch für C++ anpassen. 
# Der Vergleich der aktuellen Peltier-Temperatur und der Soll-Temperatur des Sinus

#float(input(Sensor_0)) = Temperatur_Peltier

#While Cycle_number < 20:
    #if Temperatur_Peltier < sinus[i]:
        #Digitalwrite_2 = high
    #else:
        #Digitalwrite_2 = low

    #delay(100)