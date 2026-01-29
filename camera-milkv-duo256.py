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

HR911105A_height=13.5


def build_fix_angle():
    with BuildPart() as fix:
        Box(30,30,30)
        # with BuildSketch():
        #     with BuildLine():
        #         Polyline(
        #             (20,0),
        #             (0,0),
        #             (0,5),
        #             (20,25),
        #             (20,0)
        #         )
        #     make_face()
        # extrude(amount=2)
        RigidJoint(label='fix',joint_location=Location((5,0,1)))

    return fix


def build_eth_socket_HR911105A(width=16, length=21.5, height=13.5):
    with BuildPart() as socket:
        box=Box(width, length, height)
        RigidJoint(label='fix', joint_location=Location((0,-length/2,-height/2)))
        # far_face=faces().filter_by(Axis.Y)[-1]
        # f2=far_face.
        # face=Face()
        #box.faces()[0].label = 'plug'#.filter_by(Axis.Y)[0].label='plug'
        # print('faces',box.faces())
        # for f in box.faces():
        #     f.label="sfdws"
        #     print("f label", f, f.label)
        # for f in box.faces():
        #     # f.label="sfdws"
        #     print("f label", f, f.label)
    return socket

def build_pin_header(width=0.6, height=12):
    with BuildPart() as pin:
        box=Box(width, width, height)
        RigidJoint(label='fix', joint_location=Location((0,0,-height*4/(5*2))))#/2 because centered
    return pin


# HanRun HR911105A 
# dims 16 x 13.5 x 21.4
# tot h 15.3 mm
# socket out 2.5 mm
def build_eth_board_as_compound(board_width=20, board_length=30, board_thickness=1.7,
                                plane=Plane.XY):
    out_shift=2.5
    pin_header_in_shift=3

    fix_angle = build_fix_angle()

    eth_socket=build_eth_socket_HR911105A()
    # for f in eth_socket.faces():
    #     print('label=',f.label)
    pin_header1=build_pin_header()

    with BuildPart(plane) as eth_board:
        board=Box(board_width, board_length ,board_thickness)
        RigidJoint(label='fix_eth_socket', joint_location=Location((0,-board_length/2-out_shift,15.3-HR911105A_height-board_thickness/2)))
        RigidJoint(label='fix_pin_header', joint_location=Location((0,board_length/2-pin_header_in_shift,0)))
        RigidJoint(label='fix_stand', joint_location=Location((0,board_length,0)))

    eth_board.joints['fix_eth_socket'].connect_to(eth_socket.joints['fix'])
    eth_board.joints['fix_pin_header'].connect_to(pin_header1.joints['fix'])
    eth_board.joints['fix_stand'].connect_to(fix_angle.joints['fix'])

    eth_board_comp = Compound(label="eth_boardc", children=[board,eth_socket.part,pin_header1.part])
    joint=RigidJoint(label="fix", to_part=eth_board_comp, joint_location=Location((0,board_length/2-pin_header_in_shift,0),(0,180,0)))
    eth_board_comp.joints['fix']=joint

    return eth_board_comp

# 8.5 + 2.7
header_socket_height=8.5
header_pin_height=2.7


def build_header_socket(width=15, length=2.7, height=8.5, plane=Plane.XY):
    with BuildPart(plane) as board:
        socket=Box(width, length, height)
        RigidJoint(label="fix_bottom_center", joint_location=Location((0,0,-height/2)))
        RigidJoint(label="fix_top_center", joint_location=Location((0,0,height/2),(0,0,0)))
    for it in board.faces().filter_by(Axis.Z):
        it.color =Color(0xff0000)
    return board


def build_MPU_board(width=20, length=50, thickness=1.5, plane=Plane.XY):
    with BuildPart(plane) as board:
        MPU_board=Box(width, length, thickness)
        RigidJoint(label="eth_socket", joint_location=Location((0,length/2,thickness/2),(-90,0,0)))
        RigidJoint("center")

    # header_socket=build_header_socket()
    # b
    return board

