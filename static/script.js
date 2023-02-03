

  function setPreviewImage(file) {
    const fileReader = new FileReader();
    fileReader.readAsDataURL(file);
    fileReader.onload = () => {
        document.querySelector("#imagePreview").src = fileReader.result;
    };
};

const toastLiveExample = document.getElementById('liveToast')

const fileInput = document.querySelector("#inputFile");

fileInput.onchange = function(e) {
    setPreviewImage(fileInput.files[0]);
    const filename = document.querySelector("#filename");
    filename.text = fileInput.files[0].name;
  };

window.addEventListener('load', function() {
    const toast = new bootstrap.Toast(toastLiveExample)
    //toast.show()
})

const dropdown = document.querySelector("#dropdown");

dropdown.addEventListener("click", function() {
    fileInput.click()
})

const btnSubmit = document.getElementById("submit");


btnSubmit.addEventListener("click", function() {
    //document.getElementById("spinner").classList.remove("d-none");
    document.getElementById("upload").click();
    btnSubmit.disabled = true;
    btnSubmit.innerHTML = '<span class="spinner-border spinner-border-sm mx-2" role="status" aria-hidden="true"></span>Loading...'
})


// Execute a function when the user presses a key on the keyboard
window.addEventListener("keypress", function(event) {
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter") {
      // Cancel the default action, if needed
      event.preventDefault();
      // Trigger the button element with a click
      btnSubmit.click();
    }
  });

  //document.getElementById("spinner").classList.remove("d-none");

  document.addEventListener("paste", e => {
    /* the session has shut down */
    if(e.clipboardData.files.length > 0) {
        const fileInput = document.querySelector("#inputFile");
        fileInput.files = e.clipboardData.files;
        setPreviewImage(fileInput.files[0]);
        //const filename = document.querySelector("#filename");
        //filename.text = fileInput.files[0].name;
        btnSubmit.click();
    };

  });

