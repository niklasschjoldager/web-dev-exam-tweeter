const DROPDOWN_IDENTIFIER = "data-dropdown"
const MODAL_IDENTIFIER = "data-modal"

document.addEventListener("click", handleClick)

function handleClick(event) {
  const target = event.target

  console.log(target)

  if (target.hasAttribute("data-dropdown") || target.closest("[data-dropdown]")) {
    const dropdown = target.closest("[data-dropdown]")
    console.log("Dropdown")
    event.preventDefault()
    closeAllDropdowns(DROPDOWN_IDENTIFIER)
    openDropdown(dropdown)
  }
}

function closeAllDropdowns(dropdownIdentifier) {
  document.querySelectorAll(dropdownIdentifier).forEach((dropdown) => dropdown.classList.add("is-hidden"))
}

function openDropdown(dropdown) {
  dropdown.nextElementSibling.classList.remove("is-hidden")
}
