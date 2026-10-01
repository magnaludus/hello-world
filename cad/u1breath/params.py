"""Every dimension of U1 Breath in one place (millimetres).

Coordinate frame (shared by every part, all parts are modelled in their
assembled position):
  X  width, 0..172.  The frame is right-handed with Y toward the chamber and
     Z up, so +X runs to your LEFT when you stand in the chamber facing the
     unit (it runs to the right when the unit lies on its back, as printed).
     "Low X" holds the blower, "high X" the electronics bay.
  Y  depth, 0 = back face that mounts flat on the printer's rear wall,
     +Y toward the chamber (front).  Everything is serviced from +Y.
  Z  height, 0 = bottom.  Air flows bottom to top.
"""

# ----------------------------------------------------------------------------
# Overall envelope and generic rules
# ----------------------------------------------------------------------------
UNIT_W = 172.0          # X, overall width of the unit
UNIT_H = 273.0          # Z, overall height of the unit
ENVELOPE_MAX_W = 175.0  # X, test limit (Panda Breath class envelope)
ENVELOPE_MAX_D = 55.0   # Y, test limit for total depth
ENVELOPE_MAX_H = 273.0  # Z, test limit
BUILD_VOLUME = 256.0    # Snapmaker U1 build volume, every printed part must fit a cube of this

WALL = 3.0              # default wall thickness of the ASA shells
SLIDE_CLEAR = 0.3       # clearance on every sliding fit (filters, cartridge, cover)
PRESS_CLEAR = 0.15      # clearance on every press fit (grille snap nubs)

INSERT_HOLE_D = 4.0     # hole for an M3 heat-set insert
INSERT_DEPTH = 6.0      # depth of the insert bosses
BOSS_SIZE = 8.0         # square boss cross section around an M3 insert
M3_CLEAR_D = 3.4        # M3 button screw clearance hole
M4_CLEAR_D = 4.5        # M4 clearance hole (rear wall mounting)
M4_CSK_D = 9.0          # countersink diameter for the M4 flat-head mounting screws
M2_INSERT_HOLE_D = 3.2  # hole for an M2 heat-set insert (carbon cartridge lid)
M2_CLEAR_D = 2.4        # M2 screw clearance hole

# ----------------------------------------------------------------------------
# Back plate (Y 0..3), spans the whole unit
# ----------------------------------------------------------------------------
BACK_PLATE_T = 3.0
BACK_PLATE_W = UNIT_W
BACK_PLATE_H = UNIT_H
# The full 273 mm plate does not fit the 256 mm build volume, so it is printed
# as two halves joined by a half-thickness lap joint at BACK_PLATE_SPLIT_Z.
BACK_PLATE_SPLIT_Z = 140.0
BACK_PLATE_LAP = 10.0   # Z length of the lap joint overlap
# Rear-wall mounting pattern.  Pick whichever holes match your printer wall.
MOUNT_GRID_X = (10.0, UNIT_W - 10.0)                     # two vertical columns
MOUNT_GRID_Z = tuple(float(z) for z in range(20, 261, 20))  # 20 mm pitch
MOUNT_HOLES = [(x, z) for x in MOUNT_GRID_X for z in MOUNT_GRID_Z]  # 4.5 mm holes
MOUNT_CSK_HOLES = [                  # countersunk M4 clearance holes, explicit
    (30.0, 30.0), (142.0, 30.0),
    (30.0, 136.5), (142.0, 136.5),
    (30.0, 243.0), (142.0, 243.0),
]
# Section bodies attach to the back plate with M3 inserts in boss columns that
# run the full cavity depth (so they print as plain columns, front face down).
# Centres are chosen to clear the 20 mm mounting grid at X = 10 / 162.
ATTACH_POINTS = {
    "filter": [(x, z) for x in (18.0, UNIT_W - 18.0) for z in (7.5, 102.5)],
    "mid":    [(x, z) for x in (7.0, UNIT_W - 7.0) for z in (130.0, 170.0)],
    "heater": [(x, z) for x in (6.0, UNIT_W - 6.0) for z in (203.0, 263.0)],
}

