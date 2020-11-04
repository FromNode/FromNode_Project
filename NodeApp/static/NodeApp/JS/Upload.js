document.querySelectorAll(".drop-zone__input").forEach(inputElement => {
    const dropZoneElement = inputElement.closest(".drop-zone");

    dropZoneElement.addEventListener("click", e => {
        inputElement.click();
    });

    inputElement.addEventListener("change", e =>{
        if (inputElement.files.length) {
            updateThumnail(dropZoneElement, inputElement.files[0]);
        }
    });

    dropZoneElement.addEventListener("dragover", e => {
        e.preventDefault();
        dropZoneElement.classList.add("drop-zone__over")
    });

    ["dragleave", "dragend"].forEach(type =>{
        dropZoneElement.addEventListener(type, e=>{
            dropZoneElement.classList.remove("drop-zone__over");
        })
    })

    dropZoneElement.addEventListener("drop", e => {
        e.preventDefault();
        // console.log(e.dataTransfer.files);
        if (e.dataTransfer.files.length) {
            inputElement.files = e.dataTransfer.files;
            updateThumnail(dropZoneElement, e.dataTransfer.files[0]);
        }
        dropZoneElement.classList.remove("drop-zone__over");
    });
/**
    * @param {HTMLElement} dropZoneElement
    * @param {File} file
    */
    
});
function updateThumnail(dropZoneElement, file){
    let thumnailElement = dropZoneElement.querySelector(".drop-zone__thumb");
    
    //없을때 prompt
    if (dropZoneElement.querySelector(".drop-zone__prompt")) {
        dropZoneElement.querySelector(".drop-zone__prompt").remove();
    }

    //없을때 썸네일
    if(!thumnailElement){
        thumnailElement = document.createElement("div");
        thumnailElement.classList.add("drop-zone__thumb");
        dropZoneElement.appendChild(thumnailElement);
    }

    thumnailElement.dataset.label= file.name;

    
    //썸네일 이미지 
    if(file.type.startsWith("image/")){
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            thumnailElement.style.backgroundImage = `url('${ reader.result }')`;
        };
    } else {
        thumnailElement.style.backgroundImage = null;
    }
}