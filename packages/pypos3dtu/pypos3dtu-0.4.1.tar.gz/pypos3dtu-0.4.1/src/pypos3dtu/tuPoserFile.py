'''
Created on 12 mai 2020

@author: olivier
'''
import unittest
import logging
import sys, cProfile, pstats
import os

from pypos3dtu.tuConst import ChronoMem, P7ROOT
from langutil import C_OK, C_ERROR 
from pypos3d.wftk.WFBasic import Vector3d, Point3d
from pypos3d.pftk.PoserBasic import PoserToken, PoserConst
from pypos3d.pftk.SimpleAttribut import ValueOpDelta
from pypos3d.pftk.PoserMeshed import ReportOption
from pypos3d.pftk.PoserFile import PoserFile

PROFILING = False

class Test(unittest.TestCase):

  def setUp(self):
    logging.basicConfig(format='%(asctime)s %(module)s.%(funcName)s %(message)s') # , datefmt='%H:%M:%S,uuu')
    logging.getLogger().setLevel(logging.INFO)
    if PROFILING:
      self.pr = cProfile.Profile()
      self.pr.enable()


  def tearDown(self):
    if PROFILING:
      self.pr.disable()
      sortby = 'time'
      ps = pstats.Stats(self.pr, stream=sys.stdout).sort_stats(sortby)
      ps.print_stats()


  def testPoserFile(self):
    pfv3 = PoserFile("srcdata/Earth.pp2")
    self.assertTrue(pfv3 != None)
    lf = pfv3.getLstFigure()
    self.assertTrue(len(lf) == 0)
    lp = pfv3.getLstProp()
    self.assertTrue(len(lp) == 1)
    # Check internal Geom
    p = lp[0]
    self.assertEqual(p.getGeomCustom().getWaveGeom().getCoordListLength(), 3970)
    self.assertEqual(len(p.getGeomCustom().getWaveGeom().getTexList()), 4095)
    self.assertEqual(len(p.getGeomCustom().getWaveGeom().getGroups()), 1)
    
    c = ChronoMem.start("PoserFile.read-PHF-LoRes.cr2")
    pfv3 = PoserFile("srcdata/PoserRoot/Runtime/Librairies/Character/tu1/PHF-LoRes.cr2")
    c.stopRecord("PoserFilePerf.txt")
    self.assertTrue(pfv3 != None)

    c = ChronoMem.start("PoserFile.read-PHF-LoRes.crz")
    pfv3 = PoserFile("srcdata/PoserRoot/Runtime/Librairies/Character/tu1/PHF-LoRes.crz")
    c.stopRecord("PoserFilePerf.txt")

    self.assertTrue(pfv3 != None)
    lf = pfv3.getLstFigure()
    self.assertTrue(len(lf) == 1)

    pfv3 = PoserFile("srcdata/PoserRoot/Runtime/Librairies/Pose/tu1/AnkleSpandex.p2z")
    self.assertTrue(pfv3 != None)
    lf = pfv3.getLstFigure()
    self.assertTrue(len(lf) == 0)

    pfv3 = PoserFile("srcdata/PoserRoot/Runtime/Librairies/Pose/tu1/V3 Stride.pz2")
    self.assertTrue(pfv3 != None)
    lf = pfv3.getLstFigure()
    self.assertTrue(len(lf) == 1)

    pfv3 = PoserFile("srcdata/PoserRoot/Runtime/Librairies/Props/tu1/gymnase.ppz")
    self.assertTrue(pfv3 != None)
    lf = pfv3.getLstFigure()
    self.assertTrue(len(lf) == 0)
    lp = pfv3.getLstProp()
    self.assertTrue(len(lp) == 1)

    pfv3 = PoserFile("srcdata/PoserRoot/Runtime/Librairies/Props/tu1/HV Jetty.pp2")
    self.assertTrue(pfv3 != None)
    lf = pfv3.getLstFigure()
    self.assertTrue(len(lf) == 0)
    lp = pfv3.getLstProp()
    self.assertTrue(len(lp) == 1)


    c = ChronoMem.start("PoserFile.read-v3_buxom_barbarian2.pzz")
    sc1 = PoserFile("srcdata/scenes/v3_buxom_barbarian2.pzz")
    c.stopRecord("PoserFilePerf.txt")
    self.assertTrue(sc1 != None)

    c = ChronoMem.start("PoserFile.read-v3_book_top.pz3")
    sc2 = PoserFile("srcdata/scenes/v3_book_top.pz3")
    c.stopRecord("PoserFilePerf.txt")
    self.assertTrue(sc2 != None)

    c = ChronoMem.start("PoserFile.hairProp")
    sc2 = PoserFile("srcdata/PoserRoot/Runtime/Librairies/Hair/hairPropTest.hrz")
    c.stopRecord("PoserFilePerf.txt")
    self.assertTrue(sc2 != None)

  def testWrite(self):
