export default async function handleUnlikeTweet(id, target) {
  const unlikeTweet = await requestUnlikeTweet(id)
  // TODO: Validation
  displayUnlike(target)
}

async function requestUnlikeTweet(id) {
  const request = await fetch(`/tweets/${id}/unlike`, {
    method: "DELETE",
  })

  const response = await request

  if (!response.ok) return alert("Could not unlike tweet")
}

function displayUnlike(target) {
  const unlikeButton = target.querySelector("[data-button=unlike]")
  const unlikeCounter = target.querySelector("[data-field=unlike-counter]")
  const likeButton = target.querySelector("[data-button=like")
  const likeCounter = target.querySelector("[data-field=like-counter]")
  const currentLikes = Number(likeCounter.textContent)

  if (currentLikes - 1) {
    unlikeCounter.textContent = currentLikes - 1
    likeCounter.textContent = currentLikes - 1
  } else {
    unlikeCounter.textContent = ""
    likeCounter.textContent = ""
  }

  likeButton.classList.remove("is-hidden")
  unlikeButton.classList.add("is-hidden")
}
