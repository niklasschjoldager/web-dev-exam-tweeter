export default class Modal {
  constructor(modal, target = null, onAction = null) {
    if (modal instanceof Element) {
      this.modal = modal
    } else {
      this.modal = document.querySelector(modal)
    }
    this.target = target
    this.openClass = "is-hidden"
    this.bodyModalOpenClass = "modal-is-open"
    this.onAction = onAction
    this.openModal = this.openModal.bind(this)
    this.closeModal = this.closeModal.bind(this)
    this.closeTriggers = this.modal.querySelectorAll("[data-modal-dismiss]") || null
    this.actionButton = this.modal.querySelector("[data-modal-action]") || null
    this.target && this.target.addEventListener("click", this.openModal)
  }

  openModal() {
    document.body.classList.add(this.bodyModalOpenClass)
    this.modal.classList.remove(this.openClass)
    this.addListeners()
  }

  closeModal() {
    document.body.classList.remove(this.bodyModalOpenClass)
    this.modal.classList.add(this.openClass)
    this.removeListeners()
  }

  addListeners() {
    this.target && this.target.addEventListener("click", this.closeModal)
    this.closeTriggers.forEach((trigger) => trigger.addEventListener("click", this.closeModal))
    this.actionButton && this.actionButton.addEventListener("click", this.onAction)
  }

  removeListeners() {
    this.target && this.target.removeEventListener("click", this.closeModal)
    this.actionButton && this.actionButton.removeEventListener("click", this.onAction)
    this.closeTriggers.forEach((trigger) => trigger.removeEventListener("click", this.closeModal))
  }
}