# ----------------------------------------------------------------------------
# Section 1, filter bay (Z 0..110)
# ----------------------------------------------------------------------------
FILTER_Z0 = 0.0
FILTER_Z1 = 110.0
BAYS = 2
HEPA_W = 80.0           # X, one HEPA cell
HEPA_H = 40.0           # Z, one HEPA cell
HEPA_T = 15.0           # Y, HEPA cell thickness
CELLS_PER_BAY = 2       # two cells stacked in Z make the 80 x 80 face
CARBON_T = 15.0         # Y, carbon cartridge thickness (slot depth)
CARBON_MESH_PITCH = 2.0 # size of the square mesh openings of the cartridge faces
CARBON_MESH_BAR = 1.0   # bar between mesh openings
PLENUM_T = 12.0         # Y, plenum behind the HEPA cells
GRILLE_T = 3.0          # Y, intake grille thickness
GRILLE_SLOT_W = 5.0     # width of the grille slots
GRILLE_SLOT_BAR = 2.0   # bar between grille slots
FRONT_LIP = 2.0         # extra front frame thickness (front wall = WALL + FRONT_LIP)
HEPA_RETAINER_T = 3.0   # Y, retainer frame behind the HEPA cells (adds to depth)
BAY_OPEN = HEPA_W       # 80 x 80 bay opening (X x Z)
BAY_DIVIDER = 3.0       # wall between the two bays
BAY_X0 = (UNIT_W - (BAYS * BAY_OPEN + (BAYS - 1) * BAY_DIVIDER)) / 2.0  # 4.5
BAY_Z0 = 15.0           # bottom of the bay openings
BAY_X = [BAY_X0 + i * (BAY_OPEN + BAY_DIVIDER) for i in range(BAYS)]
# Depth stack of the filter bay, from the back
FILTER_PLENUM_Y0 = BACK_PLATE_T                      # 3
FILTER_RETAINER_Y0 = FILTER_PLENUM_Y0 + PLENUM_T     # 15
FILTER_HEPA_Y0 = FILTER_RETAINER_Y0 + HEPA_RETAINER_T  # 18
FILTER_CARBON_Y0 = FILTER_HEPA_Y0 + HEPA_T           # 33
FILTER_GRILLE_Y0 = FILTER_CARBON_Y0 + CARBON_T       # 48
FILTER_FRONT_Y0 = FILTER_GRILLE_Y0                   # front wall starts where the grille sits
FILTER_Y1 = FILTER_GRILLE_Y0 + WALL + FRONT_LIP      # 53, front face of the filter bay
GRILLE_NUB = 1.0        # snap nub height on the grille edges
GRILLE_NUB_L = 8.0      # snap nub length
RETAINER_STOP_LIP = 1.5 # inward lip at the back of each bay bore that the retainer frame rests on
# Carbon cartridge (separate printed box)
CARBON_BOX = 79.5       # X and Z outer size of the cartridge
CARBON_WALL = 2.0       # cartridge side wall
CARBON_MESH_T = 1.5     # thickness of the mesh faces
CARBON_LID_T = 2.0      # lid thickness (lid is one of the two mesh faces)
CARBON_BOSS = 6.0       # square boss for the M2 lid inserts
# Crossover duct: opening in the roof of the filter bay into the mid section
DUCT_X0 = WALL
DUCT_X1 = 88.0          # = left edge of the mid-section partition
DUCT_Y0 = FILTER_RETAINER_Y0
DUCT_Y1 = 45.0

# ----------------------------------------------------------------------------
# Section 2, blower + electronics (Z 110..195)
# ----------------------------------------------------------------------------
MID_Z0 = FILTER_Z1      # 110
MID_Z1 = 195.0
BLOWER_W = 75.0         # X, 7530 blower
BLOWER_H = 75.0         # Z
BLOWER_T = 30.0         # Y
BLOWER_INLET_PLENUM = 12.0  # Y, space in front of the inlet face
BLOWER_MOUNT_SQ = 64.0  # M4 mounting holes on a 64 mm square
BLOWER_MOUNT_D = 4.5
BLOWER_OUTLET_W = 30.0  # X extent of the rectangular outlet
BLOWER_OUTLET_D = 25.0  # Y extent of the rectangular outlet
MID_Y1 = BACK_PLATE_T + BLOWER_T + BLOWER_INLET_PLENUM + WALL  # 48, front face
PARTITION_X0 = 88.0     # wall between the blower cavity and the electronics bay
PARTITION_T = WALL
BLOWER_X0 = 11.5        # blower body left edge (clears the 8 mm boss columns)
BLOWER_Z0 = MID_Z0 + WALL + 2.0  # 115, blower body bottom
BLOWER_CX = BLOWER_X0 + BLOWER_W / 2.0
BLOWER_CZ = BLOWER_Z0 + BLOWER_H / 2.0
BLOWER_OUTLET_X0 = BLOWER_X0 + 2.0  # outlet rectangle (points +Z through the roof)
BLOWER_OUTLET_Y0 = BACK_PLATE_T + (BLOWER_T - BLOWER_OUTLET_D) / 2.0  # 5.5
ELEC_X0 = PARTITION_X0 + PARTITION_T  # 91, electronics cavity
ELEC_X1 = UNIT_W - WALL               # 169
ELEC_Z0 = MID_Z0 + WALL               # 113
ELEC_Z1 = MID_Z1 - WALL               # 192
ELEC_Y0 = BACK_PLATE_T                # 3 (components stand on the back plate)
ELEC_Y1 = MID_Y1 - WALL               # 45, inside face of the cover
COVER_T = WALL
# Electronics keep-out boxes: (name, x0, z0, w (X), h (Z), depth (Y)) in the
# assembled frame; components mount on standoff bosses on the back plate.
ELEC_KEEPOUTS = [
    ("hlk_10m24",    94.0, 166.0, 38.0, 23.0, 18.0),
    ("terminal_blk", 135.0, 178.0, 30.0, 12.0, 15.0),
    ("buck",         136.0, 160.0, 22.0, 17.0, 10.0),
    ("fuse_holder",  136.0, 146.0, 30.0, 12.0, 15.0),
    ("ssr_carrier",  94.0, 140.0, 40.0, 20.0, 20.0),
    ("xiao_esp32c3", 94.0, 118.0, 21.0, 17.5, 8.0),
    ("mosfet",       118.0, 118.0, 30.0, 15.0, 10.0),
]
STANDOFF_D = 6.0        # standoff boss diameter on the back plate
STANDOFF_H = 4.0        # standoff height above the back plate
STANDOFF_HOLE_D = 2.0   # pilot hole for M2.5 self-tapping screws
STANDOFF_INSET = 3.0    # standoff centre inset from the keep-out corners
PG7_HOLE_D = 12.5       # cord grip through the right wall near the bottom
PG7_Y = 24.0
PG7_Z = MID_Z0 + 30.0
JST_SLOT_W = 8.0        # JST-XH 2-pin bed-probe connector slot in the cover
JST_SLOT_H = 6.0
JST_X0 = 126.0
JST_Z0 = ELEC_Z0 + 5.0
LED_WINDOW = 10.0       # status LED window in the cover
LED_X0 = 100.0
LED_Z0 = 175.0
COVER_BOSS_INSET = 4.0  # cover boss centre inset from the cavity corners

