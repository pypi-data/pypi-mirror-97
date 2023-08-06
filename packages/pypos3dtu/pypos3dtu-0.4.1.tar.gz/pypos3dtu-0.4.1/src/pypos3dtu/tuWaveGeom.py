'''
Created on 12 mai 2020

UnitTests for class WaveGeom (basic methods)

Unittests of high level algorithms are in the module tuPlaneCut.py

@author: olivier
'''
import unittest
import sys, cProfile, pstats
import random
import math
from pypos3dtu.tuConst import *

from langutil import C_OK, C_ERROR, C_FAIL
from pypos3d.wftk.WFBasic import C_MISSING_MAT, findCommonPoints
from pypos3d.wftk.WaveGeom import readGeom

PROFILING = False

class Test(unittest.TestCase):
  wg_cube_gris = None
  wg_ressort = None
  wg_ressort2800 = None

  def setUp(self):
    logging.basicConfig(format='%(asctime)s %(module)s.%(funcName)s %(message)s') # , datefmt='%H:%M:%S,uuu')
    logging.getLogger().setLevel(logging.INFO)
    Test.wg_cube_gris = readGeom(OBJ_FILE_GREY_CUBE)
    if PROFILING:
      self.pr = cProfile.Profile()
      self.pr.enable()


  def tearDown(self):
    if PROFILING:
      self.pr.disable()
      sortby = 'time'
      ps = pstats.Stats(self.pr, stream=sys.stdout).sort_stats(sortby)
      ps.print_stats()



  def testsMtlLoading(self):
    objsrc = readGeom('srcdata/MappingCube-c1bis.obj', usemtl=True)
    self.assertEqual(len(objsrc.libMat), 0)
    
    objsrc = readGeom('srcdata/CutterCubey0_25Tex.obj', usemtl=True)
    self.assertEqual(len(objsrc.libMat), 1)
    mat  = objsrc.libMat['Cubey0_25_auv']
    self.assertEqual(mat.d, 1.0)
    self.assertEqual(mat.map_kd, 'auvBG.png')
    
#     objsrc = readGeom('srcdata/PoserRoot/Runtime/Geometries/Pojamas/Globe.obj', usemtl=True, imgdirpath='srcdata/PoserRoot/Runtime/Geometries/Pojamas/')
#     objsrc.writeOBJ('tures/Globe.obj')


