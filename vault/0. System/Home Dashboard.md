---
banner: "https://abrakadabra.fun/uploads/posts/2022-03/1647485799_2-abrakadabra-fun-p-marmok-shapka-2.jpg"
banner_y: 0.528
notetoolbar: none
dg-publish:
---
- **[[Q1 2026]]**
- **[[Q2 2026]]**
- **[[Q3 2026]]**
- **[[Q4 2026]]**
- **[[Фундаментальный 2026 YEAR]]**
- **[[LIFE]]**
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
> > - [[MOC - YouTube]]
> > - [[MOC - Telegram]]
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
> > - [[MOC - Personal]]
> > - [[MOC - Productivity]]
> > - [[MOC - Habits]]
> > - [[MOC - Future & Dreams]]
> > - [[MOC - Travel]]
> > - [[MOC - Learning]]
> > - [[MOC - Thinking]]
> > - [[MOC - Psychology]]
>
>>[!info]+ Health
>> - [[MOC - Nutrition]]
>> - [[MOC - Training]]
>> - [[MOC - Sleep]]
>> - [[MOC - Anatomia]]
>
> > [!info]+ Vault
> > - [[MOC - Film Library]]
> > - [[MOC - Book Library]]
> > - [[MOC - Passwords]]
---
# 3️⃣ Resources
> [!multi-column]
> 
>> [!info]+ Hard Editing
> > - [[MOC - After Effects]]
> > - [[MOC - Premiere Pro]]
> > - [[MOC - Sound Design]]
> > - [[MOC - VFX]]
> > - [[MOC - Editing Fundamentals]]
> > - [[MOC - Narrative Flow]]
> 
> > [!info]+ Soft Editing
> > - [[MOC - Portfolio]]
> > - [[MOC - Clients]]
> > - [[MOC - Personal Brand]]
>
> > [!info]+ Other
> > - [[MOC - Съёмка]]
> > - [[MOC - Obsidian]]
> > - [[MOC - n8n Assistant]]
> > - [[MOC - Marketing]]
> > - [[MOC - Neural Networks]]
> > - [[MOC - Thumbnails]]
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
