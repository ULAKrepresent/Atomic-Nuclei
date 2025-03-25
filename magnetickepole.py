import bpy
import math
import mathutils
# Vymažeme všetky existujúce objekty v scéne


# Pridanie kamery do scény
bpy.ops.object.camera_add(location=(16, -12, 6), rotation=(math.radians(72), 0, 7.2))
kamera = bpy.context.active_object

bpy.context.scene.frame_end = 1020
def create_material_from_rgb(name, r, g, b, a=255):
    """
    Vytvorí materiál s danou farbou.
    :param name: názov materiálu
    :param r: červená zložka (0-255)
    :param g: zelená zložka (0-255)
    :param b: modrá zložka (0-255)
    :param a: alfa zložka (0-255), predvolene 255 (nepriehľadné)
    :return: vytvorený materiál
    """
    mat = bpy.data.materials.new(name)
    # Normalizácia farieb na rozsah 0-1
    mat.diffuse_color = (r/255, g/255, b/255, a/255)
    return mat

# =============================================================================
# Vaše existujúce objekty a animácie (prvá, druhá aj tretia rada)
# =============================================================================

# ------------------------------
# 1. Prvá rotujúca guľa (červená)
# ------------------------------
# Vytvorenie červenej planéty
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(0, 0, 0))
planet1 = bpy.context.active_object
planet1.name = "Planet1"

# Vytvorenie materiálu s RGB hodnotami (225, 2, 0)
mat_red = create_material_from_rgb("RedMaterial", 225, 2, 0)
planet1.data.materials.append(mat_red)

# Zvislá os (čierna šípka)
bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=3.0, location=(0, 0, 0))
black_axis1 = bpy.context.active_object
black_axis1.name = "BlackAxis1"

bpy.ops.mesh.primitive_cone_add(radius1=0.1, depth=0.2, location=(0, 0, 1.5))
black_tip1 = bpy.context.active_object
black_tip1.name = "BlackArrowTip1"
black_tip1.parent = black_axis1

mat_black = create_material_from_rgb("BlackMaterial", 0, 0, 0)
black_axis1.data.materials.append(mat_black)
black_tip1.data.materials.append(mat_black)

# Na začiatku (frame 1) nech je čierna šípka skrytá:
black_axis1.hide_viewport = True
black_axis1.hide_render = True
black_axis1.keyframe_insert(data_path="hide_viewport", frame=1)
black_axis1.keyframe_insert(data_path="hide_render", frame=1)

black_tip1.hide_viewport = True
black_tip1.hide_render = True
black_tip1.keyframe_insert(data_path="hide_viewport", frame=1)
black_tip1.keyframe_insert(data_path="hide_render", frame=1)

# Od frame 480 sa má zobraziť:
black_axis1.hide_viewport = False
black_axis1.hide_render = False
black_axis1.keyframe_insert(data_path="hide_viewport", frame=1120)
black_axis1.keyframe_insert(data_path="hide_render", frame=1120)

black_tip1.hide_viewport = False
black_tip1.hide_render = False
black_tip1.keyframe_insert(data_path="hide_viewport", frame=1120)
black_tip1.keyframe_insert(data_path="hide_render", frame=1120)

# Naklonená os (zelená šípka)
bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=3.0, location=(0, 0, 0))
green_axis1 = bpy.context.active_object
green_axis1.name = "GreenAxis1"
green_axis1.rotation_euler = (0.4, 0.0, 0.0)  # naklonenie približne 23°

bpy.ops.mesh.primitive_cone_add(radius1=0.16, depth=0.4, location=(0, 0, 1.6))
green_tip1 = bpy.context.active_object
green_tip1.name = "GreenArrowTip1"
green_tip1.parent = green_axis1

mat_green = create_material_from_rgb("GreenMaterial", 10, 12, 65)  # zjednodušené farebné hodnoty
green_axis1.data.materials.append(mat_green)
green_tip1.data.materials.append(mat_green)

# Nastavenie rodičovstva - planéta sa otáča spolu s naklonenou osou
planet1.parent = green_axis1

# Animácia pre prvú skupinu od frame 1 do 480
start_rot = 6 * 2 * math.pi  # 10 otočiek

# Animácia pre naklonenú os (green_axis1)
green_axis1.rotation_euler = (2.8, 2.0, 0.0)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=1)
green_axis1.rotation_euler = (2.8, 2.0, start_rot)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=480)
green_axis1.rotation_euler = (0.4, 0.0, start_rot)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=495)

green_axis1.rotation_euler = (0.4, 0.0, start_rot + 6*2 * math.pi)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=700)

# Animácia pre planétu (planet1)
planet1.rotation_euler = (0.0, 0.0, 0.0)
planet1.keyframe_insert(data_path="rotation_euler", frame=1)
planet1.rotation_euler = (0.0, 0.0, start_rot)
planet1.keyframe_insert(data_path="rotation_euler", frame=480)

# Zmena interpolácie na LINEAR pre prvú skupinu
for fcurve in green_axis1.animation_data.action.fcurves:
    for key in fcurve.keyframe_points:
        if key.co[0] <= 690:
            key.interpolation = 'LINEAR'
for fcurve in planet1.animation_data.action.fcurves:
    for key in fcurve.keyframe_points:
        if key.co[0] <= 690:
            key.interpolation = 'LINEAR'
# Frame 480: východiskový stav
start_rot2  = start_rot + 6*2 * math.pi
green_axis1.rotation_euler = (0.4, 0.0, start_rot2)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=700)

# Frame 490: rýchly prechod – dosiahnutie 90° tilt, rotácia ostáva rovnaká
green_axis1.rotation_euler = (1.57, 0.0, start_rot2)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=710)

# Pridanie medzikľúčového snímku, kde rotácia dosiahne vyššiu hodnotu – simulujeme rýchly úsek
# Tu nastavte hodnotu tak, aby medzi frame 490 a 600 bola vyššia rýchlosť (väčší nárast rotácie)
green_axis1.rotation_euler = (1.57, 0.0, start_rot2 + 2 * math.pi)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=720)

# Frame 720: finálna hodnota – tilt sa vráti na pôvod (0.4) a rotácia dosiahne cieľovú hodnotu
green_axis1.rotation_euler = (0.4, 0.0, start_rot2 + 36 * math.pi)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=840)

new_start_rot = start_rot2 + 36 * math.pi  # začneme od poslednej hodnoty
green_axis1.rotation_euler = (0.4, 0.0, new_start_rot + 10 * 2 * math.pi)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=1120)