#     pfv3 = PoserFile("srcdata/scenes/n1.pz3")
#     pfv3.writeFile("tures/n1.pz3")

    pfv3 = PoserFile("srcdata/scenes/TeleSat_Fig.pz3")
    pfv3.writeFile("tures/TeleSat_Fig.pz3")

    pfv3 = PoserFile("srcdata/scenes/MapMonde+Prop+Channels-01.pz3")
    pfv3.writeFile("tures/MapMonde+Prop+Channel-01.pz3")
  
    pfv3 = PoserFile("srcdata/PoserRoot/Runtime/Librairies/Character/tu1/PHF-LoRes.crz")

    r = pfv3.writeFile("badrep/toto.cr2")
    self.assertTrue(r == C_ERROR)

    c = ChronoMem.start("PoserFile.write-v3.cr2")
    r = pfv3.writeFile("tures/v3.cr2")
    c.stopRecord("PoserFilePerf.txt")
    self.assertTrue(r == C_OK)

    r = pfv3.writeZ("badrep/toto.crz")
    self.assertTrue(r == C_ERROR)

    c = ChronoMem.start("PoserFile.write-v3.crz")
    r = pfv3.writeZ("tures/v3.crz")
    c.stopRecord("PoserFilePerf.txt")
    self.assertTrue(r == C_OK)


  def testGetFactor(self):
    sc1 = PoserFile("srcdata/scenes/v3_buxom_barbarian2.pzz")
    # self.assertTrue(sc1 != None)

    # Bad name but not used for the moment
    f = sc1.getFactor("BadFigure 1", "BODY:1", "PBMBuxom")
    self.assertTrue(f == 0.0)

    f = sc1.getFactor("Figure 1", "badPart:1", "badname")
    self.assertTrue(f == 0.0)

    f = sc1.getFactor("Figure 1", "BODY:1", "badname")
    self.assertTrue(f == 0.0)

    # Nominal Case
    f = sc1.getFactor("Figure 1", "BODY:1", "PBMBuxom")
    self.assertEqual(0.0, f)

    # Nominal Case
    f = sc1.getFactor("Figure 1", "lThigh:1", "PBMBarbarian2")
    print("f=" + str(f))
    self.assertAlmostEqual(0.5, f, delta=1e-6)


  def testGetDescendant(self):
    sc1 = PoserFile("srcdata/scenes/v3_buxom_barbarian2.pzz")

    ls = sc1.getDescendant(-1, "Hip")
    self.assertTrue(ls == None)

    ls = sc1.getDescendant(1, "hip")
    self.assertTrue(ls != None)
    self.assertEqual(56, len(ls))
    #print(str(ls))
    self.assertEqual(
      "['abdomen:1', 'chest:1', 'neck:1', 'head:1', 'lEye:1', 'rEye:1', 'rCollar:1', 'rShldr:1', 'rForeArm:1', 'rHand:1', 'rThumb1:1', 'rThumb2:1', 'rThumb3:1', 'rIndex1:1', 'rIndex2:1', 'rIndex3:1', 'rMid1:1', 'rMid2:1', 'rMid3:1', 'rRing1:1', 'rRing2:1', 'rRing3:1', 'rPinky1:1', 'rPinky2:1', 'rPinky3:1', 'lCollar:1', 'lShldr:1', 'lForeArm:1', 'lHand:1', 'lThumb1:1', 'lThumb2:1', 'lThumb3:1', 'lIndex1:1', 'lIndex2:1', 'lIndex3:1', 'lMid1:1', 'lMid2:1', 'lMid3:1', 'lRing1:1', 'lRing2:1', 'lRing3:1', 'lPinky1:1', 'lPinky2:1', 'lPinky3:1', 'rThigh:1', 'rShin:1', 'rFoot:1', 'rToe:1', 'lThigh:1', 'lShin:1', 'lFoot:1', 'lToe:1', 'rBreast1:1', 'lBreast1:1', 'lBreast2:1', 'rBreast2:1']",
      str(ls))

    ls = sc1.getDescendant(1, "rHand")
    self.assertTrue(ls != None)
    self.assertEqual(15, len(ls))
    self.assertEqual(
        "['rThumb1:1', 'rThumb2:1', 'rThumb3:1', 'rIndex1:1', 'rIndex2:1', 'rIndex3:1', 'rMid1:1', 'rMid2:1', 'rMid3:1', 'rRing1:1', 'rRing2:1', 'rRing3:1', 'rPinky1:1', 'rPinky2:1', 'rPinky3:1']",
        str(ls))

    fig = sc1.getFigure(1)
    pa = fig.findActor("rThumb2:1")
    ls = sc1.getDescendant(1, pa)
    self.assertTrue(ls != None)
    self.assertEqual(1, len(ls))
    self.assertEqual("['rThumb3:1']", str([ pa.getName() for pa in ls ]))


  def testGetWelded(self):
    sc1 = PoserFile("srcdata/scenes/v3_buxom_barbarian2.pzz")

    ls = sc1.getWelded(-1, "Hip")
    self.assertTrue(ls == None)

    ls = sc1.getWelded(1, "hip:1")
    self.assertTrue(ls != None)
    self.assertEqual(len(ls), 3)
    ls.sort()
    self.assertEqual("['abdomen:1', 'lThigh:1', 'rThigh:1']", str(ls))

    ls = sc1.getWelded(1, "rHand:1")
    self.assertTrue(ls != None)
    self.assertEqual(len(ls), 6)
    ls.sort()
    self.assertEqual("['rForeArm:1', 'rIndex1:1', 'rMid1:1', 'rPinky1:1', 'rRing1:1', 'rThumb1:1']", str(ls))


  def testFigResFileGeom(self):
    sc1 = PoserFile("srcdata/scenes/v3_buxom_barbarian2.pzz")

    g = sc1.getFigResFileGeom(-1, "srcdata/P7Root")
    self.assertTrue(g == None)

    g = sc1.getFigResFileGeom(1, "baddir/P7Root")
    self.assertEqual(g.isValid(), False)

    g = sc1.getFigResFileGeom(1, "srcdata/PoserRoot")
    self.assertTrue(g != None)
    self.assertEqual(g.isValid(), True)
    self.assertEqual("srcdata/PoserRoot/Runtime/Geometries/ProjectHuman/PHFemaleLowRes.obj", g.getName())


  def testCleanNonNullDeltaIntSetOfString(self):
    sc1 = PoserFile("srcdata/scenes/v3_buxom_barbarian2.pzz")

    r = sc1.cleanNonNullDelta(-1, None)
    self.assertEqual(r, C_ERROR)

    #// Clean all PBM
    r = sc1.cleanNonNullDelta(1, None)
    self.assertEqual(r, C_OK)
    sc1.writeFile("tures/v3_buxom_barbarian2_cleanedAll.pz3")

