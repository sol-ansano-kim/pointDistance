from maya.OpenMayaMPx import *
from maya.OpenMaya import *
import sys


PLUGIN_NAME = 'pointDistance'
### this node id from maya sample plugin.
### please change this.
NODE_ID = OpenMaya.MTypeId(0x00085000)


class PointDistance(MPxNode):
    def __init__(self):
        super(PointDistance, self).__init__()

    @staticmethod
    def createor():
        return asMPxPtr(PointDistance())

    @staticmethod
    def initializer():
        num_attr = MFnNumericAttribute()
        type_attr = MFnTypedAttribute()
        matrix_attr = MFnMatrixAttribute()

        PointDistance.index1 = num_attr.create('index1', 'i1',
                                               MFnNumericData.kInt, 0)
        num_attr.setStorable(True)
        num_attr.setMin(0)

        PointDistance.index2 = num_attr.create('index2', 'i2',
                                               MFnNumericData.kInt, 0)
        num_attr.setMin(0)
        num_attr.setStorable(True)

        PointDistance.out_value = num_attr.create('outValue', 'ov',
                                                  MFnNumericData.kFloat, 0.0)
        num_attr.setStorable(False)
        num_attr.setWritable(False)

        PointDistance.in_matrix = matrix_attr.create("inMatrix", "imx")
        matrix_attr.setStorable(True)
        matrix_attr.setHidden(True)

        PointDistance.add_matrix = matrix_attr.create("additionalMatrix", "amx")
        matrix_attr.setStorable(True)
        matrix_attr.setHidden(True)

        PointDistance.in_mesh = type_attr.create('inMesh', 'im',
                                                 MFnMeshData.kMesh)
        type_attr.setStorable(True)
        type_attr.setHidden(True)

        PointDistance.add_mesh = type_attr.create('addtionalMesh', 'adm',
                                                  MFnMeshData.kMesh)
        type_attr.setStorable(True)
        type_attr.setHidden(True)

        PointDistance.addAttribute(PointDistance.index1)
        PointDistance.addAttribute(PointDistance.index2)
        PointDistance.addAttribute(PointDistance.in_mesh)
        PointDistance.addAttribute(PointDistance.add_mesh)
        PointDistance.addAttribute(PointDistance.out_value)
        PointDistance.addAttribute(PointDistance.in_matrix)
        PointDistance.addAttribute(PointDistance.add_matrix)

        PointDistance.attributeAffects(PointDistance.index1,
                                       PointDistance.out_value)
        PointDistance.attributeAffects(PointDistance.index2,
                                       PointDistance.out_value)
        PointDistance.attributeAffects(PointDistance.in_mesh,
                                       PointDistance.out_value)
        PointDistance.attributeAffects(PointDistance.add_mesh,
                                       PointDistance.out_value)
        PointDistance.attributeAffects(PointDistance.in_matrix,
                                       PointDistance.out_value)
        PointDistance.attributeAffects(PointDistance.add_matrix,
                                       PointDistance.out_value)

    def __getVertexPoint(self, mesh, index):
        if 0 <= index < mesh.numVertices():
            pos = MPoint()
            mesh.getPoint(index, pos)
            return pos
        return None

    def __getDistance(self, obj1, obj2, ind1, ind2, mtx1, mtx2):
        node = MFnDependencyNode(self.thisMObject())
        mesh1 = MFnMesh(obj1)
        mesh2 = None

        if (obj2.isNull() == False):
            mesh2 = MFnMesh(obj2)
        pos1 = self.__getVertexPoint(mesh1, ind1)

        if mesh2:
            pos2 = self.__getVertexPoint(mesh2, ind2)
        else:
            pos2 = self.__getVertexPoint(mesh1, ind2)
        if not (pos1) or not (pos2):
            return 0

        if node.findPlug("imx").isConnected():
            pos1 *= mtx1
            if node.findPlug("amx").isConnected():
                pos2 *= mtx2
            pos2 *= mtx1

        return pos2.distanceTo(pos1)

    def compute(self, plug, data):
        if (plug.attribute() == self.out_value):
            index1_in = data.inputValue(self.index1)
            index2_in = data.inputValue(self.index2)
            mesh1_in = data.inputValue(self.in_mesh)
            mesh2_in = data.inputValue(self.add_mesh)
            matrix_in = data.inputValue(self.in_matrix)
            matrix_add_in = data.inputValue(self.add_matrix)
            mesh1_obj = mesh1_in.asMesh()
            mesh2_obj = mesh2_in.asMesh()
            if (mesh1_obj.isNull() == False):
                dis = self.__getDistance(mesh1_obj, mesh2_obj,
                                         index1_in.asInt(), index2_in.asInt(),
                                         matrix_in.asMatrix(),
                                         matrix_add_in.asMatrix())
                out_handle = data.outputValue(self.out_value)
                out_handle.setFloat(dis)
            data.setClean(plug)

def initializePlugin(object):
    mplugin = MFnPlugin(object)
    try:
        mplugin.registerNode(PLUGIN_NAME, NODE_ID,
                             PointDistance.createor, PointDistance.initializer)
    except:
        sys.stderr.write('Failed to register node: %s' % PLUGIN_NAME)
        raise

def uninitializePlugin(object):
    mplugin = MFnPlugin(object)
    try:
        mplugin.deregisterNode(NODE_ID)
    except:
        sys.stderr.write('Failed to deregister node: %s' % PLUGIN_NAME)
        raise