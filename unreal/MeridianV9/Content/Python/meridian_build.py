# ============================================================
#  MERIDIAN DATA INFRASTRUCTURE v9 - UNREAL ENGINE SCENE BUILDER
#  Original concept: Brandon (Vaddix123) - Kingdom Merry Protocol lineage
#
#  Constructs the full v9 facility as a saved level:
#  SOFC array (115 MW) - back-pressure steam turbine - ORC -
#  carbon capture plant - BESS - greenhouses - DC - water systems -
#  wetland - LFG flare - substation - flow piping - Lumen lighting.
#
#  Coordinates mirror the web model (index.html) 1:1.
#  Units: web meters -> UE centimeters (x100).
#  Axis map: web(x, y-up, z) -> UE(X=x, Y=z, Z=y).
#
#  Compatible UE 5.0 - 5.4 (defensive API usage throughout).
# ============================================================
import math
import unreal

CONTENT_DIR = "/Game/Meridian"
MAT_DIR = CONTENT_DIR + "/Materials"
LEVEL_ASSET = CONTENT_DIR + "/MeridianFacility"

# ---------- subsystem-agnostic helpers ----------

def _lvl_subsys():
    try:
        return unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    except Exception:
        return None

def _actor_subsys():
    try:
        return unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    except Exception:
        return None

def new_level(path):
    ls = _lvl_subsys()
    if ls:
        try:
            return ls.new_level(path)
        except Exception:
            pass
    return unreal.EditorLevelLibrary.new_level(path)

def save_level():
    ls = _lvl_subsys()
    if ls:
        try:
            ls.save_current_level()
            return
        except Exception:
            pass
    unreal.EditorLevelLibrary.save_current_level()

def spawn(cls, loc=(0, 0, 0), rot=(0, 0, 0)):
    l = unreal.Vector(loc[0], loc[1], loc[2])
    r = unreal.Rotator(rot[0], rot[1], rot[2])  # roll, pitch, yaw
    a = _actor_subsys()
    if a:
        try:
            return a.spawn_actor_from_class(cls, l, r)
        except Exception:
            pass
    return unreal.EditorLevelLibrary.spawn_actor_from_class(cls, l, r)

def _mesh(path, fallback=None):
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        return unreal.load_asset(path)
    if fallback:
        return unreal.load_asset(fallback)
    return None

MESH_CUBE = "/Engine/BasicShapes/Cube"
MESH_CYL = "/Engine/BasicShapes/Cylinder"
MESH_SPHERE = "/Engine/BasicShapes/Sphere"
MESH_CONE = "/Engine/BasicShapes/Cone"
MESH_PLANE = "/Engine/BasicShapes/Plane"

_actor_count = 0

def _place(mesh_path, material, loc, rot, scale, label, folder):
    global _actor_count
    mesh = _mesh(mesh_path, MESH_CYL)
    actor = spawn(unreal.StaticMeshActor, loc, rot)
    try:
        comp = actor.static_mesh_component
    except Exception:
        comp = actor.get_editor_property("static_mesh_component")
    comp.set_static_mesh(mesh)
    if material:
        comp.set_material(0, material)
    actor.set_actor_scale3d(unreal.Vector(scale[0], scale[1], scale[2]))
    try:
        actor.set_actor_label(label)
        actor.set_folder_path(unreal.Name("Meridian/" + folder))
    except Exception:
        pass
    _actor_count += 1
    return actor

# web meters -> UE cm; axis map (x, y-up, z) -> (X, Y=z, Z=y)
def box(x, z, y_bottom, w, h, d, material, label, folder, yaw=0.0):
    return _place(MESH_CUBE, material,
                  (x * 100.0, z * 100.0, (y_bottom + h / 2.0) * 100.0),
                  (0, 0, yaw), (w, d, h), label, folder)

def cyl(x, z, y_bottom, radius, height, material, label, folder):
    return _place(MESH_CYL, material,
                  (x * 100.0, z * 100.0, (y_bottom + height / 2.0) * 100.0),
                  (0, 0, 0), (radius * 2.0, radius * 2.0, height), label, folder)