#    // Clean only one
    sc2 = PoserFile("srcdata/scenes/v3_buxom_barbarian2.pzz")
    hs = { "PBMBuxom" }

    c = ChronoMem.start("PoserFile.cleanNonNullDelta-v3_buxom_barbarian2")
    r = sc2.cleanNonNullDelta(1, hs)
    c.stopRecord("PoserFilePerf.txt")

    self.assertEqual(r, C_OK)
    sc2.writeFile("tures/v3_buxom_barbarian2_cleanedBuxom.pz3")



  def testCleanNonNullDeltaPoserPropSetOfString(self):
    sc1 = PoserFile("srcdata/scenes/v3_book_top2.pzz")

    lp = sc1.getLstProp()
    self.assertEqual(1, len(lp))

    lp2 = sc1.getFigure(1).getProps()
    self.assertEqual(3, len(lp2))

    sc1.cleanNonNullDelta(pp=lp[0], setTargetMorph=None)

    hs = { "Custom_Morph" }

    c = ChronoMem.start("PoserFile.cleanNonNullDelta-v3_book_top2")
    sc1.cleanNonNullDelta(pp=lp2[2], setTargetMorph=hs)
    c.stopRecord("PoserFilePerf.txt")


  def testExtractAll(self):
    sc1 = PoserFile("srcdata/scenes/v3_buxom_barbarian2.pzz")
