import { displayTweet, resetForm, prepareActions } from "./global.js"

export default function setupCreateTweet(target) {
  const forms = document.querySelectorAll(target)

  forms.forEach((form) => {
    prepareActions(form)
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
