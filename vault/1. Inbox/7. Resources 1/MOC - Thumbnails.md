![[Pasted image 20260108134622.png]]
![[Pasted image 20260108134627.png]]
![[Pasted image 20260108134653.png]]
![[Pasted image 20260108135214.png]]
![[Screenshot 2025-12-28 131314.png]]
# Actions
```dataview
list
from [[MOC - Thumbnails]]
where contains(file.tags, "action")
sort file.ctime desc
```
# Ideas
```dataview
list
from [[MOC - Thumbnails]]
where contains(file.tags, "idea")
sort file.ctime desc
```
# Info
```dataview
list
from [[MOC - Thumbnails]]
where contains(file.tags, "info")
sort file.ctime desc
```

#### Linked References to MOC - Thumbnails
```dataview
list from [[MOC - Thumbnails]]
```