#
    lg = sc1.extractAll("", 1, None)
    self.assertEqual(lg, None)

    lg = sc1.extractAll("srcdata/P7Root", -11, None)
    self.assertEqual(lg, None)

    hs = set()
    hs.add("PBMBuxom")
#
    c = ChronoMem.start("PoserFile.extractAll-HS")
    lg = sc1.extractAll("srcdata/PoserRoot", 1, hs)
    c.stopRecord("PoserFilePerf.txt")

    self.assertTrue(lg != None)
    self.assertEqual(53, len(lg))
    self.assertEqual("hip:1", lg[0].getName())
    self.assertEqual("lToe:1", lg[52].getName())
#
    c = ChronoMem.start("PoserFile.extractAll-All")
    lg = sc1.extractAll("srcdata/PoserRoot", 1, None)
    c.stopRecord("PoserFilePerf.txt")
#
    self.assertTrue(lg != None)
    self.assertEqual(53, len(lg))
    self.assertEqual("hip:1", lg[0].getName())
    self.assertEqual("lToe:1", lg[52].getName())
#
  def testGetAncestorChannels(self):
    c = ChronoMem.start("PoserFile.read-PHF-LoRes.cr2")
    pfv3 = PoserFile("srcdata/PoserRoot/Runtime/Librairies/Character/tu1/PHF-LoRes.cr2")
    c.stopRecord("PoserFilePerf.txt")

    self.assertTrue(pfv3 != None)

    rl = pfv3.getChannelAncestor("", "", "")
    self.assertTrue(len(rl)==0)

    rl = pfv3.getChannelAncestor("PHF-LoRes", "BODY:2", "zOffset")
    self.assertEqual(1, len(rl))
    self.assertEqual("zOffset", rl[0].getName())

    rl = pfv3.getChannelAncestor("PHF-LoRes", "chest:2", "PHFEMLeftBreastUp-Down")
    self.assertEqual(2, len(rl))
    self.assertEqual("PHFEMLeftBreastUp-Down", rl[0].getName())
    self.assertEqual("PHFEMBreastsUp-Down", rl[1].getName())

    rl = pfv3.getChannelAncestor("PHF-LoRes", "lEye:2", "yrot")
    self.assertEqual(2, len(rl))
    self.assertEqual("yrot", rl[0].getName())
    self.assertEqual("PHFEMEyesSide-Side", rl[1].getName())

    rl = pfv3.getChannelAncestor("PHF-LoRes", "rThumb1:2", "yrot")
    self.assertEqual(5, len(rl))
    rstr = sorted([ c.getName() for c in rl ])
    
    self.assertEqual("yrot", rl[0].getName())
    self.assertEqual("['PHFEMALEGrasp', 'PHFEMALESpread', 'PHFEMALEThumbBend', 'PHFEMALEThumbSide', 'yrot']", str(rstr))
