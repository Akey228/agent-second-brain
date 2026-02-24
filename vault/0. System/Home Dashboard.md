---
banner: "https://abrakadabra.fun/uploads/posts/2022-03/1647485799_2-abrakadabra-fun-p-marmok-shapka-2.jpg"
banner_y: 0.528
notetoolbar: none
dg-publish:
---
- **[[1. Inbox/6. Areas 1/Goals/Q1 2026]]**
- **[[Q2 2026]]**
- **[[Q3 2026]]**
- **[[Q4 2026]]**
- **[[1. Inbox/6. Areas 1/Goals/Фундаментальный 2026 YEAR]]**
- **[[1. Inbox/6. Areas 1/Goals/2025/LIFE]]**
- - - 
# 0️⃣Action

> [!Action]
> ```dataview
> list from ""
> where contains(file.tags, "action")
> sort file.mtime desc
> ```
# 1️⃣Projects
> [!multi-column]
>
> > [!note]+ Social media
> > - [[1. Inbox/7. Resources 1/MOC - YouTube]]
> > - [[1. Inbox/7. Resources 1/MOC - Telegram]]
>
> > [!info]+ Products
> > - [[MOC - Курсик про клиентов]]
>
>
---
# 2️⃣ Areas
> [!multi-column]
>
> > [!info]+ Lifestyle
> > - [[1. Inbox/6. Areas 1/MOC - Personal]]
> > - [[1. Inbox/6. Areas 1/MOC - Productivity]]
> > - [[1. Inbox/6. Areas 1/MOC - Habits]]
> > - [[1. Inbox/6. Areas 1/MOC - Future & Dreams]]
> > - [[1. Inbox/6. Areas 1/MOC - Travel]]
> > - [[1. Inbox/6. Areas 1/MOC - Learning]]
> > - [[1. Inbox/6. Areas 1/MOC - Thinking]]
> > - [[1. Inbox/6. Areas 1/MOC - Psychology]]
>
>>[!info]+ Health
>> - [[1. Inbox/6. Areas 1/Health/MOC - Nutrition]]
>> - [[1. Inbox/6. Areas 1/Health/MOC - Training]]
>> - [[1. Inbox/6. Areas 1/Health/MOC - Sleep]]
>> - [[1. Inbox/7. Resources 1/MOC - Anatomia]]
>
> > [!info]+ Vault
> > - [[1. Inbox/6. Areas 1/MOC - Film Library]]
> > - [[1. Inbox/6. Areas 1/MOC - Book Library]]
> > - [[1. Inbox/6. Areas 1/MOC - Passwords]]
---
# 3️⃣ Resources
> [!multi-column]
> 
>> [!info]+ Hard Editing
> > - [[1. Inbox/7. Resources 1/Editing/MOC - After Effects]]
> > - [[1. Inbox/7. Resources 1/Editing/MOC - Premiere Pro]]
> > - [[1. Inbox/7. Resources 1/Editing/MOC - Sound Design]]
> > - [[1. Inbox/7. Resources 1/Editing/MOC - VFX]]
> > - [[1. Inbox/7. Resources 1/Editing/MOC - Editing Fundamentals]]
> > - [[1. Inbox/7. Resources 1/Editing/MOC - Narrative Flow]]
> 
> > [!info]+ Soft Editing
> > - [[1. Inbox/7. Resources 1/MOC - Portfolio]]
> > - [[1. Inbox/7. Resources 1/MOC - Clients]]
> > - [[1. Inbox/7. Resources 1/MOC - Personal Brand]]
>
> > [!info]+ Other
> > - [[1. Inbox/7. Resources 1/MOC - Съёмка]]
> > - [[1. Inbox/7. Resources 1/MOC - Obsidian]]
> > - [[1. Inbox/7. Resources 1/MOC - n8n Assistant]]
> > - [[1. Inbox/7. Resources 1/MOC - Marketing]]
> > - [[1. Inbox/7. Resources 1/MOC - Neural Networks]]
> > - [[1. Inbox/7. Resources 1/MOC - Thumbnails]]
>

---
# 4️⃣ System
> [!multi-column]
>
> > [!info] Recently Created
> > ```dataview
> > list from ""
> > sort file.ctime desc
> > limit 5
> > ```
> 
> > [!info] Recently Modified
> > ```dataview
> > list from ""
> > sort file.mtime desc
> > limit 5
> > ```

```dataviewjs
try {
  const files = dv.pages("").values;
  if (!files || files.length === 0) {
    dv.paragraph("No notes found.");
  } else {
    const oldestFile = files.slice().sort((a,b) => a.file.ctime - b.file.ctime)[0];
    const daysSinceStart = Math.floor((Date.now() - oldestFile.file.ctime) / (1000 * 60 * 60 * 24));
    const totalNotes = files.length;
    const allTags = files.flatMap(p => (p.file.tags ?? []));
    const totalTags = [...new Set(allTags)].length;

    dv.paragraph(`<div style="
      background-color: var(--background-secondary);
      border: 1px solid var(--background-modifier-border);
      border-radius: 10px;
      padding: 20px;
      text-align: center;
      font-family: var(--font-text);
      color: var(--text-normal);
    ">
      <h2 style="margin:0 0 8px 0;">📊 Obsidian Stats</h2>
      <p style="margin:6px 0;">🗓️ <strong>${daysSinceStart}</strong> дней с начала работы</p>
      <p style="margin:6px 0;">📝 <strong>${totalNotes}</strong> заметок</p>
      <p style="margin:6px 0;">🏷️ <strong>${totalTags}</strong> уникальных тегов</p>
    </div>`);
  }
} catch (e) {
  dv.paragraph("DataviewJS error: " + e.message);
}
```