def assemble_MPU_board():
    header_socket=build_header_socket()
    eth_board_c = build_eth_board_as_compound()
    MPU_board = build_MPU_board()

    MPU_board.joints['eth_socket'].connect_to(header_socket.joints['fix_bottom_center'])
    header_socket.joints['fix_top_center'].connect_to(eth_board_c.joints['fix'])

    MPU_board_asm=Compound([header_socket.part, eth_board_c, MPU_board.part])
    joint=RigidJoint(label='fix',to_part=MPU_board_asm,joint_location=Location((0,0,-2.7)))
    MPU_board_asm.joints['fix']=joint

    return MPU_board_asm



def build_main_board(width=30, length=70, thickness=1.5, plane=Plane.XY):
    MPU_board_y_shift=0
    with BuildPart(plane) as board:
        MPU_board=Box(width, length, thickness)
        RigidJoint(label="fix_MPU_board", 
                   joint_location=Location((0,MPU_board_y_shift,header_socket_height+header_pin_height+thickness/2)))
    return board

def assemble_main_board():
    
    main_board=build_main_board()
    MPU_board_asm=assemble_MPU_board()

    main_board.joints['fix_MPU_board'].connect_to(MPU_board_asm.joints['fix'])

    main_board_asm = Compound([main_board.part, MPU_board_asm])
    joint=RigidJoint(label='fix',to_part=main_board_asm,joint_location=Location((0,0,0)))
    main_board_asm.joints['fix']=joint

    return main_board_asm



def build_boards(plane=Plane.XY):

    MPU_board = build_MPU_board()
    main_board = build_main_board()
    main_board.joints['fix_MPU_board'].connect_to(MPU_board.joints['center'])
    # with BuildPart(plane) as boards:
    #     main_board=Box(30,70,1.5)
        
    #     with Locations((0,7.4,10)):
    #         MPU_board=Box(20,50,1.5)

    #     face = MPU_board.faces().sort_by(Axis.Y)[-1]
    #     with BuildPart(face):
    #         eth_conn=Box(15,8.5,2.7,rotation=(0,90,90),align=[Align.CENTER,Align.MIN,Align.MIN])

    #     # face = eth_conn.faces().sort_by(Axis.Y)[-1]
    #     # eth_board = build_eth_board(face)#*Pos(0,0,-40))
    #     # boards.part += eth_board.part
    #     RigidJoint(label="fix", joint_location=Location((0,40,0),(90,0,0)))

    boards = Compound([MPU_board.part, main_board.part])

    return boards

class EthBoard(Compound):
    def __init__(self):
        
        with BuildPart() as pin:
            board1=Box(20,20,4)
        # with BuildPart() as pin2:
            board=Box(10,30,10)

        # joint=RigidJoint(label='fix', to_part=self, joint_location=Location((0,10,5)))
        super().__init__()
        self.children=[pin.part]
        RigidJoint(label="fix", to_part=self, joint_location=Location((0,20,15)))


def build_camera_module():

    with BuildPart(Plane.XY*Pos(0,-40,0)) as camera_module:

        cam_board = Box(27,1,17,align=[Align.CENTER,Align.MAX,Align.CENTER])

        with Locations((0,-1,0)):
            matrix_sensor_base=Box(17,3.5,17,align=[Align.CENTER,Align.MAX,Align.CENTER])

        with Locations((0,-1-3.5,0)):
            lens_tube=Cylinder(7.25,19,rotation=(-90,0,0),align=[Align.CENTER,Align.CENTER,Align.MAX])
        with Locations((0,-24,0)):
            Cylinder(5,2,rotation=(-90,0,0),align=[Align.CENTER,Align.CENTER,Align.CENTER],mode=Mode.SUBTRACT)

    return camera_module



with BuildLine() as axY:
    Line((0,-100),(0,100))
with BuildLine(Plane.YZ) as axZ:
    Line((0,-100),(0,100))
with BuildLine() as axX:
    Line((-100,0),(100,0))


with BuildPart(Plane.ZY*Pos(0,0,20)) as MPU_board:
    mainboard=Box(50,70,1)
    with Locations((0,0,-11)):
        cam_board=Box(21,51,1)
    with Locations((0,26.5,-11)):
        eth_conn=Box(15,8.5,2.7,align=[Align.CENTER,Align.MIN,Align.MAX])

