export default function setupImageViewer(images) {
  images.forEach((image) => image.addEventListener("click", handleImageViewer))
}

function handleImageViewer(event) {
  const image = event.target
  document.body.classList.add("modal-is-open")

  if (image.src == "#") return

  const template = document.querySelector("[data-template=modal-user-image-viewer]").content.cloneNode(true)
  const modal = template.querySelector("[data-modal=user-image-viewer]")
  const imageField = template.querySelector("[data-field=image]")
  const dismissButtons = template.querySelectorAll("[data-modal-dismiss]")
  dismissButtons.forEach((button) =>
    button.addEventListener("click", () => {
      document.body.classList.remove("modal-is-open")
      modal.remove()
    })
  )
  imageField.src = image.src
  document.body.append(template)
}