# -----------------------------------------
# 2. Druhá rotujúca guľa (modrá) - posunutá na X osi
# -----------------------------------------
offset = 3.0  # Posun medzi guľami

# Vytvorenie modrej planéty
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(0, 0, 0))
planet2 = bpy.context.active_object
planet2.name = "Planet2"

mat_blue = create_material_from_rgb("BlueMaterial", 225, 2, 0)
planet2.data.materials.append(mat_blue)

# Zvislá os pre druhú guľu (čierna šípka)
bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=3.0, location=(3, 0, 0))
black_axis2 = bpy.context.active_object
black_axis2.name = "BlackAxis2"

bpy.ops.mesh.primitive_cone_add(radius1=0.1, depth=0.2, location=(0, 0, 1.5))
black_tip2 = bpy.context.active_object
black_tip2.name = "BlackArrowTip2"
black_tip2.parent = black_axis2

black_axis2.data.materials.append(mat_black)
black_tip2.data.materials.append(mat_black)

# Na začiatku (frame 1) nech je čierna šípka skrytá:
black_axis2.hide_viewport = True
black_axis2.hide_render = True
black_axis2.keyframe_insert(data_path="hide_viewport", frame=1)
black_axis2.keyframe_insert(data_path="hide_render", frame=1)

black_tip2.hide_viewport = True
black_tip2.hide_render = True
black_tip2.keyframe_insert(data_path="hide_viewport", frame=1)
black_tip2.keyframe_insert(data_path="hide_render", frame=1)

# Od frame 480 sa má zobraziť:
black_axis2.hide_viewport = False
black_axis2.hide_render = False
black_axis2.keyframe_insert(data_path="hide_viewport", frame=1020)
black_axis2.keyframe_insert(data_path="hide_render", frame=1020)

black_tip2.hide_viewport = False
black_tip2.hide_render = False
black_tip2.keyframe_insert(data_path="hide_viewport", frame=1020)
black_tip2.keyframe_insert(data_path="hide_render", frame=1020)

# Naklonená os pre druhú guľu (oranžová šípka)
bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=3.0, location=(3, 0, 0))
green_axis2 = bpy.context.active_object
green_axis2.name = "GreenAxis2"
green_axis2.rotation_euler = (0.4, 0.0, 0.0)

bpy.ops.mesh.primitive_cone_add(radius1=0.16, depth=0.4, location=(0, 0, 1.6))
green_tip2 = bpy.context.active_object
green_tip2.name = "GreenArrowTip2"
green_tip2.parent = green_axis2

mat_orange = create_material_from_rgb("OrangeMaterial", 10, 12, 65)
green_axis2.data.materials.append(mat_orange)
green_tip2.data.materials.append(mat_orange)

planet2.parent = green_axis2

start_rot = 10 * 2 * math.pi

# Animácia pre naklonenú os (green_axis1)
green_axis2.rotation_euler = (-2.5, 3.0, 0.0)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=1)
green_axis2.rotation_euler = (-2.5, 3.0, start_rot)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=480)
green_axis2.rotation_euler = (0.4, 3.0, start_rot)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=495)

green_axis2.rotation_euler = (0.4, 3.0, start_rot + 6*2 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=700)

# Animácia pre planétu (planet1)
planet2.rotation_euler = (0.0, 0.0, 0.0)
planet2.keyframe_insert(data_path="rotation_euler", frame=1)
planet2.rotation_euler = (0.0, 0.0, start_rot)
planet2.keyframe_insert(data_path="rotation_euler", frame=480)

# Zmena interpolácie na LINEAR pre prvú skupinu
for fcurve in green_axis2.animation_data.action.fcurves:
    for key in fcurve.keyframe_points:
        if key.co[0] <= 690:
            key.interpolation = 'LINEAR'
for fcurve in planet2.animation_data.action.fcurves:
    for key in fcurve.keyframe_points:
        if key.co[0] <= 690:
            key.interpolation = 'LINEAR'
# Frame 480: východiskový stav
start_rot2  = start_rot + 6*2 * math.pi
green_axis2.rotation_euler = (0.4, 3.0, start_rot2)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=700)

# Frame 490: rýchly prechod – dosiahnutie 90° tilt, rotácia ostáva rovnaká
green_axis2.rotation_euler = (1.57, 3.0, start_rot2)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=710)

# Pridanie medzikľúčového snímku, kde rotácia dosiahne vyššiu hodnotu – simulujeme rýchly úsek
# Tu nastavte hodnotu tak, aby medzi frame 490 a 600 bola vyššia rýchlosť (väčší nárast rotácie)
green_axis2.rotation_euler = (1.57, 3.0, start_rot2 + 2 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=720)

# Frame 720: finálna hodnota – tilt sa vráti na pôvod (0.4) a rotácia dosiahne cieľovú hodnotu
green_axis2.rotation_euler = (0.4, 3.0, start_rot2 + 36 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=840)

new_start_rot = start_rot2 + 36 * math.pi  # začneme od poslednej hodnoty
green_axis2.rotation_euler = (0.4, 3.0, new_start_rot + 10 * 2 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=1120)

# -----------------------------------------
# 3. Tretia varianta - modrá guľa na opačnej strane (X osi)
# -----------------------------------------
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(0, 0, 0))
planet2 = bpy.context.active_object
planet2.name = "Planet2"

mat_blue = create_material_from_rgb("BlueMaterial", 225, 2, 0)
planet2.data.materials.append(mat_blue)

bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=3.0, location=(-3, 0, 0))
black_axis2 = bpy.context.active_object
black_axis2.name = "BlackAxis2"

bpy.ops.mesh.primitive_cone_add(radius1=0.1, depth=0.2, location=(0, 0, 1.5))
black_tip2 = bpy.context.active_object
black_tip2.name = "BlackArrowTip2"
black_tip2.parent = black_axis2

black_axis2.data.materials.append(mat_black)
black_tip2.data.materials.append(mat_black)

# Na začiatku (frame 1) nech je čierna šípka skrytá:
black_axis2.hide_viewport = True
black_axis2.hide_render = True
black_axis2.keyframe_insert(data_path="hide_viewport", frame=1)
black_axis2.keyframe_insert(data_path="hide_render", frame=1)

black_tip2.hide_viewport = True
black_tip2.hide_render = True
black_tip2.keyframe_insert(data_path="hide_viewport", frame=1)
black_tip2.keyframe_insert(data_path="hide_render", frame=1)

# Od frame 480 sa má zobraziť:
black_axis2.hide_viewport = False
black_axis2.hide_render = False
black_axis2.keyframe_insert(data_path="hide_viewport", frame=1020)
black_axis2.keyframe_insert(data_path="hide_render", frame=1020)

