import { toggleButtons } from "./global.js"

export default async function handleFollowUser(id) {
  await requestFollowUser(id)
  toggleButtons(id, '[data-button="unfollow"]', '[data-button="follow"]')
  toggleButtons(id, '[data-button="unfollow"]', '[data-button="follow"]')
}

async function requestFollowUser(id) {
  const request = await fetch(`/users/${id}/follow`, {
    method: "PUT",
  })

  const response = await request
  if (!response.ok) return alert("Could not follow user")

  return response
}