# with BuildPart(Plane.XZ*Pos(0,0,-40)) as eth_board:
#     board=Box(20,30,1.5)
#     with Locations((0,-7,0)):
#         eth_socket=Box(16,21.5,13,align=[Align.CENTER,Align.CENTER,Align.MIN])
#     # with Locations((0,0,-11)):
#     #     cam_board=Box(21,51,1)
#     # with Locations((0,26.5,-11)):
#     #     eth_conn=Box(15,8.5,2.7,align=[Align.CENTER,Align.MIN,Align.MAX])
#     # # mainboard.position=(-20,20,20)


camera_module=build_camera_module()
main_board_asm = assemble_main_board()
print(main_board_asm.faces().filter_by(Axis.Z))

for it in main_board_asm.faces().filter_by(Axis.Z):
    it.color =Color(0xff0000)
# boards = build_boards()


# boards.part.joints['fix'].connect_to(eth_board_c.joints['fix'])
# boards.part.joints['fix'].connect_to(box2.joints['fix'])
# boards.part.joints['fix'].connect_to(ethBoard.joints['fix'])

face=main_board_asm.faces().filter_by(Axis.Z)[-1]

# with BuildLine(face.global_location):
with BuildLine(face.global_location):
    mline=Line((-10,0),(10,0))

length, width, thickness = 80.0, 60.0, 10.0
case_inner_width=50
case_inner_height=50
case_inner_length=100
case_fillet_radius=5
# with BuildPart(Plane.ZY*Pos(0,50,0)) as case:
with BuildPart() as case:
    with BuildSketch(Plane.XZ*Pos(0,0,-40)) as base:
        with BuildLine() as line:
            # FilletPolyline((-50,50),(50,50),(50,-50), (-50,-50),radius=5, close=True)
            l=FilletPolyline((0,case_inner_height/2),
                           (case_inner_width/2,case_inner_height/2),
                           (case_inner_width/2,0),radius=case_fillet_radius)
            l2=offset(l,amount=1,side=Side.LEFT)
        make_face()
    p=extrude(amount=case_inner_length)
    p2=mirror(p,about = Plane.XY)
    p3=mirror([p,p2],about = Plane.YZ)

    RigidJoint(label="main_board_fix",joint_location=Location((0,0,20),(180,0,180)))

    
case.joints['main_board_fix'].connect_to(main_board_asm.joints['fix'])

all_asm=Compound([case.part, main_board_asm])

def build_line(st,end,plane=Plane.XY):
    with BuildLine(plane) as line:
        Line(st, end)
    return line

facesz=all_asm.faces().filter_by(Axis.Z)

faces=all_asm.faces().filter_by(Axis.Z)
# ind=faces.index()


fz=[f for f in all_asm.faces() if abs(f.area - 16*13.5) <1e-6]
fzs=sorted(fz, key=lambda f: f.location.position.center().Z)
print('fz=',fz)

lines=[ build_line((-20,0),(20,0),fz[0])]# for f in fz ]

wire_offsetted = fz[0].wire().offset_2d(distance=0.5, kind=Kind.TANGENT)
face = Face(wire_offsetted)
cut_box=extrude(face, -20)
case_cutted = case.part - cut_box
hole_edges = new_edges(case.part, combined=case_cutted)
print("hole_edges=",hole_edges)

hole_top_face = case_cutted.faces().filter_by(lambda f: len(f.inner_wires()) == 1).sort_by(Axis.Z)[1]
print("hole_top_face=", hole_top_face)

wire_inn = hole_top_face.inner_wires()[-1]
print("wire_inn", wire_inn)
wire_out = wire_inn.offset_2d(1,kind=Kind.TANGENT)
f = make_face(wire_out)-make_face(wire_inn)
fe=extrude(f,2.5)
# feo=fe.offset_3d(thickness=1, openings=fe.faces().sort_by(Axis.Z)[-1])


case_back_face_inner_wire = case.faces().sort_by(Axis.Y)[-1].inner_wires()[0]
face=make_face(case_back_face_inner_wire)



show(
    axX,axY,axZ,
    fe,
    lines,
    mline,
    camera_module, 
     main_board_asm, 
     face,
    #  boards,
    #  ethBoard
    #  eth_board_c, 
    #  box2,
    #  eth_board1, 
    #  eb2r,
     case_cutted,
    #  names=["din fix","matrix_sensor_base","lens_tube","MPU_board","case"]
    # ,
    render_joints=True,
    ortho=False,
    transparent=True
     )
# export_stl(din_fix.part,"din_fix.stl")