def sphere(x, z, y_center, radius, material, label, folder, squash=1.0):
    return _place(MESH_SPHERE, material,
                  (x * 100.0, z * 100.0, y_center * 100.0),
                  (0, 0, 0), (radius * 2.0, radius * 2.0, radius * 2.0 * squash),
                  label, folder)

def pipe(x1, z1, x2, z2, y, radius, material, label, folder):
    dx, dz = x2 - x1, z2 - z1
    length = math.sqrt(dx * dx + dz * dz)
    yaw = math.degrees(math.atan2(dz, dx))
    return _place(MESH_CYL, material,
                  ((x1 + x2) * 50.0, (z1 + z2) * 50.0, y * 100.0),
                  (0, 90, yaw), (radius * 2.0, radius * 2.0, length),
                  label, folder)

# ---------- materials ----------

_mats = {}

def mat(name, color, metallic=0.0, roughness=0.6, emissive=None,
        emissive_mult=1.0, opacity=None):
    if name in _mats:
        return _mats[name]
    path = MAT_DIR + "/" + name
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        m = unreal.load_asset(path)
        _mats[name] = m
        return m
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    m = tools.create_asset(name, MAT_DIR, unreal.Material,
                           unreal.MaterialFactoryNew())
    mel = unreal.MaterialEditingLibrary

    c = mel.create_material_expression(
        m, unreal.MaterialExpressionConstant3Vector, -400, 0)
    c.set_editor_property("constant",
        unreal.LinearColor(color[0], color[1], color[2], 1.0))
    mel.connect_material_property(c, "", unreal.MaterialProperty.MP_BASE_COLOR)

    met = mel.create_material_expression(
        m, unreal.MaterialExpressionConstant, -400, 180)
    met.set_editor_property("r", metallic)
    mel.connect_material_property(met, "", unreal.MaterialProperty.MP_METALLIC)

    rgh = mel.create_material_expression(
        m, unreal.MaterialExpressionConstant, -400, 300)
    rgh.set_editor_property("r", roughness)
    mel.connect_material_property(rgh, "", unreal.MaterialProperty.MP_ROUGHNESS)

    if emissive:
        e = mel.create_material_expression(
            m, unreal.MaterialExpressionConstant3Vector, -400, 420)
        e.set_editor_property("constant", unreal.LinearColor(
            emissive[0] * emissive_mult, emissive[1] * emissive_mult,
            emissive[2] * emissive_mult, 1.0))
        mel.connect_material_property(
            e, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)

    if opacity is not None:
        try:
            m.set_editor_property("blend_mode", unreal.BlendMode.BLEND_TRANSLUCENT)
            o = mel.create_material_expression(
                m, unreal.MaterialExpressionConstant, -400, 560)
            o.set_editor_property("r", opacity)
            mel.connect_material_property(
                o, "", unreal.MaterialProperty.MP_OPACITY)
        except Exception as ex:
            unreal.log_warning("translucent setup failed for {}: {}".format(name, ex))

    mel.recompile_material(m)
    unreal.EditorAssetLibrary.save_asset(path)
    _mats[name] = m
    return m

