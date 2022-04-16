export default function setupMobileMenu(trigger) {
  const triggerButton = document.querySelector(trigger)
  const menu = document.querySelector('[data-menu="mobile"]')

  if (!triggerButton || !menu) return

  const backdrop = menu.querySelector("[data-menu-backdrop]")
  const content = menu.querySelector("[data-menu-content]")
  const closeButtons = menu.querySelectorAll("[data-menu-dismiss]")
  closeButtons.forEach((button) => button.addEventListener("click", closeMenu))

  triggerButton.addEventListener("click", openMenu)

  function openMenu() {
    menu.classList.remove("invisible")
    content.classList.remove("-translate-x-full")
    backdrop.classList.remove("opacity-0")
  }

  function closeMenu() {
    content.classList.add("-translate-x-full")
    backdrop.classList.add("opacity-0")
    backdrop.addEventListener("transitionend", setMenuInvisible)
  }

  function setMenuInvisible() {
    menu.classList.add("invisible")
    backdrop.removeEventListener("transitionend", setMenuInvisible)
  }
}
