export function handleAddImage(input, image, container) {
  const selectedFile = input.files[0]

  if (!selectedFile) {
    container && container.classList.add("is-hidden")
    return
  }

  image.src = URL.createObjectURL(selectedFile)
  container && container.classList.remove("is-hidden")
}

export function handleRemoveImage(image, container) {
  image.src = ""
  container && container.classList.add("is-hidden")
}
