import re
from maya import cmds


NODE_ATTR_RE = re.compile("(?P<nodename>[^.]+)[.]vtx[[](?P<index>[0-9]+)[]]")
PLUGIN_NAME = "pointDistance"


def __getNodeAndIndex(tg):
    res = NODE_ATTR_RE.match(tg)
    if res:
        return (res.group("nodename"), int(res.group("index")))
    return (None, None)


def __getSelection():
    selection = cmds.ls(sl=1, fl=1)

    if len(selection) < 2:
        return (None, None)

    tg1 = selection[0]
    tg2 = selection[1]
    if (cmds.objectType(tg1) != "mesh") or\
       (cmds.objectType(tg2) != "mesh"):
       return (None, None)

    if ("vtx" in tg1) == False or\
       ("vtx" in tg2) == False:
       return (None, None)

    return (tg1, tg2)


def __checkPlugin():
    if cmds.pluginInfo(PLUGIN_NAME, q=1, l=1) == False:
        cmds.loadPlugin(PLUGIN_NAME)


def Set():
    __checkPlugin()
    (tg1, tg2) = __getSelection()

    if tg1 == None or tg2 == None:
        cmds.warning("select 2 vertices")
        return None

    (mesh1, index1) = __getNodeAndIndex(tg1)
    (mesh2, index2) = __getNodeAndIndex(tg2)

    if mesh1 == None or index1 == None or mesh2 == None or index2 == None:
        cmds.warning("select 2 vertices")
        return None

    node = cmds.createNode("pointDistance")
    cmds.connectAttr("%s.worldMatrix" % (mesh1), "%s.imx" % (node))
    cmds.connectAttr("%s.outMesh" % (mesh1), "%s.im" % (node))

    if mesh1 != mesh2:
        cmds.connectAttr("%s.worldMatrix" % (mesh2), "%s.amx" % (node))
        cmds.connectAttr("%s.outMesh" % (mesh2), "%s.am" % (node))

    cmds.setAttr("%s.i1" % (node), index1)
    cmds.setAttr("%s.i2" % (node), index2)
    return node



