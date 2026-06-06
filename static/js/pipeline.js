const foldersForm = document.querySelector("[data-folders-form]");
const folderList = document.querySelector("[data-folder-list]");
const addPathButton = document.querySelector("[data-add-path]");
const folderRowTemplate = document.querySelector("#folder-row-template");

function refreshFolderIds() {
  const inputs = folderList.querySelectorAll("input[name='folders']");

  inputs.forEach((input, index) => {
    const id = `folder-${index + 1}`;
    input.id = id;
  });
}

function addFolderRow() {
  const row = folderRowTemplate.content.firstElementChild.cloneNode(true);

  folderList.append(row);
  refreshFolderIds();
  row.querySelector("input").focus();
}

function getFoldersFromInputs() {
  const inputs = folderList.querySelectorAll("input[name='folders']");

  return Array.from(inputs)
    .map((input) => input.value.trim())
    .filter((folder) => folder.length > 0);
}

async function sendFolders(folders) {
  const response = await fetch("/sending_paths", {  
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      folders: folders,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    console.error("Ошибка backend:", error);
    return;
  }

  const data = await response.json();
  console.log("Ответ backend:", data);
}

addPathButton.addEventListener("click", addFolderRow);

folderList.addEventListener("click", (event) => {
  const removeButton = event.target.closest("[data-remove-path]");

  if (!removeButton) {
    return;
  }

  removeButton.closest(".folder-row").remove();
  refreshFolderIds();
});

foldersForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const folders = getFoldersFromInputs();

  if (folders.length === 0) {
    console.warn("Не указано ни одной папки");
    return;
  }

  await sendFolders(folders);
});