import math
import bpy
#import types and props ---->
from bpy.props import *
Scene = bpy.types.Scene

Scene.intg_light_method =   EnumProperty(
    items = (
        ("Direct Lighting", "Direct Lighting", ""),
        ("Photon Mapping", "Photon Mapping", ""),
        ("Pathtracing", "Pathtracing", ""),
        ("Debug", "Debug", ""),
        ("Bidirectional", "Bidirectional", ""),
        ("SPPM", "SPPM", ""),
        ("PBGI", "PBGI", "")
    ),
    default="Direct Lighting",
    name = "Lighting Method")
Scene.intg_use_caustics =   BoolProperty(attr="intg_use_caustics",
                                        description = "Enable photon map for caustics only",
                                        default = False)
Scene.intg_photons =        IntProperty(attr="intg_photons",
                                        description = "Number of photons to be shot",
                                        min = 1, max = 100000000,
                                        default = 500000)
Scene.intg_caustic_mix =    IntProperty(attr="intg_caustic_mix",
                                        description = "Max. number of photons to mix (blur)",
                                        min = 1, max = 10000,
                                        default = 100)
Scene.intg_caustic_depth =  IntProperty(attr="intg_caustic_depth",
                                        description = "Max. number of scatter events for photons",
                                        min = 0, max = 50,
                                        default = 10)
Scene.intg_caustic_radius = FloatProperty(attr="intg_caustic_radius",
                                        description = "Max. radius to search for photons",
                                        min = 0.0001, max = 100.0,
                                        default = 1.0)
Scene.intg_use_AO =         BoolProperty(attr="intg_use_AO",
                                        description = "Enable ambient occlusion",
                                        default = False)
Scene.intg_AO_samples =     IntProperty(attr="intg_AO_samples",
                                        description = "Number of samples for ambient occlusion",
                                        min = 1, max = 1000,
                                        default = 32)
Scene.intg_AO_distance =    FloatProperty(attr="intg_AO_distance",
                                        description = "Max. occlusion distance. Surfaces further away do not occlude ambient light",
                                        min = 0.0, max = 10000.0,
                                        default = 1.0)
Scene.intg_AO_color =       FloatVectorProperty(attr="intg_AO_color",
                                        description = "Color Settings", subtype = "COLOR",
                                        default = (0.9, 0.9, 0.9),
                                        step = 1, precision = 2,
                                        min = 0.0, max = 1.0,
                                        soft_min = 0.0, soft_max = 1.0)
Scene.intg_bounces =        IntProperty(attr="intg_bounces",
                                        description = "",
                                        min = 4, default = 4, soft_min = 4)
Scene.intg_diffuse_radius = FloatProperty(attr="intg_diffuse_radius",
                                        description = "Radius to search for diffuse photons",
                                        min = 0.001,
                                        default = 1.0)
Scene.intg_cPhotons =       IntProperty(attr="intg_cPhotons",
                                        description = "Number of caustic photons to be shot",
                                        min = 1,
                                        default = 500000)
Scene.intg_search =         IntProperty(attr="intg_search",
                                        description = "Maximum number of diffuse photons to be filtered",
                                        min = 1, max = 10000,
                                        default = 100)
Scene.intg_final_gather =   BoolProperty(attr="intg_final_gather",
                                        description = "Use final gathering (recommended)",
                                        default = True)
Scene.intg_fg_bounces =     IntProperty(attr="intg_fg_bounces",
                                        description = "Allow gather rays to extend to paths of this length",
                                        min = 1, max = 20,
                                        default = 3)
Scene.intg_fg_samples =     IntProperty(attr="intg_fg_samples",
                                        description = "Number of samples for final gathering",
                                        min = 1,
                                        default = 16)
Scene.intg_show_map =       BoolProperty(attr="intg_show_map",
                                        description = "Directly show radiance map, useful to calibrate the photon map (disables final gathering step)",
                                        default = False)
Scene.intg_use_bg =         BoolProperty(attr="intg_use_bg",
                                        description = "",
                                        default = False)
Scene.intg_caustic_method = EnumProperty(attr="intg_caustic_method",
                                        description = "Choose caustic rendering method",
    items = (
        ("None", "None", ""),
        ("Path", "Path", ""),
        ("Path+Photon", "Path+Photon", ""),
        ("Photon", "Photon", "")),
    default = "None",
    name = "Caustic Method")
Scene.intg_path_samples =   IntProperty(attr = "intg_path_samples",
                                        description = "Number of path samples per pixel sample",
                                        min = 1,
                                        default = 32)
