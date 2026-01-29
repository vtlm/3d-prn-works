from build123d import *
from ocp_vscode import show

r = Rectangle(200, 100)
ro = offset(r, amount=15,openings=[])
f = make_face(ro) - make_face(r)
fe = extrude(f, amount=40 )


r2 = Rectangle(70,70)
r2e = extrude(r2, 50)
r2e_faces=r2e.faces().sort_by(Axis.Z)
r2eo = offset(r2e, amount=3, openings=[r2e_faces[0],r2e_faces[-1]])

show(fe, r2eo)