#     self.assertEqual("PHFEMALEThumbSide", rl[1].getName())  # ok
#     self.assertEqual("PHFEMALEThumbBend", rl[2].getName())  # ok
#     self.assertEqual("PHFEMALESpread", rl[3].getName())
#     self.assertEqual("PHFEMALEGrasp", rl[4].getName())

    pfmm1 = PoserFile("srcdata/scenes/MapMonde+Prop+Channels-01.pz3")
    rl = pfmm1.getChannelAncestor("", "box_1", "m1")
    self.assertEqual(2, len(rl))
    self.assertEqual("m1", rl[0].getName())
    self.assertEqual("Montagnes", rl[1].getName())

    pfmm2 = PoserFile("srcdata/scenes/MapMonde+Prop+Channels-02.pz3")
    rl = pfmm2.getChannelAncestor("", "Globe:1", "Vagues")
    self.assertEqual(2, len(rl))
    self.assertEqual("Vagues", rl[0].getName())
    self.assertEqual("m1", rl[1].getName())

  def testDeleteChannelImpact(self):
    c = ChronoMem.start("PoserFile.ImpactDeleteChannel")
    pfv3 = PoserFile("srcdata/PoserRoot/Runtime/Librairies/Character/tu1/PHF-LoRes.cr2")

    self.assertTrue(pfv3 != None)

    fig = pfv3.getFigure(2)
    body2 = fig.findActor("BODY:2")
    zOffsetCh = body2.getGenericTransform("zOffset")

    rl = pfv3.deleteChannelImpact(zOffsetCh)
    self.assertEqual(1, len(rl))
    self.assertEqual("zOffset", list(rl)[0].getName())

    chest2 = fig.findActor("chest:2")
    chan = chest2.getGenericTransform("PHFEMLeftBreastUp-Down")

    rl = pfv3.deleteChannelImpact(chan)
    self.assertEqual(2, len(rl))
    rstr = sorted([ c.getName() for c in rl ])
    self.assertEqual("PHFEMLeftBreastUp-Down", rstr[0])
    self.assertEqual("xRotate", rstr[1])

    lhead2 = fig.findActor("head:2")
    yrotCh = lhead2.getGenericTransform("PHFEMEyesSide-Side")

    rl = pfv3.deleteChannelImpact(yrotCh)
    self.assertEqual(3, len(rl))

    rstr = sorted([ c.getName() for c in rl ])
    self.assertEqual("['PHFEMEyesSide-Side', 'yrot', 'yrot']", str(rstr))

    rstr = sorted([ c.getPoserMeshedObject().getName() for c in rl ])
    self.assertEqual("['head:2', 'lEye:2', 'rEye:2']", str(rstr))

    pfmm1 = PoserFile("srcdata/scenes/MapMonde+Prop+Channels-02.pz3", createLinks=True)
    fig = pfmm1.getFigure(2)
    pp = pfmm1.findAllMeshedObject("box_1")[0]
    self.assertEqual("box_1", pp.getName())
    m1Ch = pp.getGenericTransform("m1")

    rl = pfmm1.deleteChannelImpact(m1Ch)
    self.assertEqual(2, len(rl))
    rstr = sorted([ c.getName() for c in rl ])
    self.assertEqual("['Vagues', 'm1']", str(rstr))

    pfmm2 = PoserFile("srcdata/scenes/MapMonde+Prop+Channels-01.pz3")
    fig = pfmm2.getFigure(1)
    globe1 = fig.findActor("Globe:1")
    vaguesCh = globe1.getGenericTransform("Vagues")

    rl = pfmm2.deleteChannelImpact(vaguesCh)
    self.assertEqual(1, len(rl))
    self.assertEqual("Vagues", list(rl)[0].getName())

    mountsCh =  globe1.getGenericTransform("Montagnes")
    rl = pfmm2.deleteChannelImpact( mountsCh)
    self.assertEqual(2, len(rl))
    rstr = sorted([ c.getName() for c in rl ])
    self.assertEqual("['Montagnes', 'm1']", str(rstr))
    #self.assertEqual("m1", list(rl)[1].getName())

    c.stopRecord("PoserFilePerf.txt")


  def testDeleteChannel(self):
    pfv3 = PoserFile("srcdata/PoserRoot/Runtime/Librairies/Character/tu1/PHF-LoRes.cr2")
    self.assertTrue(pfv3 != None)

    c = ChronoMem.start("PoserFile.DeleteChannel")
    fig = pfv3.getFigure(2)
    body2 = fig.findActor("BODY:2")
    zOffsetCh = body2.getChannel("zOffset")

    rl = pfv3.deleteChannelImpact(zOffsetCh)

    pfv3.deleteChannel(zOffsetCh, rl)

    chest2 = fig.findActor("chest:2")
    chan = chest2.getChannel("PHFEMLeftBreastUp-Down")

    rl = pfv3.deleteChannelImpact(chan)
    self.assertEqual(49, len(chest2.getChannels()))
    pfv3.deleteChannel(chan, rl)
    self.assertEqual(48, len(chest2.getChannels()))

    pfmm1 = PoserFile("srcdata/scenes/MapMonde+Prop+Channels-02.pz3", createLinks=True)
    fig = pfmm1.getFigure(2)
    pp = pfmm1.findAllMeshedObject("box_1")[0]
    #    // self.assertEqual("box_1", pp.getName())
    m1Ch =  pp.getChannel("m1")
    rl = pfmm1.deleteChannelImpact( m1Ch)
    pfmm1.deleteChannel( m1Ch, rl)
    pfmm1.writeFile("tures/MapMonde+Prop+Channels-02.pz3")

    pfmm2 = PoserFile("srcdata/scenes/MapMonde+Prop+Channels-01.pz3")
    fig = pfmm2.getFigure(1)
    globe1 = fig.findActor("Globe:1")
    mountsCh = globe1.getChannel("Montagnes")
    pfmm2.deleteChannel(mountsCh, None)
    pfmm2.writeFile("tures/MapMonde+Prop+Channels-01.pz3")

    c.stopRecord("PoserFilePerf.txt")


  def testgetReferencedFiles(self):
    pfv3 = PoserFile("srcdata/PoserRoot/Runtime/Librairies/Character/tu1/PHF-LoRes.cr2")
    
    l1 = pfv3.getReferencedFiles(P7ROOT)
    self.assertEqual(8, len(l1))
    
