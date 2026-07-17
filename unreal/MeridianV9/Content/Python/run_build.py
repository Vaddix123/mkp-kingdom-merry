# Explicit headless entry point. Unambiguous regardless of __name__.
# Invoked via: UnrealEditor-Cmd.exe <project> -run=pythonscript -script=run_build.py
import unreal
try:
    import meridian_build
    meridian_build.build_all()
    unreal.log("run_build: build_all() returned normally.")
except Exception as e:
    unreal.log_error("run_build: build failed: {}".format(e))
    import traceback
    unreal.log_error(traceback.format_exc())