black_tip2.hide_viewport = False
black_tip2.hide_render = False
black_tip2.keyframe_insert(data_path="hide_viewport", frame=1020)
black_tip2.keyframe_insert(data_path="hide_render", frame=1020)

bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=3.0, location=(-3, 0, 0))
green_axis2 = bpy.context.active_object
green_axis2.name = "GreenAxis2"
green_axis2.rotation_euler = (0.4, 0.0, 0.0)

bpy.ops.mesh.primitive_cone_add(radius1=0.16, depth=0.4, location=(0, 0, 1.6))
green_tip2 = bpy.context.active_object
green_tip2.name = "GreenArrowTip2"
green_tip2.parent = green_axis2

mat_orange = create_material_from_rgb("OrangeMaterial", 10, 12, 65)
green_axis2.data.materials.append(mat_orange)
green_tip2.data.materials.append(mat_orange)

planet2.parent = green_axis2

start_rot = 10 * 2 * math.pi

# Animácia pre naklonenú os (green_axis1)
green_axis2.rotation_euler = (1.1, 0.0, 0.0)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=1)
green_axis2.rotation_euler = (1.1, 0.0, start_rot)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=480)
green_axis2.rotation_euler = (0.4, 0.0, start_rot)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=495)

green_axis2.rotation_euler = (0.4, 0.0, start_rot + 6*2 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=700)

# Animácia pre planétu (planet1)
planet2.rotation_euler = (0.0, 0.0, 0.0)
planet2.keyframe_insert(data_path="rotation_euler", frame=1)
planet2.rotation_euler = (0.0, 0.0, start_rot)
planet2.keyframe_insert(data_path="rotation_euler", frame=480)

# Zmena interpolácie na LINEAR pre prvú skupinu
for fcurve in green_axis2.animation_data.action.fcurves:
    for key in fcurve.keyframe_points:
        if key.co[0] <= 690:
            key.interpolation = 'LINEAR'
for fcurve in planet2.animation_data.action.fcurves:
    for key in fcurve.keyframe_points:
        if key.co[0] <= 690:
            key.interpolation = 'LINEAR'
# Frame 480: východiskový stav
start_rot2  = start_rot + 6*2 * math.pi
green_axis2.rotation_euler = (0.4, 0.0, start_rot2)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=700)

# Frame 490: rýchly prechod – dosiahnutie 90° tilt, rotácia ostáva rovnaká
green_axis2.rotation_euler = (1.57, 0.0, start_rot2)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=710)

# Pridanie medzikľúčového snímku, kde rotácia dosiahne vyššiu hodnotu – simulujeme rýchly úsek
# Tu nastavte hodnotu tak, aby medzi frame 490 a 600 bola vyššia rýchlosť (väčší nárast rotácie)
green_axis2.rotation_euler = (1.57, 0.0, start_rot2 + 2 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=720)

# Frame 720: finálna hodnota – tilt sa vráti na pôvod (0.4) a rotácia dosiahne cieľovú hodnotu
green_axis2.rotation_euler = (0.4, 0.0, start_rot2 + 36 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=840)

new_start_rot = start_rot2 + 36 * math.pi  # začneme od poslednej hodnoty
green_axis2.rotation_euler = (0.4, 0.0, new_start_rot + 10 * 2 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=1120)

################################################################################
# 2. rad
################################################################################
# ------------------------------
# 1. Prvá rotujúca guľa (červená)
# ------------------------------
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(0, 0, 0))
planet1 = bpy.context.active_object
planet1.name = "Planet1"

mat_red = create_material_from_rgb("RedMaterial", 225, 2, 0)
planet1.data.materials.append(mat_red)

bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=3.0, location=(0, 3, 0))
black_axis1 = bpy.context.active_object
black_axis1.name = "BlackAxis1"

bpy.ops.mesh.primitive_cone_add(radius1=0.1, depth=0.2, location=(0, 0, 1.5))
black_tip1 = bpy.context.active_object
black_tip1.name = "BlackArrowTip1"
black_tip1.parent = black_axis1

black_axis1.data.materials.append(mat_black)
black_tip1.data.materials.append(mat_black)

# Na začiatku (frame 1) nech je čierna šípka skrytá:
black_axis1.hide_viewport = True
black_axis1.hide_render = True
black_axis1.keyframe_insert(data_path="hide_viewport", frame=1)
black_axis1.keyframe_insert(data_path="hide_render", frame=1)

black_tip1.hide_viewport = True
black_tip1.hide_render = True
black_tip1.keyframe_insert(data_path="hide_viewport", frame=1)
black_tip1.keyframe_insert(data_path="hide_render", frame=1)

# Od frame 480 sa má zobraziť:
black_axis1.hide_viewport = False
black_axis1.hide_render = False
black_axis1.keyframe_insert(data_path="hide_viewport", frame=1020)
black_axis1.keyframe_insert(data_path="hide_render", frame=1020)

black_tip1.hide_viewport = False
black_tip1.hide_render = False
black_tip1.keyframe_insert(data_path="hide_viewport", frame=1020)
black_tip1.keyframe_insert(data_path="hide_render", frame=1020)


bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=3.0, location=(0, 3, 0))
green_axis1 = bpy.context.active_object
green_axis1.name = "GreenAxis1"
green_axis1.rotation_euler = (0.4, 0.0, 0.0)

bpy.ops.mesh.primitive_cone_add(radius1=0.16, depth=0.4, location=(0, 0, 1.6))
green_tip1 = bpy.context.active_object
green_tip1.name = "GreenArrowTip1"
green_tip1.parent = green_axis1

mat_green = create_material_from_rgb("GreenMaterial", 10, 12, 65)
green_axis1.data.materials.append(mat_green)
green_tip1.data.materials.append(mat_green)

planet1.parent = green_axis1

start_rot = 10 * 2 * math.pi

# Animácia pre naklonenú os (green_axis1)
green_axis1.rotation_euler = (2.8, 2.0, 0.0)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=1)
green_axis1.rotation_euler = (2.8, 2.0, start_rot)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=480)
green_axis1.rotation_euler = (0.4, 3.0, start_rot)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=495)

green_axis1.rotation_euler = (0.4, 3.0, start_rot + 6*2 * math.pi)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=700)

# Animácia pre planétu (planet1)
planet1.rotation_euler = (0.0, 0.0, 0.0)
planet1.keyframe_insert(data_path="rotation_euler", frame=1)
planet1.rotation_euler = (0.0, 0.0, start_rot)
planet1.keyframe_insert(data_path="rotation_euler", frame=480)

