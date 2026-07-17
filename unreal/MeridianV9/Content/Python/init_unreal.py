# Meridian v9 - auto-build hook.
# Runs on every editor launch (PythonScriptPlugin executes init_unreal.py).
# Builds the facility level once; skips if it already exists.
import os
import unreal

LEVEL_ASSET = "/Game/Meridian/MeridianFacility"

def _kickoff():
    try:
        if os.environ.get("MERIDIAN_SKIP_AUTOBUILD"):
            unreal.log("Meridian: MERIDIAN_SKIP_AUTOBUILD set - startup hook standing down "
                       "(explicit build run will drive it).")
            return
        if unreal.EditorAssetLibrary.does_asset_exist(LEVEL_ASSET):
            unreal.log("Meridian: facility level already built - skipping auto-build.")
            return
        unreal.log("Meridian: first launch detected - building the v9 facility now...")
        import meridian_build
        meridian_build.build_all()
    except Exception as e:
        unreal.log_error("Meridian auto-build failed: {}".format(e))
        unreal.log_error("Run manually: Tools > Execute Python Script > meridian_build.py")

_kickoff()
