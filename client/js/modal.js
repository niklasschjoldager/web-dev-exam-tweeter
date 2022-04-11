const elements = document.querySelectorAll("[data-target][data-action]")
let currentElement = null

elements.forEach((element) => {
  const { target, action } = element.dataset
  if (!target || !action) return
  const targetElement = document.querySelector(`[data-modal=${target}]`)

  element.addEventListener("click", () => {
    if (currentElement && currentElement !== targetElement) currentElement.classList.add("is-hidden")
    currentElement = targetElement

    switch (action) {
      case "toggle":
        if (targetElement.classList.contains("is-hidden")) {
          document.body.classList.add("modal-is-open")
        } else {
          document.body.classList.remove("modal-is-open")
        }
        targetElement.classList.toggle("is-hidden")
        break
      case "open":
        targetElement.classList.remove("is-hidden")
        document.body.classList.add("modal-is-open")
        break
      case "close":
        targetElement.classList.add("is-hidden")
        document.body.classList.remove("modal-is-open")
        break
      default:
        console.log("Action does not exist.")
        return
    }
  })
})
