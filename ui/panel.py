import bpy


class Panel(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Tools"
    bl_label = "Power Sequencer"
    bl_idname = "power_sequencer.panel"
    # bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return context.space_data.view_type == 'SEQUENCER'

    def draw(self, context):
        scene = context.scene
        active_tab = scene.power_sequencer_active_tab
        categories = {"Sequencer" : "SEQ_SEQUENCER",
                      "Render" : "RENDER_ANIMATION",
                      "Modifier" : "MODIFIER", 
                      "Sound" : "SOUND",
                     }
        remaining_space = 1.0
        space_per_button = 1.0 / len(categories.keys())
        
        layout = self.layout
        box = layout.box()
        split = box.row()
        
        split = split.split(0.0, align=True)
        for i in range(len(categories.keys())):
            category = list(categories.keys())[i]
            icon = categories[category]
            
            used_space = space_per_button * (i + 1)
            percent = space_per_button / remaining_space
            
            split = split.split(percentage=percent, align=True)
            remaining_space = 1.0 - used_space
            
            split.operator(
                "power_sequencer.change_panel_tab", 
                text="", 
                icon=icon,
                emboss=active_tab != category).active_tab = category
        
        if scene.power_sequencer_active_tab == "Sequencer":
            row = box.row()
            row.operator('power_sequencer.ripple_delete', 
                icon='AUTOMERGE_ON')
        
        elif scene.power_sequencer_active_tab == "Render":
            row = box.row()
            row.label("Render Functions Here")
        
        elif scene.power_sequencer_active_tab == "Modifier":
            row = box.row()
            row.operator('power_sequencer.add_crossfade', 
                icon="IMAGE_ALPHA")
            
        elif scene.power_sequencer_active_tab == "Sound":
            row = box.row()
            row.label("Sound Functions Here")
