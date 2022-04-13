const DROPDOWN = "[data-dropdown]"
const DROPDOWN_BUTTON = "[data-dropdown-button]"
const DROPDOWN_CONTAINER = "[data-dropdown-container]"
const DROPDOWN_DISMISS = "[data-dropdown-dismiss]"

let currentDropdownButton = null
let isDropdownOpen = false

document.addEventListener("click", handleClick)

function handleClick(event) {
  const target = event.target
  const isClickOnDropdownButton = target.matches(DROPDOWN_BUTTON) || target.closest(DROPDOWN_BUTTON)
  const isClickInsideDropdown = target.closest(DROPDOWN_CONTAINER)
  const isClickOnDismissButton = target.closest(DROPDOWN_DISMISS)

  if (
    (isDropdownOpen && !isClickInsideDropdown) ||
    (isDropdownOpen && isClickOnDismissButton) ||
    (currentDropdownButton !== null && currentDropdownButton == isClickOnDropdownButton)
  ) {
    isDropdownOpen = false
    currentDropdownButton = null
    closeAllDropdowns(DROPDOWN)
    return
  }

  if (isClickOnDropdownButton) {
    event.preventDefault()
    const dropdown = target.closest(DROPDOWN_CONTAINER).querySelector(DROPDOWN)
    isDropdownOpen = true
    currentDropdownButton = isClickOnDropdownButton
    closeAllDropdowns(DROPDOWN)
    openDropdown(dropdown)
  }
}

function closeAllDropdowns(dropdownIdentifier) {
  document.querySelectorAll(dropdownIdentifier).forEach((dropdown) => dropdown.classList.add("is-hidden"))
}

function openDropdown(dropdown) {
  dropdown.classList.remove("is-hidden")
}