# Zmena interpolácie na LINEAR pre prvú skupinu
for fcurve in green_axis1.animation_data.action.fcurves:
    for key in fcurve.keyframe_points:
        if key.co[0] <= 690:
            key.interpolation = 'LINEAR'
for fcurve in planet1.animation_data.action.fcurves:
    for key in fcurve.keyframe_points:
        if key.co[0] <= 690:
            key.interpolation = 'LINEAR'
# Frame 480: východiskový stav
start_rot2  = start_rot + 6*2 * math.pi
green_axis1.rotation_euler = (0.4, 3.0, start_rot2)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=700)

# Frame 490: rýchly prechod – dosiahnutie 90° tilt, rotácia ostáva rovnaká
green_axis1.rotation_euler = (1.57, 3.0, start_rot2)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=710)

# Pridanie medzikľúčového snímku, kde rotácia dosiahne vyššiu hodnotu – simulujeme rýchly úsek
# Tu nastavte hodnotu tak, aby medzi frame 490 a 600 bola vyššia rýchlosť (väčší nárast rotácie)
green_axis1.rotation_euler = (1.57, 3.0, start_rot2 + 2 * math.pi)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=720)

# Frame 720: finálna hodnota – tilt sa vráti na pôvod (0.4) a rotácia dosiahne cieľovú hodnotu
green_axis1.rotation_euler = (0.4, 3.0, start_rot2 + 36 * math.pi)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=840)

new_start_rot = start_rot2 + 36 * math.pi  # začneme od poslednej hodnoty
green_axis1.rotation_euler = (0.4, 3.0, new_start_rot + 10 * 2 * math.pi)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=1120)

# -----------------------------------------
# 2. Druhá rotujúca guľa (modrá) - posunutá na X osi
# -----------------------------------------
offset = 3.0

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(0, 0, 0))
planet2 = bpy.context.active_object
planet2.name = "Planet2"

mat_blue = create_material_from_rgb("BlueMaterial", 225, 2, 0)
planet2.data.materials.append(mat_blue)

bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=3.0, location=(3, 3, 0))
black_axis2 = bpy.context.active_object
black_axis2.name = "BlackAxis2"

bpy.ops.mesh.primitive_cone_add(radius1=0.1, depth=0.2, location=(0, 0, 1.5))
black_tip2 = bpy.context.active_object
black_tip2.name = "BlackArrowTip2"
black_tip2.parent = black_axis2

black_axis2.data.materials.append(mat_black)
black_tip2.data.materials.append(mat_black)

# Na začiatku (frame 1) nech je čierna šípka skrytá:
black_axis2.hide_viewport = True
black_axis2.hide_render = True
black_axis2.keyframe_insert(data_path="hide_viewport", frame=1)
black_axis2.keyframe_insert(data_path="hide_render", frame=1)

black_tip2.hide_viewport = True
black_tip2.hide_render = True
black_tip2.keyframe_insert(data_path="hide_viewport", frame=1)
black_tip2.keyframe_insert(data_path="hide_render", frame=1)

# Od frame 480 sa má zobraziť:
black_axis2.hide_viewport = False
black_axis2.hide_render = False
black_axis2.keyframe_insert(data_path="hide_viewport", frame=1020)
black_axis2.keyframe_insert(data_path="hide_render", frame=1020)

black_tip2.hide_viewport = False
black_tip2.hide_render = False
black_tip2.keyframe_insert(data_path="hide_viewport", frame=1020)
black_tip2.keyframe_insert(data_path="hide_render", frame=1020)

bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=3.0, location=(3, 3, 0))
green_axis2 = bpy.context.active_object
green_axis2.name = "GreenAxis2"
green_axis2.rotation_euler = (0.4, 0.0, 0.0)

bpy.ops.mesh.primitive_cone_add(radius1=0.16, depth=0.4, location=(0, 0, 1.6))
green_tip2 = bpy.context.active_object
green_tip2.name = "GreenArrowTip2"
green_tip2.parent = green_axis2

mat_orange = create_material_from_rgb("OrangeMaterial", 10, 12, 65)
green_axis2.data.materials.append(mat_orange)
green_tip2.data.materials.append(mat_orange)

planet2.parent = green_axis2

start_rot = 10 * 2 * math.pi

# Animácia pre naklonenú os (green_axis1)
green_axis2.rotation_euler = (-2.5, 0.0, 0.0)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=1)
green_axis2.rotation_euler = (-2.5, 0.0, start_rot)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=480)
green_axis2.rotation_euler = (0.4, 0.0, start_rot)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=495)

green_axis2.rotation_euler = (0.4, 0.0, start_rot + 6*2 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=700)

# Animácia pre planétu (planet1)
planet2.rotation_euler = (0.0, 0.0, 0.0)
planet2.keyframe_insert(data_path="rotation_euler", frame=1)
planet2.rotation_euler = (0.0, 0.0, start_rot)
planet2.keyframe_insert(data_path="rotation_euler", frame=480)

# Zmena interpolácie na LINEAR pre prvú skupinu
for fcurve in green_axis2.animation_data.action.fcurves:
    for key in fcurve.keyframe_points:
        if key.co[0] <= 690:
            key.interpolation = 'LINEAR'
for fcurve in planet2.animation_data.action.fcurves:
    for key in fcurve.keyframe_points:
        if key.co[0] <= 690:
            key.interpolation = 'LINEAR'
# Frame 480: východiskový stav
start_rot2  = start_rot + 6*2 * math.pi
green_axis2.rotation_euler = (0.4, 0.0, start_rot2)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=700)

# Frame 490: rýchly prechod – dosiahnutie 90° tilt, rotácia ostáva rovnaká
green_axis2.rotation_euler = (1.57, 0.0, start_rot2)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=710)

# Pridanie medzikľúčového snímku, kde rotácia dosiahne vyššiu hodnotu – simulujeme rýchly úsek
# Tu nastavte hodnotu tak, aby medzi frame 490 a 600 bola vyššia rýchlosť (väčší nárast rotácie)
green_axis2.rotation_euler = (1.57, 0.0, start_rot2 + 2 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=720)

# Frame 720: finálna hodnota – tilt sa vráti na pôvod (0.4) a rotácia dosiahne cieľovú hodnotu
green_axis2.rotation_euler = (0.4, 0.0, start_rot2 + 36 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=840)

new_start_rot = start_rot2 + 36 * math.pi  # začneme od poslednej hodnoty
green_axis2.rotation_euler = (0.4, 0.0, new_start_rot + 10 * 2 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=1120)

