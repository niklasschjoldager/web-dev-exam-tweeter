export function handleAddImage(input, image, container) {
  const selectedFile = input.files[0]

  if (!selectedFile) return container.classList.add("is-hidden")

  image.src = URL.createObjectURL(selectedFile)
  container.classList.remove("is-hidden")
}

export function handleRemoveImage(input, image, container) {
  input.value = ""
  image.src = ""
  container.classList.add("is-hidden")
}
