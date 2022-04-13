import { displayTweet, resetForm, handleAddImage, handleRemoveImage } from "./global.js"

export default function setupCreateTweet(target) {
  const forms = document.querySelectorAll(target)

  forms.forEach((form) => {
    const buttonAddImage = form.querySelector("[data-action=add-image]")
    const buttonRemoveImage = form.querySelector("[data-action=remove-image]")
    const inputAddImage = form.querySelector("[data-hook=input-tweet-image")
    const tweetImageContainer = form.querySelector("[data-hook=tweet-image-container]")
    const tweetImage = form.querySelector("[data-hook=tweet-image]")

    inputAddImage.addEventListener("change", () => handleAddImage(inputAddImage, tweetImage, tweetImageContainer))
    buttonAddImage.addEventListener("click", () => inputAddImage.click())
    buttonRemoveImage.addEventListener("click", () => handleRemoveImage(tweetImage, tweetImageContainer))

    form.addEventListener("submit", handleCreateTweet)
  })
}

async function handleCreateTweet(event) {
  event.preventDefault()
  const form = event.target
  const tweet = await requestCreateTweet(form)
  resetForm(form)
  displayTweet(tweet)
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
