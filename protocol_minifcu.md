# Protocol Notes

## Receive

| Code             | Description                          |
|------------------|--------------------------------------|
| 14, 13           | right-left speed                     |
| 11, 12           | push-pull speed                      |
| 1, 2, 3, 4       | left-right push-pull heading         |
| 53               | localizer                            |
| 57               | heading-track                        |
| 50; 51; 52       | autopilot 1, autopilot 2, autothrust |
| 59, 60           | altitude change (100 in 1000 steps)  |
| 15, 16, 17, 18   | push-pull left-right altitude        |
| 58               | metric altitude                      |
| 19, 20, 21, 22   | vertical speed push-pull left-right  |
| 55               | approach mode                        |
| 56               | speed match                          |

## Send

| Code  | Description             |
|-------|-------------------------|
| C     | start receiving data    |
| A5000 | set altitude to 5000 ft |
| V600  | set vspd to 600 ft/min  |
| H43   | set heading to 43       |
| S105  | set speed to 105 knots  |
