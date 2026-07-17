# Meridian v9 — Unreal Engine Build

Self-constructing UE project for the Meridian Data Infrastructure v9 facility.
Original concept: **Brandon (Vaddix123)**.

## What this is

`MeridianV9/` is a complete Unreal Engine project. On **first launch** a Python
editor script (`Content/Python/meridian_build.py`, auto-run by `init_unreal.py`)
constructs the entire v9 facility as a saved level:

- 115 MW SOFC array (3×3 Bloom-class modules, exhaust manifold, transformer skid)
- Back-pressure steam turbine hall + tiered cooling tower
- Carbon-capture plant: absorber + stripper columns, reboiler kettle,
  4-stage compression hall, amine tank, CO2 export pipeline
- BESS row (4× Megapack + inverters + status LEDs)
- Heat-offtake greenhouses (translucent glass, grow-light interiors)
- 100 MW data center with glowing server-window band
- MD water plant + 3 domed storage tanks + constructed wetland
- LFG flare (emissive flame + orange point light) + wellheads + landfill hill
- Substation, export tie, 11 color-coded process pipe runs
- Lumen lighting rig: sun + sky atmosphere + height fog + skylight +
  post-process (bloom, exposure clamp) + overview camera

Every coordinate mirrors the web model (`../index.html`) 1:1.

## How to run it

1. **Install Unreal Engine** (one-time, ~40 GB): open the **Epic Games
   Launcher** (already installed) → sign in → *Unreal Engine* tab → *Library* →
   **Install 5.0** (or any 5.x — the project is version-tolerant; if a newer
   version asks to convert, choose "Open a copy" or "Convert in place", both work).
2. **Double-click `MeridianV9/MeridianV9.uproject`.**
3. First open compiles shaders (5–20 min one-time), then the build script runs
   automatically and saves the level. Watch progress in *Output Log* — lines
   prefixed `Meridian:`.
4. The level `/Game/Meridian/MeridianFacility` opens on startup thereafter.

Manual rebuild: delete the `/Game/Meridian` folder in the Content Browser, or run
*Tools → Execute Python Script →* `Content/Python/meridian_build.py`.

## Why UE at all

Nothing in the facility needs a physics solver — the model is process-flow, not
rigid-body dynamics. UE's value here is the **renderer**: Lumen global
illumination, real shadows, atmospheric scattering, cinematic cameras for
investor stills and flythroughs. The web build (`../index.html`) remains the
shareable pitch link; this is the cinematic tier.

## Headless build (optional, after engine install)

```
"C:\Program Files\Epic Games\UE_5.0\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" ^
  "<repo>\unreal\MeridianV9\MeridianV9.uproject" ^
  -run=pythonscript -script="<repo>\unreal\MeridianV9\Content\Python\meridian_build.py" ^
  -unattended -nopause -nosplash
```