def build_materials():
    mat("M_Ground",      (0.045, 0.055, 0.075), 0.0, 0.95)
    mat("M_Pad",         (0.16, 0.17, 0.19),    0.0, 0.90)
    mat("M_Steel",       (0.50, 0.52, 0.55),    0.85, 0.35)
    mat("M_SteelDark",   (0.20, 0.22, 0.26),    0.70, 0.50)
    mat("M_White",       (0.85, 0.86, 0.88),    0.30, 0.40)
    mat("M_GoldSOFC",    (0.55, 0.42, 0.15),    0.50, 0.50)
    mat("M_DCBlue",      (0.10, 0.16, 0.28),    0.20, 0.60)
    mat("M_Transformer", (0.10, 0.20, 0.11),    0.50, 0.55)
    mat("M_Copper",      (0.55, 0.30, 0.12),    0.70, 0.40)
    mat("M_TankCyan",    (0.14, 0.38, 0.48),    0.50, 0.45)
    mat("M_Concrete",    (0.35, 0.35, 0.36),    0.00, 0.85)
    mat("M_Soil",        (0.13, 0.10, 0.06),    0.00, 1.00)
    mat("M_LandfillGrass", (0.10, 0.15, 0.06),  0.00, 1.00)
    mat("M_WindowGlow",  (0.05, 0.10, 0.20), 0.0, 0.4, (0.25, 0.55, 1.0), 25.0)
    mat("M_StatusGreen", (0.05, 0.20, 0.08), 0.0, 0.5, (0.20, 1.00, 0.40), 20.0)
    mat("M_FlameCore",   (1.00, 0.50, 0.10), 0.0, 0.9, (1.00, 0.42, 0.06), 90.0)
    mat("M_FlameTip",    (1.00, 0.80, 0.30), 0.0, 0.9, (1.00, 0.75, 0.25), 60.0)
    mat("M_Water",       (0.06, 0.25, 0.30), 0.6, 0.10, (0.02, 0.10, 0.12), 1.5, 0.75)
    mat("M_Glass",       (0.70, 0.85, 0.75), 0.1, 0.15, (0.9, 0.75, 0.45), 0.6, 0.35)
    mat("M_PipeAmber",   (0.60, 0.38, 0.12), 0.6, 0.40, (0.55, 0.30, 0.08), 2.0)
    mat("M_PipeSteam",   (0.75, 0.77, 0.85), 0.7, 0.30, (0.60, 0.62, 0.75), 1.5)
    mat("M_PipeGreen",   (0.20, 0.55, 0.30), 0.5, 0.40, (0.15, 0.55, 0.25), 2.0)
    mat("M_PipeCyan",    (0.15, 0.50, 0.60), 0.5, 0.40, (0.10, 0.45, 0.55), 2.0)
    mat("M_PipePurple",  (0.45, 0.35, 0.60), 0.5, 0.40, (0.40, 0.28, 0.55), 1.5)
    mat("M_PipeWhite",   (0.88, 0.92, 0.94), 0.6, 0.30, (0.70, 0.75, 0.78), 1.2)

def M(name):
    return _mats[name]

# ---------- subsystems (coordinates mirror index.html v9) ----------

def build_ground():
    box(0, 0, -0.5, 1400, 0.5, 1400, M("M_Ground"), "Ground", "Site")

def build_sofc():  # (-60,-50)
    cx, cz = -60, -50
    box(cx, cz, 0, 80, 1, 60, M("M_Pad"), "SOFC_Pad", "SOFC")
    for r in range(3):
        for c in range(3):
            mx = cx - 22 + c * 22
            mz = cz - 18 + r * 18
            n = "SOFC_{}{}".format(r, c)
            box(mx, mz, 1, 14, 7, 10, M("M_GoldSOFC"), n, "SOFC")
            box(mx, mz, 8.0, 14.8, 0.4, 10.8, M("M_SteelDark"), n + "_roof", "SOFC")
            cyl(mx + 5, mz, 8.4, 0.7, 4, M("M_Steel"), n + "_stack", "SOFC")
    cyl(cx, cz - 30, 1, 3, 25, M("M_Steel"), "SOFC_Manifold", "SOFC")
    sphere(cx, cz - 30, 27.5, 2.2, M("M_FlameTip"), "SOFC_HotGlow", "SOFC")
    # transformer skid
    box(cx + 50, cz, 0.3, 12, 7, 10, M("M_Transformer"), "SOFC_Transformer", "SOFC")
    for b in range(3):
        cyl(cx + 46 + b * 4, cz, 7.3, 0.4, 5, M("M_White"), "SOFC_Bushing{}".format(b), "SOFC")

