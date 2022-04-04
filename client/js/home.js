import "./tweets.js"

const QUERIES = {
  forms: {
    createTweet: document.querySelector("[data-form=create-tweet]"),
  },
  hooks: {
    tweets: document.querySelector("[data-hook=tweets]"),
  },
  templates: {
    tweetItem: document.querySelector("[data-template=tweet-item]"),
  },
  modals: {
    deleteTweet: document.querySelector("[data-modal=delete-tweet]"),
    editTweet: document.querySelector("[data-modal=edit-tweet]"),
  },
}

QUERIES.forms.createTweet.addEventListener("submit", handleCreateTweet)
const buttonAddImage = QUERIES.forms.createTweet.querySelector("[data-action=add-image]")
const buttonRemoveImage = QUERIES.forms.createTweet.querySelector("[data-action=remove-image]")
const inputAddImage = QUERIES.forms.createTweet.querySelector("[data-hook=input-tweet-image")
const tweetImageContainer = QUERIES.forms.createTweet.querySelector("[data-hook=tweet-image-container]")
const tweetImage = QUERIES.forms.createTweet.querySelector("[data-hook=tweet-image]")

inputAddImage.addEventListener("change", () => handleTweetAddImage(inputAddImage, tweetImage, tweetImageContainer))
buttonAddImage.addEventListener("click", () => inputAddImage.click())
buttonRemoveImage.addEventListener("click", () => handleTweetRemoveImage(tweetImage, tweetImageContainer))

initTweetTextResize()

function initTweetTextResize() {
  const tweetText = document.querySelector("[data-hook=tweet-text]")
  tweetText.style.height = `${tweetText.scrollHeight}px`
  tweetText.addEventListener("input", handleTweetTextResize)
}

function handleTweetTextResize() {
  this.style.height = ""
  this.style.height = `${this.scrollHeight}px`
}

function handleTweetAddImage(imageInput, image, imageContainer) {
  const selectedFile = imageInput.files[0]

  if (!selectedFile) return imageContainer.classList.add("is-hidden")

  image.src = URL.createObjectURL(selectedFile)
  imageContainer.classList.remove("is-hidden")
}

function handleTweetRemoveImage(image, imageContainer) {
  console.log({ image, imageContainer })
  image.src = ""
  imageContainer.classList.add("is-hidden")
}

async function handleCreateTweet(event) {
  event.preventDefault()
  const form = event.target
  const request = await fetch("/tweets", {
    method: "POST",
    body: new FormData(form),
  })

  const { tweet_id: id, tweet_image_file_name: image_file_name, tweet_text: text } = await request.json()

  if (!request.ok) return alert("Could not tweet")
  tweetImageContainer.classList.add("is-hidden")
  tweetImage.src = ""

  form.reset()

  const template = QUERIES.templates.tweetItem.content.cloneNode(true)
  template.querySelector("[data-form=tweet]").setAttribute("data-id", id)
  template.querySelector("[data-field=text]").textContent = text

  if (image_file_name) {
    template.querySelector("[data-field=image]").src = `static/tweets/${image_file_name}`
    template.querySelector("[data-field=image]").classList.remove("is-hidden")
  } else {
    template.querySelector("[data-field=image]").remove()
  }
  QUERIES.hooks.tweets.prepend(template)

  function showTweetInEdit() {
    const tweetImage = editTweetModal.modal.querySelector("[data-hook=tweet-image]")
    const buttonAddImage = editTweetModal.modal.querySelector("[data-action=add-image]")
    const buttonRemoveImage = editTweetModal.modal.querySelector("[data-action=remove-image]")
    const inputAddImage = editTweetModal.modal.querySelector("[data-hook=input-tweet-image")
    const tweetImageContainer = editTweetModal.modal.querySelector("[data-hook=tweet-image-container]")
    editTweetModal.modal.querySelector("[data-hook=tweet-text]").textContent = text

    if (image_file_name) {
      tweetImage.src = `static/tweets/${image_file_name}`
      tweetImage.classList.remove("is-hidden")
      tweetImageContainer.classList.remove("is-hidden")
    } else {
      tweetImage.remove()
    }

    inputAddImage.addEventListener("change", () => handleTweetAddImage(inputAddImage, tweetImage, tweetImageContainer))
    buttonAddImage.addEventListener("click", () => inputAddImage.click())
    buttonRemoveImage.addEventListener("click", () => handleTweetRemoveImage(tweetImage, tweetImageContainer))
  }
}

async function requestEditTweet(id, modal) {
  event.preventDefault()
  const request = await fetch(`/tweets/${id}`, {
    method: "PUT",
    body: new FormData(QUERIES.modals.editTweet.querySelector("[data-form=edit-tweet]")),
  })

  const response = await request

  if (!response.ok) return alert("Could not edit tweet")

  alert("Ok!")
  modal.closeModal()
}

async function requestDeleteTweet(id, modal) {
  const request = await fetch(`/tweets/${id}`, {
    method: "DELETE",
  })

  const response = await request

  if (!response.ok) return alert("Could not delete tweet")

  QUERIES.hooks.tweets.querySelector(`[data-form="tweet"][data-id="${id}"]`).remove()
  modal.closeModal()
}