# -----------------------------------------
# 3. Tretia varianta - modrá guľa na opačnej strane (X osi)
# -----------------------------------------
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(0, 0, 0))
planet2 = bpy.context.active_object
planet2.name = "Planet2"

mat_blue = create_material_from_rgb("BlueMaterial", 225, 2, 0)
planet2.data.materials.append(mat_blue)

bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=3.0, location=(-3, 3, 0))
black_axis2 = bpy.context.active_object
black_axis2.name = "BlackAxis2"

bpy.ops.mesh.primitive_cone_add(radius1=0.1, depth=0.2, location=(0, 0, 1.5))
black_tip2 = bpy.context.active_object
black_tip2.name = "BlackArrowTip2"
black_tip2.parent = black_axis2

black_axis2.data.materials.append(mat_black)
black_tip2.data.materials.append(mat_black)

# Na začiatku (frame 1) nech je čierna šípka skrytá:
black_axis2.hide_viewport = True
black_axis2.hide_render = True
black_axis2.keyframe_insert(data_path="hide_viewport", frame=1)
black_axis2.keyframe_insert(data_path="hide_render", frame=1)

black_tip2.hide_viewport = True
black_tip2.hide_render = True
black_tip2.keyframe_insert(data_path="hide_viewport", frame=1)
black_tip2.keyframe_insert(data_path="hide_render", frame=1)

# Od frame 480 sa má zobraziť:
black_axis2.hide_viewport = False
black_axis2.hide_render = False
black_axis2.keyframe_insert(data_path="hide_viewport", frame=1020)
black_axis2.keyframe_insert(data_path="hide_render", frame=1020)

black_tip2.hide_viewport = False
black_tip2.hide_render = False
black_tip2.keyframe_insert(data_path="hide_viewport", frame=1020)
black_tip2.keyframe_insert(data_path="hide_render", frame=1020)

bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=3.0, location=(-3, 3, 0))
green_axis2 = bpy.context.active_object
green_axis2.name = "GreenAxis2"
green_axis2.rotation_euler = (0.4, 0.0, 0.0)

bpy.ops.mesh.primitive_cone_add(radius1=0.16, depth=0.4, location=(0, 0, 1.6))
green_tip2 = bpy.context.active_object
green_tip2.name = "GreenArrowTip2"
green_tip2.parent = green_axis2

mat_orange = create_material_from_rgb("OrangeMaterial", 10, 12, 65)
green_axis2.data.materials.append(mat_orange)
green_tip2.data.materials.append(mat_orange)

planet2.parent = green_axis2

start_rot = 10 * 2 * math.pi

# Animácia pre naklonenú os (green_axis1)
green_axis2.rotation_euler = (-0.25, 3.0, 0.0)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=1)
green_axis2.rotation_euler = (-0.25, 3.0, start_rot)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=480)
green_axis2.rotation_euler = (0.4, 3.0, start_rot)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=495)

green_axis2.rotation_euler = (0.4, 3.0, start_rot + 6*2 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=700)

# Animácia pre planétu (planet1)
planet2.rotation_euler = (0.0, 0.0, 0.0)
planet2.keyframe_insert(data_path="rotation_euler", frame=1)
planet2.rotation_euler = (0.0, 0.0, start_rot)
planet2.keyframe_insert(data_path="rotation_euler", frame=480)

# Zmena interpolácie na LINEAR pre prvú skupinu
for fcurve in green_axis2.animation_data.action.fcurves:
    for key in fcurve.keyframe_points:
        if key.co[0] <= 690:
            key.interpolation = 'LINEAR'
for fcurve in planet2.animation_data.action.fcurves:
    for key in fcurve.keyframe_points:
        if key.co[0] <= 690:
            key.interpolation = 'LINEAR'
# Frame 480: východiskový stav
start_rot2  = start_rot + 6*2 * math.pi
green_axis2.rotation_euler = (0.4, 3.0, start_rot2)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=700)

# Frame 490: rýchly prechod – dosiahnutie 90° tilt, rotácia ostáva rovnaká
green_axis2.rotation_euler = (1.57, 3.0, start_rot2)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=710)

# Pridanie medzikľúčového snímku, kde rotácia dosiahne vyššiu hodnotu – simulujeme rýchly úsek
# Tu nastavte hodnotu tak, aby medzi frame 490 a 600 bola vyššia rýchlosť (väčší nárast rotácie)
green_axis2.rotation_euler = (1.57, 3.0, start_rot2 + 2 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=720)

# Frame 720: finálna hodnota – tilt sa vráti na pôvod (0.4) a rotácia dosiahne cieľovú hodnotu
green_axis2.rotation_euler = (0.4, 3.0, start_rot2 + 36 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=840)

new_start_rot = start_rot2 + 36 * math.pi  # začneme od poslednej hodnoty
green_axis2.rotation_euler = (0.4, 3.0, new_start_rot + 10 * 2 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=1120)

################################################################################
# 3. rad
################################################################################
# ------------------------------
# 1. Prvá rotujúca guľa (červená)
# ------------------------------
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(0, 0, 0))
planet1 = bpy.context.active_object
planet1.name = "Planet1"

mat_red = create_material_from_rgb("RedMaterial", 225, 2, 0)
planet1.data.materials.append(mat_red)

bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=3.0, location=(0, -3, 0))
black_axis1 = bpy.context.active_object
black_axis1.name = "BlackAxis1"

bpy.ops.mesh.primitive_cone_add(radius1=0.1, depth=0.2, location=(0, 0, 1.5))
black_tip1 = bpy.context.active_object
black_tip1.name = "BlackArrowTip1"
black_tip1.parent = black_axis1

black_axis1.data.materials.append(mat_black)
black_tip1.data.materials.append(mat_black)

# Na začiatku (frame 1) nech je čierna šípka skrytá:
black_axis1.hide_viewport = True
black_axis1.hide_render = True
black_axis1.keyframe_insert(data_path="hide_viewport", frame=1)
black_axis1.keyframe_insert(data_path="hide_render", frame=1)

black_tip1.hide_viewport = True
black_tip1.hide_render = True
black_tip1.keyframe_insert(data_path="hide_viewport", frame=1)
black_tip1.keyframe_insert(data_path="hide_render", frame=1)

# Od frame 480 sa má zobraziť:
black_axis1.hide_viewport = False
black_axis1.hide_render = False
black_axis1.keyframe_insert(data_path="hide_viewport", frame=1020)
black_axis1.keyframe_insert(data_path="hide_render", frame=1020)

black_tip1.hide_viewport = False
black_tip1.hide_render = False
black_tip1.keyframe_insert(data_path="hide_viewport", frame=1020)
black_tip1.keyframe_insert(data_path="hide_render", frame=1020)



bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=3.0, location=(0, -3, 0))
green_axis1 = bpy.context.active_object
green_axis1.name = "GreenAxis1"
green_axis1.rotation_euler = (0.4, 0.0, 0.0)

bpy.ops.mesh.primitive_cone_add(radius1=0.16, depth=0.4, location=(0, 0, 1.6))
green_tip1 = bpy.context.active_object
green_tip1.name = "GreenArrowTip1"
green_tip1.parent = green_axis1

mat_green = create_material_from_rgb("GreenMaterial", 10, 12, 65)
green_axis1.data.materials.append(mat_green)
green_tip1.data.materials.append(mat_green)

planet1.parent = green_axis1

start_rot = 10 * 2 * math.pi

# Animácia pre naklonenú os (green_axis1)
green_axis1.rotation_euler = (-1.8, 1.2, 0.0)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=1)
green_axis1.rotation_euler = (-1.8, 1.2, start_rot)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=480)
green_axis1.rotation_euler = (0.4, 0.0, start_rot)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=495)

green_axis1.rotation_euler = (0.4, 0.0, start_rot + 6*2 * math.pi)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=700)

# Animácia pre planétu (planet1)
planet1.rotation_euler = (0.0, 0.0, 0.0)
planet1.keyframe_insert(data_path="rotation_euler", frame=1)
planet1.rotation_euler = (0.0, 0.0, start_rot)
planet1.keyframe_insert(data_path="rotation_euler", frame=480)

# Zmena interpolácie na LINEAR pre prvú skupinu
for fcurve in green_axis1.animation_data.action.fcurves:
    for key in fcurve.keyframe_points:
        if key.co[0] <= 690:
            key.interpolation = 'LINEAR'
for fcurve in planet1.animation_data.action.fcurves:
    for key in fcurve.keyframe_points:
        if key.co[0] <= 690:
            key.interpolation = 'LINEAR'
# Frame 480: východiskový stav
start_rot2  = start_rot + 6*2 * math.pi
green_axis1.rotation_euler = (0.4, 0.0, start_rot2)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=700)

# Frame 490: rýchly prechod – dosiahnutie 90° tilt, rotácia ostáva rovnaká
green_axis1.rotation_euler = (1.57, 0.0, start_rot2)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=710)

# Pridanie medzikľúčového snímku, kde rotácia dosiahne vyššiu hodnotu – simulujeme rýchly úsek
# Tu nastavte hodnotu tak, aby medzi frame 490 a 600 bola vyššia rýchlosť (väčší nárast rotácie)
green_axis1.rotation_euler = (1.57, 0.0, start_rot2 + 2 * math.pi)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=720)

# Frame 720: finálna hodnota – tilt sa vráti na pôvod (0.4) a rotácia dosiahne cieľovú hodnotu
green_axis1.rotation_euler = (0.4, 0.0, start_rot2 + 36 * math.pi)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=840)

new_start_rot = start_rot2 + 36 * math.pi  # začneme od poslednej hodnoty
green_axis1.rotation_euler = (0.4, 0.0, new_start_rot + 10 * 2 * math.pi)
green_axis1.keyframe_insert(data_path="rotation_euler", frame=1120)


# -----------------------------------------
# 2. Druhá rotujúca guľa (modrá) - posunutá na X osi
# -----------------------------------------
offset = 3.0

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(0, 0, 0))
planet2 = bpy.context.active_object
planet2.name = "Planet2"

mat_blue = create_material_from_rgb("BlueMaterial", 225, 2, 0)
planet2.data.materials.append(mat_blue)

bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=3.0, location=(3, -3, 0))
black_axis2 = bpy.context.active_object
black_axis2.name = "BlackAxis2"

bpy.ops.mesh.primitive_cone_add(radius1=0.1, depth=0.2, location=(0, 0, 1.5))
black_tip2 = bpy.context.active_object
black_tip2.name = "BlackArrowTip2"
black_tip2.parent = black_axis2

black_axis2.data.materials.append(mat_black)
black_tip2.data.materials.append(mat_black)

# Na začiatku (frame 1) nech je čierna šípka skrytá:
black_axis2.hide_viewport = True
black_axis2.hide_render = True
black_axis2.keyframe_insert(data_path="hide_viewport", frame=1)
black_axis2.keyframe_insert(data_path="hide_render", frame=1)

black_tip2.hide_viewport = True
black_tip2.hide_render = True
black_tip2.keyframe_insert(data_path="hide_viewport", frame=1)
black_tip2.keyframe_insert(data_path="hide_render", frame=1)

# Od frame 480 sa má zobraziť:
black_axis2.hide_viewport = False
black_axis2.hide_render = False
black_axis2.keyframe_insert(data_path="hide_viewport", frame=1020)
black_axis2.keyframe_insert(data_path="hide_render", frame=1020)

black_tip2.hide_viewport = False
black_tip2.hide_render = False
black_tip2.keyframe_insert(data_path="hide_viewport", frame=1020)
black_tip2.keyframe_insert(data_path="hide_render", frame=1020)

bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=3.0, location=(3, -3, 0))
green_axis2 = bpy.context.active_object
green_axis2.name = "GreenAxis2"
green_axis2.rotation_euler = (0.4, 0.0, 0.0)

bpy.ops.mesh.primitive_cone_add(radius1=0.16, depth=0.4, location=(0, 0, 1.6))
green_tip2 = bpy.context.active_object
green_tip2.name = "GreenArrowTip2"
green_tip2.parent = green_axis2

mat_orange = create_material_from_rgb("OrangeMaterial", 10, 12, 65)
green_axis2.data.materials.append(mat_orange)
green_tip2.data.materials.append(mat_orange)

planet2.parent = green_axis2

start_rot = 10 * 2 * math.pi

# Animácia pre naklonenú os (green_axis1)
green_axis2.rotation_euler = (2.5, 1.0, 0.0)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=1)
green_axis2.rotation_euler = (2.5, 1.0, start_rot)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=480)
green_axis2.rotation_euler = (0.4, 0.0, start_rot)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=495)

green_axis2.rotation_euler = (0.4, 0.0, start_rot + 6*2 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=700)

# Animácia pre planétu (planet1)
planet2.rotation_euler = (0.0, 0.0, 0.0)
planet2.keyframe_insert(data_path="rotation_euler", frame=1)
planet2.rotation_euler = (0.0, 0.0, start_rot)
planet2.keyframe_insert(data_path="rotation_euler", frame=480)

