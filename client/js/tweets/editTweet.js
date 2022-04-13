import { handleAddImage, handleRemoveImage } from "./global.js"

export default async function handleEditTweet(id, tweet) {
  const template = document.querySelector("[data-template=modal-edit-tweet]").content.cloneNode(true)
  const modal = template.querySelector("[data-modal=edit-tweet]")
  const editButton = template.querySelector("[data-modal-action=edit-tweet]")
  const dismissButtons = template.querySelectorAll("[data-modal-dismiss]")
  const tweetCopy = getTweet(tweet)
  showTweet(modal, tweetCopy)

  dismissButtons.forEach((button) => button.addEventListener("click", () => modal.remove()))
  editButton.addEventListener("click", async function () {
    await requestEditTweet(id, modal)
    modal.remove()
  })
  prepareActions(modal)
  document.body.append(template)

  modal.querySelector("[data-hook=tweet-text]").focus()
}

function getTweet(tweet) {
  const text = tweet.querySelector("[data-field=text]").textContent
  const image = tweet.querySelector("[data-field=image]")

  return { text, image }
}

function showTweet(modal, tweet) {
  const { text, image } = tweet

  const textField = modal.querySelector("[data-hook=tweet-text]")
  const imageElement = modal.querySelector("[data-hook=tweet-image]")
  const imageContainer = modal.querySelector("[data-hook=tweet-image-container]")
  imageElement.src = image.src

  if (image.classList.contains("is-hidden")) {
    imageContainer.classList.add("is-hidden")
  } else {
    imageContainer.classList.remove("is-hidden")
  }

  textField.value = text
  textField.style.height = ""
  textField.style.height = `${textField.scrollHeight}px`
}

function prepareActions(modal) {
  const buttonAddImage = modal.querySelector("[data-action=add-image]")
  const buttonRemoveImage = modal.querySelector("[data-action=remove-image]")
  const inputAddImage = modal.querySelector("[data-hook=input-tweet-image")
  const tweetImageContainer = modal.querySelector("[data-hook=tweet-image-container]")
  const tweetImage = modal.querySelector("[data-hook=tweet-image]")
  inputAddImage.addEventListener("change", () => handleAddImage(inputAddImage, tweetImage, tweetImageContainer))
  buttonAddImage.addEventListener("click", () => inputAddImage.click())
  buttonRemoveImage.addEventListener("click", () => handleRemoveImage(tweetImage, tweetImageContainer))
}

async function requestEditTweet(id, modal) {
  event.preventDefault()
  const form = modal.querySelector("[data-form=edit-tweet]")
  const formData = new FormData(form)

  if (form.querySelector("[data-hook=tweet-image-container]").classList.contains("is-hidden")) {
    formData.set("tweet_image", null)
  }

  const request = await fetch(`/tweets/${id}`, {
    method: "PUT",
    body: formData,
  })

  const response = await request

  if (!response.ok) return alert("Could not edit tweet")
  const data = await response.json()

  const tweet = document.querySelector(`[data-form="tweet"][data-id="${id}"]`)
  tweet.querySelector("[data-field=text]").textContent = formData.get("tweet_text")
  if (data["tweet_image_file_name"]) {
    tweet.querySelector("[data-field=image]").src = `/static/tweets/${data["tweet_image_file_name"]}`
    tweet.querySelector("[data-field=image]").classList.remove("is-hidden")
  } else {
    tweet.querySelector("[data-field=image]").src = "#"
    tweet.querySelector("[data-field=image]").classList.add("is-hidden")
  }
}
