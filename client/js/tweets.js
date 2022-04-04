const DROPDOWN_BUTTON = "[data-dropdown-button]"
const DROPDOWN_CONTAINER = "[data-dropdown-container]"
const DROPDOWN = "[data-dropdown]"
const BUTTON_VALUES = ["edit", "delete", "like", "dislike", "comment", "retweet", "share"]

let isDropdownOpen = false

document.addEventListener("click", handleClick)

function handleClick(event) {
  const target = event.target
  console.log(target)

  if (isDropdownOpen) {
    isDropdownOpen = false
    closeAllDropdowns(DROPDOWN)
  }

  if (!target.closest("[data-form=tweet]")) return

  BUTTON_VALUES.forEach((value) => {
    const selector = `[data-button=${value}]`
    if (target.matches(selector) || target.closest(selector)) console.log(value)
  })

  if (target.matches(DROPDOWN_BUTTON) || target.closest(DROPDOWN_BUTTON)) {
    event.preventDefault()
    console.log("Dropdown!")
    const dropdown = target.closest(DROPDOWN_CONTAINER).querySelector(DROPDOWN)
    isDropdownOpen = true
    openDropdown(dropdown)
  }
}

function closeAllDropdowns(dropdownIdentifier) {
  document.querySelectorAll(dropdownIdentifier).forEach((dropdown) => dropdown.classList.add("is-hidden"))
}

function openDropdown(dropdown) {
  dropdown.classList.remove("is-hidden")
}
