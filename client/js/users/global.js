import handleUnfollowUser from "./unfollowUser.js"
import handleFollowUser from "./followUser.js"

export function toggleButtons(id, showSelector, hideSelector) {
  const showButtons = document.querySelectorAll(`${showSelector}[data-id="${id}"]`)
  const hideButtons = document.querySelectorAll(`${hideSelector}[data-id="${id}"]`)
  showButtons.forEach((button) => button.classList.remove("is-hidden"))
  hideButtons.forEach((button) => button.classList.add("is-hidden"))
}

export function prepareUser(user) {
  const id = user.dataset.id
  const username = user.dataset.username
  const followButton = user.querySelector("[data-button=follow-user]")
  const unfollowButton = user.querySelector("[data-button=unfollow-user]")

  followButton && followButton.addEventListener("click", () => handleFollowButton(id, followButton, unfollowButton))
  if (unfollowButton) {
    unfollowButton.addEventListener("click", () => {
      event.preventDefault()
      handleUnfollowUser(id, username)
    })
    unfollowButton.addEventListener("mouseenter", () => enterUnfollowButton(unfollowButton))
    unfollowButton.addEventListener("mouseleave", () => leaveUnfollowButton(unfollowButton))
  }
}

async function handleFollowButton(id, followButton, unfollowButton) {
  event.preventDefault()
  await handleFollowUser(id)
  followButton.classList.add("is-hidden")
  unfollowButton.classList.remove("is-hidden")
}

export function enterUnfollowButton(button) {
  button.style.width = `${button.offsetWidth}px`
  button.textContent = "Unfollow"
  button.classList.add("text-danger-200", "border-danger-200", "hover:bg-danger-200/10", "hover:border-danger-200/50")
}

export function leaveUnfollowButton(button) {
  button.textContent = "Following"
  button.classList.remove(
    "text-danger-200",
    "border-danger-200",
    "hover:bg-danger-200/10",
    "hover:border-danger-200/50"
  )
}