#   def textBinSearch(self):
#     t = [1,2,10,20,30,40,500]
#     
#     r = Arrays_binarySearch(t, 1)
#     self.assertEqual(r, 0, "ok")
#     
#     r = Arrays_binarySearch(t, 20)
#     self.assertEqual(r, 3, "ok")
# 
#     r = Arrays_binarySearch(t, 500)
#     self.assertEqual(r, 6, "ok")
#   
#     r = Arrays_binarySearch(t, -20)
#     self.assertEqual(r, -1, "ok")

  def testCommonPoints(self):
    t1 = [ ]
    t2 = [ ]
    rt1 = []
    rt2 = []
    rt3 = []
    
    NbTour = 10000
    
    c = ChronoMem.start("CommonPoints-Init")
    for i in range(0,NbTour):
      t1 += [ [ random.randint(1,100) for j in range(1,1000)], ]
      t2 += [ [ random.randint(1,100) for j in range(1,1000)], ]
    c.stopRecord("WaveFrontPerf.txt")

    c = ChronoMem.start("CommonPoints-Manual")
    for i in range(0,NbTour):
      rt1 += [ findCommonPoints(t1[i],t2[i]), ]
    c.stopRecord("WaveFrontPerf.txt")
    
    c = ChronoMem.start("CommonPoints-And")
    for i in range(0,NbTour):
      rt2 += [ t1[i] and t2[i] , ]
    c.stopRecord("WaveFrontPerf.txt")
    
    c = ChronoMem.start("CommonPoints-Set")
    for i in range(0,NbTour):
      rt3 += [ list(set(t1[i]) & set(t2[i])), ]
    c.stopRecord("WaveFrontPerf.txt")

    for i in range(0,NbTour):
      rt1[i].sort()
      #rt2[i].sort()
      rt3[i].sort()
      
      #print('rt1-rt2:' + str(rt1[i]==rt2[i]))
      if rt1[i]!=rt3[i]:
        print('rt1-rt3:' + str(rt1[i]) + ' ' + str(rt3[i]))
      #print('rt2-rt3:' + str(rt2[i]==rt3[i]))

  def testWaveFrontRead(self):
    self.assertTrue(self.wg_cube_gris != None)
    self.assertTrue(self.wg_cube_gris.getName() == OBJ_FILE_GREY_CUBE)
    self.assertEqual(8, len(self.wg_cube_gris.getCoordList()))
    self.assertEqual(1, len(self.wg_cube_gris.getGroups()))

    # For coverage purpose
    readGeom("srcdata/cube_gris.obz")
    
    # Read a obj file with lines
    light = readGeom(OBJ_FILE_LIGHT)
    self.assertEqual(98, len(light.getCoordList()))
    self.assertEqual(1, len(light.getGroups()))
    self.assertEqual(17, len(light.getGroups()[0].lineStripCount))
    
    
  # ---------------------------------------------------------------------------
  # Textured Cube to verify Identity 
  #
  def testCutCubeTexDiag(self):
    objsrc = readGeom('srcdata/CutterCubey0_25Tex.obj')
    cube = objsrc.getGroup("Cubey0_25")
    objsrc.writeOBJ("tures/CutterCubey0_25TexId.obj")
    

  def testCreateGeomGroup(self):
    gg1 = self.wg_cube_gris.createGeomGroup("grp3")
    self.assertTrue(gg1 != None)

    gg2 = self.wg_cube_gris.createGeomGroup(None)
    self.assertTrue(gg2 != None)

  def testGetMaterialList(self):
    lm = self.wg_cube_gris.getMaterialList()
    self.assertEqual(lm[0], "cube1_auv")
    self.assertEqual(lm[1], "matRouge")
   

  def testScale(self):
    self.wg_cube_gris.scale(2.0, 3.0, -4.0)
    
    lstpt = self.wg_cube_gris.getCoordList()

    self.assertEqual(lstpt[0].x, -2.0)
    self.assertEqual(self.wg_cube_gris.getCoordList()[0].y, -3.0)
    self.assertEqual(self.wg_cube_gris.getCoordList()[0].z, -4.0)

  def testWriteOBJ(self):
    res = self.wg_cube_gris.writeOBJ(OBJ_FILE_GREY_CUBE_RES)
    self.assertTrue(res == C_OK)

    res = self.wg_cube_gris.writeOBJ("badrep/toto.obj")
    self.assertTrue(res == C_ERROR)

    # self.wg_cube_gris.removeGroupLoc()
    res = self.wg_cube_gris.writeOBJ(OBJ_FILE_GREY_CUBE_RES)
    self.assertTrue(res == C_OK)

  def testWriteOBZ(self):
    res = self.wg_cube_gris.writeOBZ(OBZ_FILE_GREY_CUBE_RES)
    self.assertTrue(res == C_OK)#

    res = self.wg_cube_gris.writeOBZ("badrep/toto.obz")
    self.assertTrue(res == C_ERROR)

    wg = readGeom(OBZ_FILE_PHF_LOWRES)

    c = ChronoMem.start("writeOBZ-PHFemaleLowRes.obz")
    wg.writeOBZ(OBZ_FILE_PHF_LOWRES_RES)
    c.stopRecord("WaveFrontPerf.txt")

  def testFusion(self):
    wg = readGeom(OBJ_FILE_RED_CUBE)
    wg_ressort = readGeom(OBJ_FILE_GREEN_TRON)
    li = [ wg_ressort ]
    outMapLst = [ ]
    wg.fusion(li, outMapLst)
    wg.writeOBJ("tures/fusioned_cubes.obj")


  def testCopy(self):
    wgnew = Test.wg_cube_gris.copy()
    self.assertTrue(wgnew != None)
    
    ret = wgnew.selectMaterial('Unfound')
    self.assertEqual(ret, -1)
    ret = wgnew.selectMaterial('matRouge')
    self.assertEqual(ret, 1)
    
    wgnew.scale(1.0,1.0,1.0)
    
    wgnew.translate(.0,.0,.0)

    grp = wgnew.getGroups()[0]
    r = grp.getFaceVertex(0, restab=[None, None, None, None])

    d = grp.calcXYRadius(grp.getFaceVertIdx(1))
    self.assertEqual(d, math.sqrt(2.0))
    

    
    r = grp.findFace(10)
    self.assertEqual(r, -1)
    
    grp.invertFaceOrder()
    self.assertEqual(grp.getFaceVertIdx(0), [1,2,3,0])
    
    ret = grp.extractFaces(materialName='Bad Material')
    self.assertEqual(ret, None)
    
    ret = wgnew.removeGroup('Not a Group', cleaning=True)
    self.assertEqual(ret, C_FAIL)

    
    ret = wgnew.removeGroup('cube1', cleaning=True)
    self.assertEqual(ret, C_OK)
    

  def testReadPerf(self):
    for i in range(0, 5):      
      c = ChronoMem.start("AbsWaveGeom.readGeom-2800f")
      wg_ressort = readGeom(OBJ_FILE_RESSORT)
      self.assertTrue(wg_ressort != None)
      c.stopRecord("WaveFrontPerf.txt")

 
  def testFillHoleSpider(self):
    #ChronoMem c
    wg = readGeom(OBJ_FILE_SPHERE_HOLE)

    r = wg.fillHole("sphere1", "Notfound", "unused", "Color", True, 2, 0.0625)
    self.assertEqual(r, C_MISSING_MAT)

    c = ChronoMem.start("fillHoleSpider-Sphere1")
    r = wg.fillHole("sphere1", "TROU", "unused", "Color", True, 2, 0.0625)
    c.stopRecord("WaveFrontPerf.txt")

    self.assertEqual(r, C_OK)
    wg.writeOBJ("tures/sphere_filled3.obj")

    wg = readGeom(OBJ_FILE_SPHERE_HOLE)

    c = ChronoMem.start("fillHoleSpider-Sphere2")
    r = wg.fillHole(None, "TROU", "unused", "Color", False, 2, 0.1)
    c.stopRecord("WaveFrontPerf.txt")

    self.assertEqual(r, C_OK)
    wg.writeOBJ("tures/sphere_filled4.obj")

    wg = readGeom(OBJ_FILE_EARTH_HOLE)
    r = wg.fillHole("Terre", "TROU", "newGrp", "Color", True, 2, 0.0625) #, createCenter=False)
    
    wg.writeOBJ("tures/TerrePoignees+Trou_filled.obj")

    self.assertEqual(r, C_OK)
    self.assertEqual(814, len(wg.coordList))
    self.assertAlmostEqual(0.08213272, wg.coordList[801].x, delta=1e-6)
    self.assertAlmostEqual(0.35574902, wg.coordList[801].y, delta=1e-6)
    self.assertAlmostEqual(0.03402049, wg.coordList[801].z, delta=1e-6)

    self.assertAlmostEqual(0.0765935, wg.coordList[813].x, delta=1e-6)
    self.assertAlmostEqual(0.363881, wg.coordList[813].y, delta=1e-6)
    self.assertAlmostEqual(0.0218888, wg.coordList[813].z, delta=1e-6)

    self.assertEqual(299, len(wg.texList))
    self.assertAlmostEqual(0.330287, wg.texList[286].x, delta=1e-6)
    self.assertAlmostEqual(0.206048, wg.texList[286].y, delta=1e-6)
    self.assertAlmostEqual(0.379576, wg.texList[298].x, delta=1e-6)
    self.assertAlmostEqual(0.220285, wg.texList[298].y, delta=1e-6)


    wg = readGeom(OBJ_FILE_TOP_HOLE)
    c = ChronoMem.start("fillHoleSpider-Sphere2-01Top")
    r = wg.fillHole("lCollar", "TROU", "newGrp", "Color", True, 2, 0.0625)
    self.assertEqual(r, C_OK)
    self.assertEqual(7571, len(wg.coordList))
    self.assertEqual(7619, len(wg.texList))
    c.stopRecord("WaveFrontPerf.txt")

  def testExtract(self):
    c = ChronoMem.start("AbsWaveGeom.readGeom-PHFemaleLowRes.obz")
    wg = readGeom(OBZ_FILE_PHF_LOWRES)
    c.stopRecord("WaveFrontPerf.txt")

    wgr = wg.extractSortGeom("badname")
    self.assertTrue(wgr == None)

    wgr = wg.extractSortGeom("hip:1")
    self.assertTrue(wgr != None)
    wgr.writeOBJ("tures/hip_extracted.obj")

    t = wg.extractSortJonction("lForeArm:1", "daube:1")
    self.assertTrue(t == None)

    t = wg.extractSortJonction("daube:1", "lShldr:1")
    self.assertTrue(t == None)

    c = ChronoMem.start("extractSortJonction-PHFemaleLowRes.obz")
    wg = readGeom(OBJ_FILE_ICOSAHEDRON)
    t = wg.extractSortJonction("icosahedron", "Prisme")
    c.stopRecord("WaveFrontPerf.txt")

    self.assertTrue(t != None)
    self.assertEqual(3, len(t))

  def testCleanDupVert(self):
    wg_cube_gris = readGeom(OBJ_FILE_GREY_CUBE)
    r = wg_cube_gris.cleanDupVert(0.0)
    self.assertEqual(C_FAIL, r)

    wg = readGeom(OBJ_FILE_DUPVERT_01)
    r = wg.cleanDupVert(1.e-7)
    self.assertEqual(C_OK, r)
    self.assertEqual(20, len(wg.coordList))
    wg.writeOBJ("tures/t1.obj")

    wg = readGeom(OBJ_FILE_DUPVERT_02)
    r = wg.cleanDupVert(1.e-7)
    self.assertEqual(C_OK, r)
    self.assertEqual(32, len(wg.coordList))
    wg.writeOBJ("tures/t2.obj")

    wg = readGeom(OBZ_FILE_PHF_LOWRES_SRC)
    self.assertEqual(17184, len(wg.coordList))
    r = wg.cleanDupVert(1e-7)
    self.assertEqual(15981, len(wg.coordList))
    self.assertEqual(C_OK, r)
    wg.writeOBJ("tures/PHFemaleLowRes.obj")


  def testRemoveFace(self):
    wg_cube_gris = readGeom(OBJ_FILE_GREY_CUBE)
    cube = wg_cube_gris.groups[0]
    cube.removeFace(0)
    cube.removeFace(2)
    cube.removeFace(cube.getNbFace()-1)
    cube.sanityCheck()
    wg_cube_gris.writeOBJ('tures/Cube-removeFace.obj')

    wg = readGeom(OBJ_FILE_EARTH_HOLE)
    terre = wg.getGroup('Terre')
    terre.sanityCheck()

    terre.removeFace(0)
    terre.sanityCheck()
    terre.removeFace(50)
    terre.sanityCheck()
    terre.removeFace(terre.getNbFace()-1)
    terre.sanityCheck()
    
    wg.writeOBJ('tures/Terre-removeFace.obj')
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