# Zmena interpolácie na LINEAR pre prvú skupinu
for fcurve in green_axis2.animation_data.action.fcurves:
    for key in fcurve.keyframe_points:
        if key.co[0] <= 690:
            key.interpolation = 'LINEAR'
for fcurve in planet2.animation_data.action.fcurves:
    for key in fcurve.keyframe_points:
        if key.co[0] <= 690:
            key.interpolation = 'LINEAR'
# Frame 480: východiskový stav
start_rot2  = start_rot + 6*2 * math.pi
green_axis2.rotation_euler = (0.4, 0.0, start_rot2)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=700)

# Frame 490: rýchly prechod – dosiahnutie 90° tilt, rotácia ostáva rovnaká
green_axis2.rotation_euler = (1.57, 0.0, start_rot2)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=710)

# Pridanie medzikľúčového snímku, kde rotácia dosiahne vyššiu hodnotu – simulujeme rýchly úsek
# Tu nastavte hodnotu tak, aby medzi frame 490 a 600 bola vyššia rýchlosť (väčší nárast rotácie)
green_axis2.rotation_euler = (1.57, 0.0, start_rot2 + 2 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=720)

# Frame 720: finálna hodnota – tilt sa vráti na pôvod (0.4) a rotácia dosiahne cieľovú hodnotu
green_axis2.rotation_euler = (0.4, 0.0, start_rot2 + 36 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=840)

new_start_rot = start_rot2 + 36 * math.pi  # začneme od poslednej hodnoty
green_axis2.rotation_euler = (0.4, 0.0, new_start_rot + 10 * 2 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=1120)
# -----------------------------------------
# 3. Tretia varianta - modrá guľa na opačnej strane (X osi)
# -----------------------------------------
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(0, 0, 0))
planet2 = bpy.context.active_object
planet2.name = "Planet2"

mat_blue = create_material_from_rgb("BlueMaterial", 225, 2, 0)
planet2.data.materials.append(mat_blue)

bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=3.0, location=(-3, -3, 0))
black_axis2 = bpy.context.active_object
black_axis2.name = "BlackAxis2"

bpy.ops.mesh.primitive_cone_add(radius1=0.1, depth=0.2, location=(0, 0, 1.5))
black_tip2 = bpy.context.active_object
black_tip2.name = "BlackArrowTip2"
black_tip2.parent = black_axis2

black_axis2.data.materials.append(mat_black)
black_tip2.data.materials.append(mat_black)

# Na začiatku (frame 1) nech je čierna šípka skrytá:
black_axis2.hide_viewport = True
black_axis2.hide_render = True
black_axis2.keyframe_insert(data_path="hide_viewport", frame=1)
black_axis2.keyframe_insert(data_path="hide_render", frame=1)

black_tip2.hide_viewport = True
black_tip2.hide_render = True
black_tip2.keyframe_insert(data_path="hide_viewport", frame=1)
black_tip2.keyframe_insert(data_path="hide_render", frame=1)

# Od frame 480 sa má zobraziť:
black_axis2.hide_viewport = False
black_axis2.hide_render = False
black_axis2.keyframe_insert(data_path="hide_viewport", frame=1020)
black_axis2.keyframe_insert(data_path="hide_render", frame=1020)

black_tip2.hide_viewport = False
black_tip2.hide_render = False
black_tip2.keyframe_insert(data_path="hide_viewport", frame=1020)
black_tip2.keyframe_insert(data_path="hide_render", frame=1020)

bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=3.0, location=(-3, -3, 0))
green_axis2 = bpy.context.active_object
green_axis2.name = "GreenAxis2"
green_axis2.rotation_euler = (0.4, 0.0, 0.0)

bpy.ops.mesh.primitive_cone_add(radius1=0.16, depth=0.4, location=(0, 0, 1.6))
green_tip2 = bpy.context.active_object
green_tip2.name = "GreenArrowTip2"
green_tip2.parent = green_axis2

mat_orange = create_material_from_rgb("OrangeMaterial", 10, 12, 65)
green_axis2.data.materials.append(mat_orange)
green_tip2.data.materials.append(mat_orange)

planet2.parent = green_axis2

start_rot = 10 * 2 * math.pi

# Animácia pre naklonenú os (green_axis1)
green_axis2.rotation_euler = (5.4, 0.0, 0.0)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=1)
green_axis2.rotation_euler = (1.4, 0.0, start_rot)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=480)
green_axis2.rotation_euler = (0.4, 3.0, start_rot)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=495)

green_axis2.rotation_euler = (0.4, 3.0, start_rot + 6*2 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=700)

# Animácia pre planétu (planet1)
planet2.rotation_euler = (0.0, 0.0, 0.0)
planet2.keyframe_insert(data_path="rotation_euler", frame=1)
planet2.rotation_euler = (0.0, 0.0, start_rot)
planet2.keyframe_insert(data_path="rotation_euler", frame=480)

# Zmena interpolácie na LINEAR pre prvú skupinu
for fcurve in green_axis2.animation_data.action.fcurves:
    for key in fcurve.keyframe_points:
        if key.co[0] <= 690:
            key.interpolation = 'LINEAR'
for fcurve in planet2.animation_data.action.fcurves:
    for key in fcurve.keyframe_points:
        if key.co[0] <= 690:
            key.interpolation = 'LINEAR'
# Frame 480: východiskový stav
start_rot2  = start_rot + 6*2 * math.pi
green_axis2.rotation_euler = (0.4, 3.0, start_rot2)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=700)

# Frame 490: rýchly prechod – dosiahnutie 90° tilt, rotácia ostáva rovnaká
green_axis2.rotation_euler = (1.57, 3.0, start_rot2)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=710)

# Pridanie medzikľúčového snímku, kde rotácia dosiahne vyššiu hodnotu – simulujeme rýchly úsek
# Tu nastavte hodnotu tak, aby medzi frame 490 a 600 bola vyššia rýchlosť (väčší nárast rotácie)
green_axis2.rotation_euler = (1.57, 3.0, start_rot2 + 2 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=720)

# Frame 720: finálna hodnota – tilt sa vráti na pôvod (0.4) a rotácia dosiahne cieľovú hodnotu
green_axis2.rotation_euler = (0.4, 3.0, start_rot2 + 36 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=840)

new_start_rot = start_rot2 + 36 * math.pi  # začneme od poslednej hodnoty
green_axis2.rotation_euler = (0.4, 3.0, new_start_rot + 10 * 2 * math.pi)
green_axis2.keyframe_insert(data_path="rotation_euler", frame=1120)

