
# Actions
```dataview
list
from [[{{title}}]]
where contains(file.tags, "action")
sort file.ctime desc
```
# Ideas
```dataview
list
from [[{{title}}]]
where contains(file.tags, "idea")
sort file.ctime desc
```
# Info
```dataview
list
from [[{{title}}]]
where contains(file.tags, "info")
sort file.ctime desc
```

#### Linked References to {{title}}
```dataview
list from [[{{title}}]]
```