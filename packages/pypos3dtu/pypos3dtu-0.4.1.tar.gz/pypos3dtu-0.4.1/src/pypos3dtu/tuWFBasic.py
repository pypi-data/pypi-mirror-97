'''
Created on 8 déc. 2020

@author: olivier
'''
import unittest


from pypos3d.wftk.WFBasic import Point3d, TexCoord2f

class Test(unittest.TestCase):


  def setUp(self):
      pass


  def tearDown(self):
      pass

  def testPoint3dOps(self):
    Orig = Point3d(0.0,0.0,0.0)
    Orig2 = Point3d(Orig)
    Orig3 = Point3d([0.1, 0.0, 0.0])
    
    Orig2.set( (50.0, 50.0, 50.0) )
    
    self.assertTrue(Orig.isNull())
    self.assertFalse(Orig3.isNull())

    p0 = Orig + Point3d(1.0,1.0,1.0)
    self.assertEqual(p0.x, 1.0)
    p1 = Orig - Point3d(1.0,1.0,1.0)
    self.assertEqual(p1.x, -1.0)
    
    p0 = Orig + [1.0,1.0,1.0]
    self.assertEqual(p0.x, 1.0)
    p1 = Orig - [1.0,1.0,1.0]
    self.assertEqual(p1.x, -1.0)
    
    # Java like
    p0.add(Orig, Point3d(1.0,1.0,1.0))
    self.assertEqual(p0.x, 1.0)
    
    p1.sub(Orig, Point3d(1.0,1.0,1.0))
    self.assertEqual(p1.x, -1.0)

    p0.add((1.0,1.0,1.0), Orig)
    self.assertEqual(p0.x, 1.0)
    
    p1.sub((1.0,1.0,1.0), Orig)
    self.assertEqual(p1.x, 1.0)


    d = p0.distanceSquared(p1)
    self.assertEqual(d, 0.0)
    
    d = p0.distanceSquared([ 10.0, -5.0, 4.0 ])
    self.assertEqual(d, 126.0)


  def testTexCoord2fOps(self):
    Orig = TexCoord2f(0.0,0.0)
    Orig2 = TexCoord2f(Orig)
    Orig3 = TexCoord2f([0.1, 0.0])
    
    Orig2.set( (50.0, 50.0) )
    
    self.assertTrue(Orig==TexCoord2f(0.0,0.0))
    #self.assertFalse(Orig3.isNull())

#     p0 = Orig + TexCoord2f(1.0,1.0)
#     self.assertEqual(p0.x, 1.0)
#     p1 = Orig - TexCoord2f(1.0,1.0)
#     self.assertEqual(p1.x, -1.0)
#     
#     p0 = Orig + [1.0,1.0]
#     self.assertEqual(p0.x, 1.0)
#     p1 = Orig - [1.0,1.0,1.0]
#     self.assertEqual(p1.x, -1.0)
    
    # Java like
    p0 = TexCoord2f()
    p0.add(Orig, TexCoord2f(1.0,1.0))
    self.assertEqual(p0.x, 1.0)
    
    p1 = TexCoord2f()
    p1.sub(Orig, TexCoord2f(1.0,1.0))
    self.assertEqual(p1.x, -1.0)

    p0.add((1.0,1.0,1.0), Orig)
    self.assertEqual(p0.x, 1.0)
    
    p1.sub((1.0,1.0,1.0), Orig)
    self.assertEqual(p1.x, 1.0)


#     d = p0.distanceSquared(p1)
#     self.assertEqual(d, 0.0)
#     
#     d = p0.distanceSquared([ 10.0, -5.0, 4.0 ])
#     self.assertEqual(d, 126.0)






if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testPoint3dOps']
    unittest.main()