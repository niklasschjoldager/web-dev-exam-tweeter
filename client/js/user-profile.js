import handleUnfollowUser from "./users/unfollowUser.js"
import handleFollowUser from "./users/followUser.js"
import handleEditUser from "./users/editUser.js"
import setupImageViewer from "./users/imageViewer.js"
import { enterUnfollowButton, leaveUnfollowButton } from "./users/global.js"

const followButton = document.querySelector("[data-button=follow-user]")
const unfollowButton = document.querySelector("[data-button=unfollow-user]")
const id = document.body.dataset.userId
const username = document.body.dataset.userUsername
const followersField = document.querySelector("[data-field=followers]")
const editProfileButton = document.querySelector("[data-button=edit-user]")

const coverImage = document.querySelector("[data-field=user-cover-image]")
const profileImage = document.querySelector("[data-field=user-profile-image]")
const imagesToView = [coverImage, profileImage]
setupImageViewer(imagesToView)

editProfileButton && editProfileButton.addEventListener("click", () => handleEditUser(id))

if (followButton) {
  followButton.addEventListener("click", async function () {
    await handleFollowUser(id)
    followButton.classList.add("is-hidden")
    unfollowButton.classList.remove("is-hidden")
    const currentFollowers = Number(followersField.textContent)
    followersField.textContent = currentFollowers + 1
  })
}

if (unfollowButton) {
  unfollowButton.addEventListener("mouseenter", () => enterUnfollowButton(unfollowButton))
  unfollowButton.addEventListener("mouseleave", () => leaveUnfollowButton(unfollowButton))
  unfollowButton.addEventListener("click", () => {
    handleUnfollowUser(id, username)
    const currentFollowers = Number(followersField.textContent)
    followersField.textContent = currentFollowers - 1
  })
}
