```dataviewjs
const container = this.container;

const allPages = dv.pages('"1. Inbox/3. Literature Notes/Films & Serials"')
  .where(p => p["Жанр"] && p["Рейтинг"])
  .sort(p => -Number(p["Рейтинг"] || 0));

// --- UI блок: Фильтр + Поиск ---
const controls = document.createElement("div");
controls.style.display = "flex";
controls.style.gap = "1rem";
controls.style.marginBottom = "1rem";

// Фильтр по жанрам
const genres = [...new Set(
  allPages.flatMap(p => Array.isArray(p["Жанр"]) ? p["Жанр"] : [p["Жанр"]])
)];

const genreSelect = document.createElement("select");

const allOption = document.createElement("option");
allOption.value = "all";
allOption.textContent = "Все жанры";
genreSelect.appendChild(allOption);

for (let genre of genres.sort()) {
  const option = document.createElement("option");
  option.value = genre;
  option.textContent = genre;
  genreSelect.appendChild(option);
}

controls.appendChild(genreSelect);

// Поиск
const searchInput = document.createElement("input");
searchInput.type = "text";
searchInput.placeholder = "Поиск по названию...";
searchInput.style.flex = "1";
controls.appendChild(searchInput);

container.appendChild(controls);

// --- Таблица ---
const table = document.createElement("table");
table.className = "dataview table-view-table";

const header = table.insertRow();
["Обложка", "Название", "Жанр", "Рейтинг", "Инсайт"].forEach(text => {
  const th = document.createElement("th");
  th.textContent = text;
  header.appendChild(th);
});

function renderTable(filterGenre = "all", searchTerm = "") {
  table.querySelectorAll("tr:not(:first-child)").forEach(row => row.remove());

  const filteredPages = allPages.filter(p => {
    const genreMatch =
      filterGenre === "all" ||
      (Array.isArray(p["Жанр"])
        ? p["Жанр"].includes(filterGenre)
        : p["Жанр"] === filterGenre);

    const searchMatch =
      !searchTerm ||
      (p.file?.name?.toLowerCase().includes(searchTerm.toLowerCase()));

    return genreMatch && searchMatch;
  });

  for (let p of filteredPages) {
    const row = table.insertRow();

    // Обложка
    const cellCover = row.insertCell();
    cellCover.innerHTML = p["Постер"]
      ? `<img src="${p["Постер"]}" width="100" style="border-radius: 8px;">`
      : "—";

    // Название
    const cellTitle = row.insertCell();
    const link = document.createElement("a");
    link.href = p.file.path;
    link.textContent = p.file.name;
    link.className = "internal-link";
    cellTitle.appendChild(link);

    // Жанр
    const cellGenre = row.insertCell();
    const genreVal = p["Жанр"];
    cellGenre.textContent = Array.isArray(genreVal)
      ? genreVal.join(", ")
      : (genreVal || "—");

    // Рейтинг
    const cellRating = row.insertCell();
    cellRating.textContent =
      p["Рейтинг"] !== undefined && p["Рейтинг"] !== null
        ? `${p["Рейтинг"]}/10`
        : "—";

    // Инсайт
    const cellInsight = row.insertCell();
    cellInsight.textContent = p["Инсайт"] || "–";
  }
}

// --- Слушатели ---
genreSelect.onchange = () => renderTable(genreSelect.value, searchInput.value);
searchInput.oninput = () => renderTable(genreSelect.value, searchInput.value);

// Первый рендер
renderTable();
container.appendChild(table);


```


# Список фильмов, которые хочу посмотреть:
```dataview
list
from ""
where
(
  contains(file.outlinks, [[MOC - Film Library]])
  or contains(Links, "[[MOC - Film Library]]")
)
and
(
  (Статус = false)
  or (status = false)
  or (watched = false)
)
sort file.ctime desc

```
