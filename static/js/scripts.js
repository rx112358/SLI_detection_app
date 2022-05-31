/*!
 * Start Bootstrap - Agency v7.0.10 (https://startbootstrap.com/theme/agency)
 * Copyright 2013-2021 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-agency/blob/master/LICENSE)
 */
//
// Scripts
//

// Check for BlobURL support
var blob = window.URL || window.webkitURL;
if (!blob) {
  console.log("Your browser does not support Blob URLs :(");
}
document.getElementById("file").addEventListener("change", function (event) {
  console.log("change on input#file triggered");
  var file = this.files[0],
    fileURL = blob.createObjectURL(file);

  console.log("File BlobURL: " + fileURL);
  const filename = file.name;
  const filetype = file.type;
  document.getElementById("audio").src = fileURL;
});

function handleSubmit(filename,prediction) {
  document.getElementById("filename").innerHTML = "Filename " +filename;

  if(prediction == 0)
  {document.getElementById("result").innerText = "Result SLI not detected";}
  else
  {document.getElementById("result").innerText = "Result SLI detected";}
}

function modelPredict()
{
  const formData = new FormData();
  const file = document.querySelector('input[type="file"]')
  formData.append('file',file.files[0])
  console.log(file)
  fetch('/model/prediction', {
  method: 'POST',
  body: formData,
  })
  .then(response => response.json())
  .then(data => {
    console.log(data)
  handleSubmit( data["file_name"], data["model_prediction"] )
  console.log('Success:', result);
  })
  .catch((error) => {
  console.error('Error:', error);
  });
  return false;
}

window.addEventListener("DOMContentLoaded", (event) => {
  // Navbar shrink function
  var navbarShrink = function () {
    const navbarCollapsible = document.body.querySelector("#mainNav");
    if (!navbarCollapsible) {
      return;
    }
    if (window.scrollY === 0) {
      navbarCollapsible.classList.remove("navbar-shrink");
    } else {
      navbarCollapsible.classList.add("navbar-shrink");
    }
  };

  // Shrink the navbar
  navbarShrink();

  // Shrink the navbar when page is scrolled
  document.addEventListener("scroll", navbarShrink);

  // Activate Bootstrap scrollspy on the main nav element
  const mainNav = document.body.querySelector("#mainNav");
  if (mainNav) {
    new bootstrap.ScrollSpy(document.body, {
      target: "#mainNav",
      offset: 74,
    });
  }

  // Collapse responsive navbar when toggler is visible
  const navbarToggler = document.body.querySelector(".navbar-toggler");
  const responsiveNavItems = [].slice.call(
    document.querySelectorAll("#navbarResponsive .nav-link")
  );
  responsiveNavItems.map(function (responsiveNavItem) {
    responsiveNavItem.addEventListener("click", () => {
      if (window.getComputedStyle(navbarToggler).display !== "none") {
        navbarToggler.click();
      }
    });
  });
});
