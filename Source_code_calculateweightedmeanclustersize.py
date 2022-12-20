#Source code 01 (Figure 1E and FigS3).
#This code corrects the distribution of cellular biomass over the range of cluster sizes, and finds the mean of this biomass distribution (see Fig1E for the average cluster size and Fig. S3 for a visual representation of size distribution, calculated using this code).
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd


X=[]
Y=[]
numbins=10
rep=[]
rep_Vol_weighted=[]
days=600
strain_list=[]
rep_vol_weighted=[]


data1 = np.genfromtxt("file_name.csv", dtype=float, delimiter=',')
data2 = np.genfromtxt("file_name.csv", dtype=str, delimiter=',')
Vol=data1[1:,2]
timepoint=data1[1:,1]
Vol=np.array(Vol)
LogVol=np.log10(Vol)
strain=data2[1:,0]
volumes=zip(Vol, LogVol)
#putting it into a dataframe so that we can index on strain label
dataframe=pd.DataFrame(volumes, index=strain)
print dataframe
#print dataframe.loc['E3-16']

#calculating the number of unique labels
strain=data2[1:,0]
strain_noDupes = []
[strain_noDupes.append(i) for i in strain if not strain_noDupes.count(i)]
strain=str(strain)
print strain
print "number of strains",len(strain_noDupes)

colormap = plt.cm.gist_ncar
plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, len(strain_noDupes))])

for i in range(0,len(strain_noDupes)):
    print "computing strain", strain_noDupes[i]
    binmeans=[]
    biomass=[]
    binvec=[]
    biomass_vec=[]
    total_biomass=[]
    tempslice=dataframe.loc[strain_noDupes[i]]
    tempslice=np.array(tempslice)
    tempVol=tempslice[0:,0]
    tempLogVol=tempslice[0:,1]
    total_biomass=sum(tempslice[0:,0])
    binsize=(max(tempLogVol)-min(tempLogVol))/(numbins) 
    for d in range(0,(numbins+1)):
        binvec.append(min(tempLogVol)+binsize*d)
    for h in range(0,len(binvec)-1):
        temp_size=[]
        for a in range(0,(len(tempLogVol))):
            if tempLogVol[a]>=binvec[h] and tempLogVol[a]<=binvec[h+1]:
                temp_size.append((10**(tempLogVol[a]))*100/total_biomass)
        #print "we are now on bin number", h        
        #print len(temp_size)    
        #print sum(temp_size)
        biomass.append(sum(temp_size))
    for e in range(0,len(binvec)-1):
        binmeans.append((binvec[e]+binvec[e+1])/2) 
    rep_vol_weighted.append(np.average(binmeans, weights=biomass)) 
    print "binmeans", binmeans[1]
    print "biomass", biomass[1]
    plt.plot(binmeans, biomass, alpha=.9)
    plt.xlabel('Volume (log), a.u.')
    plt.ylabel('Fraction biomass at that size')  
    #plt.xlim([0,12])
    plt.tight_layout()
    
plt.savefig("day %s Vol biomass plot.pdf" %(days), dpi=300)
#plt.close()    
print "weighted biomass mean", rep_vol_weighted
#biomassoutput=zip(strain_noDupes, rep_vol_weighted)
#print biomassoutput
#np.savetxt("day %s biomass means.csv" %(days), biomassoutput, delimiter=",", fmt="%s")    






