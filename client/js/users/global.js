export function toggleButtons(id, showSelector, hideSelector) {
  const showButtons = document.querySelectorAll(`${showSelector}[data-id="${id}"]`)
  const hideButtons = document.querySelectorAll(`${hideSelector}[data-id="${id}"]`)
  showButtons.forEach((button) => button.classList.remove("is-hidden"))
  hideButtons.forEach((button) => button.classList.add("is-hidden"))
}
