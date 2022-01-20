import sys

# append the path of the parent directory
sys.path.append("..")

from readers import enso

nino12 = enso.nino12_index()
nino34 = enso.nino34_index()
nino4 = enso.nino4_index()
oni = enso.oni_index()
tni = enso.tni_index()
cti = enso.cti_index()
ep = enso.ep_nino_index()
cp = enso.cp_nino_index()
