from build123d import *
from ocp_vscode import show


def bld_comp():
    box=Box(100,50,10)
    box2=Box(100,50,10).move(Location((0,10,0))).rotate(Axis.X,90)

    return Compound(label="Comp1",children=[box,box2])

# with BuildPart() as box:
box=Box(100,50,10)#.rotate(Axis.X,45)
# box.color=Color(0xff0000)
fs= box.faces().filter_by(Axis.Z)
print(fs)
# with BuildPart(f) as marks:
#     f.color=Color(0x0000ff)
#     Box(2,2,10)

# box2=Box(100,50,10).move(Location((0,0,50)))#rotate(Axis.X,45)
# box2.orientation=(-45,0,0)
    # b.orientation=(45,0,0)
comp=bld_comp()
comp2=bld_comp()
cc=comp2.relocate(Location((0,50,0),(0,0,90)))



show(box,#box2,
    #  comp,cc, 
    # marks,
     names=["box","box2","Comp","cc"])
# export_stl(din_fix.part,"din_fix.stl")