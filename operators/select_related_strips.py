import bpy
from operator import attrgetter

class SelectRelatedStrips(bpy.types.Operator):
    """
    Find and select effects related to the selection,
    but also inputs of selected effects. This helps to then copy
    or duplicate strips with all attached effects.
    """
    bl_idname = 'power_sequencer.select_related_strips'
    bl_label = 'Select Related Strips'
    bl_description = "Find and select all strips related to the selection"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.selected_sequences) > 0

    def execute(self, context):
        related_strips = set()
        for s in context.selected_sequences:
            self.dfs(related_strips, s, context)
            
        for s in related_strips:
            s.select = True
        
        return {'FINISHED'}
    
    def dfs(self, visited, strip, context):
        """
        Performs a depth first search traversal to the graph of strips, to find
        all related strips.
        Args:
        - visited: A set with all the strips that have been visited.
        - strip: The strip to start the search from.
        """
        visited.add(strip)
        neighbours = self.find_neighbours(strip, context)
        for s in neighbours:
            if s not in visited:
                self.dfs(visited, s, context)
    
    def find_neighbours(self, strip, context):
        """
        Strips and their effect strips define a graph, where each node is a 
        strip and edges are their connections. It finds all the neighbours of a 
        strip in the graph, and *sometimes neighbours of neighbours and so on*.
        *In order to find the neighbours of a strip the 
        bpy.ops.transform.seq_slide operator is used, and usually finds many
        levels of neighbours, but always finds the first level, which is needed,
        the other levels are redundant, but are included for brevity reasons. 
        Args:
        - strip: The strip to find all its neighbours.
        Returns: A list with all the neighbours of the strip and sometimes 
                 neighbours of neighbours and so on.
        """
        #Respects initial selection
        init_selected_strips = [s for s in context.selected_sequences]
        
        neighbours = []
        bpy.ops.sequencer.select_all(action='DESELECT')
        strip.select = True
        bpy.ops.transform.seq_slide(value=(0, 0))
        strip.select = False
        for s in context.selected_sequences:
            neighbours.append(s)
                
        try:
            neighbours.append(strip.input_1)
            neighbours.append(strip.input_2)
        except Exception:
            pass
        
        bpy.ops.sequencer.select_all(action='DESELECT')
        for s in init_selected_strips:
            s.select = True
            
        return neighbours
