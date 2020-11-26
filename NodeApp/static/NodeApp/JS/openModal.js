console.log("hello")
const setOpenModal = async() => {
    const openButton = document.querySelectorAll(".openModal");
    const modal = document.querySelector(".uploadModal");
    const overlay = modal.querySelector(".modal_Overlay");
    const toggleModal = () => {
        modal.classList.toggle("hidden");
    }
    overlay.addEventListener("click", toggleModal);
    openButton.addEventListener("click", toggleModal);
    console.log(openButton);
  }