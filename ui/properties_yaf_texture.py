# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from rna_prop_ui import PropertyPanel
from bpy.props import *
Texture = bpy.types.Texture

Texture.yaf_tex_type = EnumProperty(
    items = (
            # ("TEXTURE_TYPE","Texture Type",""),
            ("NONE", "None", ""),
            ("BLEND", "Blend", ""),
            ("CLOUDS", "Clouds", ""),
            ("WOOD", "Wood", ""),
            ("MARBLE", "Marble", ""),
            ("VORONOI", "Voronoi", ""),
            ("MUSGRAVE", "Musgrave", ""),
            ("DISTORTED_NOISE", "Distorted Noise", ""),
            ("IMAGE", "Image", "")),
    default = "NONE",
    name = "Texture Type")

Texture.yaf_texture_coordinates = EnumProperty(attr = "yaf_texture_coordinates",
        items = (
                ("TEXTURE_COORDINATES", "Texture Co-Ordinates", ""),
                ("GLOBAL", "Global", ""),
                ("ORCO", "Orco", ""),
                ("WINDOW", "Window", ""),
                ("NORMAL", "Normal", ""),
                ("REFLECTION", "Reflection", ""),
                ("STICKY", "Sticky", ""),
                ("STRESS", "Stress", ""),
                ("TANGENT", "Tangent", ""),
                ("OBJECT", "Object", ""),
                ("UV", "UV", ""),
), default = "GLOBAL")

Texture.tex_file_name = StringProperty(attr='tex_file_name', subtype = 'FILE_PATH')

Texture.yaf_is_normal_map = BoolProperty(default = False, name = "Normal map")

try:
    from properties_material import active_node_mat
except ImportError:
    from bl_ui.properties_material import active_node_mat  # API changes since rev. 35667


def context_tex_datablock(context):
    idblock = context.material
    if idblock:
        return active_node_mat(idblock)

    idblock = context.lamp
    if idblock:
        return idblock

    idblock = context.world
    if idblock:
        return idblock

    idblock = context.brush
    return idblock


class YAF_TextureButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "texture"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod  # no 2.53
    def poll(self, context):
        tex = context.texture
        engine = context.scene.render.engine

        return tex and (tex.type != 'NONE' or tex.use_nodes) and (engine in self.COMPAT_ENGINES)


class YAF_TEXTURE_PT_context_texture(YAF_TextureButtonsPanel, bpy.types.Panel):
    bl_label = "YafaRay Textures"
    bl_show_header = True  # False orig.
    COMPAT_ENGINES = {'YAFA_RENDER'}
    count = 0

    @classmethod
    def poll(self, context):
        engine = context.scene.render.engine
        if not hasattr(context, "texture_slot"):
            return False
        ##
        """ #  deprecated.. usefull?
        import properties_world

        import properties_texture

        if (context.world  and  (engine in self.COMPAT_ENGINES) ) :
            try :
                properties_world.unregister()
            except:
                pass
        else:
            try:
                properties_world.register()
            except:
                pass
        if (context.texture and  (engine in self.COMPAT_ENGINES) ) :
            try :
                properties_texture.unregister()
            except:
                pass
        else:
            try:
                properties_texture.register()
            except:
                pass
        """
        #return (context.texture  or context.world and  (engine in self.COMPAT_ENGINES) )
        return ((context.material or context.world or context.lamp or context.brush or context.texture)
            and (engine in self.COMPAT_ENGINES))

    def draw(self, context):
        layout = self.layout
        slot = context.texture_slot
        node = context.texture_node
        space = context.space_data
        tex = context.texture
        idblock = context_tex_datablock(context)
        pin_id = space.pin_id

        if not isinstance(pin_id, bpy.types.Material):  # isinstance, recen change  for beta 2.56
            pin_id = None

        tex_collection = (pin_id is None) and (node is None) and (not isinstance(idblock, bpy.types.Brush))

        if tex_collection:
            row = layout.row()

            row.template_list(idblock, "texture_slots", idblock, "active_texture_index", rows=2)

            col = row.column(align=True)
            col.operator("texture.slot_move", text="", icon='TRIA_UP').type = 'UP'
            col.operator("texture.slot_move", text="", icon='TRIA_DOWN').type = 'DOWN'
            #col.menu("TEXTURE_MT_specials", icon='DOWNARROW_HLT', text="")

        col = layout.column()

        if tex_collection:
            col.template_ID(idblock, "active_texture", new="texture.new")
        elif node:
            col.template_ID(node, "texture", new="texture.new")
        elif idblock:
            col.template_ID(idblock, "texture", new="texture.new")

        if space.pin_id:
            col.template_ID(space, "pin_id")

        if tex:
            split = layout.split(percentage=0.2)

            if tex.use_nodes:
                if slot:
                    split.label(text="Output:")
                    split.prop(slot, "output_node", text="")
            else:
                # FIXME: this should be yaf_tex_type, but then it seems the panels need to be changed.
                # right now with the Blender "type", we have lots of texture types we don't support
                layout.prop(tex, "type", text = "Type", icon = "TEXTURE")
                # layout.prop(tex, "yaf_tex_type", text = "Type", icon = "TEXTURE")


