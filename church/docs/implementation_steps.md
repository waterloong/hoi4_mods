# Restoring the earlier mod

Each step receives its own commit. Perform combined in-game verification at the end.

1. Christianity ideology, three subtypes, icon, localisation and original political rules.
2. Missionary trait and generated advisers using a unique history filename.
3. Spread the Gospel decision.
4. Optional debug civil-war decisions, restricted to debug mode.
5. China leaders and a controlled way to choose a Christian government.
6. Christian flags with correct ideology suffixes.
7. Church bonuses, after choosing balance values.

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

No country starts Christian automatically in step 1, and churches still provide
no bonuses. Advisers, decisions, China history and flags are later steps.
