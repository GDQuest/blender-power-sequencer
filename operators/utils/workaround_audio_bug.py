def sequencer_workaround_2_80_audio_bug(context):
    for s in context.sequences:
        if s.lock:
            continue
        s.select = True
        bpy.ops.transform.seq_slide(value=(0, 0))
        s.select = False
        break
