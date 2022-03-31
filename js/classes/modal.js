export default class Modal {
  constructor(modal, target, onOpen = () => {}, onClose = () => {}) {
    this.modal = modal
    this.target = target
    this.openClass = "is-hidden"
    this.onOpen = onOpen
    this.onClose = onClose
    this.openModal = this.openModal.bind(this)
    this.closeModal = this.closeModal.bind(this)
    this.target.addEventListener("click", this.openModal)
    this.closeTriggers = this.modal.querySelectorAll("[data-modal-dismiss]") || null
  }

  openModal() {
    this.modal.classList.remove(this.openClass)
    this.onOpen()
    this.addListeners()
  }

  closeModal() {
    this.modal.classList.add(this.openClass)
    this.onClose()
    this.removeListeners()
  }

  addListeners() {
    this.target.addEventListener("click", this.closeModal)
    this.closeTriggers.forEach((trigger) => trigger.addEventListener("click", this.closeModal))
  }

  removeListeners() {
    this.target.removeEventListener("click", this.closeModal)
    this.closeTriggers.forEach((trigger) => trigger.removeEventListener("click", this.closeModal))
  }
}
