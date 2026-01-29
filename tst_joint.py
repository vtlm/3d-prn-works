from build123d import *
from ocp_vscode import show

with BuildPart() as base:
    Box(20,50,10)

    RigidJoint(label="fix", joint_location=Location((0,25,0),(90,0,0)))

with BuildPart() as box2:
    Box(10,20,5)

    RigidJoint(label="fix", joint_location=Location((0,4,3)))

base.part.joints['fix'].connect_to(box2.joints['fix'])

show(base,box2,["base"], render_joints=True)