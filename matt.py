import scipy.io
from fnc.matching import matching
mat1 = scipy.io.loadmat('/home/pi/Downloads/python/templates/brunda1.jpg.mat')
#mat2 = scipy.io.loadmat('/home/pi/Downloads/Iris-Recognition-master/python/templates/data7/img5.jpg.mat')
a=mat1['template']
print(a)
#b=mat2['template']
#c1=mat1['mask']
#b1=mat2['mask']
##print(c)
##print(b)
##result = matching(c, c1, b, )
print(a[0])
print(a[1])
print(a[2])
print(a[3])
print(a[4])
print(a[5])
print(a[6])
print(a[7])
print(a[8])
print(a[9])
print(a[10])
print(a[11])
print(a[12])
print(a[13])
print(a[14])
print(a[15])
print(a[16])
print(a[17])
print(a[18])
print(a[19])
#print(a[20])
#c=a==b
#print(c)