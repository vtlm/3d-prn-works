from build123d import *
from ocp_vscode import show

wall_thickness = 3 * MM
fillet_radius = wall_thickness * 0.49

din_thickness = 1.5
din_thickness_gap = 0.5
holder_thickness=2
main_thickness=2

din_height=35
main_height=65
hold_offset=1.5

base_point = (0, 0)
din_thickness_with_gap=din_thickness+din_thickness_gap

with BuildPart() as din_fix:
    # Create the bowl of the cup as a revolved cross section
    with BuildSketch(Plane.XZ) as bowl_section:
        with BuildLine():
            # Polyline((0,0),(0,10),(2,10),(2,0))
            Polyline((0,0), 
                     (0, din_height/2),
                     (din_thickness_with_gap, din_height/2),
                     (din_thickness_with_gap,din_height/2-hold_offset),
                     (din_thickness_with_gap+hold_offset,din_height/2-hold_offset),
                     (din_thickness_with_gap+hold_offset*2,din_height/2),
                     (din_thickness_with_gap+hold_offset*2,din_height/2+holder_thickness),
                     (0, din_height/2+holder_thickness),
                     (0, main_height/2),
                     (-main_thickness, main_height/2),
                     (-main_thickness, 0),
                     (0,0)
                     )
        make_face()  # Create a filled 2D shape
        mirror(about=Plane.XZ)    
    # Hollow out the bowl with openings on the top and bottom
    extrude(amount = 12)
    # mirror(about=Plane.XY) 

show(din_fix, names=["din fix"])
# export_stl(din_fix.part,"din_fix.stl")