def build_steam_turbine():  # (50,-70) back-pressure config
    cx, cz = 50, -70
    box(cx, cz, 0, 52, 1, 40, M("M_Pad"), "ST_Pad", "SteamTurbine")
    box(cx - 6, cz, 1, 32, 14, 20, M("M_Steel"), "ST_Hall", "SteamTurbine")
    box(cx - 6, cz, 15, 33, 2.5, 10, M("M_White"), "ST_Roof", "SteamTurbine")
    # turbine casing + generator (horizontal cylinders)
    _place(MESH_CYL, M("M_SteelDark"),
           ((cx - 8) * 100, (cz + 4) * 100, 600), (0, 90, 0), (7, 7, 16),
           "ST_Casing", "SteamTurbine")
    _place(MESH_CYL, M("M_SteelDark"),
           ((cx + 5.5) * 100, (cz + 4) * 100, 600), (0, 90, 0), (5.6, 5.6, 8),
           "ST_Generator", "SteamTurbine")
    # cooling tower (tiered)
    cyl(cx + 16, cz + 14, 1, 6, 4, M("M_Concrete"), "ST_CT1", "SteamTurbine")
    cyl(cx + 16, cz + 14, 5, 5, 10, M("M_Concrete"), "ST_CT2", "SteamTurbine")
    cyl(cx + 16, cz + 14, 15, 5.5, 6, M("M_Concrete"), "ST_CT3", "SteamTurbine")
    cyl(cx - 22, cz - 14, 1, 2.2, 26, M("M_Steel"), "ST_Stack", "SteamTurbine")

def build_orc():  # (110,-40)
    cx, cz = 110, -40
    box(cx, cz, 0, 26, 0.8, 22, M("M_Pad"), "ORC_Pad", "ORC")
    cyl(cx - 6, cz - 2, 0.8, 2.3, 14, M("M_Copper"), "ORC_Column", "ORC")
    sphere(cx - 6, cz - 2, 15.2, 2.3, M("M_Copper"), "ORC_Dome", "ORC", 0.6)
    box(cx + 4, cz, 0.8, 10, 4, 10, M("M_Copper"), "ORC_HX", "ORC")
    cyl(cx + 8, cz + 5, 0.8, 1.2, 3, M("M_SteelDark"), "ORC_Pump", "ORC")

def build_substation():  # (70,15)
    cx, cz = 70, 15
    box(cx, cz, 0, 36, 0.6, 30, M("M_Pad"), "Sub_Pad", "Substation")
    for i in range(3):
        tx = cx - 10 + i * 10
        box(tx, cz - 5, 0.6, 7, 6, 8, M("M_Transformer"),
            "Sub_XFMR{}".format(i), "Substation")
        for b in range(3):
            cyl(tx - 2 + b * 2, cz - 5, 6.6, 0.35, 4.5, M("M_White"),
                "Sub_Bushing{}_{}".format(i, b), "Substation")
    for k in range(4):  # simplified lattice tower legs
        lx = cx + 14 + (1.2 if k % 2 else -1.2)
        lz = cz + 8 + (1.2 if k > 1 else -1.2)
        cyl(lx, lz, 0.6, 0.15, 24, M("M_Steel"),
            "Sub_TowerLeg{}".format(k), "Substation")
    box(cx + 14, cz + 8, 22, 9, 0.3, 0.3, M("M_Steel"), "Sub_Crossarm1", "Substation")
    box(cx + 14, cz + 8, 19, 9, 0.3, 0.3, M("M_Steel"), "Sub_Crossarm2", "Substation")

