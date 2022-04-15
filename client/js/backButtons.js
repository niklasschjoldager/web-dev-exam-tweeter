export default function handleBackButtons(selector) {
  const backButtons = document.querySelectorAll(selector)
  backButtons.forEach((button) => button.addEventListener("click", () => window.history.back()))
}
