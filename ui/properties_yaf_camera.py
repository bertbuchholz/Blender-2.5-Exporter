import bpy
#import types and props ---->
from bpy.props import *
Camera = bpy.types.Camera


Camera.camera_type = EnumProperty(
    items = (
        ("perspective", "Perspective", ""),
        ("architect", "Architect", ""),
        ("angular", "Angular", ""),
        ("orthographic", "Ortho", "")),
    default = "perspective",
    name = "Camera Type")
Camera.angular_angle =      FloatProperty(attr = "angular_angle", max = 180.0, default = 90.0, precision = 3)
Camera.max_angle     =      FloatProperty(attr = "max_angle", max = 180.0, default = 90.0, precision = 3)
Camera.mirrored      =      BoolProperty(attr = "mirrored")
Camera.circular      =      BoolProperty(attr = "circular")
Camera.use_clipping  =      BoolProperty(default = False)
Camera.bokeh_type    =      EnumProperty(attr = "bokeh_type",
    items = (
        ("disk1", "Disk1", ""),
        ("disk2", "Disk2", ""),
        ("triangle", "Triangle", ""),
        ("square", "Square", ""),
        ("pentagon", "Pentagon", ""),
        ("hexagon", "Hexagon", ""),
        ("ring", "Ring", "")
    ),
    default = "disk1",
    name = "Bokeh Type")
Camera.aperture =       FloatProperty(attr = "aperture", min = 0.0, max = 20.0, precision = 5)
Camera.bokeh_rotation = FloatProperty(attr = "bokeh_rotation", min = 0.0, max = 180, precision =3)
Camera.bokeh_bias =     EnumProperty(attr = "bokeh_bias",
    items = (
        ("uniform", "Uniform", ""),
        ("center", "Center", ""),
        ("edge", "Edge", "")),
    default = "uniform",
    name = "Bokeh Bias")
Camera.color_data =     FloatVectorProperty(attr = "color_data", description = "Point Info", subtype = "XYZ", step = 10, precision = 3)


class YAF_PT_camera(bpy.types.Panel):

    bl_label = 'Camera'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    COMPAT_ENGINES = ['YAFA_RENDER']

    @classmethod
    def poll(self, context):

        engine = context.scene.render.engine
        from bl_ui import properties_data_camera
        return (context.camera and (engine in self.COMPAT_ENGINES))

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        camera = context.camera

        col.row().prop(context.camera, "camera_type", expand = True, text = "Camera Type")
        col.separator()

        if context.camera.camera_type == 'angular':
            col.prop(context.camera, "angular_angle", text = "Angle")
            col.prop(context.camera, "max_angle", text = "Max Angle")
            col.prop(context.camera, "mirrored", text = "Mirrored")
            col.prop(context.camera, "circular", text = "Circular")

        elif camera.camera_type == 'orthographic':
            col.prop(context.camera, "ortho_scale", text = "Scale")

        elif camera.camera_type in ['perspective', 'architect']:
            col.prop(context.camera, "lens", text = "Focal Length")

            col.separator()

            col.label("Depth of Field")
            col.prop(context.camera, "aperture", text = "Aperture")
            col.prop(context.camera, "dof_object", text = "DOF object")
            if camera.dof_object == None:
                col.prop(context.camera, "dof_distance", text = "DOF distance")

            col.prop(context.camera, "bokeh_type", text = "Bokeh Type")
            col.prop(context.camera, "bokeh_bias", text = "Bokeh Bias")
            col.prop(context.camera, "bokeh_rotation", text = "Bokeh Rotation")


class YAF_PT_camera_display(bpy.types.Panel):

    bl_label = 'Display'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    COMPAT_ENGINES = ['YAFA_RENDER']

    @classmethod
    def poll(self, context):

        engine = context.scene.render.engine
        from bl_ui import properties_data_camera
        return (context.camera and (engine in self.COMPAT_ENGINES))

    def draw(self, context):
        layout = self.layout

        camera = context.camera

        split = layout.split()

        col = split.column()
        col.prop(camera, "show_limits", text = "Limits")
        col.prop(camera, "show_title_safe", text = "Title Safe")
        col.prop(camera, "show_name", text = "Name")
        col.separator()
        col.separator()
        col.label(text = "Clipping:")
        col.prop(context.camera, "use_clipping", text = "Use Clipping in render")

        col = split.column()
        col.prop(camera, "show_passepartout", text = "Passepartout")
        sub = col.column()
        sub.active = camera.show_passepartout
        sub.prop(camera, "passepartout_alpha", text = "Alpha", slider = True)
        col.label(text = "Camera size:")
        col.prop(camera, "draw_size", text = "")
        col.separator()
        col.separator()
        clip = col.column(align = True)
        clip.active = camera.use_clipping
        clip.prop(context.camera, "clip_start", text = "Start")
        clip.prop(context.camera, "clip_end", text = "End")
        layout.separator()
        layout.prop_menu_enum(camera, "show_guide")
