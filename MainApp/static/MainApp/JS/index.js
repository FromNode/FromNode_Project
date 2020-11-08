const openButton = document.querySelector(".login_Button");
const openButton_Bottom = document.querySelector(".section4Btn");
const modal = document.querySelector(".loginModal");
const overlay = modal.querySelector(".modal_Overlay");
const toggleModal = () => {
    modal.classList.toggle("hidden");
}
overlay.addEventListener("click", toggleModal);
openButton.addEventListener("click", toggleModal);
openButton_Bottom.addEventListener("click", toggleModal);
const goToTop = () => {
    window.scrollTo(0,0);
}