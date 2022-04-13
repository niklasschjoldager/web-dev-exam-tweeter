export default async function handleLikeTweet(id, target) {
  const likeTweet = await requestLikeTweet(id)
  // TODO: Validation
  displayLike(target)
}

async function requestLikeTweet(id) {
  const request = await fetch(`/tweets/${id}/like`, {
    method: "POST",
  })

  const response = await request

  if (!response.ok) return alert("Could not like tweet")

  return response
}

function displayLike(target) {
  const unlikeButton = target.querySelector("[data-button=unlike")
  const unlikeCounter = target.querySelector("[data-field=unlike-counter]")
  const likeButton = target.querySelector("[data-button=like]")
  const likeCounter = target.querySelector("[data-field=like-counter]")
  likeCounter.textContent = Number(likeCounter.textContent) + 1
  unlikeCounter.textContent = Number(unlikeCounter.textContent) + 1
  likeButton.classList.add("is-hidden")
  unlikeButton.classList.remove("is-hidden")
}
