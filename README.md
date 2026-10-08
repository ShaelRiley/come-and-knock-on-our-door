# Come and Knock on Our Door: WIP source bank revision 3

Corrected public edition, revision2: revision1 removed two unused administrative inputs and updated their dependency metadata. This revision corrects the public description of that completed work; component inputs and outputs are unchanged. See `late/CORRECTION-REVISION1.json` and `late/CORRECTION-REVISION2.json`.
This is an editable development source checkpoint, not a new playable release.
The last tested player release remains the five-puzzle checkpoint at commit
`ab65f4a6f3aea28ba849a0a99074a989cdeef458`, tag
`v0.5.0-checkpoint-20261006-r2`.

This edition preserves that tested source and the earlier revision-2 WIP
components. It adds accepted inactive P09 foundation/geometry and isolated
P10–P14 reference/domain/scene components, including P12 original Audience
reply audio and the P14 R1 case-preserving font, date and credits exporter.
Separately accepted components preserve the stateless SceneRenderer991
extraction and P08 evening ACK kernel; these are not newly composed together.
The complete game, later production hosts, E03 actor presentation and native
integration remain unfinished. No new playable release is supplied.

## Reconstruct editable components

Read [the later-source guide](late/README.md) for exact scope and commands.
Each selected component is materialized into a new writable directory from
hash-checked ordinary files and shared dependencies. For example:

```sh
python3 progress/verify_source.py
python3 late/reproduce.py p14-domain --out /absolute/new/p14-domain
python3 late/reproduce.py p14-scene --out /absolute/new/p14-scene
```

The unchanged root `reproduce.py` reconstructs the tested five-puzzle baseline.
The earlier `progress/reproduce.py` commands remain available for revision-2
components. Read [the baseline guide](progress/docs/BASELINE-README.md) and
[earlier WIP status](progress/docs/STATUS.md) for those components' boundaries.

## Source edition and rights

This is a separately audited public source edition, not a byte-identical copy
of the reviewed working archives. Its dependency changes and exact byte
comparisons are recorded in `late/manifests/COMPONENTS.json` and
`late/VALIDATION.json`. Administrative archives and correspondence are excluded;
necessary technical fixtures and input guards are retained. Generated build
fixtures used by a later component are retained when required and deduplicated.

All existing `LICENSE.md`, `THIRD-PARTY.md`, `CREDITS-AND-RIGHTS.txt`, compiler
notices and source-fixture attribution remain. There is no new blanket game
license. The pinned compiler and its already-audited 198-file corresponding
source closure are reused; compiler bootstrapping was not repeated for this
bank. Broad vendor/GUI trees, proprietary Prof-UIS and Sierra game data are
not added. See [later-source provenance](late/PROVENANCE.md).
