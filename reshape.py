import numpy as np
array = np.arange(12)
print(array)

print("shape of the array is ", array.shape)

new_array = array.reshape(3, 4)
print(new_array)

print(np.arange(12).reshape(4, 3))

# write the array in three dimensions
print("Here the new array")
new = np.arange(12).reshape(2, 2, 3)
print(new)
print("shape of the new array is ", new.shape)

# shawp axises of the array
print("swap axes")
print(new_array)
swap = np.swapaxes(new_array, 1, 0)
print(swap)
