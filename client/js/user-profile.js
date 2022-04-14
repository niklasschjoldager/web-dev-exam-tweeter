import requestUnfollowUser from "./users/unfollowUser.js"
import requestFollowUser from "./users/followUser.js"

const followButton = document.querySelector("[data-button=follow-user]")
const unfollowButton = document.querySelector("[data-button=unfollow-user]")
const id = document.body.dataset.userId
const username = document.body.dataset.userUsername
const followersField = document.querySelector("[data-field=followers]")

if (unfollowButton) {
  followButton.addEventListener("click", async function () {
    await requestFollowUser(id)
    followButton.classList.add("hidden")
    unfollowButton.classList.remove("hidden")
    const currentFollowers = Number(followersField.textContent)
    followersField.textContent = currentFollowers + 1
  })
}

if (unfollowButton) {
  unfollowButton.addEventListener("mouseenter", () => {
    console.log("enter")
    unfollowButton.style.width = `${unfollowButton.offsetWidth}px`
    unfollowButton.textContent = "Unfollow"
    unfollowButton.classList.add(
      "text-danger-200",
      "border-danger-200",
      "hover:bg-danger-200/10",
      "hover:border-danger-200/50"
    )
  })

  unfollowButton.addEventListener("mouseleave", () => {
    console.log("leave")
    unfollowButton.textContent = "Following"
    unfollowButton.classList.remove(
      "text-danger-200",
      "border-danger-200",
      "hover:bg-danger-200/10",
      "hover:border-danger-200/50"
    )
  })

  unfollowButton.addEventListener("click", () => {
    const template = document.querySelector("[data-template=modal-unfollow-user]").content.cloneNode(true)
    const modal = template.querySelector("[data-modal=unfollow-user]")
    const usernameField = template.querySelector("[data-field=username]")
    const dismissButtons = template.querySelectorAll("[data-modal-dismiss]")
    const actionButton = template.querySelector("[data-modal-action=unfollow]")

    usernameField.textContent = username
    dismissButtons.forEach((button) => button.addEventListener("click", () => modal.remove()))
    actionButton.addEventListener("click", async function () {
      const response = await requestUnfollowUser(id)
      followButton.classList.remove("hidden")
      unfollowButton.classList.add("hidden")
      const currentFollowers = Number(followersField.textContent)
      followersField.textContent = currentFollowers - 1
      modal.remove()
    })

    document.body.append(template)
  })
}

function toggleButtons(openSelector, closeSelector) {
  closeButtons = document.querySelectorAll(closeSelector)
  openButtons = document.querySelectorAll(openSelector)
  closeButtons.forEach((button) => button.classList.add("hidden"))
  openButtons.forEach((button) => button.classList.remove("hidden"))
}
