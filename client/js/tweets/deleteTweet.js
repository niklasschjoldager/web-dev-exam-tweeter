export default async function handleDeleteTweet(id, tweet) {
  // TODO: Validate
  const template = document.querySelector("[data-template=modal-delete-tweet]").content.cloneNode(true)
  const modal = template.querySelector("[data-modal=delete-tweet]")
  const deleteButton = template.querySelector("[data-modal-action=delete]")
  const dismissButtons = template.querySelectorAll("[data-modal-dismiss]")

  deleteButton.addEventListener("click", async function () {
    const response = await requestDeleteTweet(id)
    tweet.remove()
    modal.remove()
  })
  dismissButtons.forEach((button) => button.addEventListener("click", () => modal.remove()))

  document.body.append(template)
}

async function requestDeleteTweet(id) {
  const request = await fetch(`/tweets/${id}`, {
    method: "DELETE",
  })

  const response = await request
  if (!response.ok) return alert("Could not delete tweet")

  return response
}