# ----------------------------------------------------------------------------
# Section 3, heater (Z 195..273)
# ----------------------------------------------------------------------------
HEATER_Z0 = MID_Z1      # 195
HEATER_Z1 = UNIT_H      # 273
PTC_L = 150.0           # X, finned PTC element length
PTC_D = 32.0            # Y, element depth (airflow direction)
PTC_H = 26.0            # Z, element height
PTC_CLEAR = 1.0         # clearance between the element and the liner, per side
LINER_T = 1.0           # aluminium sheet thickness
HOT_GAP = 8.0           # air gap kept between the liner's inner volume and any plastic
HEATER_PLENUM_T = 8.0   # Y, plenum between the liner back wall and the element
HEATER_SIDE_WALL = 2.0  # the shell side walls are thinner so the 8 mm gap fits in 172 mm
LINER_LIP = 16.0        # outward lips on the top/bottom liner walls (screw flanges)
LINER_TAB = 10.0        # corner tabs on the side walls (riveted/screwed to top and bottom)
# Depth stack: back plate 3 | gap 8 | liner 1 | plenum 8 | element 32 | lips 1 | plate 1
LINER_IN_Y0 = BACK_PLATE_T + HOT_GAP + LINER_T      # 12, inner back face of the liner
LINER_IN_Y1 = LINER_IN_Y0 + HEATER_PLENUM_T + PTC_D # 52, front edge of the liner box
LINER_IN_X0 = (UNIT_W - (PTC_L + 2 * PTC_CLEAR)) / 2.0  # 10
LINER_IN_X1 = UNIT_W - LINER_IN_X0                   # 162
LINER_IN_Z0 = 216.0                                  # inner bottom of the liner
LINER_IN_Z1 = LINER_IN_Z0 + PTC_H + 2 * PTC_CLEAR    # 244
LINER_PLATE_T = LINER_T                              # slotted outlet plate (front face)
HEATER_Y1 = LINER_IN_Y1 + LINER_T + LINER_PLATE_T    # 54, the front face of the unit
HEATER_DEPTH = HEATER_Y1                             # asserted <= 55 in the tests
SHELL_FRONT_Y1 = LINER_IN_Y1                         # 52, shell front frame face (lips sit on it)
SHELL_FRONT_Y0 = SHELL_FRONT_Y1 - WALL               # 49
LINER_INLET_X0 = 20.0   # inlet slot in the liner bottom wall (over the plenum)
LINER_INLET_X1 = 152.0
LINER_SLOT_W = 3.0      # outlet slots in the front plate
LINER_SLOT_PITCH = 6.0
LINER_SLOT_X0 = 20.0
LINER_SLOT_X1 = 152.0
LINER_SCREW_X = (30.0, 142.0)       # screws through the plate + lips into shell bosses
LINER_SCREW_Z = (203.0, 256.0)      # bottom lip / top lip screw rows
LINER_SCREW_D = 3.4
PROTECTOR_HOLE = (86.0, 36.0)       # bimetal thermal protector M3 hole on the outer top face (X, Y)
NTC_HOLE_Y = 36.0                   # ring-lug NTC M3 hole on the outer right side face (Y)
PTC_LEAD_HOLE_D = 8.0               # element lead grommet hole in the left side wall
PTC_LEAD_HOLE_Y = 30.0