#     Bug fixed with Zephyr11 character (on alternate Geometries)
#     pfv4 = PoserFile("srcdata/PoserRoot/Runtime/Librairies/Character/tu1/Carmel.cr2")
#     l1 = pfv4.getReferencedFiles("/home/olivier/vol32G/Poser7/")
#     self.assertEqual(14, len(l1))
    
  def testDelete(self):
    #pfv3 = PoserFile("srcdata/PoserRoot/Runtime/Librairies/Character/tu1/PHF-LoRes.cr2")
    pfmm2 = PoserFile("srcdata/scenes/MapMonde+Prop+Channels-01.pz3")

    #lfp = pfv3.getLstFigProp()
    #pfv3.findMeshedObject("")
    lfp = pfmm2.getLstFigProp()
    for a in ["box_1", "szerzer", "Pied:1"]:
      o = pfmm2.findMeshedObject(a)
      pfmm2.delete(o)
    
    pfmm2.delete(pfmm2.getLstCamera()[0])
    pfmm2.delete(pfmm2.getLstLight()[0])
    pfmm2.delete(pfmm2.getLstFigure()[0])


  def testERCCalc(self):
    op0 = ValueOpDelta(PoserToken.E_valueOpDeltaAdd, 'Figure 1', 'arm:1', 'xrot', ctrlRatio=1.0)    
    op1 = ValueOpDelta(PoserToken.E_valueOpPlus, 'Figure 1', 'arm:1', 'xrot')
    op2 = ValueOpDelta(PoserToken.E_valueOpMinus, 'Figure 1', 'arm:1', 'xrot')
    op3 = ValueOpDelta(PoserToken.E_valueOpTimes, 'Figure 1', 'arm:1', 'xrot')
    op4 = ValueOpDelta(PoserToken.E_valueOpDivideBy, 'Figure 1', 'arm:1', 'xrot')
    
    self.assertEqual(op0.calc(0.0, 1.0), 1.0)
    self.assertEqual(op0.calc(-1.0, 10.0), 9.0)

    self.assertEqual(op1.calc(0.0, 1.0), 1.0)
    self.assertEqual(op1.calc(-1.0, 10.0), 9.0)
    
    self.assertEqual(op2.calc(0.0, 1.0), -1.0)
    self.assertEqual(op2.calc(-1.0, 10.0), -11.0)

    self.assertEqual(op3.calc(0.0, 1.0), 0.0)
    self.assertEqual(op3.calc(-1.0, 10.0), -10.0)

    self.assertEqual(op4.calc(0.0, 1.0), 0.0)
    self.assertEqual(op4.calc(-1.0, 10.0), -.1)

    op5 = ValueOpDelta(PoserToken.E_valueOpKey, 'Figure 1', 'arm:1', 'xrot', keys=((0.0, 0.0),(1.0, 1.0)))
    self.assertEqual(op5.calc(0.0, 0.0), 0.0)
    self.assertEqual(op5.calc(-10.0, 0.0), 0.0)
    self.assertEqual(op5.calc(1.0, 1.0), 1.0)
    self.assertEqual(op5.calc(0.0, 200.0), 1.0)
    self.assertEqual(op5.calc(0.0, 0.2), 0.2)

    op5 = ValueOpDelta(PoserToken.E_valueOpKey, 'Figure 1', 'arm:1', 'xrot', keys=((0.0, 0.0),(1.0, 1.0), (2.2, 2.2)))
    self.assertEqual(op5.calc(0.0, 0.0), 0.0)
    self.assertEqual(op5.calc(-10.0, -10.0), 0.0)
    self.assertEqual(op5.calc(10.0, 10.0), 2.2)
    self.assertEqual(op5.calc(200.0, 200.0), 2.2)
    self.assertEqual(op5.calc(0.0, 1.0), 1.0)
    self.assertAlmostEqual(op5.calc(.2, 0.2), 0.2, delta=1e-8)

    op5 = ValueOpDelta(PoserToken.E_valueOpKey, 'Figure 1', 'arm:1', 'xrot', keys=(( -1.0, -2.0), (1.0, 0.860), (2.0, 4.0)))
    self.assertAlmostEqual(op5.calc(0.0, 1.0), 0.860, delta=1e-8)
    
    # WARNING: Poser result is -0.807!
    self.assertAlmostEqual(op5.calc(0.0, 0.2), -0.8312, delta=1e-8)

    op5 = ValueOpDelta(PoserToken.E_valueOpKey, 'Figure 1', 'arm:1', 'xrot', keys=(( -1.0, -2.0), (0.2, 2.61166), (1.0, 0.860), (2.0, 4.0)))
    self.assertAlmostEqual(op5.calc(0.0, 1.0), 0.860, delta=1e-8)
        
    # WARNING: Poser result is 2.017 --> self.assertAlmostEqual(op5.calc(0.5, 0.0), 2.017, delta=1e-8)
    self.assertAlmostEqual(op5.calc(0.0, 0.5), 1.9589453125000005, delta=1e-8)    
    
    #pf = PoserFile("/home/olivier/vol32G/VIE/rev-param.pz3")
    
  #  word:waveDeformerProp
  def testWave(self):
    pf = PoserFile('srcdata/scenes/MappingCubes+Clothe+Wave.pz3')

    w = pf.getLstFigure()[0].findActor("Wave 1:1")
    chan = w.getChannel("Amplitude")
    self.assertEqual(chan.getPrintName(), 'Amplitude')
    self.assertEqual(chan.getPoserType(), PoserToken.E_waveAmplitude)
    chan = w.getChannel("offset")
    self.assertEqual(chan.getPrintName(), 'Offset')
    self.assertEqual(chan.getPoserType(), PoserToken.E_waveOffset)

    pf.writeFile('tures/MappingCubes+Clothe+Wave.pz3')

  # Unknown word:coneForceFieldProp
  def testWind(self):
    pf = PoserFile('srcdata/scenes/MappingCubes+Clothe+Wind.pz3')
    w = pf.getLstFigure()[0].findActor("ForceField:1")
    chan = w.getChannel("Amplitude")
    self.assertEqual(chan.getPrintName(), 'Amplitude')
    self.assertEqual(chan.getPoserType(), PoserToken.E_forceAmplitude)
    chan = w.getChannel("turbulence")
    self.assertEqual(chan.getPrintName(), 'Turbulence')
    self.assertEqual(chan.getPoserType(), PoserToken.E_simpleFloat)
    pf.writeFile('tures/MappingCubes+Clothe+Wind.pz3')
    
    
  def testCustomData(self):
    pf = PoserFile('srcdata/scenes/TeleSat_Fig.pz3')
    
    # Verif at Global Prop level
    orb = pf.findMeshedObject('Orbite36000')
    ot = orb.getCustomData('OrbiteType')
    self.assertEqual(ot.val, "GEO")
    orb.setCustomData('Altitude', "35786.0")
    
    fig = pf.getLstFigure()[0]
    self.assertEqual(len(fig.getCustomData()), 2)
    ot = fig.getCustomData('OrbiteType')
    self.assertEqual(ot.val, "inclined")
    
    act = fig.findActor('SatCom1-1:1')
    ot = act.getCustomData('OrbiteType')
    self.assertEqual(ot.val, "LEO")
    act.setCustomData('Altitude', "1200.0")
    
    pf.writeFile('tures/TeleSat+customData.pz3')
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    