class YAF_TEXTURE_PT_preview(YAF_TextureButtonsPanel, bpy.types.Panel):
    bl_label = "Preview"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture
        slot = getattr(context, "texture_slot", None)
        idblock = context_tex_datablock(context)

        if idblock:
            layout.template_preview(tex, parent=idblock, slot=slot)
        else:
            layout.template_preview(tex, slot=slot)

# Texture Slot Panels #


class YAF_TextureSlotPanel(YAF_TextureButtonsPanel):
    #bl_label = "Slots Textures"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(self, context):
        if not hasattr(context, "texture_slot"):
            return False

        engine = context.scene.render.engine
        return YAF_TextureButtonsPanel.poll(self, context) and (engine in self.COMPAT_ENGINES)


class YAF_TEXTURE_PT_mapping(YAF_TextureSlotPanel, bpy.types.Panel):
    bl_label = "YafaRay Mapping (Map Input)"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(self, context):
        idblock = context_tex_datablock(context)
        if isinstance(idblock, bpy.types.Brush) and not context.sculpt_object:
            return False

        if not getattr(context, "texture_slot", None):
            return False

        engine = context.scene.render.engine
        return (engine in self.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        idblock = context_tex_datablock(context)

        #yaf_tex_type = context.texture_slot

        tex = context.texture_slot

        if not isinstance(idblock, bpy.types.Brush):
            col = layout.column()
            col.prop(tex, "texture_coords", text="Coordinates")  # 2.55
            # change to same type of blender mapping, for make stable

            if tex.texture_coords == 'ORCO':  # 2.55
                ob = context.object
                if ob and ob.type == 'MESH':
                    col.prop(ob.data, "texco_mesh", text="Mesh")

            elif tex.texture_coords == 'UV':
                ob = context.object
                if ob and ob.type == 'MESH':
                    col.prop_search(tex, "uv_layer", ob.data, "uv_textures", text="Layer")
                else:
                    col.prop(tex, "uv_layer", text="Layer")

            elif tex.texture_coords == 'OBJECT':
                col.prop(tex, "object", text="Object")

        if isinstance(idblock, bpy.types.Brush):  # recent change for beta 2.56
            if context.sculpt_object:
                layout.label(text="Brush Mapping:")
                layout.prop(tex, "map_mode", expand=True)

                row = layout.row()
                row.active = tex.map_mode in ('FIXED', 'TILED')
                row.prop(tex, "angle")
        else:
            if isinstance(idblock, bpy.types.Material):
                col.prop(tex, "mapping", text="Projection")

                split = layout.split()

                if tex.texture_coords in ('ORCO', 'UV'):
                    col.prop(tex, "use_from_dupli")
                elif tex.texture_coords == 'OBJECT':
                    col.prop(tex, "use_from_original")

                row = col.row()
                row.prop(tex, "mapping_x", text="")
                row.prop(tex, "mapping_y", text="")
                row.prop(tex, "mapping_z", text="")

        splitCol = col.split()

        splitCol.prop(tex, "offset")

        splitCol.prop(tex, "scale")


class YAF_TEXTURE_PT_influence(YAF_TextureSlotPanel, bpy.types.Panel):
    bl_label = "YafaRay Influence (Map To)"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(self, context):
        idblock = context_tex_datablock(context)
        if isinstance(idblock, bpy.types.Brush):  # recent change
            return False

        if not getattr(context, "texture_slot", None):
            return False

        engine = context.scene.render.engine
        return (engine in self.COMPAT_ENGINES)

    def factor_but(self, tex, layout, toggle, factor, name):  # new in last rev. of Blender
        row = layout.row(align = True)
        row.prop(tex, toggle, text = "")
        sub = row.row()
        sub.enabled = getattr(tex, toggle)
        sub.prop(tex, factor, text = name, slider = True)
        return sub  # XXX, temp. use_map_normal needs to override.

    def draw(self, context):

        layout = self.layout

        idblock = context_tex_datablock(context)

        tex_slot = context.texture_slot
        texture = context.texture

        shaderNodes = dict()
        shaderNodes["Bump"]         = ["use_map_normal", "normal_factor", "Bump"]
        shaderNodes["MirrorAmount"] = ["use_map_specular", "specular_factor", "Mirror Amount"]
        shaderNodes["MirrorColor"]  = ["use_map_color_spec", "specular_color_factor", "Mirror Color"]
        shaderNodes["DiffuseColor"] = ["use_map_color_diffuse", "diffuse_color_factor", "Diffuse Color"]
        shaderNodes["GlossyColor"]  = ["use_map_color_spec", "specular_color_factor", "Glossy Color"]
        shaderNodes["GlossyAmount"] = ["use_map_specular", "specular_factor", "Glossy Amount"]
        shaderNodes["Transparency"] = ["use_map_alpha", "alpha_factor", "Transparency"]
        shaderNodes["Translucency"] = ["use_map_translucency", "translucency_factor", "Translucency"]
        shaderNodes["BlendAmount"]  = ["use_map_diffuse", "diffuse_factor", "Blending Amount"]

        materialShaderNodes = dict()
        materialShaderNodes["glass"]           = ["Bump", "MirrorColor"]
        materialShaderNodes["rough_glass"]     = ["Bump", "MirrorColor"]
        materialShaderNodes["glossy"]          = ["DiffuseColor", "GlossyColor", "GlossyAmount", "Bump"]
        materialShaderNodes["coated_glossy"]   = ["DiffuseColor", "GlossyColor", "GlossyAmount", "Bump"]
        materialShaderNodes["shinydiffusemat"] = ["DiffuseColor", "MirrorAmount", "MirrorColor", "Transparency", "Translucency", "Bump"]
        materialShaderNodes["blend"]           = ["BlendAmount"]

        if isinstance(idblock, bpy.types.Material):
            material = context.material
            materialType = material.mat_type

            nodes = materialShaderNodes[materialType]

            col = layout.column()

            for node in nodes:
                value = shaderNodes[node]
                self.factor_but(tex_slot, col, value[0], value[1], value[2])
                if node == "Bump" and getattr(tex_slot, "use_map_normal") and texture.type == "IMAGE":
                    col.prop(texture, "yaf_is_normal_map", "Use map as normal map")

            col.separator()
            col.prop(tex_slot, "blend_type", text = "Blend")
            col.prop(tex_slot, "use_rgb_to_intensity")
            sub = col.column()
            sub.active = tex_slot.use_rgb_to_intensity
            sub.prop(tex_slot, "color", text = "")

            col.prop(tex_slot, "invert", text = "Negative")
            col.prop(tex_slot, "use_stencil")

        elif isinstance(idblock, bpy.types.World):  # for setup world texture
            split = layout.split()

            col = split.column()
            self.factor_but(tex_slot, col, "use_map_blend", "blend_factor", "Blend")
            self.factor_but(tex_slot, col, "use_map_horizon", "horizon_factor", "Horizon")
            col = split.column()
            self.factor_but(tex_slot, col, "use_map_zenith_up", "zenith_up_factor", "Zenith Up")
            self.factor_but(tex_slot, col, "use_map_zenith_down", "zenith_down_factor", "Zenith Down")

        if isinstance(idblock, bpy.types.Material) or isinstance(idblock, bpy.types.World):
            split = layout.split()
            col = split.column()
            col.prop(tex_slot, "default_value", text="Default Value", slider=True)

# Texture Type Panels #


class YAF_TextureTypePanel(YAF_TextureButtonsPanel):
    bl_label = "Texture Type "
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(self, context):
        tex = context.texture
        engine = context.scene.render.engine

        #next definition
        return tex and ((tex.type == self.tex_type and not tex.use_nodes) and (engine in self.COMPAT_ENGINES))


class YAF_TEXTURE_PT_clouds(YAF_TextureTypePanel, bpy.types.Panel):
    bl_label = "Clouds"
    tex_type = 'CLOUDS'
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture

        layout.prop(tex, "cloud_type", text="Cloud", expand=True)

        layout.label(text="Noise:")
        layout.prop(tex, "noise_type", text="Type", expand=True)
        layout.prop(tex, "noise_basis", text="Basis")

        split = layout.split()

        col = split.column()
        col.prop(tex, "noise_scale", text="Size")
        col.prop(tex, "noise_depth", text="Depth")


class YAF_TEXTURE_PT_wood(YAF_TextureTypePanel, bpy.types.Panel):
    bl_label = "Wood"
    tex_type = 'WOOD'
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture

        layout.prop(tex, "noisebasis_2", expand=True)
        layout.prop(tex, "wood_type", text="Wood Type")

        col = layout.column()
        col.active = tex.wood_type in ('RINGNOISE', 'BANDNOISE')
        col.label(text="Noise:")
        col.row().prop(tex, "noise_type", text="Type", expand=True)
        layout.prop(tex, "noise_basis", text="Basis")

        split = layout.split()
        split.active = tex.wood_type in ('RINGNOISE', 'BANDNOISE')

        col = split.column()
        col.prop(tex, "noise_scale", text="Size")
        col.prop(tex, "turbulence")


class YAF_TEXTURE_PT_marble(YAF_TextureTypePanel, bpy.types.Panel):
    bl_label = "Marble"
    tex_type = 'MARBLE'
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture

        layout.prop(tex, "marble_type", expand=True)
        layout.prop(tex, "noisebasis_2", expand=True)
        layout.label(text = "Noise:")
        layout.prop(tex, "noise_type", text="Type", expand=True)
        layout.prop(tex, "noise_basis", text="Basis")

        split = layout.split()

        col = split.column()
        col.prop(tex, "noise_scale", text="Size")
        col.prop(tex, "noise_depth", text="Depth")

        col.prop(tex, "turbulence", text="Turbulence")


class YAF_TEXTURE_PT_blend(YAF_TextureTypePanel, bpy.types.Panel):
    bl_label = "Blend"
    tex_type = 'BLEND'
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture

        layout.prop(tex, "progression")
        #
        sub = layout.row()
        #
        sub.enabled = (tex.progression in ('LINEAR', 'QUADRATIC', 'EASING', 'RADIAL'))
        sub.prop(tex, "use_flip_axis", expand=True)


class YAF_TEXTURE_PT_image(YAF_TextureTypePanel, bpy.types.Panel):
    bl_label = "Map Image"
    tex_type = 'IMAGE'
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture

        layout.template_image(tex, "image", tex.image_user)


def texture_filter_common(tex, layout):
    layout.label(text="Filter:")
    layout.prop(tex, "filter_type", text="")
    if tex.use_mipmap and tex.filter_type in ('AREA', 'EWA', 'FELINE'):
        if tex.filter_type == 'FELINE':
            layout.prop(tex, "filter_probes", text="Probes")
        else:
            layout.prop(tex, "filter_eccentricity", text="Eccentricity")

    layout.prop(tex, "filter_size")
    layout.prop(tex, "use_filter_size_min")


#   class YAF_TEXTURE_PT_image_sampling(YAF_TextureTypePanel, bpy.types.Panel):
#   bl_label = "Image Sampling"
#   bl_options = {'DEFAULT_CLOSED'}
#   tex_type = 'IMAGE'
#   COMPAT_ENGINES = {'YAFA_RENDER'}
#
#   def draw(self, context):
#       layout = self.layout
#
#       idblock = context_tex_datablock(context)
#       tex = context.texture
#
#       split = layout.split()
#
#       col = split.column()
#       col.label(text="Alpha:")
#       col.prop(tex, "use_alpha", text="Use")
#       col.prop(tex, "use_calculate_alpha", text="Calculate")
#       col.prop(tex, "use_flip_axis", text="Flip X/Y Axis")
#
#       col.separator()
#
#       #Only for Material based textures, not for Lamp/World...
#       if isinstance(idblock, bpy.types.Material):
#           col.prop(tex, "use_normal_map")
#           row = col.row()
#           row.active = tex.use_normal_map
#
#       col.prop(tex, "use_mipmap")
#       row = col.row()
#       row.active = tex.use_mipmap
#       row.prop(tex, "use_mipmap_gauss")
#       col.prop(tex, "use_interpolation")
#
#       texture_filter_common(tex, col)


class YAF_TEXTURE_PT_image_mapping(YAF_TextureTypePanel, bpy.types.Panel):
    bl_label = "Image Mapping"
    bl_options = {'DEFAULT_CLOSED'}
    tex_type = 'IMAGE'
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture

        layout.prop(tex, "extension")

        col = layout.column()

        if tex.extension == 'REPEAT':
            row = col.row(align = True)
            row.prop(tex, "repeat_x", text="X")
            row.prop(tex, "repeat_y", text="Y")
            col.separator()

        elif tex.extension == 'CHECKER':
            row = col.row()
            row.prop(tex, "use_checker_even", text="Even")
            row.prop(tex, "use_checker_odd", text="Odd")
            col.prop(tex, "checker_distance", text="Distance")
            col.separator()

        row = col.row(align = True)
        row.label(text = "Crop Minimum:")
        row.prop(tex, "crop_min_x", text="X")
        row.prop(tex, "crop_min_y", text="Y")

        col.separator()

        row = col.row(align = True)
        row.label(text = "Crop Maximum:")
        row.prop(tex, "crop_max_x", text="X")
        row.prop(tex, "crop_max_y", text="Y")


class YAF_TEXTURE_PT_musgrave(YAF_TextureTypePanel, bpy.types.Panel):
    bl_label = "Musgrave"
    tex_type = 'MUSGRAVE'
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture

        layout.prop(tex, "musgrave_type")

        split = layout.split()

        col = split.column()
        col.prop(tex, "dimension_max", text="Dimension")
        col.prop(tex, "lacunarity", text="Lacunarity")
        col.prop(tex, "octaves", text="Octaves")

        if (tex.musgrave_type in ('HETERO_TERRAIN', 'RIDGED_MULTIFRACTAL', 'HYBRID_MULTIFRACTAL')):
            col.prop(tex, "offset")
        if (tex.musgrave_type in ('RIDGED_MULTIFRACTAL', 'HYBRID_MULTIFRACTAL')):
            col.prop(tex, "gain")
            col.prop(tex, "noise_intensity", text="Intensity")

        layout.label(text="Noise:")

        layout.prop(tex, "noise_basis", text="Basis")

        split = layout.split()

        col = split.column()
        col.prop(tex, "noise_scale", text="Size")


class YAF_TEXTURE_PT_voronoi(YAF_TextureTypePanel, bpy.types.Panel):
    bl_label = "Voronoi"
    tex_type = 'VORONOI'
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture

        split = layout.split()

        col = split.column()
        col.label(text="Distance Metric:")
        col.prop(tex, "distance_metric", text="")
        sub = col.column()
        sub.enabled = tex.distance_metric == 'MINKOVSKY'
        sub.prop(tex, "minkovsky_exponent", text="Exponent")
        col.label(text="Coloring:")
        col.prop(tex, "color_mode", text="")
        col.prop(tex, "noise_intensity", text="Intensity")

        sub = col.column(align=True)
        sub.label(text="Feature Weights:")
        sub.prop(tex, "weight_1", text="1", slider=True)
        sub.prop(tex, "weight_2", text="2", slider=True)
        sub.prop(tex, "weight_3", text="3", slider=True)
        sub.prop(tex, "weight_4", text="4", slider=True)

        layout.label(text="Noise:")

        split = layout.split()

        col = split.column()
        col.prop(tex, "noise_scale", text="Size")


class YAF_TEXTURE_PT_distortednoise(YAF_TextureTypePanel, bpy.types.Panel):
    bl_label = "Distorted Noise"
    tex_type = 'DISTORTED_NOISE'
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture

        layout.prop(tex, "noise_distortion", text="")
        layout.prop(tex, "noise_basis", text="Basis")

        split = layout.split()

        col = split.column()
        col.prop(tex, "distortion", text="Distortion")
        col.prop(tex, "noise_scale", text="Size")
