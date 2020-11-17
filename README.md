# ScriptGame

this is a common image identification project



rules：

| file name pattern  | rule                                                 |
| ------------------ | ---------------------------------------------------- |
| exit.(mode)        | switch to (mode) after this mode quit                |
| limit.(number)     | quit after click (number) pic with end               |
| duplicate.(number) | quit after click same pic (number) times             |
| *.d                | exclude from scan                                    |
| *ignore\*          | exclude from duplicate check                         |
| *@(mode).png       | switch to (mode) when hit this pic                   |
| *[(x),(y)]\*       | click position move(x),(y)                           |
| *{(file)}\*        | click (file) before this click                       |
| *{(file)}}\*       | click (file) before this click and cancel this click |
| *end\*             | count +1                                             |
| *start\*           | sleep for 3~5s                                       |
| *wait\*            | sleep for 20~30s                                     |

