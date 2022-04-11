export default async function setupCreateTweet() {
  const createTweetForms = document.querySelectorAll("[data-form=create-tweet]")

  createTweetForms.forEach((form) => {
    const buttonAddImage = form.querySelector("[data-action=add-image]")
    const buttonRemoveImage = form.querySelector("[data-action=remove-image]")
    const inputAddImage = form.querySelector("[data-hook=input-tweet-image")
    const tweetImageContainer = form.querySelector("[data-hook=tweet-image-container]")
    const tweetImage = form.querySelector("[data-hook=tweet-image]")

    inputAddImage.addEventListener("change", () => handleAddImage(inputAddImage, tweetImage, tweetImageContainer))
    buttonAddImage.addEventListener("click", () => inputAddImage.click())
    buttonRemoveImage.addEventListener("click", () => handleRemoveImage(inputAddImage, tweetImage, tweetImageContainer))

    form.addEventListener("submit", handleCreateTweet)
  })
}

async function handleCreateTweet(event) {
  event.preventDefault()
  const form = event.target
  const tweetData = await requestCreateTweet(form)
  resetForm(form)
  displayTweet(tweetData)
}

async function requestCreateTweet(form) {
  const request = await fetch("/tweets", {
    method: "POST",
    body: new FormData(form),
  })

  const response = await request.json()

  if (!request.ok) return alert("Could not tweet")

  return response
}

function displayTweet(tweetData) {
  const {
    tweet_id: id,
    tweet_image_file_name: image_file_name,
    tweet_text: text,
    user_username: username,
    user_name: name,
  } = tweetData

  const hook = document.querySelector("[data-hook=tweets]")
  const template = document.querySelector("[data-template=tweet-item]").content.cloneNode(true)
  template.querySelector("[data-form=tweet]").setAttribute("data-id", id)
  template.querySelector("[data-field=text]").textContent = text
  template.querySelector("[data-field=username]").href = `/users/${username}`
  template.querySelector("[data-field=username]").textContent = `@${username}`
  template.querySelector("[data-field=name-link]").href = `/users/${username}`
  template.querySelector("[data-field=name]").textContent = name

  if (image_file_name) {
    template.querySelector("[data-field=image]").src = `static/tweets/${image_file_name}`
    template.querySelector("[data-field=image]").classList.remove("is-hidden")
  } else {
    template.querySelector("[data-field=image]").src = "#"
    template.querySelector("[data-field=image]").classList.add("is-hidden")
  }
  hook.prepend(template)
}

function resetForm(form) {
  const tweetImageContainer = form.querySelector("[data-hook=tweet-image-container]")
  const tweetImage = form.querySelector("[data-hook=tweet-image]")
  tweetImageContainer.classList.add("is-hidden")
  tweetImage.src = ""

  form.reset()
  form.elements["tweet_text"].style.height = ""

  const isModal = form.closest("[data-modal]")

  if (isModal) {
    document.body.classList.remove("modal-is-open")
    isModal.classList.add("is-hidden")
  }
}

function handleAddImage(imageInput, image, imageContainer) {
  const selectedFile = imageInput.files[0]

  if (!selectedFile) return imageContainer.classList.add("is-hidden")

  image.src = URL.createObjectURL(selectedFile)
  imageContainer.classList.remove("is-hidden")
}

function handleRemoveImage(image, imageContainer) {
  image.src = ""
  imageContainer.classList.add("is-hidden")
}