def build_ccs():  # (170,-115) v9 carbon capture
    cx, cz = 170, -115
    box(cx, cz, 0, 64, 1, 52, M("M_Pad"), "CCS_Pad", "CarbonCapture")
    # absorber + stripper columns with platform rings
    cyl(cx - 18, cz - 8, 1, 4.5, 34, M("M_Steel"), "CCS_Absorber", "CarbonCapture")
    sphere(cx - 18, cz - 8, 35.6, 4.5, M("M_Steel"), "CCS_AbsorberCap", "CarbonCapture", 0.55)
    cyl(cx - 4, cz - 10, 1, 3.2, 24, M("M_Steel"), "CCS_Stripper", "CarbonCapture")
    sphere(cx - 4, cz - 10, 25.6, 3.2, M("M_Steel"), "CCS_StripperCap", "CarbonCapture", 0.55)
    for p in range(1, 4):
        cyl(cx - 18, cz - 8, (34.0 / 4.0) * p + 0.8, 5.4, 0.25,
            M("M_SteelDark"), "CCS_Platform{}".format(p), "CarbonCapture")
    # crossover piping
    pipe(cx - 18, cz - 8.5, cx - 4, cz - 9.5, 15, 0.5, M("M_PipeSteam"),
         "CCS_Crossover1", "CarbonCapture")
    pipe(cx - 18, cz - 7.5, cx - 4, cz - 10.5, 21, 0.5, M("M_PipeSteam"),
         "CCS_Crossover2", "CarbonCapture")
    # reboiler kettle (horizontal, amber) - fed by BP-ST exhaust
    _place(MESH_CYL, M("M_Copper"),
           ((cx - 4) * 100, (cz + 2) * 100, 320), (0, 90, 0), (4.4, 4.4, 9),
           "CCS_Reboiler", "CarbonCapture")
    # compression hall + 4-stage train
    box(cx + 14, cz + 8, 1, 22, 7, 12, M("M_SteelDark"), "CCS_CompHall", "CarbonCapture")
    for c in range(4):
        _place(MESH_CYL, M("M_Transformer"),
               ((cx - 8 + c * 4.6 + 15) * 100, (cz + 16) * 100, 220),
               (0, 90, 0), (2.2, 2.2, 3.4),
               "CCS_Compressor{}".format(c), "CarbonCapture")
    cyl(cx - 22, cz + 14, 1, 3.6, 7, M("M_Steel"), "CCS_AmineTank", "CarbonCapture")
    # CO2 export pipeline heading east
    pipe(cx + 14, cz + 18, cx + 250, cz + 17, 1.6, 0.7, M("M_PipeWhite"),
         "CCS_CO2Pipeline", "CarbonCapture")

def build_bess():  # (120,52)
    cx, cz = 120, 52
    box(cx, cz, 0, 34, 0.6, 16, M("M_Pad"), "BESS_Pad", "BESS")
    for i in range(4):
        mx = cx - 12 + i * 8
        box(mx, cz - 2, 0.6, 6.8, 2.6, 1.7, M("M_White"),
            "BESS_Megapack{}".format(i), "BESS")
        box(mx, cz + 2.5, 0.6, 1.6, 1.8, 1.2, M("M_SteelDark"),
            "BESS_Inverter{}".format(i), "BESS")
        sphere(mx + 3.1, cz - 1.2, 2.9, 0.14, M("M_StatusGreen"),
               "BESS_LED{}".format(i), "BESS")

def build_greenhouses():  # (215,150)
    cx, cz = 215, 150
    box(cx, cz, 0, 48, 0.5, 34, M("M_Soil"), "GH_Soil", "Greenhouses")
    for h in range(3):
        hz = cz - 10 + h * 11
        box(cx, hz, 0.5, 40, 3.2, 8, M("M_Glass"), "GH_House{}".format(h), "Greenhouses")
        box(cx, hz, 3.7, 40, 2.2, 5.6, M("M_Glass"), "GH_Roof{}".format(h), "Greenhouses")
        box(cx, hz, 5.9, 40, 0.18, 0.18, M("M_White"), "GH_Ridge{}".format(h), "Greenhouses")
        gl = spawn(unreal.PointLight,
                   (cx * 100, hz * 100, 260), (0, 0, 0))
        try:
            gl.set_actor_label("GH_GrowLight{}".format(h))
            gl.set_folder_path(unreal.Name("Meridian/Greenhouses"))
            lc = gl.light_component
            lc.set_editor_property("intensity", 3000.0)
            lc.set_light_color(unreal.LinearColor(1.0, 0.82, 0.55, 1.0))
            lc.set_editor_property("attenuation_radius", 3200.0)
        except Exception:
            pass

def build_dc():  # (-50,110)
    cx, cz = -50, 110
    box(cx, cz, 0, 108, 1, 68, M("M_Pad"), "DC_Pad", "DataCenter")
    box(cx, cz, 1, 100, 20, 60, M("M_DCBlue"), "DC_Building", "DataCenter")
    box(cx, cz, 21, 101, 1.5, 61, M("M_SteelDark"), "DC_Parapet", "DataCenter")
    for r in range(3):
        for c in range(6):
            hx = cx - 40 + c * 16
            hz = cz - 20 + r * 20
            box(hx, hz, 22.5, 8, 2, 6, M("M_Steel"),
                "DC_HVAC_{}_{}".format(r, c), "DataCenter")
    # glowing server-window band (south face) + logo strip
    box(cx, cz - 30.2, 5, 96, 10, 0.3, M("M_WindowGlow"), "DC_WindowBand", "DataCenter")
    box(cx, cz - 30.3, 18.2, 82, 0.8, 0.25, M("M_PipeCyan"), "DC_LogoStrip", "DataCenter")

