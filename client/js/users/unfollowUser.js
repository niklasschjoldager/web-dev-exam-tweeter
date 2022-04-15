import { toggleButtons } from "./global.js"

export default async function handleUnfollowUser(id, username) {
  const template = document.querySelector("[data-template=modal-unfollow-user]").content.cloneNode(true)
  const modal = template.querySelector("[data-modal=unfollow-user]")
  const usernameField = template.querySelector("[data-field=username]")
  const dismissButtons = template.querySelectorAll("[data-modal-dismiss]")
  const actionButton = template.querySelector("[data-modal-action=unfollow]")

  usernameField.textContent = username
  dismissButtons.forEach((button) => button.addEventListener("click", () => modal.remove()))
  actionButton.addEventListener("click", async function () {
    const response = await requestUnfollowUser(id)
    modal.remove()
    toggleButtons(id, "[data-button=follow]", "[data-button=unfollow]")
    toggleButtons(id, "[data-button=follow-user]", "[data-button=unfollow-user]")
  })

  document.body.append(template)
}

async function requestUnfollowUser(id) {
  const request = await fetch(`/users/${id}/unfollow`, {
    method: "DELETE",
  })

  const response = await request
  if (!response.ok) return alert("Could not unfollow user")

  return response
}
