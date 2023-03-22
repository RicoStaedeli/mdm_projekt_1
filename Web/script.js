// Get the input element that has the image
const inputElement = document.getElementById("image-input");

// Listen for the "change" event on the input element
inputElement.addEventListener("change", handleFiles, false);

// Define the handleFiles function
function handleFiles() {
    console.log("Try to send the image")
    const fileList = this.files;
    if (!fileList.length) {
        console.log("No file selected");
        return;
    }
    // Create a new FormData object
    const formData = new FormData();

    // Append the image file to the FormData object
    formData.append("image", fileList[0]);

    // Create a new XMLHttpRequest object
    const xhr = new XMLHttpRequest();

    fetch('/upload', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
        },
        body: formData
    }).then(response => response.json())
    .then(data => {
        // Display the text on the HTML page
        const textDiv = document.getElementById("answer");
        console.log(data)
        textDiv.innerHTML = data.generated_caption;})
    
 
}

