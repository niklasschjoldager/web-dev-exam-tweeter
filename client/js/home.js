import { handleTweetAddImage, handleTweetRemoveImage } from "./global.js"

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
buttonRemoveImage.addEventListener("click", () =>
  handleTweetRemoveImage(inputAddImage, tweetImage, tweetImageContainer)
)

initTweetTextResize()

function initTweetTextResize() {
  const tweetText = document.querySelectorAll("[data-hook=tweet-text]")

  tweetText.forEach((input) => {
    input.style.height = `${input.scrollHeight}px`
    input.addEventListener("input", () => handleTweetTextResize(input))
    window.addEventListener("resize", () => handleTweetTextResize(input))
  })
}

function handleTweetTextResize(input) {
  input.style.height = ""
  input.style.height = `${input.scrollHeight}px`
}

async function handleCreateTweet(event) {
  event.preventDefault()
  const form = event.target
  console.log(new FormData(form))
  console.log(form)
  const request = await fetch("/tweets", {
    method: "POST",
    body: new FormData(form),
  })

  const {
    tweet_id: id,
    tweet_image_file_name: image_file_name,
    tweet_text: text,
    user_username: username,
    user_name: name,
  } = await request.json()

  if (!request.ok) return alert("Could not tweet")
  tweetImageContainer.classList.add("is-hidden")
  tweetImage.src = ""

  form.reset()
  form.elements["tweet_text"].style.height = ""

  const template = QUERIES.templates.tweetItem.content.cloneNode(true)
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
  QUERIES.hooks.tweets.prepend(template)
}
