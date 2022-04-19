const users = document.querySelectorAll("[data-form=user]")

console.log(users)

// const id = document.body.dataset.userId
// const username = document.body.dataset.userUsername
// const followersField = document.querySelector("[data-field=followers]")

// if (followButton) {
//   followButton.addEventListener("click", async function () {
//     await handleFollowUser(id)
//     followButton.classList.add("is-hidden")
//     unfollowButton.classList.remove("is-hidden")
//     const currentFollowers = Number(followersField.textContent)
//     followersField.textContent = currentFollowers + 1
//   })
// }

// if (unfollowButton) {
//   unfollowButton.addEventListener("mouseenter", () => {
//     unfollowButton.style.width = `${unfollowButton.offsetWidth}px`
//     unfollowButton.textContent = "Unfollow"
//     unfollowButton.classList.add(
//       "text-danger-200",
//       "border-danger-200",
//       "hover:bg-danger-200/10",
//       "hover:border-danger-200/50"
//     )
//   })

//   unfollowButton.addEventListener("mouseleave", () => {
//     unfollowButton.textContent = "Following"
//     unfollowButton.classList.remove(
//       "text-danger-200",
//       "border-danger-200",
//       "hover:bg-danger-200/10",
//       "hover:border-danger-200/50"
//     )
//   })

//   unfollowButton.addEventListener("click", () => {
//     handleUnfollowUser(id, username)
//     const currentFollowers = Number(followersField.textContent)
//     followersField.textContent = currentFollowers - 1
//   })
// }