Scene.intg_no_recursion =   BoolProperty(attr = "intg_no_recursion",
                                        description = "No recursive raytracing, only pure path tracing",
                                        default = False)
Scene.intg_debug_type =     EnumProperty(attr = "intg_debug_type",
    items = (
        ("N", "N", ""),
        ("dPdU", "dPdU", ""),
        ("dPdV", "dPdV", ""),
        ("NU", "NU", ""),
        ("NV", "NV", ""),
        ("dSdU", "dSdU", ""),
        ("dSdV", "dSdV", "")),
    default = "dSdV",
    name = "Debug Type")
Scene.intg_show_perturbed_normals = BoolProperty(attr = "intg_show_perturbed_normals",
                                        description = "Show the normals perturbed by bump and normal maps",
                                        default = False)

Scene.intg_pm_ire = BoolProperty(default = False);
Scene.intg_pass_num = IntProperty(min = 1, default = 1000);
Scene.intg_times = FloatProperty(min = 0.0, default = 1.0);
Scene.intg_photon_radius = FloatProperty(min = 0.0, default = 1.0);

Scene.intg_pbgi_samples = IntProperty(min = 1, default = 10);
Scene.intg_pbgi_debug = BoolProperty(default = False);
Scene.intg_pbgi_indirect = BoolProperty(default = False);
Scene.intg_pbgi_maxSolidAngle = FloatProperty(min = 0.0, max = 50.0, default = 0.5, precision = 3);
Scene.intg_pbgi_debugTreeDepth = IntProperty(min = 0, default = 2);
Scene.intg_pbgi_debugPointsToFile = BoolProperty(default = False);
Scene.intg_pbgi_debug_type = EnumProperty(
    items = (
        ("NoTree", "No Tree", ""),
        ("Tree", "Tree", ""),
        ("Tree_sh", "Tree SH", ""),
        ("Tree_sh_fb", "Tree SH FB", ""),
        ("Tree_sh_leafs", "Tree SH leafs", "")
        ),
    default = "Tree_sh",
    name = "Debug Tree Type")
Scene.intg_pbgi_render_single_pixel = BoolProperty(default = False);
Scene.intg_pbgi_pixel_x = IntProperty(min = 0, max = 1000, default = 0);
Scene.intg_pbgi_pixel_y = IntProperty(min = 0, max = 1000, default = 0);
Scene.intg_pbgi_do_load_gi_points = BoolProperty(default = False);
Scene.intg_pbgi_fb_resolution = IntProperty(min = 2, max = 128, default = 16);
Scene.intg_pbgi_fb_type = EnumProperty(
    items = (
        ("Simple", "Simple", ""),
        ("Accumulating", "Accumulating", "")
        ),
    default = "Simple",
    name = "FB Type")