# -----------------------------------------
# =============================================================================
# Nová časť: 4 čierne šípky – umiestnené pozdĺž osi Z
# =============================================================================
# Funkcia na vytvorenie šípky (zložená z valca a kužeľa)
def create_arrow(name, location):
    """
    Vytvorí šípku orientovanú pozdĺž osi Z so šedým tvarom:
      - Telo (cylinder) s polomerom 0.15 a výškou 3
      - Hlava (kužeľ) s polomerom 0.2 a výškou 1
    Šípka sa následne spojí do jedného objektu a je priradený čierny materiál.
    :param name: názov výsledného objektu
    :param location: počiatočné súradnice (x, y, z)
    :return: vytvorený objekt so šípkou
    """
    # Vytvoríme telo šípky
    bpy.ops.mesh.primitive_cylinder_add(radius=0.13, depth=3, location=(0, 0, 0.7))
    body = bpy.context.active_object
    body.name = name + "_Body"
    
    # Vytvoríme hlavu šípky
    bpy.ops.mesh.primitive_cone_add(radius1=0.2, depth=0.8, location=(0, 0, 2.5))
    head = bpy.context.active_object
    head.name = name + "_Head"
    
    # Vyberieme obe časti a spojíme ich
    body.select_set(True)
    head.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.join()
    arrow = bpy.context.active_object
    arrow.name = name
    
    # Aplikujeme čierny materiál (vytvorený pomocou funkcie)
    arrow_mat = create_material_from_rgb("ArrowBlack", 0, 0, 0)
    if arrow.data.materials:
        arrow.data.materials[0] = arrow_mat
    else:
        arrow.data.materials.append(arrow_mat)
    
    # Nastavíme počiatočnú polohu a vložíme keyframe na frame 1
    arrow.location = location
    arrow.keyframe_insert(data_path="location", frame=1)
    
    # Nastavíme šípku ako skrytú na začiatku (frame 1)
    arrow.hide_viewport = True
    arrow.hide_render = True
    arrow.keyframe_insert(data_path="hide_viewport", frame=1)
    arrow.keyframe_insert(data_path="hide_render", frame=1)
    
    # Na frame 100 nastavíme šípku ako viditeľnú
    arrow.hide_viewport = False
    arrow.hide_render = False
    arrow.keyframe_insert(data_path="hide_viewport", frame=380)
    arrow.keyframe_insert(data_path="hide_render", frame=380)
    
    return arrow

# Definícia počiatočných a konečných súradníc pre každú šípku
arrows_data = [
    {"name": "Arrow1", "start": (150, 150, 0), "end": (4, 4, 0)},
    {"name": "Arrow2", "start": (-150, 150, 0), "end": (-4, 4, 0)},
    {"name": "Arrow3", "start": (150, -150, 0), "end": (4, -4, 0)},
    {"name": "Arrow4", "start": (-150, -150, 0), "end": (-4, -4, 0)},
]

# Vytvorenie šípok a nastavenie animácie (premiestnenie na frame 200)
for data in arrows_data:
    arrow = create_arrow(data["name"], data["start"])
    arrow.location = data["end"]
    arrow.keyframe_insert(data_path="location", frame=480)


import bpy
import numpy as np
import math

def create_sine_curve(phase=0.0, rotation_angle=90, amplitude=1.0, frequency=1.0, name="SineCurve"):
    # Ak už objekt existuje, vrátime ho
    existing_obj = bpy.data.objects.get(name)
    if existing_obj:
        return existing_obj

    theta = math.radians(rotation_angle)
    
    # Vytvorenie novej krivky typu CURVE
    curve_data = bpy.data.curves.new(name=name, type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.bevel_depth = 0.05  # Hrúbka čiary
    
    # Vytvorenie polyline spline – počet bodov nastavte podľa potreby
    num_points = 50
    spline = curve_data.splines.new(type='POLY')
    spline.points.add(num_points - 1)  # prvý bod už existuje
    
    # Vypočítame súradnice bodov na základe sínusovej funkcie
    x_values = np.linspace(-2, 2, num_points)
    for i, x in enumerate(x_values):
        y = amplitude * np.sin(frequency * (x - phase))
        x_rot = x * math.cos(theta) - y * math.sin(theta)
        y_rot = x * math.sin(theta) + y * math.cos(theta)
        # Os X = 0, os Y dostáva y_rot, os Z dostáva x_rot
        spline.points[i].co = (0, y_rot, x_rot, 1)
    
    # Vytvorenie objektu pre krivku a pripojenie do kolekcie
    curve_obj = bpy.data.objects.new(name, curve_data)
    bpy.context.collection.objects.link(curve_obj)
    return curve_obj

# Použitie funkcie na vytvorenie alebo získanie existujúcej sínusovej krivky
sine_obj = create_sine_curve(phase=0, rotation_angle=90, amplitude=1.0, frequency=2)

# Pridanie materiálu s čiernou farbou, ak ešte nie je priradený
if not sine_obj.data.materials:
    black_mat = bpy.data.materials.new(name="BlackMaterial")
    black_mat.diffuse_color = (0, 0, 0, 1)  # RGBA: čierna
    sine_obj.data.materials.append(black_mat)

# Aktualizácia animácie a ďalších vlastností podľa potreby...
sine_obj.location = (0, 20, 6)
sine_obj.keyframe_insert(data_path="location", frame=650)
sine_obj.location = (0, 1, 2)
sine_obj.keyframe_insert(data_path="location", frame=700)

sine_obj.rotation_euler = (math.radians(35), 0, 0)

# Handler pre aktualizáciu sínusovej krivky pri zmene frame
def update_sine_curve(scene):
    frame = scene.frame_current
    if frame < 650 or frame > 700:
        sine_obj.hide_viewport = True
        sine_obj.hide_render = True
        return
    else:
        sine_obj.hide_viewport = False
        sine_obj.hide_render = False

    phase = (frame / 50.0) * 2 * np.pi
    theta = math.radians(90)
    amplitude = 0.5
    frequency = 6

    spline = sine_obj.data.splines[0]
    num_points = len(spline.points)
    x_values = np.linspace(-2, 2, num_points)
    for i, x in enumerate(x_values):
        y = amplitude * np.sin(frequency * (x - phase))
        x_rot = x * math.cos(theta) - y * math.sin(theta)
        y_rot = x * math.sin(theta) + y * math.cos(theta)
        spline.points[i].co = (0, y_rot, x_rot, 1)
    sine_obj.data.update()

# Odstránenie existujúcich handlerov a priradenie nového
bpy.app.handlers.frame_change_post.clear()
bpy.app.handlers.frame_change_post.append(update_sine_curve)

print("Skript spustený – sínusová krivka je viditeľná len medzi frame 650 a 700.")