def build_water():  # MD (20,180) + tanks (-42,185)
    box(20, 180, 0, 38, 1, 30, M("M_Pad"), "MD_Pad", "Water")
    box(10, 180, 1, 14, 3, 18, M("M_TankCyan"), "MD_Rack", "Water")
    cyl(28, 176, 1, 4.5, 10, M("M_TankCyan"), "MD_Condenser", "Water")
    sphere(28, 176, 11.6, 4.5, M("M_TankCyan"), "MD_CondDome", "Water", 0.55)
    box(-42, 185, 0, 52, 0.5, 22, M("M_Pad"), "Tank_Pad", "Water")
    for i in range(3):
        tx = -60 + i * 18
        cyl(tx, 185, 0.5, 7.5, 16, M("M_TankCyan"), "Tank{}".format(i), "Water")
        sphere(tx, 185, 17.0, 7.5, M("M_TankCyan"), "Tank{}_Dome".format(i), "Water", 0.5)

def build_wetland():  # (-170,160)
    box(-170, 160, 0.2, 100, 1, 60, M("M_Water"), "Wetland_Pool", "Wetland")
    box(-170, 129, 0, 102, 1.5, 2, M("M_Concrete"), "Wetland_EdgeN", "Wetland")
    box(-170, 191, 0, 102, 1.5, 2, M("M_Concrete"), "Wetland_EdgeS", "Wetland")
    box(-221, 160, 0, 2, 1.5, 60, M("M_Concrete"), "Wetland_EdgeW", "Wetland")
    box(-119, 160, 0, 2, 1.5, 60, M("M_Concrete"), "Wetland_EdgeE", "Wetland")
    for b in range(3):  # weir baffles
        box(-200 + b * 30, 160 + (6 if b % 2 == 0 else -6), 0.5, 8, 2.5, 2,
            M("M_Concrete"), "Wetland_Baffle{}".format(b), "Wetland")

def build_lfg():  # (-280,-40) flare + wellheads; landfill hill beyond
    cx, cz = -280, -40
    box(cx, cz - 30, 0, 14, 0.8, 14, M("M_Pad"), "Flare_Pad", "LFG")
    cyl(cx, cz - 30, 0.8, 2.2, 32, M("M_SteelDark"), "Flare_Stack", "LFG")
    cyl(cx, cz - 30, 32.8, 2.8, 3, M("M_Steel"), "Flare_Tip", "LFG")
    sphere(cx, cz - 30, 38.5, 2.6, M("M_FlameCore"), "Flare_Flame1", "LFG", 1.8)
    sphere(cx, cz - 30, 42.5, 1.6, M("M_FlameTip"), "Flare_Flame2", "LFG", 1.6)
    fl = spawn(unreal.PointLight, (cx * 100, (cz - 30) * 100, 4000), (0, 0, 0))
    try:
        fl.set_actor_label("Flare_Light")
        fl.set_folder_path(unreal.Name("Meridian/LFG"))
        lc = fl.light_component
        lc.set_editor_property("intensity", 60000.0)
        lc.set_light_color(unreal.LinearColor(1.0, 0.45, 0.1, 1.0))
        lc.set_editor_property("attenuation_radius", 18000.0)
    except Exception:
        pass
    box(cx, cz + 5, 0, 32, 1, 32, M("M_Pad"), "Wellhead_Pad", "LFG")
    for i, (dx, dz) in enumerate([(-10, -10), (10, -10), (-10, 10), (10, 10)]):
        cyl(cx + dx, cz + 5 + dz, 1, 1.8, 5, M("M_GoldSOFC"),
            "Wellhead{}".format(i), "LFG")
        cyl(cx + dx, cz + 5 + dz, 6, 0.6, 7, M("M_SteelDark"),
            "WellheadTree{}".format(i), "LFG")
    # terraced landfill hill (northwest context)
    for l in range(5):
        r = 130 - l * 18
        cyl(-560, -420, l * 8, r, 8, M("M_LandfillGrass"),
            "Landfill_Tier{}".format(l), "LFG")

