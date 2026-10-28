# Blender sources for the portfolio's 3D models

Python scripts that build every model in `assets/3d/` from scratch (Blender 5.2):

| Script | Builds |
| --- | --- |
| `hero.py` | `hero.glb`: the room seen from behind: three-monitor desk by the window, 8 s loop where he swivels round to wave "hi, I'm Akhiljith!" |
| `small.py` | `badge.glb` and the six `icon-*.glb` skill icons (4 s loops) |
| `helpers.py` | Shared mesh/material helpers |
| `export.py` | `export_glb(name)`: Draco-compressed glTF export into `../assets/3d/` |

Run in Blender's Scripting tab (or over MCP), with `S` pointing at this folder:

```python
S = r"C:\path\to\portfolio\blender"
HELPERS = S + r"\helpers.py"; EXPORT = S + r"\export.py"
ONLY = None          # or e.g. ["badge", "icon-ai"]
NO_EXPORT = False
exec(open(S + r"\small.py").read())   # badge + 6 skill icons (exports each)
exec(open(S + r"\hero.py").read())    # hero room
exec(open(EXPORT).read()); export_glb("hero")
```

## Night mode hooks

`assets/main.js` drives the day/night look through material names in `hero.glb`, so keep these
names if you edit the scene:

- `Sky`, `Orb`: sky colour and sun/moon
- `Bulb`, `LampGlow`, `LampPool`, `LampPoolCore`: desk lamp (flickers on in dark mode)
- `Spill*`: screen light on the desk, floor and curtains
- `Curtain0` … `Curtain7`: curtain positions from open to closed; the page shows one at a time
- `Skin`: gets the monitor glow at night
- `Scr*`, `CityLights`, `Bubble*`: keep their colours at night