class YAF_PT_render(bpy.types.Panel):

    bl_label = 'Yafaray Integrator'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    COMPAT_ENGINES = ['YAFA_RENDER']

    @classmethod
    def poll(self, context):

        engine = context.scene.render.engine
        return (context.scene.render and  (engine in self.COMPAT_ENGINES))

    def draw(self, context):

        layout = self.layout

        layout.prop(context.scene, "intg_light_method", text = "Lighting Methods")

        if context.scene.intg_light_method == 'Direct Lighting':

            row = layout.row()

            col = row.column(align=True)
            col.prop(context.scene, "intg_use_caustics", text = "Use Caustics", toggle = True)

            if context.scene.intg_use_caustics:
                col.prop(context.scene, "intg_photons", text = "Photons")
                col.prop(context.scene, "intg_caustic_mix", text = "Caustic Mix")
                col.prop(context.scene, "intg_caustic_depth", text = "Caustic Depth")
                col.prop(context.scene, "intg_caustic_radius", text = "Caustic Radius")

            col = row.column(align = True)
            col.prop(context.scene, "intg_use_AO", text = "Use Ambient Occlusion", toggle = True)

            if context.scene.intg_use_AO:
                col.prop(context.scene, "intg_AO_samples", text = "AO Samples")
                col.prop(context.scene, "intg_AO_distance", text = "AO Distance")
                col.prop(context.scene, "intg_AO_color", text = "AO Color")

        elif context.scene.intg_light_method == 'Photon Mapping':
            row = layout.row()

            row.prop(context.scene, "intg_bounces", text = "Depth")

            row = layout.row()

            col = row.column(align = True)
            col.label(" Diffuse Photons:", icon = "MOD_PHYSICS")
            col.prop(context.scene, "intg_photons", text = "Count")
            col.prop(context.scene, "intg_diffuse_radius", text = "Search Radius")
            col.prop(context.scene, "intg_search", text = "Search Count")

            col = row.column(align = True)
            col.label(" Caustic Photons:", icon = "MOD_PARTICLES")
            col.prop(context.scene, "intg_cPhotons", text = "Count")
            col.prop(context.scene, "intg_caustic_radius", text = "Search Radius")
            col.prop(context.scene, "intg_caustic_mix", text = "Search Count")

            row = layout.row()
            row.prop(context.scene, "intg_final_gather", text = "Final Gather", toggle = True, icon = "FORCE_FORCE")

            if context.scene.intg_final_gather:
                col = layout.row()
                col.prop(context.scene, "intg_fg_bounces", text = "Bounces")
                col.prop(context.scene, "intg_fg_samples", text = "Samples")
                col = layout.row()
                col.prop(context.scene, "intg_show_map", text = "Show radiance map", toggle = True)

        #col = layout.column() # only afect to pathtracing bloq
        elif context.scene.intg_light_method == 'Pathtracing':
            col = layout.row()
            col.prop(context.scene, "intg_caustic_method", text = "Caustic Method")

            col = layout.row()

            if context.scene.intg_caustic_method == 'Path+Photon':
                col.prop(context.scene, "intg_photons", text = "Photons")
                col.prop(context.scene, "intg_caustic_mix", text = "Caus. Mix")
                col = layout.row()
                col.prop(context.scene, "intg_caustic_depth", text = "Caus. Depth")
                col.prop(context.scene, "intg_caustic_radius", text = "Caus. Radius")

            if context.scene.intg_caustic_method == 'Photon':
                col.prop(context.scene, "intg_photons", text = "Photons")
                col.prop(context.scene, "intg_caustic_mix", text = "Caus. Mix")
                col = layout.row()
                col.prop(context.scene, "intg_caustic_depth", text = "Caus. Depth")
                col.prop(context.scene, "intg_caustic_radius", text = "Caus. Radius")

            col = layout.row()
            col.prop(context.scene, "intg_path_samples", text = "Path Samples")
            col.prop(context.scene, "intg_bounces", text = "Depth")
            col = layout.row()
            col.prop(context.scene, "intg_no_recursion", text = "No Recursion")
            col.prop(context.scene, "intg_use_bg", text = "Use Background")

        elif context.scene.intg_light_method == 'Debug':
            col = layout.row()
            col.prop(context.scene, "intg_debug_type", text = "Debug Type")
            col.prop(context.scene, "intg_show_perturbed_normals", text = "Perturbed Normals")

        elif context.scene.intg_light_method == 'SPPM':
            col = layout.column()
            col.prop(context.scene, "intg_photons", text= "Photons")
            col.prop(context.scene, "intg_pass_num", text= "Passes")
            col.prop(context.scene, "intg_bounces", text= "Bounces")
            col.prop(context.scene, "intg_times", text= "Times (?)")
            col.prop(context.scene, "intg_diffuse_radius", text= "Search radius")
            col.prop(context.scene, "intg_search", text= "Search count")
            col.prop(context.scene, "intg_pm_ire", text= "PM IRE")

        elif context.scene.intg_light_method == 'PBGI':
            col = layout.column()
            col.prop(context.scene, "intg_pbgi_samples", text= "Samples")
            col.prop(context.scene, "intg_pbgi_indirect", text= "Indirect Only")
            col.prop(context.scene, "intg_pbgi_debug", text= "Debug")
            col.prop(context.scene, "intg_pbgi_maxSolidAngle", text= "Solid Angle")
            col.prop(context.scene, "intg_pbgi_debugTreeDepth", text= "Debug Tree Depth")
            col.prop(context.scene, "intg_pbgi_debugPointsToFile", text= "Debug Output to File")
            col.prop(context.scene, "intg_pbgi_debug_type", text= "Debug Type")
            col.prop(context.scene, "intg_pbgi_render_single_pixel", text= "Render Single Pixel")
            col.prop(context.scene, "intg_pbgi_pixel_x", text= "X")
            col.prop(context.scene, "intg_pbgi_pixel_y", text= "Y")
            col.prop(context.scene, "intg_pbgi_do_load_gi_points", text= "Load Points from File")
            col.prop(context.scene, "intg_pbgi_fb_resolution", text= "FB Resolution")
            col.prop(context.scene, "intg_pbgi_fb_type", text= "FB Type")

            angle = math.atan(1.0 / (context.scene.intg_pbgi_fb_resolution / 2))
            maxSolidAngle = 2.0 * math.pi * (1.0 - math.cos(angle))
            col.label("Solid angle: " + str(maxSolidAngle))

