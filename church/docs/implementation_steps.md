# Restoring the earlier mod

Each step receives its own commit. Perform combined in-game verification at the end.

1. Christianity ideology, three subtypes, icon, localisation and original political rules.
2. Missionary trait and generated advisers using a unique history filename.
3. Spread the Gospel decision.
4. Optional debug civil-war decisions, restricted to debug mode.
5. China leaders and a controlled way to choose a Christian government.
6. Christian flags with correct ideology suffixes.
7. Church bonuses: +0.01 daily political power and +0.01 Christian drift each.

## Step 1: ideology

Restores the old local ideology definition, including its gold color,
diplomatic permissions and bonuses. Christianity is a political ideology group;
Catholicism, Protestantism and Orthodoxy are leader subtypes, not demographic data.
Subtypes do not have separate popularity percentages.

Start a fresh non-Ironman game after restarting HOI4. In the console:

```
add_party_popularity christianity 10
```

Check the political party breakdown for Christian support, name and icon.
For an optional government check in a disposable save:

```
set_ruling_party christianity
```

Check the government description and diplomacy rules. No historical leader is
assigned yet. Do not use this test save to evaluate later China history changes.
Check `logs/error.log` for references to `church_ideologies`, `christianity`
or `church_ideology.gfx`. In-game validation is still pending.

No country starts Christian automatically. All seven implementation steps are
now present. The checks below cover the combined build.

## Combined in-game verification

1. Start a fresh non-Ironman game as China after fully restarting HOI4.
2. Confirm all five ideology groups are present and the Christian icon fits.
3. Check that a Missionary adviser is offered for 150 political power. Hire one
   and check for +0.1 daily Christian support. Existing vanilla advisers should remain.
4. Use `pp 1000` for test funds. Take Spread the Gospel while at peace; verify
   support increases by 10 percentage points and the 90-day cooldown applies.
5. Raise Christian support above 50 percent. Test the Catholic China choice in
   one save and the Protestant Chiang choice in a separate fresh save. Verify
   the selected leader, subtype, ruling party, and exclusion of the other path.
6. Check the Christian government's flag at country, map and small UI sizes.
   Flags reuse democratic artwork as in the earlier mod, not new cross designs.
7. Construct a church, check the model, province cap, and national modifiers.
   Political power remains conservative; Christian support per church is
   now ten times the initial province-building value.
8. Confirm debug civil-war decisions are hidden in normal mode. In debug mode,
   test one in a disposable save. They cost 1 PP, trigger 80 percent uprisings,
   require a target without an existing civil war, and cannot be used by the AI.
9. Check game error logs after loading and after exercising the features.

AI selection of missionary advisers and these political decisions is disabled
for the first balance pass. China retains vanilla startup history and portraits;
Chiang is reused rather than duplicated. Paul uses the game's generic portrait
fallback because no dedicated portrait was supplied. Decisions to choose a new
government require peace, so China may need a separate peaceful test save.
## Log-based verification fixes

The first combined load reported a direct building modifier rejection for
`christianity_drift`, a warning about recruiting Paul from a decision, and a
map row error at EOF. Building influence now uses a registered country modifier
and a daily refreshed dynamic modifier. Paul is recruited at startup and only
promoted by the Catholic decision. The map exporter no longer adds a final
empty row. These changes still require a fresh game load to confirm resolution.
