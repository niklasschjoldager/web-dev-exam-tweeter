export default function setupInputResize(target) {
  const inputs = document.querySelectorAll(target)

  inputs.forEach((input) => {
    if (input.offsetHeight > 0 || input.offsetWidth > 0) {
      input.style.height = `${input.scrollHeight}px`
    }
    input.addEventListener("input", () => handleInputResize(input))
    window.addEventListener("resize", () => handleInputResize(input))
  })
}

function handleInputResize(input) {
  input.style.height = ""
  input.style.height = `${input.scrollHeight}px`
}