def build_cleanup():  # (-190,-40)
    cx, cz = -190, -40
    box(cx, cz, 0, 36, 1, 32, M("M_Pad"), "GC_Pad", "GasCleanup")
    cyl(cx - 10, cz - 6, 1, 4.5, 16, M("M_Copper"), "GC_IronSponge", "GasCleanup")
    sphere(cx - 10, cz - 6, 17.5, 4.5, M("M_Copper"), "GC_Cap1", "GasCleanup", 0.55)
    cyl(cx + 5, cz - 3, 1, 3.5, 12, M("M_Copper"), "GC_Carbon", "GasCleanup")
    sphere(cx + 5, cz - 3, 13.4, 3.5, M("M_Copper"), "GC_Cap2", "GasCleanup", 0.55)
    box(cx + 12, cz + 10, 1, 10, 5, 8, M("M_SteelDark"), "GC_Control", "GasCleanup")

def build_export():  # (250,15)
    cx, cz = 250, 15
    box(cx, cz, 0, 28, 0.5, 28, M("M_Pad"), "Export_Pad", "ExportTie")
    for i in range(3):
        box(cx - 6 + i * 6, cz - 5, 0.5, 4, 5, 5, M("M_Transformer"),
            "Export_XFMR{}".format(i), "ExportTie")
    for k in range(4):
        lx = cx + 8 + (1.2 if k % 2 else -1.2)
        lz = cz + 6 + (1.2 if k > 1 else -1.2)
        cyl(lx, lz, 0.5, 0.15, 28, M("M_Steel"), "Export_TowerLeg{}".format(k), "ExportTie")

def build_pipes():
    P = [
        (-270, -25, -195, -40, 6, 0.9, "M_PipeAmber", "LFG_to_Cleanup"),
        (-170, -40, -110, -50, 6, 1.1, "M_PipeAmber", "Cleanup_to_SOFC"),
        (-20, -50, 30, -60, 14, 1.2, "M_PipeSteam", "SOFC_to_ST"),
        (-60, -80, 152, -123, 18, 1.3, "M_PipeSteam", "SOFC_Flue_to_CCS"),
        (60, -75, 166, -113, 5, 1.0, "M_PipeSteam", "BPST_to_Reboiler"),
        (112, -32, 185, 140, 2, 0.9, "M_PipeAmber", "HeatMain_to_Greenhouse"),
        (82, 22, 118, 48, 3, 0.8, "M_PipeGreen", "Substation_to_BESS"),
        (65, 25, -10, 100, 8, 1.3, "M_PipeGreen", "Substation_to_DC"),
        (-30, -50, 15, 170, 6, 1.0, "M_PipeCyan", "SOFC_Water_to_MD"),
        (-95, 110, -130, 150, 4, 1.0, "M_PipePurple", "DC_to_Wetland"),
        (0, 180, -30, 185, 8, 0.8, "M_PipeCyan", "MD_to_Tanks"),
    ]
    for (x1, z1, x2, z2, y, r, mname, label) in P:
        pipe(x1, z1, x2, z2, y, r, M(mname), label, "Piping")

