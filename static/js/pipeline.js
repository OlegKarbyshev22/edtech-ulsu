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

addPathButton.addEventListener("click", addFolderRow);

folderList.addEventListener("click", (event) => {
  const removeButton = event.target.closest("[data-remove-path]");

  if (!removeButton) {
    return;
  }

  removeButton.closest(".folder-row").remove();
  refreshFolderIds();
});
