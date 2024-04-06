### Board Dimensions, Walls, and Checkpoints
```
B{ncols}x{nrows}
W wstr|wstr|wstr...
C cstr|cstr|cstr...
```
where each `wstr` places walls and each `cstr` places checkpoints as follows:
* `:` to fill the entire row
* `n` to fill column n
* `m:n` to fill columns m through n
* `segment,segment...` where each `segment` matches one of the previous two patterns

*`ncols` should divide 160, `nrows` should divide 144, and their aspect ratio should equal that of the CIT display*

### Entities
Each line corresponds to one entity with the format `{name} {behavior} {args}`. Specifically, it should match one of the following:
* `P MANUAL ({r}, {c})` to initialize the player at row `r` and column `c`.
* `E CIRCLE V{m} ({h}, {k}) R{r} A{a}` to initialize an enemy traveling in a circle of radius `r` centered at `(h, k)`, starting at angle `a`, and with speed multiplier `m`.
* `E NODE V{m} [(r1, c1), (r2, c2), ...]` to initialize an enemy traveling with speed multiplier `m` between the nodes listed. A list of length 1 will specify a stationary enemy.

*Note that all rows and columns in level files are 1-indexed and inclusive of both endpoints. Spacing inside node lists is flexible as they are parsed using the Python interpreter.*