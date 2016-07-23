import bpy

# Sets video strips as proxies
# TODO: Only if setting enabled in preferences
class SetVideosProxies(bpy.types.Operator):
    bl_idname = "gdquest_vse.set_video_proxies"
    bl_label = "Set Videos as Proxies"
    bl_description = "Set all video strips as proxies and rebuild"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        sequencer = bpy.ops.sequencer

        for s in bpy.context.sequences:
            if s.type == 'MOVIE':
                s.select = True

        sequencer.enable_proxies(proxy_25 = True,
                                proxy_50 =  False,
                                proxy_75 =  False,
                                proxy_100 = False,
                                override =  False)
        # sequencer.rebuild_proxy()
        return {"FINISHED"}


class VSEQFSetting(bpy.types.PropertyGroup):
    proxy_on_import = bpy.props.BoolProperty(
    name = "Set and build videos strips as proxies when importing local footage",
    default = True)
    proxy_25 = bpy.props.BoolProperty(
    name = "Proxy at 25%",
    default = True)
    proxy_50 = bpy.props.BoolProperty(
    name = "Proxy at 50%",
    default = False)
    proxy_75 = bpy.props.BoolProperty(
    name = "Proxy at 75%",
    default = False)
    proxy_100 = bpy.props.BoolProperty(
    name = "Proxy at 100%",
    default = False)
    proxy_quality = bpy.props.IntProperty(
    name = "Proxy JPG quality",
    default = 90,
    min = 1,
    max = 100)


# Panel for proxy options management
# def proxy_menu(self, context):
#     # prefs = context.user_preferences.addons[__name__].preferences
#     gdquest_vse_proxy = context.scene.gdquest_vse_proxy
#     layout = self.layout
#
#     # if prefs.enable_auto_proxies:
#     row = layout.row()
#     row.separator()
#     row = layout.row()
#     row.prop(gdquest_vse_proxy, 'proxy_on_import')
#
#     row = layout.row(align=True)
#     row.prop(gdquest_vse_proxy, "proxy_25", toggle=True)
#     row.prop(gdquest_vse_proxy, "proxy_50", toggle=True)
#     row.prop(gdquest_vse_proxy, "proxy_75", toggle=True)
#     row.prop(gdquest_vse_proxy, "proxy_100", toggle=True)
#
#     row = layout.row()
#     row.prop(gdquest_vse_proxy, "proxy_quality")
