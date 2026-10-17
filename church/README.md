# Church

A Hearts of Iron IV mod targeting the locally installed 1.19.3 version.

Christianity is also available as a political ideology, with Catholic,
Protestant and Orthodox leader subtypes. No country is converted at startup.
See [implementation steps](docs/implementation_steps.md) for the test procedure
and the sequence for restoring the earlier mod's features.

## Prototype

- Adds `church` as a province building, limited to one per province.
- Does not consume shared state building slots. Construction uses civilian factories as usual.
- Costs 1,000 construction points, affected by infrastructure construction speed.
- Provides no gameplay bonuses and requires no technology or DLC.
- Uses a custom church construction icon (frame 32), a province detail icon,
  and a custom low-poly stone church model with a bell tower and cross.
- Adds no starting churches and does not replace vanilla building definitions.

## Install

Copy `church.mod` into your HOI4 user data folder's `mod` directory (normally
`Documents/Paradox Interactive/Hearts of Iron IV/mod`). Leave the project here:
the launcher file points to this directory. If you move the project, update
the `path` in `church.mod`.

The machine-specific `church.mod` is excluded from Git. For a fresh clone,
copy `descriptor.mod` to `church.mod`, append `path="C:/path/to/your/checkout"`,
and place that launcher file in the HOI4 user data `mod` folder.

Enable **Church** in a launcher playset and start a new game.

## In-game verification still required

1. Fully restart HOI4. Open Construction and find the church icon under province buildings.
2. Queue a church in an owned, controlled land province and let it finish.
3. Confirm that a second church cannot be queued in that province and that another province can have its own church.
4. Zoom in and check that the church model appears after construction.
5. Check the HOI4 `logs/error.log` for errors mentioning `church` or `church_mesh`.

The user confirmed the construction button appeared in the first prototype.
The new graphics have not yet been verified in-game. An independent PDX mesh
reader successfully parsed the exported vertices, normals and triangle indices.

## Graphics source and compatibility

The active icon is the user's `art/church_user_icon.png`, imported from the
existing Church mod's `gfx/interface/buildings/cathedral.png`. It replaces
the initial generated illustration in both construction and province icons.
The original artwork is preserved; only game-size resampling is applied.

`art/church_source.png` was generated with the built-in ImageGen tool using:
"A single centered small European stone church with a square bell tower,
pitched roof and simple cross, isometric three-quarter view. Muted warm gray
stone, charcoal roof, parchment highlights, crisp readable silhouette,
illustrated strategy-game building icon. Transparent background, no scenery,
text, border or watermark. Entire building visible, readable at 46 by 46 pixels."

`art/church.obj` is an editable version of the custom mesh. The map model is a
separate simplified 3D asset, not the generated image. Preview it using
`tools/preview_model.py`. Rebuild graphics with Pillow and
`tools/build_assets.py --game "PATH TO Hearts of Iron IV"`.

The icon strip preserves all 31 vanilla frames and appends Church as frame 32.
This overrides `GFX_buildings_strip` and may conflict with other building-icon mods.
`map/buildings.txt` preserves the installed game's entries and adds 10,154 church
anchors at existing fort positions; churches and forts can visually overlap.
This map file can conflict with map mods and should be regenerated after a game
update that changes building placement. No starting churches are added.
