export default async function requestUnfollowUser(id) {
  const request = await fetch(`/users/${id}/unfollow`, {
    method: "DELETE",
  })

  const response = await request
  if (!response.ok) return alert("Could not unfollow user")

  return response
}
