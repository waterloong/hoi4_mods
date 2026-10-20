# ROC sandbox mod

Targets the installed HOI4 1.19 series. This preserves the newer local version
of the mod, including the intentionally large sandbox rewards and three custom
Chinese commanders. It is separate from the Church mod.

## Corrections

- Custom adviser traits load from `common/country_leader` and use ROC-prefixed IDs.
- Commander trait capitalization and duplicate offensive traits are corrected.
  The admiral no longer receives a land-only career trait.
- Only the three ROC characters are recruited, through a unique general history
  file. The mod no longer duplicates China's vanilla history or recruits its
  existing leaders a second time.
- Qingdao keeps the current game's PRC and DLC-specific SND cores, with the
  original ROC infrastructure/factory/port/fort upgrades.
- The technology grant references 552 real 1.19 technologies and 49 special
  projects. Removed doctrine technologies are no longer passed to `set_technology`.
  Current grand/subdoctrines must be selected through the current doctrine UI;
  the grant does not force several incompatible doctrine branches at once.
- Research bonus categories match the installed definitions. The scientist
  decision includes nuclear researchers and requires an existing scientist.
- All eight peace decisions target their named opponent and require an active
  war. The USA peace button no longer starts a civil war. Peace conferences are
  forced victories, not negotiated white peace, matching the original design.
- Civil wars require a valid target without an ongoing civil war or an already
  non-aligned government. Resource grants require ownership of the target state.
- Cheat decisions are hidden from AI countries and have zero AI selection weight.
  All decision names/descriptions are localised; English localisation has a BOM.
- The extraction helper reads actual installed definitions and no longer emits
  empty categories, uses an outdated technology list, or hardcodes a Steam path.

## Verification

The existing game log confirmed the old invalid `cl_tech` research category,
duplicate China leader recruitment and invalid old technology IDs. Those paths
are corrected. Installed-definition checks pass with no identifier issues:

```
python tools/audit_roc.py --game "C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV"
```

This checks syntax blocks, referenced technologies/projects/equipment/traits,
research categories, localisation, peace targets, war guards, and AI controls.
It does not prove every effect works in-game or bypass DLC entitlements.

After restarting HOI4, begin a fresh non-Ironman China game. Check the three
commanders, adviser traits, Qingdao, and decision labels. Test each reward in a
disposable save; declare a test war before using a peace tool. Confirm the right
opponent appears. Check `logs/error.log` for ROC file paths after these actions.
Existing saves can retain old recruitment, leader names and state setup.

To export updated grant snippets after a game update:

```
python extract_tech.py --game "PATH TO HOI4" --kind technologies
python extract_tech.py --game "PATH TO HOI4" --kind projects
```
