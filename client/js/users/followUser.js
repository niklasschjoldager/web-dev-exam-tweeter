export default async function requestFollowUser(id) {
  const request = await fetch(`/users/${id}/follow`, {
    method: "PUT",
  })

  const response = await request
  if (!response.ok) return alert("Could not follow user")

  return response
}