def build_lighting():
    sun = spawn(unreal.DirectionalLight, (0, 0, 20000), (0, -38, 40))
    try:
        sun.set_actor_label("Sun")
        sun.set_folder_path(unreal.Name("Meridian/Lighting"))
        lc = sun.light_component
        lc.set_editor_property("intensity", 8.0)
        lc.set_light_color(unreal.LinearColor(1.0, 0.93, 0.82, 1.0))
        lc.set_editor_property("atmosphere_sun_light", True)
    except Exception:
        pass
    for cls, name in [(unreal.SkyAtmosphere, "SkyAtmosphere"),
                      (unreal.ExponentialHeightFog, "HeightFog"),
                      (unreal.SkyLight, "SkyLight")]:
        try:
            a = spawn(cls, (0, 0, 100), (0, 0, 0))
            a.set_actor_label(name)
            a.set_folder_path(unreal.Name("Meridian/Lighting"))
            if cls is unreal.SkyLight:
                slc = a.light_component
                slc.set_editor_property("real_time_capture", True)
            if cls is unreal.ExponentialHeightFog:
                fc = a.component
                fc.set_editor_property("fog_density", 0.006)
        except Exception as ex:
            unreal.log_warning("light rig piece {} failed: {}".format(name, ex))
    try:
        ppv = spawn(unreal.PostProcessVolume, (0, 0, 100), (0, 0, 0))
        ppv.set_actor_label("PostProcess_Global")
        ppv.set_folder_path(unreal.Name("Meridian/Lighting"))
        ppv.set_editor_property("unbound", True)
        s = ppv.settings
        s.set_editor_property("override_bloom_intensity", True)
        s.set_editor_property("bloom_intensity", 0.55)
        s.set_editor_property("override_auto_exposure_min_brightness", True)
        s.set_editor_property("auto_exposure_min_brightness", 0.3)
        s.set_editor_property("override_auto_exposure_max_brightness", True)
        s.set_editor_property("auto_exposure_max_brightness", 2.0)
    except Exception as ex:
        unreal.log_warning("post-process setup failed: {}".format(ex))
    # SOFC hot glow + DC interior blue
    for (x, z, y, col, inten, lbl) in [
            (-60, -80, 28, (1.0, 0.5, 0.15), 30000.0, "SOFC_Glow"),
            (-50, 80, 12, (0.3, 0.6, 1.0), 20000.0, "DC_Glow")]:
        try:
            pl = spawn(unreal.PointLight, (x * 100, z * 100, y * 100), (0, 0, 0))
            pl.set_actor_label(lbl)
            pl.set_folder_path(unreal.Name("Meridian/Lighting"))
            lc = pl.light_component
            lc.set_editor_property("intensity", inten)
            lc.set_light_color(unreal.LinearColor(col[0], col[1], col[2], 1.0))
            lc.set_editor_property("attenuation_radius", 12000.0)
        except Exception:
            pass

def build_camera():
    # overview vantage matching the web model's opening shot
    px, py, pz = 340 * 100, 340 * 100, 240 * 100   # UE X, Y, Z
    tx, ty, tz = 0, 3000, 1500
    dx, dy, dz = tx - px, ty - py, tz - pz
    yaw = math.degrees(math.atan2(dy, dx))
    pitch = math.degrees(math.atan2(dz, math.sqrt(dx * dx + dy * dy)))
    try:
        cam = spawn(unreal.CameraActor, (px, py, pz), (0, pitch, yaw))
        cam.set_actor_label("Camera_Overview")
        cam.set_folder_path(unreal.Name("Meridian/Cameras"))
    except Exception as ex:
        unreal.log_warning("camera spawn failed: {}".format(ex))

# ---------- top-level ----------

def build_all():
    unreal.log("=== MERIDIAN v9 UNREAL BUILD - concept by Brandon (Vaddix123) ===")
    if not unreal.EditorAssetLibrary.does_directory_exist(CONTENT_DIR):
        unreal.EditorAssetLibrary.make_directory(CONTENT_DIR)
    if not unreal.EditorAssetLibrary.does_directory_exist(MAT_DIR):
        unreal.EditorAssetLibrary.make_directory(MAT_DIR)
    new_level(LEVEL_ASSET)
    build_materials()
    steps = [build_ground, build_lfg, build_cleanup, build_sofc,
             build_steam_turbine, build_orc, build_ccs, build_bess,
             build_substation, build_export, build_dc, build_water,
             build_wetland, build_greenhouses, build_pipes,
             build_lighting, build_camera]
    for step in steps:
        try:
            step()
            unreal.log("Meridian: {} OK".format(step.__name__))
        except Exception as ex:
            unreal.log_error("Meridian: {} FAILED: {}".format(step.__name__, ex))
    save_level()
    try:
        unreal.EditorAssetLibrary.save_directory(CONTENT_DIR, recursive=True)
    except Exception:
        pass
    unreal.log("=== MERIDIAN BUILD COMPLETE: {} actors placed ===".format(_actor_count))

if __name__ == "__main__":
    build_all()
